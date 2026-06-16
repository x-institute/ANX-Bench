# ANX-Bench US 2026 Wave 2 Somatic Calibration Codebook v0.2.3

## Codebook Control

- Wave ID: `anx_us_2026w02_somatic`
- Study label: `anx_us_2026w02_somatic_calibration`
- Benchmark release: `v0.2.3`
- Codebook version: `anx_us_2026w02_somatic_codebook_v0.2.3`
- Freeze date: `2026-06-16`
- Paired instrument: `releases/v0.2.3/anx_us_2026w02_somatic_instrument.md`
- Paired preregistration: `releases/v0.2.3/anx_us_2026w02_somatic_calibration_preregistration.md`
- Anchoring vignette set: `anchors/v0.2/somatic_ambient/response_scale_vignettes.json`
- Frozen event registry: `events/v0.2/anx_us_2026w02_somatic_event_registry.json`
- Canonical respondent-item schema: `schema/wave_response.schema.json`
- Canonical behavioral criterion schema: `schema/behavioral_response.schema.json`

This codebook defines the respondent-item schema mapping, item allowlist, non-scored anchoring vignette variables, non-scored behavioral criterion-validity variables, quality-control variables, response-time variables, covariates, and sensitivity-analysis variables for the v0.2.3 somatic and ambient calibration packet. ANX item responses are represented as one row per respondent per administered item under `schema/wave_response.schema.json`. The revealed AI review allocation task is represented as one row per respondent under `schema/behavioral_response.schema.json`. Anchoring vignette responses are respondent-level calibration variables and must not be represented as ANX respondent-item rows.

## File Families

| File family | Access level | Contents |
| --- | --- | --- |
| Canonical respondent-item analytic file | Public or restricted according to disclosure review | One row per respondent-item response validating against `schema/wave_response.schema.json`. Includes the four randomized ANX items only. |
| Behavioral criterion analytic file | Public or restricted according to disclosure review | One row per respondent for the revealed AI review allocation task validating against `schema/behavioral_response.schema.json`. Includes the randomized high-impact decision arm, 100-cent allocation, comprehension result, behavioral missingness, behavioral exclusions, and derived criterion score. This file is validation infrastructure only and is never an ANX scored item file. |
| Respondent-level analytic covariate file | Public or restricted according to disclosure review | One row per respondent with eligibility, sampling, demographics, AI exposure, sleep sensitivity, health anxiety sensitivity, baseline general anxiety, anchor ratings, response-style strata, quality control, paradata summaries, and weights. |
| Restricted operations file | Restricted, not public | Vendor respondent IDs, survey tokens, duplicate-detection fields, device fingerprints, IP-derived fraud flags, exact timestamps when not disclosure-safe, raw open-text comments, and linkage materials needed for audit. |

Public files must exclude direct identifiers, vendor IDs, raw device fingerprints, raw IP fields, exact contact information, clinical details, and raw open text. Restricted files may be used to reproduce exclusions and linkage, but must not be merged into public releases.

## Mapping Into `wave_response.schema.json`

The canonical respondent-item file must contain the following schema fields for every administered somatic and ambient ANX item. Anchoring vignettes are excluded from this file.

