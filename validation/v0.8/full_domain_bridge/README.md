# v0.8.1 Full-Domain Bridge Evidence Bundle

This directory is the canonical location for the observed Wave 8 evidence bundle that can promote the frozen `v0.8.0` full-domain bridge packet to a citable `v0.8.1` evidence release. The bundle is evidence for seven-domain bridge readiness only. It does not authorize a new scored item, domain score, seven-domain aggregate score, overall ANX score, trend claim, event-study estimate, causal claim, individual-level use, clinical interpretation, or policy-decision ranking.

## Scope

The observed bundle is limited to:

- `study_id: anx_us_2026w08_full_domain_bridge`
- `wave_id: anx_us_2026w08_full_domain_bridge`
- `benchmark_version: v0.8.0`
- `promotion_target_version: v0.8.1`
- `event_id: no_event`
- the 24 frozen Wave 8 item IDs and item versions in `releases/v0.8.0/manifest.json`
- the preregistration at `docs/preregistrations/anx_us_2026w08_full_domain_bridge.md`
- the sampling plan at `sampling/v0.8/anx_us_2026w08_full_domain_bridge_sampling_plan.json`
- the no-event registry at `events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json`

Every observed artifact must be generated after the preregistration, event registry, sampling plan, item files, schema dependencies, construct registry, and manifest inputs are frozen. Outcome inspection begins when any analyst, maintainer, or reviewer sees respondent-level ANX outcomes, item distributions, split-sample EFA or CFA results, reliability estimates, IRT diagnostics, DIF flags, invariance diagnostics, latent correlations, somatic-anchor drift, or aggregate-readiness outputs. The evidence bundle must record that timestamp and confirm that no threshold, exclusion rule, item-retention rule, scoring rule, or claim boundary changed after that point.

## Allowed Files

Only these observed evidence filenames are allowed for the `v0.8.1` full-domain bridge bundle:

```text
validation/v0.8/full_domain_bridge/observed_wave8_results.json
validation/v0.8/full_domain_bridge/content_validity_dossier.json
validation/v0.8/full_domain_bridge/wave8_full_domain_bridge_evidence.json
validation/v0.8/full_domain_bridge/wave8_evidence_provenance.json
validation/v0.8/full_domain_bridge/wave8_evidence_manifest.json
releases/v0.8.1/manifest.json
```

The matching preregistered templates currently supplied by this directory are:

```text
validation/v0.8/full_domain_bridge/observed_wave8_results.template.json
validation/v0.8/full_domain_bridge/content_validity_dossier.template.json
validation/v0.8/full_domain_bridge/wave8_full_domain_bridge_evidence.template.json
validation/v0.8/full_domain_bridge/wave8_evidence_provenance.template.json
validation/v0.8/full_domain_bridge/wave8_evidence_manifest.template.json
```

`observed_wave8_results.template.json` is the frozen observed-results ledger structure for the `v0.8.0` Wave 8 packet. It fixes the no-event classification, 24-item allowlist, item versions, source paths, respondent-flow fields, split-assignment metadata, item-distribution shells, model-output pointers, sensitivity-summary fields, claim limits, and signoff roles. It must be copied to `observed_wave8_results.json` only after observed fielding, split assignment, outcome-inspection timing, model outputs, and reviewer signoff can be populated. The template itself is schema-valid but cannot pass the observed ledger validator because `result_status` remains `template_pending_observed_data`.

`content_validity_dossier.template.json` is only the frozen content-validity review blueprint. It must be copied to `content_validity_dossier.json` only after at least three independent expert reviewers have completed ratings for relevance, clarity, facet fit, and ethical acceptability; all item-level unresolved flags have been adjudicated; and the reviewer panel, CVI values, revision decisions, promotion eligibility fields, and signoff fields have been populated from the completed review record.

`wave8_full_domain_bridge_evidence.template.json` is the frozen bridge-evidence decision structure. It must be copied to `wave8_full_domain_bridge_evidence.json` only after the observed ledger and completed content-validity dossier pass, all preregistered psychometric gates have observed values, and every scoring authorization field remains false.

`wave8_evidence_provenance.template.json` is the frozen statistic-level provenance structure using `schema/evidence_provenance.schema.json`. It includes planned placeholder records for sample and exclusions, split assignment, EFA, CFA, omega, IRT, DIF, invariance, latent correlations, somatic-anchor drift, and the final bridge decision. It must be copied to `wave8_evidence_provenance.json` only after every gate has restricted input hashes, split-file hashes, script or notebook hashes, output hashes, analyst signoff, reviewer signoff, and outcome-inspection timing.

`wave8_evidence_manifest.template.json` is the frozen reproducibility manifest using `schema/psychometric_evidence_manifest.schema.json`. It binds each planned statistic to restricted data hashes, split-file hash, analysis script or notebook hash, software/session lock, output artifact hash, analyst placeholder, reviewer signoff requirement, and reproduction command. Its zero-filled hashes and placeholder values must be replaced before the manifest can be treated as observed evidence.

`wave8_bridge_dossier.json`, `full_domain_results.json`, and `overall_anx_validation.json` are not allowed names. The canonical observed results ledger is `observed_wave8_results.json`, and it must pass before any content-validity or bridge-evidence validation:

```bash
python3 tools/validate_full_domain_observed_results.py validation/v0.8/full_domain_bridge/observed_wave8_results.json
```

The canonical observed bridge evidence artifact is `wave8_full_domain_bridge_evidence.json`, and it must pass after the observed ledger and content-validity dossier pass:

