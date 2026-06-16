# ANX-Bench

ANX-Bench is the Anthropogenic Nervousness Benchmark: a longitudinal, domain-stratified benchmark for measuring human psychological response to AI capabilities. It is designed as a standardized, repeatable, versioned research instrument rather than an ad hoc survey. The benchmark supports psychometric validation, pre-registration, event-study analysis around AI capability shocks, and comparisons across populations and waves.

The current citable somatic release line includes **ANX-Bench v0.3.2** for repeatability evidence and **ANX-Bench v0.3.1** for the source scored construct definition. Version `v0.3.2` is defined by the machine-readable release manifest at `releases/v0.3.2/manifest.json`, with the human-readable retest benchmark card at `docs/releases/v0.3.2_retest_benchmark_card.md` and observed retest evidence at `validation/v0.3/somatic_ambient_retest/wave3_retest_evidence.json`. It is a citable evidence release for 14-day repeatability only. It does not create new scored items, change item wording, alter score calculation, or authorize trend, event-study, causal-shock, overall ANX, cross-domain, or clinical claims. Version `v0.3.1` remains the source scored construct definition at `releases/v0.3.1/manifest.json` and `docs/releases/v0.3.1_benchmark_card.md`; it promotes the four retained somatic and ambient AI anxiety items to `approved_scored` status for the restricted `somatic_ambient_anxiety` construct mean after observed Wave 1 validation. Overall ANX scoring remains disabled: neither `v0.3.1` nor `v0.3.2` authorizes an overall ANX-Bench score, cross-domain score, clinical interpretation, translated administration, non-online administration, or IRT theta scoring. The frozen `v0.1.0` release remains immutable at `releases/v0.1.0/manifest.json` and is not reinterpreted by v0.3.2. Only manifests with top-level `release_status: citable` may support ANX-Bench benchmark claims, and only within the claim scope stated by that manifest and benchmark card; `draft`, `frozen_candidate`, and `deprecated` manifests may document reproducible artifacts but cannot authorize item-level, construct, domain, overall, longitudinal, or event-study benchmark claims.

`v0.3.0` is a preregistered provisional scoring candidate package with `release_status: frozen_candidate`, not a citable scored benchmark release. Its manifest freezes the somatic and ambient candidate item set, validation targets, scoring-note draft, analysis plan, and evidence-provenance contract before post-fielding validation. It has `official_scored_items: []` and `scoring_eligibility.aggregate_scoring_permitted: false`; no item-level, construct, domain, overall, longitudinal, or event-study ANX-Bench score may be cited from `v0.3.0` until a later non-future-dated validation dossier passes the scored-release promotion gate in `docs/releases/v0.3_to_v0.3.1_promotion_gate.md` and the later manifest is marked `release_status: citable`.

`v0.4.0` is the next somatic event-study candidate packet, not a citable scored release. Its manifest at `releases/v0.4.0/manifest.json` freezes a trigger-based preregistration, event registry template, event-wave instrument, and machine-readable analysis plan for the next qualifying major AI capability release. The packet reuses the v0.3.1 four-item `somatic_ambient_anxiety_mean` outcome, but keeps `official_scored_items: []` and `aggregate_scoring_permitted: false` for v0.4.0 itself. Version `v0.3.1` remains the only citable scored ANX-Bench release until the v0.4.0 event packet is completed with a locked qualifying event registry, observed evidence, validation checks, and a later citable evidence-bound manifest.

`v0.5.0` is the frozen economic-vocational calibration packet, not a citable scored release. Its manifest at `releases/v0.5.0/manifest.json` freezes the four development-only `economic_vocational_anxiety` items, Wave 5 preregistration, fielding instrument, codebook, no-event registry, psychometric analysis-plan schema reference, and machine-readable Wave 5 analysis plan. It keeps `official_scored_items: []` and `aggregate_scoring_permitted: false`; economic item-level, construct, domain, overall, longitudinal, and event-study scoring await observed validation, a completed validation dossier, reviewer approval, updated item metadata, and a later citable release.

`v0.7.0` is the required frozen cross-domain bridge packet before any overall ANX or cross-domain score can be proposed. Its manifest at `releases/v0.7.0/manifest.json` freezes a Wave 7 preregistration, sampling and weighting plan, no-event registry, and machine-readable analysis plan that co-administers the citable somatic item set with frozen economic and epistemic candidates in one independent sample. The sampling plan at `sampling/v0.7/anx_us_2026w07_cross_domain_bridge_sampling_plan.json` fixes `N=1500`, minimum eligible `N=1200`, the US English online adult target population, quota variables, exclusion flow, raking weights, 0.30 to 3.00 trim bounds, Taylor-linearization variance treatment, subgroup suppression rules, and blocked longitudinal, event-study, causal, clinical, and individual-level claims. The packet is intentionally non-scored: `official_scored_items: []`, `aggregate_scoring_permitted: false`, and no new scored items. A later overall ANX, domain-combined, or cross-domain score proposal is blocked unless Wave 7 or a successor bridge packet first provides preregistered evidence for factor structure, omega, IRT linking, DIF, invariance, and bounded cross-domain correlations.

