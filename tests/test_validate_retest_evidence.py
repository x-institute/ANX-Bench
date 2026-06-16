import importlib.util
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = (
    REPO_ROOT
    / "validation"
    / "v0.3"
    / "somatic_ambient_retest"
    / "wave3_retest_evidence.template.json"
)
OBSERVED_PATH = (
    REPO_ROOT
    / "validation"
    / "v0.3"
    / "somatic_ambient_retest"
    / "wave3_retest_evidence.json"
)
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_retest_evidence.py"

spec = importlib.util.spec_from_file_location("validate_retest_evidence", VALIDATOR_PATH)
validate_retest_evidence = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_retest_evidence"] = validate_retest_evidence
spec.loader.exec_module(validate_retest_evidence)


def _template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _observed() -> dict:
    return json.loads(OBSERVED_PATH.read_text(encoding="utf-8"))


def _write_temp(payload: dict) -> Path:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with handle:
        json.dump(payload, handle)
    return Path(handle.name)


def _complete_passing_evidence() -> dict:
    evidence = _template()
    evidence["linkage_counts"] = {
        "wave1_eligible_with_recontact_permission_n": 780,
        "invited_n": 780,
        "bounced_or_unreachable_n": 20,
        "started_retest_n": 650,
        "consented_n": 640,
        "complete_before_exclusions_n": 620,
        "unique_linked_pairs_n": 612,
        "ambiguous_or_duplicate_link_excluded_n": 8,
        "complete_primary_window_pairs_n": 560,
        "timing_sensitivity_pairs_n": 42,
        "final_primary_analytic_pairs_n": 540,
    }
    evidence["exclusion_flow"] = {
        "excluded_no_retest_consent_n": 10,
        "excluded_unmatched_or_nonunique_link_n": 8,
        "excluded_outside_primary_window_n": 42,
        "excluded_attention_check_n": 12,
        "excluded_comprehension_check_n": 8,
        "excluded_somatic_attribution_check_n": 6,
        "excluded_fast_completion_n": 5,
        "excluded_straightline_plus_qc_failure_n": 3,
        "excluded_missing_or_invalid_retest_item_n": 4,
        "excluded_vendor_duplicate_fraud_bot_n": 2,
        "excluded_self_reported_nonunderstanding_n": 0,
        "total_excluded_primary_n": 100,
    }
    evidence["attrition_diagnostics"].update(
        {
            "max_absolute_standardized_mean_difference": 0.08,
            "max_absolute_weighted_percentage_point_difference": 4.2,
            "wave1_construct_mean_difference_points": 0.08,
            "wave1_construct_mean_difference_sd": 0.12,
            "flagged_covariates": [],
            "attrition_sensitive": False,
            "attrition_adjusted_weighting_applied": True,
            "decision": "pass",
        }
    )
    evidence["icc_2_1"].update(
        {
            "analytic_n": 540,
            "estimate": 0.74,
            "ci_95_lower": 0.64,
            "ci_95_upper": 0.82,
            "bootstrap_resamples": 2000,
            "weighted_sensitivity_estimate": 0.73,
            "decision": "pass",
        }
    )
    evidence["mean_change"].update(
        {
            "weighted_wave1_mean": 2.72,
            "weighted_retest_mean": 2.68,
            "weighted_mean_change": -0.04,
            "robust_standard_error": 0.03,
            "ci_95_lower": -0.1,
            "ci_95_upper": 0.02,
            "standardized_response_mean": -0.06,
            "decision": "pass",
        }
    )
    for item in evidence["item_stability"]:
        item.update(
            {
                "paired_item_n": 540,
                "weighted_mean_change": -0.03,
                "unweighted_stability_correlation": 0.58,
                "weighted_exact_agreement": 0.48,
                "weighted_adjacent_agreement": 0.88,
                "weighted_two_or_more_category_move_share": 0.11,
                "missing_or_unusable_retest_rate": 0.04,
                "decision": "pass",
            }
        )
    evidence["longitudinal_invariance"].update(
        {
            "configural_converged": True,
            "configural_one_factor_preserved": True,
            "metric_delta_cfi": -0.006,
            "metric_delta_rmsea": 0.008,
            "scalar_delta_cfi": -0.007,
            "scalar_delta_rmsea": 0.009,
            "max_expected_construct_score_impact": 0.06,
            "max_same_item_residual_correlation": 0.14,
            "status_label": "longitudinal_invariance_passed",
            "decision": "pass",
        }
    )
    evidence["panel_conditioning_sensitivity"].update(
        {
            "excluded_conditioning_n": 44,
            "conditioning_excluded_icc": 0.72,
            "conditioning_excluded_weighted_mean_change": -0.02,
            "absolute_mean_change_difference": 0.02,
            "panel_conditioning_sensitive": False,
            "decision": "pass",
        }
    )
    evidence["decision_table"] = {
        "construct_repeatability_decision": "pass",
        "item_level_failed_item_count": 0,
        "item_level_caution_item_ids": [],
        "overall_retest_evidence_decision": "pass",
        "claim_authorized": True,
    }
    return evidence


