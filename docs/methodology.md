# ANX-Bench Methodology

This document defines the methodological contract for ANX-Bench v0.1.0. ANX-Bench is a longitudinal benchmark instrument for measuring psychological response to AI capabilities across domains of human life. Its core requirements are standardization, repeatability, version control, psychometric defensibility, and comparability across measurement waves.

## Item Versioning Rules

Each benchmark item has two identifiers:

- `item_id`: A stable snake_case identifier that names the conceptual item.
- `version`: A semantic version for the item record.

Released item files are immutable except for patch-level corrections that do not alter participant-facing meaning, response options, scoring, eligibility, or interpretation. Examples of permitted patch changes include correcting a typographical error that does not change meaning, adding non-substantive metadata, or clarifying an administration note without changing the procedure.

Any change to scenario wording, response anchors, scoring direction, exclusion criteria, target population, or interpretation bands requires a new item version. If the change affects longitudinal comparability, the modified item must either receive a new `item_id` or be explicitly linked to the prior item through a documented bridge study.

Items must be validated against `schema/item.schema.json` before inclusion in a benchmark release. Schema validation is necessary but not sufficient: inclusion also requires substantive review for construct validity, ethical risk, clarity, reading level, consistency with the domain taxonomy, and completion of the psychometric validation gate in `docs/psychometric_validation_protocol.md`.

Each release manifest must carry a top-level `release_status` lifecycle state: `draft`, `frozen_candidate`, `citable`, or `deprecated`. This manifest-level state is distinct from item-level `release_status`. Only a manifest marked `release_status: citable` may support ANX-Bench benchmark claims, including item-level scored claims, construct scores, domain scores, overall scores, longitudinal wave comparisons, event-study estimates, calibration claims, or public benchmark trend statements. A `frozen_candidate` manifest may freeze preregistered materials, item candidates, analysis plans, fielding instruments, evidence-provenance contracts, and checksums for reproducibility, but it must not contain official scored items, must not mark frozen items as scoring eligible, and must keep aggregate scoring disabled. A `citable` manifest must not be future-dated relative to the validation run that authorizes publication.

Every item file must carry a machine-readable lifecycle state in `release_status` and a required `validation` object with the psychometric decision, decision date, validation dossier path, preregistration path, and scoring eligibility. The allowed release states are `exemplar`, `development_only`, `approved_item_level_only`, `approved_scored`, and `blocked`. The validation dossier path must point to the evidence record for the item version once available, using the structure in `docs/validation_dossier_template.md`; preregistration pointers must identify the frozen protocol that governs scored or confirmatory use.

Schema-valid items may be stored as exemplar or development items while they are being drafted, piloted, or revised. They must not be treated as benchmark-scored items, included in construct, domain, or overall ANX aggregation, or used as confirmatory longitudinal or event-study outcomes until the psychometric validation dossier approves the item version for scored release. Only items with `release_status: approved_scored` and `validation.scoring_eligible: true` may enter construct, domain, or overall ANX scoring.

## Domain Taxonomy

ANX-Bench v0.1.0 uses seven top-level domains:

1. `economic_vocational`: Anxiety about employment, wages, skill obsolescence, occupational status, bargaining power, and career security.
2. `epistemic`: Anxiety about truth, evidence, deepfakes, misinformation, provenance, expertise, and the ability to trust information environments.
3. `relational`: Anxiety about AI effects on friendship, intimacy, family life, care, social substitution, and attachment.
4. `existential_identity`: Anxiety about meaning, human distinctiveness, creativity, dignity, agency, and self-concept.
5. `autonomy_surveillance`: Anxiety about monitoring, manipulation, automated evaluation, profiling, loss of choice, and institutional control.
6. `safety_catastrophic`: Anxiety about physical safety, misuse, weapons, loss of control, systemic failure, and extreme-risk narratives.
7. `somatic_ambient`: Diffuse bodily unease, vigilance, sleep disturbance, background dread, and other low-specificity anxiety responses to AI progress.

Every item must have exactly one primary domain. Secondary domains may be discussed in documentation, but the item record must use one primary `domain` value so aggregation remains reproducible.

## Response Scale and Scoring

ANX-Bench v0.1.0 uses a 5-point Likert scale for released self-report items. The standard response values are integers from 1 to 5, where higher scored values indicate greater AI-related anxiety unless `reverse_coded` is true.

Each item must include:

- A response prompt.
- Five ordered anchors.
- A `reverse_coded` flag.
- A scoring key mapping raw responses to scored values.
- Missing-response handling.
- Exclusion criteria.
- Interpretation bands.

