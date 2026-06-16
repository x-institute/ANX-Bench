# ANX-Bench Preregistrations

This directory stores frozen preregistration packets for ANX-Bench calibration waves, longitudinal waves, bridge studies, and event-study analyses. A preregistration file is part of the evidence chain for item validation. It specifies what was intended before data were inspected, while the validation dossier records what was observed and how the release decision was made.

## Filename Convention

Use lowercase snake case:

```text
anx_<population>_<year>w<wave>_<purpose>.md
```

Examples:

- `anx_us_2026w01_calibration.md`: US adult Wave 1 calibration study for initial item validation.
- `anx_us_2026w02_event_study.md`: US adult Wave 2 event-study wave.
- `anx_us_2026w01_bridge.md`: bridge study for revised item wording or administration mode.

Filename fields:

- `population`: the target population or geography, such as `us`, `uk`, `jp`, or `us_healthcare_workers`.
- `year`: four-digit calendar year in which fielding is planned to begin.
- `w<wave>`: two-digit wave number within that population and year.
- `purpose`: the preregistered purpose, such as `calibration`, `confirmation`, `bridge`, `translation`, or `event_study`.

## Freeze Rules

A preregistration is frozen when respondent recruitment begins or when the study team declares the instrument frozen, whichever comes first. After freeze:

- Administered item IDs, item versions, scenario text, response anchors, item order rules, primary outcomes, exclusion rules, QC rules, sampling targets, and primary analyses cannot be changed in place.
- Corrections to typos or broken links must be made through an addendum section that preserves the original text.
- Changes required by IRB, vendor implementation, or fielding problems must be timestamped and labeled as pre-outcome or post-outcome.
- Any change to participant-facing item wording, response anchors, scoring key, administration mode, language, or population eligibility requires a new item version or a bridge preregistration before comparability can be claimed.
- A preregistration cannot be used to justify a scored release if it was written or materially changed after outcome data were inspected.

Prose preregistrations are necessary but not sufficient for calibration-release claims. When a preregistration references a machine-readable psychometric analysis plan, that JSON plan must pass `python3 tools/validate_analysis_plan.py analysis/.../wave*_analysis_plan.json --release releases/.../manifest.json` before the release can be treated as frozen, citable calibration infrastructure. The validator checks the plan against `schema/psychometric_analysis_plan.schema.json`, confirms the preregistration path exists, requires `authoritative_contract: true` and `outcome_inspection_status: not_inspected`, verifies that the plan benchmark version matches the release manifest, and confirms that the planned item IDs equal the manifest's frozen item set.

## Linkage to Validation Dossiers

Every validation dossier must name the preregistration file that governed the sample and analysis plan. The corresponding item JSON `validation.preregistration_path` must point to that same preregistration before the item can move to `approved_item_level_only` or `approved_scored`.

The linkage is:

1. Preregistration freezes the planned sample, administered item versions, outcomes, exclusions, QC checks, and analyses.
2. Fielding produces a locked raw dataset and codebook.
3. Analysis scripts implement the preregistered plan and archive any deviations.
4. Validation dossiers report item-level evidence, retention thresholds, DIF and invariance results, and reviewer signoff.
5. Item JSON files and release manifests are updated only after the dossier decision is complete.

For Wave 1, the governing preregistration is `docs/preregistrations/anx_us_2026w01_calibration.md`. It supports calibration evidence for the `items/v0.1` item versions, but it does not itself approve any item for official aggregate ANX scoring.
