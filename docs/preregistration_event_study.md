# ANX-Bench v0.1 Event-Study Preregistration Protocol

This protocol defines the fixed preregistration template for every ANX-Bench longitudinal wave and every event-study claim made under the v0.1 benchmark line. A completed preregistration file is a study artifact, not an optional analysis note. It must be written, dated, versioned, and stored before response data from the relevant wave are inspected.

The protocol is designed to make ANX-Bench waves standardized, repeatable, versioned, and auditable. It separates exposure definition from outcome inspection, fixes the analysis population before scoring, and makes longitudinal claims depend on an explicit benchmark version, item set, sampling frame, and analysis freeze date.

## Required File Naming

Each completed preregistration must be saved as:

```text
docs/preregistrations/anx_wave_<wave_id>_event_study.md
```

The `wave_id` must be stable across all materials for the wave, including survey instruments, fielding logs, analysis scripts, release notes, and public reports. If a wave is not tied to a discrete AI event, the file must still be completed and must mark the event-study fields as `not_applicable` with a reason.

## Preregistration Status

Complete this section before fielding begins.

| Field | Required content |
| --- | --- |
| Preregistration title | Human-readable study title. |
| Wave ID | Stable identifier, for example `anx_us_2026w01`. |
| Preregistration version | Semantic version for this preregistration file. |
| Benchmark version | Released ANX-Bench version, for example `v0.1.0`. |
| Preregistration author and approver | Names, roles, affiliations, and approval date. |
| Date created | Calendar date when the preregistration file was first written. |
| Last allowed amendment date | Final date on which amendments may be made before outcome inspection. |
| Response data inspection lock | Statement that no response outcomes, score distributions, subgroup estimates, or item-level response summaries have been inspected before finalizing this file. |
| Analysis freeze date | Calendar date after which the primary analysis specification, exclusion rules, item set, weighting plan, and event windows are frozen. |

Amendments after the analysis freeze date are permitted only for clerical correction or documented error repair. Any substantive amendment after response data inspection must be labeled exploratory and cannot support a confirmatory longitudinal or event-study claim.

## Wave Definition

Complete this section for every ANX-Bench wave.

| Field | Required content |
| --- | --- |
| Wave ID | Stable wave identifier used in all study materials. |
| Fielding dates | Planned start and end dates, plus allowed extensions if quotas are not met. |
| Benchmark version | Exact benchmark release used for administration. |
| Item versions | Complete list of item IDs and item versions administered in the wave. |
| Instrument language and mode | Language, survey mode, device restrictions, interviewer involvement, and accessibility accommodations. |
| Target population | Population to which estimates are intended to generalize, including geography, age range, language eligibility, and any domain-specific eligibility. |
| Sampling frame | Source population and recruitment mechanism, such as probability panel, address-based sample, occupational registry, or nonprobability panel. |
| Planned sample size | Target completed responses overall and within preregistered strata. |
| Power or precision rationale | Minimum detectable change or expected confidence interval width for the primary overall ANX estimate and key domain estimates. |
| Weighting plan | Base weights, post-stratification or raking targets, trimming rules, replicate weights if used, and whether unweighted estimates will be reported only as descriptive summaries. |
| Exclusion rules | Complete respondent-level and item-level exclusions applied before scoring. |
| Quality controls | Attention checks, straightlining rules, speeding thresholds, duplicate detection, bot detection, and language comprehension criteria. |
| Analysis freeze date | Date on which the wave definition, item list, exclusions, weights, and primary analysis become fixed. |

The item version list is part of the benchmark contract. A wave cannot be used for longitudinal comparison unless the administered item versions match a released benchmark item set or a documented bridge study supports comparability.

## Event Definition

Complete this section before inspecting response data whenever the wave will support an event-study claim.

