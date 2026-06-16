# ANX-Bench US 2026 Wave 7 Cross-Domain Bridge Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md`
- Study label: `anx_us_2026w07_cross_domain_bridge`
- Wave ID: `anx_us_2026w07_cross_domain_bridge`
- Benchmark release line: `ANX-Bench v0.7.x`
- Fielding-ready packet release: `v0.7.0`
- Frozen release manifest: `releases/v0.7.0/manifest.json`
- Frozen event registry: `events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json`
- Authoritative machine-readable analysis contract: `analysis/v0.7/cross_domain_bridge/wave7_analysis_plan.json`
- Instrument freeze date: `2026-06-16`
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Primary validation purpose: cross-domain linking evidence for later overall ANX readiness review
- Scoring status at registration: no new scored item, cross-domain score, domain score, or overall ANX score is preregistered or authorized by this packet

This preregistration freezes a non-event bridge study that co-administers the citable four-item `somatic_ambient_anxiety` item set with the frozen economic-vocational and epistemic candidate item pools in one independent sample. The study is designed to estimate whether the validated somatic construct, the economic candidate construct, and the epistemic candidate construct can be placed on a coherent cross-domain measurement map without erasing domain specificity. It is prerequisite evidence for later proposals of any domain-combined or overall ANX score, but it does not itself propose, score, publish, or validate such a score.

The bridge study has two distinct purposes. First, it tests whether the already citable somatic item set remains psychometrically stable when administered beside economic and epistemic items. Second, it estimates the latent correlations, IRT linking behavior, measurement invariance, and discriminant-validity boundaries needed before maintainers may even propose a combined cross-domain scoring model. Passing this preregistered bridge is necessary but not sufficient for overall ANX readiness. A later citable release would still need observed validation dossiers for each contributing construct, reviewer signoff, construct-registry updates, and an explicit scoring manifest.

The frozen event registry has `event_id: no_event`. Wave 7 is a bridge and calibration wave only. It cannot be retrospectively described as an event study, capability-shock study, baseline wave, follow-up wave, benchmark trend, model-release reaction, causal exposure design, or event-window analysis. Every respondent-item row must map `event_id` to `no_event`; `event_exposure_window`, `baseline_or_followup`, and `fielding_time_relative_to_event_hours` must be null or absent.

## Administered Item Set

The bridge packet co-administers the following ANX-Bench items without changing wording, response anchors, item versions, scoring keys, construct IDs, or quality-control metadata.

| Domain | Construct ID | Item ID | Item version | Current status in source release | Wave 7 role |
| --- | --- | --- | --- | --- | --- |
| somatic_ambient | `somatic_ambient_anxiety` | `sleep_disruption_ai_news` | `v0.2.0` | `approved_scored` in `v0.3.1` | Citable anchor construct, analyzed only for bridge evidence |
| somatic_ambient | `somatic_ambient_anxiety` | `body_vigilance_model_release` | `v0.2.0` | `approved_scored` in `v0.3.1` | Citable anchor construct, analyzed only for bridge evidence |
| somatic_ambient | `somatic_ambient_anxiety` | `background_dread_ai_progress` | `v0.2.0` | `approved_scored` in `v0.3.1` | Citable anchor construct, analyzed only for bridge evidence |
| somatic_ambient | `somatic_ambient_anxiety` | `avoidance_after_ai_capability_demo` | `v0.2.0` | `approved_scored` in `v0.3.1` | Citable anchor construct, analyzed only for bridge evidence |
| economic_vocational | `economic_vocational_anxiety` | `skill_obsolescence_software` | `v0.1.0` | `development_only` in `v0.5.0` | Frozen candidate construct |
| economic_vocational | `economic_vocational_anxiety` | `wage_pressure_customer_support` | `v0.1.0` | `development_only` in `v0.5.0` | Frozen candidate construct |
| economic_vocational | `economic_vocational_anxiety` | `retraining_pressure_accounting` | `v0.1.0` | `development_only` in `v0.5.0` | Frozen candidate construct |
| economic_vocational | `economic_vocational_anxiety` | `status_loss_creative_work` | `v0.1.0` | `development_only` in `v0.5.0` | Frozen candidate construct |
| epistemic | `epistemic_trust_anxiety` | `deepfake_evidence_trust` | `v0.1.0` | `development_only` in `v0.6.0` | Frozen candidate construct |
| epistemic | `epistemic_trust_anxiety` | `synthetic_news_provenance` | `v0.1.0` | `development_only` in `v0.6.0` | Frozen candidate construct |
| epistemic | `epistemic_trust_anxiety` | `ai_expert_claim_conflict` | `v0.1.0` | `development_only` in `v0.6.0` | Frozen candidate construct |
| epistemic | `epistemic_trust_anxiety` | `personalized_misinformation_targeting` | `v0.1.0` | `development_only` in `v0.6.0` | Frozen candidate construct |

