# ANX-Bench Psychometric Validation Protocol

This protocol defines the release-blocking psychometric validation gate for ANX-Bench items. It applies to every item before the item can move from exemplar or development status into benchmark-scored status. Schema-valid items may be used for drafting, cognitive interviewing, and pilot administration, but they are not released benchmark-scored items until the evidence required here has been completed, reviewed, versioned, and archived.

The purpose of the gate is to make ANX-Bench a reproducible measurement instrument rather than a collection of plausible survey prompts. The protocol requires independent development and confirmation samples, explicit dimensionality checks, reliability evidence, item response modeling, differential item functioning review, and measurement-invariance evidence for intended comparisons across waves, populations, languages, and administration modes.

## Validation Artifacts

Each item or item set submitted for benchmark-scored release must have a validation dossier stored with the release materials. The dossier must include:

- The benchmark version, item IDs, item versions, domain assignments, construct assignments, and response scale.
- The development pilot sampling plan, fielding dates, recruitment source, exclusions, and analytic sample.
- The independent confirmation sampling plan, fielding dates, recruitment source, exclusions, and analytic sample.
- The refresh or bridge sampling plan for any revised item, translated item, changed administration mode, or new population used for longitudinal comparison.
- Analysis scripts or reproducible notebooks for factor analysis, reliability, IRT, DIF, measurement invariance, missingness, and response-distribution checks.
- A retention table listing every candidate item, every psychometric decision rule, the observed statistic, and the retain, revise, or exclude decision.
- A reviewer signoff stating whether the item is approved for benchmark-scored status, approved only for exploratory development use, or blocked.

The dossier is part of the benchmark contract. A release may include exemplar or development items without a completed dossier only if they are clearly labeled as non-scored and excluded from benchmark scoring, longitudinal comparison, and event-study outcomes.

## Minimum Calibration Samples

Validation requires three sample types unless a documented reason makes one not applicable. Convenience samples may be used during early drafting, but they do not satisfy this gate unless they also meet the sampling and documentation requirements below.

| Sample | Minimum analytic sample | Required purpose |
| --- | ---: | --- |
| Development pilot | 500 completed eligible respondents overall, with at least 150 respondents in each major population stratum used for item development decisions when stratified results are reviewed. | Cognitive and statistical item development, exploratory factor analysis, preliminary reliability, response-distribution checks, and early DIF screening. |
| Independent confirmation sample | 1,000 completed eligible respondents overall, fielded after the development pilot and recruited from a non-overlapping respondent pool. | Confirmatory factor analysis, final reliability estimates, IRT calibration, preregistered DIF checks, and approval for benchmark-scored release. |
| Refresh or bridge sample | 500 completed eligible respondents overall, plus at least 300 respondents who receive both the prior and revised forms when direct comparability is claimed. | Calibration of revised wording, translations, changed response anchors, new administration modes, or population extensions against the released item version. |

If the instrument includes domain or construct scores, the confirmation sample must include enough respondents for stable estimates at that score level. As a default, each domain submitted for release must have at least 300 respondents with valid responses to the relevant item set after exclusions. Smaller domain samples may support exploratory reporting, but they cannot support benchmark-scored release without a written precision justification approved before outcome inspection.

No respondent may contribute to both the development pilot and the independent confirmation sample for the same item version. Refresh and bridge samples may overlap with a live benchmark wave only if the bridge design, item order, randomization, and analytic plan are fixed before response outcomes are inspected.

## Pilot Design Requirements

The development pilot must be designed to find bad items, not to defend drafted items. It must include:

- A sampling frame that matches the intended benchmark population or the specific development population under review.
- Quotas or post-stratification variables for age, gender, education, geography, AI exposure, and any domain-relevant subgroup such as occupation for economic or vocational items.
- Randomized item order within domains unless a fixed order is theoretically required and documented.
- At least one attention or comprehension quality control that is not scored as an ANX-Bench item.
- Open-text debriefing or cognitive-interview evidence for items with high nonresponse, ambiguous interpretation, or ethically sensitive wording.
- Documentation of exclusions before factor analysis, reliability estimation, IRT, DIF, and response-distribution review.