| Schema field | Wave 2 somatic source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w02_somatic`. |
| `benchmark_version` | Constant `v0.2.3` for the anchoring-vignette packet. Item files remain version `v0.2.0` because v0.2.3 does not change ANX item meaning. |
| `item_id` | Item ID from the randomized somatic and ambient block. Allowed IDs are the four item IDs listed in the allowlist below. |
| `item_version` | Constant `v0.2.0` for every administered somatic and ambient ANX item. |
| `respondent_id_hash` | Study-scoped salted SHA-256 or stronger keyed hash of the restricted respondent linkage key. The salt is stored outside analytic data. |
| `raw_response` | Numeric response `1` to `5` from the ANX item screen, or null if no answer was captured. Vendor labels must be mapped back to numeric anchors before analytic export. |
| `scored_value` | For observed non-excluded item responses, equal to `raw_response` because all four items use non-reverse-coded 1 to 5 scoring. Null when missingness or exclusion prevents scoring. |
| `response_timestamp` | UTC timestamp when the item response was submitted or finalized. Public files may coarsen precision if documented. |
| `administration_mode` | `web` for desktop or laptop browser completes and `mobile_web` for phone or tablet browser completes. |
| `language` | Constant `en-US`. |
| `survey_weight` | Final respondent-level analysis weight for the relevant sample. Use `1.0` until final weights are constructed. |
| `exclusion_flags` | Array derived from respondent-level and row-level QC variables. Empty array means no exclusion flag applies. |
| `missingness_code` | `observed`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, `not_scored_item_ineligible`, or `not_scored_excluded_respondent`, as applicable. |
| `event_id` | Constant `no_event`, matching `events/v0.2/anx_us_2026w02_somatic_event_registry.json`. |
| `event_exposure_window` | Null for this non-event calibration wave. |
| `baseline_or_followup` | Null for this non-event calibration wave unless a later preregistered longitudinal addendum creates a new packet and release. |
| `fielding_time_relative_to_event_hours` | Null for this non-event calibration wave. |

## Mapping Into `behavioral_response.schema.json`

The behavioral criterion analytic file is the canonical export for the non-scored task `revealed_ai_review_allocation_v1`. Each eligible survey record must contribute exactly one behavioral row, including rows where the task was not presented, was skipped, failed quality review, or is otherwise missing. The file validates against `schema/behavioral_response.schema.json` and must not be merged into `schema/wave_response.schema.json`, item scoring files, official score outputs, item-retention counts, factor analyses, IRT models, or event-study outcomes.

The task asks respondents to allocate a 100-cent review budget between AI-only review and human review after random assignment to one high-impact decision scenario. The derived criterion score is `human_review_cents / 100`, so higher values indicate greater revealed preference for human review over AI-only review. The criterion is used to test behavioral validity of somatic and ambient AI anxiety responses; it is not an ANX-Bench item, construct, domain, overall, longitudinal, or public benchmark score.

Required exported fields for `revealed_ai_review_allocation_v1` are:

| Schema field | Required export rule |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w02_somatic`. |
| `respondent_id` | Study-scoped salted 64-character lowercase hexadecimal respondent hash. It must join to `respondent_id_hash` in respondent-level covariates through the same salted identifier and must never expose a raw vendor ID. |
| `task_id` | Constant `revealed_ai_review_allocation_v1`. |
| `benchmark_version` | Constant `v0.2.3`, because the behavioral task is introduced and frozen by this packet. |
| `randomized_arm` | Randomly assigned scenario arm, one of `employment_hiring`, `healthcare_triage`, `public_benefits`, or `school_placement`. Assignment is independent of ANX item order and anchoring vignette responses. |
| `allocation_mode` | `real_bonus` if the allocation affected respondent compensation or a real research budget, otherwise `bonus_stated` if implemented as a stated allocation. The mode must be constant within a sample unless the preregistered fielding design documents otherwise. |
| `ai_only_review_cents` | Integer 0 to 100 when `missingness_code == observed`; null when the allocation is not observed. It records cents allocated to AI-only review. |
| `human_review_cents` | Integer 0 to 100 when `missingness_code == observed`; null when the allocation is not observed. It records cents allocated to human review. |
| `allocation_total_cents` | Must equal 100 for observed rows and null for unobserved rows. Export validation must reject observed rows where `ai_only_review_cents + human_review_cents` is not 100, even if a vendor total field is present. |
| `allocation_confirmed` | `true` only when the respondent actively submitted or confirmed the allocation. Observed rows require `true`; unobserved rows may be `false` if the task was not confirmed. |
| `behavioral_comprehension_response` | Integer 1 to 4 for an administered comprehension check, or null if the check was not administered or not captured. Option 1 is the only correct response. |
| `behavioral_comprehension_passed` | `true` only when `behavioral_comprehension_response == 1`; `false` when the check was administered and failed; null only when the check was not administered or not captured. Observed rows require `true`. |
| `exclusion_flags` | Unique array of behavioral and survey-level exclusion flags allowed by `schema/behavioral_response.schema.json`. Empty array means no behavioral exclusion flag has been applied. |
| `missingness_code` | One of `observed`, `not_presented_by_design`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, or `not_scored_excluded_respondent`. Only `observed` rows may have a non-null `revealed_anxiety_score`. |
| `revealed_anxiety_score` | Number from 0.00 to 1.00 in 0.01 increments for observed, confirmed, comprehension-passing rows, computed as `human_review_cents / 100`. Must be null for every non-observed missingness code. |