## Benchmark Contract

Every ANX-Bench release is a fixed package of:

- A semantic benchmark version, such as `v0.1.0`.
- A JSON Schema for benchmark item records.
- A JSON Schema for the versioned construct registry.
- A JSON Schema for versioned wave response rows.
- A versioned construct registry defining domains, construct IDs, aggregation status, retained-item requirements, validation requirements, anchor status, and allowed item IDs.
- A versioned item directory containing all items admitted to that release.
- Methodology documentation specifying scoring, aggregation, longitudinal comparability, and release rules.
- A wave response data dictionary specifying response variables, allowed values, privacy rules, missingness codes, exclusion flags, event-study fields, and raw-to-scored response conversion.
- A preregistration protocol for longitudinal waves and event-study claims.
- A frozen sampling and weighting plan for every fielded wave, validating the target population, sampling frame, recruitment source, quotas, planned N, weight construction, variance design, subgroup cells, and claim limits before outcome inspection.
- A validated longitudinal linking and equating plan for every cross-release comparison, naming the source release, target release, anchor items, item-version continuity, bridge sample, linking model, invariance gates, drift thresholds, and permitted and blocked claims.
- A psychometric validation protocol defining the evidence required before items become benchmark-scored.
- A validation dossier pointer in every item file, linking the item version to its evidence record and preregistration status.

Items are not part of a benchmark-scored release until they validate against `schema/item.schema.json`, reference a construct ID registered in the applicable `constructs/` registry, appear in that construct's `allowed_item_ids`, satisfy the psychometric validation gate in `docs/psychometric_validation_protocol.md`, carry `release_status: approved_scored`, carry `validation.scoring_eligible: true`, and are placed under the appropriate versioned item directory. Fielded response data are not eligible to support validation, longitudinal, or event-study claims until the respondent-item response rows validate against `schema/wave_response.schema.json` and follow `docs/wave_data_dictionary.md`. Any longitudinal, trend, cross-release, or event-study comparison also requires a release-pair linking plan that validates against `schema/longitudinal_linking_plan.schema.json`, passes repository-reference checks with `tools/validate_longitudinal_linking_plan.py`, and cites observed linking evidence when item versions, anchor behavior, or measurement invariance are in question. Schema-valid items may exist as exemplars or development candidates, but schema validity alone does not mean an item is psychometrically validated, linked across releases, or eligible for official ANX-Bench scoring.

## Stable Directory Structure

```text
ANX-Bench/
  README.md
  doc/
    claude.md
  docs/
    instruments/
      anx_us_2026w01_codebook.md
      anx_us_2026w01_instrument.md
    methodology.md
    psychometric_validation_protocol.md
    preregistration_event_study.md
    preregistrations/
      README.md
      anx_us_2026w01_calibration.md
    validation_dossier_template.md
    wave_data_dictionary.md
  schema/
    construct_registry.schema.json
    item.schema.json
    release.schema.json
    wave_response.schema.json
  constructs/
    v0.1/
      registry.json
    v0.2/
      registry.json
  releases/
    v0.1.0/
      manifest.json
    v0.2.0/
      manifest.json
    v0.2.1/
      manifest.json
    v0.2.2/
      anx_us_2026w02_somatic_calibration_preregistration.md
      anx_us_2026w02_somatic_codebook.md
      anx_us_2026w02_somatic_instrument.md
      manifest.json
    v0.2.3/
      anx_us_2026w02_somatic_calibration_preregistration.md
      anx_us_2026w02_somatic_codebook.md
      anx_us_2026w02_somatic_instrument.md
      manifest.json
  items/
    v0.1/
      autonomy_surveillance/
        institutional_scoring_automation.json
      economic_vocational/
        job_displacement_radiology.json
        retraining_pressure_accounting.json
        skill_obsolescence_software.json
        status_loss_creative_work.json
        wage_pressure_customer_support.json
      epistemic/
        deepfake_evidence_trust.json
      existential_identity/
        creativity_status_displacement.json
      relational/
        child_companion_attachment.json
      safety_catastrophic/
        ai_enabled_systemic_harm.json
      somatic_ambient/
        ambient_bodily_unease.json
    v0.2/
      somatic_ambient/
        avoidance_after_ai_capability_demo.json
        background_dread_ai_progress.json
        body_vigilance_model_release.json
        sleep_disruption_ai_news.json
  validation/
    v0.2/
      somatic_ambient_anxiety/
        wave1_calibration_dossier.json
  events/
    v0.2/
      anx_us_2026w02_somatic_event_registry.json
```

