# ANX-Bench US 2026 Wave 6 Epistemic Trust Calibration Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w06_epistemic_calibration.md`
- Study label: `anx_us_2026w06_epistemic_calibration`
- Wave ID: `anx_us_2026w06_epistemic`
- Benchmark release line: `ANX-Bench v0.6.x`
- Fielding-ready packet release: `v0.6.0`
- Administered item directory: `items/v0.1/epistemic`
- Frozen fielding instrument: `docs/instruments/anx_us_2026w06_epistemic_instrument.md`
- Frozen codebook: `docs/instruments/anx_us_2026w06_epistemic_codebook.md`
- Frozen event registry: `events/v0.6/anx_us_2026w06_epistemic_event_registry.json`
- Authoritative machine-readable analysis contract: `analysis/v0.6/epistemic_trust/wave6_analysis_plan.json`
- Instrument freeze date: `2026-06-16`
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Primary validation purpose: psychometric calibration of the four-item `epistemic_trust_anxiety` construct candidate
- Scoring status at registration: no item in this wave is preregistered for official ANX-Bench scoring

This preregistration freezes a non-event US English online calibration packet for `epistemic_trust_anxiety` before outcome inspection. The design uses a development pilot of `N=500` and an independent confirmation sample of `N=1000`. The development pilot supports item distribution review, ordinal EFA, preliminary omega, early IRT diagnostics, implementation checks, and retention recommendations. The confirmation sample supports preregistered CFA, ordinal omega, graded-response IRT, DIF, measurement invariance, external validity, behavioral criterion validity, incremental validity, and release-decision evidence.

The frozen event registry has `event_id: no_event`. Wave 6 cannot be retrospectively described as an event study, capability-shock study, baseline wave, follow-up wave, longitudinal trend wave, or event-window analysis. Every respondent-item row must map `event_id` to `no_event`; `event_exposure_window`, `baseline_or_followup`, and `fielding_time_relative_to_event_hours` must be null or absent.

## Administered Item Set

The four administered ANX-Bench items are frozen exactly as they appear in `items/v0.1/epistemic/`.

| Domain | Item ID | Item version | File | Construct ID | Current release status |
| --- | --- | --- | --- | --- | --- |
| epistemic | `deepfake_evidence_trust` | `v0.1.0` | `items/v0.1/epistemic/deepfake_evidence_trust.json` | `epistemic_trust_anxiety` | `development_only` |
| epistemic | `synthetic_news_provenance` | `v0.1.0` | `items/v0.1/epistemic/synthetic_news_provenance.json` | `epistemic_trust_anxiety` | `development_only` |
| epistemic | `ai_expert_claim_conflict` | `v0.1.0` | `items/v0.1/epistemic/ai_expert_claim_conflict.json` | `epistemic_trust_anxiety` | `development_only` |
| epistemic | `personalized_misinformation_targeting` | `v0.1.0` | `items/v0.1/epistemic/personalized_misinformation_targeting.json` | `epistemic_trust_anxiety` | `development_only` |

Item order is randomized within the four-item epistemic block using a respondent-level uniform random permutation. Response options remain in ascending order from 1 `Not at all anxious` to 5 `Extremely anxious`. No wording, response anchor, scoring key, construct ID, item version, or metadata field may be changed within this packet.

## Population, Sampling, and Weighting

The target population is non-institutionalized US adults age 18 or older who reside in the United States, can complete an English-language online survey without assistance, and provide informed consent. Recruitment may use a professional online panel or probability-based panel with profile variables sufficient for quota monitoring, weighting, duplicate detection, and subgroup analyses.

Soft quotas will monitor age group, gender, race and ethnicity, education, Census region, prior AI exposure, AI-news exposure, political information exposure, institutional trust, media literacy, and information-environment role. Post-stratification or raking weights will be constructed separately for the development and confirmation samples. Primary EFA, CFA, omega, IRT, DIF, invariance, criterion, behavioral, and incremental-validity pass-fail decisions are unweighted unless the estimator has a validated survey-weight implementation. Weighted and unweighted descriptive distributions must both be reported.

## Exclusions and Quality Control

Eligibility criteria are age 18 or older, US residence, English self-administration, informed consent, non-duplicate participation, and no development-pilot participation for confirmation respondents.

Respondents are excluded from primary analyses if they fail the instructed-response attention check, fail the scenario-comprehension check, fail the epistemic trust attribution check, complete the survey in less than one-third of the same-sample median time after breakoffs are removed, give the same substantive response to all four ANX items and also fail an attention or minimum-reading-time check, miss more than 25 percent of administered ANX items, are confirmed duplicates, have unusable survey records, withdraw consent, are protocol-ineligible, or report that they understood only a few scenarios or did not understand the scenarios.

The following are sensitivity flags rather than automatic exclusions by themselves: a single low item response time, vendor low-confidence flag not confirmed as fraud, high baseline general anxiety, high AI exposure, low institutional trust, high news exposure, political information intensity, mobile device use, open-text confusion, and open-text distress. Exclusion counts and exclusion rates must be reported overall and by preregistered DIF groups. Any subgroup exclusion rate above 15 percent triggers sensitivity review.

## DIF and Invariance Groups

