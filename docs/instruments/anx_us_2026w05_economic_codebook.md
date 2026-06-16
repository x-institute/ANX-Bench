# ANX-Bench US 2026 Wave 5 Economic and Vocational Calibration Codebook

## Codebook Control

- Wave ID: `anx_us_2026w05_economic`
- Study label: `anx_us_2026w05_economic_calibration`
- Benchmark release: `v0.5.0`
- Codebook version: `anx_us_2026w05_economic_codebook`
- Freeze date: `2026-06-16`
- Paired instrument: `docs/instruments/anx_us_2026w05_economic_instrument.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w05_economic_calibration.md`
- Frozen event registry: `events/v0.5/anx_us_2026w05_economic_event_registry.json`
- Canonical respondent-item schema: `schema/wave_response.schema.json`

This codebook defines the respondent-item schema mapping, item allowlist, quality-control variables, response-time variables, covariates, weights, missingness rules, exclusion flags, and restricted operations fields for the Wave 5 `economic_vocational_anxiety` calibration packet. ANX item responses are represented as one row per respondent per administered item under `schema/wave_response.schema.json`. Respondent-level files support sampling, exclusions, psychometric diagnostics, DIF, invariance, and external-validity analyses. They are not ANX-Bench scored items.

## File Families

| File family | Access level | Contents |
| --- | --- | --- |
| Canonical respondent-item analytic file | Public or restricted according to disclosure review | One row per respondent-item response validating against `schema/wave_response.schema.json`. Includes no direct vendor IDs. |
| Respondent-level analytic covariate file | Public or restricted according to disclosure review | One row per respondent with eligibility, sampling, demographics, employment, occupation, AI exposure, perceived occupational AI exposure, baseline general anxiety, QC, paradata summaries, and weights. |
| Restricted operations file | Restricted, not public | Vendor respondent IDs, survey tokens, duplicate-detection fields, device fingerprints, IP-derived fraud flags, exact timestamps when not disclosure-safe, raw open-text comments, and linkage materials needed for audit. |

Public files must exclude direct identifiers, vendor IDs, raw device fingerprints, raw IP fields, exact contact information, employer names, client names, school names, compensation records, tax records, performance reviews, union membership details, raw open text, and any linkage key or hash salt.

## Mapping Into `wave_response.schema.json`

The canonical respondent-item file must contain the following schema fields for every administered economic and vocational ANX item.

