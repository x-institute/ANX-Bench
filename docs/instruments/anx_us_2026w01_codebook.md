# ANX-Bench US 2026 Wave 1 Codebook

## Codebook Control

- Wave ID: `anx_us_2026w01`
- Study label: `anx_us_2026w01_calibration`
- Benchmark release: `v0.1.0`
- Codebook version: `anx_us_2026w01_codebook`
- Freeze date: `2026-06-15`
- Paired instrument: `docs/instruments/anx_us_2026w01_instrument.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w01_calibration.md`
- Canonical respondent-item schema: `schema/wave_response.schema.json`
- Canonical behavioral-response schema: `schema/behavioral_response.schema.json`

This codebook defines every non-ANX variable collected, appended, derived, or retained for Wave 1. ANX item responses are defined by the item JSON files in `items/v0.1` and represented in public or restricted analytic files as one row per respondent per item under `schema/wave_response.schema.json`. The behavioral validation task is represented as one row per respondent under `schema/behavioral_response.schema.json`. Variables in this codebook describe respondent eligibility, sampling, demographics, occupation, AI exposure, behavioral criterion validation, quality control, paradata, weighting, and restricted vendor operations.

## File Families

Wave 1 data are split into three file families.

| File family | Access level | Contents |
| --- | --- | --- |
| Canonical respondent-item analytic file | Public or restricted according to disclosure review | One row per respondent-item response validating against `schema/wave_response.schema.json`. Includes only schema fields and no direct vendor IDs. |
| Behavioral criterion analytic file | Public or restricted according to disclosure review | One row per respondent for the revealed AI review allocation task validating against `schema/behavioral_response.schema.json`. Includes randomized task arm, allocation cents, comprehension check, exclusion flags, and derived `revealed_anxiety_score`. |
| Respondent-level analytic covariate file | Public or restricted according to disclosure review | One row per respondent with demographics, occupation, AI exposure, quota variables, weights, QC summaries, and disclosure-safe paradata defined below. |
| Restricted operations file | Restricted, not public | Vendor respondent IDs, vendor survey tokens, duplicate-detection fields, device fingerprints, IP-derived fraud flags, exact timestamps when not disclosure-safe, raw open-text debrief comments, and linkage materials needed for audit. |

Public files must exclude direct identifiers and vendor IDs. Restricted files may be used to reproduce exclusions and linkage, but must not be merged into public releases.

## Mapping Into `wave_response.schema.json`

The canonical respondent-item file must contain the following schema fields for every administered ANX item.

