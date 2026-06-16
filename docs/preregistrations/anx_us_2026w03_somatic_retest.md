# ANX-Bench US 2026 Wave 3 Somatic Test-Retest Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w03_somatic_retest.md`
- Study label: `anx_us_2026w03_somatic_retest`
- Benchmark version under repeatability review: `ANX-Bench v0.3.1`
- Release manifest: `releases/v0.3.1/manifest.json`
- Construct registry: `constructs/v0.3/registry.json`
- Governing benchmark card: `docs/releases/v0.3.1_benchmark_card.md`
- Baseline Wave 1 source packet: `anx_us_2026w02_somatic`
- Baseline calibration preregistration: `docs/preregistrations/anx_us_2026w02_somatic_calibration.md`
- Retest event registry: `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`
- Event status: `no_event`
- Registry lock date: `2026-06-16`
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Retest interval: 14 days after each eligible respondent's Wave 1 completion timestamp
- Primary purpose: estimate short-interval repeatability of the approved v0.3.1 `somatic_ambient_anxiety` construct and its four approved scored items

This preregistration freezes a recontact wave for the four approved v0.3.1 somatic and ambient AI anxiety items. It is a test-retest reliability and longitudinal measurement-quality study, not a new calibration wave, not a validation rescue analysis, and not an event study. The retest wave may be used as evidence about repeatability, attrition, panel conditioning, missingness, and longitudinal measurement invariance for the restricted US English online adult v0.3.1 construct scope. It must not be used to claim population trend, event response, causal change after an AI capability shock, or general longitudinal movement in AI anxiety.

The frozen event registry for this wave is `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`. It fixes `event_id` to `no_event`, records `registry_status: frozen`, records `outcome_inspection_status: not_inspected`, and explicitly prohibits event-study claims. Every retest respondent-item row must therefore map `event_id` to `no_event`. No exposure window, baseline window, follow-up window, event-relative timestamp, or competing-event adjustment may be inferred for confirmatory reporting from this retest wave.

## Approved Item Set

The retest administers exactly the four approved v0.3.1 somatic and ambient items. Item wording, response anchors, scoring keys, item versions, construct ID, and respondent-facing scenario text must be identical to the approved Wave 1 materials.

| Domain | Item ID | Item version | File | Construct ID | v0.3.1 status |
| --- | --- | --- | --- | --- | --- |
| somatic_ambient | `sleep_disruption_ai_news` | `v0.2.0` | `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json` | `somatic_ambient_anxiety` | `approved_scored` |
| somatic_ambient | `body_vigilance_model_release` | `v0.2.0` | `items/v0.2/somatic_ambient/body_vigilance_model_release.json` | `somatic_ambient_anxiety` | `approved_scored` |
| somatic_ambient | `background_dread_ai_progress` | `v0.2.0` | `items/v0.2/somatic_ambient/background_dread_ai_progress.json` | `somatic_ambient_anxiety` | `approved_scored` |
| somatic_ambient | `avoidance_after_ai_capability_demo` | `v0.2.0` | `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json` | `somatic_ambient_anxiety` | `approved_scored` |

The retest uses the same ordered 5-point response scale:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

The primary construct score at both waves is `somatic_ambient_anxiety_mean`, the arithmetic mean of the four item scores for an eligible respondent. Higher values indicate stronger self-reported somatic and ambient AI anxiety under the released scenarios. The score is not a clinical screen, diagnosis, individual risk classification, or overall ANX-Bench score.

## Population, Matching, And Recontact Design

The target population is the subset of eligible US adult Wave 1 respondents from `anx_us_2026w02_somatic` who completed the approved v0.3.1 somatic item block in English online administration, passed Wave 1 respondent-level exclusion rules, provided permission for recontact, and have a stable panel identifier that can be linked without exposing direct identifiers in the analytic file.

Wave 1 respondents are matched to retest records using a hierarchy fixed before outcome inspection:

- Primary key: vendor-provided stable panel member ID or encrypted respondent linkage token.
- Secondary consistency checks: Wave 1 survey token, vendor project ID, birth-year band or age group, gender category, state or Census region, device class, and completion timestamp metadata.
- Conflict rule: if one Wave 1 record maps to multiple retest records, retain the earliest complete retest submitted within the eligible retest window and exclude later duplicate retests. If multiple Wave 1 records map to one retest record, exclude the ambiguous match from paired analyses.
- Privacy rule: direct names, emails, phone numbers, street addresses, IP addresses, and raw device fingerprints must not appear in the analytic repeatability file.

