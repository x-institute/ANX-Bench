# ANX-Bench Wave 3 Somatic Test-Retest Codebook

## Control Record

- Wave ID: `anx_us_2026w03_somatic_retest`
- Study label: `anx_us_2026w03_somatic_retest`
- Benchmark release: `v0.3.1`
- Source scored release: `ANX-Bench v0.3.1`
- Codebook version: `anx_us_2026w03_somatic_retest_codebook`
- Retested construct: `somatic_ambient_anxiety`
- Paired instrument: `docs/instruments/anx_us_2026w03_somatic_retest_instrument.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w03_somatic_retest.md`
- Frozen event registry: `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`
- Canonical respondent-item schema: `schema/wave_response.schema.json`

This codebook defines the retest respondent-item mapping, linkage fields, timing-window fields, exclusion flags, panel-conditioning variables, weights, and restricted operations fields for `anx_us_2026w03_somatic_retest`. The wave repeats exactly the four v0.3.1 approved somatic and ambient items. It introduces no new scored items, no event-study exposure, no clinical interpretation, and no population-trend endpoint.

## Data Files

| File class | Disclosure status | Unit of record | Description |
| --- | --- | --- | --- |
| Retest respondent-item analytic file | Public or restricted according to disclosure review | One row per respondent per retest item | Must validate against `schema/wave_response.schema.json`; direct identifiers are prohibited. |
| Retest respondent-level analytic file | Restricted or controlled public summary | One row per retest respondent | Contains linkage quality, retest timing, QC flags, conditioning variables, attrition weights, and paired analysis eligibility. |
| Linkage operations file | Restricted only | One row per vendor panel member or linkage token | Contains direct vendor identifiers, salted linkage inputs, and audit fields used to construct analytic hashes. |
| Attrition disposition file | Restricted or controlled aggregate | One row per eligible Wave 1 respondent | Tracks invitation, contact, consent, completion, exclusion, and timing-window status. |

## Mapping Into `wave_response.schema.json`

The canonical respondent-item file must contain the following schema fields for every administered retest item.