Development pilot analyses may be exploratory. However, item retention decisions must be recorded before the independent confirmation sample is analyzed. Items modified after the development pilot must receive a new item version before confirmation.

## EFA and CFA Split

Dimensionality evidence must be separated between exploratory and confirmatory samples.

Exploratory factor analysis must be conducted on the development pilot. The analysis must use an ordinal correlation approach appropriate for Likert responses, such as polychoric correlations, unless a different method is justified in the dossier. The number of factors must be evaluated using parallel analysis, scree inspection, theoretical interpretability, and domain coverage. Oblique rotation is required unless the dossier justifies an orthogonal structure.

Confirmatory factor analysis must be conducted only on the independent confirmation sample or on a held-out confirmation split that was fixed before analysis. The CFA model must match the retained construct structure from the development pilot. For ordinal item responses, estimation must use an estimator appropriate for ordered categorical data or otherwise justify the treatment of responses as continuous.

The default CFA fit targets for a construct or domain item set are:

- Comparative fit index at least 0.95 for strong support, with 0.90 to 0.949 requiring written justification.
- Tucker-Lewis index at least 0.95 for strong support, with 0.90 to 0.949 requiring written justification.
- Root mean square error of approximation at most 0.06 for strong support, with 0.061 to 0.08 requiring written justification.
- Standardized root mean square residual at most 0.08.

Modification indices may be inspected for diagnosis, but post hoc correlated residuals or cross-loadings cannot be used to approve an item unless the revised model is confirmed in a new independent sample or a preregistered holdout split.

## Reliability Targets

Reliability must be reported at the construct, domain, and overall score levels when enough items exist at each level. Single items may be released only as item-level indicators and must not be represented as internally reliable scales.

The minimum reliability targets are:

- Ordinal alpha or coefficient omega of at least 0.70 for early benchmark-scored construct use.
- Coefficient omega of at least 0.80 for mature construct scores used in headline reporting.
- Test-retest reliability of at least 0.70 over a 7 to 21 day interval for constructs expected to be stable absent major AI events.
- Standard error of measurement reported for construct, domain, and overall scores whenever scale scores are released.

If alpha and omega disagree materially, omega is the preferred decision statistic because ANX-Bench constructs are not assumed to be tau-equivalent. Low reliability blocks benchmark-scored release unless the item is explicitly retained only as a standalone item-level outcome with no construct, domain, or overall aggregation role.

## IRT Calibration

Every multi-item construct submitted for benchmark-scored release must receive an item response theory review in the independent confirmation sample. Ordinal items should be evaluated with a graded response model or another model suitable for ordered Likert categories.

The IRT review must report:

- Item discrimination parameters.
- Ordered threshold parameters and any disordered thresholds.
- Item and test information across the latent anxiety range.
- Local dependence diagnostics.
- Person or response-pattern fit diagnostics used to identify unstable item behavior.

Items with very low discrimination, disordered thresholds that cannot be explained substantively, severe local dependence, or negligible information across the intended score range must be revised or excluded before release. IRT parameters used for scoring or linking must be versioned with the item release.

## DIF Checks

Differential item functioning must be evaluated before benchmark-scored release for any subgroup that will be used in public comparison, weighting, longitudinal analysis, or event-study reporting. At minimum, the confirmation sample must screen for DIF by age group, gender, education, geography or country when applicable, prior AI use, and administration language or mode when applicable.

DIF may be evaluated with ordinal logistic regression, multi-group IRT, multiple-indicators multiple-causes modeling, or another documented method appropriate for ordinal items. The method, grouping variables, minimum subgroup sample sizes, covariates, and multiple-testing correction must be fixed before confirmation outcomes are inspected.

An item is blocked from benchmark-scored release when DIF is both statistically supported after correction and practically meaningful. Practical significance is defined by at least one of the following unless a stricter preregistered threshold is used:

- A change in pseudo-R-squared of 0.02 or greater in ordinal logistic DIF screening.
- A standardized expected score difference of 0.10 standard deviations or greater for a focal group at the same latent trait level.
- A material change in domain or construct rank ordering across groups after removing the item.

