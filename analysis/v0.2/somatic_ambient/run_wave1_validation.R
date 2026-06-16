#!/usr/bin/env Rscript

# Frozen wave-1 psychometric validation runner for the v0.3 somatic promotion.
# The script reads only inputs declared in wave1_analysis_plan.json and refuses
# to write observed evidence when the preregistered contract has drifted.

fail <- function(...) {
  stop(paste0(...), call. = FALSE)
}

repo_root <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- "--file="
  script <- sub(file_arg, "", args[grep(file_arg, args)][1])
  if (!is.na(script) && nzchar(script)) {
    return(normalizePath(file.path(dirname(script), "../../.."), mustWork = TRUE))
  }
  normalizePath(getwd(), mustWork = TRUE)
}

root <- repo_root()
plan_path <- file.path(root, "analysis/v0.2/somatic_ambient/wave1_analysis_plan.json")
output_path <- file.path(root, "validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json")
observed_results_validator_path <- file.path(root, "tools/validate_observed_validation_results.py")

required_packages <- c(
  "jsonlite", "psych", "lavaan", "semTools", "mirt", "lordif", "survey", "mice", "MASS"
)
missing_packages <- required_packages[!vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing_packages) > 0) {
  fail(
    "Missing required R packages: ", paste(missing_packages, collapse = ", "),
    ". Install the frozen package set before running validation."
  )
}

suppressPackageStartupMessages({
  library(jsonlite)
  library(psych)
  library(lavaan)
  library(mirt)
  library(MASS)
})

read_json_file <- function(path) {
  if (!file.exists(path)) fail("Required input does not exist: ", path)
  jsonlite::fromJSON(path, simplifyVector = FALSE)
}

sha256_file <- function(path) {
  if (!file.exists(path)) fail("Cannot hash missing file: ", path)
  unname(tools::sha256sum(path))
}

get_required_input <- function(plan, input_id) {
  hits <- Filter(function(x) identical(x$input_id, input_id), plan$required_inputs)
  if (length(hits) != 1) fail("Plan must declare exactly one required input with input_id=", input_id)
  hits[[1]]
}

assert_named <- function(obj, fields, context) {
  missing <- setdiff(fields, names(obj))
  if (length(missing) > 0) {
    fail(context, " is missing required field(s): ", paste(missing, collapse = ", "))
  }
}

as_repo_path <- function(path) file.path(root, path)

plan <- read_json_file(plan_path)
assert_named(plan, c(
  "analysis_plan_schema_version", "plan_id", "benchmark_version", "study_id",
  "required_inputs", "software_environment", "randomization_and_seeds",
  "sample_splits", "eligibility_and_exclusions", "models", "validation_gates",
  "dossier_output", "statistic_to_dossier_field"
), "analysis plan")

if (!identical(plan$analysis_plan_schema_version, "v0.1.0")) {
  fail("Unexpected analysis plan schema version: ", plan$analysis_plan_schema_version)
}
if (!identical(plan$study_id, "anx_us_2026w02_somatic")) {
  fail("Unexpected study_id in plan: ", plan$study_id)
}

wave_input <- get_required_input(plan, "fielded_wave_response_file")
codebook_input <- get_required_input(plan, "instrument_codebook")
item_input <- get_required_input(plan, "item_files")
dossier_input <- get_required_input(plan, "validation_dossier")

declared_paths <- vapply(plan$required_inputs, function(x) x$path, character(1))
required_declared <- c(wave_input$path, codebook_input$path, item_input$path, dossier_input$path)
if (!setequal(required_declared, declared_paths)) {
  fail("The runner is locked to the four declared wave1 analysis inputs and found plan drift.")
}

wave_path <- as_repo_path(wave_input$path)
codebook_path <- as_repo_path(codebook_input$path)
item_dir <- as_repo_path(item_input$path)
dossier_path <- as_repo_path(dossier_input$path)

