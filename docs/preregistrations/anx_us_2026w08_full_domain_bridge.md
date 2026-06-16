# ANX-Bench US 2026 Wave 8 Full-Domain Bridge Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w08_full_domain_bridge.md`
- Study label: `anx_us_2026w08_full_domain_bridge`
- Wave ID: `anx_us_2026w08_full_domain_bridge`
- Benchmark release line: `ANX-Bench v0.8.x`
- Fielding-ready packet release: `v0.8.0`
- Frozen release manifest: `releases/v0.8.0/manifest.json`
- Frozen event registry: `events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json`
- Frozen sampling plan: `sampling/v0.8/anx_us_2026w08_full_domain_bridge_sampling_plan.json`
- Paired instrument: `docs/instruments/anx_us_2026w08_full_domain_bridge_instrument.md`
- Paired codebook: `docs/instruments/anx_us_2026w08_full_domain_bridge_codebook.md`
- Construct registry: `constructs/v0.8/registry.json`
- Instrument freeze date: `2026-06-16`
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Primary validation purpose: confirmatory full-domain bridge evidence across all seven ANX-Bench domains
- Scoring status at registration: no v0.8 item, domain score, cross-domain score, overall score, longitudinal trend, or event-study estimate is preregistered or authorized

This preregistration freezes a non-event confirmatory bridge wave that co-administers the current ANX-Bench domain item pools across all seven domains: somatic and ambient, economic and vocational, epistemic, relational, existential and identity, autonomy and surveillance, and safety and catastrophic. The wave is designed to test whether the full domain taxonomy can be administered in one standardized packet with interpretable domain structure, acceptable reliability, bounded cross-domain correlations, stable item functioning, and defensible invariance evidence. It is evidence for later readiness review only. It does not create any official scored item, domain score, cross-domain score, overall ANX score, event-study estimate, clinical interpretation, or policy ranking.

The frozen event registry for Wave 8 has `event_id: no_event`. Wave 8 is intentionally not anchored to a model release, viral incident, policy event, labor-market announcement, safety incident, or any other time-localized AI event. All retrospective event-study, capability-shock, before-after, event-window, trend, and causal exposure claims are blocked by design.

## Administered Item Set

| Domain | Construct ID | Item ID | Item version | Release status in v0.8.0 | Wave 8 role |
| --- | --- | --- | --- | --- | --- |
| somatic_ambient | somatic_ambient_anxiety | sleep_disruption_ai_news | v0.2.0 | source approved_scored anchor | Anchor evidence only |
| somatic_ambient | somatic_ambient_anxiety | body_vigilance_model_release | v0.2.0 | source approved_scored anchor | Anchor evidence only |
| somatic_ambient | somatic_ambient_anxiety | background_dread_ai_progress | v0.2.0 | source approved_scored anchor | Anchor evidence only |
| somatic_ambient | somatic_ambient_anxiety | avoidance_after_ai_capability_demo | v0.2.0 | source approved_scored anchor | Anchor evidence only |
| economic_vocational | economic_vocational_anxiety | skill_obsolescence_software | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| economic_vocational | economic_vocational_anxiety | wage_pressure_customer_support | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| economic_vocational | economic_vocational_anxiety | retraining_pressure_accounting | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| economic_vocational | economic_vocational_anxiety | status_loss_creative_work | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| epistemic | epistemic_trust_anxiety | deepfake_evidence_trust | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| epistemic | epistemic_trust_anxiety | synthetic_news_provenance | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| epistemic | epistemic_trust_anxiety | ai_expert_claim_conflict | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| epistemic | epistemic_trust_anxiety | personalized_misinformation_targeting | v0.1.0 | development_only candidate | Candidate bridge evidence only |
| relational | relational_ai_anxiety | partner_ai_confidant_displacement | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| relational | relational_ai_anxiety | friend_group_ai_mediation | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| relational | relational_ai_anxiety | eldercare_ai_attachment_shift | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| existential_identity | existential_identity_ai_anxiety | ai_personhood_boundary_uncertainty | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| existential_identity | existential_identity_ai_anxiety | human_judgment_status_loss | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| existential_identity | existential_identity_ai_anxiety | life_purpose_ai_substitution | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| autonomy_surveillance | autonomy_surveillance_ai_anxiety | public_space_tracking | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| autonomy_surveillance | autonomy_surveillance_ai_anxiety | workplace_behavior_scoring | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| autonomy_surveillance | autonomy_surveillance_ai_anxiety | personalized_behavior_nudging | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| safety_catastrophic | safety_catastrophic_ai_anxiety | autonomous_cyber_cascade | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| safety_catastrophic | safety_catastrophic_ai_anxiety | biosecurity_protocol_misuse | v0.8.0 | development_only candidate | Candidate bridge evidence only |
| safety_catastrophic | safety_catastrophic_ai_anxiety | military_escalation_ai_advice | v0.8.0 | development_only candidate | Candidate bridge evidence only |