For non-reverse-coded items, raw responses `1` through `5` map directly to scored values `1` through `5`. For reverse-coded items, the scoring key must map raw `1` to scored `5`, raw `2` to scored `4`, raw `3` to scored `3`, raw `4` to scored `2`, and raw `5` to scored `1`.

Primary analyses must not impute missing single-item responses unless the pre-registered analysis plan specifies a missing-data model. Respondents excluded by item-level or survey-level criteria must be removed before score aggregation for the affected analysis.

## Score Aggregation

Construct and domain aggregation must be driven by the versioned construct registry for the applicable release line. For `v0.1.0`, the authoritative registry is `constructs/v0.1/registry.json`, validated by `schema/construct_registry.schema.json`. Construct labels embedded in item JSON are item metadata only; they are not sufficient authority for aggregation, item retention, anchor interpretation, or domain scoring. A scoring pipeline must resolve each item's `construct.construct_id` against the registry, confirm that the item ID is listed in the construct's `allowed_item_ids`, and apply the registry's `intended_aggregation_level`, `minimum_retained_items`, `anchor_status`, and validation requirements before computing any construct, domain, or overall ANX score.

Aggregation proceeds in four levels:

1. Item score: The scored value after applying the item scoring key.
2. Construct score: The mean of valid item scores assigned to the same construct within a wave.
3. Domain score: The mean of valid construct scores within a domain, weighted equally by construct unless a pre-registered alternative is used.
4. Overall ANX score: The mean of valid domain scores, weighted equally by domain for the headline benchmark.

Aggregation must filter item records before scoring. Items with `release_status` equal to `exemplar`, `development_only`, `approved_item_level_only`, or `blocked` must be excluded from construct, domain, and overall ANX scoring even if they are schema-valid, even if raw responses exist, and even if their embedded item JSON contains a plausible construct label. `approved_item_level_only` items may be summarized only as item-level descriptive or exploratory outcomes when the validation dossier, preregistration, and construct registry authorize that reporting.

Validated constructs must not be combined into domain-composite, cross-domain, or overall benchmark scores solely because each construct has passed its own within-domain validation gate. Before any release may propose a combined score, maintainers must freeze and complete a bridge study that co-administers the contributing constructs in one sample and provides preregistered evidence for multidomain factor structure, reliability, IRT linking or another documented linking model, DIF, measurement invariance, bounded cross-domain correlations, and discriminant validity against general anxiety. For the current release sequence, `v0.7.0` is the required bridge packet before any overall ANX or cross-domain score can be proposed; it is bridge evidence only and must keep aggregate scoring disabled until a later citable release explicitly authorizes a scoring model.

Domain and overall scores must report the number of contributing items, constructs, respondents, exclusions, and missing responses. A domain score should not be reported for a respondent unless at least half of the released construct coverage for that domain is observed. Wave-level reports must include confidence intervals or credible intervals and must distinguish population-weighted estimates from unweighted sample summaries.

Interpretation bands are item-level aids, not diagnostic categories. They may describe low, moderate, and high anxiety responses for a scenario, but they must not be presented as clinical cutoffs.

## Longitudinal Comparability Requirements

Longitudinal comparability is a primary benchmark requirement. A score from one wave is comparable to a score from another wave only when the following conditions hold:

- The respondent-item response data validate against `schema/wave_response.schema.json`.
- The same released item versions are administered or a documented bridge study links old and new item versions.
- Response anchors, scoring keys, exclusion criteria, and administration mode are unchanged.
- Sampling frame, weighting, and recruitment source are documented for each wave.
- Measurement invariance is evaluated when comparing major populations, languages, or time periods.
- Event-study windows are pre-registered before outcome data are inspected.
- Any major AI event used as an exposure is timestamped, documented, and classified independently of the observed ANX-Bench response.

If wording or administration changes are necessary, the release must document whether the change is patch-level, minor, or breaking. Breaking changes require a new benchmark major version and should be analyzed as a new time series unless calibration evidence supports continuity.

## Longitudinal and Event-Study Preregistration Gate

Any ANX-Bench release, report, dashboard, manuscript, or public artifact that makes a longitudinal wave comparison or event-study claim must include a completed preregistration file following `docs/preregistration_event_study.md`. This requirement is release-blocking. A wave may be fielded for instrument development without a completed preregistration, but its results must not be presented as a confirmatory longitudinal estimate, event-study estimate, benchmark trend, or capability-shock response.

