# ANX-Bench US 2026 Wave 8 Full-Domain Bridge Codebook

## Codebook Control

- Wave ID: `anx_us_2026w08_full_domain_bridge`
- Study label: `anx_us_2026w08_full_domain_bridge`
- Benchmark release: `v0.8.0`
- Codebook version: `anx_us_2026w08_full_domain_bridge_codebook`
- Freeze date: `2026-06-16`
- Paired instrument: `docs/instruments/anx_us_2026w08_full_domain_bridge_instrument.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w08_full_domain_bridge.md`
- Frozen event registry: `events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json`
- Canonical respondent-item schema: `schema/wave_response.schema.json`
- Canonical non-scored anchor response schema: `schema/anchor_response.schema.json`

This codebook defines the Wave 8 respondent-item mapping, item allowlist, fixed domain-block sequence, within-block randomization paradata, exclusions, weights, covariates, missingness rules, QC variables, and public-data restrictions. ANX item responses are represented as one row per respondent per administered item under `schema/wave_response.schema.json`. Respondent-level files support psychometric validation and disclosure review. They are not ANX-Bench scored output files.

## Mapping Into `wave_response.schema.json`

| Schema field | Wave 8 full-domain bridge source and derivation |
| --- | --- |
| `wave_id` | Constant `anx_us_2026w08_full_domain_bridge`. |
| `benchmark_version` | Constant `v0.8.0`. |
| `item_id` | One of the 24 administered item IDs in the allowlist. No other ANX item ID is valid for Wave 8. |
| `item_version` | Item-file `version`: `v0.2.0` for somatic items, `v0.1.0` for economic and epistemic items, and `v0.8.0` for relational, existential_identity, autonomy_surveillance, and safety_catastrophic items. |
| `respondent_id_hash` | Study-scoped salted SHA-256 or stronger keyed hash of the restricted respondent linkage key. The salt and source linkage key are never included in analytic files. |
| `raw_response` | Numeric response `1` to `5` from the ANX item screen, or null if no answer was captured. Vendor labels must be mapped back to numeric anchors before export. |
| `scored_value` | Equal to `raw_response` for observed non-excluded item responses in psychometric diagnostics; null when missingness or exclusion prevents analytic use. This is not an official item, domain, cross-domain, or overall ANX score. |
| `response_timestamp` | UTC timestamp when the item response was submitted or finalized. Public files may coarsen precision only after disclosure review. |
| `administration_mode` | `web` for desktop or laptop browser completes and `mobile_web` for phone or tablet browser completes. Other modes are protocol deviations unless preregistered before fielding. |
| `language` | Constant `en-US`. |
| `survey_weight` | Final respondent-level analysis weight; use `1.0` until final weights are constructed. |
| `exclusion_flags` | Array using only values allowed by `schema/wave_response.schema.json`; respondent-level exclusions propagate to all 24 item rows. |
| `missingness_code` | `observed`, `skipped_by_respondent`, `survey_breakoff`, `technical_failure`, `removed_by_quality_control`, `not_scored_excluded_respondent`, `not_scored_item_ineligible`, or `item_not_administered_by_design` as applicable. |
| `event_id` | Constant `no_event`, matching `events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json`. |
| `event_exposure_window` | Omit or null. Wave 8 has no event window. |
| `baseline_or_followup` | Omit or null. Wave 8 is not a longitudinal baseline or follow-up packet. |
| `fielding_time_relative_to_event_hours` | Omit or null because `event_id` is `no_event`. |

## Administered ANX Item Allowlist