The planned retest invitation is sent 13 days after each eligible respondent's Wave 1 completion. The target completion time is day 14. The primary eligible retest window is from 13 completed days through 16 completed days after Wave 1 completion, inclusive at the start and exclusive after day 16. Retests completed from day 10 through day 12 or from day 16 through day 21 are retained only for timing sensitivity analyses. Retests outside day 10 through day 21 are excluded from all repeatability estimates because the interval no longer represents the preregistered 14-day retest design.

The target recontact pool is all eligible Wave 1 respondents with recontact permission. The target paired analytic sample is at least `N = 500` complete Wave 1 and retest pairs. If the final complete-pair `N` is below 400, primary repeatability estimates may be reported descriptively, but the wave fails the preregistered evidence threshold for supporting v0.3.1 repeatability claims.

## Fixed Eligibility And Exclusion Rules

Wave 1 eligibility must already have been determined under the Wave 1 preregistration and validation packet. A respondent is eligible for the retest analytic frame only if all of the following hold:

- Age 18 years or older at Wave 1.
- United States residence at Wave 1.
- English online self-administration at Wave 1.
- Passed Wave 1 consent, attention, comprehension, duplicate, timing, and item-missingness exclusions.
- Completed all four approved somatic and ambient items at Wave 1.
- Provided vendor-permitted recontact status before retest invitation.
- Has a stable linkage token that resolves to exactly one Wave 1 analytic record.

Retest records are excluded from primary paired analyses if any of the following hold:

- The retest respondent does not provide informed consent.
- The retest record cannot be uniquely matched to one eligible Wave 1 respondent.
- The retest is submitted before day 13 or on or after day 16 relative to Wave 1 completion for the primary analysis.
- The retest respondent fails the instructed-response attention check.
- The retest respondent fails the scenario-comprehension check.
- The retest respondent fails the somatic-attribution check, meaning the respondent rates a current medical condition rather than anxiety linked to the AI scenario.
- Retest completion time is less than one-third of the median retest completion time among non-breakoff records.
- The respondent gives the same substantive answer to all four retest ANX-Bench items and also fails either the attention check or the minimum reading-time check.
- Any of the four retest ANX-Bench item responses is missing, refused, non-substantive, or outside the released response scale.
- Vendor records indicate duplicate, fraudulent, bot-assisted, or non-human response behavior.
- The respondent self-reports that they could not understand most of the retest scenarios.

Incomplete retests are excluded from the primary respondent-level ICC and mean-change analyses when the respondent does not provide valid responses to all four approved somatic and ambient items at retest. Incomplete retests are not imputed. For item-level stability analyses, an incomplete retest contributes only to an item-specific sensitivity table when that specific item has valid Wave 1 and retest responses and all respondent-level QC rules are passed; it does not contribute to primary construct-level repeatability.

## Missingness, Attrition, And Weighting

Missing Wave 1 item responses are not allowed in the primary paired analytic sample because v0.3.1 repeatability is defined for the complete four-item construct mean. Missing retest item responses exclude the respondent from primary paired construct analyses. Missing covariates used only for attrition modeling may be handled with explicit missing categories when the source variable is categorical, or median plus missing-indicator coding when the source variable is continuous.

Attrition will be reported from the full eligible recontact pool to the final paired analytic sample. The report must include counts and percentages for invitation eligible, invited, bounced or unreachable, started retest, consented, complete before exclusions, excluded by each fixed exclusion rule, complete primary-window pairs, timing-sensitivity pairs, and final primary analytic pairs.

Attrition bias will be assessed by comparing retained complete-pair respondents with eligible nonrespondents on Wave 1 `somatic_ambient_anxiety_mean`, the four Wave 1 item scores, age group, gender, race and ethnicity, education, Census region, employment status, prior AI exposure, AI-news exposure, baseline general anxiety, device type, and Wave 1 response time. Standardized mean differences greater than 0.10 or absolute weighted percentage-point differences greater than 5.0 must be flagged. If retained respondents differ from nonrespondents on Wave 1 `somatic_ambient_anxiety_mean` by more than 0.15 score points or 0.20 standard deviations, the repeatability evidence must be labeled attrition-sensitive.

