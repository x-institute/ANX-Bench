# ANX-Bench US 2026 Wave 7 Cross-Domain Bridge Codebook

## Codebook Control

- Wave ID: `anx_us_2026w07_cross_domain_bridge`
- Study label: `anx_us_2026w07_cross_domain_bridge`
- Benchmark release: `v0.7.0`
- Codebook version: `anx_us_2026w07_cross_domain_bridge_codebook`
- Freeze date: `2026-06-16`
- Paired instrument: `docs/instruments/anx_us_2026w07_cross_domain_bridge_instrument.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md`
- Frozen event registry: `events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json`
- Canonical respondent-item schema: `schema/wave_response.schema.json`

This codebook defines the Wave 7 respondent-item mapping, item allowlist, block-order paradata, within-block randomization paradata, exclusions, weights, covariates, missingness rules, and public-data restrictions. ANX item responses are represented as one row per respondent per administered item under `schema/wave_response.schema.json`. Respondent-level files support cross-domain bridge diagnostics, psychometric linking, DIF, invariance, reliability, latent-correlation, and disclosure review. They are not ANX-Bench scored output files.

## File Families

| File family | Access level | Contents |
| --- | --- | --- |
| Canonical respondent-item analytic file | Public or restricted after disclosure review | One row per respondent-item response validating against `schema/wave_response.schema.json`; includes no direct vendor IDs and no raw unrestricted text. |
| Respondent-level analytic covariate file | Public or restricted after disclosure review | One row per respondent with eligibility, sampling, demographics, employment, occupation, AI exposure, AI-news exposure, baseline general anxiety, QC, block-order paradata summaries, weights, and analysis eligibility. |
| Restricted operations file | Restricted, not public | Vendor IDs, survey tokens, duplicate-detection fields, raw device and IP signals, exact timestamps when not disclosure-safe, raw open text, fraud review materials, and hash salts or linkage keys. |

## Mapping Into `wave_response.schema.json`

Every administered ANX item creates one respondent-item row. The canonical file must validate against `schema/wave_response.schema.json`.