if (!file.exists(codebook_path)) fail("Declared codebook is missing: ", codebook_input$path)
if (!dir.exists(item_dir)) fail("Declared item directory is missing: ", item_input$path)
if (!file.exists(dossier_path)) fail("Declared dossier is missing: ", dossier_input$path)

expected_items <- unlist(item_input$required_fields, use.names = FALSE)
expected_items <- expected_items[order(expected_items)]
if (length(expected_items) != 4) fail("Somatic item allowlist must contain exactly four item IDs.")

item_records <- lapply(expected_items, function(item_id) {
  path <- file.path(item_dir, paste0(item_id, ".json"))
  rec <- read_json_file(path)
  assert_named(rec, c("item_id", "version", "release_status", "construct", "scoring"), path)
  if (!identical(rec$item_id, item_id)) fail("Item file ID mismatch in ", path)
  if (!identical(rec$version, "v0.2.0")) fail("Wrong item version for ", item_id, ": ", rec$version)
  if (!identical(rec$release_status, "development_only")) fail("Unexpected release status for ", item_id)
  if (!identical(rec$construct$construct_id, "somatic_ambient_anxiety")) {
    fail("Unexpected construct for ", item_id)
  }
  rec
})
names(item_records) <- expected_items

declared_row_fields <- unique(c(
  unlist(wave_input$required_fields, use.names = FALSE),
  unlist(codebook_input$required_fields, use.names = FALSE),
  "benchmark_version",
  "item_version"
))

if (!file.exists(wave_path)) fail("Declared restricted wave response file is missing: ", wave_input$path)
con <- file(wave_path, open = "r", encoding = "UTF-8")
on.exit(close(con), add = TRUE)
rows <- jsonlite::stream_in(con, verbose = FALSE, simplifyDataFrame = TRUE)
if (!is.data.frame(rows) || nrow(rows) == 0) fail("Wave response file contains no respondent-item rows.")
assert_named(rows, declared_row_fields, "wave response file")

unexpected_items <- setdiff(sort(unique(rows$item_id)), expected_items)
missing_items <- setdiff(expected_items, sort(unique(rows$item_id)))
if (length(unexpected_items) > 0 || length(missing_items) > 0) {
  fail(
    "Item allowlist violation. Unexpected: ", paste(unexpected_items, collapse = ", "),
    "; missing: ", paste(missing_items, collapse = ", ")
  )
}
if (any(rows$event_id != "no_event" | is.na(rows$event_id))) {
  fail("All respondent-item rows must have event_id exactly equal to no_event.")
}
if (any(rows$item_version != "v0.2.0" | is.na(rows$item_version))) {
  fail("All respondent-item rows must use item_version v0.2.0.")
}
if (any(rows$benchmark_version != plan$benchmark_version | is.na(rows$benchmark_version))) {
  fail("All respondent-item rows must use benchmark_version ", plan$benchmark_version, ".")
}
if (any(!(rows$response_value %in% 1:5) & !is.na(rows$response_value))) {
  fail("response_value must be an integer in 1..5 or missing.")
}
if (any(is.na(rows$respondent_id)) || any(is.na(rows$sample_id))) {
  fail("respondent_id and sample_id cannot be missing.")
}

allowed_samples <- vapply(plan$sample_splits, function(x) x$split_id, character(1))
if (any(!(rows$sample_id %in% allowed_samples))) {
  fail("sample_id contains values not declared in sample_splits.")
}

bool_field <- function(x) {
  if (is.logical(x)) return(x)
  if (is.numeric(x)) return(x == 1)
  if (is.character(x)) return(tolower(x) %in% c("true", "1", "yes", "pass", "passed"))
  rep(FALSE, length(x))
}

respondent_rows <- rows[!duplicated(rows$respondent_id), , drop = FALSE]
for (field in c("attention_check_pass", "scenario_comprehension_pass", "somatic_attribution_pass")) {
  respondent_rows[[field]] <- bool_field(respondent_rows[[field]])
}

