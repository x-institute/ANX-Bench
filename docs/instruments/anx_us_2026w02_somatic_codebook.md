# ANX-Bench US 2026 Wave 2 Somatic Calibration Codebook

## Codebook Control

- Wave ID: `anx_us_2026w02_somatic`
- Study label: `anx_us_2026w02_somatic_calibration`
- Benchmark release: `v0.2.1`
- Codebook version: `anx_us_2026w02_somatic_codebook`
- Freeze date: `2026-06-15`
- Paired instrument: `docs/instruments/anx_us_2026w02_somatic_instrument.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w02_somatic_calibration.md`
- Frozen event registry: `events/v0.2/anx_us_2026w02_somatic_event_registry.json`
- Canonical respondent-item schema: `schema/wave_response.schema.json`

This codebook defines the respondent-item schema mapping, item allowlist, quality-control variables, response-time variables, and covariates for the v0.2 somatic and ambient calibration packet. ANX item responses are represented as one row per respondent per administered item under `schema/wave_response.schema.json`. Respondent-level variables support sampling, exclusion, psychometric diagnostics, DIF, invariance, and external-validity analyses. They are not ANX-Bench scored items.

## File Families

| File family | Access level | Contents |
| --- | --- | --- |
| Canonical respondent-item analytic file | Public or restricted according to disclosure review | One row per respondent-item response validating against `schema/wave_response.schema.json`. Includes no direct vendor IDs. |
| Respondent-level analytic covariate file | Public or restricted according to disclosure review | One row per respondent with eligibility, sampling, demographics, AI exposure, sleep sensitivity, health anxiety sensitivity, baseline general anxiety, quality control, paradata summaries, and weights. |
| Restricted operations file | Restricted, not public | Vendor respondent IDs, survey tokens, duplicate-detection fields, device fingerprints, IP-derived fraud flags, exact timestamps when not disclosure-safe, raw open-text comments, and linkage materials needed for audit. |

Public files must exclude direct identifiers, vendor IDs, raw device fingerprints, raw IP fields, exact contact information, clinical details, and raw open text. Restricted files may be used to reproduce exclusions and linkage, but must not be merged into public releases.

## Mapping Into `wave_response.schema.json`

The canonical respondent-item file must contain the following schema fields for every administered somatic and ambient ANX item.

| Schema field | Wave 2 somatic source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w02_somatic`. |
| `benchmark_version` | Constant `v0.2.1` for the fielding-ready packet. Item files remain version `v0.2.0` because v0.2.1 freezes the packet without changing item meaning. |
| `item_id` | Item ID from the randomized somatic and ambient block. Allowed IDs are the four item IDs listed in the allowlist below. |
| `item_version` | Constant `v0.2.0` for every administered somatic and ambient item. |
| `respondent_id_hash` | Study-scoped salted SHA-256 or stronger keyed hash of the restricted respondent linkage key. The salt is stored outside analytic data. |
| `raw_response` | Numeric response `1` to `5` from the ANX item screen, or null if no answer was captured. Vendor labels must be mapped back to numeric anchors before analytic export. |
| `scored_value` | For observed non-excluded item responses, equal to `raw_response` because all four items use non-reverse-coded 1 to 5 scoring. Null when missingness or exclusion prevents scoring. |
| `response_timestamp` | UTC timestamp when the item response was submitted or finalized. Public files may coarsen precision only if the coarsening is documented and does not affect planned analyses. |
| `administration_mode` | `web` for desktop or laptop browser completes and `mobile_web` for phone or tablet browser completes. Other modes are protocol deviations. |
| `language` | Constant `en-US`. |
| `survey_weight` | Final respondent-level analysis weight for the relevant sample. Use `1.0` until final weights are constructed. |
| `exclusion_flags` | Array derived from respondent-level and row-level QC variables. Empty array means no exclusion flag applies. |
| `missingness_code` | `observed`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, `not_scored_item_ineligible`, or `not_scored_excluded_respondent`, as applicable. |
| `event_id` | Constant `no_event`, matching `events/v0.2/anx_us_2026w02_somatic_event_registry.json`. This calibration wave is explicitly not keyed to a capability event. |
| `event_exposure_window` | Null for this non-event calibration wave. Do not derive an exposure window from fielding dates or AI news observed after the registry lock. |
| `baseline_or_followup` | Null for this non-event calibration wave unless a later preregistered longitudinal addendum creates a new packet and release. |
| `fielding_time_relative_to_event_hours` | Null for this non-event calibration wave because `event_id` is `no_event` and no event timestamp exists. |

## Administered ANX Item Allowlist

The following four item IDs are the only ANX item IDs allowed in `anx_us_2026w02_somatic` respondent-item rows. Vendor exports must not add, drop, rename, recode, or substitute ANX items without a dated preregistration addendum and a new release packet.

| Domain | Item ID | Item file version | File | Construct ID |
| --- | --- | --- | --- | --- |
| somatic_ambient | `sleep_disruption_ai_news` | `v0.2.0` | `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `body_vigilance_model_release` | `v0.2.0` | `items/v0.2/somatic_ambient/body_vigilance_model_release.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `background_dread_ai_progress` | `v0.2.0` | `items/v0.2/somatic_ambient/background_dread_ai_progress.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `avoidance_after_ai_capability_demo` | `v0.2.0` | `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json` | `somatic_ambient_anxiety` |