| Schema field | Wave 7 cross-domain bridge source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w07_cross_domain_bridge`. |
| `benchmark_version` | Constant `v0.7.0`. |
| `item_id` | One of the 12 administered item IDs listed in the allowlist below. No other ANX item ID is valid for Wave 7. |
| `item_version` | `v0.2.0` for `somatic_ambient` items and `v0.1.0` for `economic_vocational` and `epistemic` items, exactly as listed in the allowlist. |
| `respondent_id_hash` | Study-scoped salted SHA-256 or stronger keyed hash of the restricted respondent linkage key. The salt and source linkage key are never included in analytic files. |
| `raw_response` | Numeric response `1` to `5` from the ANX item screen, or null if no answer was captured. Vendor labels must be mapped back to numeric anchors before analytic export. |
| `scored_value` | Equal to `raw_response` for observed non-excluded item responses because all 12 items use non-reverse-coded 1 to 5 scoring for psychometric diagnostics; null when missingness or exclusion prevents analytic scoring. This is not an official domain, cross-domain, or overall ANX score. |
| `response_timestamp` | UTC timestamp when the item response was submitted or finalized. Public files may coarsen precision only with documented disclosure review. |
| `administration_mode` | `web` for desktop or laptop browser completes and `mobile_web` for phone or tablet browser completes. Other modes are protocol deviations unless preregistered before fielding. |
| `language` | Constant `en-US`. |
| `survey_weight` | Final respondent-level analysis weight for the relevant sample; use `1.0` until final weights are constructed. |
| `exclusion_flags` | Array using only values allowed by `schema/wave_response.schema.json`; respondent-level exclusions propagate to all 12 item rows. |
| `missingness_code` | `observed`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, `not_scored_excluded_respondent`, `not_scored_item_ineligible`, or `item_not_administered_by_design` as applicable. |
| `event_id` | Constant `no_event`, matching `events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json`. |
| `event_exposure_window` | Omit or null. Wave 7 has no event window. |
| `baseline_or_followup` | Omit or null. Wave 7 is not a longitudinal baseline or follow-up packet. |
| `fielding_time_relative_to_event_hours` | Omit or null because `event_id` is `no_event`. |

## Administered ANX Item Allowlist

The following 12 item IDs are the only ANX item IDs allowed in `anx_us_2026w07_cross_domain_bridge` respondent-item rows. Vendor exports must not add, drop, rename, recode, substitute, or update ANX items without a dated preregistration addendum and a new release packet.

| Domain | Item ID | Item file version | File | Construct ID | Scoring variable |
| --- | --- | --- | --- | --- | --- |
| somatic_ambient | `sleep_disruption_ai_news` | `v0.2.0` | `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json` | `somatic_ambient_anxiety` | `sleep_disruption_ai_news_anxiety` |
| somatic_ambient | `body_vigilance_model_release` | `v0.2.0` | `items/v0.2/somatic_ambient/body_vigilance_model_release.json` | `somatic_ambient_anxiety` | `body_vigilance_model_release_anxiety` |
| somatic_ambient | `background_dread_ai_progress` | `v0.2.0` | `items/v0.2/somatic_ambient/background_dread_ai_progress.json` | `somatic_ambient_anxiety` | `background_dread_ai_progress_anxiety` |
| somatic_ambient | `avoidance_after_ai_capability_demo` | `v0.2.0` | `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json` | `somatic_ambient_anxiety` | `avoidance_after_ai_capability_demo_anxiety` |
| economic_vocational | `skill_obsolescence_software` | `v0.1.0` | `items/v0.1/economic_vocational/skill_obsolescence_software.json` | `economic_vocational_anxiety` | `software_skill_obsolescence_anxiety` |
| economic_vocational | `wage_pressure_customer_support` | `v0.1.0` | `items/v0.1/economic_vocational/wage_pressure_customer_support.json` | `economic_vocational_anxiety` | `customer_support_wage_pressure_anxiety` |
| economic_vocational | `retraining_pressure_accounting` | `v0.1.0` | `items/v0.1/economic_vocational/retraining_pressure_accounting.json` | `economic_vocational_anxiety` | `accounting_retraining_pressure_anxiety` |
| economic_vocational | `status_loss_creative_work` | `v0.1.0` | `items/v0.1/economic_vocational/status_loss_creative_work.json` | `economic_vocational_anxiety` | `creative_status_loss_anxiety` |
| epistemic | `deepfake_evidence_trust` | `v0.1.0` | `items/v0.1/epistemic/deepfake_evidence_trust.json` | `epistemic_trust_anxiety` | `deepfake_evidence_trust_anxiety` |
| epistemic | `synthetic_news_provenance` | `v0.1.0` | `items/v0.1/epistemic/synthetic_news_provenance.json` | `epistemic_trust_anxiety` | `synthetic_news_provenance_anxiety` |
| epistemic | `ai_expert_claim_conflict` | `v0.1.0` | `items/v0.1/epistemic/ai_expert_claim_conflict.json` | `epistemic_trust_anxiety` | `ai_expert_claim_conflict_anxiety` |
| epistemic | `personalized_misinformation_targeting` | `v0.1.0` | `items/v0.1/epistemic/personalized_misinformation_targeting.json` | `epistemic_trust_anxiety` | `personalized_misinformation_targeting_anxiety` |

All administered ANX items use this ordered 5-point anxiety scale: 1 `Not at all anxious`, 2 `Slightly anxious`, 3 `Moderately anxious`, 4 `Very anxious`, 5 `Extremely anxious`. No ANX item response option is a prefer-not-to-answer category.

## Block-Order and Item-Randomization Paradata

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `domain_block_order_id` | string | `order_1`, `order_2`, `order_3`, `order_4`, `order_5`, `order_6` | Public or restricted after disclosure review | Assigned balanced domain-block order. |
| `domain_block_order` | array of strings | One of the six ordered domain triples listed below | Restricted, with public summaries allowed | Full respondent-level order of the three domain blocks. |
| `domain_block_position` | integer | 1, 2, 3 | Public | Position of the item's domain block for that respondent. |
| `item_within_block_position` | integer | 1, 2, 3, 4 | Public | Randomized position of the item within its domain block. |
| `item_global_position` | integer | 1 through 12 | Public | Overall item screen position after combining block order and within-block item randomization. |
| `within_block_item_order` | array of item IDs | Four-item permutation from the relevant domain allowlist | Restricted | Respondent-level within-block randomized item order. |
| `item_response_time_seconds` | number | 0 or greater | Public or restricted | Time between item screen display and answer submission. |
| `anx_block_duration_seconds` | number | 0 or greater | Public | Time from first ANX item display to final ANX item submission. |

The six valid domain-block orders are:

| Order ID | Block 1 | Block 2 | Block 3 |
| --- | --- | --- | --- |
| `order_1` | `somatic_ambient` | `economic_vocational` | `epistemic` |
| `order_2` | `somatic_ambient` | `epistemic` | `economic_vocational` |
| `order_3` | `economic_vocational` | `somatic_ambient` | `epistemic` |
| `order_4` | `economic_vocational` | `epistemic` | `somatic_ambient` |
| `order_5` | `epistemic` | `somatic_ambient` | `economic_vocational` |
| `order_6` | `epistemic` | `economic_vocational` | `somatic_ambient` |

Within each domain block, the allowed item set is the four item IDs from that domain in the allowlist. A repeated item, omitted item, item from a different domain, or non-allowlisted item is a protocol deviation. Public releases may include positions and order IDs, but full order arrays should remain restricted if disclosure review finds that they increase linkage risk in combination with exact timestamps or sample-source strata.

## Respondent-Level Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Public or restricted | Study-scoped salted respondent identifier used to join respondent-level covariates to respondent-item rows. |
| `sample_id` | string | `confirmation_sample`, `development_pilot` if a pilot is separately documented | Public | Non-overlapping sample label. Confirmatory bridge decisions use only the preregistered eligible confirmation sample. |
| `wave_id` | string | `anx_us_2026w07_cross_domain_bridge` | Public | Wave identifier. |
| `benchmark_version` | string | `v0.7.0` | Public | Release packet governing the instrument, codebook, preregistration, event registry, analysis plan, and checksums. |
| `analytic_eligible` | boolean | `true`, `false` | Public | Respondent is eligible after consent, population criteria, duplicate review, breakoff review, and preregistered QC exclusions. |
| `age_group` | string | `18_29`, `30_44`, `45_59`, `60_plus` | Public | Quota, weighting, DIF, and invariance category. |
| `gender` | string | `woman`, `man`, `nonbinary_another_gender`, `prefer_not_to_answer` | Public, subject to suppression | Gender category for quotas, weighting, DIF, and invariance. |
| `race_ethnicity` | string | `hispanic_latino`, `non_hispanic_white`, `non_hispanic_black`, `non_hispanic_asian`, `non_hispanic_other_multiracial`, `prefer_not_to_answer` | Public, subject to suppression | Race and ethnicity category for quotas, weighting, DIF, and invariance. |
| `education` | string | `high_school_or_less`, `some_college_associate`, `bachelors`, `graduate`, `prefer_not_to_answer` | Public | Highest educational attainment. |
| `census_region` | string | `northeast`, `midwest`, `south`, `west` | Public | US Census region. |
| `employment_status` | string | `employed_full_time`, `employed_part_time`, `self_employed`, `unemployed_looking`, `student`, `retired`, `not_in_labor_force_other`, `prefer_not_to_answer` | Public | Employment category for quotas, DIF, and economic-vocational bridge diagnostics. |
| `occupation_group` | string | Harmonized broad occupation category or `not_currently_employed`, `student`, `other`, `prefer_not_to_answer` | Public, subject to coarsening | Broad occupation group used for quota monitoring, DIF, and disclosure review. |
| `device_type` | string | `desktop_laptop`, `mobile_tablet`, `unknown` | Public | Device category used for mode assignment and sensitivity analysis. |

## Covariates and Comparator Variables

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `prior_ai_exposure_frequency` | integer | 1 `never_rare`, 2 `monthly`, 3 `weekly`, 4 `daily_near_daily`, 9 `prefer_not_to_answer` | Public | Frequency of personal generative AI use. |
| `ai_news_exposure_30d` | integer | 1 `not_at_all`, 2 `less_than_once_a_week`, 3 `about_once_a_week`, 4 `several_times_a_week`, 5 `daily_almost_daily`, 9 `prefer_not_to_answer` | Public | Frequency of exposure to AI capability news or commentary during the past 30 days. |
| `perceived_occupational_ai_exposure` | integer | 1 `not_at_all_exposed`, 2 `slightly_exposed`, 3 `moderately_exposed`, 4 `very_exposed`, 5 `extremely_exposed`, 9 `prefer_not_to_answer` | Public | Respondent's perceived exposure of current, recent, or intended work to current or near-future AI tools. |
| `perceived_ai_information_exposure` | integer | 1 `not_at_all_exposed`, 2 `slightly_exposed`, 3 `moderately_exposed`, 4 `very_exposed`, 5 `extremely_exposed`, 9 `prefer_not_to_answer` | Public | Perceived exposure of the respondent's information environment to current or near-future AI tools. |
| `labor_force_attachment` | integer | 1 `working_full_time`, 2 `working_part_time`, 3 `self_employed_freelance`, 4 `unemployed_looking`, 5 `student_training`, 6 `retired`, 7 `not_in_labor_force_other`, 9 `prefer_not_to_answer` | Public | Current connection to paid work. |
| `information_environment_role` | integer | 1 `private_citizen`, 2 `information_professional_or_student`, 3 `law_public_health_science_education_journalism_or_tech`, 4 `helps_others_interpret_information`, 5 `none_fit_well`, 9 `prefer_not_to_answer` | Public, subject to suppression | Role in which respondent most often evaluates public information. |
| `baseline_general_anxiety_nervous_2w` | integer | 0 to 3, 9 prefer not to answer | Public | Recent general anxiety covariate asking about feeling nervous, tense, or on edge during the past 2 weeks. |
| `baseline_general_anxiety_worry_2w` | integer | 0 to 3, 9 prefer not to answer | Public | Recent general worry covariate asking about difficulty stopping or controlling ordinary-life worry during the past 2 weeks. |
| `baseline_general_anxiety_2item_mean` | number or null | Mean of valid 0 to 3 values | Public | Discriminant and incremental-validity covariate. Compute when at least one source item has a valid 0 to 3 response. |

## Quality Control, Exclusions, and Missingness

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `consent_status` | string | `agreed`, `declined`, `withdrawn` | Restricted summary public | Consent disposition from Screen 1. |
| `eligibility_age_18_plus` | boolean | `true`, `false` | Public | Whether respondent confirmed or profile data indicated age 18 or older. |
| `eligibility_us_resident` | boolean | `true`, `false` | Public | Whether respondent resides in the United States. |
| `eligibility_english_self_administered` | boolean | `true`, `false` | Public | Whether respondent can complete the English survey unaided. |
| `attention_check_passed` | boolean | `true`, `false` | Public | `true` only when the instructed-response item equals 3. Failed respondents receive `attention_check_failed`. |
| `scenario_comprehension_passed` | boolean | `true`, `false` | Public | `true` only when the respondent identifies scenarios as hypothetical research materials. Failed respondents receive `other_preregistered_exclusion` with restricted reason `scenario_comprehension_failed`. |
| `cross_domain_attribution_passed` | boolean | `true`, `false` | Public | `true` only when the respondent identifies the task as rating anxiety about the situations described. Failed respondents receive `other_preregistered_exclusion` with restricted reason `cross_domain_attribution_failed`. |
| `self_reported_understanding` | integer | 1 to 5 | Public | Values 4 and 5 trigger `quality_review_failed`. |
| `duplicate_review_status` | string | `not_duplicate`, `duplicate_confirmed`, `duplicate_possible_unconfirmed` | Restricted summary public | Duplicate review result from vendor IDs, survey tokens, and device or fingerprint evidence. |
| `vendor_quality_status` | string | `passed`, `low_confidence`, `failed`, `not_provided` | Restricted summary public | Vendor fraud or quality flag. Vendor-failed completes receive `quality_review_failed` unless manual review overturns the flag before outcome inspection. |
| `straightline_all_12_anx_items` | boolean | `true`, `false` | Public | `true` when all 12 ANX items receive the same substantive response. Exclusion requires straightlining plus failed attention check or minimum reading-time check. |
| `straightline_domain_block` | boolean | `true`, `false` | Public | `true` when all four items in at least one domain block receive the same substantive response. Used as a sensitivity flag unless paired with another QC failure. |
| `anx_items_missing_count` | integer | 0 to 12 | Public | Number of ANX items without observed response. |
| `anx_items_missing_prop` | number | 0.00 to 1.00 | Public | Missing ANX item count divided by 12. Greater than 0.25 triggers exclusion. |
| `speeding_flag` | boolean | `true`, `false` | Public | Completion time below one-third of the same-sample median after breakoffs are removed. |
| `minimum_reading_time_flag` | boolean | `true`, `false` | Public | ANX item or block time below one-third of same-sample median reading time under the preregistered rule. |
| `open_text_quality_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment indicates confusion, protest responding, or failure to treat scenarios as AI-related. Does not exclude by itself. |
| `distress_review_flag` | boolean | `true`, `false` | Restricted summary public | Debrief comment suggests notable respondent distress. Used for ethics monitoring, not automatic exclusion. |
| `final_exclusion_flags` | array of strings | Values allowed by `schema/wave_response.schema.json` | Public | Respondent-level flags propagated to all respondent-item rows when applicable. |

