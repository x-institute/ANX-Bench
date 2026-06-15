# ANX-Bench

ANX-Bench is the Anthropogenic Nervousness Benchmark: a longitudinal, domain-stratified benchmark for measuring human psychological response to AI capabilities. It is designed as a standardized, repeatable, versioned research instrument rather than an ad hoc survey. The benchmark supports psychometric validation, pre-registration, event-study analysis around AI capability shocks, and comparisons across populations and waves.

The current benchmark release is **ANX-Bench v0.1.0**. Version `v0.1.0` establishes the public instrument schema, the initial methodology contract, and one fully specified exemplar item in the economic/vocational domain.

## Benchmark Contract

Every ANX-Bench release is a fixed package of:

- A semantic benchmark version, such as `v0.1.0`.
- A JSON Schema for benchmark item records.
- A versioned item directory containing all items admitted to that release.
- Methodology documentation specifying scoring, aggregation, longitudinal comparability, and release rules.
- A preregistration protocol for longitudinal waves and event-study claims.
- A psychometric validation protocol defining the evidence required before items become benchmark-scored.

Items are not part of a benchmark-scored release until they validate against `schema/item.schema.json`, satisfy the psychometric validation gate in `docs/psychometric_validation_protocol.md`, and are placed under the appropriate versioned item directory. Schema-valid items may exist as exemplars or development candidates, but schema validity alone does not mean an item is psychometrically validated or eligible for official ANX-Bench scoring.

## Stable Directory Structure

```text
ANX-Bench/
  README.md
  doc/
    claude.md
  docs/
    methodology.md
    psychometric_validation_protocol.md
    preregistration_event_study.md
  schema/
    item.schema.json
  items/
    v0.1/
      economic_vocational/
        job_displacement_radiology.json
```

Directory meanings:

- `schema/`: Machine-readable validation contracts for benchmark artifacts.
- `items/`: Versioned benchmark items, grouped first by release line and then by domain.
- `docs/`: Methodology, scoring, aggregation, psychometric validation, longitudinal comparability rules, and preregistration protocols.
- `doc/`: Project notes and conceptual background.

Future benchmark versions must preserve this structure. New releases may add directories, but they must not move, rename, or reinterpret existing released item files.

## Release Versioning

ANX-Bench uses semantic versioning for benchmark releases:

- `MAJOR`: Breaking changes to item semantics, score interpretation, core constructs, or aggregation rules.
- `MINOR`: Addition of validated domains, constructs, items, populations, or administration modes that preserve comparability with earlier releases.
- `PATCH`: Corrections that do not change item meaning, score calculation, or comparability.

The `items/v0.1/` directory is the canonical item set for the `0.1.x` release line. Any future `v0.1.x` patch release must document the patch reason and show that existing item responses remain interpretable under the same scoring rules.

## Required Item Validation

Every future item must validate against `schema/item.schema.json` before inclusion in a benchmark release. Schema validation is a release-blocking requirement, but it is only the first gate. Items that fail schema validation, lack a 5-point Likert response scale, omit scoring metadata, omit exclusion criteria, or lack interpretation bands cannot be included in the released benchmark item set.

Every item must also satisfy `docs/psychometric_validation_protocol.md` before it can move from exemplar or development status to benchmark-scored status. The protocol requires a development pilot, independent confirmation sample, refresh or bridge sample for revised items, EFA and CFA evidence, reliability targets, IRT calibration, DIF checks, measurement-invariance thresholds, and item retention rules. Items that are schema-valid but have not passed this gate are not psychometrically validated and must not contribute to official item-level, construct, domain, overall, longitudinal, or event-study scoring.

## Initial Exemplar

The first exemplar item is:

```text
items/v0.1/economic_vocational/job_displacement_radiology.json
```

It measures anticipated AI-driven job displacement anxiety in radiology and demonstrates the minimum required structure for a fully specified ANX-Bench item.