| Schema field | Wave 1 source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w01`. |
| `benchmark_version` | Constant `v0.1.0`. |
| `item_id` | Item ID from the randomized ANX screen presented to the respondent. Allowed IDs are the 14 item IDs listed in the Wave 1 administered ANX item allowlist below and in the paired instrument. |
| `item_version` | Constant `v0.1.0` for every Wave 1 ANX item. |
| `respondent_id_hash` | Study-scoped salted SHA-256 or stronger keyed hash of the restricted respondent linkage key. The salt is stored outside analytic data. |
| `raw_response` | Numeric response `1` to `5` from the ANX item screen, or null if no answer was captured. Vendor labels must be mapped back to numeric anchors before analytic export. |
| `scored_value` | For observed non-excluded item responses, equal to `raw_response` because all Wave 1 items use non-reverse-coded 1 to 5 scoring. Null when missingness or exclusion prevents scoring. |
| `response_timestamp` | UTC timestamp when the item response was submitted or finalized. Public files may coarsen precision only if the coarsening is documented and does not affect planned analyses. |
| `administration_mode` | `web` for desktop or laptop browser completes and `mobile_web` for phone or tablet browser completes. Other modes are protocol deviations. |
| `language` | Constant `en-US`. |
| `survey_weight` | Final respondent-level analysis weight for the relevant sample. Use `1.0` until final weights are constructed. |
| `exclusion_flags` | Array derived from respondent-level and row-level QC variables. Empty array means no exclusion flag applies. |
| `missingness_code` | `observed`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, `not_scored_item_ineligible`, or `not_scored_excluded_respondent`, as applicable. |
| `event_id` | Omit for Wave 1 calibration unless a separately preregistered event-study addendum exists. |
| `event_exposure_window` | Omit for Wave 1 calibration unless a separately preregistered event-study addendum exists. |
| `baseline_or_followup` | Omit for Wave 1 calibration unless a separately preregistered longitudinal addendum exists. |
| `fielding_time_relative_to_event_hours` | Omit for Wave 1 calibration unless a separately preregistered event-study addendum exists. |

## Mapping Into `behavioral_response.schema.json`

The behavioral criterion analytic file must contain exactly one row per respondent who reaches, is assigned to, or should have reached the behavioral review allocation task. The task is a validation criterion, not an ANX item. It must not appear in respondent-item rows and must not contribute to ANX item, construct, domain, overall, longitudinal, or event-study scores.

| Schema field | Wave 1 source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w01`. |
| `respondent_id` | Same study-scoped salted SHA-256 or stronger keyed hash used as `respondent_id_hash` in respondent-item and respondent-level analytic files. Raw vendor IDs are prohibited. |
| `task_id` | Constant `revealed_ai_review_allocation_v1`. |
| `benchmark_version` | Constant `v0.1.0`. |
| `randomized_arm` | Uniform respondent-level assignment to `employment_hiring`, `healthcare_triage`, `public_benefits`, or `school_placement` from Screen 7 of the fielding instrument. |
| `allocation_mode` | Constant `bonus_stated` for Wave 1 unless a dated preregistration addendum and vendor payment protocol implement real bonus allocation before recruitment. |
| `ai_only_review_cents` | Integer cents allocated to AI-only review, 0 to 100. Null when the task was not displayed, not submitted, or technically failed. |
| `human_review_cents` | Integer cents allocated to human review, 0 to 100. Null when the task was not displayed, not submitted, or technically failed. |
| `allocation_total_cents` | Sum of `ai_only_review_cents` and `human_review_cents`; must equal 100 for observed valid rows. |
| `allocation_confirmed` | `true` only when the respondent actively submitted or confirmed the allocation. |
| `behavioral_comprehension_response` | Integer response 1 to 4 to the required behavioral comprehension check. |
| `behavioral_comprehension_passed` | `true` only when `behavioral_comprehension_response == 1`. |
| `exclusion_flags` | Behavioral and respondent-level flags that affect confirmatory behavioral criterion-validity analyses. Empty array means no exclusion flag applies. |
| `missingness_code` | `observed`, `not_presented_by_design`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, or `not_scored_excluded_respondent`, as applicable. |
| `revealed_anxiety_score` | Equal to `human_review_cents / 100` for observed valid rows; null when the task is missing, invalid, or excluded from behavioral scoring. |

## Behavioral Criterion Validation Variables

These variables are collected in Screen 7 after the ANX item block and survey-level checks, before in-survey demographics. They are criterion variables for behavioral validation and must remain separate from ANX item responses. Public release is permitted after disclosure review because no direct identifiers, raw vendor IDs, or open text are included.

| Variable | Type | Allowed values or coding | Scoring direction | Public data status | Missingness rule | Definition |
| --- | --- | --- | --- | --- | --- | --- |
| `task_id` | string | `revealed_ai_review_allocation_v1` | Not a score. | Public | Constant for all respondents assigned to the task. | Identifier for the standardized revealed AI review allocation task. |
| `randomized_arm` | string | `employment_hiring`, `healthcare_triage`, `public_benefits`, `school_placement` | Not a score. | Public | Required for task-assigned respondents. If missing because randomization failed, set `behavioral_task_not_presented` or `technical_failure` as appropriate. | Randomized high-impact AI decision vignette shown before the allocation choice. |
| `allocation_mode` | string | `bonus_stated`, `real_bonus` | Not a score. | Public | Required for task-assigned respondents. | Whether the allocation was stated for research only or tied to a real bonus implementation. Wave 1 defaults to `bonus_stated`. |
| `ai_only_review_cents` | integer or null | 0 to 100 | Lower values imply less revealed preference for AI-only review. | Public | Null if task was not shown, allocation was not submitted, respondent broke off before submission, or technical capture failed. | Cents allocated to AI-only review. |
| `human_review_cents` | integer or null | 0 to 100 | Higher values imply stronger revealed preference for human review. | Public | Null if task was not shown, allocation was not submitted, respondent broke off before submission, or technical capture failed. | Cents allocated to human review. |
| `allocation_total_cents` | integer or null | 100 for valid observed rows | Not a score. | Public | Null if either allocation component is null. Values other than 100 trigger `behavioral_allocation_invalid`. | Sum of AI-only and human-review allocation cents. |
| `allocation_confirmed` | boolean | `true`, `false` | Not a score. | Public | `false` if the respondent did not actively submit or confirm the allocation. | Interface confirmation indicator required for valid behavioral scoring. |
| `behavioral_comprehension_response` | integer or null | 1 to 4 | Not a score. | Restricted or public summary | Null if not captured because of breakoff or technical failure. | Response to the task comprehension check asking what was divided. |
| `behavioral_comprehension_passed` | boolean or null | `true`, `false`, null | Not a score. | Public | Null only when the check was not administered or not captured. | `true` only when the respondent selects option 1, a $1.00 review budget between AI-only review and human review. |
| `revealed_anxiety_score` | number or null | 0.00 to 1.00 in 0.01 increments | Higher values indicate greater revealed preference for human review over AI-only review. | Public | Compute only when allocation is valid, allocation is confirmed, and behavioral comprehension is passed. Null otherwise. | Derived behavioral criterion score equal to `human_review_cents / 100`. |
| `behavioral_missingness_code` | string | Same allowed values as `schema/behavioral_response.schema.json` | Not a score. | Public | Required for every behavioral row. | Reason the behavioral score is present or absent. |
| `behavioral_exclusion_flags` | array of strings | Values allowed by `schema/behavioral_response.schema.json` | Not a score. | Public | Empty array if no behavioral exclusion applies. | Behavioral and respondent-level exclusions used for confirmatory behavioral validity models. |