Respondents are excluded from primary bridge analyses if they fail consent eligibility, are under 18, reside outside the United States, cannot self-administer in English, are duplicate confirmed, are vendor-confirmed fraud, fail the instructed-response attention check, fail the scenario-comprehension check, fail the cross-domain attribution check, complete the survey in less than one-third of the same-sample median time after breakoffs are removed, miss more than 25 percent of the administered ANX items, give the same substantive response to all 12 ANX items and also fail an attention or minimum-reading-time check, withdraw consent, or report that they understood only a few scenarios or did not understand the scenarios.

For respondent-item rows, `missingness_code` is `observed` only when `raw_response` is present and `scored_value` can be computed under the item scoring key. If the respondent is excluded after an observed item response, retain `raw_response`, set `scored_value` to null in scored-analysis exports, set `missingness_code` to `not_scored_excluded_respondent`, and propagate the relevant `exclusion_flags`. If an item is skipped, use `skipped_by_respondent`. If a platform failure prevents capture, use `technical_failure`. If a respondent breaks off before the item, use `survey_breakoff`. If a non-allowlisted item appears because of implementation error, use `item_not_administered_by_design`, mark the row with `item_not_administered_by_design`, and exclude it from the Wave 7 analytic item set.

## Weights

| Variable | Type | Allowed values or coding | Public data status | Definition |
| --- | --- | --- | --- | --- |
| `base_weight` | number | Positive number | Restricted or public | Design or vendor base weight before post-stratification. |
| `poststrat_weight` | number | Positive number | Public | Weight after raking or post-stratification. |
| `final_weight` | number | Positive number, target trimmed range 0.30 to 3.00 | Public | Final respondent-level analysis weight mapped to `survey_weight` in every respondent-item row. |
| `weight_trimmed` | boolean | `true`, `false` | Public | Whether the respondent's post-stratification weight was trimmed. |
| `weighting_cell_age_group` | string | Same categories as `age_group` | Public | Age group used for weighting. |
| `weighting_cell_gender` | string | Same categories as `gender` after vendor harmonization | Public | Gender category used for weighting. |
| `weighting_cell_race_ethnicity` | string | Same categories as `race_ethnicity` after vendor harmonization | Public | Race and ethnicity category used for weighting. |
| `weighting_cell_education` | string | Same categories as `education` | Public | Education category used for weighting. |
| `weighting_cell_census_region` | string | Same categories as `census_region` | Public | Region category used for weighting. |

