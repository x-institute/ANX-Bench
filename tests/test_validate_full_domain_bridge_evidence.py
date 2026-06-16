import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = (
    REPO_ROOT
    / "validation"
    / "v0.8"
    / "full_domain_bridge"
    / "wave8_full_domain_bridge_evidence.template.json"
)
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_full_domain_bridge_evidence.py"

spec = importlib.util.spec_from_file_location("validate_full_domain_bridge_evidence", VALIDATOR_PATH)
validate_full_domain_bridge_evidence = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_full_domain_bridge_evidence"] = validate_full_domain_bridge_evidence
spec.loader.exec_module(validate_full_domain_bridge_evidence)


def _template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _write_temp(payload: dict) -> Path:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with handle:
        json.dump(payload, handle)
    return Path(handle.name)


def _passing_evidence() -> dict:
    evidence = _template()
    evidence["evidence_id"] = "anx_us_2026w08_full_domain_bridge_observed_pass"
    evidence["evidence_status"] = "observed"
    evidence["study_ids"] = {
        "fielding_study_id": "fielding_2026w08_public_hash_1",
        "efa_split_id": "split_2026w08_efa_hash_1",
        "cfa_split_id": "split_2026w08_cfa_hash_1",
        "restricted_data_study_id": "restricted_2026w08_hash_1",
    }
    evidence["analytic_n"].update(
        {
            "started_n": 2240,
            "achieved_eligible_n": 2070,
            "final_analytic_n": 2000,
            "decision": "pass",
        }
    )
    evidence["exclusion_flow"].update(
        {
            "declined_or_withdrawn_n": 7,
            "under_18_n": 12,
            "non_us_n": 18,
            "non_english_or_assisted_n": 9,
            "duplicate_n": 11,
            "vendor_fraud_n": 14,
            "attention_check_failed_n": 24,
            "scenario_comprehension_failed_n": 19,
            "full_domain_attribution_failed_n": 17,
            "fast_completion_n": 16,
            "excessive_anx_missingness_n": 10,
            "straightline_plus_quality_failure_n": 8,
            "nonunderstanding_n": 4,
            "platform_order_error_n": 1,
            "total_excluded_n": 170,
            "reported_by_required_subgroups": True,
            "decision": "pass",
        }
    )
    evidence["split_sample"].update(
        {
            "randomized_before_outcome_inspection": True,
            "stratified_by_sample_source_device_order": True,
            "efa_n": 1000,
            "cfa_n": 1000,
            "full_sample_reported_as_descriptive_only": True,
            "decision": "pass",
        }
    )
    for gate in evidence["domain_gates"]:
        gate.update(
            {
                "retained_item_count": gate["minimum_required_items"],
                "omega": 0.82,
                "all_item_discriminations_at_or_above_0_65": True,
                "unresolved_material_dif_item_count": 0,
                "invariance_supported_for_key_groups": True,
                "decision": "pass",
            }
        )
    evidence["efa"].update(
        {
            "parallel_analysis_factor_count": 7,
            "seven_domain_solution_interpretable": True,
            "minimum_primary_loading": 0.54,
            "maximum_cross_loading": 0.24,
            "minimum_primary_cross_loading_gap": 0.27,
            "heywood_case_count": 0,
            "unordered_threshold_item_count": 0,
            "maximum_residual_local_dependence": 0.16,
            "decision": "pass",
        }
    )
    evidence["cfa"].update(
        {
            "correlated_seven_factor_cfi": 0.962,
            "correlated_seven_factor_tli": 0.955,
            "correlated_seven_factor_rmsea": 0.049,
            "rmsea_upper_90": 0.061,
            "srmr": 0.052,
            "minimum_standardized_loading": 0.53,
            "single_low_loading_exception_used": False,
            "single_low_loading_exception_rationale_documented": False,
            "maximum_abs_residual_correlation": 0.14,
            "better_than_unidimensional": True,
            "better_than_collapsed_domain_models": True,
            "decision": "pass",
        }
    )
    evidence["omega"].update(
        {
            "domain_omega": {
                "somatic_ambient": 0.84,
                "economic_vocational": 0.83,
                "epistemic": 0.82,
                "relational": 0.81,
                "existential_identity": 0.80,
                "autonomy_surveillance": 0.82,
                "safety_catastrophic": 0.83,
            },
            "minimum_domain_omega": 0.80,
            "all_domains_at_or_above_0_70": True,
            "all_domains_at_or_above_0_80": True,
            "decision": "pass",
        }
    )
    evidence["irt"].update(
        {
            "model_converged": True,
            "minimum_discrimination": 0.72,
            "monotonic_threshold_violations": 0,
            "material_local_dependence_detected": False,
            "central_80_information_stable": True,
            "maximum_linking_se": 0.11,
            "official_theta_scoring_introduced": False,
            "decision": "pass",
        }
    )
    evidence["dif"].update(
        {
            "max_fdr_q_for_flagged_items": 0.071,
            "max_pseudo_r2_delta": 0.013,
            "max_expected_score_difference_sd": 0.07,
            "rank_order_impact_detected": False,
            "threshold_shift_material_impact_detected": False,
            "material_unresolved_dif_item_count": 0,
            "subgroup_comparison_blocks": [],
            "decision": "pass",
        }
    )
    evidence["invariance"].update(
        {
            "configural_all_converged": True,
            "minimum_metric_delta_cfi": -0.006,
            "maximum_metric_delta_rmsea": 0.009,
            "minimum_scalar_or_threshold_delta_cfi": -0.008,
            "maximum_scalar_or_threshold_delta_rmsea": 0.011,
            "partial_invariance_used": False,
            "partial_invariance_documented_before_interpretation": False,
            "domain_ordering_changed_by_noninvariance": False,
            "failed_key_comparison_count": 0,
            "decision": "pass",
        }
    )
    correlations = {
        key: value
        for key, value in zip(
            evidence["latent_correlations"]["pairwise_domain_correlations"],
            [
                0.42,
                0.45,
                0.37,
                0.39,
                0.41,
                0.48,
                0.52,
                0.36,
                0.44,
                0.46,
                0.50,
                0.38,
                0.43,
                0.47,
                0.49,
                0.35,
                0.40,
                0.46,
                0.42,
                0.51,
                0.55,
            ],
        )
    }
    evidence["latent_correlations"].update(
        {
            "pairwise_domain_correlations": correlations,
            "minimum_abs_pairwise": 0.35,
            "maximum_abs_pairwise": 0.55,
            "confidence_intervals_reported": True,
            "positive_theoretically_coherent": True,
            "weight_and_exclusion_sensitivity_stable": True,
            "decision": "pass",
        }
    )
    evidence["somatic_anchor_drift"].update(
        {
            "mean_abs_drift_sd": 0.11,
            "max_single_item_abs_drift_sd": 0.21,
            "source_anchor_use_blocked": False,
            "decision": "pass",
        }
    )
    evidence["aggregate_readiness"].update(
        {
            "omega_hierarchical": 0.56,
            "explained_common_variance": 0.54,
            "domain_specific_factors_retain_interpretable_variance": True,
            "readiness_label": "later_aggregate_readiness_review_supported",
        }
    )
    evidence["final_decision"] = {
        "bridge_decision": "bridge_supported_for_later_aggregate_readiness_review",
        "release_blocking": False,
        "later_proposal_permitted": True,
        "scoring_authorized": False,
        "decision_rationale": "All preregistered Wave 8 bridge gates pass. This supports only a later separately preregistered aggregate-readiness review and does not calculate or permit an official score.",
    }
    return evidence


