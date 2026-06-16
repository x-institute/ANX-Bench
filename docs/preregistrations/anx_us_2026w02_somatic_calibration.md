# ANX-Bench US 2026 Wave 2 Somatic Calibration Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w02_somatic_calibration.md`
- Study label: `anx_us_2026w02_somatic_calibration`
- Benchmark release line: `ANX-Bench v0.2.x`
- Fielding-ready packet release: `v0.2.1`
- Administered item directory: `items/v0.2/somatic_ambient`
- Frozen fielding instrument: `docs/instruments/anx_us_2026w02_somatic_instrument.md`
- Frozen codebook: `docs/instruments/anx_us_2026w02_somatic_codebook.md`
- Frozen event registry: `events/v0.2/anx_us_2026w02_somatic_event_registry.json`
- Authoritative machine-readable analysis contract: `analysis/v0.2/somatic_ambient/wave1_analysis_plan.json`
- Analysis-plan schema: `schema/psychometric_analysis_plan.schema.json`
- Instrument freeze date: `2026-06-15`
- Planned development pilot fielding window: `FIELDING_START_DEVELOPMENT_PILOT` to `FIELDING_END_DEVELOPMENT_PILOT`
- Planned independent confirmation fielding window: `FIELDING_START_CONFIRMATION` to `FIELDING_END_CONFIRMATION`
- Fielding rule for placeholders: final calendar dates must be inserted before respondent recruitment starts. If dates are changed after fielding begins, the change must be recorded as an addendum and cannot be justified by outcome data.
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Primary validation purpose: psychometric calibration of the four-item somatic and ambient AI anxiety development pool in the US adult population
- Scoring status at registration: no item in this wave is preregistered for official ANX-Bench scoring

This preregistration freezes the v0.2 somatic and ambient calibration design before outcome data are inspected. It is a development and confirmation plan for item retention and construct validation. The machine-readable JSON analysis plan at `analysis/v0.2/somatic_ambient/wave1_analysis_plan.json` is the authoritative preregistered analysis contract for required inputs, software and package versions, random seeds, sample splits, exclusions, weighting, missing-data handling, model specifications, validation gates, sensitivity analyses, and validation-dossier output fields. If this prose document and the JSON plan disagree, the JSON plan governs unless a dated preregistration addendum is filed before outcome inspection. This preregistration does not authorize official item-level, construct, domain, overall, longitudinal, or event-study scoring.

This is a non-event calibration wave. The frozen event registry for this packet is `events/v0.2/anx_us_2026w02_somatic_event_registry.json`, with `registry_status: frozen`, `event_id: no_event`, and `outcome_inspection_status: not_inspected`. The registry is cited here to preserve the event-study audit trail and to prevent retrospective assignment of an AI capability event after somatic calibration outcomes are observed. All respondent-item rows for this wave must therefore map `event_id` to `no_event`; no exposure window, baseline window, follow-up window, or event-relative timing may be inferred for confirmatory analyses.

The participant-facing survey flow is frozen in `docs/instruments/anx_us_2026w02_somatic_instrument.md`. The respondent-item schema mapping, item allowlist, QC variables, response-time variables, covariates, public-data exclusions, and restricted operations variables are frozen in `docs/instruments/anx_us_2026w02_somatic_codebook.md`.

## Administered Item Set

The following item IDs and versions are the only ANX-Bench items included in this calibration preregistration. Participant-facing scenario text, response prompts, anchors, scoring keys, exclusion notes, and item metadata are taken exactly from the listed JSON files as of the instrument freeze date.

| Domain | Item ID | Item version | File | Construct ID | Current release status |
| --- | --- | --- | --- | --- | --- |
| somatic_ambient | `sleep_disruption_ai_news` | `v0.2.0` | `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json` | `somatic_ambient_anxiety` | `development_only` |
| somatic_ambient | `body_vigilance_model_release` | `v0.2.0` | `items/v0.2/somatic_ambient/body_vigilance_model_release.json` | `somatic_ambient_anxiety` | `development_only` |
| somatic_ambient | `background_dread_ai_progress` | `v0.2.0` | `items/v0.2/somatic_ambient/background_dread_ai_progress.json` | `somatic_ambient_anxiety` | `development_only` |
| somatic_ambient | `avoidance_after_ai_capability_demo` | `v0.2.0` | `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json` | `somatic_ambient_anxiety` | `development_only` |

All four items use the same ordered 5-point anxiety response scale:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

Item order will be randomized within the four-item somatic and ambient block for the development pilot and independent confirmation sample. The response scale will always be displayed in ascending order from 1 to 5. No item wording, anchors, scoring key, or item metadata may be changed after this preregistration is frozen unless the modified item receives a new version and is excluded from the preregistered v0.2.1 packet analyses.