| Schema field | Retest source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w03_somatic_retest`. |
| `benchmark_version` | Constant `v0.3.1`, the citable scored release whose four-item `somatic_ambient_anxiety` score is being retested. Any future `v0.3.2` must be treated as a post-fielding evidence release, not as the respondent-item administration version. |
| `item_id` | Item ID from the randomized four-item retest block. Allowed IDs are exactly the four IDs listed in the item allowlist. |
| `item_version` | Constant `v0.2.0` for every retest item, matching the v0.3.1 scored item files. |
| `respondent_id_hash` | SHA-256 salted, study-scoped analytic respondent ID derived from the protected retest linkage token. It must be stable across the four retest item rows and must not reveal the vendor panelist ID. |
| `raw_response` | Integer 1 through 5 as selected by the respondent for the item. Null only when the item was not validly observed. |
| `scored_value` | Same numeric value as `raw_response` for observed rows because all four items are positively keyed 1 to 5. Null when `missingness_code` is not `observed` or when exclusions prevent scoring. |
| `response_timestamp` | UTC item submission timestamp. |
| `administration_mode` | `web` or `mobile_web` unless an approved addendum permits another mode. |
| `language` | Constant `en-US`. |
| `survey_weight` | `retest_attrition_adjusted_weight_trimmed_rescaled` for primary weighted estimates; use 1.0 only for explicitly unweighted diagnostics. |
| `exclusion_flags` | Array of schema-valid exclusion flags propagated from respondent-level QC and item-level validity checks. Empty array indicates no exclusion flag for that row. |
| `missingness_code` | `observed` for valid item responses from respondents not removed before scoring; otherwise one of the schema-valid missingness codes defined below. |
| `event_id` | Constant `no_event`, matching `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`. |
| `event_exposure_window` | Omit or null in source exports because this is a no-event retest wave. No event window may be inferred. |
| `baseline_or_followup` | Constant `followup` for retest item rows used in paired analyses. |
| `fielding_time_relative_to_event_hours` | Null because `event_id` is `no_event` and no event timestamp exists. |

## Retest Item Allowlist

The following four item IDs are the only ANX item IDs allowed in `anx_us_2026w03_somatic_retest` respondent-item rows. Vendor exports must not add, drop, rename, recode, or substitute ANX items. The retest uses no new scored items.

| Domain | Item ID | Item version | File | Construct ID |
| --- | --- | --- | --- | --- |
| somatic_ambient | `sleep_disruption_ai_news` | `v0.2.0` | `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `body_vigilance_model_release` | `v0.2.0` | `items/v0.2/somatic_ambient/body_vigilance_model_release.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `background_dread_ai_progress` | `v0.2.0` | `items/v0.2/somatic_ambient/background_dread_ai_progress.json` | `somatic_ambient_anxiety` |
| somatic_ambient | `avoidance_after_ai_capability_demo` | `v0.2.0` | `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json` | `somatic_ambient_anxiety` |

## Linkage Fields

| Variable | Type | Allowed values or derivation | Disclosure | Required | Definition |
| --- | --- | --- | --- | --- | --- |
| `wave1_wave_id` | string | Constant `anx_us_2026w02_somatic` | Public | yes | Baseline wave source for the paired record. |
| `retest_wave_id` | string | Constant `anx_us_2026w03_somatic_retest` | Public | yes | Retest wave identifier. |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Public | yes | Retest analytic respondent hash used in `wave_response.schema.json`. |
| `wave1_respondent_id_hash` | string | 64 lowercase hexadecimal characters | Restricted or public if disclosure-safe | yes | Baseline analytic respondent hash from the Wave 1 somatic file. |
| `pair_id_hash` | string | SHA-256 hash of the resolved one-to-one Wave 1 and retest linkage pair | Public | yes | Stable paired-analysis identifier. |
| `linkage_token_hash` | string | SHA-256 salted hash of the vendor stable panel token | Restricted | yes | Protected linkage key used to resolve the pair. |
| `linkage_key_version` | string | `anx_retest_linkage_2026w03_v1` | Restricted | yes | Version of the salted linkage construction rule. |
| `linkage_match_status` | string | `unique_match`, `no_wave1_match`, `multiple_wave1_matches`, `multiple_retests_for_wave1`, `linkage_token_missing`, `profile_conflict` | Public summary, restricted row level | yes | Final linkage resolution status. |
| `linkage_primary_key_type` | string | `stable_panel_member_id`, `encrypted_panel_linkage_token`, `vendor_recontact_token` | Restricted | yes | Primary key class used for matching. |
| `linkage_secondary_checks_passed` | boolean | `true`, `false` | Restricted | yes | True when age or birth-year band, gender, region, device class, and timestamp checks are not contradictory. |
| `retained_retest_record_rule` | string | `only_complete`, `earliest_primary_window_complete`, `earliest_sensitivity_window_complete`, `excluded_duplicate`, `not_applicable` | Public summary, restricted row level | yes | Rule used when more than one retest record maps to the same Wave 1 respondent. |

Direct `vendor_panelist_id`, survey tokens, names, email addresses, phone numbers, IP addresses, raw device fingerprints, and raw linkage salts are restricted operations fields and must never appear in public analytic files.

## Timing-Window Fields

The primary retest window is fixed before outcome inspection. The start is inclusive at 13 completed days after Wave 1 completion and the end is exclusive after 16 completed days.

| Variable | Type | Allowed values or derivation | Disclosure | Required | Definition |
| --- | --- | --- | --- | --- | --- |
| `wave1_completion_timestamp_utc` | datetime | ISO 8601 UTC timestamp | Restricted or public if rounded | yes | Baseline completion timestamp used for retest interval calculation. |
| `retest_invitation_timestamp_utc` | datetime | ISO 8601 UTC timestamp | Restricted | yes | Timestamp at which the retest invitation was issued. |
| `retest_start_timestamp_utc` | datetime | ISO 8601 UTC timestamp | Restricted or public if rounded | yes | First retest screen timestamp. |
| `retest_completion_timestamp_utc` | datetime or null | ISO 8601 UTC timestamp | Restricted or public if rounded | yes | Final submitted retest timestamp. |
| `retest_interval_hours` | number | `(retest_completion_timestamp_utc - wave1_completion_timestamp_utc) / 3600` | Public | yes | Continuous retest interval in hours. |
| `retest_interval_days` | number | `retest_interval_hours / 24` | Public | yes | Continuous retest interval in days. |
| `primary_retest_window_start_days` | number | Constant `13` | Public | yes | Inclusive primary-window lower bound. |
| `primary_retest_window_end_days` | number | Constant `16` | Public | yes | Exclusive primary-window upper bound. |
| `sensitivity_retest_window_start_days` | number | Constant `10` | Public | yes | Inclusive timing-sensitivity lower bound. |
| `sensitivity_retest_window_end_days` | number | Constant `21` | Public | yes | Exclusive timing-sensitivity upper bound. |
| `retest_window_class` | string | `primary_13_to_before_16_days`, `early_sensitivity_10_to_before_13_days`, `late_sensitivity_16_to_before_21_days`, `out_of_window`, `missing_completion_time` | Public | yes | Timing class used for primary and sensitivity analyses. |
| `primary_retest_window_eligible` | boolean | `true`, `false` | Public | yes | True when `13 <= retest_interval_days < 16`. |
| `timing_sensitivity_window_eligible` | boolean | `true`, `false` | Public | yes | True when `10 <= retest_interval_days < 21`. |
| `fielding_time_relative_to_event_hours` | null | Always null | Public | yes | No-event field required to remain null. |

## Consent, Eligibility, And QC Variables

| Variable | Type | Allowed values | Disclosure | Required | Exclusion mapping |
| --- | --- | --- | --- | --- | --- |
| `retest_consent_response` | integer | 1 `agree`, 2 `do_not_agree` | Restricted | yes | Option 2 maps to `consent_withdrawn`. |
| `retest_consented` | boolean | `true`, `false` | Public | yes | False maps to `consent_withdrawn`. |
| `retest_eligibility_confirmation` | integer | 1 `eligible`, 2 `not_eligible` | Restricted | yes | Option 2 maps to `ineligible_population`. |
| `retest_attention_response` | integer | 1 to 5 | Restricted | yes | Any value other than 2 maps to `attention_check_failed`. |
| `retest_attention_passed` | boolean | `true`, `false` | Public | yes | False maps to `attention_check_failed`. |
| `retest_scenario_comprehension_response` | integer | 1 to 4 | Restricted | yes | Any value other than 1 maps to `other_preregistered_exclusion`. |
| `retest_scenario_comprehension_passed` | boolean | `true`, `false` | Public | yes | False restricted reason `retest_scenario_comprehension_failed`. |
| `retest_somatic_attribution_response` | integer | 1 to 4 | Restricted | yes | Any value other than 1 maps to `other_preregistered_exclusion`. |
| `retest_somatic_attribution_passed` | boolean | `true`, `false` | Public | yes | False restricted reason `retest_somatic_attribution_failed`. |
| `retest_understanding_response` | integer | 1 `yes`, 2 `no` | Restricted | yes | Option 2 maps to `other_preregistered_exclusion`. |
| `retest_understanding_passed` | boolean | `true`, `false` | Public | yes | False restricted reason `retest_self_reported_noncomprehension`. |
| `retest_total_duration_seconds` | number | 0 or greater | Restricted or public if binned | yes | Used for speed exclusion. |
| `retest_speeding_flag` | boolean | `true`, `false` | Public | yes | True maps to `speeding` when total duration is below one-third of the median among non-breakoff records. |
| `retest_straightline_all_four_items` | boolean | `true`, `false` | Public | yes | True maps to `straightlining` only when paired with a failed attention check or minimum reading-time check. |
| `vendor_quality_flag` | boolean | `true`, `false` | Restricted | yes | True maps to `quality_review_failed`. |
| `duplicate_retest_flag` | boolean | `true`, `false` | Restricted | yes | True maps to `duplicate_respondent`. |
| `final_exclusion_flags` | array of strings | Values allowed by `schema/wave_response.schema.json` | Public | yes | Propagated to every respondent-item row. |
| `restricted_exclusion_reasons` | array of strings | Preregistered restricted reason codes | Restricted | yes | Stores exact reason when schema uses `other_preregistered_exclusion`. |

## Panel-Conditioning Variables

| Variable | Type | Allowed values | Disclosure | Required | Analysis role |
| --- | --- | --- | --- | --- | --- |
| `conditioning_prior_question_memory` | integer | 1 `no`, 2 `not_sure`, 3 `yes` | Public | yes | Measures memory of prior item exposure. |
| `conditioning_discussed_prior_survey` | integer | 1 `no`, 2 `not_sure`, 3 `yes` | Public | yes | Describes possible social discussion after Wave 1. |
| `conditioning_ai_news_attention_change` | integer | 1 `much_less`, 2 `somewhat_less`, 3 `no_change`, 4 `somewhat_more`, 5 `much_more` | Public | yes | Detects prior-survey influence on AI-news attention. |
| `conditioning_ai_news_avoidance_change` | integer | 1 `much_less`, 2 `somewhat_less`, 3 `no_change`, 4 `somewhat_more`, 5 `much_more` | Public | yes | Detects prior-survey influence on AI-news avoidance. |
| `conditioning_perceived_answer_influence` | integer | 1 `not_at_all`, 2 `a_little`, 3 `moderate_amount`, 4 `a_lot`, 5 `does_not_remember` | Public | yes | Descriptive panel-conditioning indicator. |
| `panel_conditioning_sensitivity_exclusion` | boolean | `true`, `false` | Public | yes | True when memory is yes and attention or avoidance increased because of the prior survey. |
| `panel_conditioning_sensitive_label` | boolean | `true`, `false` | Public result | analysis output | True if preregistered sensitivity thresholds are violated. |

## Weights And Attrition Variables

| Variable | Type | Allowed values or derivation | Disclosure | Required | Definition |
| --- | --- | --- | --- | --- | --- |
| `wave1_final_poststrat_weight` | number | Greater than 0 | Restricted or public if disclosure-safe | yes | Final Wave 1 post-stratification weight for the eligible respondent. |
| `retest_invited` | boolean | `true`, `false` | Public summary | yes | Whether the eligible Wave 1 respondent was invited. |
| `retest_started` | boolean | `true`, `false` | Public summary | yes | Whether the respondent started the retest. |
| `retest_completed_before_exclusions` | boolean | `true`, `false` | Public summary | yes | Whether the respondent reached the final debrief before exclusion rules. |
| `primary_pair_complete` | boolean | `true`, `false` | Public | yes | True when all four Wave 1 and retest item responses are valid and all respondent-level primary criteria pass. |
| `retest_response_propensity` | number | Greater than 0 and no greater than 1 | Restricted or public if binned | yes | Predicted probability of completing an eligible primary-window retest. |
| `retest_inverse_propensity_factor` | number | `1 / retest_response_propensity` | Restricted or public if binned | yes | Attrition adjustment multiplier before trimming. |
| `retest_attrition_adjusted_weight_untrimmed` | number | `wave1_final_poststrat_weight * retest_inverse_propensity_factor` | Restricted or public if disclosure-safe | yes | Untrimmed primary weight. |
| `retest_attrition_adjusted_weight_trimmed` | number | Trimmed to 0.30 through 3.00 after scaling convention | Public | yes | Trimmed attrition-adjusted weight. |
| `retest_attrition_adjusted_weight_trimmed_rescaled` | number | Rescaled to sum to complete-pair analytic N | Public | yes | Primary `survey_weight` for respondent-item rows. |
| `attrition_sensitive_label` | boolean | `true`, `false` | Public result | analysis output | True if preregistered attrition bias thresholds are violated. |

## Missingness And Exclusion Coding

Observed item responses use `missingness_code: observed` with `raw_response` and `scored_value` in the range 1 to 5. If an item is missing because of breakoff, use `survey_breakoff`. If a technical problem prevents capture, use `technical_failure`. If respondent-level QC removes a complete response from scoring, use `not_scored_excluded_respondent` and propagate the applicable `exclusion_flags`. The retest has no planned `item_not_administered_by_design` rows for the four approved items.

Primary paired analyses require valid Wave 1 and retest responses for all four approved items, a unique linkage match, primary-window timing, consent, eligibility, and all required QC passes. Item-level sensitivity analyses may include an item with valid paired responses from a respondent who passes respondent-level QC even if another retest item is missing, but such rows do not contribute to the primary construct ICC or mean-change endpoint.

## Restricted Operations Fields

The following variables may exist only in restricted operations files and must never appear in public analytic files: `vendor_panelist_id`, `vendor_survey_token`, `vendor_project_id`, `vendor_session_id`, `vendor_transaction_id`, `email_address`, `phone_number`, `name`, `ip_address`, `ip_geolocation`, `device_fingerprint`, `browser_user_agent_raw`, `panel_profile_raw_json`, `hash_salt_or_linkage_key`, `raw_linkage_token`, and `open_text_support_request`.

## Analysis-Ready Derived Scores

| Variable | Type | Derivation | Required | Use |
| --- | --- | --- | --- | --- |
| `wave1_somatic_ambient_anxiety_mean` | number | Arithmetic mean of the four Wave 1 scored item values | yes | Baseline construct score. |
| `retest_somatic_ambient_anxiety_mean` | number | Arithmetic mean of the four retest scored item values | yes | Retest construct score. |
| `somatic_ambient_anxiety_mean_change` | number | `retest_somatic_ambient_anxiety_mean - wave1_somatic_ambient_anxiety_mean` | yes | Mean-change endpoint. |
| `item_change_value` | number | Retest item score minus Wave 1 item score for each item | yes | Item-level stability endpoint. |

No overall ANX score, domain score outside `somatic_ambient_anxiety`, IRT theta score, clinical category, event-study contrast, or population-trend variable is authorized for this retest packet.
