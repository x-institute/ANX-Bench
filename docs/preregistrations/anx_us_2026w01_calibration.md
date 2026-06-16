# ANX-Bench US 2026 Wave 1 Calibration Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w01_calibration.md`
- Study label: `anx_us_2026w01_calibration`
- Benchmark release line: `ANX-Bench v0.1.x`
- Administered item directory: `items/v0.1`
- Frozen fielding instrument: `docs/instruments/anx_us_2026w01_instrument.md`
- Frozen Wave 1 codebook: `docs/instruments/anx_us_2026w01_codebook.md`
- Behavioral validation protocol: `docs/behavioral_validation_protocol.md`
- Instrument freeze date: `2026-06-15`
- Planned development pilot fielding window: `FIELDING_START_DEVELOPMENT_PILOT` to `FIELDING_END_DEVELOPMENT_PILOT`
- Planned independent confirmation fielding window: `FIELDING_START_CONFIRMATION` to `FIELDING_END_CONFIRMATION`
- Fielding rule for placeholders: final calendar dates must be inserted before respondent recruitment starts. If dates are changed after fielding begins, the change must be recorded as an addendum and cannot be justified by outcome data.
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Primary validation purpose: first psychometric calibration of the `items/v0.1` development item set in the US adult population
- Scoring status at registration: no item in this wave is preregistered for official aggregate ANX scoring

This preregistration is a completed Wave 1 calibration plan for the first ANX-Bench validation wave. It is not a template for future waves. It freezes the administered item versions, target population, sampling plan, quality control rules, exclusion rules, and primary psychometric analyses before outcome data are inspected.

The participant-facing survey flow and non-ANX variable definitions are frozen as fielding artifacts, not merely described in this preregistration. `docs/instruments/anx_us_2026w01_instrument.md` is the authoritative Wave 1 administration packet for consent language, respondent instructions, randomized ANX item block, required attention check, required scenario-comprehension check, behavioral review allocation task, optional debrief comment, final debrief, and distress language. `docs/instruments/anx_us_2026w01_codebook.md` is the authoritative Wave 1 codebook for demographics, occupation, AI exposure, behavioral criterion validation, quality-control variables, response-time variables, weighting variables, restricted vendor IDs, and mapping into `schema/wave_response.schema.json` and `schema/behavioral_response.schema.json`.

## Administered Item Set

The following item IDs and versions are the only ANX-Bench items included in this calibration preregistration. Participant-facing scenario text, response prompts, anchors, scoring keys, exclusion notes, and item metadata are taken exactly from the listed JSON files as of the instrument freeze date.