## Population, Sampling Frame, And Samples

The target population is non-institutionalized US adults aged 18 years or older who can complete an English-language online survey without assistance and can provide informed consent. The intended inference population is the US adult population reachable through a professional online survey panel or probability-based panel with demographic profiling sufficient for quota sampling and post-stratification.

The sampling frame will be a US adult online panel maintained by the contracted survey vendor. The vendor must provide panel-level controls or profile variables for age, gender, race and ethnicity, Census region, education, employment status, occupation group, prior AI exposure, and AI-news exposure. Panel members who participate in the development pilot are ineligible for the independent confirmation sample.

This preregistration includes two non-overlapping samples:

| Sample | Planned completed eligible analytic N | Role |
| --- | ---: | --- |
| Development pilot | 500 | Item distribution checks, missingness review, ordinal EFA, preliminary omega, early graded-response IRT diagnostics, cognitive debrief review, and item-retention recommendations before confirmation. |
| Independent confirmation sample | 1000 | CFA, final omega, graded-response IRT calibration, DIF, invariance screens, external-validity hypothesis tests, and release-decision evidence for the v0.2 somatic validation dossier. |

Recruitment will continue until the target number of eligible completes is reached after removing duplicate respondents, respondents outside eligibility criteria, respondents with unusable survey records, and respondents failing preregistered survey-level quality controls. Over-recruitment is permitted only to offset expected exclusions and quota balancing.

## Quotas And Weighting Variables

Both samples will use soft quotas to approximate the US adult population. The target marginal quota variables are age group, gender, race and ethnicity, education, Census region, employment status, prior AI exposure, and AI-news exposure during the past 30 days. AI-news exposure is included because the construct is explicitly tied to AI capability news and demonstrations, and severe imbalance could distort item distributions.

Post-stratification or raking weights will be generated separately for the development pilot and confirmation sample. The minimum weighting variables are age group, gender, race and ethnicity, education, Census region, and employment status. AI-news exposure and prior AI exposure will be included as calibration or trimming variables if stable margins are available or if sample imbalance threatens planned analyses. Weights will be trimmed so that no final weight is below 0.30 or above 3.00 unless a written sensitivity analysis shows that a wider range is necessary and does not change primary conclusions.

Unweighted analyses are primary for psychometric model estimation unless the method supports survey weights cleanly. Weighted descriptive item distributions will be reported as population-facing descriptive estimates. Sensitivity analyses will compare weighted and unweighted item distributions, factor loadings where feasible, and DIF conclusions.

## Eligibility, Exclusion Rules, And Quality Control

Eligibility criteria:

- Respondent is aged 18 or older.
- Respondent resides in the United States.
- Respondent can read and answer the English survey unaided.
- Respondent provides informed consent.
- Respondent is not a duplicate participant in the same sample.
- Respondent in the confirmation sample did not complete the development pilot.

Exclusion rules applied before primary analyses:

- Exclude respondents who fail the instructed-response attention check.
- Exclude respondents who fail the scenario-comprehension check.
- Exclude respondents who fail the somatic-attribution check, which verifies that the task was to rate anxiety linked to the AI scenario rather than report a current medical condition.
- Exclude respondents with a survey completion time less than one-third of the median completion time for the same sample after removing clear breakoffs.
- Exclude respondents who give the same substantive response to all four ANX-Bench items and also fail either the attention check or a minimum reading-time check.
- Exclude respondents with missing or non-substantive responses on more than 25 percent of administered ANX-Bench items.
- Exclude respondents with duplicate panel identifiers, duplicate survey tokens, or duplicate device fingerprints when vendor records indicate the same person submitted multiple completes.
- Exclude respondents who self-report that they could not understand most of the scenarios.

Quality control checks that do not automatically exclude by themselves:

- Item-level response time less than one-third of the sample median item time.
- Long-string responding within the four-item ANX block.
- Extremely high Mahalanobis distance or improbable response pattern under the fitted IRT model.
- Open-text debrief comments indicating confusion, satire, protest responding, or distress.
- Device, browser, and IP metadata patterns flagged by the vendor as low confidence but not confirmed duplicate or fraudulent.
- High baseline general anxiety, sleep sensitivity, or health anxiety sensitivity. These are analytic covariates and DIF or sensitivity variables, not automatic exclusion criteria.

Excluded records will be counted in a CONSORT-style flow table for each sample. Exclusion rates will be reported overall and by quota variables. If any subgroup has more than 15 percent excluded records, analyses involving that subgroup will be flagged for sensitivity review.