Items with unstable DIF across the development pilot, confirmation sample, and refresh or bridge sample must be excluded from scored release until a revised item version demonstrates stable behavior in a new confirmation sample. A scored release must not average across known unstable DIF and describe the result as comparable.

## Measurement-Invariance Thresholds

Measurement invariance is required for any released item set used to compare groups, languages, modes, or waves. Multi-group CFA, alignment optimization, IRT linking, or a documented bridge design may be used, but the method must match the score claim being made.

For multi-group CFA, the default sequence is configural, metric, scalar, and residual invariance when residual invariance is required for the claim. Thresholds are:

- Configural invariance: same factor structure, no gross group-specific misfit, and acceptable fit in each group with adequate sample size.
- Metric invariance: change in CFI no less than -0.010 and change in RMSEA no greater than 0.015 relative to configural invariance.
- Scalar invariance: change in CFI no less than -0.010 and change in RMSEA no greater than 0.015 relative to metric invariance.
- Residual invariance: required only for strict comparison of observed item residuals, with change in CFI no less than -0.010 and change in RMSEA no greater than 0.015 relative to scalar invariance.

Partial invariance may support benchmark use only when non-invariant parameters are named, theoretically justified, and small enough that construct, domain, and overall score conclusions are unchanged in sensitivity analysis. If scalar invariance or a validated linking alternative is not supported, ANX-Bench may report descriptive group means but must not claim that score differences represent comparable differences in latent anxiety.

## Item Retention Rules

Candidate items must satisfy all retention rules before benchmark-scored release:

| Criterion | Required threshold |
| --- | --- |
| Primary factor loading | Standardized loading at least 0.50 in the confirmation sample. Items from 0.40 to 0.49 may be retained only with written construct-coverage justification and no stronger replacement item available. |
| Cross-loading | No secondary loading greater than 0.30, and no secondary loading within 0.20 of the primary loading. |
| Corrected item-total correlation | At least 0.30 with the intended construct score, excluding the item from the total. |
| Ceiling or floor response concentration | No more than 70 percent of valid responses in the lowest category or highest category, and no more than 85 percent in the two lowest or two highest adjacent categories unless the item is intentionally targeted to an extreme-risk construct and retains adequate IRT information. |
| Missing or non-substantive response | Item-level missing, prefer-not-to-answer, or unusable response rate no greater than 10 percent in the confirmation sample and no greater than 15 percent in any public comparison subgroup. |
| DIF stability | No statistically supported and practically meaningful DIF that is unstable across samples or unresolved for intended public comparisons. |
| Local dependence | No residual association or IRT local dependence large enough to duplicate another item or inflate reliability without unique construct coverage. |

Failure on any rule blocks benchmark-scored release for that item version. The item may remain in exemplar or development status if clearly labeled as non-scored and excluded from official benchmark scoring.

## Revised Items and Bridge Studies

Any change to participant-facing wording, response anchors, administration mode, language, scoring key, exclusion rule, or interpretation band requires a refresh or bridge evaluation before the revised item can support longitudinal comparison.

The bridge study must include:

- The prior released item version and the revised item version.
- Randomized order or counterbalancing when both versions are administered to the same respondents.
- A linking analysis estimating whether the revised item preserves the prior scale location and discrimination.
- DIF and invariance checks for the revised item against the intended comparison groups.
- A release decision stating whether the revision is patch-level, minor but bridged, or breaking.

If bridge evidence is inadequate, the revised item may be released only as a new non-comparable item version or new item ID. It must not be pooled with prior responses in longitudinal or event-study estimates.

## Release Decision

The psychometric validation gate has four possible decisions:

- `approved_scored`: The item version satisfies this protocol and may contribute to construct, domain, overall, longitudinal, and event-study scoring according to the release notes.
- `approved_item_level_only`: The item version may be reported as a standalone scored item but must not contribute to construct, domain, or overall aggregation.
- `development_only`: The item version is schema-valid and may be used in pilots or exemplars, but it is excluded from benchmark scoring.
- `blocked`: The item version must not be fielded as part of an ANX-Bench release until revised and revalidated.

The decision must be recorded before release. Any public benchmark artifact must distinguish schema validation, development status, item-level scoring status, and full benchmark-scored status.