Directory meanings:

- `schema/`: Machine-readable validation contracts for benchmark artifacts.
- `constructs/`: Versioned construct registries that define the authoritative domain and construct map for scoring, aggregation, anchor status, retained-item rules, validation requirements, and allowed item IDs.
- `releases/`: Machine-readable release manifests that define benchmark versions, frozen item sets, scoring eligibility, and reproducibility checksums.
- `items/`: Versioned benchmark items, grouped first by release line and then by domain.
- `docs/`: Methodology, scoring, aggregation, psychometric validation, longitudinal comparability rules, preregistration protocols, and frozen fielding instruments.
- `docs/instruments/`: Versioned participant-facing instrument packets and wave-specific codebooks. Every fielded wave must have a frozen instrument packet before recruitment begins, including consent language, instructions, item administration order rules, quality-control checks, debrief and distress language, non-ANX variable definitions, public-data exclusions, and mapping into `schema/wave_response.schema.json`.
- `doc/`: Project notes and conceptual background.

Future benchmark versions must preserve this structure. New releases may add directories, but they must not move, rename, or reinterpret existing released item files.

## Release Versioning

ANX-Bench uses semantic versioning for benchmark releases:

- `MAJOR`: Breaking changes to item semantics, score interpretation, core constructs, or aggregation rules.
- `MINOR`: Addition of validated domains, constructs, items, populations, or administration modes that preserve comparability with earlier releases.
- `PATCH`: Corrections that do not change item meaning, score calculation, or comparability.

The `items/v0.1/` directory is the item directory for the `0.1.x` release line, but a release is official only when a corresponding manifest exists under `releases/`. For `v0.1.0`, `releases/v0.1.0/manifest.json` is the canonical release definition: it lists the frozen item files, records the manifest-level release lifecycle state, records each item's release status and scoring eligibility, identifies the applicable schema and methodology documents, and stores SHA-256 checksums. Any future `v0.1.x` patch release must document the patch reason and show that existing item responses remain interpretable under the same scoring rules.

The `items/v0.2/` directory starts the `0.2.x` release line. Version `v0.2.0` adds a somatic and ambient anxiety development pool while preserving v0.1.0 immutability. It contains no official scored items, permits no aggregate scoring, and functions as a psychometric development release for planned calibration rather than as a validated scale release.

Version `v0.2.1` is a patch release that freezes the somatic and ambient calibration packet for fielding. It does not change item wording, item versions, scoring keys, construct definitions, or scoring eligibility. It adds a frozen packet manifest, the `anx_us_2026w02_somatic` fielding instrument and codebook, the somatic calibration preregistration, and a frozen `no_event` event registry so the wave cannot be retrospectively converted into an event study after outcomes are inspected.

Version `v0.2.2` is a patch release that preserves the same four frozen v0.2 somatic and ambient item files, the same development-only item status, empty `official_scored_items`, and `aggregate_scoring_permitted: false`. Its sole substantive packet addition is a fixed, non-scored response-scale anchoring vignette module for low, moderate, and high somatic and ambient AI-anxiety severity. The anchoring vignettes are calibration materials for response-style and comparability sensitivity analyses; they are not ANX-Bench items, do not create respondent-item rows, and do not authorize item-level, construct, domain, overall, longitudinal, or event-study scoring.

Version `v0.2.3` is a patch release. It preserves the v0.2.2 anchors, the same four frozen v0.2 somatic and ambient item files, the same development-only item status, empty `official_scored_items`, and `aggregate_scoring_permitted: false`. Its substantive addition is the non-scored `revealed_ai_review_allocation_v1` behavioral task and the canonical `schema/behavioral_response.schema.json` export contract. The task is criterion-validity infrastructure for testing whether candidate somatic and ambient AI anxiety responses predict a revealed preference for human review over AI-only review in high-impact decision scenarios. It is not an ANX-Bench item, does not create respondent-item rows, and does not authorize item-level, construct, domain, overall, longitudinal, or event-study scoring.

Version `v0.3.0` is a preregistered candidate package for possible future somatic and ambient scoring. It preserves the same four v0.2.0 somatic and ambient item files as development-only candidates, freezes the planned post-fielding calibration dossier targets, and records the evidence-provenance artifacts required for later scored approval. It is intentionally not a scored release: `official_scored_items` is empty, aggregate scoring is prohibited, and the candidate scoring note is not citable as validation evidence until observed fielding results pass the dossier and release validators in a later release.

