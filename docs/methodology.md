# ANX-Bench Methodology

This document defines the methodological contract for ANX-Bench v0.1.0. ANX-Bench is a longitudinal benchmark instrument for measuring psychological response to AI capabilities across domains of human life. Its core requirements are standardization, repeatability, version control, psychometric defensibility, and comparability across measurement waves.

## Item Versioning Rules

Each benchmark item has two identifiers:

- `item_id`: A stable snake_case identifier that names the conceptual item.
- `version`: A semantic version for the item record.

Released item files are immutable except for patch-level corrections that do not alter participant-facing meaning, response options, scoring, eligibility, or interpretation. Examples of permitted patch changes include correcting a typographical error that does not change meaning, adding non-substantive metadata, or clarifying an administration note without changing the procedure.

Any change to scenario wording, response anchors, scoring direction, exclusion criteria, target population, or interpretation bands requires a new item version. If the change affects longitudinal comparability, the modified item must either receive a new `item_id` or be explicitly linked to the prior item through a documented bridge study.

Items must be validated against `schema/item.schema.json` before inclusion in a benchmark release. Schema validation is necessary but not sufficient: inclusion also requires substantive review for construct validity, ethical risk, clarity, reading level, consistency with the domain taxonomy, and completion of the psychometric validation gate in `docs/psychometric_validation_protocol.md`.

Schema-valid items may be stored as exemplar or development items while they are being drafted, piloted, or revised. They must not be treated as benchmark-scored items, included in construct, domain, or overall ANX aggregation, or used as confirmatory longitudinal or event-study outcomes until the psychometric validation dossier approves the item version for scored release.

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

Aggregation proceeds in four levels:

1. Item score: The scored value after applying the item scoring key.
2. Construct score: The mean of valid item scores assigned to the same construct within a wave.
3. Domain score: The mean of valid construct scores within a domain, weighted equally by construct unless a pre-registered alternative is used.
4. Overall ANX score: The mean of valid domain scores, weighted equally by domain for the headline benchmark.

Domain and overall scores must report the number of contributing items, constructs, respondents, exclusions, and missing responses. A domain score should not be reported for a respondent unless at least half of the released construct coverage for that domain is observed. Wave-level reports must include confidence intervals or credible intervals and must distinguish population-weighted estimates from unweighted sample summaries.

Interpretation bands are item-level aids, not diagnostic categories. They may describe low, moderate, and high anxiety responses for a scenario, but they must not be presented as clinical cutoffs.

## Longitudinal Comparability Requirements

Longitudinal comparability is a primary benchmark requirement. A score from one wave is comparable to a score from another wave only when the following conditions hold:

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

## Psychometric Validation Gate

Before an item moves from exemplar or development status to benchmark-scored status, maintainers must complete the validation protocol in `docs/psychometric_validation_protocol.md`. This gate is release-blocking for any item that will contribute to item-level scored reporting, construct scores, domain scores, the overall ANX score, longitudinal comparisons, or event-study outcomes.

The validation dossier must show, at minimum, that:

- The item version was evaluated in a development pilot with adequate sample size for exploratory factor analysis, preliminary reliability review, response-distribution checks, and early DIF screening.
- The retained item version was evaluated in an independent confirmation sample for confirmatory factor analysis, reliability, IRT calibration, preregistered DIF checks, and final item retention.
- Any revised, translated, re-anchored, re-scored, or mode-changed item has a refresh or bridge sample sufficient to support the claimed continuity with the prior released item version.
- The item satisfies the protocol's retention rules for primary factor loading, cross-loading, corrected item-total correlation, ceiling or floor concentration, missing or non-substantive response, local dependence, and unstable DIF.
- Measurement invariance or a documented linking alternative supports every intended comparison across populations, languages, modes, and waves.

An item that fails this gate may remain in the repository only as an exemplar or development item if its status is explicit and it is excluded from benchmark scoring. A schema-valid item that lacks psychometric approval is not a released benchmark-scored item.

## Benchmark Release Gate

Before an item can be included in a benchmark release, maintainers must verify that:

- The item validates against `schema/item.schema.json`.
- The item has completed the psychometric validation gate in `docs/psychometric_validation_protocol.md`, unless it is explicitly labeled exemplar or development and excluded from benchmark scoring.
- The item belongs to exactly one approved domain.
- The scenario text is concrete, comprehensible, and ethically acceptable for the target population.
- The item has a 5-point Likert scale, reverse-coding flag, scoring key, exclusion criteria, and interpretation bands.
- The item can be administered without changing prior released items in the same benchmark version.
- The release notes state whether the item is new, patched, bridged, or breaking.

Failure to satisfy any release gate blocks inclusion in the released ANX-Bench item set.

Before any longitudinal wave or event-study claim can be included in a benchmark release, maintainers must also verify that the completed preregistration file required by `docs/preregistration_event_study.md` exists and was frozen before response data inspection. Failure to satisfy this preregistration gate blocks the longitudinal or event-study claim even if the underlying item set is valid.
