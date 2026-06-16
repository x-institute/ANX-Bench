# ANX-Bench Item Validation Dossier Template

This template defines the minimum validation dossier required before an ANX-Bench item version can be assigned `release_status: approved_item_level_only` or `release_status: approved_scored`. A completed dossier must be stored as a versioned, repository-relative file and referenced from the item record under `validation.dossier_path`.

The dossier is item-version specific. Evidence for a prior item version, translated item, alternate administration mode, or revised scoring key may support continuity only when the bridge evidence is documented in this dossier and the preregistration permits that use.

## Item Identification

- Item ID:
- Item version:
- Domain:
- Construct ID:
- Candidate release status:
- Candidate psychometric decision:
- Dossier path:
- Preregistration path:
- Validation samples:
- Analysis freeze date:
- Dossier author:
- Independent reviewer:

## Required Evidence Table

Every completed dossier must include the following table. Each row is required for each item version. When evidence is not applicable, the dossier must state why it is not applicable and identify the release consequence. Missing evidence is not equivalent to non-applicability.

| Evidence component | Required evidence | Minimum reporting standard | Pass criterion | Decision recorded |
| --- | --- | --- | --- | --- |
| EFA | Exploratory factor analysis in the development pilot using the preregistered item pool or a documented development pool. | Report sample size, extraction method, rotation, factor-retention rule, primary loading, cross-loadings, item communalities, and response-distribution diagnostics. | Primary loading and cross-loading pattern support the intended construct, with no distributional defect that invalidates interpretation under the psychometric validation protocol. | Retain, revise, reject, or escalate to reviewer. |
| CFA | Confirmatory factor analysis in an independent confirmation sample using the retained item specification. | Report sample size, estimator, model specification, fit indices, standardized loading, residual diagnostics, and any correlated residuals or post hoc modifications. | Fit and loading evidence support the preregistered construct model without undocumented model search that changes the item interpretation. | Retain, revise, reject, or require new confirmation sample. |
| Reliability | Internal consistency or appropriate single-item reliability evidence for the construct score that would include the item. | Report omega or alpha for multi-item constructs, corrected item-total correlation, test-retest evidence when available, and sensitivity to removing the item. | Reliability evidence meets the protocol threshold for the intended use and the item does not degrade construct reliability in the scored item set. | Retain for scoring, retain item-level only, revise, or reject. |
| IRT | Item response theory or ordinal item calibration appropriate to the response scale. | Report model family, category thresholds, discrimination, item information, local dependence checks, and calibration sample characteristics. | Item parameters are stable, ordered, and informative in the target anxiety range without unacceptable local dependence. | Retain, revise anchors, restrict use, or reject. |
| DIF | Differential item functioning checks for preregistered demographic, occupational, language, and exposure groups. | Report grouping variables, sample sizes, method, effect sizes, multiplicity handling, and direction of any DIF. | No practically important unexplained DIF remains for comparisons the item is intended to support, or a documented adjustment or restriction is approved. | Retain unrestricted, retain with restriction, revise, or reject. |
| Invariance | Measurement invariance evidence for intended population, language, mode, and longitudinal comparisons. | Report configural, metric, scalar, or approximate invariance tests as applicable, fit deltas, alignment or linking method, and comparison scope. | The item supports the claimed comparison level, or the dossier explicitly limits the comparison and scoring scope. | Approve comparison, limit comparison, require bridge study, or reject comparison. |
| External validity | Convergent, discriminant, criterion, and incremental-validity evidence for any item set proposed for `approved_scored` status. | Report preregistered comparator variables, criterion variables, covariate blocks, expected directions and magnitudes, observed estimates, confidence intervals, missingness, and whether the structured `external_validity` evidence object is complete. | External validity evidence supports the intended score interpretation and satisfies the release-blocking thresholds in `docs/psychometric_validation_protocol.md`. | Approve scored use, approve item-level only, require new validation sample, or block scored use. |
| Retention decision | Integrated psychometric and substantive decision for the item version. | Summarize evidence across EFA, CFA, reliability, IRT, DIF, invariance, ethics, construct coverage, and longitudinal comparability. | Decision is consistent with the evidence and with `validation.scoring_eligible`; only `approved_scored` items may enter construct, domain, or overall ANX scoring. | Exemplar, development_only, approved_item_level_only, approved_scored, or blocked. |
| Reviewer signoff | Independent methodological review of the completed dossier before scored release. | Record reviewer name or identifier, role, date, conflicts of interest, required revisions, and final signoff decision. | Reviewer confirms that evidence, preregistration, scoring eligibility, and item release status are aligned. | Signed off, signed off with restrictions, returned for revision, or blocked. |