### Behavioral Scoring Rubric

The primary behavioral criterion score is:

`revealed_anxiety_score = human_review_cents / 100`

Examples:

| Human review cents | AI-only review cents | `revealed_anxiety_score` |
| ---: | ---: | ---: |
| 0 | 100 | 0.00 |
| 25 | 75 | 0.25 |
| 50 | 50 | 0.50 |
| 75 | 25 | 0.75 |
| 100 | 0 | 1.00 |

Rows fail behavioral scoring when allocation cents are outside 0 to 100, are non-integer, do not sum to 100, lack active confirmation when required, or fail the behavioral comprehension check. Failed behavioral scoring does not automatically remove the respondent from ANX psychometric analyses unless a separate preregistered survey-level exclusion also applies.

## Wave 1 Administered ANX Item Allowlist

The following 14 item IDs are the only ANX item IDs allowed in Wave 1 respondent-item rows. The item ID, version, domain, and construct ID must match the frozen fielding instrument, Wave 1 preregistration, and `releases/v0.1.0/manifest.json`. Vendor exports must not add, drop, rename, recode, or substitute ANX items without a dated preregistration addendum and a new release packet.

| Domain | Item ID | Version | Construct ID |
| --- | --- | --- | --- |
| autonomy_surveillance | `institutional_scoring_automation` | `v0.1.0` | `autonomy_surveillance_ai_anxiety_anchor` |
| economic_vocational | `job_displacement_radiology` | `v0.1.0` | `anticipated_job_displacement_anxiety` |
| economic_vocational | `retraining_pressure_accounting` | `v0.1.0` | `economic_vocational_anxiety` |
| economic_vocational | `skill_obsolescence_software` | `v0.1.0` | `economic_vocational_anxiety` |
| economic_vocational | `status_loss_creative_work` | `v0.1.0` | `economic_vocational_anxiety` |
| economic_vocational | `wage_pressure_customer_support` | `v0.1.0` | `economic_vocational_anxiety` |
| epistemic | `ai_expert_claim_conflict` | `v0.1.0` | `epistemic_trust_anxiety` |
| epistemic | `deepfake_evidence_trust` | `v0.1.0` | `epistemic_trust_anxiety` |
| epistemic | `personalized_misinformation_targeting` | `v0.1.0` | `epistemic_trust_anxiety` |
| epistemic | `synthetic_news_provenance` | `v0.1.0` | `epistemic_trust_anxiety` |
| existential_identity | `creativity_status_displacement` | `v0.1.0` | `existential_identity_ai_anxiety_anchor` |
| relational | `child_companion_attachment` | `v0.1.0` | `relational_ai_anxiety_anchor` |
| safety_catastrophic | `ai_enabled_systemic_harm` | `v0.1.0` | `safety_catastrophic_ai_anxiety_anchor` |
| somatic_ambient | `ambient_bodily_unease` | `v0.1.0` | `somatic_ambient_ai_anxiety_anchor` |

