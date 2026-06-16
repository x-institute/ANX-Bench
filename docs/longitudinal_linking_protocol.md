# Longitudinal Linking Protocol

ANX-Bench longitudinal comparisons are release comparisons, not informal comparisons of similarly named survey waves. A trend, cross-release difference, event-window contrast, or statement that anxiety increased or decreased over time is allowed only when a versioned linking plan validates against `schema/longitudinal_linking_plan.schema.json` and the observed linking evidence passes the gates in that plan.

## Comparability Rule

Two waves or releases are comparable only when all of the following conditions hold before claims are made:

- The source and target releases have machine-readable manifests under `releases/`, and every item used in the comparison is listed in the applicable frozen item set.
- The comparison uses a preregistered linking plan that names the source release, target release, wave ID, preregistration paths, anchor items, bridge sample, linking model, invariance gates, drift thresholds, and permitted and blocked claims.
- Anchor items are coadministered or otherwise observed in a bridge design that supports estimating release-to-release scale alignment without inspecting outcomes first.
- Anchor item IDs, item versions, wording, response anchors, scoring keys, eligibility rules, administration mode, and target population scope are identical unless the linking plan explicitly marks the item as changed and cites observed bridge evidence for that change.
- Observed evidence passes configural, metric, and scalar or threshold invariance gates for the construct being compared, or a preregistered partial-invariance rule shows that freed parameters do not change score ordering or substantive interpretation.
- Drift, DIF, linking standard error, and subgroup stability remain inside the thresholds fixed in the plan.

If any condition fails, the releases may still be described as separate measurement packets, but they cannot support longitudinal, trend, cross-release, or event-study inference.

## Anchor Selection

Anchor items must be selected for construct continuity, not convenience. A valid anchor item should have stable wording, a stable five-point response scale, an unchanged scoring key, an unchanged construct interpretation, and prior evidence that it measures the same latent response process in the source release. For a scored construct, the preferred anchor set is the complete scored source item set. Dropping a source item from the anchor set requires a preregistered exclusion reason such as administration impossibility, copyright or safety restriction, or observed evidence that the item became noninvariant.

Anchor sets must cover the latent continuum represented by the source construct. For somatic and ambient AI anxiety, the v0.3.1 source anchors are the four approved scored v0.2.0 items: `sleep_disruption_ai_news`, `body_vigilance_model_release`, `background_dread_ai_progress`, and `avoidance_after_ai_capability_demo`. These anchors may link Wave 8 to the source somatic construct only after observed bridge evidence passes. They do not validate new Wave 8 domains by themselves.

## Minimum Overlap

A release pair must have at least three anchor items for any construct-level comparison, and a scored source construct with four or fewer items must carry forward the full scored item set unless the linking plan documents a blocked item and supplies bridge evidence. Each anchor must have enough eligible responses to estimate item parameters and subgroup DIF. The default Wave 8 rule is a minimum analytic bridge sample of 2000 and at least 1800 eligible responses per anchor after preregistered exclusions.

Overlap must be substantive as well as numeric. Items with changed wording, changed response labels, changed score direction, changed target population, changed language, or changed administration mode are not common anchors unless observed bridge evidence shows that the change is measurement-equivalent under the preregistered model.

## DIF And Invariance

Longitudinal linking requires tests for differential item functioning and measurement invariance across release, wave, sample source, device class, age group, gender, education, race and ethnicity, prior AI exposure, and AI-news exposure when cell sizes permit. The minimum gate is:

- Configural invariance must converge and preserve the preregistered factor structure.
- Metric invariance must not exceed an absolute CFI decrement of 0.01 or RMSEA increase of 0.015.
- Scalar or ordinal-threshold invariance must pass the same limits unless a preregistered partial-invariance rule is invoked.
- Material DIF must be zero for anchor items used to support official longitudinal claims. Materiality is defined by rank-order impact, expected score difference of 0.10 SD or greater, or pseudo-R2 change of 0.02 or greater.
- Anchor drift must remain at or below 0.20 SD mean absolute drift and 0.30 SD for any single anchor unless a stricter plan threshold applies.

Partial invariance is a repair, not a default. It is acceptable only when the plan states which parameters may be freed, why that freeing was anticipated, and how sensitivity models will show that conclusions are unchanged.

## Blocking Conditions

Any of the following blocks trend and event-study claims:

- No validated linking plan exists for the source and target release pair.
- The target release is a frozen candidate or development packet and has not passed observed linking evidence review.
- Fewer than the required anchor items are present, or an anchor item ID cannot be found in both release manifests.
- An anchor item version changed without observed bridge evidence and reviewer signoff.
- Wording, response anchors, scoring, language, administration mode, eligibility, or target population changed without evidence of measurement equivalence.
- Configural, metric, scalar, threshold, DIF, drift, linking standard error, or subgroup stability gates fail.
- The event registry is `no_event`, unlocked after outcome inspection, or does not identify a qualifying event before analysis.
- The sampling plan does not support the population, subgroup, or event-window claim being made.
- The release manifest does not authorize the scored outcome used in the comparison.

When a block occurs, reports must use non-comparative wording such as "Wave 8 administered a non-scored full-domain bridge packet" rather than "Wave 8 scores increased," "AI anxiety trended upward," or "the event changed ANX-Bench."