Version `v0.3.1` is the source citable scored release for the somatic and ambient construct only. It records observed Wave 1 validation evidence in `validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json`, retains all four frozen v0.2.0 somatic and ambient item files as `approved_scored`, and permits the `somatic_ambient_anxiety` construct mean within the US English online adult administration scope documented in `docs/releases/v0.3.1_benchmark_card.md`. Overall ANX-Bench headline scoring, cross-domain scoring, clinical interpretation, translation claims, non-online administration claims, and IRT theta scoring remain disabled.

Version `v0.3.2` is the current repeatability-supported somatic release. It adds the checksum-bound observed 14-day retest evidence packet at `validation/v0.3/somatic_ambient_retest/wave3_retest_evidence.json`, governed by the preregistration at `docs/preregistrations/anx_us_2026w03_somatic_retest.md` and the frozen no-event registry at `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`. The retest administration remains frozen against `v0.3.1`; respondent-item rows use `benchmark_version: v0.3.1` with `event_id: no_event` and `baseline_or_followup: followup`. The v0.3.2 evidence packet passed the preregistered ICC(2,1), mean-change, item-stability, attrition, longitudinal-invariance, and panel-conditioning gates. The authorized claim is limited to 14-day repeatability evidence for `somatic_ambient_anxiety_mean` under the v0.3.1 US English online adult scope. The retest packet is repeatability and longitudinal measurement-quality evidence only; its `event_id: no_event` registry prohibits trend, event-study, causal-shock, event-window, overall ANX, cross-domain, and clinical claims from the retest wave itself.

Version `v0.4.0` is the next event-study candidate for the v0.3.1 somatic outcome. It adds `docs/preregistrations/anx_us_2026w04_somatic_event_study.md`, `events/v0.4/anx_us_2026w04_somatic_event_registry.template.json`, `docs/instruments/anx_us_2026w04_somatic_event_instrument.md`, and `analysis/v0.4/somatic_event_study/wave4_event_study_analysis_plan.json`. New event-study claims remain disabled until a qualifying event is independently classified, the registry is locked before outcome inspection with `event_locked_before_outcome_inspection: true`, baseline and follow-up fielding are completed, and observed evidence passes the preregistered thresholds. Until then, v0.3.1 remains the only citable scored release.

Version `v0.5.0` is the frozen economic-vocational calibration packet for Wave 5. It adds `docs/preregistrations/anx_us_2026w05_economic_calibration.md`, `docs/instruments/anx_us_2026w05_economic_instrument.md`, `docs/instruments/anx_us_2026w05_economic_codebook.md`, `events/v0.5/anx_us_2026w05_economic_event_registry.json`, `analysis/v0.5/economic_vocational/wave5_analysis_plan.json`, and `releases/v0.5.0/manifest.json`. The packet fixes the four economic item IDs, the `N=500` development pilot and `N=1000` independent confirmation split, exclusions, weighting rules, seeds, R package versions, EFA, CFA, omega, IRT, DIF, invariance thresholds, and validation-dossier output mappings before outcome inspection. It is intentionally non-scored: `official_scored_items` remains empty, aggregate scoring is prohibited, and economic scoring requires observed validation and a later citable release.

Version `v0.6.0` is the frozen non-scored epistemic calibration packet for Wave 6. It adds `releases/v0.6.0/manifest.json` and `validation/v0.6/epistemic_trust_anxiety/wave6_calibration_dossier.json` around the already frozen Wave 6 epistemic preregistration, instrument, codebook, no-event registry, construct registry, and analysis plan. The packet fixes the four `epistemic_trust_anxiety` item IDs, the planned `N=500` development pilot and `N=1000` independent confirmation split, the no-event status, and the preregistered EFA, CFA, omega, IRT, DIF, invariance, external-validity, behavioral-validity, and incremental-validity gates before outcome inspection. It is intentionally non-scored: `official_scored_items` is empty, aggregate scoring is prohibited, all four epistemic items remain `development_only` with `validation.scoring_eligible: false`, and any epistemic scoring requires observed validation, reviewer signoff, updated item metadata, and a later citable release. The release-blocking checklist for any later `v0.6.1` `epistemic_trust_anxiety_mean` scored promotion is `docs/releases/v0.6_to_v0.6.1_promotion_gate.md`.