## Respondent-Level Identifiers And Sample Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Public or restricted | Study-scoped salted respondent identifier used to join respondent-level covariates to respondent-item rows. |
| `sample_id` | string | `development_pilot`, `confirmation` | Public | Non-overlapping Wave 1 sample. |
| `wave_id` | string | `anx_us_2026w01` | Public | Wave identifier. |
| `benchmark_version` | string | `v0.1.0` | Public | Release governing administered item versions. |
| `survey_start_timestamp_utc` | datetime | ISO 8601 UTC | Restricted or coarsened | Survey start time. Public files may coarsen to date or hour after disclosure review. |
| `survey_end_timestamp_utc` | datetime | ISO 8601 UTC | Restricted or coarsened | Survey completion or breakoff time. |
| `survey_duration_seconds` | integer | 0 or greater | Public | End timestamp minus start timestamp after removing known platform pauses if vendor provides validated pause metadata. |
| `complete_status` | string | `complete`, `screenout`, `breakoff`, `quota_full`, `nonconsent`, `vendor_quality_termination` | Restricted summary public | Operational completion status before analytic exclusions. |
| `consent_status` | string | `agreed`, `declined`, `withdrawn` | Restricted summary public | Consent disposition from Screen 1. |
| `eligibility_age_18_plus` | boolean | `true`, `false` | Public | Whether respondent confirmed or profile data indicated age 18 or older. |
| `eligibility_us_resident` | boolean | `true`, `false` | Public | Whether respondent resides in the United States. |
| `eligibility_english_self_administered` | boolean | `true`, `false` | Public | Whether respondent can complete the English survey unaided. |
| `analytic_eligible` | boolean | `true`, `false` | Public | Respondent is eligible after consent, population criteria, duplicate review, breakoff review, and preregistered QC exclusions. |

## Demographics

Demographic variables may be asked in the survey or appended from vendor profile records. If appended, the vendor must document field recency. Public data may coarsen categories when needed for disclosure control.

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `age_years` | integer | 18 to 120 | Restricted or binned | Respondent age in years. Public files should use `age_group` unless exact age passes disclosure review. |
| `age_group` | string | `18_29`, `30_44`, `45_59`, `60_plus` | Public | Preregistered quota and DIF category. |
| `gender` | string | `woman`, `man`, `nonbinary_another_gender`, `prefer_not_to_answer` | Public, subject to suppression | Gender category for quotas, DIF, and descriptive reporting. |
| `race_ethnicity` | string | `hispanic_latino`, `non_hispanic_white`, `non_hispanic_black`, `non_hispanic_asian`, `non_hispanic_other_multiracial`, `prefer_not_to_answer` | Public, subject to suppression | Race and ethnicity category used for quotas and weighting. |
| `education` | string | `high_school_or_less`, `some_college_associate`, `bachelors`, `graduate`, `prefer_not_to_answer` | Public | Highest educational attainment. |
| `census_region` | string | `northeast`, `midwest`, `south`, `west` | Public | US Census region. |
| `household_income_group` | string | `under_25000`, `25000_49999`, `50000_74999`, `75000_99999`, `100000_149999`, `150000_or_more`, `prefer_not_to_answer` | Public, subject to coarsening | Annual household income before taxes. |
| `urbanicity` | string | `urban`, `suburban`, `rural`, `prefer_not_to_answer` | Public | Respondent's self-described community type or vendor-coded equivalent. |
| `political_party_or_ideology` | string | Vendor harmonized categories | Restricted or coarsened | Party identification or ideology if collected by vendor profile. Used only for preregistered DIF sensitivity if adequate cell sizes exist. |

## Occupation And Labor Variables