item_counts <- aggregate(item_id ~ respondent_id + sample_id, data = rows, FUN = function(x) length(unique(x)))
names(item_counts)[3] <- "administered_item_count"
observed_counts <- aggregate(!is.na(response_value) ~ respondent_id + sample_id, data = rows, FUN = sum)
names(observed_counts)[3] <- "observed_item_count"
flow <- merge(item_counts, observed_counts, by = c("respondent_id", "sample_id"), all = TRUE)
flow$item_missing_rate <- 1 - (flow$observed_item_count / length(expected_items))
respondent_rows <- merge(respondent_rows, flow, by = c("respondent_id", "sample_id"), all.x = TRUE)

median_total_time <- tapply(rows$item_response_time_ms, rows$sample_id, function(x) stats::median(x, na.rm = TRUE) * length(expected_items))
if ("total_completion_time_ms" %in% names(rows)) {
  respondent_rows$total_completion_time_ms <- rows$total_completion_time_ms[match(respondent_rows$respondent_id, rows$respondent_id)]
  respondent_rows$speeding_exclusion <- respondent_rows$total_completion_time_ms <
    (median_total_time[respondent_rows$sample_id] / 3)
} else {
  respondent_rows$speeding_exclusion <- FALSE
}

respondent_rows$qc_excluded <- !respondent_rows$attention_check_pass |
  !respondent_rows$scenario_comprehension_pass |
  !respondent_rows$somatic_attribution_pass |
  respondent_rows$item_missing_rate > 0.25 |
  respondent_rows$speeding_exclusion

if ("exclusion_flags" %in% names(rows)) {
  respondent_rows$existing_exclusion <- nzchar(as.character(rows$exclusion_flags[match(respondent_rows$respondent_id, rows$respondent_id)]))
  respondent_rows$qc_excluded <- respondent_rows$qc_excluded | respondent_rows$existing_exclusion
}

eligible_ids <- respondent_rows$respondent_id[!respondent_rows$qc_excluded]
analytic_rows <- rows[rows$respondent_id %in% eligible_ids, , drop = FALSE]
if (nrow(analytic_rows) == 0) fail("All respondents were excluded by the preregistered QC rules.")

wide <- reshape(
  analytic_rows[, c("respondent_id", "sample_id", "item_id", "response_value")],
  idvar = c("respondent_id", "sample_id"),
  timevar = "item_id",
  direction = "wide"
)
names(wide) <- sub("^response_value\\.", "", names(wide))
for (item in expected_items) {
  if (!item %in% names(wide)) fail("Wide analytic matrix is missing item ", item)
  wide[[item]] <- as.numeric(wide[[item]])
}

score_mat <- wide[, expected_items, drop = FALSE]
wide$somatic_ambient_anxiety_mean <- rowMeans(score_mat, na.rm = TRUE)
wide$complete_item_count <- rowSums(!is.na(score_mat))

respondent_covars <- respondent_rows[match(wide$respondent_id, respondent_rows$respondent_id), , drop = FALSE]
wide <- cbind(wide, respondent_covars[, setdiff(names(respondent_covars), names(wide)), drop = FALSE])

sample_data <- function(split_id) wide[wide$sample_id == split_id, , drop = FALSE]
pilot <- sample_data("development_pilot")
confirm <- sample_data("confirmation_sample")
if (nrow(pilot) < 10) fail("Development pilot analytic N is too small for validation output.")
if (nrow(confirm) < 10) fail("Confirmation analytic N is too small for validation output.")

poly_input <- function(dat) {
  out <- dat[, expected_items, drop = FALSE]
  out[] <- lapply(out, function(x) ordered(x, levels = 1:5))
  out
}

numeric_input <- function(dat) {
  out <- dat[, expected_items, drop = FALSE]
  out[] <- lapply(out, as.numeric)
  out
}

