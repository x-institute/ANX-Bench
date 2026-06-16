# ANX-Bench US 2026 Wave 5 Economic and Vocational Calibration Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w05_economic_calibration.md`
- Study label: `anx_us_2026w05_economic_calibration`
- Wave ID: `anx_us_2026w05_economic`
- Benchmark release line: `ANX-Bench v0.5.x`
- Fielding-ready packet release: `v0.5.0`
- Administered item directory: `items/v0.1/economic_vocational`
- Frozen fielding instrument: `docs/instruments/anx_us_2026w05_economic_instrument.md`
- Frozen codebook: `docs/instruments/anx_us_2026w05_economic_codebook.md`
- Frozen event registry: `events/v0.5/anx_us_2026w05_economic_event_registry.json`
- Authoritative machine-readable analysis contract: `analysis/v0.5/economic_vocational/wave5_analysis_plan.json`
- Analysis-plan schema: `schema/psychometric_analysis_plan.schema.json`
- Instrument freeze date: `2026-06-16`
- Planned development pilot fielding window: `FIELDING_START_DEVELOPMENT_PILOT` to `FIELDING_END_DEVELOPMENT_PILOT`
- Planned independent confirmation fielding window: `FIELDING_START_CONFIRMATION` to `FIELDING_END_CONFIRMATION`
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Primary validation purpose: psychometric calibration of the four-item `economic_vocational_anxiety` pool in the US adult population
- Scoring status at registration: no item in this wave is preregistered for official ANX-Bench scoring

This preregistration freezes a second-domain calibration packet for `economic_vocational_anxiety` before outcome data are inspected. The design mirrors the somatic and ambient calibration protocol: a development pilot of `N=500`, an independent confirmation sample of `N=1000`, ordinal EFA in the pilot, CFA in the confirmation sample, ordinal omega, graded-response IRT, DIF, measurement-invariance screening, item-retention thresholds, validation-dossier linkage, and claim-blocking conditions. The machine-readable JSON plan at `analysis/v0.5/economic_vocational/wave5_analysis_plan.json` is the authoritative analysis contract. If this prose document and the JSON plan disagree, the JSON plan governs unless a dated preregistration addendum is filed before outcome inspection.

This is a non-event calibration wave. The frozen event registry at `events/v0.5/anx_us_2026w05_economic_event_registry.json` has `registry_status: frozen`, `event_id: no_event`, and `outcome_inspection_status: not_inspected`. Every respondent-item row must therefore map `event_id` to `no_event`, and `event_exposure_window`, `baseline_or_followup`, and `fielding_time_relative_to_event_hours` must be null or absent according to `schema/wave_response.schema.json`. No exposure window, baseline window, follow-up window, or event-relative timing may be inferred after fielding. This rule blocks retrospective conversion of Wave 5 calibration into an event study.

## Administered Item Set

The following four item IDs are the only ANX-Bench items administered in this calibration packet. They are taken unchanged from `items/v0.1/economic_vocational/`, including scenario text, prompts, anchors, scoring keys, exclusions, and metadata.

| Domain | Item ID | Item version | File | Construct ID | Current release status |
| --- | --- | --- | --- | --- | --- |
| economic_vocational | `skill_obsolescence_software` | `v0.1.0` | `items/v0.1/economic_vocational/skill_obsolescence_software.json` | `economic_vocational_anxiety` | `development_only` |
| economic_vocational | `wage_pressure_customer_support` | `v0.1.0` | `items/v0.1/economic_vocational/wage_pressure_customer_support.json` | `economic_vocational_anxiety` | `development_only` |
| economic_vocational | `retraining_pressure_accounting` | `v0.1.0` | `items/v0.1/economic_vocational/retraining_pressure_accounting.json` | `economic_vocational_anxiety` | `development_only` |
| economic_vocational | `status_loss_creative_work` | `v0.1.0` | `items/v0.1/economic_vocational/status_loss_creative_work.json` | `economic_vocational_anxiety` | `development_only` |

All four items use the existing ordered 5-point anxiety response scale from the item JSON files. Item order will be randomized within the four-item economic and vocational block for both samples. Response options will always be displayed in ascending order from 1 to 5. No item wording, anchor, scoring key, metadata field, construct ID, or item version may be changed within this packet. Any modified wording requires a new item version and exclusion from the preregistered Wave 5 analyses.

The `job_displacement_radiology` exemplar in the same directory is not administered in this packet because its item JSON maps to `anticipated_job_displacement_anxiety`, not `economic_vocational_anxiety`.

## Population, Sampling Frame, and Samples

The target population is non-institutionalized US adults aged 18 years or older who can complete an English-language online survey without assistance and can provide informed consent. The intended inference population is the US adult population reachable through a professional online panel or probability-based panel with demographic, employment, occupation, and AI-exposure profiling sufficient for quota sampling and post-stratification.