| Domain | Item ID | Version | File | Construct ID | Current release status |
| --- | --- | --- | --- | --- | --- |
| autonomy_surveillance | `institutional_scoring_automation` | `v0.1.0` | `items/v0.1/autonomy_surveillance/institutional_scoring_automation.json` | `autonomy_surveillance_ai_anxiety_anchor` | `development_only` |
| economic_vocational | `job_displacement_radiology` | `v0.1.0` | `items/v0.1/economic_vocational/job_displacement_radiology.json` | `anticipated_job_displacement_anxiety` | `exemplar` |
| economic_vocational | `retraining_pressure_accounting` | `v0.1.0` | `items/v0.1/economic_vocational/retraining_pressure_accounting.json` | `economic_vocational_anxiety` | `development_only` |
| economic_vocational | `skill_obsolescence_software` | `v0.1.0` | `items/v0.1/economic_vocational/skill_obsolescence_software.json` | `economic_vocational_anxiety` | `development_only` |
| economic_vocational | `status_loss_creative_work` | `v0.1.0` | `items/v0.1/economic_vocational/status_loss_creative_work.json` | `economic_vocational_anxiety` | `development_only` |
| economic_vocational | `wage_pressure_customer_support` | `v0.1.0` | `items/v0.1/economic_vocational/wage_pressure_customer_support.json` | `economic_vocational_anxiety` | `development_only` |
| epistemic | `ai_expert_claim_conflict` | `v0.1.0` | `items/v0.1/epistemic/ai_expert_claim_conflict.json` | `epistemic_trust_anxiety` | `development_only` |
| epistemic | `deepfake_evidence_trust` | `v0.1.0` | `items/v0.1/epistemic/deepfake_evidence_trust.json` | `epistemic_trust_anxiety` | `development_only` |
| epistemic | `personalized_misinformation_targeting` | `v0.1.0` | `items/v0.1/epistemic/personalized_misinformation_targeting.json` | `epistemic_trust_anxiety` | `development_only` |
| epistemic | `synthetic_news_provenance` | `v0.1.0` | `items/v0.1/epistemic/synthetic_news_provenance.json` | `epistemic_trust_anxiety` | `development_only` |
| existential_identity | `creativity_status_displacement` | `v0.1.0` | `items/v0.1/existential_identity/creativity_status_displacement.json` | `existential_identity_ai_anxiety_anchor` | `development_only` |
| relational | `child_companion_attachment` | `v0.1.0` | `items/v0.1/relational/child_companion_attachment.json` | `relational_ai_anxiety_anchor` | `development_only` |
| safety_catastrophic | `ai_enabled_systemic_harm` | `v0.1.0` | `items/v0.1/safety_catastrophic/ai_enabled_systemic_harm.json` | `safety_catastrophic_ai_anxiety_anchor` | `development_only` |
| somatic_ambient | `ambient_bodily_unease` | `v0.1.0` | `items/v0.1/somatic_ambient/ambient_bodily_unease.json` | `somatic_ambient_ai_anxiety_anchor` | `development_only` |

All administered ANX-Bench items use the same ordered 5-point anxiety response scale:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

Item order will be randomized within the full ANX-Bench block for the development pilot and the independent confirmation sample. The response scale will always be displayed in ascending order from 1 to 5. No item wording, anchors, scoring key, or item metadata may be changed after this preregistration is frozen unless the modified item receives a new version and is excluded from the preregistered `v0.1.0` calibration analyses.

## Frozen Fielding Instrument and Codebook

Wave 1 recruitment may begin only after the fielding vendor implementation has been checked against the frozen instrument and codebook:

- The consent stub, instructions, item screens, attention check, scenario-comprehension check, understanding check, optional debrief comment prompt, final debrief, and distress language must match `docs/instruments/anx_us_2026w01_instrument.md`.
- The 14 ANX item screens must be presented exactly once per respondent in a respondent-level uniform random order. Response anchors must remain in ascending order from 1 to 5.
- The attention check is preregistered as an instructed-response item requiring response 3, "Moderately anxious." Failure maps to `attention_check_failed`.
- The scenario-comprehension check is preregistered as a required check requiring response 1, "They were hypothetical research scenarios about possible AI capabilities and social effects." Failure maps to `other_preregistered_exclusion` with restricted reason `scenario_comprehension_failed`.
- The self-reported understanding check is preregistered as a required check. Responses indicating that the respondent understood only a few scenarios or did not understand the scenarios map to `quality_review_failed`.
- The behavioral review allocation task is preregistered as a post-ANX, pre-demographics revealed-preference criterion task. Respondents are uniformly randomized to one of four high-impact decision vignette arms and allocate exactly $1.00 between AI-only review and human review. The behavioral task comprehension check requires response 1, "A $1.00 review budget between AI-only review and human review." Failure maps to behavioral exclusion flag `behavioral_comprehension_failed` for confirmatory behavioral validity models.
- Non-ANX respondent-level variables, paradata, vendor operational variables, public-data exclusions, and schema mappings must follow `docs/instruments/anx_us_2026w01_codebook.md`.

Any change to participant-facing wording, response anchors, required status, item randomization, quality-control scoring, debrief language, distress language, or codebook-defined public-data exclusions after recruitment begins must be recorded as an addendum and cannot be justified by observed outcome data.
Any change to behavioral task wording, randomized behavioral vignette arms, allocation UI rules, comprehension-check scoring, `revealed_anxiety_score` derivation, or behavioral exclusion flags after recruitment begins must also be recorded as an addendum and cannot be justified by observed outcome data.

