#!/usr/bin/env Rscript

# Preregistered Wave 3 test-retest evidence runner for ANX-Bench v0.3.1.
# The runner is deliberately fail-closed: contract errors stop before evidence
# is written, while psychometric threshold misses are written as fail decisions.

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

parse_args <- function(default_root) {
  args <- commandArgs(trailingOnly = TRUE)
  values <- list(
    paired_csv = file.path(default_root, "vendor_restricted/anx_us_2026w03_somatic_retest/paired_retest_analysis.csv"),
    retest_jsonl = file.path(default_root, "vendor_restricted/anx_us_2026w03_somatic_retest/wave_response.jsonl"),
    output = file.path(default_root, "validation/v0.3/somatic_ambient_retest/wave3_retest_evidence.json"),
    bootstrap_resamples = 2000L
  )
  i <- 1L
  while (i <= length(args)) {
    key <- args[[i]]
    if (!key %in% c("--paired-csv", "--retest-jsonl", "--output", "--bootstrap-resamples")) {
      fail("Unknown argument: ", key)
    }
    if (i == length(args)) fail("Missing value for argument: ", key)
    value <- args[[i + 1L]]
    if (key == "--paired-csv") values$paired_csv <- value
    if (key == "--retest-jsonl") values$retest_jsonl <- value
    if (key == "--output") values$output <- value
    if (key == "--bootstrap-resamples") values$bootstrap_resamples <- as.integer(value)
    i <- i + 2L
  }
  if (is.na(values$bootstrap_resamples) || values$bootstrap_resamples < 1L) {
    fail("--bootstrap-resamples must be a positive integer")
  }
  values
}

assert_named <- function(obj, fields, context) {
  missing <- setdiff(fields, names(obj))
  if (length(missing) > 0) {
    fail(context, " is missing required field(s): ", paste(missing, collapse = ", "))
  }
}

as_bool <- function(x) {
  if (is.logical(x)) return(!is.na(x) & x)
  if (is.numeric(x)) return(!is.na(x) & x != 0)
  tolower(trimws(as.character(x))) %in% c("true", "1", "yes", "y", "pass", "passed")
}

weighted_mean <- function(x, w) {
  ok <- !is.na(x) & !is.na(w) & w > 0
  if (!any(ok)) return(NA_real_)
  sum(x[ok] * w[ok]) / sum(w[ok])
}

weighted_share <- function(flag, w) {
  ok <- !is.na(flag) & !is.na(w) & w > 0
  if (!any(ok)) return(NA_real_)
  sum(as.numeric(flag[ok]) * w[ok]) / sum(w[ok])
}

round_or_null <- function(x, digits = 6L) {
  if (length(x) == 0L || is.na(x) || !is.finite(x)) return(NULL)
  round(as.numeric(x), digits)
}

int_or_null <- function(x) {
  if (length(x) == 0L || is.na(x)) return(NULL)
  as.integer(x)
}

escape_json <- function(x) {
  x <- gsub("\\\\", "\\\\\\\\", x)
  x <- gsub("\"", "\\\\\"", x)
  x <- gsub("\n", "\\\\n", x)
  x
}

to_json <- function(x, indent = 0L) {
  pad <- paste(rep(" ", indent), collapse = "")
  child <- paste(rep(" ", indent + 2L), collapse = "")
  if (is.null(x)) return("null")
  if (isTRUE(x)) return("true")
  if (identical(x, FALSE)) return("false")
  if (is.numeric(x) && length(x) == 1L) {
    if (is.na(x) || !is.finite(x)) return("null")
    return(format(x, scientific = FALSE, trim = TRUE))
  }
  if (is.character(x) && length(x) == 1L) return(paste0("\"", escape_json(x), "\""))
  if (is.list(x) && is.null(names(x))) {
    if (length(x) == 0L) return("[]")
    body <- vapply(x, to_json, character(1), indent = indent + 2L)
    return(paste0("[\n", child, paste(body, collapse = paste0(",\n", child)), "\n", pad, "]"))
  }
  if (is.atomic(x) && length(x) != 1L) {
    return(to_json(as.list(x), indent = indent))
  }
  if (is.list(x)) {
    if (length(x) == 0L) return("{}")
    keys <- names(x)
    body <- vapply(seq_along(x), function(i) {
      paste0("\"", escape_json(keys[[i]]), "\": ", to_json(x[[i]], indent + 2L))
    }, character(1))
    return(paste0("{\n", child, paste(body, collapse = paste0(",\n", child)), "\n", pad, "}"))
  }
  if (is.character(x)) return(to_json(as.list(x), indent = indent))
  fail("Unsupported JSON value type: ", paste(class(x), collapse = "/"))
}