Two non-overlapping samples are preregistered:

| Sample | Planned completed eligible analytic N | Role |
| --- | ---: | --- |
| Development pilot | 500 | Item distribution checks, missingness review, ordinal EFA, preliminary omega, early graded-response IRT diagnostics, cognitive debrief review, and item-retention recommendations before confirmation. |
| Independent confirmation sample | 1000 | CFA, final omega, graded-response IRT calibration, DIF, invariance screens, external-validity tests, and release-decision evidence. |

Pilot respondents are ineligible for the confirmation sample. Recruitment may over-sample only to offset expected exclusions and quota balancing. The vendor must provide controls or profile variables for age, gender, race and ethnicity, Census region, education, employment status, occupation group, prior AI exposure, AI-news exposure, current labor-force attachment, and occupational AI exposure.

## Quotas and Weighting

Both samples will use soft quotas to approximate the US adult population on age group, gender, race and ethnicity, education, Census region, employment status, occupation group, prior AI exposure, and AI-news exposure. Because this construct concerns labor-market threat, quota monitoring will also track current labor-force attachment and whether respondents work in, study for, or recently worked in software, customer support, accounting or finance, creative work, or adjacent occupations.

Post-stratification or raking weights will be generated separately for the development pilot and confirmation sample. Minimum weighting variables are age group, gender, race and ethnicity, education, Census region, and employment status. Prior AI exposure, AI-news exposure, broad occupation group, and labor-force attachment may be included when stable margins are available. Final weights will be trimmed to 0.30 through 3.00 unless a documented sensitivity analysis shows that a wider range is necessary and does not change primary conclusions.

Unweighted analyses are primary for EFA, CFA, omega, IRT, DIF, invariance, and external-validity pass-fail decisions unless the selected estimator has a validated survey-weight implementation. Weighted and unweighted descriptive item distributions will both be reported.

## Eligibility, Exclusions, and Quality Control

Eligibility criteria are age 18 or older, US residence, English self-administration, informed consent, non-duplicate participation, and no pilot participation for confirmation respondents.

Respondents are excluded before primary analyses if they fail the instructed-response attention check, fail the scenario-comprehension check, fail the economic-vocational attribution check, have completion time below one-third of the same-sample median after breakoffs are removed, give the same substantive response to all four ANX items and also fail an attention or minimum-reading-time check, miss or give non-substantive responses on more than 25 percent of administered ANX items, are confirmed duplicates, have unusable survey records, or self-report that they could not understand most scenarios.

The following flags do not automatically exclude by themselves: item-level response time below one-third of the sample median item time, long-string responding within the four-item block, high Mahalanobis distance, improbable IRT response pattern, vendor low-confidence flag not confirmed as fraud, open-text debrief confusion, open-text distress, unemployment, low income, career transition, high perceived occupational AI exposure, or high baseline general anxiety. These variables support sensitivity, DIF, ethics monitoring, or external-validity analysis.

Excluded records will be counted in a CONSORT-style flow table for each sample. Exclusion rates will be reported overall and by quota variables. Any subgroup with more than 15 percent excluded records will be flagged for sensitivity review.

## Outcomes and Validation Hypotheses

Primary outcomes are item-level response distributions for the four economic and vocational items. The candidate construct outcome is the retained `economic_vocational_anxiety` structure across software skill obsolescence, customer-support wage pressure, accounting retraining pressure, and creative-work status loss. No official item, construct, domain, overall, longitudinal, or event-study score will be computed from this calibration wave.

External-validity hypotheses are confirmatory only in the independent confirmation sample and only after dimensionality and reliability support a coherent retained item set with at least three retained items.

H1, convergent validity with perceived occupational AI exposure: retained economic and vocational anxiety scores will show a positive association with `perceived_occupational_ai_exposure`. The expected Spearman correlation is 0.15 to 0.45.

H2, discriminant validity from baseline general anxiety: retained scores will correlate positively but remain distinguishable from `baseline_general_anxiety_2item_mean`. A correlation above 0.70 blocks scored approval unless incremental AI-specific variance is demonstrated.

H3, labor-market worry specificity: retained scores will positively predict `ai_labor_market_worry_6m`, with an ordinal odds ratio of at least 1.20 per one standard deviation increase treated as practically meaningful.

H4, retraining criterion validity: retained scores will positively predict `ai_retraining_pressure_expectation_6m` after adjustment for demographics, employment status, occupation group, prior AI exposure, AI-news exposure, baseline general anxiety, and current labor-force attachment.

H5, domain-specific item evidence: each focal item should show its strongest adjusted association with its matching comparator where measured: software workers or technical training for `skill_obsolescence_software`, customer-support or service work for `wage_pressure_customer_support`, accounting or finance exposure for `retraining_pressure_accounting`, and creative-work exposure for `status_loss_creative_work`. A focal subgroup association cannot rescue an item with weak factor loading or unresolved DIF.