All administered ANX items use the same ordered 5-point anxiety response scale:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

## Respondent-Level Identifiers And Sample Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Public or restricted | Study-scoped salted respondent identifier used to join respondent-level covariates to respondent-item rows. |
| `sample_id` | string | `development_pilot`, `confirmation` | Public | Non-overlapping calibration sample. |
| `wave_id` | string | `anx_us_2026w02_somatic` | Public | Wave identifier. |
| `benchmark_version` | string | `v0.2.1` | Public | Release packet governing the fielding instrument, codebook, preregistration, dossier, and checksums. |
| `item_file_version` | string | `v0.2.0` | Public | Item JSON version for all four administered items. |
| `survey_start_timestamp_utc` | datetime | ISO 8601 UTC | Restricted or coarsened | Survey start time. Public files may coarsen to date or hour after disclosure review. |
| `survey_end_timestamp_utc` | datetime | ISO 8601 UTC | Restricted or coarsened | Survey completion or breakoff time. |
| `survey_duration_seconds` | integer | 0 or greater | Public | End timestamp minus start timestamp after removing known platform pauses if vendor provides validated pause metadata. |
| `complete_status` | string | `complete`, `screenout`, `breakoff`, `quota_full`, `nonconsent`, `vendor_quality_termination` | Restricted summary public | Operational completion status before analytic exclusions. |
| `consent_status` | string | `agreed`, `declined`, `withdrawn` | Restricted summary public | Consent disposition from Screen 1. |
| `eligibility_age_18_plus` | boolean | `true`, `false` | Public | Whether respondent confirmed or profile data indicated age 18 or older. |
| `eligibility_us_resident` | boolean | `true`, `false` | Public | Whether respondent resides in the United States. |
| `eligibility_english_self_administered` | boolean | `true`, `false` | Public | Whether respondent can complete the English survey unaided. |
| `analytic_eligible` | boolean | `true`, `false` | Public | Respondent is eligible after consent, population criteria, duplicate review, breakoff review, and preregistered QC exclusions. |

## Covariates

### Demographics And Quotas

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `age_group` | string | `18_29`, `30_44`, `45_59`, `60_plus` | Public | Preregistered quota and DIF category. |
| `gender` | string | `woman`, `man`, `nonbinary_another_gender`, `prefer_not_to_answer` | Public, subject to suppression | Gender category for quotas, DIF, and descriptive reporting. |
| `race_ethnicity` | string | `hispanic_latino`, `non_hispanic_white`, `non_hispanic_black`, `non_hispanic_asian`, `non_hispanic_other_multiracial`, `prefer_not_to_answer` | Public, subject to suppression | Race and ethnicity category used for quotas, weighting, and DIF. |
| `education` | string | `high_school_or_less`, `some_college_associate`, `bachelors`, `graduate`, `prefer_not_to_answer` | Public | Highest educational attainment. |
| `census_region` | string | `northeast`, `midwest`, `south`, `west` | Public | US Census region. |
| `employment_status` | string | `employed_full_time`, `employed_part_time`, `self_employed`, `unemployed_looking`, `student`, `retired`, `not_in_labor_force_other`, `prefer_not_to_answer` | Public | Current employment status. |
| `occupation_group` | string | Harmonized broad occupation category or `not_currently_employed`, `other`, `prefer_not_to_answer` | Public, subject to coarsening | Broad occupation group used for descriptive heterogeneity and disclosure review. |

