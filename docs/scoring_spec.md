# ANX-Bench Wave Scoring Specification

This document defines the canonical scoring contract for ANX-Bench wave response files. It applies to respondent-item rows that validate against `schema/wave_response.schema.json` and to release manifests that validate against `schema/release.schema.json`.

The scoring contract is intentionally conservative. A row can be schema-valid and still contribute nothing to an official aggregate score when the item has not passed the release, validation, or manifest gates. The release manifest is the authority for whether aggregate scoring is permitted.

## Inputs

A scoring run requires:

- A JSON Lines wave response file with one respondent-item record per line.
- A release manifest path, for example `releases/v0.1.0/manifest.json`.
- The item files listed in the manifest's `frozen_item_set.items`.
- The construct registry applicable to the release line. For `v0.1.0`, this is `constructs/v0.1/registry.json`.
- `schema/wave_response.schema.json` for input row validation.
- `schema/score_output.schema.json` for output validation.

All paths are interpreted relative to the repository root containing the manifest.

## Row Validation

Before scoring, every response row must validate against `schema/wave_response.schema.json`.

The scorer then enforces these analytic consistency checks:

- `benchmark_version` must equal the manifest `benchmark_version`.
- `item_id` must appear in the manifest frozen item set.
- `item_version` must equal the item version recorded in the manifest and item file.
- `missingness_code: observed` requires a non-null `raw_response` and a non-null numeric `scored_value`.
- Any non-observed `missingness_code` requires `scored_value: null`.
- For observed rows on official scored items, `raw_response` must be an integer or string key present in the item `scoring.scoring_key`.
- For observed rows on official scored items, the row `scored_value` must equal the value obtained by applying the released item scoring key to `raw_response`.

Rows that fail schema validation or these consistency checks are invalid input and must stop the scoring run. Rows that are valid but not eligible for scoring are retained in counts and excluded from estimates.

## Raw-To-Scored Item Handling

Each item file contains the released raw-to-scored mapping under `scoring.scoring_key`.

For a valid observed response to an official scored item:

1. Convert `raw_response` to its canonical string key.
2. Look up the key in `scoring.scoring_key`.
3. Use the mapped numeric value as the scored item value.
4. Compare the mapped value with row `scored_value`; any mismatch is a fatal reproducibility error.

No other transformation is permitted during wave scoring. Reverse coding must already be represented in the item `scoring.scoring_key`. The scorer does not infer reverse coding from `scoring.reverse_coded` and does not rescale item values.

Missing responses are not imputed. Non-observed missingness codes produce null item contributions.

## Eligibility And Exclusion Filtering

A row contributes to official scoring only when all of the following are true:

- The manifest has `scoring_eligibility.aggregate_scoring_permitted: true`.
- The row item appears in `official_scored_items`.
- The manifest item record has `release_status: approved_scored`.
- The manifest item record has `validation.scoring_eligible: true`.
- The item file has `release_status: approved_scored`.
- The item file has `validation.scoring_eligible: true`.
- The row has `missingness_code: observed`.
- The row has an empty `exclusion_flags` array.
- The raw response maps exactly to the item scoring key.
- The row scored value equals the recomputed value.

Rows are excluded from estimates, but counted, when:

- They are non-observed because of skipped response, breakoff, not presented by design, technical failure, prefer-not-to-answer, quality-control removal, or item ineligibility.
- They carry any exclusion flag, including respondent-level flags such as `attention_check_failed`, `speeding`, `straightlining`, duplicate respondent, ineligible population, consent withdrawal, or preregistered exclusion.
- The item is present in the frozen item set but is not in `official_scored_items`.
- The item is in `official_scored_items` but no longer satisfies the approved-scored and scoring-eligible gates, in which case scoring must stop because the manifest is internally inconsistent.

The scorer reports missingness counts by `missingness_code`, exclusion counts by `exclusion_flags`, scoring-ineligible row counts, and included row counts.