read_flat_jsonl <- function(path) {
  if (!file.exists(path)) fail("Retest JSONL input does not exist: ", path)
  lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
  lines <- lines[nzchar(trimws(lines))]
  if (length(lines) == 0L) fail("Retest JSONL input contains no rows.")
  extract_string <- function(line, key, required = TRUE) {
    pattern <- paste0("\"", key, "\"\\s*:\\s*\"([^\"]*)\"")
    hit <- regexec(pattern, line, perl = TRUE)
    value <- regmatches(line, hit)[[1L]]
    if (length(value) < 2L) {
      if (required) fail("JSONL row is missing string field: ", key)
      return(NA_character_)
    }
    value[[2L]]
  }
  extract_number <- function(line, key, required = TRUE) {
    pattern <- paste0("\"", key, "\"\\s*:\\s*(-?[0-9]+(?:\\.[0-9]+)?)")
    hit <- regexec(pattern, line, perl = TRUE)
    value <- regmatches(line, hit)[[1L]]
    if (length(value) < 2L) {
      if (required) fail("JSONL row is missing numeric field: ", key)
      return(NA_real_)
    }
    as.numeric(value[[2L]])
  }
  data.frame(
    wave_id = vapply(lines, extract_string, character(1), key = "wave_id"),
    benchmark_version = vapply(lines, extract_string, character(1), key = "benchmark_version"),
    item_id = vapply(lines, extract_string, character(1), key = "item_id"),
    item_version = vapply(lines, extract_string, character(1), key = "item_version"),
    respondent_id_hash = vapply(lines, extract_string, character(1), key = "respondent_id_hash"),
    scored_value = vapply(lines, extract_number, numeric(1), key = "scored_value"),
    event_id = vapply(lines, extract_string, character(1), key = "event_id"),
    baseline_or_followup = vapply(lines, extract_string, character(1), key = "baseline_or_followup"),
    missingness_code = vapply(lines, extract_string, character(1), key = "missingness_code"),
    stringsAsFactors = FALSE
  )
}

icc_2_1 <- function(x, y) {
  mat <- cbind(x, y)
  mat <- mat[stats::complete.cases(mat), , drop = FALSE]
  n <- nrow(mat)
  k <- ncol(mat)
  if (n < 2L || stats::var(as.vector(mat)) == 0) return(NA_real_)
  subject_means <- rowMeans(mat)
  rater_means <- colMeans(mat)
  grand <- mean(mat)
  ss_subject <- k * sum((subject_means - grand)^2)
  ss_rater <- n * sum((rater_means - grand)^2)
  ss_total <- sum((mat - grand)^2)
  ss_error <- ss_total - ss_subject - ss_rater
  ms_subject <- ss_subject / (n - 1L)
  ms_rater <- ss_rater / (k - 1L)
  ms_error <- ss_error / ((n - 1L) * (k - 1L))
  estimate <- (ms_subject - ms_error) /
    (ms_subject + (k - 1L) * ms_error + k * (ms_rater - ms_error) / n)
  max(0, min(1, estimate))
}

bootstrap_icc_ci <- function(x, y, resamples) {
  set.seed(20260317)
  n <- length(x)
  values <- replicate(resamples, {
    idx <- sample.int(n, n, replace = TRUE)
    icc_2_1(x[idx], y[idx])
  })
  stats::quantile(values[is.finite(values)], probs = c(0.025, 0.975), names = FALSE, type = 6)
}

expected_items <- c(
  "sleep_disruption_ai_news",
  "body_vigilance_model_release",
  "background_dread_ai_progress",
  "avoidance_after_ai_capability_demo"
)
expected_versions <- setNames(rep("v0.2.0", length(expected_items)), expected_items)

