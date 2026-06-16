# ANX-Bench Wave Response Data Dictionary

This document defines the canonical respondent-item response row for all fielded ANX-Bench waves. The machine-readable contract is `schema/wave_response.schema.json`. Every released wave dataset, validation packet, longitudinal analysis file, and event-study analysis file must be representable as one row per respondent, per administered item version, per wave.

The response schema is intentionally row-level. Construct, domain, and overall ANX scores are derived products. They must be reproducible from validated response rows, released item files, the versioned construct registry, the preregistered exclusion rules, and the scoring code used for the analysis.

## Unit Of Observation

Each row records one respondent's response to one ANX-Bench item version in one fielded wave. A respondent who answers 11 items contributes 11 rows. A planned-missingness design must still emit rows for item and respondent combinations that are part of the wave design but were not presented, using `raw_response: null`, `scored_value: null`, and `missingness_code: not_presented_by_design`.

Rows must be stored in a non-identifying analytic dataset. Direct identifiers, contact data, device fingerprints, IP addresses, free-text fields that can contain personal information, and unsalted cross-study person identifiers are not part of the canonical response row.

## Required Variables

| Variable | Type | Allowed values | Definition and use |
| --- | --- | --- | --- |
| `wave_id` | string | Pattern `anx_[a-z]{2,3}_[0-9]{4}w[0-9]{2}(_[a-z0-9]+)*`, for example `anx_us_2026w01` | Stable identifier for the fielded wave. It must be assigned before data collection and must match the preregistration, wave methods file, and analysis outputs. |
| `benchmark_version` | string | Semantic version such as `v0.1.0` | ANX-Bench release version governing the administered item set, item schema, construct registry, scoring rules, and release gates. |
| `item_id` | string | Lowercase snake_case ID registered in the applicable item file | Stable item identifier. It must match a released or explicitly development-status item in the benchmark version used for the wave. |
| `item_version` | string | Semantic version such as `v0.1.0` | Exact administered item record. Longitudinal comparisons require identical item versions unless a bridge study supports a documented link. |
| `respondent_id_hash` | string | 64 lowercase hexadecimal characters | Study-scoped pseudonymous respondent identifier generated with SHA-256 or a stronger salted hashing procedure. The salt must be stored separately from released analytic data. |
| `raw_response` | integer, string, or null | Usually integers `1` to `5` for ANX-Bench Likert items; null when no response was observed | Response as captured before scoring. Numeric Likert responses should remain numeric when possible. If a fielding vendor exports labeled values, the codebook must map them back to the released response anchors. |
| `scored_value` | number or null | `1` to `5`, or null | Score after applying the released item's scoring key. Higher values indicate greater AI-related anxiety unless the item file defines reverse coding and the scoring key has already reversed the raw value. |
| `response_timestamp` | string | ISO 8601 date-time with UTC offset, preferably UTC `Z` | Time at which the item response was submitted or finalized. Timestamps are required for fielding audit, longitudinal ordering, and event-study exposure windows. |
| `administration_mode` | string | `web`, `mobile_web`, `telephone`, `in_person`, `mail`, `mixed_mode`, `api_import` | Data collection mode for the row. Mode changes can affect measurement equivalence and must be documented in wave methods and validation analyses. |
| `language` | string | BCP 47 tag such as `en`, `en-US`, `es`, or `ja-JP` | Language of the item text shown to the respondent. Translations require validation or bridge evidence before confirmatory cross-language comparisons. |
| `survey_weight` | number | Positive number; use `1.0` for unweighted analyses | Final analysis weight attached to the respondent for the relevant wave. Weight construction must be preregistered or documented before confirmatory analysis. |
| `exclusion_flags` | array of strings | Empty array or schema-defined flags | Machine-readable exclusions affecting the row or respondent. Exclusions do not delete rows from the canonical dataset; they make analytic inclusion reproducible. |
| `missingness_code` | string | Schema-defined missingness code | Required status code explaining whether the response is observed and, if not, why no scored value is available. |

## Optional Event-Study Variables

These fields are required for any row used in a confirmatory event-study analysis and optional otherwise. If an analysis claims a response to an AI capability event, the event identifier, event timestamp, exposure windows, and baseline or follow-up role must be preregistered before response outcomes are inspected.

For confirmatory use, `event_id`, exposure window assignment, baseline or follow-up role, and relative timing must match the frozen event registry exactly. The registry must validate against `schema/event_registry.schema.json`, and the `event_id` in each response row must appear in the registry cited by the wave preregistration. `fielding_time_relative_to_event_hours` must be calculated from the registry's `event_timestamp` and the row's `response_timestamp`; `event_exposure_window` and `baseline_or_followup` must be assigned from the registry's locked baseline, exposure, and follow-up windows. Non-event calibration rows may use the reserved registry value `no_event` only when the frozen registry contains the explicit `no_event` record.

| Variable | Type | Allowed values | Definition and use |
| --- | --- | --- | --- |
| `event_id` | string | Lowercase snake_case ID | Preregistered event identifier, such as a model release, major AI incident, high-salience capability demonstration, or policy shock. The event must be defined independently of observed ANX-Bench outcomes. |
| `event_exposure_window` | string | `pre_event_baseline`, `immediate_post_event`, `short_post_event`, `extended_post_event`, `washout_or_buffer` | Preregistered exposure window for the response relative to the event. Window boundaries must be stated in hours or calendar times in the event-study preregistration. |
| `baseline_or_followup` | string | `baseline`, `followup`, `same_wave_event_only` | Role of the row in a longitudinal or event-study comparison. Baseline rows anchor pre-event or pre-follow-up estimates; follow-up rows support change estimates. |
| `fielding_time_relative_to_event_hours` | number | Signed hours | Difference between `response_timestamp` and the preregistered event timestamp. Negative values are pre-event responses; positive values are post-event responses. |