## Outcomes

Primary outcomes are item-level response distributions for the four somatic and ambient items. For each item and sample, the report will include the count and percentage in each response category, item mean and standard deviation reported only as descriptive summaries of ordered categories, median, interquartile range, item-level missingness, item response time distribution, floor concentration, ceiling concentration, and two-adjacent-category concentration.

The primary construct outcome is the candidate `somatic_ambient_anxiety` structure among:

- `sleep_disruption_ai_news`
- `body_vigilance_model_release`
- `background_dread_ai_progress`
- `avoidance_after_ai_capability_demo`

No official aggregate ANX score, domain score, construct score, benchmark ranking, longitudinal index, event-study outcome, or public headline score will be computed from this calibration wave. Any scale-like statistics produced during EFA, CFA, reliability, or IRT are validation evidence only and do not authorize scored benchmark use unless a later validation dossier and release decision approve the relevant item versions.

## External-Validity Hypotheses

External-validity hypotheses are confirmatory for validation-dossier review in the independent confirmation sample. Candidate somatic and ambient scores may be evaluated only if dimensionality and reliability support a coherent retained item set. If fewer than three items are retained, construct-score external validity is not interpreted as score validation.

H1, convergent validity with AI-news exposure: retained somatic and ambient anxiety scores will show a positive association with `ai_news_exposure_30d`. The expected zero-order Spearman correlation is 0.15 to 0.40. A null or negative association will require review of whether the items are measuring general distress detached from AI capability exposure.

H2, discriminant validity from baseline general anxiety: retained somatic and ambient anxiety scores will correlate positively but remain distinguishable from `baseline_general_anxiety_2item_mean`. The expected association is 0.15 to 0.45. A correlation above 0.70 will be treated as possible redundancy with general anxiety and blocks scored approval unless latent or incremental analyses demonstrate AI-specific variance.

H3, sleep-specific validity: `sleep_disruption_ai_news` will show a stronger association with `sleep_sensitivity_stress_news` than the other three items show, after adjusting for baseline general anxiety and AI-news exposure. This pattern supports subconstruct specificity without allowing the item to become a general sleep-problem proxy.

H4, bodily-vigilance validity: `body_vigilance_model_release` will show a stronger association with `health_anxiety_body_sensation_worry` than the other three items show, but the item must still load on the somatic and ambient AI anxiety factor. A strong health-anxiety association combined with weak factor loading will trigger revision or exclusion.

H5, criterion validity for avoidance: retained somatic and ambient anxiety scores will positively predict `ai_information_avoidance_intention_6m`. The expected association is positive and practically interpretable, with an ordinal odds ratio of at least 1.20 per one standard deviation increase in the candidate score treated as meaningful.

H6, incremental validity: retained somatic and ambient anxiety scores will predict AI information avoidance after adjusting for age group, gender, education, Census region, employment status, prior AI exposure, AI-news exposure, sleep sensitivity, health anxiety sensitivity, and baseline general anxiety. The default pass threshold is either a change in adjusted `R^2` of at least 0.01 for linear sensitivity models or a standardized candidate-score coefficient whose confidence interval excludes zero in ordinal or generalized models.

## Analysis Plan

All analyses will be conducted separately for the development pilot and independent confirmation sample unless explicitly stated otherwise. Analytic scripts must preserve the distinction between exploratory pilot outputs and confirmation outputs.

### Response Distributions And Item Screening

For each item, report response-category frequencies, weighted and unweighted percentages, missingness, completion time, floor and ceiling concentration, and two-adjacent-category concentration. Items are flagged for revision or exclusion if more than 70 percent of valid responses fall in the lowest or highest category, more than 85 percent fall in the two lowest or two highest adjacent categories, item-level missing or unusable response exceeds 10 percent in the confirmation sample, or item-level missing or unusable response exceeds 15 percent in any public comparison subgroup.

### Ordinal EFA

Exploratory factor analysis will use the `N=500` development pilot. EFA will be conducted on ordinal item responses using polychoric correlations. The extraction method will be minimum residual or weighted least squares factor analysis appropriate for polychoric input. Rotation will be oblique when more than one factor is extracted. The number of retained factors will be evaluated using parallel analysis, scree inspection, factor interpretability, factor determinacy where available, item loading strength, cross-loading patterns, and coverage of sleep disruption, bodily vigilance, background dread, and avoidance.

The expected structure is a one-factor somatic and ambient AI anxiety model with four related manifestations. A two-factor solution may be retained only if it is substantively interpretable before confirmation sample inspection, for example arousal and avoidance, and if at least three items remain usable for any proposed scored construct. A four-item pool cannot support scored construct approval if EFA implies four unrelated single items.