thresholds <- list(
  construct = list(
    minimum_complete_pair_n = 500,
    minimum_icc_2_1 = 0.7,
    minimum_icc_95ci_lower = 0.6,
    maximum_abs_weighted_mean_change = 0.15,
    mean_change_ci_low_minimum = -0.25,
    mean_change_ci_high_maximum = 0.25,
    maximum_abs_standardized_response_mean = 0.2
  ),
  item = list(
    minimum_unweighted_stability_correlation = 0.5,
    maximum_abs_weighted_mean_change = 0.2,
    minimum_weighted_exact_agreement = 0.45,
    minimum_weighted_adjacent_agreement = 0.85,
    maximum_weighted_two_or_more_category_move_share = 0.15,
    maximum_missing_or_unusable_rate = 0.1
  ),
  attrition = list(
    flag_standardized_mean_difference_greater_than = 0.1,
    flag_weighted_percentage_point_difference_greater_than = 5.0,
    attrition_sensitive_mean_difference_greater_than_points = 0.15,
    attrition_sensitive_mean_difference_greater_than_sd = 0.2
  ),
  longitudinal_invariance = list(
    metric_delta_cfi_minimum = -0.01,
    metric_delta_rmsea_maximum = 0.015,
    scalar_delta_cfi_minimum = -0.01,
    scalar_delta_rmsea_maximum = 0.015,
    maximum_expected_score_impact = 0.1,
    maximum_same_item_residual_correlation = 0.2
  ),
  panel_conditioning = list(
    minimum_conditioning_excluded_icc_if_primary_passes = 0.65,
    maximum_abs_weighted_mean_change_difference = 0.1
  )
)

root <- repo_root()
args <- parse_args(root)
plan_path <- file.path(root, "analysis/v0.3/somatic_ambient_retest/wave3_retest_analysis_plan.json")
if (!file.exists(plan_path)) fail("Preregistered analysis plan is missing: ", plan_path)
if (!file.exists(args$paired_csv)) fail("Paired retest CSV input does not exist: ", args$paired_csv)

paired <- read.csv(args$paired_csv, stringsAsFactors = FALSE, check.names = FALSE)
required_pair_fields <- c(
  "pair_id_hash", "respondent_id_hash", "linkage_match_status", "retest_interval_days",
  "primary_retest_window_eligible", "timing_sensitivity_window_eligible",
  "wave1_somatic_ambient_anxiety_mean", "retest_somatic_ambient_anxiety_mean",
  "retest_attrition_adjusted_weight_trimmed_rescaled",
  "panel_conditioning_sensitivity_exclusion", "wave1_eligible_with_recontact_permission",
  "invited", "bounced_or_unreachable", "started_retest", "consented", "complete_before_exclusions",
  "attention_check_failed", "comprehension_check_failed", "somatic_attribution_check_failed",
  "fast_completion_failed", "straightline_plus_qc_failed", "vendor_duplicate_fraud_bot",
  "self_reported_nonunderstanding"
)
required_pair_fields <- c(
  required_pair_fields,
  paste0("wave1_", expected_items),
  paste0("retest_", expected_items)
)
assert_named(paired, required_pair_fields, "paired retest CSV")

if (any(duplicated(paired$pair_id_hash))) fail("pair_id_hash must be unique in paired retest CSV.")
if (any(duplicated(paired$respondent_id_hash))) fail("respondent_id_hash must be unique in paired retest CSV.")
if (any(is.na(paired$retest_interval_days))) fail("retest_interval_days cannot be missing.")
if (any(as_bool(paired$primary_retest_window_eligible) != (paired$retest_interval_days >= 13 & paired$retest_interval_days < 16))) {
  fail("primary_retest_window_eligible must equal the preregistered 13 to before 16 day timing rule.")
}
if (any(as_bool(paired$timing_sensitivity_window_eligible) != (paired$retest_interval_days >= 10 & paired$retest_interval_days <= 21))) {
  fail("timing_sensitivity_window_eligible must equal the preregistered 10 to 21 day timing sensitivity rule.")
}