```bash
python3 tools/validate_full_domain_bridge_evidence.py validation/v0.8/full_domain_bridge/wave8_full_domain_bridge_evidence.json
```

Wave 8 bridge evidence is non-citable until this validator passes on the observed `wave8_full_domain_bridge_evidence.json` file. The template is a preregistered structure only; it cannot support bridge-readiness, scoring, trend, event-study, clinical, or policy claims.

## Artifact Roles

`observed_wave8_results.json` records respondent flow, input checksums, outcome-inspection timing, item-level distributions, split assignment, model outputs, sensitivity checks, and analyst and reviewer signoff needed to reproduce the bridge decisions. It is the observed-result ledger and should not contain release language beyond bounded bridge diagnostics.

`content_validity_dossier.json` records independent expert review of seven-domain content coverage, item-domain assignment, construct representation, unresolved flags, and claim boundaries before psychometric evidence is used. It must be created from `content_validity_dossier.template.json` only after completed expert ratings are available, not as an empty or partially rated copy.

`wave8_full_domain_bridge_evidence.json` is the machine-validated decision artifact. It maps observed results to the preregistered Wave 8 gates for analytic `N`, exclusions, split-sample EFA and CFA, seven-domain gates, omega, IRT, DIF, invariance, latent correlations, somatic-anchor drift, aggregate readiness, scoring authorization, and final decision. It must keep every scoring authorization field false.

`wave8_evidence_provenance.json` binds each statistic to the restricted data artifact, covariate file, fielding disposition file, split file, analysis script or notebook, generated output, checksum, analyst, reviewer, and outcome-inspection timing.

`wave8_evidence_manifest.json` is the reproducibility index for the bundle. It lists every release-relevant artifact, its SHA-256 checksum, its role, the command or procedure that produced it, and the signoff status required before `releases/v0.8.1/manifest.json` can checksum the completed bundle.

`releases/v0.8.1/manifest.json` is the release manifest. It can be created only after the observed files above are complete, reviewed, and checksum-bound.

## Required Signoff Roles

The bundle must record distinct roles, even when an organization assigns more than one person to a role:

- Fielding custodian: confirms sample source, eligibility rules, no-event administration, fielding windows, restricted data hashes, item-order reconstruction, and respondent disposition counts.
- Data custodian: confirms public-data exclusions, restricted identifiers, linkage hashes, split assignment file, disclosure review, and checksum stability.
- Analysis lead: runs the preregistered analysis without changing thresholds after outcome inspection and records software, package, seed, and output checksums.
- Psychometric reviewer: verifies split-sample EFA and CFA, omega, IRT, DIF, invariance, latent-correlation, somatic-anchor drift, and aggregate-readiness results against the preregistered gates.
- Content-validity reviewer: confirms seven-domain coverage and unresolved content flags before bridge promotion language is drafted.
- Release reviewer: confirms checksum completeness, allowed filenames, no scoring authorization, claim limits, and consistency with the `v0.8.1` promotion scope.

Analyst signoff alone is insufficient. Reviewer signoff must explicitly state whether outcome inspection occurred before or after each rule, threshold, and claim-boundary decision was locked.

## Promotion Order

Promotion to a citable `v0.8.1` bridge-evidence release must proceed in this order:

1. Freeze `v0.8.0` source inputs, including the manifest, preregistration, no-event registry, sampling plan, construct registry, schema dependencies, and 24 item files.
2. Complete fielding under `event_id: no_event`, preserving the preregistered administration, fixed domain sequence, within-block randomization, and exclusion rules.
3. Assign the eligible analytic sample to EFA and CFA splits before outcome inspection, stratified by sample source, device category, and domain-block order.
4. Populate `observed_wave8_results.json` from restricted respondent-item data, fielding disposition data, covariate data, split assignment, and preregistered analysis outputs.
5. Populate `wave8_evidence_provenance.json` and `wave8_evidence_manifest.json` with nonzero SHA-256 checksums for every restricted input, script, software lock, generated output, signoff record, and public evidence artifact.
6. Complete and validate `content_validity_dossier.json`.
7. Populate and validate `wave8_full_domain_bridge_evidence.json`.
8. Create `releases/v0.8.1/manifest.json` only after the observed evidence files are complete and checksum-stable.
9. Validate the release manifest.
10. Publish only full-domain bridge-evidence claims. Any aggregate-score proposal must be separately preregistered after this gate and must keep Wave 8 scoring unauthorized until a later scored-release gate passes.

Required commands from the repository root:

```bash
python3 tools/validate_full_domain_observed_results.py validation/v0.8/full_domain_bridge/observed_wave8_results.json
python3 tools/validate_content_validity_dossier.py validation/v0.8/full_domain_bridge/content_validity_dossier.json
python3 tools/validate_full_domain_bridge_evidence.py validation/v0.8/full_domain_bridge/wave8_full_domain_bridge_evidence.json
python3 tools/validate_release.py releases/v0.8.1/manifest.json
```

## Blocked Claims for v0.8.1

Even if every gate passes, `v0.8.1` may state only that observed Wave 8 evidence supports a bounded full-domain bridge-readiness decision under the preregistered US English online adult scope. It must not state or imply:

- any official scored-item promotion
- any new domain score
- any seven-domain aggregate score
- any overall ANX score
- any longitudinal trend, baseline, follow-up, event-study, event-window, capability-shock, or causal estimate
- any clinical, diagnostic, individual-level, employment, insurance, education, or policy-decision use
- any nationally representative claim beyond the limitations in the frozen sampling plan
- any subgroup comparison where DIF or invariance gates block interpretation
- any source-anchor claim when somatic-anchor drift fails
