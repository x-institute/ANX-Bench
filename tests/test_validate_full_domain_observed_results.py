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
    / "observed_wave8_results.template.json"
)
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_full_domain_observed_results.py"

spec = importlib.util.spec_from_file_location("validate_full_domain_observed_results", VALIDATOR_PATH)
validate_full_domain_observed_results = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_full_domain_observed_results"] = validate_full_domain_observed_results
spec.loader.exec_module(validate_full_domain_observed_results)


def _template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _write_temp(payload: dict) -> Path:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with handle:
        json.dump(payload, handle)
    return Path(handle.name)


def _passing_observed_results() -> dict:
    ledger = _template()
    ledger["result_status"] = "completed"
    ledger["evidence_date"] = "2026-06-16"
    ledger["outcome_inspection"].update(
        {
            "preregistered_inputs_locked_at_utc": "2026-06-15T13:00:00Z",
            "split_assignment_completed_at_utc": "2026-06-15T14:00:00Z",
            "first_outcome_inspection_at_utc": "2026-06-15T15:00:00Z",
            "assigned_before_outcome_inspection": True,
            "no_post_hoc_threshold_or_claim_changes": True,
        }
    )
    ledger["sample_exclusion_flow"].update(
        {
            "started_n": 2310,
            "consented_eligible_n": 2250,
            "achieved_eligible_n": 2200,
            "weighted_descriptive_n": 2100.0,
            "unweighted_analytic_n": 2100,
            "final_analytic_n": 2100,
            "reported_by_required_subgroups": True,
        }
    )
    ledger["sample_exclusion_flow"]["exclusions"].update(
        {
            "declined_or_withdrawn_n": 10,
            "under_18_n": 10,
            "non_us_n": 12,
            "non_english_or_assisted_n": 8,
            "duplicate_n": 8,
            "vendor_fraud_n": 9,
            "attention_check_failed_n": 12,
            "scenario_comprehension_failed_n": 8,
            "full_domain_attribution_failed_n": 7,
            "fast_completion_n": 6,
            "excessive_anx_missingness_n": 3,
            "straightline_plus_quality_failure_n": 3,
            "nonunderstanding_n": 2,
            "platform_order_error_n": 2,
            "total_excluded_n": 100,
        }
    )
    ledger["split_ids"].update(
        {
            "split_assignment_seed_id": "wave8_split_seed_sha256_6b2a",
            "efa_split_id": "wave8_efa_split_v1",
            "cfa_split_id": "wave8_cfa_split_v1",
            "efa_respondent_ids": ["restricted://wave8/splits/efa_ids.sha256"],
            "cfa_respondent_ids": ["restricted://wave8/splits/cfa_ids.sha256"],
            "assigned_before_outcome_inspection": True,
        }
    )
    ledger["split_sample"].update(
        {
            "efa_n": 1050,
            "cfa_n": 1050,
            "stratified_by_sample_source_device_order": True,
            "full_sample_descriptive_only": True,
        }
    )
    for index, item_id in enumerate(ledger["frozen_item_ids"]):
        ledger["item_distributions"][item_id].update(
            {
                "n_administered": 2100,
                "n_observed": 2075,
                "missing_n": 25,
                "missing_rate": 0.0119,
                "response_counts": {"1": 280, "2": 395, "3": 520, "4": 510, "5": 370},
                "response_proportions": {"1": 0.135, "2": 0.190, "3": 0.251, "4": 0.246, "5": 0.178},
                "single_category_concentration": 0.251,
                "two_adjacent_category_concentration": 0.497,
                "mean": 3.14 + (index % 3) * 0.03,
                "sd": 1.18,
            }
        )
    for domain in ledger["domain_summaries"].values():
        domain.update(
            {
                "retained_item_ids": domain["administered_item_ids"],
                "analytic_n": 2100,
                "mean": 3.12,
                "sd": 0.82,
                "omega": 0.82,
                "minimum_discrimination": 0.72,
                "unresolved_material_dif_item_count": 0,
                "invariance_supported": True,
                "bridge_readiness_decision": "pass",
            }
        )
    ledger["model_output_pointers"] = {
        "efa_output": "restricted://wave8/outputs/efa_seven_domain.json",
        "cfa_output": "restricted://wave8/outputs/cfa_seven_domain.json",
        "omega_output": "restricted://wave8/outputs/domain_omega.json",
        "irt_output": "restricted://wave8/outputs/graded_response_irt.json",
        "dif_output": "restricted://wave8/outputs/dif_screen.json",
        "invariance_output": "restricted://wave8/outputs/invariance.json",
        "latent_correlation_output": "restricted://wave8/outputs/latent_correlations.json",
        "somatic_anchor_drift_output": "restricted://wave8/outputs/somatic_anchor_drift.json",
        "aggregate_readiness_output": "restricted://wave8/outputs/aggregate_readiness.json",
        "software_session_lock": "restricted://wave8/outputs/session_lock.txt",
    }
    ledger["model_fit_outputs"]["efa"].update(
        {
            "parallel_analysis_factor_count": 7,
            "seven_domain_solution_interpretable": True,
            "minimum_primary_loading": 0.54,
            "maximum_cross_loading": 0.24,
            "maximum_residual_local_dependence": 0.16,
            "heywood_case_count": 0,
            "unordered_threshold_item_count": 0,
        }
    )
    ledger["model_fit_outputs"]["cfa"].update(
        {
            "correlated_seven_factor_cfi": 0.962,
            "correlated_seven_factor_tli": 0.955,
            "correlated_seven_factor_rmsea": 0.049,
            "rmsea_upper_90": 0.061,
            "srmr": 0.052,
            "minimum_standardized_loading": 0.53,
            "maximum_abs_residual_correlation": 0.14,
            "better_than_unidimensional": True,
            "better_than_collapsed_domain_models": True,
        }
    )
    ledger["model_fit_outputs"]["omega"].update(
        {
            "minimum_domain_omega": 0.80,
            "all_domains_at_or_above_0_70": True,
            "all_domains_at_or_above_0_80": True,
        }
    )
    ledger["model_fit_outputs"]["irt"].update(
        {
            "model_converged": True,
            "minimum_discrimination": 0.72,
            "monotonic_threshold_violations": 0,
            "material_local_dependence_detected": False,
            "central_80_information_stable": True,
            "maximum_linking_se": 0.11,
        }
    )
    ledger["model_fit_outputs"]["latent_correlations"].update(
        {
            "minimum_abs_pairwise": 0.35,
            "maximum_abs_pairwise": 0.55,
            "confidence_intervals_reported": True,
            "positive_theoretically_coherent": True,
            "weight_and_exclusion_sensitivity_stable": True,
        }
    )
    ledger["model_fit_outputs"]["aggregate_readiness"].update(
        {
            "omega_hierarchical": 0.56,
            "explained_common_variance": 0.54,
            "domain_specific_factors_retain_interpretable_variance": True,
            "readiness_label": "later_aggregate_readiness_review_supported",
        }
    )
    ledger["dif_invariance_summaries"]["dif"].update(
        {
            "max_fdr_q_for_flagged_items": 0.071,
            "max_pseudo_r2_delta": 0.013,
            "max_expected_score_difference_sd": 0.07,
            "rank_order_impact_detected": False,
            "threshold_shift_material_impact_detected": False,
            "material_unresolved_dif_item_count": 0,
        }
    )
    ledger["dif_invariance_summaries"]["invariance"].update(
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
        }
    )
    ledger["anchor_drift_outputs"].update(
        {
            "somatic_anchor_item_drifts": {
                "sleep_disruption_ai_news": 0.09,
                "body_vigilance_model_release": 0.12,
                "background_dread_ai_progress": 0.10,
                "avoidance_after_ai_capability_demo": 0.11,
            },
            "mean_abs_drift_sd": 0.105,
            "max_single_item_abs_drift_sd": 0.12,
            "source_anchor_use_blocked": False,
        }
    )
    for key, summary in ledger["sensitivity_summaries"].items():
        summary.update(
            {
                "analysis_output_pointer": f"restricted://wave8/outputs/{key}.json",
                "maximum_abs_domain_mean_shift_sd": 0.04,
                "maximum_abs_loading_shift": 0.03,
                "decision_changed": False,
                "summary": "Sensitivity analysis preserved the preregistered bridge-readiness decision and did not alter claim limits.",
            }
        )
    ledger["analyst_signoff"].update(
        {
            "name": "analysis_lead_hash_2026w08",
            "signed_at_utc": "2026-06-16T16:00:00Z",
        }
    )
    ledger["reviewer_signoff"].update(
        {
            "name": "psychometric_reviewer_hash_2026w08",
            "signed_at_utc": "2026-06-16T18:00:00Z",
        }
    )
    return ledger