| Domain | Item ID | Item version | File | Construct ID | Scoring variable |
| --- | --- | --- | --- | --- | --- |
| somatic_ambient | sleep_disruption_ai_news | v0.2.0 | items/v0.2/somatic_ambient/sleep_disruption_ai_news.json | somatic_ambient_anxiety | sleep_disruption_ai_news_anxiety |
| somatic_ambient | body_vigilance_model_release | v0.2.0 | items/v0.2/somatic_ambient/body_vigilance_model_release.json | somatic_ambient_anxiety | body_vigilance_model_release_anxiety |
| somatic_ambient | background_dread_ai_progress | v0.2.0 | items/v0.2/somatic_ambient/background_dread_ai_progress.json | somatic_ambient_anxiety | background_dread_ai_progress_anxiety |
| somatic_ambient | avoidance_after_ai_capability_demo | v0.2.0 | items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json | somatic_ambient_anxiety | avoidance_after_ai_capability_demo_anxiety |
| economic_vocational | skill_obsolescence_software | v0.1.0 | items/v0.1/economic_vocational/skill_obsolescence_software.json | economic_vocational_anxiety | software_skill_obsolescence_anxiety |
| economic_vocational | wage_pressure_customer_support | v0.1.0 | items/v0.1/economic_vocational/wage_pressure_customer_support.json | economic_vocational_anxiety | customer_support_wage_pressure_anxiety |
| economic_vocational | retraining_pressure_accounting | v0.1.0 | items/v0.1/economic_vocational/retraining_pressure_accounting.json | economic_vocational_anxiety | accounting_retraining_pressure_anxiety |
| economic_vocational | status_loss_creative_work | v0.1.0 | items/v0.1/economic_vocational/status_loss_creative_work.json | economic_vocational_anxiety | creative_status_loss_anxiety |
| epistemic | deepfake_evidence_trust | v0.1.0 | items/v0.1/epistemic/deepfake_evidence_trust.json | epistemic_trust_anxiety | deepfake_evidence_trust_anxiety |
| epistemic | synthetic_news_provenance | v0.1.0 | items/v0.1/epistemic/synthetic_news_provenance.json | epistemic_trust_anxiety | synthetic_news_provenance_anxiety |
| epistemic | ai_expert_claim_conflict | v0.1.0 | items/v0.1/epistemic/ai_expert_claim_conflict.json | epistemic_trust_anxiety | ai_expert_claim_conflict_anxiety |
| epistemic | personalized_misinformation_targeting | v0.1.0 | items/v0.1/epistemic/personalized_misinformation_targeting.json | epistemic_trust_anxiety | personalized_misinformation_targeting_anxiety |
| relational | partner_ai_confidant_displacement | v0.8.0 | items/v0.8/relational/partner_ai_confidant_displacement.json | relational_ai_anxiety | partner_ai_confidant_displacement_anxiety |
| relational | friend_group_ai_mediation | v0.8.0 | items/v0.8/relational/friend_group_ai_mediation.json | relational_ai_anxiety | friend_group_ai_mediation_anxiety |
| relational | eldercare_ai_attachment_shift | v0.8.0 | items/v0.8/relational/eldercare_ai_attachment_shift.json | relational_ai_anxiety | eldercare_ai_attachment_shift_anxiety |
| existential_identity | ai_personhood_boundary_uncertainty | v0.8.0 | items/v0.8/existential_identity/ai_personhood_boundary_uncertainty.json | existential_identity_ai_anxiety | ai_personhood_boundary_uncertainty_anxiety |
| existential_identity | human_judgment_status_loss | v0.8.0 | items/v0.8/existential_identity/human_judgment_status_loss.json | existential_identity_ai_anxiety | human_judgment_status_loss_anxiety |
| existential_identity | life_purpose_ai_substitution | v0.8.0 | items/v0.8/existential_identity/life_purpose_ai_substitution.json | existential_identity_ai_anxiety | life_purpose_ai_substitution_anxiety |
| autonomy_surveillance | public_space_tracking | v0.8.0 | items/v0.8/autonomy_surveillance/public_space_tracking.json | autonomy_surveillance_ai_anxiety | public_space_tracking_anxiety |
| autonomy_surveillance | workplace_behavior_scoring | v0.8.0 | items/v0.8/autonomy_surveillance/workplace_behavior_scoring.json | autonomy_surveillance_ai_anxiety | workplace_behavior_scoring_anxiety |
| autonomy_surveillance | personalized_behavior_nudging | v0.8.0 | items/v0.8/autonomy_surveillance/personalized_behavior_nudging.json | autonomy_surveillance_ai_anxiety | personalized_behavior_nudging_anxiety |
| safety_catastrophic | autonomous_cyber_cascade | v0.8.0 | items/v0.8/safety_catastrophic/autonomous_cyber_cascade.json | safety_catastrophic_ai_anxiety | autonomous_cyber_cascade_anxiety |
| safety_catastrophic | biosecurity_protocol_misuse | v0.8.0 | items/v0.8/safety_catastrophic/biosecurity_protocol_misuse.json | safety_catastrophic_ai_anxiety | biosecurity_protocol_misuse_anxiety |
| safety_catastrophic | military_escalation_ai_advice | v0.8.0 | items/v0.8/safety_catastrophic/military_escalation_ai_advice.json | safety_catastrophic_ai_anxiety | military_escalation_ai_advice_anxiety |

