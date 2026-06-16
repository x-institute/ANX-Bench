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
    / "v0.7"
    / "cross_domain_bridge"
    / "wave7_bridge_evidence.template.json"
)
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_cross_domain_bridge_evidence.py"

spec = importlib.util.spec_from_file_location("validate_cross_domain_bridge_evidence", VALIDATOR_PATH)
validate_cross_domain_bridge_evidence = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_cross_domain_bridge_evidence"] = validate_cross_domain_bridge_evidence
spec.loader.exec_module(validate_cross_domain_bridge_evidence)


def _template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _write_temp(payload: dict) -> Path:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with handle:
        json.dump(payload, handle)
    return Path(handle.name)


def _passing_evidence() -> dict:
    evidence = _template()
    evidence["evidence_id"] = "anx_us_2026w07_cross_domain_bridge_observed_pass"
    evidence["evidence_status"] = "observed"
    evidence["analytic_n"].update(
        {
            "achieved_eligible_n": 1538,
            "final_analytic_n": 1488,
            "independent_from_wave5_wave6": True,
            "decision": "pass",
        }
    )
    evidence["exclusion_flow"].update(
        {
            "started_n": 1680,
            "consented_eligible_n": 1538,
            "excluded_under_18_n": 8,
            "excluded_non_us_n": 11,
            "excluded_non_english_or_assisted_n": 4,
            "excluded_duplicate_n": 9,
            "excluded_vendor_fraud_n": 7,
            "excluded_attention_check_n": 29,
            "excluded_cross_domain_attribution_check_n": 18,
            "excluded_scenario_comprehension_n": 15,
            "excluded_fast_completion_n": 14,
            "excluded_excessive_anx_missingness_n": 10,
            "excluded_straightline_plus_quality_failure_n": 8,
            "excluded_withdrawal_n": 3,
            "excluded_nonunderstanding_n": 6,
            "total_excluded_n": 142,
            "non_exclusion_sensitivity_flags_retained": True,
            "reported_by_required_subgroups": True,
            "decision": "pass",
        }
    )
    evidence["factor_model_fit"].update(
        {
            "efa_primary_loading_min": 0.58,
            "efa_secondary_loading_abs_max": 0.22,
            "efa_parallel_analysis_factor_count": 3,
            "three_factor_interpretable": True,
            "correlated_three_factor_cfi": 0.966,
            "correlated_three_factor_rmsea": 0.047,
            "standardized_loading_min": 0.56,
            "unidimensional_model_not_sufficient": True,
            "decision": "pass",
        }
    )
    evidence["omega"].update(
        {
            "somatic_ambient_anxiety": 0.84,
            "economic_vocational_anxiety": 0.82,
            "epistemic_trust_anxiety": 0.81,
            "minimum_domain_omega": 0.81,
            "all_domains_at_or_above_0_70": True,
            "all_domains_at_or_above_0_80": True,
            "decision": "pass",
        }
    )
    evidence["irt_linking"].update(
        {
            "model_converged": True,
            "discrimination_min": 0.78,
            "threshold_ordering_violations": 0,
            "local_dependence_abs_max": 0.14,
            "anchor_drift_abs_mean_sd": 0.11,
            "linking_se_central_80_max": 0.09,
            "official_theta_scoring_introduced": False,
            "decision": "pass",
        }
    )
    evidence["dif"].update(
        {
            "max_fdr_q_for_flagged_items": 0.064,
            "max_pseudo_r2_delta": 0.012,
            "max_expected_score_difference_sd": 0.06,
            "rank_order_impact_detected": False,
            "material_unresolved_dif_item_count": 0,
            "decision": "pass",
        }
    )
    evidence["invariance"].update(
        {
            "configural_all_converged": True,
            "minimum_metric_delta_cfi": -0.006,
            "maximum_metric_delta_rmsea": 0.009,
            "minimum_scalar_delta_cfi": -0.008,
            "maximum_scalar_delta_rmsea": 0.011,
            "failed_key_comparison_count": 0,
            "irt_fallback_used": False,
            "irt_fallback_reviewer_approved": False,
            "decision": "pass",
        }
    )
    evidence["latent_correlations"].update(
        {
            "somatic_economic": 0.48,
            "somatic_epistemic": 0.54,
            "economic_epistemic": 0.62,
            "minimum_abs_pairwise": 0.48,
            "maximum_abs_pairwise": 0.62,
            "confidence_intervals_reported": True,
            "weight_and_exclusion_sensitivity_stable": True,
            "decision": "pass",
        }
    )
    evidence["bifactor_second_order_readiness"].update(
        {
            "model_converged": True,
            "omega_hierarchical": 0.56,
            "explained_common_variance": 0.53,
            "domain_specific_factors_retain_interpretable_variance": True,
            "overall_readiness_decision": "overall_readiness_review_supported",
        }
    )
    evidence["final_decision"] = {
        "bridge_decision": "bridge_supported_for_overall_readiness_review",
        "release_blocking": False,
        "later_proposal_permitted": True,
        "scoring_authorized": False,
        "decision_rationale": "All preregistered Wave 7 bridge gates pass. This permits only a later separately preregistered aggregate-score proposal and does not calculate or authorize a score.",
    }
    return evidence


