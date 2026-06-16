# Aggregate Score Proposal Protocol

This protocol governs any proposed overall, cross-domain, or domain-combined ANX-Bench score after `v0.7.1`. It is intentionally conservative: bridge evidence can make a proposal eligible for review, but bridge evidence never authorizes a score.

## Purpose

ANX-Bench is domain-stratified by design. A single overall ANX value is a stronger claim than an item score, construct score, or domain-specific estimate because it says that multiple psychological response domains can be combined without erasing meaningful construct differences. That claim requires a versioned proposal contract before any score is calculated, reported, trended, or used as an event-study outcome.

The required machine-readable contract is `schema/aggregate_score_proposal.schema.json`. A proposal must validate with:

```bash
python3 tools/validate_aggregate_score_proposal.py proposals/v0.8/overall_anx_score_proposal.template.json
```

The template at `proposals/v0.8/overall_anx_score_proposal.template.json` is preregistered but not scored. It keeps `scoring_authorized: false`.

## Frozen v0.8 Candidate Estimand

The `v0.8` overall ANX proposal template freezes a candidate estimand for future review: a construct-first observed-score mean on the original 1 to 5 response scale, using equal weights for the approved somatic ambient, economic vocational, and epistemic trust construct means. The primary respondent-level candidate score is the arithmetic mean of those approved construct means. The primary release-level estimate, if later authorized, is the survey-weighted population mean of that respondent-level score within the release-defined population.

This section is preregistered methodology only. It does not authorize calculation, publication, interpretation, trending, subgroup comparison, or event-study use of an overall ANX score. Authorization still requires observed bridge evidence, independent approval of each contributing source construct, passing review under this protocol, and a later citable release manifest that explicitly enables aggregate scoring while preserving the registered claim limits.

## When A Proposal Is Allowed

An overall or domain-combined ANX proposal is allowed only after all conditions below are true.

1. A citable `v0.7.1` or later bridge-evidence release exists.
2. The bridge evidence artifact is observed, not a template.
3. The bridge evidence passes `tools/validate_cross_domain_bridge_evidence.py`.
4. The bridge final decision is exactly `bridge_supported_for_overall_readiness_review`.
5. The bridge final decision keeps `scoring_authorized: false`.
6. Every contributing source construct has independent scored approval for use as an aggregate source.
7. The proposal specifies the scoring model, construct and item inputs, weights, missingness rules, uncertainty reporting, invariance and DIF limits, claim scope, blocked uses, preregistration date, and reviewer signoff.
8. The proposal passes `tools/validate_aggregate_score_proposal.py`.
9. A later release manifest explicitly approves scoring under its own release gate.

If any condition fails, the proposal may remain archived as a rejected or superseded artifact, but no aggregate ANX score may be calculated or publicized.

## Bridge Evidence Is Not Score Authorization

Bridge evidence answers a readiness question: whether observed cross-domain psychometric evidence is strong enough to justify preregistering a possible aggregate score. It does not answer the release question: whether ANX-Bench has an official score that users may compute.

The bridge evidence can support statements such as:

- observed Wave 7 evidence supports or blocks aggregate-score readiness review;
- cross-domain correlations, factor structure, reliability, IRT linking, DIF, and invariance met or failed preregistered thresholds;
- a later proposal is or is not eligible for review.

The bridge evidence cannot support statements such as:

- ANX-Bench now has an official overall score;
- the public has a national overall ANX level;
- one subgroup has a higher validated overall ANX than another when invariance limits affect that comparison;
- model releases, policy events, or news shocks caused movement in an overall ANX outcome;
- individuals, occupations, institutions, or regions can be ranked for decision use.

## Required Proposal Content

Each aggregate-score proposal must include:

- `source_bridge_evidence`: path, evidence ID, observed status, bridge decision, and an explicit statement that bridge evidence is not authorization.
- `contributing_constructs`: construct IDs, domain IDs, source releases, approval artifacts, approval dates, item membership, and bridge role.
- `contributing_items`: item IDs, versions, construct IDs, domain IDs, source item status, and scoring-key lock status.
- `scoring_model`: model family, estimand, scale, aggregation sequence, source score inputs, and release authorization state.
- `weights`: construct weights, domain weights, population weighting, and sensitivity-weight plan.
- `missingness_rules`: unit, item, and construct missingness rules, imputation prohibition or rule, and missingness reporting.
- `uncertainty_reporting`: standard error method, confidence interval method, design effect reporting, replication or bootstrap plan, and minimum reported fields.
- `invariance_dif_limits`: required invariance level, failed-comparison rule, unresolved-DIF rule, affected claim limits, and observed unresolved counts.
- `claim_scope`: population, construct, and time scope, permitted claims, explicit claim limits, and prohibited-claim acknowledgement.
- `blocked_uses`: all uses that remain disallowed even if the proposal passes review.
- `reviewer_signoff`: psychometric reviewer, release reviewer, signed date, decision, and signoff statement.

## Default Blocked Uses

The following uses remain blocked unless a later release explicitly says otherwise:

- clinical diagnosis, screening, or triage;
- individual-level classification, ranking, or targeting;
- policy-decision ranking of institutions, regions, jobs, or demographic groups;
- employment, education, insurance, credit, housing, or benefit eligibility decisions;
- longitudinal trend claims without longitudinal invariance and a preregistered time-series design;
- event-study claims without an event registry, baseline window, follow-up window, exposure definition, and causal estimand;
- national prevalence claims without a sampling and weighting design that supports that population claim;
- cross-national or non-English claims without separate linguistic and cultural validation.

## Release Gate

A passed proposal is necessary but not sufficient. It may be cited as a preregistered aggregate-score proposal only after review signoff. It still leaves scoring disabled until a release manifest changes the release state under `schema/release.schema.json`, checksums the proposal and all source artifacts, and authorizes aggregate scoring in release language that matches the proposal claim limits.