## Population, Sampling Frame, and Samples

The target population is non-institutionalized US adults aged 18 years or older who can complete an English-language online survey without assistance and can provide informed consent. The intended inference population is the US adult population reachable through a professional online survey panel or probability-based panel with demographic profiling sufficient for quota sampling and post-stratification.

The sampling frame will be a US adult online panel maintained by the contracted survey vendor. The vendor must provide panel-level controls or profile variables for age, gender, race and ethnicity, Census region, education, household income, employment status, occupation group, urbanicity, political party identification or ideology, and prior AI exposure. Panel members who participated in the development pilot are ineligible for the independent confirmation sample.

This preregistration includes two non-overlapping samples, matching `docs/psychometric_validation_protocol.md`:

| Sample | Planned completed eligible analytic N | Role |
| --- | ---: | --- |
| Development pilot | 500 | Item distribution checks, missingness review, exploratory factor analysis, preliminary reliability, early IRT diagnostics, cognitive debrief review, and item retention recommendations before confirmation. |
| Independent confirmation sample | 1000 | Confirmatory factor analysis, final reliability estimates, graded-response IRT calibration, preregistered DIF checks, measurement-invariance screens where sample sizes permit, and release decision evidence for item validation dossiers. |

Recruitment will continue until the target number of eligible completes is reached after removing duplicate respondents, respondents outside eligibility criteria, respondents with unusable survey records, and respondents failing preregistered survey-level quality controls. Over-recruitment is permitted only to offset expected exclusions and quota balancing.

## Quotas and Weighting Variables

Both samples will use soft quotas to approximate the US adult population. Quotas will be monitored during fielding and evaluated before analytic weights are constructed. The target marginal quota variables are:

- Age group: 18 to 29, 30 to 44, 45 to 59, 60 or older.
- Gender: woman, man, nonbinary or another gender, with nonbinary or another gender not forced to a fixed population target if vendor feasibility requires monitoring rather than quota closure.
- Race and ethnicity: Hispanic or Latino; non-Hispanic White; non-Hispanic Black; non-Hispanic Asian; non-Hispanic other or multiracial.
- Education: high school or less, some college or associate degree, bachelor's degree, graduate degree.
- Census region: Northeast, Midwest, South, West.
- Employment status: employed full-time, employed part-time, self-employed, unemployed and looking, student, retired, not in labor force for another reason.
- Prior AI exposure: never or rare use, monthly use, weekly use, daily or near-daily use.

Post-stratification or raking weights will be generated separately for the development pilot and confirmation sample. The minimum weighting variables are age group, gender, race and ethnicity, education, Census region, and employment status. Prior AI exposure and occupation group will be included as calibration or trimming variables if the vendor provides stable benchmark margins or if internal sample imbalance threatens the economic/vocational analyses. Weights will be trimmed so that no final weight is below 0.30 or above 3.00 unless a written sensitivity analysis shows that a wider range is necessary and does not change primary conclusions.

Unweighted analyses are primary for psychometric model estimation unless the method supports survey weights cleanly. Weighted descriptive item distributions will be reported as population-facing descriptive estimates. Sensitivity analyses will compare weighted and unweighted item distributions, factor loadings where feasible, and DIF conclusions.

## Eligibility, Exclusion Rules, and Quality Control

Eligibility criteria:

- Respondent is aged 18 or older.
- Respondent resides in the United States.
- Respondent can read and answer the English survey unaided.
- Respondent provides informed consent.
- Respondent is not a duplicate participant in the same sample.
- Respondent in the confirmation sample did not complete the development pilot.

Exclusion rules applied before primary analyses:

- Exclude respondents who fail the survey-level instructed-response attention check.
- Exclude respondents who fail a scenario comprehension check asking whether the items described hypothetical AI capability scenarios rather than personal predictions about the respondent's own employer, school, child, medical provider, or government file.
- Exclude respondents with a survey completion time less than one-third of the median completion time for the same sample after removing clear breakoffs.
- Exclude respondents who give the same substantive response to every ANX-Bench item and also fail either the attention check or a minimum reading-time check.
- Exclude respondents with missing or non-substantive responses on more than 30 percent of administered ANX-Bench items.
- Exclude respondents with duplicate panel identifiers, duplicate survey tokens, or duplicate device fingerprints when vendor records indicate the same person submitted multiple completes.
- Exclude respondents who self-report that they could not understand most of the scenarios.

The exact participant-facing text, correct responses, and variable mappings for the attention check, scenario-comprehension check, and self-reported understanding check are preregistered in `docs/instruments/anx_us_2026w01_instrument.md` and `docs/instruments/anx_us_2026w01_codebook.md`. These checks are therefore frozen administration rules for Wave 1, not post-fielding quality-control judgments.

Quality control checks that do not automatically exclude by themselves:

- Item-level response time less than one-third of the sample median item time.
- Long-string responding within the ANX-Bench block.
- Extremely high Mahalanobis distance or improbable response pattern under the fitted IRT model.
- Open-text debrief comments indicating confusion, satire, protest responding, or distress.
- Device, browser, and IP metadata patterns flagged by the vendor as low confidence but not confirmed duplicate or fraudulent.

Excluded records will be counted in a CONSORT-style flow table for each sample. Exclusion rates will be reported overall and by quota variables. If any subgroup has more than 15 percent excluded records, analyses involving that subgroup will be flagged for sensitivity review.

## Outcomes

Primary outcomes for Wave 1 calibration are item-level response distributions for each administered item. For each item and sample, the report will include the count and percentage in each response category, item mean and standard deviation reported only as descriptive summaries of ordered categories, median, interquartile range, item-level missingness, item response time distribution, floor concentration, ceiling concentration, and two-adjacent-category concentration.

The main exploratory construct outcome is the economic/vocational construct structure among the five economic/vocational items:

- `job_displacement_radiology`
- `skill_obsolescence_software`
- `wage_pressure_customer_support`
- `retraining_pressure_accounting`
- `status_loss_creative_work`

The second exploratory construct outcome is the epistemic trust anxiety construct structure among the four epistemic items:

- `deepfake_evidence_trust`
- `synthetic_news_provenance`
- `ai_expert_claim_conflict`
- `personalized_misinformation_targeting`

The five remaining non-economic, non-epistemic anchors are exploratory item-level domain coverage indicators only. They are not preregistered as single-item validated domains or as an aggregate scale.

No official aggregate ANX score, domain score, construct score, benchmark ranking, longitudinal index, event-study outcome, or public headline score will be computed from this calibration wave. Any scale-like statistics produced during EFA, CFA, reliability, or IRT are validation evidence only and do not authorize scored benchmark use unless a later validation dossier and release decision approve the relevant item versions.

## External Validity Hypotheses

The post-ANX validation module in `docs/instruments/anx_us_2026w01_instrument.md` is included to test external validity of candidate ANX construct scores before any future `approved_scored` release decision. These hypotheses are confirmatory for validation-dossier review, although they do not authorize official scoring in Wave 1 by themselves.

H1, convergent validity with AI and technology anxiety: retained ANX economic/vocational and epistemic trust anxiety scores will show moderate positive association with `tech_ai_anxiety_comparator_mean`. The expected zero-order Pearson or Spearman correlation, depending on distributional diagnostics fixed before analysis, is 0.30 to 0.60 in the independent confirmation sample. A correlation below 0.20 will be treated as weak convergent evidence. A correlation above 0.80 will be treated as possible redundancy and will require reviewer evaluation before any scored release.