The completed preregistration must identify the wave ID, benchmark version, item versions, target population, sampling frame, weighting plan, exclusion rules, analysis freeze date, event definition if applicable, primary outcomes, and statistical plan before response outcomes are inspected. If the file is missing, incomplete, finalized after outcome inspection, or inconsistent with the administered item versions, the release must either be blocked or the affected analyses must be labeled exploratory and excluded from confirmatory benchmark claims.

The canonical analytic file for any fielded wave must be one respondent-item response row per administered item version and must validate against `schema/wave_response.schema.json`. This gate applies to validation samples, longitudinal waves, and event-study waves. A wave whose response data do not validate against the wave response schema cannot support psychometric validation evidence, longitudinal comparison, benchmark trend reporting, or event-study claims, even if the item files and preregistration are otherwise valid. Schema-valid response data are necessary but not sufficient: the wave must still satisfy preregistration, privacy, weighting, exclusion, measurement-invariance, and psychometric validation requirements before confirmatory claims are permitted.

## Psychometric Validation Gate

Before an item moves from exemplar or development status to benchmark-scored status, maintainers must complete the validation protocol in `docs/psychometric_validation_protocol.md` and archive a completed validation dossier using `docs/validation_dossier_template.md`. This gate is release-blocking for any item that will contribute to item-level scored reporting, construct scores, domain scores, the overall ANX score, longitudinal comparisons, or event-study outcomes.

The validation dossier must show, at minimum, that:

- The item version was evaluated in a development pilot with adequate sample size for exploratory factor analysis, preliminary reliability review, response-distribution checks, and early DIF screening.
- The retained item version was evaluated in an independent confirmation sample for confirmatory factor analysis, reliability, IRT calibration, preregistered DIF checks, and final item retention.
- Any revised, translated, re-anchored, re-scored, or mode-changed item has a refresh or bridge sample sufficient to support the claimed continuity with the prior released item version.
- The item satisfies the protocol's retention rules for primary factor loading, cross-loading, corrected item-total correlation, ceiling or floor concentration, missing or non-substantive response, local dependence, and unstable DIF.
- Measurement invariance or a documented linking alternative supports every intended comparison across populations, languages, modes, and waves.

An item that fails this gate may remain in the repository only as an exemplar, development, item-level-only, or blocked item if its status is explicit and it is excluded from benchmark scoring. A schema-valid item that lacks psychometric approval is not a released benchmark-scored item.

## Benchmark Release Gate

Before an item can be included in a benchmark release, maintainers must verify that:

- The item validates against `schema/item.schema.json`.
- The item's `construct.construct_id` is registered in the applicable versioned construct registry and the item ID appears in that construct's `allowed_item_ids`.
- The item file carries `release_status` and the required `validation` object.
- The item has completed the psychometric validation gate in `docs/psychometric_validation_protocol.md`, unless it is explicitly labeled exemplar, development, item-level-only, or blocked and excluded from benchmark scoring.
- The item has `release_status: approved_scored` and `validation.scoring_eligible: true` before it contributes to construct, domain, or overall ANX scoring.
- The item belongs to exactly one approved domain.
- The scenario text is concrete, comprehensible, and ethically acceptable for the target population.
- The item has a 5-point Likert scale, reverse-coding flag, scoring key, exclusion criteria, and interpretation bands.
- The item can be administered without changing prior released items in the same benchmark version.
- The release notes state whether the item is new, patched, bridged, or breaking.

Failure to satisfy any release gate blocks inclusion in the released ANX-Bench item set.

For all releases after `v0.1.0`, registration is a precondition for freezing: any future item must reference a registered construct ID, and the construct registry must explicitly list the item ID as allowed, before that item can enter a frozen item set. New ad hoc construct names inside item JSON do not create a construct, do not authorize scoring, and do not satisfy the release gate.

Before any longitudinal wave or event-study claim can be included in a benchmark release, maintainers must also verify that the completed preregistration file required by `docs/preregistration_event_study.md` exists and was frozen before response data inspection. Failure to satisfy this preregistration gate blocks the longitudinal or event-study claim even if the underlying item set is valid.

Maintainers must also verify that the frozen wave response dataset validates against `schema/wave_response.schema.json` and that the variables are documented according to `docs/wave_data_dictionary.md`. Failure to satisfy this wave response schema gate blocks validation, longitudinal, and event-study claims for that wave, including claims based on otherwise valid items.

Finally, maintainers must verify the manifest-level lifecycle gate. Benchmark claims may be made only from a manifest with `release_status: citable` that passes `tools/validate_release.py` on or after its `release_date`. Draft manifests, frozen candidates, and deprecated manifests may be cited descriptively as repository artifacts, but they do not authorize official ANX-Bench benchmark claims.