Version `v0.7.0` is the frozen non-scored cross-domain bridge packet for Wave 7 and is a prerequisite before maintainers may propose any overall ANX score, cross-domain score, or domain-combined benchmark score. It adds `docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md`, `sampling/v0.7/anx_us_2026w07_cross_domain_bridge_sampling_plan.json`, `events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json`, `analysis/v0.7/cross_domain_bridge/wave7_analysis_plan.json`, and `releases/v0.7.0/manifest.json`. The packet co-administers the citable four-item `somatic_ambient_anxiety` source construct with the frozen four-item `economic_vocational_anxiety` and four-item `epistemic_trust_anxiety` candidate pools in one independent US English online sample. Its sampling plan freezes a nonprobability US English online adult bridge sample with `target_n: 1500`, `minimum_usable_n: 1200`, age, gender, race and ethnicity, education, Census region, employment, occupation, prior AI exposure, and AI-news exposure quota or monitoring variables, preregistered eligibility exclusions, raking to external adult margins where justified, 0.30 to 3.00 trim bounds, Taylor-linearization standard errors, and descriptive-only subgroup suppression rules. It freezes EFA, CFA, omega, IRT linking, DIF, invariance, bifactor or second-order readiness checks, and cross-domain latent-correlation thresholds before outcome inspection. It is intentionally non-scored: no new item is promoted, `official_scored_items` is empty, aggregate scoring is prohibited, and the locked `no_event` registry plus sampling claim limits block trend, event-study, causal-shock, event-window, longitudinal-change, clinical, diagnostic, and individual-level decision claims. Passing the bridge can only permit a later separately preregistered aggregate-score proposal; it does not authorize a combined score by itself.

Version `v0.8.0` is the frozen non-scored full-domain bridge packet for Wave 8. Its manifest at `releases/v0.8.0/manifest.json` and human-readable benchmark card at `docs/releases/v0.8.0_full_domain_bridge_benchmark_card.md` freeze 24 development-only items across `somatic_ambient`, `economic_vocational`, `epistemic`, `relational`, `existential_identity`, `autonomy_surveillance`, and `safety_catastrophic`. The packet exists to support preregistered full-domain bridge-readiness testing only. It has `official_scored_items: []`, `official_scored_item_count: 0`, and `aggregate_scoring_permitted: false`; it authorizes no scored items, domain scores, cross-domain score, overall ANX score, longitudinal trend, event-study estimate, causal capability-shock claim, clinical interpretation, individual-level use, or policy ranking. Promotion to a later citable bridge-readiness evidence release requires observed Wave 8 evidence, reviewer signoff, and the release-blocking checklist in `docs/releases/v0.8_to_v0.8.1_promotion_gate.md`.

## Release Reproducibility

Before publication, every future release must update its release manifest and all SHA-256 checksums for the item schema, methodology documents, preregistration protocol, psychometric validation protocol, sampling-plan schema, longitudinal-linking schema, every frozen sampling and weighting plan, every frozen linking plan, every frozen item file, and every versioned instrument packet used for fielded waves in that release. A release must not be cited, scored, or used for population, subgroup, longitudinal, trend, cross-release, or event-study comparison until the manifest validates against `schema/release.schema.json`, the applicable sampling plan validates against `schema/sampling_plan.schema.json`, any applicable release-pair linking plan validates against `schema/longitudinal_linking_plan.schema.json`, all repository references in the linking plan resolve, and all checksums match the published files.

Run the release-validation gate from the repository root before citing or publishing a release:

```bash
python3 tools/validate_sampling_plan.py sampling/v0.3/anx_us_2026w02_somatic_calibration_sampling_plan.json
python3 tools/validate_sampling_plan.py sampling/v0.3/anx_us_2026w03_somatic_retest_sampling_plan.json
python3 tools/validate_sampling_plan.py sampling/v0.7/anx_us_2026w07_cross_domain_bridge_sampling_plan.json
python3 tools/validate_content_validity_dossier.py validation/v0.7/cross_domain_bridge/content_validity_dossier.json
python3 tools/validate_cross_domain_bridge_evidence.py validation/v0.7/cross_domain_bridge/wave7_bridge_evidence.json
python3 tools/validate_full_domain_bridge_evidence.py validation/v0.8/full_domain_bridge/wave8_full_domain_bridge_evidence.json
python3 tools/validate_longitudinal_linking_plan.py linking/v0.8/anx_us_2026w08_full_domain_linking_plan.template.json
python3 tools/validate_validation_dossier.py validation/.../wave1_calibration_dossier.json
python3 tools/validate_release.py releases/v0.1.0/manifest.json
python3 tools/validate_release.py releases/v0.2.0/manifest.json
python3 tools/validate_release.py releases/v0.2.1/manifest.json
python3 tools/validate_release.py releases/v0.2.2/manifest.json
python3 tools/validate_release.py releases/v0.2.3/manifest.json
python3 tools/validate_release.py releases/v0.3.0/manifest.json
python3 tools/validate_release.py releases/v0.3.1/manifest.json
python3 tools/validate_release.py releases/v0.3.2/manifest.json
python3 tools/validate_analysis_plan.py analysis/v0.8/full_domain_bridge/wave8_analysis_plan.json --release releases/v0.8.0/manifest.json
python3 tools/validate_release.py releases/v0.6.0/manifest.json
python3 tools/validate_release.py releases/v0.7.0/manifest.json
```

