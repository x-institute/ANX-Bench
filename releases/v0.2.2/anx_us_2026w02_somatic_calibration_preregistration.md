# ANX-Bench US 2026 Wave 2 Somatic Calibration Preregistration v0.2.2

## Registration Metadata

- Preregistration file: `releases/v0.2.2/anx_us_2026w02_somatic_calibration_preregistration.md`
- Study label: `anx_us_2026w02_somatic_calibration`
- Benchmark release line: `ANX-Bench v0.2.x`
- Fielding-ready packet release: `v0.2.2`
- Administered item directory: `items/v0.2/somatic_ambient`
- Anchoring vignette set: `anchors/v0.2/somatic_ambient/response_scale_vignettes.json`
- Frozen fielding instrument: `releases/v0.2.2/anx_us_2026w02_somatic_instrument.md`
- Frozen codebook: `releases/v0.2.2/anx_us_2026w02_somatic_codebook.md`
- Frozen event registry: `events/v0.2/anx_us_2026w02_somatic_event_registry.json`
- Instrument freeze date: `2026-06-16`
- Planned development pilot fielding window: `FIELDING_START_DEVELOPMENT_PILOT` to `FIELDING_END_DEVELOPMENT_PILOT`
- Planned independent confirmation fielding window: `FIELDING_START_CONFIRMATION` to `FIELDING_END_CONFIRMATION`
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Primary validation purpose: psychometric calibration of the four-item somatic and ambient AI anxiety development pool in the US adult population, with response-scale anchoring vignettes for sensitivity analysis
- Scoring status at registration: no item in this wave, and no anchoring vignette, is preregistered for official ANX-Bench scoring

This preregistration freezes the v0.2.2 somatic and ambient calibration design before outcome data are inspected. It preserves the v0.2.1 ANX item pool and adds three fixed response-scale anchoring vignettes after the ANX item block and before covariates. The vignettes are calibration materials only. They do not authorize official item-level, construct, domain, overall, longitudinal, or event-study scoring.

This is a non-event calibration wave. The frozen event registry for this packet is `events/v0.2/anx_us_2026w02_somatic_event_registry.json`, with `registry_status: frozen`, `event_id: no_event`, and `outcome_inspection_status: not_inspected`. All respondent-item rows for this wave must map `event_id` to `no_event`; no exposure window, baseline window, follow-up window, or event-relative timing may be inferred for confirmatory analyses.

## Administered ANX Item Set

The following item IDs and versions are the only ANX-Bench items included in this calibration preregistration.

| Domain | Item ID | Item version | File | Construct ID | Current release status |
| --- | --- | --- | --- | --- | --- |
| somatic_ambient | `sleep_disruption_ai_news` | `v0.2.0` | `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json` | `somatic_ambient_anxiety` | `development_only` |
| somatic_ambient | `body_vigilance_model_release` | `v0.2.0` | `items/v0.2/somatic_ambient/body_vigilance_model_release.json` | `somatic_ambient_anxiety` | `development_only` |
| somatic_ambient | `background_dread_ai_progress` | `v0.2.0` | `items/v0.2/somatic_ambient/background_dread_ai_progress.json` | `somatic_ambient_anxiety` | `development_only` |
| somatic_ambient | `avoidance_after_ai_capability_demo` | `v0.2.0` | `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json` | `somatic_ambient_anxiety` | `development_only` |

Item order will be randomized within the four-item somatic and ambient block for the development pilot and independent confirmation sample. The response scale will always be displayed in ascending order from 1 to 5. No ANX item wording, anchors, scoring key, or item metadata may be changed after this preregistration is frozen unless the modified item receives a new version and is excluded from the preregistered v0.2.2 packet analyses.

## Anchoring Vignette Module

The v0.2.2 packet administers three fixed anchoring vignettes:

| Vignette ID | Intended severity band | File | Scored status |
| --- | --- | --- | --- |
| `anchor_somatic_ambient_low` | low | `anchors/v0.2/somatic_ambient/response_scale_vignettes.json` | non-scored |
| `anchor_somatic_ambient_moderate` | moderate | `anchors/v0.2/somatic_ambient/response_scale_vignettes.json` | non-scored |
| `anchor_somatic_ambient_high` | high | `anchors/v0.2/somatic_ambient/response_scale_vignettes.json` | non-scored |