### AI Exposure

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `prior_ai_exposure_frequency` | string | `never_rare`, `monthly`, `weekly`, `daily_near_daily`, `prefer_not_to_answer` | Public | Frequency of using generative AI tools such as chatbots, image generators, coding assistants, or AI search tools. |
| `ai_use_work_or_school` | string | `never`, `less_than_monthly`, `monthly`, `weekly`, `daily_near_daily`, `not_applicable`, `prefer_not_to_answer` | Public | Frequency of AI tool use for work or school tasks. |
| `ai_use_personal` | string | `never`, `less_than_monthly`, `monthly`, `weekly`, `daily_near_daily`, `prefer_not_to_answer` | Public | Frequency of AI tool use for personal tasks. |
| `ai_news_exposure_30d` | integer | 1 `not_at_all`, 2 `less_than_once_a_week`, 3 `about_once_a_week`, 4 `several_times_a_week`, 5 `daily_almost_daily`, 9 `prefer_not_to_answer` | Public | Frequency of exposure to AI capability news or commentary during the past 30 days. |
| `self_rated_ai_familiarity` | integer | 1 to 5, where 1 is not familiar and 5 is very familiar; 9 prefer not to answer | Public | General familiarity with AI capabilities. |

### Sleep Sensitivity, Health Anxiety, And Baseline General Anxiety

| Variable | Type | Allowed values or coding | Scoring direction | Public data status | Missingness rule | Definition |
| --- | --- | --- | --- | --- | --- | --- |
| `sleep_sensitivity_stress_news` | integer | 1 `not_at_all_easily`, 2 `slightly_easily`, 3 `moderately_easily`, 4 `very_easily`, 5 `extremely_easily`, 9 `prefer_not_to_answer` | Higher valid values indicate greater sleep sensitivity to stressful news or worries. | Public | Required screen. If no value is captured, code null and set `covariate_item_missing`. Value 9 is retained as prefer not to answer and excluded from numeric covariate scoring. | Covariate for sleep vulnerability that may affect responses to `sleep_disruption_ai_news`. |
| `health_anxiety_body_sensation_worry` | integer | 1 `never_almost_never`, 2 `rarely`, 3 `sometimes`, 4 `often`, 5 `very_often`, 9 `prefer_not_to_answer` | Higher valid values indicate greater tendency to worry about body sensations. | Public | Required screen. If no value is captured, code null and set `covariate_item_missing`. Value 9 is retained as prefer not to answer and excluded from numeric covariate scoring. | Covariate for health anxiety sensitivity that may affect bodily vigilance responses. |
| `baseline_general_anxiety_nervous_2w` | integer | 0 `not_at_all`, 1 `several_days`, 2 `more_than_half_the_days`, 3 `nearly_every_day`, 9 `prefer_not_to_answer` | Higher valid values indicate greater recent general anxiety. | Public | Required screen. If no value is captured, code null and set `covariate_item_missing`. Value 9 is retained as prefer not to answer and excluded from scoring. | General anxiety covariate asking about feeling nervous, tense, or on edge during the past 2 weeks. |
| `baseline_general_anxiety_worry_2w` | integer | 0 `not_at_all`, 1 `several_days`, 2 `more_than_half_the_days`, 3 `nearly_every_day`, 9 `prefer_not_to_answer` | Higher valid values indicate greater recent general worry. | Public | Required screen. If no value is captured, code null and set `covariate_item_missing`. Value 9 is retained as prefer not to answer and excluded from scoring. | General anxiety covariate asking about difficulty stopping or controlling ordinary-life worry during the past 2 weeks. |
| `baseline_general_anxiety_2item_mean` | number or null | Mean of valid 0 to 3 values from the two baseline general anxiety items, range 0.00 to 3.00 | Higher values indicate higher recent general anxiety. | Public | Compute when at least one source item has a valid 0 to 3 response. Do not impute prefer not to answer. | Two-item general anxiety covariate used for discriminant and incremental-validity analyses. |
| `baseline_general_anxiety_2item_valid_n` | integer | 0, 1, 2 | Not a score. | Public | Count valid 0 to 3 responses among the two baseline general anxiety items. | Completeness indicator for the baseline general anxiety covariate. |
| `covariate_item_missing` | boolean | `true`, `false` | Not a score. | Public | Set `true` if any required covariate screen has null because no response was captured. Prefer not to answer values do not by themselves set this flag. | Respondent-level indicator that a required non-ANX covariate was technically missing or skipped despite required status. |