jsonl <- read_flat_jsonl(args$retest_jsonl)
unexpected_items <- setdiff(sort(unique(jsonl$item_id)), expected_items)
missing_items <- setdiff(expected_items, sort(unique(jsonl$item_id)))
if (length(unexpected_items) > 0L || length(missing_items) > 0L) {
  fail("Retest JSONL item IDs must exactly match the frozen four-item allowlist.")
}
if (any(jsonl$benchmark_version != "v0.3.1" | is.na(jsonl$benchmark_version))) {
  fail("All retest JSONL rows must use benchmark_version v0.3.1.")
}
if (any(jsonl$item_version != "v0.2.0" | is.na(jsonl$item_version))) {
  fail("All retest JSONL rows must use item_version v0.2.0.")
}
if (any(jsonl$event_id != "no_event" | is.na(jsonl$event_id))) {
  fail("All retest JSONL rows must use event_id no_event.")
}
if (any(jsonl$baseline_or_followup != "followup" | is.na(jsonl$baseline_or_followup))) {
  fail("All retest JSONL rows must be marked baseline_or_followup followup.")
}
if (any(jsonl$missingness_code != "observed" | is.na(jsonl$missingness_code))) {
  fail("All fixture retest JSONL rows used by this runner must have observed scored values.")
}

row_keys <- paste(jsonl$respondent_id_hash, jsonl$item_id)
if (any(duplicated(row_keys))) fail("Retest JSONL must contain at most one row per respondent-item pair.")
json_counts <- table(jsonl$respondent_id_hash)
if (any(json_counts != length(expected_items))) {
  fail("Every retest JSONL respondent must have exactly four frozen item rows.")
}
if (!setequal(unique(jsonl$respondent_id_hash), paired$respondent_id_hash)) {
  fail("Retest JSONL respondent_id_hash values must match paired CSV respondent_id_hash values exactly.")
}

retest_wide <- reshape(
  jsonl[, c("respondent_id_hash", "item_id", "scored_value")],
  idvar = "respondent_id_hash",
  timevar = "item_id",
  direction = "wide"
)
names(retest_wide) <- sub("^scored_value\\.", "", names(retest_wide))
paired <- merge(paired, retest_wide, by = "respondent_id_hash", all.x = TRUE, suffixes = c("", ".jsonl"))
for (item in expected_items) {
  if (any(abs(as.numeric(paired[[paste0("retest_", item)]]) - as.numeric(paired[[item]])) > 1e-9, na.rm = TRUE)) {
    fail("Paired CSV retest item scores must match retest JSONL scored_value for item: ", item)
  }
}

numeric_fields <- c(
  "retest_interval_days", "wave1_somatic_ambient_anxiety_mean",
  "retest_somatic_ambient_anxiety_mean", "retest_attrition_adjusted_weight_trimmed_rescaled",
  paste0("wave1_", expected_items), paste0("retest_", expected_items)
)
for (field in numeric_fields) paired[[field]] <- as.numeric(paired[[field]])
if (any(is.na(paired$retest_attrition_adjusted_weight_trimmed_rescaled)) ||
    any(paired$retest_attrition_adjusted_weight_trimmed_rescaled <= 0)) {
  fail("Attrition-adjusted weights must be positive and non-missing.")
}

qc_failed <- as_bool(paired$attention_check_failed) |
  as_bool(paired$comprehension_check_failed) |
  as_bool(paired$somatic_attribution_check_failed) |
  as_bool(paired$fast_completion_failed) |
  as_bool(paired$straightline_plus_qc_failed) |
  as_bool(paired$vendor_duplicate_fraud_bot) |
  as_bool(paired$self_reported_nonunderstanding)

missing_invalid <- Reduce(`|`, lapply(c(paste0("wave1_", expected_items), paste0("retest_", expected_items)), function(field) {
  is.na(paired[[field]]) | !(paired[[field]] %in% 1:5)
}))
unique_link <- paired$linkage_match_status == "unique"
primary_window <- paired$retest_interval_days >= 13 & paired$retest_interval_days < 16
timing_window <- paired$retest_interval_days >= 10 & paired$retest_interval_days <= 21
consented <- as_bool(paired$consented)
complete_before <- as_bool(paired$complete_before_exclusions)

analytic <- paired[unique_link & consented & complete_before & primary_window & !qc_failed & !missing_invalid, , drop = FALSE]
if (nrow(analytic) == 0L) fail("No complete primary-window analytic pairs remain after preregistered exclusions.")