Primary descriptive estimates use attrition-adjusted Wave 1 weights. These weights start from the final Wave 1 post-stratification weight and are multiplied by the inverse predicted probability of completing an eligible retest within the primary window. The response-propensity model will include age group, gender, race and ethnicity, education, Census region, employment status, prior AI exposure, AI-news exposure, baseline general anxiety, Wave 1 device type, Wave 1 completion time, the four Wave 1 item scores, and Wave 1 `somatic_ambient_anxiety_mean`. Final weights will be trimmed to the interval 0.30 to 3.00 and rescaled to the complete-pair analytic sample size. Unweighted estimates remain required for psychometric model diagnostics and ICC sensitivity reporting.

## Panel-Conditioning Rules

Panel conditioning is defined as response change caused by prior exposure to the same ANX-Bench scenarios, response scale, or AI anxiety framing rather than a stable latent change in the respondent. The retest questionnaire must not include new AI capability demonstrations, news prompts, explanatory text about the prior wave, feedback about the respondent's previous answers, benchmark score labels, or claims that the study expects stability.

The retest will include a brief post-item conditioning module after the four approved items. It may ask whether the respondent remembers answering similar questions, discussed the prior survey with someone else, sought AI-related news because of the prior survey, or changed AI-news avoidance because of the prior survey. These conditioning variables are not ANX-Bench scored items and must not alter the four approved item responses.

Primary repeatability estimates include all otherwise eligible complete retests regardless of self-reported memory of Wave 1. Sensitivity analyses will repeat the ICC and mean-change endpoints after excluding respondents who report both remembering the prior item block and changing AI-news attention or avoidance because of it. If the primary ICC passes but the conditioning-excluded ICC falls below 0.65, or if weighted mean change changes by more than 0.10 points after conditioning exclusion, the repeatability evidence must be labeled panel-conditioning-sensitive.

## Primary Repeatability Endpoints

The primary endpoints are fixed before retest outcomes are inspected.

1. Respondent-level ICC(2,1) for `somatic_ambient_anxiety_mean`. The model is a two-way random-effects, absolute-agreement, single-measure intraclass correlation across Wave 1 and retest for complete paired respondents. The primary estimate is unweighted ICC(2,1), with a bootstrap confidence interval using respondent resampling. A weighted reliability sensitivity estimate will be reported using attrition-adjusted weights if software support is adequate.

2. Weighted mean change in `somatic_ambient_anxiety_mean`. Mean change is retest minus Wave 1 among complete paired respondents, estimated with attrition-adjusted weights. The report must include the weighted mean at Wave 1, weighted mean at retest, weighted mean change, robust standard error, 95 percent confidence interval, and standardized response mean.

3. Item-level stability for each of the four approved items. Item-level endpoints include weighted mean change, unweighted polychoric or Spearman stability correlation, weighted exact agreement, weighted adjacent agreement, and the share moving by two or more response categories. Each item is evaluated on paired respondents with valid Wave 1 and retest responses for that item and with all respondent-level QC rules passed.

4. Repeatability decision table. The final retest report must classify the construct and each item as passed, caution, or failed against the thresholds below.

## Preregistered Acceptable Thresholds

The retest wave supports acceptable v0.3.1 construct repeatability only if all primary construct thresholds pass:

- Complete-pair analytic `N` is at least 500.
- ICC(2,1) for `somatic_ambient_anxiety_mean` is at least 0.70.
- The lower bound of the bootstrap 95 percent confidence interval for ICC(2,1) is at least 0.60.
- Absolute weighted mean change in `somatic_ambient_anxiety_mean` is no greater than 0.15 points on the 1 to 5 scale.
- The 95 percent confidence interval for weighted mean change lies within -0.25 to 0.25 points.
- Standardized response mean for construct change is no greater than 0.20 in absolute value.
- Attrition diagnostics do not require the label attrition-sensitive under the rules above, or the same pass decision holds after attrition-adjusted weighting.
- Panel-conditioning sensitivity does not require the label panel-conditioning-sensitive under the rules above.