H6, incremental validity: retained scores will predict labor-market worry, retraining expectation, or AI-related career-planning avoidance after adjusting for age group, gender, education, region, employment status, occupation group, prior AI exposure, AI-news exposure, perceived occupational AI exposure, and baseline general anxiety. The default pass threshold is adjusted `R^2` change of at least 0.01 in linear sensitivity models or a standardized coefficient whose confidence interval excludes zero in ordinal or generalized models.

## Psychometric Analysis Plan

The development pilot will be used for item screening, ordinal EFA using polychoric correlations, preliminary omega, early IRT diagnostics, and implementation review. The confirmation sample will be used for CFA with ordered-categorical estimators, ordinal omega, graded-response IRT, DIF, measurement invariance, external validity, and release-decision evidence. Confirmation models may not be modified using confirmation outcomes and then treated as preregistered.

The expected structure is a one-factor `economic_vocational_anxiety` model with four related manifestations. A two-factor solution may be carried forward only if the pilot supports a substantively interpretable distinction, such as skill-value threat versus bargaining-power or status threat, and if at least three retained items remain available for any proposed scored construct. A four-item pool cannot support construct scoring if EFA implies four unrelated single items.

CFA strong fit support is defined as CFI at least 0.95, TLI at least 0.95, RMSEA at most 0.06, and SRMR at most 0.08. CFI or TLI from 0.90 to 0.949 or RMSEA from 0.061 to 0.080 requires written validation-dossier justification. Worse fit blocks construct scoring.

Ordinal omega is the primary reliability statistic. Omega must be at least 0.70 for early scored construct review and at least 0.80 for any later mature headline scoring review. Corrected item-total correlations must be at least 0.30 unless an item is retained for preregistered construct coverage with explicit reviewer justification.

The graded-response IRT model will report item discrimination, ordered thresholds, item information, test information, local dependence, and response-pattern fit. Disordered thresholds, discrimination below 0.65, negligible information, or local dependence of 0.20 or greater triggers revision, exclusion, or claim blocking according to the JSON plan.

DIF screening will cover age group, gender, race and ethnicity, education, Census region, employment status, occupation group, current labor-force attachment, prior AI exposure, AI-news exposure, perceived occupational AI exposure, baseline general anxiety, and device type when subgroup sample sizes permit. Ordinal logistic DIF will use Benjamini-Hochberg FDR at 0.05 within the four-item family. Practical DIF is defined as pseudo-R-squared change at least 0.02, expected score difference at least 0.10 standard deviations, or material rank-order impact. Invariance screens will use configural, metric, and scalar ordered-categorical CFA or a preregistered IRT linking alternative. Metric and scalar invariance require delta CFI no less than -0.010 and delta RMSEA no greater than 0.015.

## Retention Thresholds and Claim Blocking

Item versions may be recommended for continued development, revision, item-level-only approval, or future scored approval. Required gates include primary standardized loading at least 0.50, no secondary loading greater than 0.30, no secondary loading within 0.20 of the primary loading in a multi-factor model, corrected item-total correlation at least 0.30, confirmation item missingness no greater than 10 percent, public subgroup item missingness no greater than 15 percent, no more than 70 percent of valid responses in one category, no more than 85 percent in two adjacent categories unless extreme targeting is justified with adequate IRT information, no unresolved meaningful DIF, no severe local dependence, at least three retained items for construct scoring, omega at least 0.70, and supportive external-validity evidence.

Aggregate scoring is blocked until observed validation passes, a completed validation dossier is archived, reviewer signoff is recorded, item metadata are updated in a later release, and a later manifest explicitly lists official scored items. Passing Wave 5 thresholds is necessary but not sufficient for official ANX-Bench scoring.

## Ethics and Respondent Protections

The survey presents hypothetical employment, wages, retraining, skill-value, and occupational-status scenarios. It may induce mild concern about career security or economic change. The instrument uses informed consent, voluntary participation, the right to stop, no collection of employer names or identifiable workplace details, debrief language clarifying that scenarios are standardized research materials, and distress guidance. The survey is not employment advice, financial advice, legal advice, clinical assessment, or a prediction about any respondent's job.

## Reproducibility and Dossier Linkage

The final validation packet must archive this preregistration, the analysis plan, the frozen instrument, the frozen codebook, the no-event registry, item-file checksums, fielding dates, vendor name, sampling disposition, exclusion flow, codebooks for raw and derived variables, analysis scripts or notebooks, weighted and unweighted descriptive tables, EFA, CFA, omega, IRT, DIF, invariance, external-validity outputs, item-retention table, and a completed validation dossier for `economic_vocational_anxiety`.