Rows with `behavioral_comprehension_failed`, `behavioral_allocation_invalid`, `behavioral_task_not_presented`, `technical_failure`, `removed_by_quality_control`, or `not_scored_excluded_respondent` flags remain in the behavioral analytic file for reproducibility, but are excluded from the preregistered primary behavioral criterion-validity model unless a sensitivity analysis explicitly includes them under a documented rule.

## Administered ANX Item Allowlist

| Domain | Item ID | Item file version | File | Construct ID |
| --- | --- | --- | --- | --- |
| somatic_ambient | `sleep_disruption_ai_news` | `v0.2.0` | `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `body_vigilance_model_release` | `v0.2.0` | `items/v0.2/somatic_ambient/body_vigilance_model_release.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `background_dread_ai_progress` | `v0.2.0` | `items/v0.2/somatic_ambient/background_dread_ai_progress.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `avoidance_after_ai_capability_demo` | `v0.2.0` | `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json` | `somatic_ambient_anxiety` |

All administered ANX items use the ordered 5-point anxiety response scale from 1 `Not at all anxious` to 5 `Extremely anxious`.

## Anchoring Vignette Variables

Anchoring vignettes are administered after the ANX item block and before covariates. They are non-scored calibration variables. They are excluded from ANX item counts, item missingness proportions, factor analyses, IRT calibration, reliability estimation, item-retention thresholds, and all official scoring.

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `anchor_somatic_low_raw` | integer or null | 1 to 5, null if missing | Public | Raw response to `anchor_somatic_ambient_low`, the low-severity somatic and ambient response-scale vignette. |
| `anchor_somatic_moderate_raw` | integer or null | 1 to 5, null if missing | Public | Raw response to `anchor_somatic_ambient_moderate`, the moderate-severity response-scale vignette. |
| `anchor_somatic_high_raw` | integer or null | 1 to 5, null if missing | Public | Raw response to `anchor_somatic_ambient_high`, the high-severity response-scale vignette. |
| `anchor_order_violation` | boolean or null | `true`, `false`, null | Public | `true` if any observed pair violates low <= moderate <= high. `false` if all three ratings are observed and monotone. Null if fewer than two anchor ratings are observed. |
| `anchor_response_style_stratum` | string | `compressed_low`, `calibrated_monotone`, `compressed_high`, `nonmonotone`, `incomplete`, `other` | Public | Descriptive response-style category derived from the three raw anchor ratings. Used for sensitivity analyses, never for ANX scoring. |
| `anchor_ratings_missing_count` | integer | 0 to 3 | Public | Count of missing raw anchoring vignette ratings. |
| `anchor_block_duration_seconds` | number or null | 0 or greater | Restricted or public summary | Time from first anchoring vignette display to final anchoring vignette submission. |

`anchor_response_style_stratum` is derived as follows:

| Stratum | Rule |
| --- | --- |
| `compressed_low` | All observed anchor ratings are 1 or 2, all three are observed, and `anchor_order_violation == false`. |
| `calibrated_monotone` | All three ratings are observed, `anchor_order_violation == false`, and `anchor_somatic_high_raw - anchor_somatic_low_raw >= 2`. |
| `compressed_high` | All observed anchor ratings are 4 or 5, all three are observed, and `anchor_order_violation == false`. |
| `nonmonotone` | `anchor_order_violation == true`. |
| `incomplete` | Fewer than three anchor ratings are observed. |
| `other` | Complete monotone ratings that do not meet the compressed or calibrated-monotone rules. |

Anchor variables may be included in sensitivity analyses for response style, DIF, invariance, and cross-wave comparability. They must not be used as exclusion criteria by themselves, and they must not be used to adjust primary ANX item responses unless the adjustment is clearly labeled as a sensitivity analysis.

## Respondent-Level Identifiers And Sample Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Public or restricted | Study-scoped salted respondent identifier used to join respondent-level covariates to respondent-item rows. |
| `sample_id` | string | `development_pilot`, `confirmation` | Public | Non-overlapping calibration sample. |
| `wave_id` | string | `anx_us_2026w02_somatic` | Public | Wave identifier. |
| `benchmark_version` | string | `v0.2.3` | Public | Release packet governing the fielding instrument, codebook, preregistration, anchors, and checksums. |
| `item_file_version` | string | `v0.2.0` | Public | Item JSON version for all four administered ANX items. |
| `analytic_eligible` | boolean | `true`, `false` | Public | Respondent is eligible after consent, population criteria, duplicate review, breakoff review, and preregistered QC exclusions. |

## Covariates And Criteria

The v0.2.3 packet retains the v0.2.1 covariate and criterion families: demographics and quotas, prior AI exposure, AI-news exposure, sleep sensitivity, health anxiety sensitivity, two baseline general anxiety items, AI information avoidance intention, and AI information checking intention. Prefer-not-to-answer options are retained as explicit categories where offered. The anchoring vignette variables are not covariates for primary scoring and do not affect item missingness.

Key validation covariates retain the following coding:

| Variable | Type | Allowed values or coding | Definition |
| --- | --- | --- | --- |
| `sleep_sensitivity_stress_news` | integer | 1 to 5, 9 prefer not to answer | General sleep sensitivity to stressful news or worries. |
| `health_anxiety_body_sensation_worry` | integer | 1 to 5, 9 prefer not to answer | Tendency for ordinary body sensations to trigger health worry. |
| `ai_news_exposure_30d` | integer | 1 to 5, 9 prefer not to answer | Frequency of AI capability news or commentary exposure during the past 30 days. |
| `baseline_general_anxiety_2item_mean` | number or null | 0.00 to 3.00 | Mean of valid responses to the two baseline general anxiety items. |
| `ai_information_avoidance_intention_6m` | integer | 1 to 5, 9 prefer not to answer | Intended avoidance of AI-related information during the next 6 months. |
| `ai_information_checking_intention_6m` | integer | 1 to 5, 9 prefer not to answer | Intended checking or information seeking about AI during the next 6 months. |

## Quality Control Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `attention_check_response` | integer | 1 to 5 | Restricted or public summary | Response to the instructed-response attention check. |
| `attention_check_passed` | boolean | `true`, `false` | Public | `true` only when `attention_check_response == 3`. |
| `scenario_comprehension_response` | integer | 1 to 4 | Restricted or public summary | Response to the required scenario-comprehension check. |
| `scenario_comprehension_passed` | boolean | `true`, `false` | Public | `true` only when response is 1. |
| `somatic_attribution_response` | integer | 1 to 4 | Restricted or public summary | Response to the somatic-attribution check. |
| `somatic_attribution_passed` | boolean | `true`, `false` | Public | `true` only when response is 1. |
| `self_reported_understanding` | integer | 1 to 5 | Public | Values 4 and 5 trigger `quality_review_failed`. |
| `straightline_anx_block` | boolean | `true`, `false` | Public | `true` when the same substantive response is given to all four ANX items. Anchors are not included. |
| `anx_items_missing_count` | integer | 0 to 4 | Public | Number of ANX items without observed response. Anchoring vignettes are excluded. |
| `anx_items_missing_prop` | number | 0.00 to 1.00 | Public | Missing ANX item count divided by 4. |
| `final_exclusion_flags` | array of strings | Values allowed by `schema/wave_response.schema.json` | Public | Respondent-level flags propagated to all respondent-item rows when applicable. |

`anchor_order_violation` and `anchor_response_style_stratum` are not exclusion variables. Analysts may report their association with QC indicators, but exclusion decisions must follow the preregistered QC rules for the ANX packet.

## Sensitivity-Analysis Usage

The confirmation validation dossier must report anchor usage in three places:

1. Response-style calibration: distribution of the three raw anchor ratings, monotone ordering rate, response-style strata, and subgroup differences in these quantities.
2. DIF and invariance sensitivity: whether ordinal DIF, MIMIC, multi-group IRT, or ordered-categorical CFA conclusions change after including `anchor_response_style_stratum`, excluding `nonmonotone` anchor respondents in a sensitivity model, or estimating models within the largest response-style strata when sample size permits.
3. Cross-wave comparability: whether differences between v0.2.3 and later waves remain after comparing fixed vignette response distributions.

Anchor-adjusted results are sensitivity analyses. The primary psychometric decision for the v0.2 somatic ANX items remains based on the preregistered item pool, quality-control rules, dimensionality, reliability, IRT, DIF, invariance, and external-validity evidence.