The vignettes are administered in fixed low, moderate, high order immediately after the randomized ANX item block and before covariates. They use the same 5-point anxiety response scale as the ANX items. The expected ordering is low <= moderate <= high. A respondent may violate this expected order for many reasons, including response style, misunderstanding, inattentiveness, or sincere idiosyncratic interpretation. Therefore, `anchor_order_violation` is not an automatic exclusion criterion.

Anchoring vignette ratings are never ANX scored items. They must not be included in ANX item distributions, item-retention thresholds, reliability estimates, factor analyses, IRT calibration, candidate construct scores, official scores, event-study outcomes, or public benchmark headline values.

## Population, Sampling Frame, And Samples

The target population is non-institutionalized US adults aged 18 years or older who can complete an English-language online survey without assistance and can provide informed consent. The sampling frame will be a US adult online panel maintained by the contracted survey vendor. Panel members who participate in the development pilot are ineligible for the independent confirmation sample.

This preregistration includes two non-overlapping samples:

| Sample | Planned completed eligible analytic N | Role |
| --- | ---: | --- |
| Development pilot | 500 | Item distribution checks, missingness review, ordinal EFA, preliminary omega, early graded-response IRT diagnostics, cognitive debrief review, anchoring vignette distribution checks, and item-retention recommendations before confirmation. |
| Independent confirmation sample | 1000 | CFA, final omega, graded-response IRT calibration, DIF, invariance screens, external-validity hypothesis tests, anchoring sensitivity analyses, and release-decision evidence for the v0.2 somatic validation dossier. |

Recruitment will continue until the target number of eligible completes is reached after removing duplicate respondents, respondents outside eligibility criteria, respondents with unusable survey records, and respondents failing preregistered survey-level quality controls. Over-recruitment is permitted only to offset expected exclusions and quota balancing.

## Quotas And Weighting Variables

Both samples will use soft quotas to approximate the US adult population. Target marginal quota variables are age group, gender, race and ethnicity, education, Census region, employment status, prior AI exposure, and AI-news exposure during the past 30 days. Post-stratification or raking weights will be generated separately for the development pilot and confirmation sample. Unweighted analyses are primary for psychometric model estimation unless the method supports survey weights cleanly. Weighted descriptive item distributions will be reported as population-facing descriptive estimates.

## Eligibility, Exclusion Rules, And Quality Control

Eligibility criteria are age 18 or older, US residence, English self-administered completion, informed consent, no duplicate participation in the same sample, and no confirmation-sample participation after development-pilot completion.

Exclusion rules applied before primary analyses:

- Exclude respondents who fail the instructed-response attention check.
- Exclude respondents who fail the scenario-comprehension check.
- Exclude respondents who fail the somatic-attribution check.
- Exclude respondents with a survey completion time less than one-third of the median completion time for the same sample after removing clear breakoffs.
- Exclude respondents who give the same substantive response to all four ANX-Bench items and also fail either the attention check or a minimum reading-time check.
- Exclude respondents with missing or non-substantive responses on more than 25 percent of administered ANX-Bench items.
- Exclude respondents with duplicate panel identifiers, duplicate survey tokens, or duplicate device fingerprints when vendor records indicate the same person submitted multiple completes.
- Exclude respondents who self-report that they could not understand most of the scenarios.

Quality indicators that do not automatically exclude by themselves include item-level response time flags, long-string responding within the ANX block, improbable IRT response patterns, open-text debrief concerns, high baseline general anxiety, high sleep sensitivity, high health anxiety sensitivity, `anchor_order_violation`, and `anchor_response_style_stratum`.

## Outcomes

Primary outcomes are item-level response distributions for the four somatic and ambient ANX items. The primary construct outcome is the candidate `somatic_ambient_anxiety` structure across the four administered ANX items. No official aggregate ANX score, domain score, construct score, benchmark ranking, longitudinal index, event-study outcome, or public headline score will be computed from this calibration wave.

Anchoring outcomes are secondary calibration outputs:

- Raw response distributions for the low, moderate, and high anchoring vignettes.
- The proportion of respondents preserving the expected low <= moderate <= high order.
- The distribution of `anchor_response_style_stratum`.
- Subgroup differences in anchor response patterns by quota variables, AI exposure, sleep sensitivity, health anxiety sensitivity, baseline general anxiety, and device type.

## Psychometric Analysis Plan