All administered ANX items use the ordered 5-point anxiety scale: 1 `Not at all anxious`, 2 `Slightly anxious`, 3 `Moderately anxious`, 4 `Very anxious`, 5 `Extremely anxious`. No ANX item response option is a prefer-not-to-answer category.

## Non-Scored Anchor Variables

Wave 8 administers 21 anchoring vignettes from `anchors/v0.8/full_domain_bridge/response_scale_vignettes.json` after the 24 ANX item screens and before post-item quality checks or covariates. Anchor responses are respondent-level calibration variables or rows in a separate non-scored anchor table. When exported as rows, the canonical machine-readable contract is `schema/anchor_response.schema.json`: one row per respondent-domain-severity anchor rating, with `anchor_id`, `domain`, `intended_severity`, `raw_response`, missingness provenance, timestamp, weight, and repeated derived monotonicity and response-style fields. Anchor rows are never `wave_response` item rows, never receive scored ANX `item_id` values, and never contribute to `raw_response` or `scored_value` fields under `schema/wave_response.schema.json`.

Anchor raw responses use the same ordered anxiety scale as ANX items: 1 `Not at all anxious`, 2 `Slightly anxious`, 3 `Moderately anxious`, 4 `Very anxious`, 5 `Extremely anxious`. Null is permitted only when no response was captured.

| Variable | Source vignette | Domain | Intended severity | Allowed values |
| --- | --- | --- | --- | --- |
| `anchor_w08_somatic_ambient_low_raw` | `anchor_somatic_ambient_low` | somatic_ambient | low | 1 to 5, or null |
| `anchor_w08_somatic_ambient_moderate_raw` | `anchor_somatic_ambient_moderate` | somatic_ambient | moderate | 1 to 5, or null |
| `anchor_w08_somatic_ambient_high_raw` | `anchor_somatic_ambient_high` | somatic_ambient | high | 1 to 5, or null |
| `anchor_w08_economic_vocational_low_raw` | `anchor_economic_vocational_low` | economic_vocational | low | 1 to 5, or null |
| `anchor_w08_economic_vocational_moderate_raw` | `anchor_economic_vocational_moderate` | economic_vocational | moderate | 1 to 5, or null |
| `anchor_w08_economic_vocational_high_raw` | `anchor_economic_vocational_high` | economic_vocational | high | 1 to 5, or null |
| `anchor_w08_epistemic_low_raw` | `anchor_epistemic_low` | epistemic | low | 1 to 5, or null |
| `anchor_w08_epistemic_moderate_raw` | `anchor_epistemic_moderate` | epistemic | moderate | 1 to 5, or null |
| `anchor_w08_epistemic_high_raw` | `anchor_epistemic_high` | epistemic | high | 1 to 5, or null |
| `anchor_w08_relational_low_raw` | `anchor_relational_low` | relational | low | 1 to 5, or null |
| `anchor_w08_relational_moderate_raw` | `anchor_relational_moderate` | relational | moderate | 1 to 5, or null |
| `anchor_w08_relational_high_raw` | `anchor_relational_high` | relational | high | 1 to 5, or null |
| `anchor_w08_existential_identity_low_raw` | `anchor_existential_identity_low` | existential_identity | low | 1 to 5, or null |
| `anchor_w08_existential_identity_moderate_raw` | `anchor_existential_identity_moderate` | existential_identity | moderate | 1 to 5, or null |
| `anchor_w08_existential_identity_high_raw` | `anchor_existential_identity_high` | existential_identity | high | 1 to 5, or null |
| `anchor_w08_autonomy_surveillance_low_raw` | `anchor_autonomy_surveillance_low` | autonomy_surveillance | low | 1 to 5, or null |
| `anchor_w08_autonomy_surveillance_moderate_raw` | `anchor_autonomy_surveillance_moderate` | autonomy_surveillance | moderate | 1 to 5, or null |
| `anchor_w08_autonomy_surveillance_high_raw` | `anchor_autonomy_surveillance_high` | autonomy_surveillance | high | 1 to 5, or null |
| `anchor_w08_safety_catastrophic_low_raw` | `anchor_safety_catastrophic_low` | safety_catastrophic | low | 1 to 5, or null |
| `anchor_w08_safety_catastrophic_moderate_raw` | `anchor_safety_catastrophic_moderate` | safety_catastrophic | moderate | 1 to 5, or null |
| `anchor_w08_safety_catastrophic_high_raw` | `anchor_safety_catastrophic_high` | safety_catastrophic | high | 1 to 5, or null |