DIF and invariance screening will cover age group, gender, race and ethnicity, education, Census region, prior AI exposure, AI-news exposure, self-rated AI familiarity, media literacy, institutional trust, political information exposure, information-environment role, baseline general anxiety, device type, and language-administration compliance. Subgroup models require adequate cell sizes; sparse categories may be collapsed using rules fixed before outcome inspection. Meaningful DIF blocks scored approval for affected items or subgroup comparison claims unless the validation dossier demonstrates immaterial expected-score impact.

## Psychometric Thresholds

The pilot EFA uses polychoric correlations with oblique rotation and parallel analysis. Items require primary loading at least 0.50, no secondary loading greater than 0.30, and no secondary loading within 0.20 of the primary loading in any retained multifactor solution. A one-factor solution is expected. A two-factor solution may be carried forward only if it is interpretable as evidence authenticity versus information manipulation and leaves at least three retained items for any proposed construct.

The confirmation CFA uses ordered-categorical WLSMV. Strong fit support requires CFI at least 0.95, TLI at least 0.95, RMSEA at most 0.06, SRMR at most 0.08, and minimum standardized loading at least 0.50. CFI or TLI from 0.90 to 0.949 or RMSEA from 0.061 to 0.080 requires a caution label and dossier justification. Fit worse than those caution ranges blocks construct scoring.

Ordinal omega is the primary reliability statistic. Omega must be at least 0.70 for early scored-construct review and at least 0.80 for any later mature headline review. Corrected item-total correlations must be at least 0.30. Confirmation item missingness must be no greater than 10 percent overall and no greater than 15 percent in public comparison subgroups. No single response category may contain more than 70 percent of valid responses, and no two adjacent categories may contain more than 85 percent unless IRT information supports intentional extreme targeting.

The graded-response IRT model must show minimum discrimination at least 0.65, zero threshold-ordering violations, useful item information in the observed trait range, and absolute residual local dependence below 0.20. DIF screening uses ordinal logistic DIF with Benjamini-Hochberg FDR 0.05 within the four-item family plus IRT DIF sensitivity where subgroup sizes permit. Practical DIF is pseudo-R-squared change at least 0.02, expected score difference at least 0.10 standard deviations, or material rank-order impact.

Measurement invariance uses configural, metric, and scalar or threshold tests in ordered-categorical CFA when estimable, with preregistered IRT linking fallback if CFA is unstable. Metric and scalar invariance require delta CFI no less than -0.010 and delta RMSEA no greater than 0.015. Failed scalar or threshold invariance blocks mean-comparison claims for affected groups.

## External, Behavioral, and Incremental Validity

External-validity hypotheses are confirmatory only in the independent confirmation sample and only after dimensionality and reliability support at least three retained items.

H1: retained scores will correlate positively with `perceived_ai_information_exposure`, expected Spearman correlation 0.15 to 0.45.

H2: retained scores will remain distinguishable from `baseline_general_anxiety_2item_mean`; a correlation above 0.70 blocks scored approval unless incremental AI-specific variance is demonstrated.

H3: retained scores will predict `ai_information_uncertainty_worry_6m`, with an ordinal odds ratio of at least 1.20 per one standard deviation increase treated as practically meaningful.

H4: retained scores will predict `ai_authenticity_verification_burden_6m` after adjustment for demographics, AI exposure, AI-news exposure, media literacy, institutional trust, baseline general anxiety, and information-environment role.

H5: retained scores will predict the non-scored behavioral criterion task `revealed_human_verification_allocation_v1`. The primary behavioral statistic is the number of 10 available credits allocated to additional human review rather than AI-only review. A practically meaningful association is a standardized coefficient whose confidence interval excludes zero or an adjusted incremental `R^2` change of at least 0.01 in linear sensitivity models.

H6: retained scores will add incremental validity for at least one preregistered criterion after adjusting for age group, gender, education, race and ethnicity, region, prior AI exposure, AI-news exposure, media literacy, institutional trust, political information exposure, baseline general anxiety, and information-environment role.

## Claim Blocking

Passing these thresholds is necessary but not sufficient for scoring. Wave 6 authorizes no item-level, construct, domain, overall, longitudinal, event-study, cross-domain, clinical, diagnostic, individual-level, or policy-decision claim. Aggregate scoring remains blocked until observed validation passes, a completed validation dossier is archived, reviewer signoff is recorded, item metadata are updated, and a later citable release manifest explicitly lists official scored epistemic items.

## Ethics and Reproducibility

The survey presents hypothetical evidence, news, expert-claim, and misinformation scenarios. It may induce mild concern about public information quality, elections, digital evidence, or institutional trust. The instrument uses informed consent, voluntary participation, the right to stop, no collection of direct identifiers or real allegations, debrief language clarifying that scenarios are fictional standardized research materials, and distress guidance.

The final validation packet must archive this preregistration, the machine-readable analysis plan, instrument, codebook, no-event registry, item-file checksums, fielding dates, vendor disposition, exclusion flow, codebooks for raw and derived variables, analysis scripts or notebooks, weighted and unweighted descriptive tables, EFA, CFA, omega, IRT, DIF, invariance, external-validity outputs, behavioral criterion outputs, incremental-validity models, item-retention table, and a completed validation dossier for `epistemic_trust_anxiety`.