class RetestEvidenceValidatorTests(unittest.TestCase):
    def assert_validates(self, evidence: dict) -> None:
        path = _write_temp(evidence)
        try:
            validate_retest_evidence.validate_retest_evidence(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)

    def assert_fails(self, evidence: dict, expected_text: str) -> None:
        path = _write_temp(evidence)
        try:
            with self.assertRaises(validate_retest_evidence.RetestEvidenceError) as raised:
                validate_retest_evidence.validate_retest_evidence(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)
        self.assertIn(expected_text, str(raised.exception))

    def test_template_structure_is_valid_with_null_observed_results(self) -> None:
        self.assert_validates(_template())

    def test_observed_v032_retest_packet_validates_and_authorizes_repeatability(self) -> None:
        evidence = _observed()

        self.assert_validates(evidence)
        self.assertEqual("pass", evidence["decision_table"]["overall_retest_evidence_decision"])
        self.assertTrue(evidence["decision_table"]["claim_authorized"])
        self.assertEqual("v0.3.1", evidence["benchmark_version"])
        self.assertEqual("no_event", evidence["event_id"])

    def test_null_template_cannot_authorize_v032_repeatability_claim(self) -> None:
        evidence = _template()

        self.assert_validates(evidence)
        self.assertIsNone(evidence["decision_table"]["overall_retest_evidence_decision"])
        self.assertIsNone(evidence["decision_table"]["claim_authorized"])
        self.assertTrue(evidence["evidence_id"].endswith("_template"))

    def test_completed_passing_evidence_is_valid(self) -> None:
        self.assert_validates(_complete_passing_evidence())

    def test_missing_icc_field_fails(self) -> None:
        evidence = _template()
        del evidence["icc_2_1"]["estimate"]
        self.assert_fails(evidence, "missing required property 'estimate'")

    def test_event_study_misuse_fails(self) -> None:
        evidence = _template()
        evidence["event_id"] = "model_release_event"
        evidence["reporting_restrictions"]["event_study_claim_permitted"] = True
        self.assert_fails(evidence, "event_id")

    def test_wrong_item_ids_fail(self) -> None:
        evidence = _template()
        evidence["frozen_item_ids"][0] = "ambient_bodily_unease"
        evidence["item_stability"][0]["item_id"] = "ambient_bodily_unease"
        self.assert_fails(evidence, "four approved")

    def test_inconsistent_pass_fail_decision_fails(self) -> None:
        evidence = _complete_passing_evidence()
        evidence["icc_2_1"]["estimate"] = 0.62
        evidence["icc_2_1"]["decision"] = "pass"
        self.assert_fails(evidence, "icc_2_1/decision")


if __name__ == "__main__":
    unittest.main()