### External-Validity Criteria

| Variable | Type | Allowed values or coding | Scoring direction | Public data status | Missingness rule | Definition |
| --- | --- | --- | --- | --- | --- | --- |
| `ai_information_avoidance_intention_6m` | integer | 1 `very_unlikely`, 2 `somewhat_unlikely`, 3 `neither_likely_nor_unlikely`, 4 `somewhat_likely`, 5 `very_likely`, 9 `prefer_not_to_answer` | Higher valid values indicate stronger intended avoidance of AI-related information. | Public | Required screen. Value 9 is retained as prefer not to answer and excluded from criterion scoring. | Criterion variable expected to correlate positively with retained somatic and ambient anxiety scores. |
| `ai_information_checking_intention_6m` | integer | 1 `very_unlikely`, 2 `somewhat_unlikely`, 3 `neither_likely_nor_unlikely`, 4 `somewhat_likely`, 5 `very_likely`, 9 `prefer_not_to_answer` | Higher valid values indicate stronger intended information seeking despite discomfort. | Public | Required screen. Value 9 is retained as prefer not to answer and excluded from criterion scoring. | Criterion variable expected to be weakly negative, null, or curvilinear after adjustment because anxious respondents may either avoid or monitor AI information. |

## Quality Control Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `attention_check_response` | integer | 1 to 5 | Restricted or public summary | Response to the instructed-response attention check. |
| `attention_check_passed` | boolean | `true`, `false` | Public | `true` only when `attention_check_response == 3`. Failed respondents receive `attention_check_failed`. |
| `scenario_comprehension_response` | integer | 1 to 4 | Restricted or public summary | Response to the required scenario-comprehension check. |
| `scenario_comprehension_passed` | boolean | `true`, `false` | Public | `true` only when response is 1. Failed respondents receive `other_preregistered_exclusion` with restricted reason `scenario_comprehension_failed`. |
| `somatic_attribution_response` | integer | 1 to 4 | Restricted or public summary | Response to the somatic-attribution check. |
| `somatic_attribution_passed` | boolean | `true`, `false` | Public | `true` only when response is 1. Failed respondents receive `other_preregistered_exclusion` with restricted reason `somatic_attribution_failed`. |
| `self_reported_understanding` | integer | 1 to 5 | Public | Response to the understanding check. Values 4 and 5 trigger `quality_review_failed`. |
| `duplicate_review_status` | string | `not_duplicate`, `duplicate_confirmed`, `duplicate_possible_unconfirmed` | Restricted summary public | Duplicate review result from vendor IDs, survey tokens, and device or fingerprint evidence. |
| `vendor_quality_status` | string | `passed`, `low_confidence`, `failed`, `not_provided` | Restricted summary public | Vendor fraud or quality flag. Vendor-failed completes receive `quality_review_failed` unless manual review overturns the flag before outcome inspection. |
| `straightline_anx_block` | boolean | `true`, `false` | Public | `true` when the same substantive response is given to all four ANX items. Exclusion requires straightlining plus failed attention check or minimum reading-time check. |
| `anx_items_missing_count` | integer | 0 to 4 | Public | Number of ANX items without observed response. |
| `anx_items_missing_prop` | number | 0.00 to 1.00 | Public | Missing ANX item count divided by 4. Greater than 0.25 triggers exclusion because one missing item is 25 percent of the four-item pool and two missing items prevent stable construct diagnostics. |
| `speeding_flag` | boolean | `true`, `false` | Public | `true` when survey completion time is less than one-third of the median completion time for the same sample after removing clear breakoffs. |
| `minimum_reading_time_flag` | boolean | `true`, `false` | Public | `true` when ANX block or item times indicate less than one-third of sample median reading time under the preregistered rule. |
| `open_text_quality_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment indicates confusion, satire, protest responding, or failure to treat scenarios as AI-related. Does not exclude by itself. |
| `distress_review_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment suggests notable respondent distress. Used for ethics monitoring, not automatic exclusion. |
| `final_exclusion_flags` | array of strings | Values allowed by `schema/wave_response.schema.json` | Public | Respondent-level flags propagated to all respondent-item rows when applicable. |