All items use the ordered 1 to 5 anxiety response scale: 1 Not at all anxious, 2 Slightly anxious, 3 Moderately anxious, 4 Very anxious, 5 Extremely anxious. The somatic items retain their prior source-release status only outside this packet. In Wave 8 they are bridge anchors and are not re-promoted, rescored, or expanded into any official aggregate.

## Population, Sampling, and Power

The target population is non-institutionalized US adults age 18 or older who reside in the United States, can complete an English-language online survey without assistance, and provide informed consent. Recruitment may use a high-quality professional online panel or probability-based panel with profile fields sufficient for quota monitoring, duplicate review, exclusion auditing, and weighting.

The target eligible analytic sample is `N=2500` after preregistered exclusions. The minimum usable eligible sample is `N=2000`. If fewer than `N=2000` respondents remain after exclusions, all confirmatory full-domain bridge decisions are automatically labeled underpowered and blocked. The target is chosen to support seven correlated ordinal factors, split-sample EFA and CFA, ordinal omega, graded-response IRT, item-level DIF, multi-group invariance tests, and sparse-domain sensitivity checks for the three-item v0.8 domains.

Primary split: randomly assign the eligible analytic sample before outcome inspection into an EFA calibration half and a CFA confirmation half, stratified by sample source, device category, and domain-block order. The EFA half is used only to inspect dimensionality, salient cross-loadings, residual dependence, threshold behavior, and candidate item retention. The CFA half is used for preregistered bridge decisions. Full-sample estimates may be reported as descriptive robustness checks only after the split-sample decisions are archived.

## Exclusions and Quality Control

Respondents are excluded from primary analyses if they decline or withdraw consent, are under age 18, reside outside the United States, cannot complete the survey in English unaided, are confirmed duplicates, are vendor-confirmed fraud, fail the instructed-response attention check, fail the scenario-comprehension check, fail the full-domain attribution check, complete the survey in less than one-third of the same-sample median time after breakoffs are removed, miss more than 25 percent of administered ANX items, straightline all administered ANX items and also fail an attention or minimum-reading-time check, report that they understood only a few scenarios or did not understand the scenarios, or encounter a platform error that prevents reliable item-order reconstruction.

Sensitivity flags that do not by themselves exclude a respondent are high recent general anxiety, high AI-news exposure, high prior AI use, prior AI companion use, cybersecurity or infrastructure employment, caregiving role, urbanicity, relationship status, occupational transition, mobile completion, one low item response time, straightlining within a single domain block, open-text confusion, and open-text distress. Exclusion counts must be reported overall and by age group, gender, race and ethnicity, education, Census region, employment status, occupation group, prior AI exposure, AI-news exposure, device type, sample source, and domain-block order.

## Confirmatory Psychometric Gates

1. EFA gate: the calibration half must support an interpretable seven-domain solution. Each retained item must have primary loading at least 0.40 on its intended factor, no cross-loading at or above 0.30 unless the cross-loading is theoretically documented and below the primary loading by at least 0.20, no Heywood case, no unordered response thresholds, and no residual local dependence above 0.20 after accounting for the domain factor. Failure of the EFA gate blocks all full-domain scoring claims.

2. CFA gate: the confirmation half must fit a correlated seven-factor ordinal CFA better than a unidimensional model and better than any collapsed-domain model that merges distinct theoretical domains. Preregistered adequacy requires CFI at least 0.950, TLI at least 0.940, RMSEA no greater than 0.060 with upper 90 percent CI no greater than 0.080, SRMR no greater than 0.080, all standardized intended loadings at least 0.50 unless a single three-item candidate domain has one loading between 0.40 and 0.50 with a documented retention rationale, and no absolute residual correlation above 0.20 within or across domains.