### CFA

Confirmatory factor analysis will use the non-overlapping `N=1000` independent confirmation sample. CFA will test the retained EFA structure using an estimator appropriate for ordered categorical data, such as WLSMV. Confirmation models may not be modified using confirmation sample outcome inspection and then treated as preregistered evidence.

Strong fit support is defined as CFI at least 0.95, TLI at least 0.95, RMSEA at most 0.06, and SRMR at most 0.08. Fit with CFI or TLI from 0.90 to 0.949 or RMSEA from 0.061 to 0.080 requires written justification in the validation dossier. Worse fit blocks approval for construct scoring from these item versions.

### Omega And Reliability

Ordinal coefficient omega is the preferred reliability statistic. Ordinal alpha will be reported as a secondary statistic for comparability. Reliability will be computed only for item sets with at least three retained items and a substantively interpretable common construct. The early benchmark-scored threshold is omega at least 0.70. Mature headline construct scoring would require omega at least 0.80, but headline scoring is not requested in this wave. Corrected item-total correlations must be at least 0.30 unless an item is retained for preregistered construct coverage with explicit reviewer justification.

### Graded-Response IRT

The confirmation sample will be used to fit a graded-response IRT model for the retained item set if dimensionality evidence supports a common trait. Models will report item discrimination parameters, ordered threshold parameters, item information, test information across the latent trait range, local dependence diagnostics, and person or response-pattern fit diagnostics. Disordered thresholds, very low discrimination, negligible information across the observed anxiety range, or severe local dependence will trigger a revise or exclude recommendation for the affected item version.

### DIF And Invariance

DIF screening in the confirmation sample is preregistered for:

- Age group: 18 to 29, 30 to 44, 45 to 59, 60 or older.
- Gender: woman, man, and nonbinary or another gender when subgroup sample size permits.
- Race and ethnicity categories listed in the quota plan when subgroup sample size permits.
- Education: no bachelor's degree versus bachelor's degree or higher, with finer categories reported descriptively where powered.
- Census region: Northeast, Midwest, South, West.
- Employment status: employed versus not employed.
- Prior AI exposure: never or rare use, monthly use, weekly use, daily or near-daily use.
- AI-news exposure during the past 30 days.
- Sleep sensitivity to stressful news or worries.
- Health anxiety sensitivity about ordinary body sensations.
- Baseline general anxiety.
- Survey device type: desktop or laptop versus mobile or tablet.

DIF will be evaluated using ordinal logistic regression and, when the retained IRT model is stable, multi-group IRT or MIMIC sensitivity models. Multiple testing will be controlled within the four-item family using Benjamini-Hochberg false discovery rate at 0.05. DIF is practically meaningful if pseudo-R-squared change is at least 0.02, expected score difference is at least 0.10 standard deviations for a focal group at the same latent trait level, or the item materially changes group rank ordering for the somatic and ambient construct.

Measurement-invariance screening will be attempted for gender, age group, education, prior AI exposure, AI-news exposure, sleep sensitivity, health anxiety sensitivity, and baseline general anxiety if subgroup sample sizes are adequate. The default sequence is configural, metric, and scalar invariance for ordered categorical CFA or an IRT linking alternative. Metric and scalar invariance use these thresholds: change in CFI no less than -0.010 and change in RMSEA no greater than 0.015 between nested levels. If scalar invariance or a documented linking alternative fails, group mean comparisons may be described as descriptive only and cannot be interpreted as comparable latent anxiety differences.

### External Validity Analyses

External validity analyses will use the independent confirmation sample as the primary sample. Development pilot analyses of the validation module may be used only for descriptive diagnostics and to identify implementation defects before confirmation outcomes are inspected.

Candidate scores for external validity analyses will be computed only for item sets that first pass the preregistered dimensionality, reliability, IRT, DIF, and invariance screens at the level needed for a candidate construct score. If the item set fails those prior screens, external validity results may be reported descriptively but cannot rescue the item set for `approved_scored` status.

Convergent and discriminant analyses will report Spearman correlations, polyserial correlations where appropriate, and model-based latent or factor-score associations where supported by the retained measurement model. Criterion and incremental-validity analyses will model `ai_information_avoidance_intention_6m` and `ai_information_checking_intention_6m` as ordered outcomes unless diagnostics support treating them as approximately continuous for sensitivity analysis. Missing validation comparators will be handled by complete-case analysis for the relevant model, with missingness counts reported for each variable and sensitivity analyses using missing-indicator categories for non-score covariates when appropriate.

## Retention Thresholds And Release Decisions