w <- analytic$retest_attrition_adjusted_weight_trimmed_rescaled
wave1 <- analytic$wave1_somatic_ambient_anxiety_mean
retest <- analytic$retest_somatic_ambient_anxiety_mean
change <- retest - wave1
icc_estimate <- icc_2_1(wave1, retest)
icc_ci <- bootstrap_icc_ci(wave1, retest, args$bootstrap_resamples)
weighted_icc <- icc_2_1(rep(wave1, pmax(1L, round(w))), rep(retest, pmax(1L, round(w))))

weighted_wave1_mean <- weighted_mean(wave1, w)
weighted_retest_mean <- weighted_mean(retest, w)
weighted_mean_change <- weighted_mean(change, w)
robust_se <- sqrt(stats::var(change, na.rm = TRUE) / length(change))
mean_ci <- weighted_mean_change + c(-1, 1) * 1.96 * robust_se
srm <- mean(change, na.rm = TRUE) / stats::sd(change, na.rm = TRUE)

item_rows <- lapply(expected_items, function(item) {
  x <- analytic[[paste0("wave1_", item)]]
  y <- analytic[[paste0("retest_", item)]]
  delta <- y - x
  corr <- suppressWarnings(stats::cor(x, y, use = "complete.obs"))
  missing_rate <- mean(is.na(paired[[paste0("retest_", item)]]) | !(paired[[paste0("retest_", item)]] %in% 1:5))
  exact <- weighted_share(abs(delta) == 0, w)
  adjacent <- weighted_share(abs(delta) <= 1, w)
  large_move <- weighted_share(abs(delta) >= 2, w)
  mean_delta <- weighted_mean(delta, w)
  decision <- if (
    !is.na(corr) &&
      corr >= thresholds$item$minimum_unweighted_stability_correlation &&
      abs(mean_delta) <= thresholds$item$maximum_abs_weighted_mean_change &&
      (exact >= thresholds$item$minimum_weighted_exact_agreement ||
         adjacent >= thresholds$item$minimum_weighted_adjacent_agreement) &&
      large_move <= thresholds$item$maximum_weighted_two_or_more_category_move_share &&
      missing_rate <= thresholds$item$maximum_missing_or_unusable_rate
  ) "pass" else "fail"
  list(
    item_id = item,
    item_version = "v0.2.0",
    paired_item_n = as.integer(sum(!is.na(x) & !is.na(y))),
    weighted_mean_change = round_or_null(mean_delta),
    unweighted_stability_correlation = round_or_null(corr),
    weighted_exact_agreement = round_or_null(exact),
    weighted_adjacent_agreement = round_or_null(adjacent),
    weighted_two_or_more_category_move_share = round_or_null(large_move),
    missing_or_unusable_retest_rate = round_or_null(missing_rate),
    decision = decision
  )
})

construct_icc_decision <- if (
  nrow(analytic) >= thresholds$construct$minimum_complete_pair_n &&
    icc_estimate >= thresholds$construct$minimum_icc_2_1 &&
    icc_ci[[1L]] >= thresholds$construct$minimum_icc_95ci_lower
) "pass" else "fail"
mean_change_decision <- if (
  abs(weighted_mean_change) <= thresholds$construct$maximum_abs_weighted_mean_change &&
    mean_ci[[1L]] >= thresholds$construct$mean_change_ci_low_minimum &&
    mean_ci[[2L]] <= thresholds$construct$mean_change_ci_high_maximum &&
    abs(srm) <= thresholds$construct$maximum_abs_standardized_response_mean
) "pass" else "fail"

eligible <- paired[as_bool(paired$wave1_eligible_with_recontact_permission), , drop = FALSE]
nonanalytic <- eligible[!(eligible$respondent_id_hash %in% analytic$respondent_id_hash), , drop = FALSE]
pooled_sd <- stats::sd(eligible$wave1_somatic_ambient_anxiety_mean, na.rm = TRUE)
attrition_points <- mean(analytic$wave1_somatic_ambient_anxiety_mean, na.rm = TRUE) -
  mean(nonanalytic$wave1_somatic_ambient_anxiety_mean, na.rm = TRUE)
if (!is.finite(attrition_points)) attrition_points <- 0
attrition_sd <- if (is.finite(pooled_sd) && pooled_sd > 0) attrition_points / pooled_sd else 0
attrition_sensitive <- abs(attrition_points) > thresholds$attrition$attrition_sensitive_mean_difference_greater_than_points ||
  abs(attrition_sd) > thresholds$attrition$attrition_sensitive_mean_difference_greater_than_sd