## Item Summaries

For each frozen item observed in the input, the scorer emits an item summary with:

- `item_id`, `item_version`, `domain`, and `construct_id`.
- `official_scored`, `scoring_eligible`, and `included_in_aggregate`.
- Input row count and unique respondent count.
- Included row count and included unique respondent count.
- Missingness counts and exclusion counts.
- Sum of survey weights contributing to the item estimate.
- Weighted mean score and confidence interval fields, or null values when the item has no eligible observations.

The item score is the weighted mean of included scored values:

```text
item_mean = sum(weight_i * score_i) / sum(weight_i)
```

where `weight_i` is the row `survey_weight`. Survey weights must be positive because `schema/wave_response.schema.json` requires a positive value.

## Construct Aggregation

Construct summaries are computed only from official scored items with at least one included observation. Construct aggregation uses equal item weighting over contributing official scored item summaries:

```text
construct_mean = mean(item_mean_j for contributing official scored items j)
```

The construct's `contributing_item_count` records how many item summaries entered this mean. `contributing_n` records the unique respondents with at least one included row for the construct. `contributing_weight_sum` records the sum of weights across included respondent-item rows before equal-item aggregation.

A construct summary must be emitted only when at least one official scored item in that construct has an included estimate. A release may require more retained items for interpretability, but the official scored item list is the release-time authority for which items are permitted to enter the score.

## Domain Aggregation

Domain summaries are computed only from construct summaries with non-null point estimates. Domain aggregation uses equal construct weighting within the domain:

```text
domain_mean = mean(construct_mean_k for contributing constructs k)
```

The domain's `contributing_construct_count`, `contributing_item_count`, `contributing_n`, and `contributing_weight_sum` are reported explicitly.

## Overall Aggregation

The overall ANX score is computed only when aggregate scoring is permitted by the manifest and at least one domain summary has a non-null point estimate. Overall aggregation uses equal domain weighting:

```text
overall_mean = mean(domain_mean_d for contributing domains d)
```

The overall summary reports `contributing_domain_count`, `contributing_construct_count`, `contributing_item_count`, unique respondent `contributing_n`, and the respondent-item `contributing_weight_sum`.

If aggregate scoring is not permitted, all construct summaries, domain summaries, and the overall score must be empty or null, and `aggregate_scoring_permitted` must be `false`.

## Confidence Interval Fields

Every score object uses the same confidence interval fields:

- `point_estimate`
- `standard_error`
- `confidence_level`
- `ci_lower`
- `ci_upper`
- `ci_method`

The canonical implementation uses a deterministic large-sample weighted mean interval for item estimates:

```text
effective_n = (sum(weight_i) ** 2) / sum(weight_i ** 2)
weighted_variance = sum(weight_i * (score_i - item_mean) ** 2) / sum(weight_i)
standard_error = sqrt(weighted_variance / effective_n)
95_percent_ci = item_mean +/- 1.96 * standard_error
```

For aggregation levels above item, the canonical implementation applies the same formula to the equally weighted contributing lower-level point estimates. This interval is a reproducibility field, not a substitute for preregistered survey-design variance estimation. If fewer than two contributing values are available, the standard error is `0.0` and the confidence interval equals the point estimate. Confidence intervals are clipped to the item score range `[1.0, 5.0]`.

## v0.1.0 Rule

ANX-Bench `v0.1.0` has:

```json
"official_scored_items": []
```

and:

```json
"scoring_eligibility": {
  "official_scored_item_count": 0,
  "aggregate_scoring_permitted": false
}
```

Therefore `v0.1.0` yields no official aggregate ANX score, no official construct scores, and no official domain scores. `tools/score_wave.py` must emit `aggregate_scoring_permitted: false`, `official_scored_item_count: 0`, empty construct and domain summaries, and `overall_score: null` for the real `v0.1.0` manifest, even if a response file contains valid observed rows for frozen development or exemplar items.