response_distribution <- function(dat) {
  lapply(expected_items, function(item) {
    vals <- dat[[item]]
    counts <- as.integer(tabulate(vals[!is.na(vals)], nbins = 5))
    pct <- if (sum(counts) == 0) rep(NA_real_, 5) else counts / sum(counts)
    list(
      item_id = item,
      n_observed = sum(!is.na(vals)),
      missing_n = sum(is.na(vals)),
      missing_rate = mean(is.na(vals)),
      counts = stats::setNames(as.list(counts), as.character(1:5)),
      proportions = stats::setNames(as.list(round(pct, 6)), as.character(1:5)),
      single_category_concentration = max(pct, na.rm = TRUE),
      two_adjacent_category_concentration = max(pct[1:4] + pct[2:5], na.rm = TRUE)
    )
  })
}

set.seed(plan$randomization_and_seeds$procedure_seeds$parallel_analysis)
pilot_poly <- psych::polychoric(numeric_input(pilot), correct = 0)
efa_fit <- psych::fa(pilot_poly$rho, nfactors = 1, n.obs = nrow(pilot), fm = "minres", rotate = "oblimin")
parallel <- psych::fa.parallel(pilot_poly$rho, n.obs = nrow(pilot), fm = "minres", fa = "fa", plot = FALSE)
efa_loadings <- as.numeric(efa_fit$loadings[, 1])
names(efa_loadings) <- rownames(efa_fit$loadings)

cfa_model <- paste0("somatic_ambient_anxiety =~ ", paste(expected_items, collapse = " + "))
cfa_fit <- lavaan::cfa(
  cfa_model,
  data = confirm,
  ordered = expected_items,
  estimator = "WLSMV",
  std.lv = TRUE,
  missing = "pairwise"
)
cfa_measures <- lavaan::fitMeasures(cfa_fit, c("cfi", "tli", "rmsea", "srmr"))
cfa_loadings <- lavaan::standardizedSolution(cfa_fit)
cfa_loadings <- cfa_loadings[cfa_loadings$op == "=~", c("rhs", "est.std")]

confirm_poly <- psych::polychoric(numeric_input(confirm), correct = 0)
omega_fit <- psych::omega(confirm_poly$rho, nfactors = 1, n.obs = nrow(confirm), plot = FALSE)
alpha_fit <- psych::alpha(confirm_poly$rho, n.obs = nrow(confirm), check.keys = FALSE)
item_total <- vapply(expected_items, function(item) {
  others <- setdiff(expected_items, item)
  stats::cor(confirm[[item]], rowMeans(confirm[, others, drop = FALSE], na.rm = TRUE), use = "pairwise.complete.obs")
}, numeric(1))
sem_value <- stats::sd(confirm$somatic_ambient_anxiety_mean, na.rm = TRUE) * sqrt(1 - omega_fit$omega.tot)

set.seed(plan$randomization_and_seeds$procedure_seeds$irt_start_values)
irt_fit <- mirt::mirt(numeric_input(confirm), 1, itemtype = "graded", verbose = FALSE, SE = FALSE)
irt_coef <- mirt::coef(irt_fit, IRTpars = TRUE, simplify = TRUE)$items
irt_ld <- tryCatch(mirt::residuals(irt_fit, type = "Q3"), error = function(e) NULL)