Occupation data support economic/vocational subgroup analyses without collecting employer names.

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `employment_status` | string | `employed_full_time`, `employed_part_time`, `self_employed`, `unemployed_looking`, `student`, `retired`, `not_in_labor_force_other`, `prefer_not_to_answer` | Public | Current employment status. |
| `occupation_group` | string | `management_business_finance`, `computer_mathematical`, `architecture_engineering`, `life_physical_social_science`, `community_social_service`, `legal`, `education_training_library`, `arts_design_entertainment_media`, `healthcare_practitioner_technical`, `healthcare_support`, `protective_service`, `food_cleaning_personal_service`, `sales_office_admin`, `construction_extraction_maintenance`, `production_transportation_material_moving`, `military`, `not_currently_employed`, `other`, `prefer_not_to_answer` | Public, subject to coarsening | Broad occupation group harmonized from respondent answer or vendor profile. |
| `occupation_soc_major_group` | string | Two-digit SOC major group where available, otherwise null | Restricted or coarsened | Standard Occupational Classification major group. |
| `supervisory_status` | string | `supervises_others`, `does_not_supervise`, `not_applicable`, `prefer_not_to_answer` | Public | Whether respondent supervises others at work. |
| `health_care_employment` | boolean or null | `true`, `false`, null | Public, subject to suppression | Whether respondent currently works in health care or health services. |
| `software_or_it_employment` | boolean or null | `true`, `false`, null | Public, subject to suppression | Whether respondent currently works in software, IT, data, or related technical roles. |
| `creative_work_employment` | boolean or null | `true`, `false`, null | Public, subject to suppression | Whether respondent currently works in arts, design, writing, media, entertainment, advertising, or similar creative work. |
| `customer_support_employment` | boolean or null | `true`, `false`, null | Public, subject to suppression | Whether respondent currently works in customer support, call centers, help desks, or related service roles. |
| `accounting_finance_employment` | boolean or null | `true`, `false`, null | Public, subject to suppression | Whether respondent currently works in accounting, audit, bookkeeping, tax, finance, or related roles. |

## AI Exposure Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `prior_ai_exposure_frequency` | string | `never_rare`, `monthly`, `weekly`, `daily_near_daily`, `prefer_not_to_answer` | Public | Frequency of using generative AI tools such as chatbots, image generators, coding assistants, or AI search tools. |
| `ai_use_work_or_school` | string | `never`, `less_than_monthly`, `monthly`, `weekly`, `daily_near_daily`, `not_applicable`, `prefer_not_to_answer` | Public | Frequency of AI tool use for work or school tasks. |
| `ai_use_personal` | string | `never`, `less_than_monthly`, `monthly`, `weekly`, `daily_near_daily`, `prefer_not_to_answer` | Public | Frequency of AI tool use for personal tasks. |
| `ai_news_following` | string | `not_at_all`, `a_little`, `somewhat`, `closely`, `very_closely`, `prefer_not_to_answer` | Public | Self-reported attention to news about AI. |
| `self_rated_ai_familiarity` | integer | 1 to 5, where 1 is not familiar and 5 is very familiar | Public | General familiarity with AI capabilities. |
| `ai_workplace_exposure` | string | `employer_uses_ai`, `employer_considering_ai`, `no_known_workplace_ai`, `not_employed`, `prefer_not_to_answer` | Public | Whether respondent's workplace uses or is considering AI tools. |

## Post-ANX External Validation Variables

These variables are collected after the randomized ANX item block and required quality-control checks. They are validation comparators and criterion variables, not ANX-Bench scored items. They must not be included in ANX item rows, construct scores, domain scores, overall ANX scores, longitudinal ANX indices, or event-study ANX outcomes. Public release is permitted after disclosure review because no direct identifiers or sensitive open text are collected in this module.

