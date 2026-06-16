# ANX-Bench Anchoring Vignettes

## Purpose

Anchoring vignettes are fixed, non-scored calibration scenarios administered alongside an ANX-Bench instrument to evaluate how respondents use the shared 1 to 5 anxiety response scale. They support response-style calibration, monotonicity checks, differential item functioning sensitivity analysis, measurement-invariance interpretation, and cross-wave comparability. They are not ANX-Bench items and must never be included in item, construct, domain, cross-domain, overall, longitudinal, or event-study scoring.

For v0.2.2 somatic calibration, the fixed vignette set is `anchors/v0.2/somatic_ambient/response_scale_vignettes.json`. For Wave 8 full-domain bridge calibration, the fixed vignette set is `anchors/v0.8/full_domain_bridge/response_scale_vignettes.json`. The Wave 8 set contains low, moderate, and high intended-severity anchors for all seven ANX-Bench domains:

1. `somatic_ambient`
2. `economic_vocational`
3. `epistemic`
4. `relational`
5. `existential_identity`
6. `autonomy_surveillance`
7. `safety_catastrophic`

The Wave 8 anchors are deliberately written as calibration stimuli with known within-domain severity ordering. Their purpose is to make response-scale interpretation visible, not to estimate a participant's anxiety level.

## Administration

All anchoring vignettes use the shared ANX-Bench anxiety response scale:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

Wave 8 full-domain anchors are administered immediately after the 24 ANX item screens and before covariates, quality-check screens that refer to the completed scenario block, external-validity criteria, demographic questions, optional comments, or debrief language. Domains are presented in the fixed Wave 8 domain-block order. Within each domain, anchors are presented in fixed low, moderate, high order. Implementations may adapt page layout for accessibility and device responsiveness, but may not change vignette text, response labels, response order, domain order, within-domain severity order, or required status without a new release packet.

The fixed low, moderate, high sequence is part of the calibration design. It is not an attempt to estimate item difficulty by random presentation. A respondent's ratings are interpreted against the known intended severity order for the same domain only.

## Non-Scored Status

Anchoring vignette ratings must be stored as respondent-level calibration variables or in a separate non-scored vignette table. They must not be exported as `wave_response.schema.json` respondent-item rows. They must not receive `item_id` values from the scored ANX item namespace. They must not be included in reliability estimates, factor analyses, IRT calibration, item retention thresholds, construct means, domain means, cross-domain means, benchmark summaries, longitudinal trend claims, or event-study outcomes.

Permitted uses are limited to:

- Describing response-scale use after standardized low, moderate, and high stimuli.
- Flagging monotonicity violations across fixed within-domain severity bands.
- Creating preregistered response-style strata.
- Stratifying or adjusting DIF and invariance sensitivity analyses for response style.
- Evaluating whether cross-domain or subgroup conclusions are sensitive to observed scale-use differences.
- Checking whether cross-wave shifts in ANX item distributions remain after accounting for fixed vignette response patterns, when the same anchor set is administered unchanged.

Prohibited uses include:

- Official ANX item, construct, domain, cross-domain, overall, longitudinal, or event-study scoring.
- Clinical classification, diagnostic screening, employment screening, individual feedback, or intervention assignment.
- Quality-control exclusion by itself unless a separate preregistered exclusion rule is approved before outcome inspection.
- Replacing psychometric validation of the administered ANX item pool.

## Wave 8 Raw Anchor Variables

For Wave 8, each anchor response is stored as a respondent-level raw variable with integer values 1 to 5 or null if missing. The canonical variable pattern is `anchor_w08_<domain>_<severity>_raw`.

| Domain | Low | Moderate | High |
| --- | --- | --- | --- |
| somatic_ambient | `anchor_w08_somatic_ambient_low_raw` | `anchor_w08_somatic_ambient_moderate_raw` | `anchor_w08_somatic_ambient_high_raw` |
| economic_vocational | `anchor_w08_economic_vocational_low_raw` | `anchor_w08_economic_vocational_moderate_raw` | `anchor_w08_economic_vocational_high_raw` |
| epistemic | `anchor_w08_epistemic_low_raw` | `anchor_w08_epistemic_moderate_raw` | `anchor_w08_epistemic_high_raw` |
| relational | `anchor_w08_relational_low_raw` | `anchor_w08_relational_moderate_raw` | `anchor_w08_relational_high_raw` |
| existential_identity | `anchor_w08_existential_identity_low_raw` | `anchor_w08_existential_identity_moderate_raw` | `anchor_w08_existential_identity_high_raw` |
| autonomy_surveillance | `anchor_w08_autonomy_surveillance_low_raw` | `anchor_w08_autonomy_surveillance_moderate_raw` | `anchor_w08_autonomy_surveillance_high_raw` |
| safety_catastrophic | `anchor_w08_safety_catastrophic_low_raw` | `anchor_w08_safety_catastrophic_moderate_raw` | `anchor_w08_safety_catastrophic_high_raw` |

## Monotonicity Checks

Within each domain, the expected order is low <= moderate <= high. The domain-specific order-violation indicator is named `anchor_w08_<domain>_order_violation`.