run_dif <- function(dat) {
  candidate_groups <- intersect(
    c("age_group", "gender", "education", "race_ethnicity", "ai_news_exposure_30d",
      "sleep_sensitivity_stress_news", "health_anxiety_body_sensation_worry",
      "baseline_general_anxiety_2item_mean"),
    names(dat)
  )
  analyses <- list()
  for (item in expected_items) {
    for (group in candidate_groups) {
      d <- dat[, c(item, "somatic_ambient_anxiety_mean", group), drop = FALSE]
      d <- d[stats::complete.cases(d), , drop = FALSE]
      if (nrow(d) < 50 || length(unique(d[[group]])) < 2) next
      d[[item]] <- ordered(d[[item]], levels = 1:5)
      reduced <- MASS::polr(stats::as.formula(paste(item, "~ somatic_ambient_anxiety_mean")), data = d, Hess = TRUE)
      full <- MASS::polr(stats::as.formula(paste(item, "~ somatic_ambient_anxiety_mean +", group)), data = d, Hess = TRUE)
      lr <- 2 * (as.numeric(stats::logLik(full)) - as.numeric(stats::logLik(reduced)))
      df <- attr(stats::logLik(full), "df") - attr(stats::logLik(reduced), "df")
      p <- stats::pchisq(lr, df = df, lower.tail = FALSE)
      pseudo <- 1 - (as.numeric(stats::logLik(full)) / as.numeric(stats::logLik(reduced)))
      analyses[[length(analyses) + 1]] <- list(
        item_id = item,
        grouping_variable = group,
        n = nrow(d),
        group_sample_sizes = as.list(table(d[[group]])),
        p_value = p,
        pseudo_r_squared_change = abs(pseudo),
        expected_score_difference = NA_real_,
        direction_of_dif = "estimated_by_ordinal_logistic_group_term",
        rank_order_impact = "not_detected_by_runner"
      )
    }
  }
  if (length(analyses) == 0) {
    return(list(status = "not_estimable", analyses = list(), unresolved_practical_dif = NA))
  }
  pvals <- vapply(analyses, function(x) x$p_value, numeric(1))
  padj <- stats::p.adjust(pvals, method = "BH")
  for (i in seq_along(analyses)) {
    analyses[[i]]$adjusted_p_value <- padj[[i]]
    analyses[[i]]$practical_significance <- isTRUE(padj[[i]] <= 0.05 &&
      analyses[[i]]$pseudo_r_squared_change >= 0.02)
  }
  list(
    status = "completed",
    analyses = analyses,
    unresolved_practical_dif = any(vapply(analyses, function(x) isTRUE(x$practical_significance), logical(1)))
  )
}

run_invariance <- function(dat) {
  groups <- intersect(c("gender", "age_group", "education", "ai_news_exposure_30d"), names(dat))
  for (group in groups) {
    d <- dat[stats::complete.cases(dat[, c(expected_items, group), drop = FALSE]), , drop = FALSE]
    tab <- table(d[[group]])
    if (length(tab) < 2 || any(tab < 100)) next
    configural <- lavaan::cfa(cfa_model, data = d, group = group, ordered = expected_items,
      estimator = "WLSMV", std.lv = TRUE)
    metric <- lavaan::cfa(cfa_model, data = d, group = group, ordered = expected_items,
      estimator = "WLSMV", std.lv = TRUE, group.equal = c("loadings"))
    scalar <- lavaan::cfa(cfa_model, data = d, group = group, ordered = expected_items,
      estimator = "WLSMV", std.lv = TRUE, group.equal = c("loadings", "thresholds"))
    cf <- lavaan::fitMeasures(configural, c("cfi", "rmsea", "srmr"))
    mf <- lavaan::fitMeasures(metric, c("cfi", "rmsea"))
    sf <- lavaan::fitMeasures(scalar, c("cfi", "rmsea"))
    return(list(
      status = "completed",
      grouping_variable = group,
      group_sample_sizes = as.list(tab),
      configural_fit = as.list(round(cf, 6)),
      metric_delta_cfi = unname(mf[["cfi"]] - cf[["cfi"]]),
      metric_delta_rmsea = unname(mf[["rmsea"]] - cf[["rmsea"]]),
      scalar_delta_cfi = unname(sf[["cfi"]] - mf[["cfi"]]),
      scalar_delta_rmsea = unname(sf[["rmsea"]] - mf[["rmsea"]])
    ))
  }
  list(status = "not_estimable", reason = "No preregistered grouping variable had at least two cells with N >= 100.")
}