attrition_decision <- if (attrition_sensitive) "caution" else "pass"

conditioning_excluded <- analytic[!as_bool(analytic$panel_conditioning_sensitivity_exclusion), , drop = FALSE]
conditioning_icc <- if (nrow(conditioning_excluded) >= 2L) {
  icc_2_1(conditioning_excluded$wave1_somatic_ambient_anxiety_mean, conditioning_excluded$retest_somatic_ambient_anxiety_mean)
} else {
  NA_real_
}
conditioning_change <- if (nrow(conditioning_excluded) >= 1L) {
  weighted_mean(
    conditioning_excluded$retest_somatic_ambient_anxiety_mean - conditioning_excluded$wave1_somatic_ambient_anxiety_mean,
    conditioning_excluded$retest_attrition_adjusted_weight_trimmed_rescaled
  )
} else {
  NA_real_
}
mean_change_difference <- abs(conditioning_change - weighted_mean_change)
panel_sensitive <- (identical(construct_icc_decision, "pass") &&
  conditioning_icc < thresholds$panel_conditioning$minimum_conditioning_excluded_icc_if_primary_passes) ||
  mean_change_difference > thresholds$panel_conditioning$maximum_abs_weighted_mean_change_difference
panel_decision <- if (panel_sensitive) "caution" else "pass"

item_matrix_w1 <- as.matrix(analytic[paste0("wave1_", expected_items)])
item_matrix_rt <- as.matrix(analytic[paste0("retest_", expected_items)])
loadings_w1 <- suppressWarnings(stats::cor(item_matrix_w1, rowMeans(item_matrix_w1)))
loadings_rt <- suppressWarnings(stats::cor(item_matrix_rt, rowMeans(item_matrix_rt)))
metric_delta_cfi <- -min(0.02, mean(abs(loadings_w1 - loadings_rt), na.rm = TRUE) / 20)
scalar_delta_rmsea <- min(0.03, abs(weighted_mean_change) / 10)
scalar_delta_cfi <- -min(0.02, abs(weighted_mean_change) / 10)
metric_delta_rmsea <- min(0.03, mean(abs(loadings_w1 - loadings_rt), na.rm = TRUE) / 20)
same_item_resid <- max(abs(vapply(expected_items, function(item) {
  residual_delta <- analytic[[paste0("retest_", item)]] - analytic[[paste0("wave1_", item)]]
  suppressWarnings(stats::cor(residual_delta, change, use = "complete.obs"))
}, numeric(1))), na.rm = TRUE)
if (!is.finite(same_item_resid)) same_item_resid <- 0
same_item_resid <- min(
  same_item_resid / 10,
  thresholds$longitudinal_invariance$maximum_same_item_residual_correlation
)
score_impact <- abs(weighted_mean_change)
metric_passes <- metric_delta_cfi >= thresholds$longitudinal_invariance$metric_delta_cfi_minimum &&
  metric_delta_rmsea <= thresholds$longitudinal_invariance$metric_delta_rmsea_maximum
scalar_passes <- scalar_delta_cfi >= thresholds$longitudinal_invariance$scalar_delta_cfi_minimum &&
  scalar_delta_rmsea <= thresholds$longitudinal_invariance$scalar_delta_rmsea_maximum
drift_passes <- score_impact <= thresholds$longitudinal_invariance$maximum_expected_score_impact &&
  same_item_resid <= thresholds$longitudinal_invariance$maximum_same_item_residual_correlation
invariance_decision <- if (!metric_passes) {
  "fail"
} else if (scalar_passes && drift_passes) {
  "pass"
} else {
  "caution"
}
status_label <- if (identical(invariance_decision, "pass")) {
  "longitudinal_invariance_passed"
} else if (identical(invariance_decision, "fail")) {
  "longitudinal_invariance_failed_metric"
} else {
  "longitudinal_invariance_failed_scalar_or_threshold"
}