An item version may be recommended for continued development, revision, item-level-only approval, or future scored approval according to the following preregistered thresholds:

- Primary standardized loading at least 0.50 in the confirmation sample. Loadings from 0.40 to 0.49 require written construct-coverage justification and no stronger replacement item.
- No secondary loading greater than 0.30 and no secondary loading within 0.20 of the primary loading if a multi-factor model is retained.
- Corrected item-total correlation at least 0.30 for the intended multi-item construct, excluding the item from the total.
- Confirmation sample item-level missing or unusable response no greater than 10 percent.
- Subgroup item-level missing or unusable response no greater than 15 percent for public comparison subgroups.
- No more than 70 percent of valid responses in the lowest or highest category.
- No more than 85 percent of valid responses in the two lowest or two highest adjacent categories unless the item is intentionally extreme-targeted and retains adequate IRT information.
- No statistically supported and practically meaningful DIF that remains unresolved for intended public comparisons.
- No local dependence large enough to make the item redundant with another retained item.
- At least three retained items before construct-level scoring can be considered.
- Omega at least 0.70 for early scored construct use.
- External-validity evidence satisfies the preregistered convergent, discriminant, criterion, and incremental-validity expectations for the proposed score.

Passing these thresholds is necessary but not sufficient for `approved_scored` status. Each item still requires a completed validation dossier, reviewer signoff, updated item metadata, and release manifest update before it can move from `development_only` to `approved_scored`.

## Missing Data And Sensitivity Analyses

Primary item distribution analyses will use all eligible respondents with valid responses to the item being summarized. Factor analyses, reliability analyses, and IRT models will use pairwise or full-information methods appropriate for ordinal data when supported by the software, with complete-case sensitivity analyses reported. Item-level skipped responses will not be imputed for primary item outcomes.

Sensitivity analyses will evaluate:

- Weighted versus unweighted item distributions.
- Models with and without respondents flagged by non-exclusion QC checks.
- EFA results using alternative plausible factor extraction methods for polychoric input.
- CFA fit after removing items that fail distribution or DIF thresholds.
- DIF conclusions under alternative reference groups for age, gender, education, prior AI exposure, AI-news exposure, sleep sensitivity, health anxiety sensitivity, and baseline general anxiety.
- External-validity models with and without baseline general anxiety, sleep sensitivity, and health anxiety sensitivity covariates.

## Ethics And Respondent Protections

The survey presents hypothetical AI capability scenarios that may induce mild anxiety about future uncertainty, sleep disruption, bodily vigilance, background dread, or avoidance. The study will use informed consent, voluntary participation, the right to stop, a debrief explaining that scenarios are hypothetical and not personalized predictions, and contact information for study questions. The survey will not request clinical diagnoses, medication details, patient information, employer names, child names, medical identifiers, government file identifiers, or other unnecessary direct identifiers.

The exact debrief and distress language is frozen in `docs/instruments/anx_us_2026w02_somatic_instrument.md`. The debrief states that the study measures psychological responses to standardized AI scenarios for benchmark validation, that no official aggregate ANX score is being assigned to participants or groups, and that the questions are not a medical or mental health assessment. The distress language advises distressed respondents to pause, step away from AI-related news, talk with someone they trust, or contact a qualified mental health professional. It provides US emergency and 988 crisis support language.

## Reproducibility And Dossier Linkage

The final validation packet for this wave must archive:

- This preregistration file.
- The authoritative machine-readable analysis contract at `analysis/v0.2/somatic_ambient/wave1_analysis_plan.json` and its schema at `schema/psychometric_analysis_plan.schema.json`.
- The frozen fielding instrument at `docs/instruments/anx_us_2026w02_somatic_instrument.md`.
- The frozen codebook at `docs/instruments/anx_us_2026w02_somatic_codebook.md`.
- The exact administered item files and checksums.
- Fielding dates and vendor name.
- Sampling disposition and exclusion flow.
- Codebooks for raw and derived variables.
- Analysis scripts or notebooks.
- Weighted and unweighted descriptive tables.
- EFA, CFA, omega, graded-response IRT, DIF, and invariance outputs, with every planned statistic written to the target validation-dossier field specified in the JSON analysis plan.
- External-validity outputs including expected and observed associations, confidence intervals, thresholds, and reviewer decisions.
- Item-level retention table.
- A completed validation dossier for `somatic_ambient_anxiety`.

Validation dossiers for these item versions must cite this preregistration path. Item JSON metadata must not be updated to `approved_scored` unless the dossier path, preregistration path, psychometric decision, decision date, and scoring eligibility are updated consistently in a later release.
