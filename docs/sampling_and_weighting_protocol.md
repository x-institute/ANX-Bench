# ANX-Bench Sampling and Weighting Protocol

## Purpose

ANX-Bench estimates must be traceable to a frozen sampling and weighting plan, not reconstructed after outcome inspection. A wave may collect useful calibration data without such a plan, but it cannot support population, subgroup, longitudinal, or event-study benchmark claims unless the sampling plan has been written, versioned, and validated before fielding outcomes are inspected.

The sampling plan is a wave-level contract. It defines who the wave is intended to represent, how respondents are reached, what quotas are monitored, what analytic sample sizes are planned, how weights are constructed, how standard errors are estimated, which subgroup cells are claim-eligible, and which claims are blocked. This contract separates sampling inference from psychometric scoring. A valid scale does not by itself create a valid population estimate.

## Required Frozen Artifact

Every fielded ANX-Bench wave must include a JSON sampling plan that validates against `schema/sampling_plan.schema.json`. The plan must be frozen before recruitment begins or, at minimum, before any ANX outcome, item distribution, construct score, event-window estimate, or subgroup difference is inspected.

The frozen plan must specify:

- Target population, including geography, language, age eligibility, inclusion rules, exclusion rules, and known coverage limits.
- Sampling frame, including whether the frame is probability-based, address-based, nonprobability online, or hybrid.
- Recruitment source, eligibility screening, duplicate prevention, and nonresponse tracking.
- Quota variables, category definitions, target margin source, and whether each quota is hard, soft, or monitor-only.
- Planned usable N by split, including development, confirmation, bridge, baseline, follow-up, and refreshment roles where applicable.
- Weighting method, construction steps, raking or calibration variables, diagnostics, trim bounds, and final mapping into the `survey_weight` field in `schema/wave_response.schema.json`.
- Variance design, including the standard-error estimator, clustering or stratification variables when available, replicate-weight variables when used, finite-population correction when applicable, and software.
- Subgroup cells eligible for confirmatory comparison, descriptive-only reporting, or suppression.
- Claim limits covering population estimates, subgroup comparisons, longitudinal change, event-study effects, causal effects, clinical interpretation, and individual-level use.

## Claim Rules

Population claims require a target population, sampling frame, recruitment source, weight construction, final `survey_weight` mapping, trim bounds, and variance metadata. If any of these components is absent, population statements must be limited to unweighted or weighted sample descriptions, not population estimates.

Subgroup claims require prespecified subgroup cells and suppression rules. A subgroup cell can be confirmatory only when the plan defines its variables, minimum usable N, weight treatment, and variance treatment before outcome inspection. Cells that miss their planned minimum N must be reported as descriptive or suppressed according to the plan.

Longitudinal claims require compatible sampling plans across waves. The plans must define the target population, frame changes, refreshment or panel overlap rules, weight harmonization, and variance estimation before trend or change estimates are inspected. A longitudinal psychometric bridge does not authorize trend inference unless the sampling plans support that inference.

Event-study claims require a valid sampling plan for each baseline and follow-up wave used in the event design. The plan must state whether the wave supports population event-window estimates, subgroup event-window estimates, or only sample-level event evidence. Event-study inference also requires the separate event registry and preregistered analysis plan gates. A locked event registry without sampling metadata is insufficient for population event-study claims.

Nonprobability samples may be used for calibration, bridge, and descriptive research when disclosed. They cannot support probability-sampling language such as nationally representative, margin of error, or unbiased population prevalence unless an explicitly justified hybrid or model-based inference design is preregistered, weighted, variance-estimated, and labeled with its assumptions. For ordinary nonprobability panels, ANX-Bench claims must say that weighted estimates are descriptive calibrated estimates for the covered online adult sample.

## Validation Gate

Validate a sampling plan from the repository root:

```bash
python3 tools/validate_sampling_plan.py sampling/v0.7/anx_us_2026w07_cross_domain_bridge_sampling_plan.json
```

The validator checks the JSON schema and ANX-specific claim gates. It rejects missing target population metadata, missing weight construction, final weights that do not map to `survey_weight`, invalid trim bounds, and any population claim that lacks weighting or variance metadata.

For Wave 7, this command must pass for `sampling/v0.7/anx_us_2026w07_cross_domain_bridge_sampling_plan.json` before any bridge evidence can be used to support a later overall ANX, cross-domain, or domain-combined score proposal. The retained `.template.json` file is only a drafting aid and cannot serve as the frozen claim-bearing contract. The frozen Wave 7 plan fixes the bridge sample size, minimum eligible sample, US English online adult frame, quota and monitoring variables, exclusion flow, raking method, trim bounds, variance design, subgroup suppression rules, and blocked longitudinal, event-study, causal, clinical, and individual-level claims.

The validated sampling plan is a release reproducibility artifact. It must be listed in release documentation and included in release checksums before a fielded wave is cited for any population, subgroup, longitudinal, or event-study claim.