The item blocks are randomized at the respondent level using a balanced block-order design with six possible domain-block orders. Items within each block are independently randomized. The standard 1 to 5 anxiety response anchors are used for all self-report items. The bridge packet may compute preregistered latent variables for analysis, but no participant, public report, release note, or manuscript may label those estimates as official ANX-Bench domain scores, cross-domain scores, or overall scores.

## Population, Sampling, and Power

The target population is non-institutionalized US adults age 18 or older who reside in the United States, can complete an English-language online survey without assistance, and provide informed consent. Recruitment may use a probability-based or high-quality professional online panel with profile variables sufficient for quota monitoring, weighting, duplicate detection, and subgroup analysis.

The target analytic sample is `N=1500` after exclusions. This sample size is chosen to support three correlated four-item ordinal factors, bifactor and second-order sensitivity models, graded-response IRT linking, and preregistered DIF and invariance tests across major demographic and AI-exposure groups. A minimum of `N=1200` eligible respondents is required for confirmatory bridge decisions. If the eligible sample is below `N=1200`, all cross-domain readiness decisions are automatically labeled underpowered and blocked.

Soft quotas monitor age group, gender, race and ethnicity, education, Census region, employment status, occupation group, prior AI exposure, AI-news exposure, and baseline general anxiety. Weights will be constructed for descriptive representativeness, but primary EFA, CFA, omega, IRT linking, DIF, invariance, and latent-correlation decisions are unweighted unless the estimator has a validated survey-weight implementation. Weighted and unweighted summaries must both be archived.

## Exclusions and Quality Control

Respondents are excluded from primary bridge analyses if they fail informed-consent eligibility, are under 18, reside outside the United States, cannot self-administer in English, are duplicates, are vendor-confirmed fraud, fail the instructed-response attention check, fail the cross-domain attribution check, fail a basic scenario-comprehension check, complete the survey in less than one-third of the same-sample median time after breakoffs are removed, miss more than 25 percent of administered ANX items, give the same substantive response to all 12 ANX items and also fail an attention or minimum-reading-time check, withdraw consent, or report that they understood only a few scenarios or did not understand the scenarios.

The following are sensitivity flags rather than automatic exclusions by themselves: high baseline general anxiety, high AI exposure, unemployment, occupational transition, low institutional trust, high news exposure, mobile completion, open-text confusion, open-text distress, and a single low item response time. Exclusion counts and exclusion rates must be reported overall and by age group, gender, race and ethnicity, education, region, occupation group, AI exposure, AI-news exposure, and baseline general anxiety.

## Confirmatory Psychometric Questions

Q1. Does a correlated three-factor model for `somatic_ambient_anxiety`, `economic_vocational_anxiety`, and `epistemic_trust_anxiety` fit the co-administered item responses better and more interpretably than a unidimensional overall ANX model?

Q2. Do all three domains show acceptable within-construct reliability in the bridge sample, with ordinal omega at least 0.70 for early readiness review and at least 0.80 for any mature headline-score consideration?