Code the indicator as:

| Value | Rule |
| --- | --- |
| `true` | At least one observed pair contradicts the expected order: low > moderate, moderate > high, or low > high. |
| `false` | All three ratings are observed and low <= moderate <= high. |
| null | Fewer than two ratings are observed. |

The all-domain indicator is `anchor_w08_any_order_violation`. Code it `true` when any domain-specific violation is `true`, `false` when all seven domain-specific indicators are `false`, and null when no domain has enough observed anchor data to evaluate ordering. A second count variable, `anchor_w08_order_violation_domain_count`, records the number of domains with `true` order violations among evaluable domains.

Monotonicity violations are descriptive calibration results. They can signal misunderstanding, scale reversal, deliberate protest responding, or genuine idiosyncratic appraisal of scenario severity. They are not automatic exclusions.

## Response-Style Strata

Wave 8 defines domain-specific response-style strata and a respondent-level all-domain stratum. Domain-specific variables use the pattern `anchor_w08_<domain>_response_style_stratum`.

| Stratum | Rule |
| --- | --- |
| `compressed_low` | All three ratings are observed, no order violation is present, and all ratings are 1 or 2. |
| `compressed_high` | All three ratings are observed, no order violation is present, and all ratings are 4 or 5. |
| `calibrated_monotone` | All three ratings are observed, no order violation is present, and the high anchor is at least two scale points above the low anchor. |
| `weakly_monotone_compressed` | All three ratings are observed, no order violation is present, but the high anchor is less than two scale points above the low anchor and the ratings do not meet a compressed-low or compressed-high rule. |
| `nonmonotone` | The domain-specific order-violation indicator is `true`. |
| `incomplete` | Fewer than three anchor ratings are observed for the domain. |

The respondent-level all-domain variable is `anchor_w08_response_style_stratum`. Code it after all domain-specific strata are derived:

| Stratum | Rule |
| --- | --- |
| `broadly_calibrated` | At least five domains are `calibrated_monotone`, no domain is `nonmonotone`, and at least six domains are complete. |
| `globally_compressed_low` | At least five complete domains are `compressed_low` or `weakly_monotone_compressed`, the median high-anchor rating across domains is 3 or lower, and no domain is `nonmonotone`. |
| `globally_compressed_high` | At least five complete domains are `compressed_high` or `weakly_monotone_compressed`, the median low-anchor rating across domains is 3 or higher, and no domain is `nonmonotone`. |
| `mixed_response_style` | At least six domains are complete, no domain is `nonmonotone`, and the respondent does not meet the preceding all-domain rules. |
| `nonmonotone_any_domain` | At least one domain-specific stratum is `nonmonotone`. |
| `anchor_incomplete` | Fewer than six domains have complete low, moderate, and high anchor ratings. |

These strata are calibration descriptors. Confirmatory item analyses must report primary results without excluding respondents solely because of anchor strata.

## DIF And Invariance Sensitivity

Anchoring vignettes help distinguish two issues that are otherwise easy to confound: a subgroup may differ in latent AI-anxiety response, or it may use the response scale differently after reading the same intended scenario severity. Wave 8 therefore treats anchor variables as sensitivity tools, not as controls that automatically remove meaningful subgroup differences.

For item-level DIF analyses, analysts should estimate the preregistered primary DIF models without anchor adjustment, then report sensitivity models that add the relevant domain-specific response-style stratum and the respondent-level all-domain stratum. When sample size permits, repeat DIF models within the largest usable response-style strata. A DIF finding that appears only in a highly compressed or nonmonotone stratum should be described as less stable. A DIF finding that persists across anchor strata should be described as more robust to observed response-style differences.

For measurement-invariance analyses, anchor variables may be used to diagnose whether threshold or scalar non-invariance aligns with systematic compression, expansion, or nonmonotone use of the response scale. The anchor-adjusted analysis should report changes in fit indices, threshold shifts, factor mean differences, and substantive conclusions relative to the preregistered primary invariance model. Anchor-adjusted models are sensitivity analyses and do not replace the preregistered invariance gate for ANX items.

For domain comparisons, analysts should avoid interpreting raw domain mean differences as substantive if the same respondent groups show large domain-specific anchor compression or nonmonotonicity in the matching domain. The appropriate report is a sensitivity comparison: unadjusted domain pattern, pattern adjusted or stratified by response-style variables, and a statement about whether conclusions depend on anchor-derived calibration.

## Cross-Wave Comparability

The fixed vignettes support longitudinal comparability only when the same vignette text, response labels, response order, domain order, within-domain severity order, placement, and required status are retained across waves. If a later wave changes any of those features, the changed vignette set must receive a new version and cannot be treated as directly comparable to the Wave 8 anchors.

Cross-wave reports should show raw ANX item distribution changes before and after anchoring sensitivity checks. Anchor results may support the interpretation that scale use shifted across waves, but they do not by themselves prove that true anxiety did or did not change. Event-study analyses must keep anchors outside the outcome definition and use them only for planned sensitivity analyses.