class FullDomainObservedResultsValidatorTests(unittest.TestCase):
    def assert_validates(self, ledger: dict) -> None:
        path = _write_temp(ledger)
        try:
            validate_full_domain_observed_results.validate_full_domain_observed_results(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)

    def assert_fails(self, ledger: dict, expected_text: str) -> None:
        path = _write_temp(ledger)
        try:
            with self.assertRaises(
                validate_full_domain_observed_results.FullDomainObservedResultsError
            ) as raised:
                validate_full_domain_observed_results.validate_full_domain_observed_results(path, repo_root=REPO_ROOT)
        finally:
            path.unlink(missing_ok=True)
        self.assertIn(expected_text, str(raised.exception))

    def test_passing_observed_ledger_validates(self) -> None:
        self.assert_validates(_passing_observed_results())

    def test_wrong_item_set_fails(self) -> None:
        ledger = _passing_observed_results()
        ledger["frozen_item_ids"][-1] = "non_frozen_wave8_item"
        self.assert_fails(ledger, "frozen_item_ids")

    def test_missing_post_hoc_outcome_inspection_timing_fails(self) -> None:
        ledger = _passing_observed_results()
        ledger["outcome_inspection"]["first_outcome_inspection_at_utc"] = None
        self.assert_fails(ledger, "outcome_inspection/first_outcome_inspection_at_utc")

    def test_underpowered_analytic_n_fails(self) -> None:
        ledger = _passing_observed_results()
        ledger["sample_exclusion_flow"]["final_analytic_n"] = 1999
        self.assert_fails(ledger, "sample_exclusion_flow/final_analytic_n")

    def test_accidental_scoring_authorization_fails(self) -> None:
        ledger = _passing_observed_results()
        ledger["claim_limits"]["overall_anx_score_authorized"] = True
        self.assert_fails(ledger, "claim_limits/overall_anx_score_authorized")


if __name__ == "__main__":
    unittest.main()