A release is citable only after the relevant content-validity, validation dossier, and manifest gates pass, and only when the manifest itself has `release_status: citable`. The content-validity validator must run before psychometric or bridge promotion so reviewer independence, I-CVI, S-CVI/Ave, facet coverage, unresolved flags, and signoff are machine-checked before outcome evidence is considered. A candidate package can validate as a frozen preregistered artifact without becoming a scored benchmark release. For somatic and ambient `v0.3.0` promotion, maintainers must first follow `docs/releases/v0.3_to_v0.3.1_promotion_gate.md`, including validation of `validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json` and replacement of every placeholder zero hash with observed, checksum-bound evidence. For epistemic `v0.6.0` promotion, maintainers must first follow `docs/releases/v0.6_to_v0.6.1_promotion_gate.md`, including validation of `validation/v0.6/epistemic_trust_anxiety/observed_wave6_results.json`, `validation/v0.6/epistemic_trust_anxiety/wave6_calibration_dossier.json`, `validation/v0.6/epistemic_trust_anxiety/wave6_evidence_provenance.json`, `validation/v0.6/epistemic_trust_anxiety/wave6_evidence_manifest.json`, updated epistemic item files, and `releases/v0.6.1/manifest.json`. The psychometric dossier gate validates `schema/validation_dossier.schema.json` and enforces machine-checkable psychometric approval thresholds for approval dossiers. The release validator derives the release line from `benchmark_version`, checks the matching `constructs/<release_line>/registry.json`, validates every frozen item file against `schema/item.schema.json`, enforces construct registry membership and `allowed_item_ids`, verifies validation dossiers listed in checksums, checks scoring eligibility for `official_scored_items`, rejects future-dated `citable` manifests, rejects `frozen_candidate` manifests that contain scored items or enable aggregate scoring, rejects unplanned future-dated scored approval evidence, and recomputes SHA-256 checksums for release-defining files. For example, `v0.1.0` validates against `constructs/v0.1/registry.json`, while `v0.2.0` validates against `constructs/v0.2/registry.json` and preserves its no-scoring eligibility posture through an empty `official_scored_items` list and `aggregate_scoring_permitted: false`.

For full-domain bridge promotion from `v0.8.0` to `v0.8.1`, maintainers must use the frozen manifest at `releases/v0.8.0/manifest.json`, the benchmark card at `docs/releases/v0.8.0_full_domain_bridge_benchmark_card.md`, and the promotion gate at `docs/releases/v0.8_to_v0.8.1_promotion_gate.md`. The required release-blocking commands are:

```bash
python3 tools/validate_content_validity_dossier.py validation/v0.8/full_domain_bridge/content_validity_dossier.json
python3 tools/validate_full_domain_bridge_evidence.py validation/v0.8/full_domain_bridge/wave8_full_domain_bridge_evidence.json
python3 tools/validate_release.py releases/v0.8.1/manifest.json
```

`v0.3.2` repeatability claims have an additional release-blocking retest evidence gate. Before any benchmark-card statement about 14-day repeatability, validate the completed evidence packet with:

```bash
python3 tools/validate_retest_evidence.py validation/v0.3/somatic_ambient_retest/wave3_retest_evidence.json
```

The template at `validation/v0.3/somatic_ambient_retest/wave3_retest_evidence.template.json` is the preregistered structure and cannot authorize `v0.3.2` because its observed results and final decisions are null. The observed v0.3.2 packet replaces those nulls with checksum-bound estimates. This validator enforces exact `benchmark_version: v0.3.1`, the four approved somatic item IDs, `event_id: no_event`, non-future evidence dates, preregistered ICC(2,1), mean-change, item-stability, attrition, longitudinal-invariance, and panel-conditioning thresholds, plus threshold-derived pass, caution, or fail labels. A passing release manifest alone is not sufficient for any repeatability claim.

Wave packets have an additional packet-consistency gate. Before fielding, citing, or using a wave as validation evidence, run:

```bash
python3 tools/validate_wave_packet.py anx_us_2026w01
python3 tools/validate_wave_packet.py anx_us_2026w02_somatic --release v0.2.1
python3 tools/validate_wave_packet.py anx_us_2026w02_somatic --release v0.2.2
python3 tools/validate_wave_packet.py anx_us_2026w02_somatic --release v0.2.3
python3 tools/validate_wave_packet.py anx_us_2026w03_somatic_retest --release v0.3.1
python3 tools/validate_wave_packet.py anx_us_2026w06_epistemic --release v0.6.0
```