H2, weaker association with general anxiety: retained ANX scores will correlate positively but more weakly with `general_anxiety_2item_mean` than with `tech_ai_anxiety_comparator_mean`. The expected association with general anxiety is 0.10 to 0.35. The difference between the ANX correlation with the AI and technology anxiety comparator and the ANX correlation with general anxiety will be estimated using a dependent-correlation test or bootstrap confidence interval. Failure to show a weaker general anxiety association will not automatically reject the item set, but it will block `approved_scored` status unless the validation dossier demonstrates that the score is not merely general distress.

H3, discriminant validity between economic and epistemic constructs: if both the economic/vocational and epistemic trust anxiety pools retain at least three items with adequate CFA fit, the two latent constructs will be positively correlated but empirically distinguishable. The expected latent or disattenuated correlation is below 0.80, and a two-factor model should fit better than a one-factor model by preregistered CFA comparison criteria. Economic/vocational items are expected to load more strongly on the economic factor than on the epistemic factor, and epistemic items are expected to load more strongly on the epistemic factor than on the economic factor.

H4, criterion validity for avoidance and regulation support: retained ANX scores will positively predict `ai_avoidance_intention_6m` and `ai_regulation_support_high_impact`. The expected bivariate association is positive and practically interpretable. Associations with `ai_adoption_intention_6m` are expected to be negative or weaker than the avoidance association because adoption intention also reflects perceived usefulness, work demands, and prior AI exposure.

H5, incremental validity: retained ANX scores will predict AI avoidance intention and AI regulation support after adjusting for demographics, AI exposure, and general anxiety. The covariate block will include age group, gender, education, Census region, employment status, prior AI exposure frequency, AI use for work or school, AI use for personal tasks, self-rated AI familiarity, and `general_anxiety_2item_mean`. The default pass threshold for validation-dossier review is either a change in adjusted `R^2` of at least 0.01 for linear models or a standardized ANX coefficient whose confidence interval excludes zero in ordinal or generalized models. For ordinal models, an odds ratio of at least 1.20 per one standard deviation increase in the ANX score will be treated as practically meaningful.

H6, behavioral criterion validity for revealed AI anxiety: retained ANX scores will positively predict `revealed_anxiety_score`, defined as `human_review_cents / 100` in the behavioral review allocation task. The theoretical expectation is that respondents with higher ANX construct scores allocate more of the $1.00 review budget to human review rather than AI-only review after a high-impact AI decision scenario. The primary behavioral score-level hypothesis pools all randomized behavioral arms and includes arm fixed effects. A domain-matched secondary hypothesis tests whether economic/vocational ANX scores are most predictive in the `employment_hiring` arm, autonomy/surveillance scores in the `public_benefits` arm, safety-related scores in the `healthcare_triage` arm, and relational scores in the `school_placement` arm when the relevant score is available.

H7, incremental behavioral validity: retained ANX scores will predict `revealed_anxiety_score` after adjusting for demographics, AI exposure, general anxiety, and behavioral randomized arm. The covariate block is age group, gender, education, Census region, employment status, prior AI exposure frequency, AI use for work or school, AI use for personal tasks, self-rated AI familiarity, `general_anxiety_2item_mean`, and fixed effects for `randomized_arm`. The pass threshold for behavioral criterion-validity evidence is a positive standardized ANX coefficient with a 95 percent confidence interval excluding zero and either adjusted `R^2` improvement of at least 0.01 over the covariate-only model or an adjusted mean difference of at least 0.03 in `revealed_anxiety_score` per one standard deviation increase in the retained ANX score. Effects below 0.01 on the 0 to 1 revealed score scale will be treated as too small for behavioral criterion validity even if statistically detectable.

## Analysis Plan

All analyses will be conducted separately for the development pilot and independent confirmation sample unless explicitly stated otherwise. Analytic scripts must preserve the distinction between exploratory pilot outputs and confirmation outputs.

### Response Distributions and Item Screening