Weights are constructed for descriptive representativeness. Minimum weighting variables are age group, gender, race and ethnicity, education, and Census region; employment status, occupation group, AI exposure, and AI-news exposure may be included when stable margins are available. Primary EFA, CFA, omega, IRT linking, DIF, invariance, and latent-correlation decisions are unweighted unless the estimator has a validated survey-weight implementation. Weighted and unweighted summaries must both be archived.

## Public-Data Restrictions

The following variables may exist only in restricted operations files and must never appear in public analytic files: `vendor_panelist_id`, `vendor_survey_token`, `vendor_project_id`, `vendor_session_id`, `vendor_transaction_id`, `ip_address`, `ip_geolocation`, `device_fingerprint`, `browser_user_agent_raw`, `panel_profile_raw_json`, `open_text_debrief_raw`, `employer_name_raw`, `client_name_raw`, `school_name_raw`, `wage_or_compensation_raw`, `tax_or_financial_record_raw`, `union_membership_raw`, `party_registration_raw`, `real_case_name_raw`, `social_media_handle_raw`, `private_message_raw`, `contact_information_raw`, and `hash_salt_or_linkage_key`.

Before public release, the data steward must review cross-classified cells involving age group, gender, race and ethnicity, region, education, employment status, occupation group, labor-force attachment, information-environment role, AI exposure, AI-news exposure, perceived occupational AI exposure, perceived AI information exposure, baseline anxiety, device type, sample source, fielding date, block-order ID, and item-position paradata. Small cells must be suppressed, combined, coarsened, or moved to restricted access. Exact timestamps, raw comments, direct vendor identifiers, raw device fields, workplace identifiers, legal or political identifiers, compensation records, and linkage materials are always restricted.

Wave 7 public files may report item-level observed responses and psychometric diagnostics after disclosure review, but they must not publish official ANX-Bench domain scores, cross-domain scores, overall scores, respondent rankings, clinical classifications, policy-decision rankings, event-study estimates, or longitudinal trend claims. `aggregate_scoring_permitted` remains false for `v0.7.0`.