| Variable | Type | Allowed values or coding | Scoring direction | Public data status | Missingness rule | Definition |
| --- | --- | --- | --- | --- | --- | --- |
| `gen_anxiety_nervous_2w` | integer | 0 `not_at_all`, 1 `several_days`, 2 `more_than_half_the_days`, 3 `nearly_every_day`, 9 `prefer_not_to_answer` | Higher values 0 to 3 indicate higher recent general anxiety. Value 9 is not scored. | Public | Required screen. If no value is captured, code null and set respondent-level validation missingness flag `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from scale scoring. | General anxiety screener item asking about feeling nervous, tense, or on edge during the past 2 weeks. |
| `gen_anxiety_worry_2w` | integer | 0 `not_at_all`, 1 `several_days`, 2 `more_than_half_the_days`, 3 `nearly_every_day`, 9 `prefer_not_to_answer` | Higher values 0 to 3 indicate higher recent general anxiety. Value 9 is not scored. | Public | Required screen. If no value is captured, code null and set respondent-level validation missingness flag `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from scale scoring. | General anxiety screener item asking about difficulty stopping or controlling ordinary-life worry during the past 2 weeks. |
| `general_anxiety_2item_mean` | number or null | Mean of valid `gen_anxiety_nervous_2w` and `gen_anxiety_worry_2w` values from 0.00 to 3.00; null if neither item has a valid 0 to 3 response. | Higher values indicate higher recent general anxiety. | Public | Compute when at least one of the two source items has a valid 0 to 3 response. Do not impute prefer not to answer. Record the valid item count in `general_anxiety_2item_valid_n`. | Two-item general anxiety comparator used as a covariate and discriminant-validity control. |
| `general_anxiety_2item_valid_n` | integer | 0, 1, 2 | Not a score. | Public | Count valid 0 to 3 responses among the two general anxiety screener items. | Completeness indicator for the two-item general anxiety comparator. |
| `tech_ai_uneasy_useful` | integer | 1 `strongly_disagree`, 2 `somewhat_disagree`, 3 `neither_agree_nor_disagree`, 4 `somewhat_agree`, 5 `strongly_agree`, 9 `prefer_not_to_answer` | Higher values 1 to 5 indicate higher AI and technology anxiety. Value 9 is not scored. | Public | Required statement. If no value is captured, code null and set `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from comparator scoring. | AI-specific comparator item measuring unease about useful AI tools. |
| `tech_digital_optimism` | integer | 1 `strongly_disagree`, 2 `somewhat_disagree`, 3 `neither_agree_nor_disagree`, 4 `somewhat_agree`, 5 `strongly_agree`, 9 `prefer_not_to_answer` | Reverse scored for the anxiety comparator so higher scored values indicate lower digital optimism and higher technology anxiety. Value 9 is not scored. | Public | Required statement. If no value is captured, code null and set `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from comparator scoring. | Technology attitude comparator item measuring expectation that new digital technologies improve the respondent's life. |
| `tech_ai_complexity_worry` | integer | 1 `strongly_disagree`, 2 `somewhat_disagree`, 3 `neither_agree_nor_disagree`, 4 `somewhat_agree`, 5 `strongly_agree`, 9 `prefer_not_to_answer` | Higher values 1 to 5 indicate higher AI and technology anxiety. Value 9 is not scored. | Public | Required statement. If no value is captured, code null and set `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from comparator scoring. | AI-specific comparator item measuring worry that AI systems are too difficult for ordinary people to understand. |
| `tech_ai_responsible_trust` | integer | 1 `strongly_disagree`, 2 `somewhat_disagree`, 3 `neither_agree_nor_disagree`, 4 `somewhat_agree`, 5 `strongly_agree`, 9 `prefer_not_to_answer` | Reverse scored for the anxiety comparator so higher scored values indicate lower trust and higher technology anxiety. Value 9 is not scored. | Public | Required statement. If no value is captured, code null and set `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from comparator scoring. | Technology attitude comparator item measuring trust in responsible organizational AI use when rules are in place. |
| `tech_ai_anxiety_comparator_mean` | number or null | Mean of scored validation values from the four technology and AI attitude items, range 1.00 to 5.00 after reverse scoring `tech_digital_optimism` and `tech_ai_responsible_trust`; null if fewer than two valid source items are available. | Higher values indicate higher AI and technology anxiety. | Public | Compute only when at least two of four source items have valid 1 to 5 responses. Do not impute null or prefer not to answer values. Record valid item count in `tech_ai_anxiety_comparator_valid_n`. | Multi-item AI and technology anxiety comparator for convergent-validity analyses. |
| `tech_ai_anxiety_comparator_valid_n` | integer | 0, 1, 2, 3, 4 | Not a score. | Public | Count valid 1 to 5 responses among the four technology and AI attitude items. | Completeness indicator for the AI and technology anxiety comparator. |
| `ai_avoidance_intention_6m` | integer | 1 `very_unlikely`, 2 `somewhat_unlikely`, 3 `neither_likely_nor_unlikely`, 4 `somewhat_likely`, 5 `very_likely`, 9 `prefer_not_to_answer` | Higher values 1 to 5 indicate stronger AI avoidance intention. Value 9 is not scored. | Public | Required screen. If no value is captured, code null and set `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from criterion scoring. | Criterion variable measuring intention to avoid AI tools during the next 6 months when a reasonable non-AI alternative is available. |
| `ai_adoption_intention_6m` | integer | 1 `very_unlikely`, 2 `somewhat_unlikely`, 3 `neither_likely_nor_unlikely`, 4 `somewhat_likely`, 5 `very_likely`, 9 `prefer_not_to_answer` | Higher values 1 to 5 indicate stronger AI adoption intention. Value 9 is not scored. | Public | Required screen. If no value is captured, code null and set `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from criterion scoring. | Criterion variable measuring intention to try an available AI tool for a personal, work, school, or household task during the next 6 months. |
| `ai_regulation_support_high_impact` | integer | 1 `strongly_oppose`, 2 `somewhat_oppose`, 3 `neither_support_nor_oppose`, 4 `somewhat_support`, 5 `strongly_support`, 9 `prefer_not_to_answer` | Higher values 1 to 5 indicate stronger support for AI regulation. Value 9 is not scored. | Public | Required screen. If no value is captured, code null and set `validation_item_missing`. Value 9 is retained as prefer not to answer and excluded from criterion scoring. | Criterion variable measuring support for stronger government rules for organizations deploying AI in high-impact settings. |
| `validation_item_missing` | boolean | `true`, `false` | Not a score. | Public | Set `true` if any required validation-module screen has null because no response was captured. Prefer not to answer values do not by themselves set this flag. | Respondent-level indicator that a required post-ANX validation variable was technically missing or skipped despite required status. |