This gate checks that the frozen fielding instrument, wave codebook, calibration or retest preregistration, event registry when present, and release manifest agree on administered item IDs, item count, item versions, domains, construct IDs, release version, and non-event status. For `anx_us_2026w02_somatic`, the current gate validates the behavioral criterion-validity packet against `releases/v0.2.3/manifest.json` and requires the preregistration and codebook to cite `events/v0.2/anx_us_2026w02_somatic_event_registry.json` with `event_id: no_event`. For `anx_us_2026w03_somatic_retest`, the gate validates the test-retest packet against `releases/v0.3.1/manifest.json`, requires `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`, and preserves the retest as repeatability evidence for the existing citable score rather than as a new scored release. For `anx_us_2026w06_epistemic`, the gate validates the non-scored epistemic calibration packet against `releases/v0.6.0/manifest.json`, requires `events/v0.6/anx_us_2026w06_epistemic_event_registry.json`, and preserves Wave 6 as planned validation infrastructure rather than as a scored epistemic release.

The release manifest must also cover the applicable construct registry. Construct and domain aggregation must use the registry rather than ad hoc construct labels embedded in item JSON. Any future item must reference a registered construct ID and appear in that construct's `allowed_item_ids` before it can enter a frozen item set.

## Wave Scoring

Wave response files use one JSON object per respondent-item row and must validate against `schema/wave_response.schema.json`. Score a fielded wave from the repository root with:

```bash
python3 tools/score_wave.py path/to/wave_responses.jsonl releases/v0.1.0/manifest.json -o path/to/score_output.json
```

The scorer implements `docs/scoring_spec.md`. It validates every JSONL row, checks that the row `benchmark_version` and `item_version` match the release manifest, recomputes each observed item score from the released item `scoring.scoring_key`, enforces exclusion and missingness rules, and emits JSON that validates against `schema/score_output.schema.json`. Rows with non-observed missingness codes, exclusion flags, or items outside the manifest's official scoring gates are counted for auditability but do not contribute to estimates.

`v0.1.0` is scoreable only as a reproducibility no-aggregate release. Its manifest has `official_scored_items: []` and `scoring_eligibility.aggregate_scoring_permitted: false`, so valid development or exemplar response rows can be checked for row-level scoring reproducibility, but the canonical output must report `overall_score: null`, empty construct and domain score arrays, `official_scored_item_count: 0`, and `aggregate_scoring_permitted: false`.

## Required Item Validation

Every future item must validate against `schema/item.schema.json` before inclusion in a benchmark release. Schema validation is a release-blocking requirement, but it is only the first gate. Items that fail schema validation, lack a 5-point Likert response scale, omit scoring metadata, omit validation metadata, omit exclusion criteria, or lack interpretation bands cannot be included in the released benchmark item set.

Every item file must carry a machine-readable lifecycle status in `release_status` and a `validation` object recording the psychometric decision, decision date, validation dossier path, preregistration path, and scoring eligibility. Allowed lifecycle states are `exemplar`, `development_only`, `approved_item_level_only`, `approved_scored`, and `blocked`. The validation dossier should follow `docs/validation_dossier_template.md` and must document EFA, CFA, reliability, IRT, DIF, invariance, retention decision, and reviewer signoff before scored release.

Every item must also satisfy `docs/psychometric_validation_protocol.md` before it can move from exemplar or development status to benchmark-scored status. The protocol requires a development pilot, independent confirmation sample, refresh or bridge sample for revised items, EFA and CFA evidence, reliability targets, IRT calibration, DIF checks, measurement-invariance thresholds, and item retention rules. Items that are schema-valid but have not passed this gate are not psychometrically validated and must not contribute to official item-level, construct, domain, overall, longitudinal, or event-study scoring.

The next required validation artifact for the `items/v0.1` pool is the Wave 1 US calibration preregistration at `docs/preregistrations/anx_us_2026w01_calibration.md`. Before any `items/v0.1` item can move from `development_only` or `exemplar` to `approved_scored`, its validation dossier must cite this preregistration or a later applicable frozen preregistration, document the preregistered `N=500` development pilot and `N=1000` independent confirmation sample, and record a release decision consistent with the psychometric validation protocol. The Wave 1 calibration packet is validation infrastructure only; it does not authorize an official aggregate ANX score.

Only items with `release_status: approved_scored` and `validation.scoring_eligible: true` may enter construct, domain, or overall ANX scoring. Items marked `approved_item_level_only` may be reported only at the item level when their dossier and preregistration permit it; they must be excluded from aggregate ANX scores.

## v0.2 Somatic and Ambient Development Pool