3. Omega gate: ordinal omega total must be at least 0.70 for every candidate domain to support continued bridge interpretation and at least 0.80 for any future mature headline-score consideration. Omega hierarchical and explained common variance for any proposed general ANX factor must each be at least 0.50 before a later overall-score proposal may even be drafted. Wave 8 itself authorizes no such score.

4. IRT gate: graded-response models must show monotonic category thresholds, discrimination at least 0.65 for retained items, no material local dependence, stable item information across the central 80 percent of the observed trait range, and linking standard error no greater than 0.15 theta units for domain comparisons used in bridge evidence. Somatic anchor drift relative to its source scoring context must be no greater than 0.20 SD on average and no single somatic item may show drift greater than 0.30 SD without blocking source-anchor use in Wave 8 bridge claims.

5. DIF gate: item-level DIF is screened by age group, gender, race and ethnicity, education, Census region, employment status, occupation group, prior AI exposure, AI-news exposure, device type, and sample source. Material DIF is defined as Benjamini-Hochberg FDR q below 0.05 plus at least one practical-impact criterion: pseudo-R-squared change at least 0.02, expected-score difference at least 0.10 SD, threshold shift with visible category-probability impact in the central trait range, or material rank-order impact. Unresolved material DIF blocks subgroup comparison for the affected item or domain and may block the full-domain bridge if it affects domain interpretation.

6. Invariance gate: configural invariance must converge for all prespecified grouping variables with sufficient cell sizes. Metric and scalar or threshold invariance require delta CFI no less than -0.010 and delta RMSEA no greater than 0.015 relative to the less constrained model. Partial invariance may support descriptive bridge evidence only when noninvariant parameters are identified before outcome-based interpretation and do not alter domain ordering or substantive conclusions. Failed invariance blocks benchmark subgroup comparison and any future aggregate-score claim spanning the affected group.

7. Cross-domain gate: latent correlations among domains must be positive, theoretically coherent, and bounded. The preregistered acceptable absolute correlation band for continued common-family interpretation is 0.20 to 0.80. A correlation below 0.20 blocks claims that the pair belongs to a common ANX family without further evidence. A correlation above 0.80 blocks simple aggregation and suggests construct collapse or method dominance.

## Decision Rules

The Wave 8 bridge decision must be one of four labels: `blocked_underpowered`, `blocked_psychometric`, `bridge_supported_domain_only`, or `bridge_supported_for_later_aggregate_readiness_review`. Passing every gate permits only a later, separately preregistered proposal for scoring. That later proposal must define retained items, weights, uncertainty, missingness handling, subgroup comparability limits, external validity evidence, release criteria, and disclosure controls before any official aggregate score is calculated.

## Blocked Scoring and Claims

Wave 8 blocks all official scored-item promotion, all new domain scores, all seven-domain aggregate scores, all overall ANX scores, all longitudinal trend claims, all baseline or follow-up claims, all event-study estimates, all capability-shock claims, all causal claims, all clinical or diagnostic uses, all individual-level decisions, all policy-decision rankings, and all claims that v0.8.0 is nationally representative without the sampling limitations in the frozen sampling plan. Public reporting may describe item distributions, psychometric diagnostics, and bridge-readiness decisions only when accompanied by this preregistration, the codebook, the sampling plan, the no-event registry, weighting diagnostics, and disclosure review.

## Ethics and Reproducibility

The survey uses standardized hypothetical scenarios about AI-related bodily unease, work, information trust, relationships, identity, autonomy, surveillance, safety, and catastrophic risk. It does not ask respondents to disclose names, employers, intimate histories, credentials, incident details, illegal conduct, health records, or direct identifiers. The instrument includes informed consent, the right to stop, attention and comprehension checks, debrief language, distress language, and public-data restrictions.

The final Wave 8 dossier must archive this preregistration, the instrument, codebook, sampling plan, no-event registry, construct registry, release manifest, item-file checksums, fielding dates, vendor disposition, exclusion flow, code and package versions, weighted and unweighted descriptive tables, EFA, CFA, omega, IRT, DIF, invariance, latent-correlation, sensitivity analyses, disclosure-review decisions, and a written release decision. Observed results must remain separate from the frozen candidate release until a later evidence-bound citable release is reviewed.