## Anchor Order-Violation Indicators

For each domain, compute `anchor_w08_<domain>_order_violation` from the low, moderate, and high raw anchor variables. Code `true` when any observed pair contradicts low <= moderate <= high. Code `false` when all three ratings are observed and preserve low <= moderate <= high. Code null when fewer than two ratings are observed.

| Variable | Derivation |
| --- | --- |
| `anchor_w08_somatic_ambient_order_violation` | `anchor_w08_somatic_ambient_low_raw > anchor_w08_somatic_ambient_moderate_raw`, or `moderate_raw > high_raw`, or `low_raw > high_raw`, among observed pairs. |
| `anchor_w08_economic_vocational_order_violation` | Same rule for economic_vocational anchors. |
| `anchor_w08_epistemic_order_violation` | Same rule for epistemic anchors. |
| `anchor_w08_relational_order_violation` | Same rule for relational anchors. |
| `anchor_w08_existential_identity_order_violation` | Same rule for existential_identity anchors. |
| `anchor_w08_autonomy_surveillance_order_violation` | Same rule for autonomy_surveillance anchors. |
| `anchor_w08_safety_catastrophic_order_violation` | Same rule for safety_catastrophic anchors. |
| `anchor_w08_any_order_violation` | `true` if any domain indicator is `true`; `false` if all seven domain indicators are `false`; null if no domain has enough observed anchor data to evaluate order. |
| `anchor_w08_order_violation_domain_count` | Integer 0 to 7, counting domains with `true` order violations among evaluable domains. |

Order-violation indicators are calibration descriptors. They are not automatic exclusion variables and do not alter ANX item missingness codes by themselves.

## Anchor Response-Style Strata

Domain-specific response-style variables use the pattern `anchor_w08_<domain>_response_style_stratum`.

| Allowed value | Coding rule |
| --- | --- |
| `compressed_low` | All three domain anchor ratings are observed, no order violation is present, and all ratings are 1 or 2. |
| `compressed_high` | All three domain anchor ratings are observed, no order violation is present, and all ratings are 4 or 5. |
| `calibrated_monotone` | All three domain anchor ratings are observed, no order violation is present, and the high rating is at least two scale points above the low rating. |
| `weakly_monotone_compressed` | All three domain anchor ratings are observed, no order violation is present, but the high rating is less than two scale points above the low rating and the ratings do not meet compressed-low or compressed-high rules. |
| `nonmonotone` | The domain-specific order-violation indicator is `true`. |
| `incomplete` | Fewer than three domain anchor ratings are observed. |

