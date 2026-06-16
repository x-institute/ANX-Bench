# ANX-Bench US 2026 Wave 6 Epistemic Trust Calibration Codebook

## Codebook Control

- Wave ID: `anx_us_2026w06_epistemic`
- Study label: `anx_us_2026w06_epistemic_calibration`
- Benchmark release: `v0.6.0`
- Codebook version: `anx_us_2026w06_epistemic_codebook`
- Freeze date: `2026-06-16`
- Paired instrument: `docs/instruments/anx_us_2026w06_epistemic_instrument.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w06_epistemic_calibration.md`
- Frozen event registry: `events/v0.6/anx_us_2026w06_epistemic_event_registry.json`
- Canonical respondent-item schema: `schema/wave_response.schema.json`

This codebook defines the Wave 6 respondent-item mapping, item allowlist, quality-control variables, comparator variables, behavioral criterion task fields, weights, exclusion flags, missingness rules, and public-data restrictions. ANX item responses are represented as one row per respondent per administered item under `schema/wave_response.schema.json`. Respondent-level files support psychometric diagnostics, DIF, invariance, external validity, behavioral validity, and incremental-validity analyses. They are not ANX-Bench scored output files.

## File Families

| File family | Access level | Contents |
| --- | --- | --- |
| Canonical respondent-item analytic file | Public or restricted after disclosure review | One row per respondent-item response validating against `schema/wave_response.schema.json`; includes no direct vendor IDs. |
| Respondent-level analytic covariate file | Public or restricted after disclosure review | Eligibility, sample split, demographics, media exposure, AI exposure, institutional trust, baseline anxiety, QC, paradata summaries, behavioral task fields, and weights. |
| Restricted operations file | Restricted, not public | Vendor IDs, survey tokens, duplicate-detection fields, raw device and IP signals, exact timestamps when not disclosure-safe, raw open text, and linkage materials. |

## Mapping Into `wave_response.schema.json`