| Field | Required content |
| --- | --- |
| AI event name | Short, specific event name, for example `Model X public release` or `AI video deepfake incident`. |
| Event description | Factual description of the event without reference to ANX-Bench outcomes. |
| Independent timestamp source | External source used to timestamp the event, such as an official release note, regulatory filing, public incident report, archived news wire, or other independently archived record. |
| Event timestamp | Date, time, time zone, and URL or citation for the timestamp source. |
| Exposure window | Start and end times defining when participants are considered exposed to the event. |
| Baseline window | Pre-event response window used to estimate baseline ANX scores. |
| Follow-up windows | One or more post-event windows, for example `0 to 72 hours`, `4 to 14 days`, and `15 to 30 days`. |
| Event classification | Preregistered category such as `frontier_model_release`, `capability_demonstration`, `AI_safety_incident`, `labor_market_announcement`, `policy_or_regulatory_action`, `misinformation_or_deepfake_incident`, or `other_prespecified`. |
| Classification rationale | Reason the event belongs to the selected category, based only on external evidence available before outcome inspection. |
| Expected affected domains | Domains expected to move, stated as hypotheses rather than post hoc findings. |
| Competing events | Known contemporaneous AI or non-AI events that could affect interpretation. |
| Event log lock | Confirmation that the event was logged before response data inspection. |

Events must be logged before inspecting ANX-Bench response data. The event log must not be edited after outcome inspection to add, remove, reclassify, or retime events for confirmatory analysis. Later changes may be reported only as exploratory sensitivity analyses.

## Primary Outcomes

All primary outcomes use scored ANX-Bench responses after applying released item scoring keys, exclusion rules, and the preregistered weighting plan.

| Outcome level | Definition | Required reporting |
| --- | --- | --- |
| Overall ANX score | Equal-weighted mean of valid domain scores under the benchmark methodology. | Point estimate, standard error, confidence interval, weighted sample size, unweighted respondent count, exclusions, and missingness. |
| Domain scores | Equal-weighted mean of valid construct scores within each released ANX-Bench domain. | Domain-specific point estimate, confidence interval, contributing constructs, contributing items, and missingness. |
| Construct scores | Mean of valid item scores assigned to the same construct. | Construct-specific point estimate, confidence interval, contributing items, and reliability or internal consistency estimate when enough items exist. |
| Item-level scores | Scored value for each released item version. | Item mean, response distribution, confidence interval, missingness, and item version. |

Primary reports must use two-sided 95 percent confidence intervals unless a different interval level is preregistered with justification. For weighted survey estimates, interval construction must account for the weighting design when design information is available.

Multiple-comparison correction is required for confirmatory claims beyond the single primary overall ANX estimate. Domain-level families must use Holm correction across the seven top-level domains. Construct-level families must use Benjamini-Hochberg false discovery rate control within each domain unless the preregistration specifies a stricter familywise method. Item-level analyses are exploratory by default unless specific item-level hypotheses are named before the analysis freeze date, in which case they must be corrected within the preregistered item family.

## Minimum Statistical Plan

Every completed preregistration must specify the following analyses before outcome inspection.

### Pre/Post Difference

Estimate the difference between baseline and each follow-up window for the overall ANX score and for all preregistered domain outcomes:

```text
Delta_k = mean(ANX_i | follow-up window k) - mean(ANX_i | baseline window)
```

Report weighted and unweighted respondent counts, point estimates, 95 percent confidence intervals, and corrected p-values for confirmatory comparisons. If the same respondents appear in baseline and follow-up windows, use paired estimators or respondent fixed effects as specified before analysis. If the design uses repeated cross sections, use independent-sample estimators with the preregistered weighting plan.

### Stratified Subgroup Estimates

Report subgroup estimates for strata that are defined before analysis. At minimum, each wave must specify whether estimates will be stratified by:

- Age group.
- Gender.
- Education.
- Occupation or labor-market exposure group.
- Prior AI use.
- Political or regulatory attitude variables, if collected.
- Country, region, or language group, if the wave covers multiple populations.