Item-level repeatability is acceptable for an item only if all item thresholds pass:

- Unweighted item stability correlation is at least 0.50.
- Absolute weighted item mean change is no greater than 0.20 points.
- Weighted exact agreement is at least 0.45 or weighted adjacent agreement is at least 0.85.
- The weighted share of respondents moving by two or more response categories is no greater than 0.15.
- Item-level missing or unusable retest response among eligible retest starters is no greater than 10 percent.

If the construct passes but one item fails item-level thresholds, v0.3.1 may retain the construct-repeatability label only with an item-level caution naming the failed item and the failed threshold. If two or more items fail item-level thresholds, the retest evidence fails to support a stable four-item v0.3.1 construct without additional bridge or revision evidence.

## Longitudinal Invariance Checks

Longitudinal invariance will be evaluated across Wave 1 and retest for the four-item `somatic_ambient_anxiety` construct before interpreting repeatability as evidence of stable measurement. The planned sequence is configural, metric, and scalar invariance for ordered categorical confirmatory factor analysis using an estimator appropriate for ordinal responses, such as WLSMV. If the CFA model is not identified or unstable with four ordered indicators, the fallback is an item-response or alignment-based linking analysis that tests whether item thresholds and loadings are sufficiently stable for mean-score repeatability interpretation.

Pass thresholds for longitudinal invariance are:

- Configural model converges without improper solutions and preserves the one-factor interpretation.
- Metric invariance has change in CFI no worse than -0.010 and change in RMSEA no greater than 0.015 relative to configural.
- Scalar or threshold invariance has change in CFI no worse than -0.010 and change in RMSEA no greater than 0.015 relative to metric.
- No item threshold or loading drift produces an expected construct-score difference greater than 0.10 points at the same latent trait level.
- Residual local dependence across repeated administrations is reported and does not exceed a preregistered review threshold of absolute residual correlation 0.20 for same-item wave pairs after accounting for the latent factor.

If configural invariance fails, the retest wave must be labeled `longitudinal_invariance_failed_configural`, and no construct-level test-retest reliability claim may be made. If metric invariance fails, the wave must be labeled `longitudinal_invariance_failed_metric`; item-level descriptive stability may be reported, but construct-level ICC must be labeled non-comparable. If scalar or threshold invariance fails while configural and metric invariance pass, ICC may be reported as a rank-order stability statistic, but weighted mean change must be labeled measurement-non-invariant and cannot be interpreted as true change. If only minor localized drift is present and partial invariance is defensible before outcome-based model modification, the report must label the result `partial_longitudinal_invariance` and identify the freed parameter, affected item, and maximum expected score impact.

## Confirmatory Reporting Restrictions

The retest report may make only the following confirmatory claims if the relevant thresholds pass:

- Short-interval repeatability of `somatic_ambient_anxiety_mean` in the restricted v0.3.1 US English online adult scope.
- Item-level 14-day stability for the four approved somatic and ambient items.
- Attrition-adjusted repeatability evidence for recontacted Wave 1 respondents.
- Longitudinal measurement-invariance status across Wave 1 and retest.
- Panel-conditioning sensitivity status for the 14-day recontact design.

The retest report must not claim:

- A population trend in AI anxiety.
- An event-study effect.
- A causal response to a model release, product launch, AI incident, policy action, or news cycle.
- A new overall ANX-Bench score.
- Cross-domain, cross-language, cross-country, clinical, occupational, organizational, or non-online comparability.
- Evidence that v0.3.1 can support longer-interval longitudinal inference without additional preregistered waves.

## Reproducibility Archive

The final retest evidence packet must archive this preregistration, the frozen no-event registry, exact Wave 1 and retest item files and checksums, linkage-token creation rules, retest invitation dates, completion timestamps, exclusion flow, attrition model specification, weight construction script, repeatability analysis script, longitudinal invariance analysis script, conditioning sensitivity tables, and a complete decision table for every preregistered threshold.

Any release note, benchmark card update, manuscript, or public report using this retest wave must cite both this preregistration and `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`. If any analysis deviates from this preregistration after outcome inspection, the deviation must be labeled exploratory and must not be used as confirmatory evidence for event-study, trend, or longitudinal benchmark claims.