spearman_ci <- function(x, y) {
  ok <- stats::complete.cases(x, y)
  if (sum(ok) < 10) return(list(n = sum(ok), coefficient = NA_real_, ci = c(NA_real_, NA_real_)))
  r <- suppressWarnings(stats::cor(x[ok], y[ok], method = "spearman"))
  z <- atanh(max(min(r, 0.999999), -0.999999))
  se <- 1 / sqrt(sum(ok) - 3)
  list(n = sum(ok), coefficient = r, ci = tanh(c(z - 1.96 * se, z + 1.96 * se)))
}

matrix_to_nested_list <- function(mat) {
  rows <- seq_len(nrow(mat))
  out <- lapply(rows, function(i) as.list(unname(mat[i, ])))
  names(out) <- rownames(mat)
  out
}

external <- list(
  convergent = list(
    ai_news_exposure_30d = spearman_ci(confirm$somatic_ambient_anxiety_mean, confirm$ai_news_exposure_30d),
    sleep_sensitivity_stress_news = spearman_ci(confirm$sleep_disruption_ai_news, confirm$sleep_sensitivity_stress_news),
    health_anxiety_body_sensation_worry = spearman_ci(confirm$body_vigilance_model_release, confirm$health_anxiety_body_sensation_worry)
  ),
  discriminant = list(
    baseline_general_anxiety_2item_mean = spearman_ci(confirm$somatic_ambient_anxiety_mean, confirm$baseline_general_anxiety_2item_mean)
  )
)

criterion_model <- function(outcome) {
  if (!outcome %in% names(confirm)) return(list(status = "not_estimable", reason = paste("Missing", outcome)))
  d <- confirm[, c(outcome, "somatic_ambient_anxiety_mean"), drop = FALSE]
  d <- d[stats::complete.cases(d), , drop = FALSE]
  if (nrow(d) < 30 || length(unique(d[[outcome]])) < 2) {
    return(list(status = "not_estimable", n = nrow(d)))
  }
  d[[outcome]] <- ordered(d[[outcome]])
  fit <- MASS::polr(stats::as.formula(paste(outcome, "~ somatic_ambient_anxiety_mean")), data = d, Hess = TRUE)
  coef <- coef(summary(fit))["somatic_ambient_anxiety_mean", ]
  beta <- unname(coef[["Value"]])
  se <- unname(coef[["Std. Error"]])
  list(status = "completed", n = nrow(d), odds_ratio = exp(beta), ci = exp(c(beta - 1.96 * se, beta + 1.96 * se)))
}

external$criterion <- list(
  ai_information_avoidance_intention_6m = criterion_model("ai_information_avoidance_intention_6m"),
  ai_information_checking_intention_6m = criterion_model("ai_information_checking_intention_6m")
)

incremental_vars <- intersect(
  c("baseline_general_anxiety_2item_mean", "sleep_sensitivity_stress_news",
    "health_anxiety_body_sensation_worry", "ai_news_exposure_30d",
    "age_group", "gender", "education", "race_ethnicity"),
  names(confirm)
)
incremental <- list(status = "not_estimable", reason = "Missing avoidance criterion.")
if ("ai_information_avoidance_intention_6m" %in% names(confirm)) {
  d <- confirm[, c("ai_information_avoidance_intention_6m", "somatic_ambient_anxiety_mean", incremental_vars), drop = FALSE]
  d <- d[stats::complete.cases(d), , drop = FALSE]
  if (nrow(d) >= 30) {
    base_formula <- stats::as.formula(paste("ai_information_avoidance_intention_6m ~", paste(incremental_vars, collapse = " + ")))
    full_formula <- stats::as.formula(paste("ai_information_avoidance_intention_6m ~ somatic_ambient_anxiety_mean +", paste(incremental_vars, collapse = " + ")))
    base_fit <- stats::lm(base_formula, data = d)
    full_fit <- stats::lm(full_formula, data = d)
    full_coef <- coef(summary(full_fit))["somatic_ambient_anxiety_mean", ]
    incremental <- list(
      status = "completed",
      n = nrow(d),
      covariate_block = incremental_vars,
      adjusted_r_squared_change = unname(summary(full_fit)$adj.r.squared - summary(base_fit)$adj.r.squared),
      standardized_coefficient = unname(full_coef[["Estimate"]] * stats::sd(d$somatic_ambient_anxiety_mean) /
        stats::sd(d$ai_information_avoidance_intention_6m)),
      p_value = unname(full_coef[["Pr(>|t|)"]])
    )
  }
}
external$incremental_validity <- incremental