## Response Time And Paradata Variables

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
| `somatic_attribution_check_time_seconds` | number | 0 or greater | Restricted | Time on the somatic-attribution check screen. |
| `covariate_module_duration_seconds` | number | 0 or greater | Restricted or public summary | Time spent on sleep sensitivity, health anxiety, AI-news exposure, baseline anxiety, and criterion screens. |
| `page_backtracking_count` | integer | 0 or greater | Restricted | Count of detected back navigation or page revisits, if available. |
| `technical_error_flag` | boolean | `true`, `false` | Restricted summary public | Platform error affecting survey presentation or response capture. |

## Weights And Quota Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `quota_age_group` | string | Same as `age_group` | Public | Age group used for quota monitoring. |
| `quota_gender` | string | Same as `gender` with vendor harmonization documented | Public | Gender category used for quota monitoring. |
| `quota_race_ethnicity` | string | Same as `race_ethnicity` | Public | Race and ethnicity category used for quota monitoring. |
| `quota_education` | string | Same as `education` | Public | Education category used for quota monitoring. |
| `quota_census_region` | string | Same as `census_region` | Public | Region category used for quota monitoring. |
| `quota_ai_news_exposure_30d` | integer | Same as `ai_news_exposure_30d` after collapsing if needed | Public | AI-news exposure category used for quota monitoring or imbalance diagnostics. |
| `base_weight` | number | Positive number | Restricted or public | Design or vendor base weight before post-stratification. |
| `poststrat_weight` | number | Positive number | Public | Weight after raking or post-stratification. |
| `final_weight` | number | Positive number, target trimmed range 0.30 to 3.00 | Public | Final analysis weight mapped to `survey_weight` in every respondent-item row. |
| `weight_trimmed` | boolean | `true`, `false` | Public | Whether the respondent's post-stratification weight was trimmed. |

## Missingness And Public-Data Exclusions

Prefer-not-to-answer options are retained as explicit categories for demographic, AI exposure, sleep sensitivity, health anxiety, and baseline general anxiety variables. ANX item skipped responses are not coded as prefer not to answer because the ANX item screens do not present that option. For respondent-item rows, missingness must follow `schema/wave_response.schema.json`.

The following variables may exist only in restricted operations files and must never appear in public analytic files: `vendor_panelist_id`, `vendor_survey_token`, `vendor_project_id`, `vendor_session_id`, `vendor_transaction_id`, `ip_address`, `ip_geolocation`, `device_fingerprint`, `browser_user_agent_raw`, `panel_profile_raw_json`, `open_text_debrief_raw`, and `hash_salt_or_linkage_key`.

Before public release, the data steward must review cross-classified cells involving age group, gender, race and ethnicity, region, education, employment status, AI exposure, sleep sensitivity, health anxiety sensitivity, baseline general anxiety, device type, and fielding date. Small cells must be suppressed, combined, or moved to restricted access. Exact timestamps, raw comments, direct vendor identifiers, raw device fields, and linkage materials are always restricted.