Version `v0.2.0` promotes the somatic and ambient domain from anchor-only coverage to a multi-item construct candidate named `somatic_ambient_anxiety`. The pool contains four development-only items:

```text
items/v0.2/somatic_ambient/sleep_disruption_ai_news.json
items/v0.2/somatic_ambient/body_vigilance_model_release.json
items/v0.2/somatic_ambient/background_dread_ai_progress.json
items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json
```

These items sample related but non-identical manifestations of somatic and ambient anxiety: sleep disruption after AI capability news, bodily vigilance after a major model release, low background dread after cumulative AI progress, and avoidance after a credible AI capability demonstration. The construct registry at `constructs/v0.2/registry.json` defines `somatic_ambient_anxiety` as a `multi_item_construct_candidate`, requires at least three retained items before construct scoring can be considered, and lists only these four item IDs as allowed members.

The planned calibration dossier at `validation/v0.2/somatic_ambient_anxiety/wave1_calibration_dossier.json` mirrors the economic and epistemic development dossiers: it reserves EFA, CFA, reliability, IRT, DIF, invariance, item-retention, and reviewer-signoff evidence before any scored release decision. All four items remain `release_status: development_only` with `validation.scoring_eligible: false`. The v0.2.3 manifest freezes these files, the anchored and behavioral fielding packet, the codebook, the somatic calibration preregistration, the frozen no-event registry, the non-scored response-scale anchoring vignette file, `schema/behavioral_response.schema.json`, and their checksums, but `official_scored_items` remains empty and aggregate scoring remains prohibited.

## Initial Exemplar

The first exemplar item is:

```text
items/v0.1/economic_vocational/job_displacement_radiology.json
```

It measures anticipated AI-driven job displacement anxiety in radiology and demonstrates the minimum required structure for a fully specified ANX-Bench item.

## Candidate Multi-Item Construct Pool

The `items/v0.1/economic_vocational/` directory also contains the first candidate multi-item construct pool for the economic/vocational domain:

```text
items/v0.1/economic_vocational/skill_obsolescence_software.json
items/v0.1/economic_vocational/wage_pressure_customer_support.json
items/v0.1/economic_vocational/retraining_pressure_accounting.json
items/v0.1/economic_vocational/status_loss_creative_work.json
```

These development-only items sample related but non-identical facets of economic and vocational anxiety: core skill-value erosion, wage and bargaining-power pressure, forced retraining pressure, and occupational status or prestige loss. The pool is intended to support exploratory factor analysis, confirmatory factor analysis, reliability estimation, item retention decisions, and measurement-invariance checks under the psychometric validation protocol. Until that evidence is collected, reviewed, preregistered where applicable, and recorded in validation dossiers, these items remain non-scored development candidates with `release_status: development_only` and `validation.scoring_eligible: false`.

The Wave 5 calibration packet freezes this four-item pool for fielding under `v0.5.0`. The authoritative preregistered analysis contract is `analysis/v0.5/economic_vocational/wave5_analysis_plan.json`; it must be schema-valid against `schema/psychometric_analysis_plan.schema.json` and referenced by the Wave 5 preregistration before fielding. This freeze does not approve economic-vocational scoring. It only fixes the evidence-generation protocol needed for a later observed validation dossier and citable release decision.

## v0.1 Cross-Domain Anchor Pool

Version `v0.1.0` also includes a development-only cross-domain anchor pool. These six items add one anchor item for each top-level ANX-Bench domain not already represented by the economic/vocational exemplar and candidate pool:

```text
items/v0.1/epistemic/deepfake_evidence_trust.json
items/v0.1/relational/child_companion_attachment.json
items/v0.1/existential_identity/creativity_status_displacement.json
items/v0.1/autonomy_surveillance/institutional_scoring_automation.json
items/v0.1/safety_catastrophic/ai_enabled_systemic_harm.json
items/v0.1/somatic_ambient/ambient_bodily_unease.json
```

The anchor pool gives `v0.1.0` coverage across all seven top-level domains: economic/vocational, epistemic, relational, existential/identity, autonomy/surveillance, safety/catastrophic, and somatic/ambient. These anchors are concrete capability-linked development items covering deepfake evidence trust, child or companion attachment, human creativity and status, automated institutional scoring, AI-enabled physical or systemic harm, and ambient bodily unease after AI news exposure.

Only the economic/vocational domain currently has a multi-item construct pool suitable for psychometric scale-development work. The six cross-domain anchors are single-item domain coverage candidates, not validated construct scales. They remain non-scored development candidates with `release_status: development_only`, `validation.scoring_eligible: false`, and no role in official ANX-Bench aggregate, domain, construct, longitudinal, or event-study scoring until future validation dossiers and preregistered release decisions approve them.