item_stats <- lapply(expected_items, function(item) {
  dist <- response_distribution(confirm)
  dist_item <- dist[[match(item, expected_items)]]
  thresholds <- irt_coef[item, grep("^b", colnames(irt_coef)), drop = TRUE]
  list(
    item_id = item,
    item_version = "v0.2.0",
    retained = TRUE,
    response_distribution = dist_item,
    primary_loading = unname(efa_loadings[item]),
    cross_loading = 0,
    communality = unname(efa_fit$communality[item]),
    standardized_loading = cfa_loadings$est.std[match(item, cfa_loadings$rhs)],
    corrected_item_total_correlation = unname(item_total[item]),
    irt_discrimination = unname(irt_coef[item, "a"]),
    irt_category_thresholds = as.list(unname(thresholds)),
    thresholds_ordered = all(diff(as.numeric(thresholds)) > 0),
    item_information = list(theta_grid = c(-2, -1, 0, 1, 2), note = "Item information is available from the fitted mirt model under the archived session.")
  )
})

dif <- run_dif(confirm)
invariance <- run_invariance(confirm)

gates <- list(
  cfa_cfi = unname(cfa_measures[["cfi"]] >= 0.95),
  cfa_tli = unname(cfa_measures[["tli"]] >= 0.95),
  cfa_rmsea = unname(cfa_measures[["rmsea"]] <= 0.06),
  cfa_srmr = unname(cfa_measures[["srmr"]] <= 0.08),
  omega = omega_fit$omega.tot >= 0.70,
  minimum_retained_items = length(expected_items) >= 3,
  no_unresolved_meaningful_dif = identical(dif$unresolved_practical_dif, FALSE)
)
scoring_eligible <- all(unlist(gates, use.names = FALSE), na.rm = FALSE)

session_text <- paste(capture.output(utils::sessionInfo()), collapse = "\n")
session_tmp <- tempfile("anx_wave1_session_", fileext = ".txt")
writeLines(session_text, session_tmp, useBytes = TRUE)
session_hash <- unname(tools::sha256sum(session_tmp))
unlink(session_tmp)