## Quality Control Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `attention_check_response` | integer | 1 to 5 | Restricted or public summary | Response to the instructed-response attention check. |
| `attention_check_passed` | boolean | `true`, `false` | Public | `true` only when `attention_check_response == 3`. Failed respondents receive `attention_check_failed`. |
| `scenario_comprehension_response` | integer | 1 to 4 | Restricted or public summary | Response to the required scenario-comprehension check. |
| `scenario_comprehension_passed` | boolean | `true`, `false` | Public | `true` only when response is 1. Failed respondents receive `other_preregistered_exclusion` with restricted reason `scenario_comprehension_failed`. |
| `self_reported_understanding` | integer | 1 to 5 | Public | Response to the understanding check. Values 4 and 5 trigger `quality_review_failed`. |
| `duplicate_review_status` | string | `not_duplicate`, `duplicate_confirmed`, `duplicate_possible_unconfirmed` | Restricted summary public | Duplicate review result from vendor IDs, survey tokens, and device or fingerprint evidence. |
| `vendor_quality_status` | string | `passed`, `low_confidence`, `failed`, `not_provided` | Restricted summary public | Vendor fraud or quality flag. Vendor-failed completes receive `quality_review_failed` unless manual review overturns the flag before outcome inspection. |
| `straightline_anx_block` | boolean | `true`, `false` | Public | `true` when the same substantive response is given to every answered ANX item. Exclusion requires straightlining plus failed attention check or minimum reading-time check. |
| `anx_items_missing_count` | integer | 0 to 14 | Public | Number of ANX items without observed response. |
| `anx_items_missing_prop` | number | 0.00 to 1.00 | Public | Missing ANX item count divided by 14. Greater than 0.30 triggers exclusion. |
| `speeding_flag` | boolean | `true`, `false` | Public | `true` when survey completion time is less than one-third of the median completion time for the same sample after removing clear breakoffs. |
| `minimum_reading_time_flag` | boolean | `true`, `false` | Public | `true` when ANX block or item times indicate less than one-third of sample median reading time under the preregistered rule. |
| `open_text_quality_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment indicates confusion, satire, protest responding, or distress requiring review. Does not exclude by itself. |
| `distress_review_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment suggests notable respondent distress. Used for ethics monitoring, not automatic exclusion. |
| `final_exclusion_flags` | array of strings | Values allowed by `schema/wave_response.schema.json` | Public | Respondent-level flags propagated to all respondent-item rows when applicable. |