class FullDomainBridgeEvidenceValidatorTests(unittest.TestCase):
    def assert_schema_validates(self, evidence: dict) -> None:
        schema = validate_full_domain_bridge_evidence.load_json(
            REPO_ROOT / "schema" / "full_domain_bridge_evidence.schema.json"
        )
        issues = validate_full_domain_bridge_evidence.validate_with_jsonschema(evidence, schema)
        self.assertEqual([], [issue.render() for issue in issues])

    def assert_validates(self, evidence: dict) -> None:
        path = _write_temp(evidence)
        try:
            validate_full_domain_bridge_evidence.validate_full_domain_bridge_evidence(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)

    def assert_fails(self, evidence: dict, expected_text: str) -> None:
        path = _write_temp(evidence)
        try:
            with self.assertRaises(
                validate_full_domain_bridge_evidence.FullDomainBridgeEvidenceError
            ) as raised:
                validate_full_domain_bridge_evidence.validate_full_domain_bridge_evidence(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)
        self.assertIn(expected_text, str(raised.exception))

    def test_template_structure_validates_without_authorizing_claims(self) -> None:
        evidence = _template()
        self.assert_schema_validates(evidence)
        self.assert_validates(evidence)
        self.assertIsNone(evidence["final_decision"]["bridge_decision"])
        self.assertIsNone(evidence["final_decision"]["scoring_authorized"])
        self.assertEqual([], evidence["scoring_authorization"]["official_scored_items"])
        self.assertFalse(evidence["scoring_authorization"]["new_domain_scores_authorized"])
        self.assertFalse(evidence["scoring_authorization"]["cross_domain_score_authorized"])
        self.assertFalse(evidence["scoring_authorization"]["overall_anx_score_authorized"])

    def test_passing_observed_evidence_validates(self) -> None:
        self.assert_schema_validates(_passing_evidence())
        self.assert_validates(_passing_evidence())

    def test_low_n_blocks(self) -> None:
        evidence = _passing_evidence()
        evidence["analytic_n"]["final_analytic_n"] = 1999
        evidence["split_sample"]["efa_n"] = 1000
        evidence["split_sample"]["cfa_n"] = 999
        evidence["analytic_n"]["decision"] = "pass"
        self.assert_fails(evidence, "analytic_n/decision")

    def test_bad_cfa_fit_blocks(self) -> None:
        evidence = _passing_evidence()
        evidence["cfa"]["correlated_seven_factor_cfi"] = 0.949
        evidence["cfa"]["decision"] = "pass"
        self.assert_fails(evidence, "cfa/decision")

    def test_over_0_80_latent_correlation_blocks(self) -> None:
        evidence = _passing_evidence()
        first_pair = next(iter(evidence["latent_correlations"]["pairwise_domain_correlations"]))
        evidence["latent_correlations"]["pairwise_domain_correlations"][first_pair] = 0.81
        evidence["latent_correlations"]["maximum_abs_pairwise"] = 0.81
        evidence["latent_correlations"]["decision"] = "pass"
        self.assert_fails(evidence, "latent_correlations/decision")

    def test_somatic_anchor_drift_blocks(self) -> None:
        evidence = _passing_evidence()
        evidence["somatic_anchor_drift"]["mean_abs_drift_sd"] = 0.21
        evidence["somatic_anchor_drift"]["decision"] = "pass"
        self.assert_fails(evidence, "somatic_anchor_drift/decision")

    def test_unauthorized_scoring_fails(self) -> None:
        evidence = _passing_evidence()
        evidence["scoring_authorization"]["overall_anx_score_authorized"] = True
        evidence["final_decision"]["decision_rationale"] = "This observed evidence authorizes an official overall ANX score."
        self.assert_fails(evidence, "scoring_authorization/overall_anx_score_authorized")


if __name__ == "__main__":
    unittest.main()