The respondent-level all-domain variable is `anchor_w08_response_style_stratum`.

| Allowed value | Coding rule |
| --- | --- |
| `broadly_calibrated` | At least five domain strata are `calibrated_monotone`, no domain is `nonmonotone`, and at least six domains are complete. |
| `globally_compressed_low` | At least five complete domains are `compressed_low` or `weakly_monotone_compressed`, median high-anchor rating across domains is 3 or lower, and no domain is `nonmonotone`. |
| `globally_compressed_high` | At least five complete domains are `compressed_high` or `weakly_monotone_compressed`, median low-anchor rating across domains is 3 or higher, and no domain is `nonmonotone`. |
| `mixed_response_style` | At least six domains are complete, no domain is `nonmonotone`, and no preceding all-domain rule is met. |
| `nonmonotone_any_domain` | At least one domain-specific response-style stratum is `nonmonotone`. |
| `anchor_incomplete` | Fewer than six domains have complete low, moderate, and high anchor ratings. |

Anchor response-style strata may be used in DIF, invariance, and domain-comparison sensitivity analyses. Primary ANX item analyses remain based on the 24 administered ANX item rows, with anchors outside the outcome definition.

## QC Variables and Schema Handling

| Variable | Type | Allowed values or coding | Public data status | Mapping rule |
| --- | --- | --- | --- | --- |
| `consent_status` | string | `agreed`, `declined`, `withdrawn` | Restricted summary public | Non-consent rows are excluded before respondent-item export. Withdrawal propagates an exclusion flag to existing rows if retained for audit. |
| `eligibility_age_18_plus` | boolean | `true`, `false` | Public | False respondents are excluded and receive the age-related schema exclusion flag when rows exist. |
| `eligibility_us_resident` | boolean | `true`, `false` | Public | False respondents are excluded from analytic rows. |
| `eligibility_english_self_administered` | boolean | `true`, `false` | Public | False respondents are excluded from analytic rows. |
| `attention_check_passed` | boolean | `true`, `false` | Public | False maps to `attention_check_failed` in `exclusion_flags`. |
| `scenario_comprehension_passed` | boolean | `true`, `false` | Public | False maps to `other_preregistered_exclusion` with restricted reason `scenario_comprehension_failed`. |
| `full_domain_attribution_passed` | boolean | `true`, `false` | Public | False maps to `other_preregistered_exclusion` with restricted reason `full_domain_attribution_failed`. |
| `self_reported_understanding` | integer | 1 to 5 | Public | Values 4 or 5 map to `quality_review_failed`. |
| `duplicate_review_status` | string | `not_duplicate`, `duplicate_confirmed`, `duplicate_possible_unconfirmed` | Restricted summary public | Confirmed duplicates map to `duplicate_response` or the closest schema-allowed duplicate flag. |
| `vendor_quality_status` | string | `passed`, `low_confidence`, `failed`, `not_provided` | Restricted summary public | Vendor failed maps to `quality_review_failed` unless overturned before outcome inspection. |
| `speeding_flag` | boolean | `true`, `false` | Public | True maps to `speeding_failed` when the schema permits, otherwise `quality_review_failed`. |
| `straightline_all_24_anx_items` | boolean | `true`, `false` | Public | Exclusion only when paired with failed attention or minimum-reading-time check; then map to `quality_review_failed`. |
| `anx_items_missing_count` | integer | 0 to 24 | Public | More than 6 missing items triggers respondent-level exclusion and item rows use `not_scored_excluded_respondent`. |
| `open_text_quality_flag` | boolean | `true`, `false` | Restricted summary public | Quality monitoring flag; does not exclude by itself. |
| `distress_review_flag` | boolean | `true`, `false` | Restricted summary public | Ethics monitoring flag; does not exclude by itself. |

## Paradata and Covariates