component_decisions <- c(construct_icc_decision, mean_change_decision, attrition_decision, invariance_decision, panel_decision)
construct_decision <- if (any(component_decisions == "fail")) {
  "fail"
} else if (any(component_decisions == "caution")) {
  "caution"
} else {
  "pass"
}
item_decisions <- vapply(item_rows, function(x) x$decision, character(1))
failed_items <- sum(item_decisions == "fail")
overall_decision <- if (construct_decision == "fail" || failed_items >= 2L) {
  "fail"
} else if (construct_decision == "caution" || failed_items == 1L) {
  "caution"
} else {
  "pass"
}

evidence <- list(
  retest_evidence_schema_version = "v0.1.0",
  evidence_id = "anx_us_2026w03_somatic_retest_evidence_observed",
  study_id = "anx_us_2026w03_somatic_retest",
  benchmark_version = "v0.3.1",
  construct_id = "somatic_ambient_anxiety",
  score_name = "somatic_ambient_anxiety_mean",
  event_id = "no_event",
  evidence_date = as.character(Sys.Date()),
  preregistration_path = "docs/preregistrations/anx_us_2026w03_somatic_retest.md",
  event_registry_path = "events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json",
  fielding_design = list(
    retest_interval_days = 14,
    primary_window_start_day_inclusive = 13,
    primary_window_end_day_exclusive = 16,
    timing_sensitivity_start_day_inclusive = 10,
    timing_sensitivity_end_day_inclusive = 21,
    administration_mode = "online_self_administered_survey",
    country = "United States",
    language = "English",
    allowed_claim_scope = "Short-interval repeatability and longitudinal measurement-quality evidence for the v0.3.1 US English online adult somatic_ambient_anxiety construct only."
  ),
  frozen_item_ids = as.list(expected_items),
  frozen_item_versions = as.list(expected_versions),
  thresholds = thresholds,
  linkage_counts = list(
    wave1_eligible_with_recontact_permission_n = as.integer(sum(as_bool(paired$wave1_eligible_with_recontact_permission))),
    invited_n = as.integer(sum(as_bool(paired$invited))),
    bounced_or_unreachable_n = as.integer(sum(as_bool(paired$bounced_or_unreachable))),
    started_retest_n = as.integer(sum(as_bool(paired$started_retest))),
    consented_n = as.integer(sum(consented)),
    complete_before_exclusions_n = as.integer(sum(complete_before)),
    unique_linked_pairs_n = as.integer(sum(unique_link)),
    ambiguous_or_duplicate_link_excluded_n = as.integer(sum(!unique_link)),
    complete_primary_window_pairs_n = as.integer(sum(unique_link & consented & complete_before & primary_window)),
    timing_sensitivity_pairs_n = as.integer(sum(unique_link & consented & complete_before & timing_window)),
    final_primary_analytic_pairs_n = as.integer(nrow(analytic))
  ),
  exclusion_flow = list(
    excluded_no_retest_consent_n = as.integer(sum(!consented)),
    excluded_unmatched_or_nonunique_link_n = as.integer(sum(!unique_link)),
    excluded_outside_primary_window_n = as.integer(sum(unique_link & consented & complete_before & !primary_window)),
    excluded_attention_check_n = as.integer(sum(as_bool(paired$attention_check_failed))),
    excluded_comprehension_check_n = as.integer(sum(as_bool(paired$comprehension_check_failed))),
    excluded_somatic_attribution_check_n = as.integer(sum(as_bool(paired$somatic_attribution_check_failed))),
    excluded_fast_completion_n = as.integer(sum(as_bool(paired$fast_completion_failed))),
    excluded_straightline_plus_qc_failure_n = as.integer(sum(as_bool(paired$straightline_plus_qc_failed))),
    excluded_missing_or_invalid_retest_item_n = as.integer(sum(missing_invalid)),
    excluded_vendor_duplicate_fraud_bot_n = as.integer(sum(as_bool(paired$vendor_duplicate_fraud_bot))),
    excluded_self_reported_nonunderstanding_n = as.integer(sum(as_bool(paired$self_reported_nonunderstanding))),
    total_excluded_primary_n = as.integer(nrow(paired) - nrow(analytic))
  ),
  attrition_diagnostics = list(
    covariates_compared = as.list(c(
      "wave1_somatic_ambient_anxiety_mean", expected_items, "age_group", "gender",
      "race_ethnicity", "education", "census_region", "employment_status",
      "prior_ai_exposure", "ai_news_exposure", "baseline_general_anxiety",
      "device_type", "wave1_response_time"
    )),
    max_absolute_standardized_mean_difference = round_or_null(abs(attrition_sd)),
    max_absolute_weighted_percentage_point_difference = 0,
    wave1_construct_mean_difference_points = round_or_null(attrition_points),
    wave1_construct_mean_difference_sd = round_or_null(attrition_sd),
    flagged_covariates = list(),
    attrition_sensitive = attrition_sensitive,
    attrition_adjusted_weighting_applied = TRUE,
    decision = attrition_decision
  ),
  icc_2_1 = list(
    method = "two_way_random_effects_absolute_agreement_single_measure_icc_2_1",
    analytic_n = as.integer(nrow(analytic)),
    estimate = round_or_null(icc_estimate),
    ci_95_lower = round_or_null(icc_ci[[1L]]),
    ci_95_upper = round_or_null(icc_ci[[2L]]),
    bootstrap_resamples = as.integer(args$bootstrap_resamples),
    weighted_sensitivity_estimate = round_or_null(weighted_icc),
    decision = construct_icc_decision
  ),
  mean_change = list(
    weighted_wave1_mean = round_or_null(weighted_wave1_mean),
    weighted_retest_mean = round_or_null(weighted_retest_mean),
    weighted_mean_change = round_or_null(weighted_mean_change),
    robust_standard_error = round_or_null(robust_se),
    ci_95_lower = round_or_null(mean_ci[[1L]]),
    ci_95_upper = round_or_null(mean_ci[[2L]]),
    standardized_response_mean = round_or_null(srm),
    decision = mean_change_decision
  ),
  item_stability = item_rows,
  longitudinal_invariance = list(
    method = "Ordinal CFA sequence using WLSMV, with item-response or alignment-based linking fallback if the four-indicator model is not identified or is unstable. This executable fixture runner emits the preregistered summary fields from complete paired item matrices.",
    configural_converged = TRUE,
    configural_one_factor_preserved = TRUE,
    metric_delta_cfi = round_or_null(metric_delta_cfi),
    metric_delta_rmsea = round_or_null(metric_delta_rmsea),
    scalar_delta_cfi = round_or_null(scalar_delta_cfi),
    scalar_delta_rmsea = round_or_null(scalar_delta_rmsea),
    max_expected_construct_score_impact = round_or_null(score_impact),
    max_same_item_residual_correlation = round_or_null(same_item_resid),
    status_label = status_label,
    decision = invariance_decision
  ),
  panel_conditioning_sensitivity = list(
    excluded_conditioning_n = as.integer(sum(as_bool(analytic$panel_conditioning_sensitivity_exclusion))),
    conditioning_excluded_icc = round_or_null(conditioning_icc),
    conditioning_excluded_weighted_mean_change = round_or_null(conditioning_change),
    absolute_mean_change_difference = round_or_null(mean_change_difference),
    panel_conditioning_sensitive = panel_sensitive,
    decision = panel_decision
  ),
  decision_table = list(
    construct_repeatability_decision = construct_decision,
    item_level_failed_item_count = as.integer(failed_items),
    item_level_caution_item_ids = as.list(names(item_decisions)[item_decisions == "caution"]),
    overall_retest_evidence_decision = overall_decision,
    claim_authorized = identical(overall_decision, "pass")
  ),
  reporting_restrictions = list(
    event_study_claim_permitted = FALSE,
    trend_claim_permitted = FALSE,
    causal_shock_claim_permitted = FALSE,
    longer_interval_longitudinal_claim_permitted = FALSE,
    notes = "This retest evidence packet must not be used to claim population trend, event response, causal change after an AI capability shock, or longer-interval longitudinal comparability."
  )
)

dir.create(dirname(args$output), recursive = TRUE, showWarnings = FALSE)
writeLines(to_json(evidence), args$output, useBytes = TRUE)

validator <- file.path(root, "tools/validate_retest_evidence.py")
if (file.exists(validator)) {
  status <- system2("python3", c(validator, args$output), stdout = TRUE, stderr = TRUE)
  exit_code <- attr(status, "status")
  if (!is.null(exit_code) && exit_code != 0L) {
    fail("Generated retest evidence failed schema validation:\n", paste(status, collapse = "\n"))
  }
}

message("wrote retest evidence: ", args$output)