| Schema field | Wave 5 economic source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w05_economic`. |
| `benchmark_version` | Constant `v0.5.0` for the frozen candidate packet. |
| `item_id` | Item ID from the randomized economic and vocational block. Allowed IDs are the four IDs listed in the allowlist below. |
| `item_version` | Constant `v0.1.0` for every administered economic and vocational item. |
| `respondent_id_hash` | Study-scoped salted SHA-256 or stronger keyed hash of the restricted respondent linkage key. The salt is stored outside analytic data. |
| `raw_response` | Numeric response `1` to `5` from the ANX item screen, or null if no answer was captured. Vendor labels must be mapped back to numeric anchors before analytic export. |
| `scored_value` | For observed non-excluded item responses, equal to `raw_response` because all four items use non-reverse-coded 1 to 5 scoring. Null when missingness or exclusion prevents scoring. |
| `response_timestamp` | UTC timestamp when the item response was submitted or finalized. Public files may coarsen precision only if the coarsening is documented and does not affect planned analyses. |
| `administration_mode` | `web` for desktop or laptop browser completes and `mobile_web` for phone or tablet browser completes. Other modes are protocol deviations. |
| `language` | Constant `en-US`. |
| `survey_weight` | Final respondent-level analysis weight for the relevant sample. Use `1.0` until final weights are constructed. |
| `exclusion_flags` | Array derived from respondent-level and row-level QC variables. Empty array means no exclusion flag applies. Allowed values are exactly those in `schema/wave_response.schema.json`: `attention_check_failed`, `speeding`, `straightlining`, `duplicate_respondent`, `ineligible_population`, `consent_withdrawn`, `quality_review_failed`, `item_not_administered_by_design`, `mode_protocol_violation`, `language_protocol_violation`, `scoring_ineligible_item`, and `other_preregistered_exclusion`. |
| `missingness_code` | `observed`, `not_presented_by_design`, `skipped_by_respondent`, `prefer_not_to_answer`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, `not_scored_item_ineligible`, or `not_scored_excluded_respondent`, as applicable. |
| `event_id` | Constant `no_event`, matching `events/v0.5/anx_us_2026w05_economic_event_registry.json`. This calibration wave is explicitly not keyed to a capability event. |
| `event_exposure_window` | Omit or null in raw exports for this non-event calibration wave. Do not derive an exposure window from fielding dates or AI news observed after the registry lock. |
| `baseline_or_followup` | Omit or null for this non-event calibration wave unless a later preregistered longitudinal packet creates a new release. |
| `fielding_time_relative_to_event_hours` | Omit or null because `event_id` is `no_event` and no event timestamp exists. |

## Administered ANX Item Allowlist

The following four item IDs are the only ANX item IDs allowed in `anx_us_2026w05_economic` respondent-item rows. Vendor exports must not add, drop, rename, recode, substitute, or update ANX items without a dated preregistration addendum and a new release packet.

| Domain | Item ID | Item file version | File | Construct ID | Scoring variable |
| --- | --- | --- | --- | --- | --- |
| economic_vocational | `skill_obsolescence_software` | `v0.1.0` | `items/v0.1/economic_vocational/skill_obsolescence_software.json` | `economic_vocational_anxiety` | `software_skill_obsolescence_anxiety` |
| economic_vocational | `wage_pressure_customer_support` | `v0.1.0` | `items/v0.1/economic_vocational/wage_pressure_customer_support.json` | `economic_vocational_anxiety` | `customer_support_wage_pressure_anxiety` |
| economic_vocational | `retraining_pressure_accounting` | `v0.1.0` | `items/v0.1/economic_vocational/retraining_pressure_accounting.json` | `economic_vocational_anxiety` | `accounting_retraining_pressure_anxiety` |
| economic_vocational | `status_loss_creative_work` | `v0.1.0` | `items/v0.1/economic_vocational/status_loss_creative_work.json` | `economic_vocational_anxiety` | `creative_status_loss_anxiety` |

All administered ANX items use this ordered 5-point anxiety scale:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

The item `job_displacement_radiology` is excluded by design for Wave 5 because it maps to `anticipated_job_displacement_anxiety`. If a vendor platform includes it, rows for that item must be coded `item_not_administered_by_design` and excluded from the Wave 5 analytic item set.

## Respondent-Level Identifiers and Sample Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Public or restricted | Study-scoped salted respondent identifier used to join respondent-level covariates to respondent-item rows. |
| `sample_id` | string | `development_pilot`, `confirmation_sample` | Public | Non-overlapping calibration sample. |
| `wave_id` | string | `anx_us_2026w05_economic` | Public | Wave identifier. |
| `benchmark_version` | string | `v0.5.0` | Public | Release packet governing the fielding instrument, codebook, preregistration, event registry, analysis plan, and checksums. |
| `item_file_version` | string | `v0.1.0` | Public | Item JSON version for all four administered items. |
| `survey_start_timestamp_utc` | datetime | ISO 8601 UTC | Restricted or coarsened | Survey start time. |
| `survey_end_timestamp_utc` | datetime | ISO 8601 UTC | Restricted or coarsened | Survey completion or breakoff time. |
| `survey_duration_seconds` | integer | 0 or greater | Public | End timestamp minus start timestamp after removing known platform pauses if validated pause metadata are available. |
| `complete_status` | string | `complete`, `screenout`, `breakoff`, `quota_full`, `nonconsent`, `vendor_quality_termination` | Restricted summary public | Operational completion status before analytic exclusions. |
| `consent_status` | string | `agreed`, `declined`, `withdrawn` | Restricted summary public | Consent disposition from Screen 1. |
| `eligibility_age_18_plus` | boolean | `true`, `false` | Public | Whether respondent confirmed or profile data indicated age 18 or older. |
| `eligibility_us_resident` | boolean | `true`, `false` | Public | Whether respondent resides in the United States. |
| `eligibility_english_self_administered` | boolean | `true`, `false` | Public | Whether respondent can complete the English survey unaided. |
| `analytic_eligible` | boolean | `true`, `false` | Public | Respondent is eligible after consent, population criteria, duplicate review, breakoff review, and preregistered QC exclusions. |

## Covariates

### Demographics, Employment, and Quotas

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `age_group` | string | `18_29`, `30_44`, `45_59`, `60_plus` | Public | Preregistered quota and DIF category. |
| `gender` | string | `woman`, `man`, `nonbinary_another_gender`, `prefer_not_to_answer` | Public, subject to suppression | Gender category for quotas, DIF, and descriptive reporting. |
| `race_ethnicity` | string | `hispanic_latino`, `non_hispanic_white`, `non_hispanic_black`, `non_hispanic_asian`, `non_hispanic_other_multiracial`, `prefer_not_to_answer` | Public, subject to suppression | Race and ethnicity category used for quotas, weighting, and DIF. |
| `education` | string | `high_school_or_less`, `some_college_associate`, `bachelors`, `graduate`, `prefer_not_to_answer` | Public | Highest educational attainment. |
| `census_region` | string | `northeast`, `midwest`, `south`, `west` | Public | US Census region. |
| `employment_status` | string | `employed_full_time`, `employed_part_time`, `self_employed`, `unemployed_looking`, `student`, `retired`, `not_in_labor_force_other`, `prefer_not_to_answer` | Public | Current employment status from vendor profile or survey harmonization. |
| `occupation_group` | string | Harmonized broad occupation category or `not_currently_employed`, `student`, `other`, `prefer_not_to_answer` | Public, subject to coarsening | Broad occupation group used for quota monitoring, DIF, and disclosure review. |
| `labor_force_attachment` | integer | 1 `working_full_time`, 2 `working_part_time`, 3 `self_employed_freelance`, 4 `unemployed_looking`, 5 `student_training`, 6 `retired`, 7 `not_in_labor_force_other`, 9 `prefer_not_to_answer` | Public | Current connection to paid work from the survey instrument. |
| `software_or_technical_work` | boolean or string | `true`, `false`, `prefer_not_to_answer` | Public, subject to suppression | Whether respondent works in, recently worked in, or is training for software or technical work. |
| `customer_support_or_service_work` | boolean or string | `true`, `false`, `prefer_not_to_answer` | Public, subject to suppression | Whether respondent works in, recently worked in, or is training for customer support, call-center, or service work. |
| `accounting_finance_work` | boolean or string | `true`, `false`, `prefer_not_to_answer` | Public, subject to suppression | Whether respondent works in, recently worked in, or is training for accounting, bookkeeping, finance, or audit work. |
| `creative_work` | boolean or string | `true`, `false`, `prefer_not_to_answer` | Public, subject to suppression | Whether respondent works in, recently worked in, or is training for writing, art, design, music, media, advertising, publishing, or entertainment work. |

### AI Exposure and Economic-Vocational Comparators

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `prior_ai_exposure_frequency` | string | `never_rare`, `monthly`, `weekly`, `daily_near_daily`, `prefer_not_to_answer` | Public | Frequency of using generative AI tools such as chatbots, image generators, coding assistants, or AI search tools. |
| `ai_use_work_or_school` | string | `never`, `less_than_monthly`, `monthly`, `weekly`, `daily_near_daily`, `not_applicable`, `prefer_not_to_answer` | Public | Frequency of AI tool use for work or school tasks. |
| `ai_use_personal` | string | `never`, `less_than_monthly`, `monthly`, `weekly`, `daily_near_daily`, `prefer_not_to_answer` | Public | Frequency of AI tool use for personal tasks. |
| `ai_news_exposure_30d` | integer | 1 `not_at_all`, 2 `less_than_once_a_week`, 3 `about_once_a_week`, 4 `several_times_a_week`, 5 `daily_almost_daily`, 9 `prefer_not_to_answer` | Public | Frequency of exposure to AI capability news or commentary during the past 30 days. |
| `self_rated_ai_familiarity` | integer | 1 to 5, 9 prefer not to answer | Public | General familiarity with AI capabilities. |
| `perceived_occupational_ai_exposure` | integer | 1 `not_at_all_exposed`, 2 `slightly_exposed`, 3 `moderately_exposed`, 4 `very_exposed`, 5 `extremely_exposed`, 9 `prefer_not_to_answer` | Public | Respondent's perceived exposure of current, recent, or intended work to current or near-future AI tools. |
| `ai_labor_market_worry_6m` | integer | 1 `very_unlikely`, 2 `somewhat_unlikely`, 3 `neither`, 4 `somewhat_likely`, 5 `very_likely`, 9 `prefer_not_to_answer` | Public | Criterion variable for expected labor-market uncertainty from AI in the next 6 months. |
| `ai_retraining_pressure_expectation_6m` | integer | 1 `very_unlikely`, 2 `somewhat_unlikely`, 3 `neither`, 4 `somewhat_likely`, 5 `very_likely`, 9 `prefer_not_to_answer` | Public | Criterion variable for expected pressure on workers to retrain quickly because of AI tools. |
| `ai_work_news_avoidance_intention_6m` | integer | 1 `very_unlikely`, 2 `somewhat_unlikely`, 3 `neither`, 4 `somewhat_likely`, 5 `very_likely`, 9 `prefer_not_to_answer` | Public | Criterion variable for likely avoidance of AI work-related news if it creates tension about jobs, wages, or skills. |

### Baseline General Anxiety

| Variable | Type | Allowed values or coding | Scoring direction | Public data status | Missingness rule | Definition |
| --- | --- | --- | --- | --- | --- | --- |
| `baseline_general_anxiety_nervous_2w` | integer | 0 `not_at_all`, 1 `several_days`, 2 `more_than_half_the_days`, 3 `nearly_every_day`, 9 `prefer_not_to_answer` | Higher valid values indicate greater recent general anxiety. | Public | Required screen. If no value is captured, code null and set `covariate_item_missing`. Value 9 is retained as prefer not to answer and excluded from scoring. | General anxiety covariate asking about feeling nervous, tense, or on edge during the past 2 weeks. |
| `baseline_general_anxiety_worry_2w` | integer | 0 `not_at_all`, 1 `several_days`, 2 `more_than_half_the_days`, 3 `nearly_every_day`, 9 `prefer_not_to_answer` | Higher valid values indicate greater recent general worry. | Public | Required screen. If no value is captured, code null and set `covariate_item_missing`. Value 9 is retained as prefer not to answer and excluded from scoring. | General anxiety covariate asking about difficulty stopping or controlling ordinary-life worry during the past 2 weeks. |
| `baseline_general_anxiety_2item_mean` | number or null | Mean of valid 0 to 3 values from the two baseline general anxiety items, range 0.00 to 3.00 | Higher values indicate higher recent general anxiety. | Public | Compute when at least one source item has a valid 0 to 3 response. Do not impute prefer not to answer. | Two-item general anxiety covariate used for discriminant and incremental-validity analyses. |
| `baseline_general_anxiety_2item_valid_n` | integer | 0, 1, 2 | Not a score. | Public | Count valid 0 to 3 responses among the two baseline general anxiety items. | Completeness indicator for the baseline general anxiety covariate. |
| `covariate_item_missing` | boolean | `true`, `false` | Not a score. | Public | Set `true` if any required covariate screen has null because no response was captured. Prefer not to answer values do not by themselves set this flag. | Respondent-level indicator that a required non-ANX covariate was technically missing or skipped despite required status. |

## Quality Control Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `attention_check_response` | integer | 1 to 5 | Restricted or public summary | Response to the instructed-response attention check. |
| `attention_check_passed` | boolean | `true`, `false` | Public | `true` only when `attention_check_response == 3`. Failed respondents receive `attention_check_failed`. |
| `scenario_comprehension_response` | integer | 1 to 4 | Restricted or public summary | Response to the required scenario-comprehension check. |
| `scenario_comprehension_passed` | boolean | `true`, `false` | Public | `true` only when response is 1. Failed respondents receive `other_preregistered_exclusion` with restricted reason `scenario_comprehension_failed`. |
| `economic_vocational_attribution_response` | integer | 1 to 4 | Restricted or public summary | Response to the economic-vocational attribution check. |
| `economic_vocational_attribution_passed` | boolean | `true`, `false` | Public | `true` only when response is 1. Failed respondents receive `other_preregistered_exclusion` with restricted reason `economic_vocational_attribution_failed`. |
| `self_reported_understanding` | integer | 1 to 5 | Public | Response to the understanding check. Values 4 and 5 trigger `quality_review_failed`. |
| `duplicate_review_status` | string | `not_duplicate`, `duplicate_confirmed`, `duplicate_possible_unconfirmed` | Restricted summary public | Duplicate review result from vendor IDs, survey tokens, and device or fingerprint evidence. |
| `vendor_quality_status` | string | `passed`, `low_confidence`, `failed`, `not_provided` | Restricted summary public | Vendor fraud or quality flag. Vendor-failed completes receive `quality_review_failed` unless manual review overturns the flag before outcome inspection. |
| `straightline_anx_block` | boolean | `true`, `false` | Public | `true` when the same substantive response is given to all four ANX items. Exclusion requires straightlining plus failed attention check or minimum reading-time check. |
| `anx_items_missing_count` | integer | 0 to 4 | Public | Number of ANX items without observed response. |
| `anx_items_missing_prop` | number | 0.00 to 1.00 | Public | Missing ANX item count divided by 4. Greater than 0.25 triggers exclusion because two missing items prevent stable construct diagnostics. |
| `speeding_flag` | boolean | `true`, `false` | Public | `true` when survey completion time is less than one-third of the median completion time for the same sample after removing clear breakoffs. |
| `minimum_reading_time_flag` | boolean | `true`, `false` | Public | `true` when ANX block or item times indicate less than one-third of sample median reading time under the preregistered rule. |
| `open_text_quality_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment indicates confusion, satire, protest responding, or failure to treat scenarios as AI-related. Does not exclude by itself. |
| `distress_review_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment suggests notable respondent distress. Used for ethics monitoring, not automatic exclusion. |
| `final_exclusion_flags` | array of strings | Values allowed by `schema/wave_response.schema.json` | Public | Respondent-level flags propagated to all respondent-item rows when applicable. |

## Response Time and Paradata Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `device_type` | string | `desktop_laptop`, `mobile_tablet`, `unknown` | Public | Device category used for DIF screening and mode assignment. |
| `administration_mode` | string | `web`, `mobile_web` | Public | Mapped into schema field `administration_mode`. |
| `anx_block_order` | string or array | Ordered list of four item IDs | Restricted | Respondent-specific randomized item order. Public releases may provide item block position per row instead. |
| `item_block_position` | integer | 1 to 4 | Public | Position of the item in the respondent's randomized ANX block. |
| `item_response_time_seconds` | number | 0 or greater | Public or restricted | Time between item screen display and answer submission. Used for item-level response-time diagnostics. |
| `anx_block_duration_seconds` | number | 0 or greater | Public | Time from first ANX item display to final ANX item submission. |
| `attention_check_time_seconds` | number | 0 or greater | Restricted | Time on the attention-check screen. |
| `comprehension_check_time_seconds` | number | 0 or greater | Restricted | Time on the scenario-comprehension screen. |
| `economic_vocational_attribution_check_time_seconds` | number | 0 or greater | Restricted | Time on the economic-vocational attribution check screen. |
| `covariate_module_duration_seconds` | number | 0 or greater | Restricted or public summary | Time spent on employment, AI exposure, baseline anxiety, and criterion screens. |
| `page_backtracking_count` | integer | 0 or greater | Restricted | Count of detected back navigation or page revisits, if available. |
| `technical_error_flag` | boolean | `true`, `false` | Restricted summary public | Platform error affecting survey presentation or response capture. |

## Weights and Quota Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `quota_age_group` | string | Same as `age_group` | Public | Age group used for quota monitoring. |
| `quota_gender` | string | Same as `gender` with vendor harmonization documented | Public | Gender category used for quota monitoring. |
| `quota_race_ethnicity` | string | Same as `race_ethnicity` | Public | Race and ethnicity category used for quota monitoring. |
| `quota_education` | string | Same as `education` | Public | Education category used for quota monitoring. |
| `quota_census_region` | string | Same as `census_region` | Public | Region category used for quota monitoring. |
| `quota_employment_status` | string | Same as `employment_status` after vendor harmonization | Public | Employment category used for quota monitoring. |
| `quota_occupation_group` | string | Same as `occupation_group` after collapsing sparse categories | Public | Occupation category used for quota monitoring and imbalance diagnostics. |
| `quota_ai_news_exposure_30d` | integer | Same as `ai_news_exposure_30d` after collapsing if needed | Public | AI-news exposure category used for quota monitoring or imbalance diagnostics. |
| `base_weight` | number | Positive number | Restricted or public | Design or vendor base weight before post-stratification. |
| `poststrat_weight` | number | Positive number | Public | Weight after raking or post-stratification. |
| `final_weight` | number | Positive number, target trimmed range 0.30 to 3.00 | Public | Final analysis weight mapped to `survey_weight` in every respondent-item row. |
| `weight_trimmed` | boolean | `true`, `false` | Public | Whether the respondent's post-stratification weight was trimmed. |

## Missingness and Exclusion Flags

Prefer-not-to-answer options are retained as explicit categories for demographics, AI exposure, perceived occupational AI exposure, labor-force attachment, baseline general anxiety, and external-validity variables. ANX item skipped responses are not coded as prefer not to answer because the ANX item screens do not present that option.

For respondent-item rows, `missingness_code` is `observed` only when `raw_response` is present and `scored_value` can be computed under the item scoring key. If the respondent is excluded after an observed item response, retain `raw_response`, set `scored_value` to null when the analytic export is for scored analyses, set `missingness_code` to `not_scored_excluded_respondent`, and propagate the relevant `exclusion_flags`. If the item is skipped, use `skipped_by_respondent`. If a platform failure prevents capture, use `technical_failure`. If a respondent breaks off before the item, use `survey_breakoff`. If a non-allowlisted item is present because of implementation error, use `item_not_administered_by_design` and do not include it in the Wave 5 analytic item set.

The following variables may exist only in restricted operations files and must never appear in public analytic files: `vendor_panelist_id`, `vendor_survey_token`, `vendor_project_id`, `vendor_session_id`, `vendor_transaction_id`, `ip_address`, `ip_geolocation`, `device_fingerprint`, `browser_user_agent_raw`, `panel_profile_raw_json`, `open_text_debrief_raw`, `employer_name_raw`, `client_name_raw`, `school_name_raw`, `wage_or_compensation_raw`, `tax_or_financial_record_raw`, `union_membership_raw`, and `hash_salt_or_linkage_key`.

Before public release, the data steward must review cross-classified cells involving age group, gender, race and ethnicity, region, education, employment status, occupation group, labor-force attachment, AI exposure, perceived occupational AI exposure, baseline general anxiety, device type, and fielding date. Small cells must be suppressed, combined, or moved to restricted access. Exact timestamps, raw comments, direct vendor identifiers, raw device fields, workplace identifiers, compensation records, and linkage materials are always restricted.