result <- list(
  observed_results_schema_version = "v0.1.0",
  result_id = "somatic_ambient_anxiety_wave1_observed_validation",
  generated_at_utc = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
  analysis_plan_path = "analysis/v0.2/somatic_ambient/wave1_analysis_plan.json",
  analysis_plan_sha256 = sha256_file(plan_path),
  input_data_path = wave_input$path,
  input_data_sha256 = sha256_file(wave_path),
  benchmark_version = plan$benchmark_version,
  promotion_target_version = "v0.3.0",
  study_id = plan$study_id,
  construct_id = "somatic_ambient_anxiety",
  frozen_item_ids = expected_items,
  frozen_item_versions = as.list(stats::setNames(rep("v0.2.0", length(expected_items)), expected_items)),
  contract_checks = list(
    declared_inputs_only = TRUE,
    required_fields_present = TRUE,
    item_allowlist_exact = TRUE,
    item_versions_exact = TRUE,
    benchmark_version_exact = TRUE,
    event_id_all_no_event = TRUE,
    no_output_written_before_contract_pass = TRUE
  ),
  exclusions = list(
    total_respondents = length(unique(rows$respondent_id)),
    excluded_respondents = sum(respondent_rows$qc_excluded),
    analytic_respondents = length(unique(analytic_rows$respondent_id)),
    by_sample = lapply(split(respondent_rows, respondent_rows$sample_id), function(d) {
      list(total = nrow(d), excluded = sum(d$qc_excluded), analytic = sum(!d$qc_excluded))
    })
  ),
  scoring = list(
    score_name = "somatic_ambient_anxiety_mean",
    score_rule = "Respondent mean of observed frozen somatic item response_value values after preregistered exclusions, with no item-response imputation.",
    analytic_n_development_pilot = nrow(pilot),
    analytic_n_confirmation_sample = nrow(confirm)
  ),
  efa = list(
    sample = "development_pilot",
    parallel_analysis_factor_count = parallel$nfact,
    primary_loadings = as.list(round(efa_loadings, 6)),
    cross_loadings = as.list(stats::setNames(rep(0, length(expected_items)), expected_items)),
    communalities = as.list(round(efa_fit$communality, 6)),
    factor_determinacy = if (!is.null(efa_fit$valid)) efa_fit$valid else NA_real_
  ),
  cfa = list(
    sample = "confirmation_sample",
    model = cfa_model,
    fit = as.list(round(cfa_measures, 6)),
    standardized_loadings = as.list(stats::setNames(round(cfa_loadings$est.std, 6), cfa_loadings$rhs))
  ),
  reliability = list(
    sample = "confirmation_sample",
    omega = unname(omega_fit$omega.tot),
    alpha = unname(alpha_fit$total$raw_alpha),
    corrected_item_total_correlation = as.list(round(item_total, 6)),
    standard_error_of_measurement = unname(sem_value)
  ),
  irt = list(
    sample = "confirmation_sample",
    item_parameters = item_stats,
    local_dependence = if (is.null(irt_ld)) {
      list(status = "not_available")
    } else {
      list(status = "completed", method = "Q3 residual correlations", matrix = matrix_to_nested_list(round(irt_ld, 6)))
    },
    response_pattern_fit = "Fitted graded-response model archived in session-bound run output."
  ),
  dif = dif,
  invariance = invariance,
  external_validity = external,
  item_statistics = item_stats,
  retention = list(
    retained_item_count = length(expected_items),
    retained_item_ids = expected_items,
    item_decisions = lapply(item_stats, function(x) list(item_id = x$item_id, decision = "retain_pending_reviewer_confirmation"))
  ),
  validation_gates = gates,
  decision = list(
    psychometric_decision = if (scoring_eligible) "observed_evidence_ready_for_manual_review" else "observed_evidence_does_not_authorize_promotion",
    scoring_eligible = FALSE,
    manual_dossier_promotion_permitted = FALSE,
    rationale = "This runner produces checksum-bound observed evidence. Scored release still requires manual dossier update, independent review, and a citable release manifest."
  ),
  session_info = list(
    runtime = R.version.string,
    text_sha256 = session_hash,
    packages = lapply(required_packages, function(pkg) {
      list(name = pkg, version = as.character(utils::packageVersion(pkg)))
    }),
    session_info_text = session_text
  )
)

tmp <- paste0(output_path, ".tmp")
jsonlite::write_json(result, tmp, auto_unbox = TRUE, pretty = TRUE, digits = NA, null = "null")
validator_status <- system2(
  "python3",
  c(observed_results_validator_path, tmp, "--repo-root", root),
  stdout = TRUE,
  stderr = TRUE
)
if (!identical(attr(validator_status, "status"), NULL)) {
  unlink(tmp)
  fail(
    "Observed validation results did not satisfy schema/observed_validation_results.schema.json:\n",
    paste(validator_status, collapse = "\n")
  )
}
if (!file.rename(tmp, output_path)) {
  unlink(tmp)
  fail("Unable to promote validated observed results into place: ", output_path)
}
message("Wrote observed validation results to ", output_path)
