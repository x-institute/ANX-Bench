# Somatic Ambient Wave 1 Validation Runner

This directory contains the frozen, reproducible psychometric validation runner for the v0.3.0 somatic and ambient promotion review. The runner is bound to `analysis/v0.2/somatic_ambient/wave1_analysis_plan.json` and must not be edited after outcome inspection except through a dated preregistered addendum.

## Required Input

Run the script from the repository root after the restricted respondent-item analytic file has been staged at the exact path declared in the analysis plan:

```bash
vendor_restricted/anx_us_2026w02_somatic/wave_response.jsonl
```

The file must contain one JSON object per respondent-item row. It must include every field declared by `fielded_wave_response_file` and the validation variables declared by `instrument_codebook` in `wave1_analysis_plan.json`. The runner also requires `benchmark_version` and `item_version` so it can fail closed on version drift. All rows must have `event_id: "no_event"` because this calibration wave is not an event study.

## Run Command

From the repository root:

```bash
Rscript analysis/v0.2/somatic_ambient/run_wave1_validation.R
```

The R environment must provide the frozen package set listed in `wave1_analysis_plan.json`: `psych`, `lavaan`, `semTools`, `mirt`, `lordif`, `survey`, and `mice`. The runner additionally uses `jsonlite` for JSON I/O and `MASS` for ordinal logistic validity and DIF models.

## Generated Artifact

The runner writes one machine-readable artifact:

```bash
validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json
```

That file records input hashes, session information, exclusion flow, scoring, EFA, CFA, omega and alpha, graded-response IRT, DIF, invariance, external-validity models, item-level retention statistics, and validation-gate outcomes. It is the only observed-results artifact reserved by the evidence manifest for this wave.

## Promotion Rule

Manual promotion of the somatic and ambient dossier is invalid unless `observed_wave1_results.json` exists, covers all four frozen item IDs, records the restricted input data hash, records the runner and session hashes in the evidence manifest, and provides every statistic needed by the dossier thresholds. The runner output does not by itself authorize scored release. It supplies checksum-bound evidence for independent psychometric review and a later citable release manifest.