class CrossDomainBridgeEvidenceValidatorTests(unittest.TestCase):
    def assert_schema_validates(self, evidence: dict) -> None:
        schema = validate_cross_domain_bridge_evidence.load_json(
            REPO_ROOT / "schema" / "cross_domain_bridge_evidence.schema.json"
        )
        issues = validate_cross_domain_bridge_evidence.validate_with_jsonschema(evidence, schema)
        self.assertEqual([], [issue.render() for issue in issues])

    def assert_validates(self, evidence: dict) -> None:
        path = _write_temp(evidence)
        try:
            validate_cross_domain_bridge_evidence.validate_cross_domain_bridge_evidence(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)

    def assert_fails(self, evidence: dict, expected_text: str) -> None:
        path = _write_temp(evidence)
        try:
            with self.assertRaises(
                validate_cross_domain_bridge_evidence.CrossDomainBridgeEvidenceError
            ) as raised:
                validate_cross_domain_bridge_evidence.validate_cross_domain_bridge_evidence(path, repo_root=REPO_ROOT)
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
        self.assertFalse(evidence["scoring_authorization"]["aggregate_scoring_permitted"])
        self.assertFalse(evidence["scoring_authorization"]["cross_domain_score_authorized"])
        self.assertFalse(evidence["scoring_authorization"]["overall_anx_score_authorized"])
        self.assertFalse(evidence["scoring_authorization"]["domain_combined_score_authorized"])

    def test_passing_observed_evidence_validates(self) -> None:
        self.assert_validates(_passing_evidence())

    def test_underpowered_observed_evidence_blocks(self) -> None:
        evidence = _passing_evidence()
        evidence["analytic_n"]["final_analytic_n"] = 1199
        evidence["analytic_n"]["decision"] = "pass"
        self.assert_fails(evidence, "analytic_n/decision")

    def test_high_latent_correlation_blocks(self) -> None:
        evidence = _passing_evidence()
        evidence["latent_correlations"]["economic_epistemic"] = 0.81
        evidence["latent_correlations"]["maximum_abs_pairwise"] = 0.81
        evidence["latent_correlations"]["decision"] = "pass"
        self.assert_fails(evidence, "latent_correlations/decision")

    def test_unresolved_material_dif_blocks(self) -> None:
        evidence = _passing_evidence()
        evidence["dif"]["max_fdr_q_for_flagged_items"] = 0.012
        evidence["dif"]["max_pseudo_r2_delta"] = 0.031
        evidence["dif"]["max_expected_score_difference_sd"] = 0.14
        evidence["dif"]["material_unresolved_dif_item_count"] = 1
        evidence["dif"]["decision"] = "pass"
        self.assert_fails(evidence, "dif/decision")

    def test_accidental_scoring_authorization_fails(self) -> None:
        evidence = _passing_evidence()
        evidence["scoring_authorization"]["overall_anx_score_authorized"] = True
        evidence["final_decision"]["decision_rationale"] = "This bridge evidence authorizes scoring for an official overall ANX score."
        self.assert_fails(evidence, "scoring_authorization/overall_anx_score_authorized")


if __name__ == "__main__":
    unittest.main()