| Schema field | Wave 6 epistemic source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w06_epistemic`. |
| `benchmark_version` | Constant `v0.6.0`. |
| `item_id` | One of the four administered epistemic item IDs listed below. |
| `item_version` | Constant `v0.1.0`. |
| `respondent_id_hash` | Study-scoped salted SHA-256 or stronger keyed hash of the restricted respondent linkage key. |
| `raw_response` | Numeric response `1` to `5` from the ANX item screen, or null if no answer was captured. |
| `scored_value` | Equal to `raw_response` for observed non-excluded item responses because all four items use non-reverse-coded 1 to 5 scoring; null when missingness or exclusion prevents analytic scoring. |
| `response_timestamp` | UTC timestamp when the item response was submitted or finalized. Public files may coarsen precision only with documented disclosure review. |
| `administration_mode` | `web` for desktop or laptop browser completes and `mobile_web` for phone or tablet browser completes. Other modes are protocol deviations. |
| `language` | Constant `en-US`. |
| `survey_weight` | Final respondent-level analysis weight for the relevant sample; use `1.0` until final weights are constructed. |
| `exclusion_flags` | Array using values allowed by `schema/wave_response.schema.json`; respondent-level exclusions propagate to all four item rows. |
| `missingness_code` | `observed`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, `not_scored_excluded_respondent`, or `not_scored_item_ineligible`, as applicable. |
| `event_id` | Constant `no_event`, matching the frozen Wave 6 event registry. |
| `event_exposure_window` | Omit or null. No event window exists. |
| `baseline_or_followup` | Omit or null. Wave 6 is not a longitudinal baseline or follow-up. |
| `fielding_time_relative_to_event_hours` | Omit or null because `event_id` is `no_event`. |

## Administered ANX Item Allowlist

| Domain | Item ID | Item file version | File | Construct ID | Scoring variable |
| --- | --- | --- | --- | --- | --- |
| epistemic | `deepfake_evidence_trust` | `v0.1.0` | `items/v0.1/epistemic/deepfake_evidence_trust.json` | `epistemic_trust_anxiety` | `deepfake_evidence_trust_anxiety` |
| epistemic | `synthetic_news_provenance` | `v0.1.0` | `items/v0.1/epistemic/synthetic_news_provenance.json` | `epistemic_trust_anxiety` | `synthetic_news_provenance_anxiety` |
| epistemic | `ai_expert_claim_conflict` | `v0.1.0` | `items/v0.1/epistemic/ai_expert_claim_conflict.json` | `epistemic_trust_anxiety` | `ai_expert_claim_conflict_anxiety` |
| epistemic | `personalized_misinformation_targeting` | `v0.1.0` | `items/v0.1/epistemic/personalized_misinformation_targeting.json` | `epistemic_trust_anxiety` | `personalized_misinformation_targeting_anxiety` |

All administered ANX items use this ordered 5-point anxiety scale: 1 `Not at all anxious`, 2 `Slightly anxious`, 3 `Moderately anxious`, 4 `Very anxious`, 5 `Extremely anxious`. No other `items/v0.1/epistemic` or cross-domain item may appear in the Wave 6 analytic item set.

## Respondent-Level Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Public or restricted | Study-scoped salted respondent identifier used to join respondent-level covariates to respondent-item rows. |
| `sample_id` | string | `development_pilot`, `confirmation_sample` | Public | Non-overlapping calibration sample. |
| `wave_id` | string | `anx_us_2026w06_epistemic` | Public | Wave identifier. |
| `benchmark_version` | string | `v0.6.0` | Public | Release packet governing the fielding instrument and analysis contract. |
| `analytic_eligible` | boolean | `true`, `false` | Public | Respondent is eligible after consent, population criteria, duplicate review, breakoff review, and preregistered QC exclusions. |
| `age_group` | string | `18_29`, `30_44`, `45_59`, `60_plus` | Public | Quota, DIF, and invariance category. |
| `gender` | string | `woman`, `man`, `nonbinary_another_gender`, `prefer_not_to_answer` | Public, subject to suppression | Gender category for quotas and DIF. |
| `race_ethnicity` | string | `hispanic_latino`, `non_hispanic_white`, `non_hispanic_black`, `non_hispanic_asian`, `non_hispanic_other_multiracial`, `prefer_not_to_answer` | Public, subject to suppression | Race and ethnicity category for quotas and DIF. |
| `education` | string | `high_school_or_less`, `some_college_associate`, `bachelors`, `graduate`, `prefer_not_to_answer` | Public | Highest educational attainment. |
| `census_region` | string | `northeast`, `midwest`, `south`, `west` | Public | US Census region. |
| `device_type` | string | `desktop_laptop`, `mobile_tablet`, `unknown` | Public | Device category for paradata and DIF screening. |

## Comparator and Validity Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `prior_ai_exposure_frequency` | integer | 1 `never_rare`, 2 `monthly`, 3 `weekly`, 4 `daily_near_daily`, 9 `prefer_not_to_answer` | Public | Frequency of personal generative AI use. |
| `ai_news_exposure_30d` | integer | 1 `not_at_all`, 2 `less_than_once_a_week`, 3 `about_once_a_week`, 4 `several_times_a_week`, 5 `daily_almost_daily`, 9 `prefer_not_to_answer` | Public | Frequency of exposure to AI capability news during the past 30 days. |
| `perceived_ai_information_exposure` | integer | 1 `not_at_all_exposed`, 2 `slightly_exposed`, 3 `moderately_exposed`, 4 `very_exposed`, 5 `extremely_exposed`, 9 `prefer_not_to_answer` | Public | Perceived exposure of the respondent's information environment to current or near-future AI tools. |
| `information_environment_role` | integer | 1 `private_citizen`, 2 `information_professional_or_student`, 3 `law_public_health_science_education_journalism_or_tech`, 4 `helps_others_interpret_information`, 5 `none_fit_well`, 9 `prefer_not_to_answer` | Public, subject to suppression | Role in which respondent most often evaluates public information. |
| `media_literacy_self_rating` | integer | 1 to 5, 9 prefer not to answer | Public | Self-rated ability to check source credibility and provenance. |
| `institutional_trust_mean` | number or null | Mean of valid 1 to 5 trust items | Public | Comparator index for trust in courts, science agencies, journalism, and election administration. |
| `political_information_exposure` | integer | 1 to 5, 9 prefer not to answer | Public | Frequency of exposure to political news or commentary. |
| `ai_information_uncertainty_worry_6m` | integer | 1 `very_unlikely` to 5 `very_likely`, 9 prefer not to answer | Public | Criterion variable for expected AI-driven uncertainty about what evidence to trust. |
| `ai_authenticity_verification_burden_6m` | integer | 1 `very_unlikely` to 5 `very_likely`, 9 prefer not to answer | Public | Criterion variable for expected burden of extra verification steps before trusting AI-mediated information. |
| `ai_news_verification_avoidance_intention_6m` | integer | 1 `very_unlikely` to 5 `very_likely`, 9 prefer not to answer | Public | Criterion variable for avoiding AI-related information because trust evaluation feels tense or burdensome. |
| `baseline_general_anxiety_nervous_2w` | integer | 0 to 3, 9 prefer not to answer | Public | General anxiety covariate asking about feeling nervous, tense, or on edge during the past 2 weeks. |
| `baseline_general_anxiety_worry_2w` | integer | 0 to 3, 9 prefer not to answer | Public | General worry covariate asking about difficulty stopping or controlling ordinary-life worry during the past 2 weeks. |
| `baseline_general_anxiety_2item_mean` | number or null | Mean of valid 0 to 3 values | Public | Discriminant and incremental-validity covariate. |

## Behavioral Criterion Task Fields

The behavioral task `revealed_human_verification_allocation_v1` is not an ANX-Bench item and must not create respondent-item rows.

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `behavioral_task_id` | string | `revealed_human_verification_allocation_v1` | Public | Stable task identifier. |
| `behavioral_human_review_credits` | integer | 0 to 10 | Public | Credits allocated to additional human review of source provenance, authenticity, and context. |
| `behavioral_ai_only_review_credits` | integer | 0 to 10 | Public | Credits allocated to accepting AI-only review as sufficient. |
| `behavioral_allocation_sum_valid` | boolean | `true`, `false` | Public | `true` only when human-review and AI-only credits sum to exactly 10. |
| `behavioral_task_response_time_seconds` | number | 0 or greater | Public or restricted | Time from behavioral task display to valid submission. |
| `behavioral_task_correction_required` | boolean | `true`, `false` | Public | Whether the platform required correction before a valid allocation was submitted. |

## Quality Control and Paradata Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `attention_check_passed` | boolean | `true`, `false` | Public | `true` only when the instructed-response item equals 3. |
| `scenario_comprehension_passed` | boolean | `true`, `false` | Public | `true` only when the respondent identifies scenarios as hypothetical research materials. |
| `epistemic_attribution_passed` | boolean | `true`, `false` | Public | `true` only when the respondent identifies the task as rating anxiety about trusting evidence, media, or expert claims. |
| `self_reported_understanding` | integer | 1 to 5 | Public | Values 4 and 5 trigger `quality_review_failed`. |
| `straightline_anx_block` | boolean | `true`, `false` | Public | `true` when all four ANX items receive the same substantive response. |
| `anx_items_missing_count` | integer | 0 to 4 | Public | Number of ANX items without observed response. |
| `anx_items_missing_prop` | number | 0.00 to 1.00 | Public | Missing ANX item count divided by 4; greater than 0.25 triggers exclusion. |
| `speeding_flag` | boolean | `true`, `false` | Public | Completion time below one-third of the same-sample median after breakoffs are removed. |
| `minimum_reading_time_flag` | boolean | `true`, `false` | Public | ANX block or item time below one-third of same-sample median reading time. |
| `item_block_position` | integer | 1 to 4 | Public | Position of the item in the respondent's randomized ANX block. |
| `item_response_time_seconds` | number | 0 or greater | Public or restricted | Time between item screen display and answer submission. |
| `final_exclusion_flags` | array of strings | Values allowed by `schema/wave_response.schema.json` | Public | Respondent-level flags propagated to respondent-item rows. |

## Missingness, Weights, and Public-Data Restrictions

ANX item skipped responses are not coded as prefer not to answer because ANX item screens do not present that option. Prefer-not-to-answer values are retained as explicit categories for covariates and validity comparators. ANX item responses are never imputed for EFA, CFA, omega, IRT, DIF, invariance, criterion, behavioral, or incremental-validity gates.

Weights are constructed separately by sample. Minimum weighting variables are age group, gender, race and ethnicity, education, and Census region; AI exposure, AI-news exposure, and information-environment role may be included when stable margins are available. Final weights should be trimmed to 0.30 through 3.00 unless documented sensitivity analyses justify a wider range without changing decisions.

Public analytic files must exclude direct identifiers, vendor IDs, social-media handles, party registration records, real case names, real allegations, private messages, raw open text, raw device fingerprints, raw IP fields, exact contact information, employer names, client names, school names, exact timestamps when not disclosure-safe, and any linkage key or hash salt. Small cells involving demographics, information-environment role, institutional trust, political information exposure, AI exposure, media literacy, baseline anxiety, device type, and fielding date must be suppressed, combined, or moved to restricted access.