For each item, report response-category frequencies, weighted and unweighted percentages, missingness, completion time, floor and ceiling concentration, and two-adjacent-category concentration. Items are flagged for revision or exclusion if more than 70 percent of valid responses fall in the lowest or highest category, more than 85 percent fall in the two lowest or two highest adjacent categories, item-level missing or unusable response exceeds 10 percent in the confirmation sample, or item-level missing or unusable response exceeds 15 percent in any public comparison subgroup.

### EFA and CFA Split

Exploratory factor analysis will use the `N=500` development pilot. Confirmatory factor analysis will use the non-overlapping `N=1000` independent confirmation sample. Confirmation models may not be modified using confirmation sample outcome inspection and then treated as preregistered evidence.

EFA will be conducted on ordinal item responses using polychoric correlations. The extraction method will be minimum residual or weighted least squares factor analysis appropriate for polychoric input. Rotation will be oblique. The number of retained factors will be evaluated using parallel analysis, scree inspection, factor interpretability, factor determinacy where available, item loading strength, cross-loading patterns, and domain coverage. The primary construct-level EFA targets are the five economic/vocational items and the four epistemic trust anxiety items. These pools will be evaluated separately and in a combined two-construct sensitivity model to identify cross-loadings or empirical collapse between occupational threat and epistemic trust anxiety. A secondary exploratory EFA including all 14 items may be reported only to describe cross-domain clustering and cannot support aggregate ANX scoring.

CFA will be conducted in the independent confirmation sample using an estimator appropriate for ordered categorical data, such as WLSMV. The primary CFA models will test the retained economic/vocational structure and the retained epistemic trust anxiety structure from the development pilot. If both pools retain at least three items, a correlated two-factor model will be estimated as a discriminant-validity sensitivity check. Strong fit support is defined as CFI at least 0.95, TLI at least 0.95, RMSEA at most 0.06, and SRMR at most 0.08. Fit with CFI or TLI from 0.90 to 0.949 or RMSEA from 0.061 to 0.080 requires written justification in the validation dossier. Worse fit blocks approval for aggregate construct scoring from these item versions.

### Reliability

Ordinal coefficient omega is the preferred reliability statistic. Ordinal alpha will be reported as a secondary statistic for comparability. Reliability will be computed only for item sets with at least three retained items and a substantively interpretable common construct. The early benchmark-scored threshold is omega at least 0.70. Mature headline construct scoring would require omega at least 0.80, but headline scoring is not requested in this wave. Single anchor items will not be described as internally reliable scales.

### IRT Calibration

The confirmation sample will be used to fit graded-response IRT models for any retained multi-item economic/vocational or epistemic trust anxiety structure with adequate dimensionality evidence. Models will report item discrimination parameters, ordered threshold parameters, item information, test information across the latent trait range, local dependence diagnostics, and person or response-pattern fit diagnostics. Disordered thresholds, very low discrimination, negligible information across the observed anxiety range, or severe local dependence will trigger a revise or exclude recommendation for the affected item version.

### DIF and Invariance

DIF screening in the confirmation sample will be preregistered for the following variables:

- Age group: 18 to 29, 30 to 44, 45 to 59, 60 or older.
- Gender: woman, man, and nonbinary or another gender when subgroup sample size permits.
- Race and ethnicity categories listed in the quota plan when subgroup sample size permits.
- Education: no bachelor's degree versus bachelor's degree or higher, with finer categories reported descriptively where powered.
- Census region: Northeast, Midwest, South, West.
- Employment status: employed versus not employed, plus occupation group for economic/vocational items when sample size permits.
- Prior AI exposure: never or rare use, monthly use, weekly use, daily or near-daily use.
- Political ideology or party identification if collected by the vendor.
- Survey device type: desktop or laptop versus mobile or tablet.

DIF will be evaluated using ordinal logistic regression and, when the retained IRT model is stable, multi-group IRT or MIMIC sensitivity models. Multiple testing will be controlled within item families using Benjamini-Hochberg false discovery rate at 0.05. DIF is practically meaningful if pseudo-R-squared change is at least 0.02, expected score difference is at least 0.10 standard deviations for a focal group at the same latent trait level, or the item materially changes group rank ordering for the economic/vocational or epistemic trust anxiety construct.