Q3. Are cross-domain latent correlations large enough to support a common ANX family, but not so large that the constructs collapse into one undifferentiated anxiety measure? The preregistered acceptable absolute latent-correlation band is 0.30 to 0.75 for each domain pair. A correlation below 0.30 blocks common-family readiness. A correlation above 0.75 blocks discriminant-validity support for simple aggregation.

Q4. Does IRT linking show that the somatic anchor and the two candidate domains can be placed on a stable cross-domain metric without substantial local dependence, threshold disordering, or anchor drift? The primary linking decision requires all retained items to have discrimination at least 0.65, zero threshold-ordering violations, residual local dependence below 0.20, anchor-drift absolute mean difference no greater than 0.20 SD, and linking standard error no greater than 0.15 theta units for the central 80 percent of the observed trait range.

Q5. Do DIF and measurement invariance results permit only cautious cross-domain comparison, or do they block combined-score proposals? Material DIF is defined as Benjamini-Hochberg FDR q below 0.05 plus pseudo-R-squared change at least 0.02, expected-score difference at least 0.10 SD, or material rank-order impact. Configural invariance must converge for each grouping variable. Metric and scalar or threshold invariance require delta CFI no less than -0.010 and delta RMSEA no greater than 0.015.

Q6. Does a bifactor or second-order model show enough general-factor saturation to justify later overall-score proposal? This packet requires omega hierarchical at least 0.50 and explained common variance at least 0.50 for readiness to propose an overall ANX model, while also requiring each domain's residual or specific factor to retain interpretable variance. If the general factor is weak, overall scoring is blocked. If specific factors collapse, domain-stratified scoring is blocked.

## Primary Decision Rules

The bridge packet has three possible decisions:

1. `blocked`: one or more core gates fail, including underpowered sample, unstable item functioning, failed correlated-factor fit, omega below 0.70 in any domain, latent correlations outside 0.30 to 0.75, material unresolved DIF, failed invariance for key comparisons, or unacceptable IRT linking.
2. `bridge_supported_domain_only`: domains show stable co-administration and interpretable correlations, but general-factor evidence is insufficient for an overall-score proposal.
3. `bridge_supported_for_overall_readiness_review`: all domain gates pass, cross-domain correlations remain in the preregistered band, IRT linking is stable, DIF and invariance risks are acceptable, and bifactor or second-order evidence meets the readiness threshold.

Even the strongest decision does not authorize scoring. It permits only a later, separately preregistered proposal for a citable cross-domain or overall ANX score. That later proposal must specify the scoring model, contributing constructs, weights, uncertainty reporting, missingness rules, subgroup-comparability limits, and release criteria before any official aggregate score is calculated or publicized.

## Claim Blocking

Wave 7 authorizes no item-level promotion, no new scored item, no economic score, no epistemic score, no cross-domain score, no domain-combined score, no overall ANX score, no event-study estimate, no longitudinal trend, no capability-shock claim, no clinical interpretation, no diagnostic use, no individual-level decision use, and no policy-decision ranking. The somatic items retain their source-release citable status outside this packet, but v0.7.0 itself is a frozen candidate bridge packet with `official_scored_items: []` and `aggregate_scoring_permitted: false`.

## Ethics and Reproducibility

The bridge survey presents standardized hypothetical scenarios about AI-related bodily unease, labor-market pressure, and information trust. The protocol uses informed consent, voluntary participation, the right to stop, no direct identifiers in analytic files, debrief language clarifying that scenarios are standardized research materials, and distress guidance.

The final bridge dossier must archive this preregistration, the machine-readable analysis plan, the no-event registry, the release manifest, item-file checksums, fielding dates, vendor disposition, exclusion flow, codebooks for raw and derived variables, analysis scripts or notebooks, weighted and unweighted descriptive tables, EFA, CFA, omega, IRT linking, DIF, invariance, cross-domain latent-correlation estimates, bifactor or second-order model outputs, sensitivity analyses, and a written release decision. Observed results must remain separated from the frozen candidate release until a later evidence-bound release is reviewed.
