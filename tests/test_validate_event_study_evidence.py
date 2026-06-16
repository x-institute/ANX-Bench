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
    / "v0.4"
    / "somatic_event_study"
    / "wave4_event_study_evidence.template.json"
)
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_event_study_evidence.py"

spec = importlib.util.spec_from_file_location("validate_event_study_evidence", VALIDATOR_PATH)
validate_event_study_evidence = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_event_study_evidence"] = validate_event_study_evidence
spec.loader.exec_module(validate_event_study_evidence)


def _template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _write_temp(payload: dict) -> Path:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with handle:
        json.dump(payload, handle)
    return Path(handle.name)


def _complete_passing_evidence() -> dict:
    evidence = _template()
    digest = "a" * 64
    evidence["evidence_id"] = "anx_us_2026w04_somatic_event_study_evidence_observed"
    evidence["locked_event_id"] = "anx_us_2026w04_frontier_model_capability_release"
    evidence["registry_lock_proof"] = {
        "registry_version": "v0.4.1-lock1",
        "registry_status": "locked",
        "lock_date": "2026-06-16",
        "event_locked_before_outcome_inspection": True,
        "outcome_inspection_status": "not_inspected_at_lock",
        "registry_sha256": digest,
        "event_record_sha256": "b" * 64,
        "release_blocking_confound_present": False,
    }
    evidence["sample_counts"] = {
        "baseline_primary_nominal_n": 820,
        "followup_primary_nominal_n": 840,
        "baseline_effective_weighted_n": 610.4,
        "followup_effective_weighted_n": 635.2,
        "analytic_exclusions_n": 91,
        "weighting_sensitive": False,
    }
    evidence["primary_estimate"] = {
        "coefficient_name": "beta_post_event",
        "coefficient": 0.22,
        "standard_error": 0.05,
        "ci_95_lower": 0.12,
        "ci_95_upper": 0.32,
        "p_value": 0.004,
        "decision": "pass",
    }
    evidence["pretrend_check"] = {
        "coefficient_name": "late_pre_period",
        "coefficient": 0.03,
        "ci_95_lower": -0.05,
        "ci_95_upper": 0.11,
        "p_value": 0.42,
        "decision": "pass",
    }
    robustness_coefficients = {
        "unweighted_primary_model": 0.18,
        "alternative_weight_trim": 0.17,
        "aware_only_followup": 0.24,
        "exclude_unrelated_personal_crisis": 0.21,
        "exclude_high_general_distress": 0.19,
        "narrow_followup_window": 0.16,
        "placebo_pretrend": 0.03,
        "event_buffer_sensitivity": 0.2,
        "negative_control_outcome": 0.01,
    }
    for check in evidence["robustness_checks"]:
        coefficient = robustness_coefficients[check["check_id"]]
        check.update(
            {
                "coefficient": coefficient,
                "ci_95_lower": coefficient - 0.08,
                "ci_95_upper": coefficient + 0.08,
                "p_value": 0.03 if coefficient >= 0.16 else 0.72,
                "decision": "pass" if check["check_id"] in {
                    "unweighted_primary_model",
                    "alternative_weight_trim",
                    "narrow_followup_window",
                } else "reported",
                "notes": "Observed robustness result archived with the Wave 4 evidence packet.",
            }
        )
    evidence["confounds"] = {
        "release_blocking_confound_present": False,
        "competing_event_review": "No release-blocking competing AI capability or unrelated public crisis event was adjudicated inside the primary window.",
        "adjudication_notes": "Two independent coders reviewed timestamped event sources before outcome inspection and confirmed the locked event-study scope.",
    }
    evidence["claim_decision"] = {
        "primary_threshold_decision": "pass",
        "claim_authorized": True,
        "authorized_claim_language": "event-associated somatic anxiety change",
        "blocked_claims": [
            "causal AI capability effect",
            "overall ANX-Bench score",
            "clinical anxiety or diagnosis",
            "long-term change beyond the preregistered follow-up window",
            "cross-domain ANX movement",
        ],
        "decision_notes": "All locked registry, N, primary coefficient, pretrend, confound, and required robustness gates passed.",
    }
    evidence["reported_claim_text"] = "Wave 4 supports an event-associated somatic anxiety change for the preregistered US English online adult sample and follow-up window."
    return evidence


class EventStudyEvidenceValidatorTests(unittest.TestCase):
    def assert_validates(self, evidence: dict) -> None:
        path = _write_temp(evidence)
        try:
            validate_event_study_evidence.validate_event_study_evidence(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)

    def assert_fails(self, evidence: dict, expected_text: str) -> None:
        path = _write_temp(evidence)
        try:
            with self.assertRaises(validate_event_study_evidence.EventStudyEvidenceError) as raised:
                validate_event_study_evidence.validate_event_study_evidence(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)
        self.assertIn(expected_text, str(raised.exception))

    def test_template_structure_is_valid_with_null_observed_values(self) -> None:
        self.assert_validates(_template())

    def test_completed_passing_evidence_validates(self) -> None:
        self.assert_validates(_complete_passing_evidence())

    def test_low_n_claim_fails(self) -> None:
        evidence = _complete_passing_evidence()
        evidence["sample_counts"]["baseline_primary_nominal_n"] = 740
        self.assert_fails(evidence, "baseline_primary_nominal_n")

    def test_unlocked_registry_claim_fails(self) -> None:
        evidence = _complete_passing_evidence()
        evidence["registry_lock_proof"]["event_locked_before_outcome_inspection"] = False
        self.assert_fails(evidence, "registry lock proof")

    def test_failed_pretrend_claim_fails(self) -> None:
        evidence = _complete_passing_evidence()
        evidence["pretrend_check"]["coefficient"] = 0.14
        evidence["pretrend_check"]["p_value"] = 0.01
        self.assert_fails(evidence, "pretrend")

    def test_overbroad_claim_fails(self) -> None:
        evidence = _complete_passing_evidence()
        evidence["reported_claim_text"] = "The event caused an increase in the overall ANX-Bench score."
        self.assert_fails(evidence, "overbroad")


if __name__ == "__main__":
    unittest.main()