The primary ANX item analysis plan remains: item response distributions and screening, ordinal EFA in the development pilot, CFA in the independent confirmation sample, ordinal omega, graded-response IRT where dimensionality supports it, DIF screening, measurement-invariance screening, external-validity analyses, and item-retention decisions. The expected structure is a one-factor somatic and ambient AI anxiety model with four related manifestations: sleep disruption, bodily vigilance, background dread, and avoidance.

DIF screening in the confirmation sample is preregistered for age group, gender, race and ethnicity, education, Census region, employment status, prior AI exposure, AI-news exposure, sleep sensitivity, health anxiety sensitivity, baseline general anxiety, survey device type, and anchor response-style stratum as a sensitivity variable. Anchor response-style stratum is not a primary grouping variable for release approval; it is used to assess whether DIF conclusions are sensitive to observed response-scale use.

Measurement-invariance screening will be attempted for gender, age group, education, prior AI exposure, AI-news exposure, sleep sensitivity, health anxiety sensitivity, and baseline general anxiety if subgroup sample sizes are adequate. Anchor variables may be used to interpret scalar non-invariance and to run sensitivity models, but they do not replace the primary invariance criteria.

## External-Validity Hypotheses

The v0.2.2 packet retains the v0.2.1 external-validity hypotheses: positive association with AI-news exposure, discriminant validity from baseline general anxiety, sleep-specific association for `sleep_disruption_ai_news`, bodily-vigilance association for `body_vigilance_model_release`, positive prediction of AI information avoidance, and incremental validity after demographic, AI exposure, sleep sensitivity, health anxiety sensitivity, and baseline general anxiety adjustment.

Anchor variables are not external-validity criteria. They may be included in sensitivity models to determine whether the external-validity conclusions remain similar after accounting for response-style strata.

## Anchoring Sensitivity Analyses

The validation dossier must include the following anchoring analyses before final release decisions:

- Descriptive distribution of each raw anchor rating, with weighted and unweighted percentages.
- Monotonicity check for low <= moderate <= high and the rate of `anchor_order_violation`.
- Distribution of `anchor_response_style_stratum`.
- Comparison of anchor distributions across preregistered DIF and invariance groups.
- DIF sensitivity models with and without `anchor_response_style_stratum`.
- Invariance sensitivity interpretation for any group where anchor response style is strongly imbalanced.
- Cross-wave comparability template showing how the fixed vignettes will be used if a later v0.2 or v0.3 wave repeats them unchanged.

Anchor sensitivity findings can qualify interpretation of ANX item results, but cannot by themselves approve an item for scoring, disqualify an item from scoring, or convert a calibration wave into an event-study outcome.

## Missing Data

Primary item distribution analyses will use all eligible respondents with valid responses to the item being summarized. Factor analyses, reliability analyses, and IRT models will use pairwise or full-information methods appropriate for ordinal data when supported by the software, with complete-case sensitivity analyses reported. Item-level skipped ANX responses will not be imputed for primary item outcomes.

Missing anchor ratings are summarized separately through `anchor_ratings_missing_count` and `anchor_response_style_stratum == incomplete`. Missing anchor ratings do not change `anx_items_missing_count`, `anx_items_missing_prop`, or ANX respondent-item missingness codes.

## Ethics And Respondent Protections

The survey presents hypothetical AI capability scenarios that may induce mild anxiety about future uncertainty, sleep disruption, bodily vigilance, background dread, or avoidance. The anchoring vignettes also contain hypothetical AI-related scenarios, but are designed to span low, moderate, and high intended severity for scale-use calibration. The study will use informed consent, voluntary participation, the right to stop, a debrief explaining that scenarios are hypothetical and not personalized predictions, and distress language appropriate for US online research.

The survey will not request clinical diagnoses, medication details, patient information, employer names, child names, medical identifiers, government file identifiers, or other unnecessary direct identifiers. The debrief states that no official aggregate ANX score is being assigned to participants or groups and that the questions are not a medical or mental health assessment.

## Reproducibility And Dossier Linkage

The final validation packet for this wave must archive this preregistration, the frozen v0.2.2 fielding instrument, the frozen v0.2.2 codebook, the exact administered item files and checksums, the anchoring vignette file and checksum, fielding dates and vendor name, sampling disposition and exclusion flow, codebooks for raw and derived variables, analysis scripts or notebooks, psychometric outputs, anchoring sensitivity outputs, external-validity outputs, item-level retention decisions, and a completed validation dossier for `somatic_ambient_anxiety`.