## Machine-Checkable Results Block

Narrative interpretation belongs in `evidence.*.result_summary`, `retention_table[*].rationale`, `decision.rationale`, and `reviewer_signoff.notes`. Approval evidence belongs in the structured top-level `results` object. A dossier with `dossier_status: approved_item_level_only` or `dossier_status: approved_scored` must include numeric `results`; narrative text alone is not valid approval evidence.

For `approved_scored`, `results.analytic_n` must equal `sample_provenance.confirmation_sample.analytic_n`, the confirmation sample must be fielded, and `results.retained_item_count` must be at least 3 before the item set may contribute to construct, domain, overall, longitudinal, or event-study scoring. `approved_item_level_only` dossiers still require the structured blocks below, but their release consequence must state that construct aggregation is not approved.

Use this shape for approval dossiers:

```json
{
  "results": {
    "analytic_n": 1042,
    "retained_item_count": 4,
    "cfa_fit": {
      "sample": "confirmation_sample",
      "model": "One-factor ordinal CFA for the retained construct item set.",
      "cfi": 0.956,
      "tli": 0.948,
      "rmsea": 0.052,
      "srmr": 0.041
    },
    "reliability": {
      "sample": "confirmation_sample",
      "omega": 0.82,
      "alpha": 0.79,
      "standard_error_of_measurement": 0.28
    },
    "item_statistics": [
      {
        "item_id": "sleep_disruption_ai_news",
        "retained": true,
        "primary_loading": 0.62,
        "max_cross_loading": 0.18,
        "corrected_item_total_correlation": 0.46,
        "floor_rate": 0.21,
        "ceiling_rate": 0.12,
        "adjacent_floor_rate": 0.43,
        "adjacent_ceiling_rate": 0.31,
        "missing_rate": 0.03
      }
    ],
    "dif": {
      "unresolved_practical_dif": false,
      "analyses": [
        {
          "item_id": "sleep_disruption_ai_news",
          "grouping_variable": "gender",
          "method": "Ordinal logistic DIF with multiplicity correction.",
          "effect_size_metric": "delta_pseudo_r2",
          "effect_size": 0.006,
          "practical_threshold": 0.02,
          "statistically_supported": false,
          "practically_meaningful": false,
          "resolved": true
        }
      ]
    },
    "invariance": {
      "method": "Multi-group ordinal CFA",
      "comparison_scope": "Age, gender, education, and prior AI exposure groups.",
      "metric_delta_cfi": -0.006,
      "metric_delta_rmsea": 0.006,
      "scalar_delta_cfi": -0.008,
      "scalar_delta_rmsea": 0.007
    },
    "external_validity": {
      "convergent": {
        "variable": "tech_ai_anxiety_comparator_mean",
        "coefficient_metric": "r",
        "coefficient": 0.44,
        "ci_low": 0.38,
        "ci_high": 0.50,
        "direction_matches": true,
        "passes_threshold": true
      },
      "discriminant": {
        "variable": "general_anxiety_2item_mean",
        "coefficient_metric": "latent_correlation",
        "coefficient": 0.42,
        "ci_low": 0.34,
        "ci_high": 0.50,
        "direction_matches": true,
        "passes_threshold": true
      },
      "criterion": {
        "variable": "ai_avoidance_intention_6m",
        "coefficient_metric": "standardized_beta",
        "coefficient": 0.26,
        "ci_low": 0.17,
        "ci_high": 0.35,
        "direction_matches": true,
        "passes_threshold": true
      },
      "incremental_validity": {
        "variable": "ai_avoidance_intention_6m",
        "coefficient_metric": "adjusted_r2_delta",
        "coefficient": 0.023,
        "ci_low": 0.014,
        "ci_high": 0.034,
        "direction_matches": true,
        "passes_threshold": true
      }
    }
  }
}
```