Measurement-invariance screening for the economic/vocational and epistemic trust anxiety item sets will be attempted for gender, age group, education, and prior AI exposure if subgroup sample sizes are adequate. The epistemic pool will additionally screen media exposure, institutional trust, and political ideology or party identification when collected and powered. The default sequence is configural, metric, and scalar invariance for ordered categorical CFA or an IRT linking alternative. Metric and scalar invariance use the thresholds in `docs/psychometric_validation_protocol.md`: change in CFI no less than -0.010 and change in RMSEA no greater than 0.015 between nested levels. If scalar invariance or a documented linking alternative fails, group mean comparisons may be described as descriptive only and cannot be interpreted as comparable latent anxiety differences.

### External Validity Analyses

External validity analyses will use the independent confirmation sample as the primary sample. Development pilot analyses of the validation module may be used only for descriptive diagnostics and to identify implementation defects before confirmation outcomes are inspected.

Candidate ANX scores for external validity analyses will be computed only for item sets that first pass the preregistered dimensionality, reliability, IRT, DIF, and invariance screens at the level needed for a candidate construct score. If an item set fails those prior screens, external validity results may be reported descriptively but cannot rescue the item set for `approved_scored` status.

Convergent and discriminant analyses will report zero-order Pearson correlations, Spearman correlations, and model-based latent or factor-score associations where supported by the retained measurement model. The primary decision statistic will be specified in the validation dossier before external-validity estimates are inspected. Confidence intervals will use bootstrap or analytic methods appropriate to the statistic and weighting plan.

Criterion and incremental-validity analyses will model `ai_avoidance_intention_6m`, `ai_adoption_intention_6m`, and `ai_regulation_support_high_impact` as ordered outcomes unless diagnostics support treating them as approximately continuous for sensitivity analysis. Incremental models will compare a covariate-only model against a model adding the retained ANX score. The covariate-only model will include demographics, AI exposure variables, and `general_anxiety_2item_mean` as specified in H5. Missing validation comparators will be handled by complete-case analysis for the relevant model, with missingness counts reported for each variable and a sensitivity analysis using missing-indicator categories for non-score covariates when appropriate.

Behavioral criterion-validity analyses will model `revealed_anxiety_score` as a bounded continuous outcome from 0.00 to 1.00. The primary model is ordinary least squares with heteroskedasticity-robust standard errors, randomized-arm fixed effects, the retained standardized ANX score, and the H7 covariate block. This model is primary because the coefficient is directly interpretable as the adjusted change in the fraction of the $1.00 budget allocated to human review. Sensitivity models will include fractional logit or beta regression when supported by the observed distribution, and an ordinal robustness check using allocation deciles if endpoints at 0.00 or 1.00 are frequent. The primary exclusion rules for behavioral validity models remove respondents with invalid allocation totals, missing or unconfirmed allocation, failed behavioral comprehension, behavioral task technical failure, survey breakoff before task completion, survey-level preregistered exclusions, or `revealed_anxiety_score` missingness. Respondents excluded only from behavioral analyses remain available for ANX psychometric analyses when otherwise eligible.

External validity evidence is interpreted at the score level, not as a property of every single item. A validation dossier seeking `approved_scored` status must document convergent, discriminant, criterion, behavioral or revealed-preference criterion, and incremental-validity results in the structured `external_validity` evidence object required by `schema/validation_dossier.schema.json`.

### Retention Thresholds and Release Decisions

An item version may be recommended for continued development, revision, item-level-only approval, or future scored approval according to the following preregistered thresholds:

- Primary standardized loading at least 0.50 in the confirmation sample. Loadings from 0.40 to 0.49 require written construct-coverage justification and no stronger replacement item.
- No secondary loading greater than 0.30 and no secondary loading within 0.20 of the primary loading.
- Corrected item-total correlation at least 0.30 for the intended multi-item construct, excluding the item from the total.
- Confirmation sample item-level missing or unusable response no greater than 10 percent.
- Subgroup item-level missing or unusable response no greater than 15 percent for public comparison subgroups.
- No more than 70 percent of valid responses in the lowest or highest category.
- No more than 85 percent of valid responses in the two lowest or two highest adjacent categories unless the item is intentionally extreme-targeted and retains adequate IRT information.
- No statistically supported and practically meaningful DIF that remains unresolved for intended public comparisons.
- No local dependence large enough to make the item redundant with another retained item.
- Omega at least 0.70 for early scored construct use when an item set is proposed for construct scoring.
- External validity evidence satisfies the preregistered convergent, discriminant, criterion, and incremental-validity expectations for the score being proposed.
- At least one preregistered behavioral or revealed-preference criterion-validity test, including the Wave 1 `revealed_anxiety_score` test when available, satisfies its preregistered direction, exclusion rules, covariate adjustment, and pass threshold.

Passing these thresholds in this calibration wave is necessary but not sufficient for `approved_scored` status. Each item still requires a completed validation dossier, reviewer signoff, updated item metadata, and release manifest update before it can move from `development_only` or `exemplar` to `approved_scored`.

## Missing Data and Sensitivity Analyses

Primary item distribution analyses will use all eligible respondents with valid responses to the item being summarized. Factor analyses, reliability analyses, and IRT models will use pairwise or full-information methods appropriate for ordinal data when supported by the software, with complete-case sensitivity analyses reported. Item-level skipped responses will not be imputed for primary item outcomes.

Sensitivity analyses will evaluate:

- Weighted versus unweighted item distributions.
- Models with and without respondents flagged by non-exclusion QC checks.
- EFA results using alternative plausible factor extraction methods for polychoric input.
- CFA fit after removing items that fail distribution or DIF thresholds.
- DIF conclusions under alternative reference groups for age, gender, education, and prior AI exposure.

## Ethics and Respondent Protections

The survey presents hypothetical AI capability scenarios that may induce mild anxiety about employment, trust, relationships, autonomy, safety, identity, or ambient unease. The study will use informed consent, voluntary participation, the right to skip any item, a debrief explaining that scenarios are hypothetical and not personalized predictions, and contact information for study questions. The survey will not request employer names, patient information, child names, medical identifiers, government file identifiers, or other unnecessary direct identifiers.

The exact debrief and distress language is frozen in `docs/instruments/anx_us_2026w01_instrument.md`. The debrief will state that the study measures psychological responses to standardized AI scenarios for benchmark validation. It will clarify that no official aggregate ANX score is being assigned to participants or groups in Wave 1. The distress language will clarify that the scenarios are hypothetical, advise distressed respondents to pause or seek support, and provide US crisis support language including 988 for respondents who may need immediate mental health support.

## Reproducibility and Dossier Linkage

The final validation packet for this wave must archive:

- This preregistration file.
- The frozen fielding instrument at `docs/instruments/anx_us_2026w01_instrument.md`.
- The frozen Wave 1 codebook at `docs/instruments/anx_us_2026w01_codebook.md`.
- The exact administered item files and checksums.
- Fielding dates and vendor name.
- Sampling disposition and exclusion flow.
- Codebooks for raw and derived variables.
- Behavioral response schema-valid export and allocation scoring audit.
- Analysis scripts or notebooks.
- Weighted and unweighted descriptive tables.
- EFA, CFA, reliability, IRT, DIF, and invariance outputs.
- External validity outputs for the post-ANX validation module and behavioral allocation task, including expected and observed associations, confidence intervals, thresholds, exclusion counts, and reviewer decisions.
- Item-level retention table.
- One validation dossier per item or item set submitted for a release decision.

Validation dossiers for these item versions must cite this preregistration path. Item JSON metadata must not be updated to `approved_scored` unless the dossier path, preregistration path, psychometric decision, decision date, and scoring eligibility are updated consistently.