## Exclusion Flags

`exclusion_flags` must be an array. An empty array means the row has no exclusion flag. Flags are retained in the public or restricted analytic file so that independent analysts can reproduce both inclusive descriptive summaries and preregistered confirmatory estimates.

Allowed flags are:

- `attention_check_failed`: Respondent failed a preregistered attention or instruction check.
- `speeding`: Completion time violated a preregistered minimum duration rule.
- `straightlining`: Response pattern violated a preregistered low-effort response rule.
- `duplicate_respondent`: The respondent was identified as a duplicate within the study-specific privacy-preserving linkage system.
- `ineligible_population`: Respondent did not satisfy the wave's target population criteria.
- `consent_withdrawn`: Respondent withdrew consent after data collection.
- `quality_review_failed`: Row or respondent failed a documented quality review rule not covered by a more specific flag.
- `item_not_administered_by_design`: Item was not presented because of rotation, planned missingness, skip logic, or experimental assignment.
- `mode_protocol_violation`: Administration mode did not match the preregistered or approved wave protocol.
- `language_protocol_violation`: Language or translation exposure did not match the approved wave protocol.
- `scoring_ineligible_item`: Item was fielded but is not eligible for the requested score because of item status, validation status, registry status, or release rules.
- `other_preregistered_exclusion`: A preregistered exclusion not otherwise enumerated. The wave methods file must define it.

Rows with exclusion flags remain in the canonical response file. Score aggregation decides whether each flag excludes the row from item-level reporting, construct scoring, domain scoring, overall ANX scoring, longitudinal comparison, or event-study estimation.

## Missingness Codes

`missingness_code` separates missing data from exclusions. Missingness concerns whether a row has an observed answer and scored value. Exclusions concern whether an observed or unobserved row is eligible for a particular analysis.

Allowed codes are:

- `observed`: A raw response was captured and a scored value is available unless exclusion flags remove the row from the analysis.
- `not_presented_by_design`: The item was not shown because of planned missingness, item rotation, skip logic, or experimental assignment.
- `skipped_by_respondent`: The item was shown, but the respondent gave no answer.
- `prefer_not_to_answer`: The respondent selected an explicit nonresponse option.
- `survey_breakoff`: The respondent exited before reaching or completing the item.
- `technical_failure`: The response could not be captured or recovered because of a platform, vendor, or data-processing failure.
- `removed_by_quality_control`: A raw response existed but was removed from scoring under preregistered quality-control rules.
- `not_scored_item_ineligible`: The item response exists but the item is not eligible for the requested benchmark score.
- `not_scored_excluded_respondent`: The respondent is excluded from scoring under preregistered respondent-level rules.

When `missingness_code` is `observed`, `raw_response` must be non-null and `scored_value` must be a number from 1 to 5. For every other missingness code, `scored_value` must be null. Primary analyses must not impute item responses unless the preregistered statistical plan defines the missing-data model.

## Scoring Rules

Raw responses become scored values only through the released item scoring key for the exact `item_id` and `item_version`. For standard non-reverse-coded 5-point Likert items, raw responses `1`, `2`, `3`, `4`, and `5` map to scored values `1`, `2`, `3`, `4`, and `5`. For reverse-coded items, the released scoring key maps raw `1` to scored `5`, raw `2` to scored `4`, raw `3` to scored `3`, raw `4` to scored `2`, and raw `5` to scored `1`.

Scoring pipelines must perform these checks before producing construct, domain, overall, longitudinal, or event-study estimates:

1. Validate every response row against `schema/wave_response.schema.json`.
2. Resolve `benchmark_version`, `item_id`, and `item_version` to the released item file.
3. Confirm that the item validates against `schema/item.schema.json`.
4. Confirm that the item's construct is registered in the applicable construct registry and that the item is allowed for that construct.
5. Apply the item scoring key to `raw_response`.
6. Verify that the stored `scored_value` equals the derived score.
7. Apply missingness and exclusion rules exactly as preregistered.
8. Aggregate only items whose release status, validation status, and registry status permit the requested level of scoring.

If the stored `scored_value` disagrees with the released scoring key, the row fails analytic validation until the discrepancy is corrected or documented as a retracted fielding file.

## Privacy Rules

The canonical response row is designed for analytic reproducibility, not respondent re-identification. ANX-Bench wave data must follow these privacy rules:

- Store no names, email addresses, phone numbers, postal addresses, account IDs, device IDs, IP addresses, precise geolocation, audio, video, or unrestricted free text in the canonical response file.
- Generate `respondent_id_hash` with a study-specific secret salt or equivalent keyed hashing procedure. Do not reuse unsalted hashes across studies, vendors, countries, or public releases.
- Keep the salt, linkage table, consent records, and payment records outside the analytic dataset under an access-controlled data management plan.
- Release only the minimum timestamp precision needed for the approved analysis. Public files may coarsen `response_timestamp` when event-study claims do not require exact timing.
- Suppress, coarsen, or restrict variables that create small cells when combined with country, language, administration mode, wave, event window, or weighting strata.
- Treat event-study timing as potentially identifying in small samples. If exact timing is needed for replication, provide it through a restricted-use file with a data-use agreement.
- Never use `respondent_id_hash` as a cross-project universal person identifier. Longitudinal linkage must be limited to the approved ANX-Bench panel or wave family.

## Validation Requirement For Claims

No fielded wave can support validation, longitudinal, or event-study claims unless the response data validate against `schema/wave_response.schema.json`. A dataset that fails the schema may still be retained as raw operational data, but it must not be cited as an ANX-Bench validation sample, benchmark trend, longitudinal estimate, or event-study estimate until a corrected, schema-valid analytic file is frozen.