The approval validator checks the structured block against `docs/psychometric_validation_protocol.md`: omega at least 0.70, CFA CFI and TLI at least 0.90, RMSEA and SRMR no greater than 0.08, retained item loading at least 0.50, corrected item-total correlation at least 0.30, floor and ceiling rates no greater than 0.70, adjacent floor and ceiling rates no greater than 0.85, confirmation missingness no greater than 0.10, invariance deltas within protocol bounds, external-validity coefficients passing their registered thresholds, and no unresolved practical DIF.

## External Validity Decision Table

Complete this table for every construct, domain, or overall score proposed for `approved_scored` status. Item-level-only dossiers may include the table when relevant, but missing external validity evidence must be recorded as a scoring limitation rather than ignored.

| Score or construct | Validity claim | Comparator or criterion variable | Expected direction and magnitude | Observed estimate | 95% confidence interval | Pass or fail threshold | Reviewer decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Economic/vocational ANX score | Convergent validity | `tech_ai_anxiety_comparator_mean` | Positive, moderate association, expected `r` or standardized beta 0.30 to 0.60. |  |  | Pass if direction is positive, confidence interval excludes zero, and magnitude is not below the preregistered minimum. |  |
| Epistemic trust ANX score | Convergent validity | `tech_ai_anxiety_comparator_mean` | Positive, moderate association, expected `r` or standardized beta 0.30 to 0.60. |  |  | Pass if direction is positive, confidence interval excludes zero, and magnitude is not below the preregistered minimum. |  |
| Candidate ANX score | Discriminant validity from general anxiety | `general_anxiety_2item_mean` | Positive but weaker than the association with the AI and technology anxiety comparator, expected 0.10 to 0.35. |  |  | Pass if the general-anxiety association is weaker than the AI and technology comparator association or the reviewer accepts a preregistered construct-specific justification. |  |
| Economic versus epistemic ANX scores | Discriminant validity between ANX constructs | Latent or corrected economic and epistemic construct association | Positive but below 0.80, with a two-factor model preferred to a one-factor model. |  |  | Pass if construct association is below 0.80 and measurement-model comparison supports separability. |  |
| Candidate ANX score | Criterion validity | `ai_avoidance_intention_6m` | Positive association. |  |  | Pass if direction is positive and the estimate is practically interpretable under the preregistered model. |  |
| Candidate ANX score | Criterion validity | `ai_adoption_intention_6m` | Negative or weaker than avoidance association. |  |  | Pass if the result matches the preregistered directional expectation or is explained by AI exposure and usefulness covariates without undermining the score interpretation. |  |
| Candidate ANX score | Criterion validity | `ai_regulation_support_high_impact` | Positive association. |  |  | Pass if direction is positive and the estimate is practically interpretable under the preregistered model. |  |
| Candidate ANX score | Incremental validity | Avoidance and regulation-support models after demographics, AI exposure, and `general_anxiety_2item_mean` | Positive incremental prediction beyond the covariate block. |  |  | Pass if change in adjusted `R^2` is at least 0.01, or if the ordinal or generalized model shows a standardized coefficient excluding zero and an odds ratio of at least 1.20 per standard deviation. |  |

## Release Decision Rules

Set `validation.scoring_eligible: true` only when the dossier supports `psychometric_decision: approved_scored` and the item record also has `release_status: approved_scored`. Items marked `exemplar`, `development_only`, `approved_item_level_only`, or `blocked` must have `validation.scoring_eligible: false`.

An `approved_item_level_only` item may be reported descriptively at the item level when the preregistration allows that use, but it must not contribute to construct, domain, or overall ANX scoring. A `blocked` item must not be administered as part of a public benchmark release unless the release documentation explicitly labels it as excluded from scoring and explains the reason for retaining the record.

## Archival Requirements

Completed dossiers must be immutable after release except for clearly versioned corrections. Any correction that changes a psychometric decision, scoring eligibility, comparison scope, or reviewer signoff requires an updated item version or a documented release patch that preserves respondent-level interpretability.