## Response Time And Paradata Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `device_type` | string | `desktop_laptop`, `mobile_tablet`, `unknown` | Public | Device category used for DIF screening and mode assignment. |
| `administration_mode` | string | `web`, `mobile_web` | Public | Mapped into schema field `administration_mode`. |
| `anx_block_order` | string or array | Ordered list of 14 item IDs | Restricted | Respondent-specific randomized item order. Public releases may provide item block position per row instead. |
| `item_block_position` | integer | 1 to 14 | Public | Position of the item in the respondent's randomized ANX block. |
| `item_response_time_seconds` | number | 0 or greater | Public or restricted | Time between item screen display and answer submission. Used for item-level response-time diagnostics. |
| `anx_block_duration_seconds` | number | 0 or greater | Public | Time from first ANX item display to final ANX item submission. |
| `attention_check_time_seconds` | number | 0 or greater | Restricted | Time on the attention-check screen. |
| `comprehension_check_time_seconds` | number | 0 or greater | Restricted | Time on the scenario-comprehension screen. |
| `page_backtracking_count` | integer | 0 or greater | Restricted | Count of detected back navigation or page revisits, if available. |
| `technical_error_flag` | boolean | `true`, `false` | Restricted summary public | Platform error affecting survey presentation or response capture. |

## Weights And Quota Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `quota_age_group` | string | Same as `age_group` | Public | Age group used for quota monitoring. |
| `quota_gender` | string | Same as `gender` with any vendor harmonization documented | Public | Gender category used for quota monitoring. |
| `quota_race_ethnicity` | string | Same as `race_ethnicity` | Public | Race and ethnicity category used for quota monitoring. |
| `quota_education` | string | Same as `education` | Public | Education category used for quota monitoring. |
| `quota_census_region` | string | Same as `census_region` | Public | Region category used for quota monitoring. |
| `quota_employment_status` | string | Same as `employment_status` | Public | Employment category used for quota monitoring. |
| `quota_prior_ai_exposure` | string | Same as `prior_ai_exposure_frequency` | Public | AI exposure category used for quota monitoring. |
| `base_weight` | number | Positive number | Restricted or public | Design or vendor base weight before post-stratification. |
| `poststrat_weight` | number | Positive number | Public | Weight after raking or post-stratification. |
| `final_weight` | number | Positive number, target trimmed range 0.30 to 3.00 | Public | Final analysis weight mapped to `survey_weight` in every respondent-item row. |
| `weight_trimmed` | boolean | `true`, `false` | Public | Whether the respondent's post-stratification weight was trimmed. |

## Vendor IDs Excluded From Public Data

The following variables may exist only in restricted operations files. They are never released in public analytic files and never appear in `schema/wave_response.schema.json`.

| Restricted variable | Reason retained | Public replacement |
| --- | --- | --- |
| `vendor_panelist_id` | Duplicate detection, payment audit, vendor reconciliation | `respondent_id_hash` |
| `vendor_survey_token` | Prevent repeated completes and verify disposition | None |
| `vendor_project_id` | Fielding audit | Wave-level metadata |
| `vendor_session_id` | Technical troubleshooting and duplicate review | None |
| `vendor_transaction_id` | Incentive and reconciliation audit | None |
| `ip_address` | Fraud review only, if provided | Excluded |
| `ip_geolocation` | Eligibility and fraud review only, if provided | Coarsened `census_region` if validated |
| `device_fingerprint` | Duplicate and fraud review | `duplicate_review_status` |
| `browser_user_agent_raw` | Technical troubleshooting and fraud review | Coarsened `device_type` |
| `panel_profile_raw_json` | Audit of appended profile variables | Harmonized variables listed in this codebook |
| `open_text_debrief_raw` | Cognitive debriefing, distress review, quality review | Excluded or coded flags only |
| `hash_salt_or_linkage_key` | Reproducible pseudonymization under controlled access | Excluded |

## Missingness And Nonresponse Coding

Prefer-not-to-answer options are retained as explicit categories for demographic, occupation, and AI exposure variables. ANX item skipped responses are not coded as prefer-not-to-answer unless the survey platform explicitly presented that response option, which Wave 1 does not do. Missing appended vendor profile values are coded null in restricted processing and harmonized to `prefer_not_to_answer` only when the respondent was explicitly offered that option.

For respondent-item rows, missingness must follow `schema/wave_response.schema.json`. Respondents excluded by preregistered respondent-level QC keep their rows, but affected rows use `missingness_code: not_scored_excluded_respondent` and include the applicable `exclusion_flags` when those rows are exported for scoring reproduction.

## Disclosure Control

Before public release, the data steward must review cross-classified cells involving age group, gender, race and ethnicity, region, occupation group, employment status, AI exposure, device type, and fielding date. Small cells must be suppressed, combined, or moved to restricted access. Exact timestamps, raw comments, direct vendor identifiers, raw device fields, and linkage materials are always restricted.