| Variable | Allowed values or coding | Use |
| --- | --- | --- |
| `domain_block_order_id` | Constant `fixed_full_domain_order_v0_8` | Documents the fixed seven-domain bridge sequence. |
| `domain_block_position` | 1 through 7 | Position of the item's domain block. |
| `item_within_block_position` | 1 through 4 for somatic, economic, epistemic; 1 through 3 for v0.8 domains | Randomized item position within domain. |
| `item_global_position` | 1 through 24 | Overall item screen position. |
| `within_block_item_order` | Domain-specific item permutation | Restricted respondent-level order array. |
| `item_response_time_seconds` | Number, 0 or greater | Reading-time and sensitivity diagnostics. |
| `anx_block_duration_seconds` | Number, 0 or greater | Total ANX item-block duration. |
| `age_group` | `18_29`, `30_44`, `45_59`, `60_plus` | Quotas, weighting, DIF, invariance. |
| `gender` | `woman`, `man`, `nonbinary_another_gender`, `prefer_not_to_answer` | Quotas, weighting, DIF, invariance, suppression. |
| `race_ethnicity` | Harmonized categories in the sampling plan | Quotas, weighting, DIF, invariance, suppression. |
| `education` | Harmonized categories in the sampling plan | Quotas, weighting, DIF, invariance. |
| `census_region` | `northeast`, `midwest`, `south`, `west` | Quotas, weighting, DIF, invariance. |
| `employment_status` | Harmonized employment categories | Quotas, weighting, economic sensitivity. |
| `occupation_group` | Broad Census-compatible group or nonemployed category | Monitoring, DIF, disclosure review. |
| `relationship_status` | Coarse respondent-reported category | Relational-domain sensitivity only. |
| `caregiving_role` | yes, no, prefer not to answer | Relational-domain sensitivity only. |
| `urbanicity` | urban, suburban, rural, unknown | Autonomy-surveillance sensitivity only. |
| `cyber_or_infrastructure_employment` | yes, no, prefer not to answer | Safety-domain sensitivity and suppression. |
| `prior_ai_exposure_frequency` | never or rare to daily | Quotas, DIF, invariance, sensitivity. |
| `ai_news_exposure_30d` | none or low to high | Quotas, DIF, invariance, sensitivity. |
| `baseline_general_anxiety_2item_mean` | 0 to 3 or null | Discriminant and incremental-validity covariate. |
| `final_weight` | Positive number, trimmed to 0.30 to 3.00 | Copied to `survey_weight` in every respondent-item row. |

## Missingness and Exclusions

For respondent-item rows, `missingness_code` is `observed` only when `raw_response` is present and the respondent is eligible for the relevant psychometric diagnostic. If the respondent is excluded after an observed response, retain `raw_response`, set `scored_value` to null in scored-analysis exports, set `missingness_code` to `not_scored_excluded_respondent`, and propagate relevant `exclusion_flags`. If an item is skipped, use `skipped_by_respondent`. If a platform failure prevents capture, use `technical_failure`. If a respondent breaks off before the item, use `survey_breakoff`. If a non-allowlisted item appears because of implementation error, mark it as `item_not_administered_by_design` and exclude it from the Wave 8 analytic item set.

## Public-Data Restrictions

The following variables may exist only in restricted operations files and must never appear in public analytic files: vendor IDs, survey tokens, IP addresses, device fingerprints, raw user agents, exact geolocation, raw profile JSON, hash salts, linkage keys, raw open text, names, contact information, employer names, school names, partner names, family names, private messages, relationship histories, credentials, cybersecurity incident details, biological protocol details, legal case details, compensation records, and any direct identifier.

Wave 8 public files may report item-level observed responses, weighted and unweighted descriptive summaries, and psychometric diagnostics after disclosure review. They must not publish official ANX-Bench item scores, domain scores, cross-domain scores, overall scores, respondent rankings, clinical classifications, policy rankings, event-study estimates, causal estimates, or longitudinal trend claims. `aggregate_scoring_permitted` remains false for `v0.8.0`.
