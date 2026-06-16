# v0.7.1 Cross-Domain Bridge Evidence Bundle

This directory is the canonical location for the observed Wave 7 evidence bundle that can promote the frozen `v0.7.0` cross-domain bridge packet to a citable `v0.7.1` bridge-evidence release. The bundle is evidence for bridge readiness only. It does not authorize an overall ANX score, a cross-domain score, a domain-combined score, trend claims, event-study claims, individual-level use, clinical interpretation, or policy-decision ranking.

## Scope

The observed bundle is limited to:

- `study_id: anx_us_2026w07_cross_domain_bridge`
- `wave_id: anx_us_2026w07_cross_domain_bridge`
- `benchmark_version: v0.7.0`
- `promotion_target_version: v0.7.1`
- `event_id: no_event`
- the 12 frozen Wave 7 item IDs and item versions in `releases/v0.7.0/manifest.json`
- the preregistered analysis plan at `analysis/v0.7/cross_domain_bridge/wave7_analysis_plan.json`
- the no-event registry at `events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json`

Every observed artifact must be generated after the analysis plan, event registry, item files, schema dependencies, and manifest inputs are frozen. Outcome inspection begins only when the first analyst or reviewer sees respondent-level outcomes, item distributions, factor results, reliability estimates, IRT diagnostics, DIF flags, invariance diagnostics, latent correlations, or general-factor readiness outputs. The evidence bundle must record that timestamp and confirm that no threshold, exclusion rule, item-retention rule, scoring rule, or claim boundary changed after that point.

## Allowed Files

Only these observed evidence filenames are allowed for the `v0.7.1` bridge bundle:

```text
validation/v0.7/cross_domain_bridge/observed_wave7_results.json
validation/v0.7/cross_domain_bridge/content_validity_dossier.json
validation/v0.7/cross_domain_bridge/wave7_bridge_evidence.json
validation/v0.7/cross_domain_bridge/wave7_evidence_provenance.json
validation/v0.7/cross_domain_bridge/wave7_evidence_manifest.json
releases/v0.7.1/manifest.json
```

The matching templates are:

```text
validation/v0.7/cross_domain_bridge/observed_wave7_results.template.json
validation/v0.7/cross_domain_bridge/content_validity_dossier.template.json
validation/v0.7/cross_domain_bridge/wave7_bridge_evidence.template.json
validation/v0.7/cross_domain_bridge/wave7_evidence_provenance.template.json
validation/v0.7/cross_domain_bridge/wave7_evidence_manifest.template.json
```

`wave7_bridge_dossier.json` is not an allowed name. The canonical observed bridge evidence artifact is `wave7_bridge_evidence.json`, and it must pass:

```bash
python3 tools/validate_cross_domain_bridge_evidence.py validation/v0.7/cross_domain_bridge/wave7_bridge_evidence.json
```

## Artifact Roles

`observed_wave7_results.json` records the respondent flow, input checksums, outcome-inspection timing, item-level distributions, model outputs, sensitivity checks, and analyst and reviewer signoff needed to reproduce the bridge decisions. It is the observed-result ledger and should not contain interpretive release language beyond bounded bridge diagnostics.

`content_validity_dossier.json` records independent expert review of cross-domain content coverage, item-domain assignment, construct representation, unresolved flags, and claim boundaries before psychometric evidence is used.

`wave7_bridge_evidence.json` is the machine-validated decision artifact. It maps the observed results to preregistered bridge gates for analytic `N`, exclusions, factor structure, omega, IRT linking, DIF, invariance, latent correlations, and bifactor or second-order readiness. It must keep all scoring authorization fields false.

`wave7_evidence_provenance.json` binds each claimed statistic to the restricted data artifact, covariate file, fielding disposition file, analysis script or notebook, generated output, checksum, analyst, reviewer, and outcome-inspection timing.

`wave7_evidence_manifest.json` is the reproducibility index for the bundle. It lists every release-relevant artifact, its SHA-256 checksum, its role, the command or procedure that produced it, and the signoff status required before `releases/v0.7.1/manifest.json` can checksum the completed bundle.

`releases/v0.7.1/manifest.json` is the release manifest. It can be created only after the observed files above are complete, reviewed, and checksum-bound.

## Required Signoff Roles

The bundle must record distinct roles, even when an organization assigns more than one person to a role:

- Fielding custodian: confirms sample source, eligibility rules, no-event administration, fielding windows, restricted data hashes, and respondent disposition counts.
- Analysis lead: runs the preregistered analysis without changing thresholds after outcome inspection and records software, package, seed, and output checksums.
- Psychometric reviewer: verifies factor, reliability, IRT, DIF, invariance, latent-correlation, and general-factor readiness results against the preregistered gates.
- Content-validity reviewer: confirms item-domain coverage and unresolved content flags before bridge promotion language is drafted.
- Release reviewer: confirms checksum completeness, allowed filenames, no scoring authorization, claim limits, and consistency with `docs/releases/v0.7_to_v0.7.1_promotion_gate.md`.

Analyst signoff alone is insufficient. Reviewer signoff must explicitly state whether outcome inspection occurred before or after each rule, threshold, and claim-boundary decision was locked.

## Promotion Order

Promotion to a citable `v0.7.1` bridge-evidence release must proceed in this order:

1. Freeze `v0.7.0` source inputs, including the manifest, preregistration, no-event registry, analysis plan, construct registry, schema dependencies, and 12 item files.
2. Complete fielding under `event_id: no_event`, preserving the preregistered administration and exclusion rules.
3. Populate `observed_wave7_results.json` from the restricted respondent-item data, fielding disposition file, covariate file, and preregistered analysis outputs.
4. Populate `wave7_evidence_provenance.json` and `wave7_evidence_manifest.json` with nonzero SHA-256 checksums for every restricted input, script, software lock, generated output, signoff record, and public evidence artifact.
5. Complete and validate `content_validity_dossier.json`.
6. Populate and validate `wave7_bridge_evidence.json`.
7. Create `releases/v0.7.1/manifest.json` only after the observed evidence files are complete and checksum-stable.
8. Validate the release manifest.
9. Publish only bridge-evidence claims. Any aggregate-score proposal must be separately preregistered after this gate and must keep Wave 7 scoring unauthorized until a later scored-release gate passes.

Required commands from the repository root:

```bash
python3 tools/validate_content_validity_dossier.py validation/v0.7/cross_domain_bridge/content_validity_dossier.json
python3 tools/validate_cross_domain_bridge_evidence.py validation/v0.7/cross_domain_bridge/wave7_bridge_evidence.json
python3 tools/validate_release.py releases/v0.7.1/manifest.json
```