Subgroup estimates must include confidence intervals and sample sizes. Confirmatory subgroup interaction claims require correction within the subgroup family. Subgroups with insufficient effective sample size must be suppressed or labeled unstable according to the preregistered threshold.

### Regression and Event-Study Model

The minimum confirmatory model for repeated cross-sectional data is:

```text
ANX_score_i = alpha
            + beta_1 PostEventWindow_i
            + beta_2 EventClassification_i
            + gamma' Covariates_i
            + delta_s Stratum_s
            + epsilon_i
```

For multiple follow-up windows, replace `PostEventWindow_i` with window indicators:

```text
ANX_score_i = alpha
            + sum_k beta_k FollowUpWindow_ki
            + gamma' Covariates_i
            + delta_s Stratum_s
            + epsilon_i
```

For panel data with repeated respondents, use:

```text
ANX_score_it = alpha_i
             + sum_k beta_k FollowUpWindow_kit
             + gamma' TimeVaryingCovariates_it
             + tau_t CalendarTime_t
             + epsilon_it
```

The preregistration must state which model applies, which score level is the dependent variable, how survey weights enter the model, how standard errors are clustered or design-adjusted, and whether calendar-time controls are included.

### Covariates

At minimum, covariates must include the variables needed to support the sampling and weighting plan. Candidate covariates include age, gender, education, region, occupation, employment status, income band, prior AI use, baseline technology attitude, political ideology or regulatory preference where ethically and legally appropriate, survey mode, and fielding date.

Covariates must be selected before outcome inspection. Adding covariates after inspecting results is exploratory unless the addition repairs a documented implementation error.

### Missing-Data Handling

The preregistration must specify:

- Item-level missingness rules before construct, domain, and overall scores are computed.
- Respondent-level exclusion thresholds.
- Whether missing covariates are handled by complete-case analysis, missingness indicators, inverse-probability adjustment, or multiple imputation.
- Whether imputed outcomes are allowed. Primary ANX-Bench analyses should not impute missing item outcomes unless a missing-data model is explicitly preregistered.
- Sensitivity analyses for missingness when item nonresponse, attrition, or panel dropout exceeds the preregistered threshold.

All reports must distinguish analytic sample size, fielded sample size, excluded respondents, and respondents with partial score coverage.

### Measurement-Invariance Check Trigger

A measurement-invariance check is required before making a longitudinal, subgroup, cross-language, or cross-population comparability claim when any of the following conditions hold:

- A new language, country, administration mode, or recruitment source is introduced.
- More than 20 percent of respondents in a comparison come from a population not represented in the prior validation evidence.
- Any item wording, response anchor, exclusion rule, or scoring key differs from the released item version.
- The domain or overall score changes by at least 0.20 standard deviations between waves and the change is used as a substantive claim.
- Differential missingness across comparison groups exceeds 10 percentage points for any domain score.
- Item reliability, factor loading patterns, or item response distributions show unexpected instability relative to prior waves.

The preregistration must state the planned invariance procedure, such as multi-group confirmatory factor analysis, alignment optimization, item response theory differential item functioning checks, or a documented bridge study. If invariance is not supported, reports must limit claims to non-comparable descriptive estimates or provide calibrated estimates with the calibration method disclosed.

## Reporting Requirements

Every wave report or event-study release must include:

- The completed preregistration file path and version.
- Benchmark version and item versions.
- Fielding dates and event timestamp.
- Sampling frame, target population, exclusions, and weighting plan.
- Analysis freeze date.
- Primary estimates with confidence intervals.
- Multiple-comparison correction method.
- Missing-data summary.
- Measurement-invariance result or a statement that no trigger was met.
- A distinction between confirmatory, preregistered analyses and exploratory analyses.

No ANX-Bench release may present a longitudinal wave comparison or event-study result as confirmatory unless the completed preregistration file existed before response data inspection and satisfies this protocol.
