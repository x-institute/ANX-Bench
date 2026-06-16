import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = (
    REPO_ROOT
    / "validation"
    / "v0.2"
    / "somatic_ambient_anxiety"
    / "observed_wave1_results.json"
)
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_observed_validation_results.py"

spec = importlib.util.spec_from_file_location("validate_observed_validation_results", VALIDATOR_PATH)
validate_observed_validation_results = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_observed_validation_results"] = validate_observed_validation_results
spec.loader.exec_module(validate_observed_validation_results)

FROZEN_SOMATIC_ITEM_IDS = {
    "sleep_disruption_ai_news",
    "body_vigilance_model_release",
    "background_dread_ai_progress",
    "avoidance_after_ai_capability_demo",
}


def _sha256(fill: str) -> str:
    return fill * 64


def _response_distribution(item_id: str) -> dict:
    return {
        "item_id": item_id,
        "n_observed": 100,
        "missing_n": 0,
        "missing_rate": 0.0,
        "counts": {"1": 12, "2": 18, "3": 28, "4": 25, "5": 17},
        "proportions": {"1": 0.12, "2": 0.18, "3": 0.28, "4": 0.25, "5": 0.17},
        "single_category_concentration": 0.28,
        "two_adjacent_category_concentration": 0.53,
    }


def _item_statistic(item_id: str) -> dict:
    return {
        "item_id": item_id,
        "item_version": "v0.2.0",
        "retained": True,
        "response_distribution": _response_distribution(item_id),
        "primary_loading": 0.62,
        "cross_loading": 0.0,
        "communality": 0.39,
        "standardized_loading": 0.68,
        "corrected_item_total_correlation": 0.46,
        "irt_discrimination": 1.2,
        "irt_category_thresholds": [-1.2, -0.2, 0.7, 1.4],
        "thresholds_ordered": True,
        "item_information": {
            "theta_grid": [-2, -1, 0, 1, 2],
            "note": "Item information is archived with the fitted graded-response model.",
        },
    }


def _minimal_observed_results() -> dict:
    item_ids = sorted(FROZEN_SOMATIC_ITEM_IDS)
    item_stats = [_item_statistic(item_id) for item_id in item_ids]
    return {
        "observed_results_schema_version": "v0.1.0",
        "result_id": "somatic_ambient_anxiety_wave1_observed_validation",
        "generated_at_utc": "2026-06-16T00:00:00Z",
        "analysis_plan_path": "analysis/v0.2/somatic_ambient/wave1_analysis_plan.json",
        "analysis_plan_sha256": _sha256("a"),
        "input_data_path": "vendor_restricted/anx_us_2026w02_somatic/wave_response.jsonl",
        "input_data_sha256": _sha256("b"),
        "benchmark_version": "v0.2.2",
        "promotion_target_version": "v0.3.0",
        "study_id": "anx_us_2026w02_somatic",
        "construct_id": "somatic_ambient_anxiety",
        "frozen_item_ids": item_ids,
        "frozen_item_versions": {item_id: "v0.2.0" for item_id in item_ids},
        "contract_checks": {
            "declared_inputs_only": True,
            "required_fields_present": True,
            "item_allowlist_exact": True,
            "item_versions_exact": True,
            "benchmark_version_exact": True,
            "event_id_all_no_event": True,
            "no_output_written_before_contract_pass": True,
        },
        "exclusions": {
            "total_respondents": 120,
            "excluded_respondents": 20,
            "analytic_respondents": 100,
            "by_sample": {
                "development_pilot": {"total": 60, "excluded": 10, "analytic": 50},
                "confirmation_sample": {"total": 60, "excluded": 10, "analytic": 50},
            },
        },
        "scoring": {
            "score_name": "somatic_ambient_anxiety_mean",
            "score_rule": "Respondent mean of observed frozen somatic item response_value values after preregistered exclusions, with no item-response imputation.",
            "analytic_n_development_pilot": 50,
            "analytic_n_confirmation_sample": 50,
        },
        "efa": {
            "sample": "development_pilot",
            "parallel_analysis_factor_count": 1,
            "primary_loadings": {item_id: 0.62 for item_id in item_ids},
            "cross_loadings": {item_id: 0.0 for item_id in item_ids},
            "communalities": {item_id: 0.39 for item_id in item_ids},
            "factor_determinacy": 0.91,
        },
        "cfa": {
            "sample": "confirmation_sample",
            "model": "somatic_ambient_anxiety =~ sleep_disruption_ai_news + body_vigilance_model_release + background_dread_ai_progress + avoidance_after_ai_capability_demo",
            "fit": {"cfi": 0.96, "tli": 0.95, "rmsea": 0.05, "srmr": 0.04},
            "standardized_loadings": {item_id: 0.68 for item_id in item_ids},
        },
        "reliability": {
            "sample": "confirmation_sample",
            "omega": 0.8,
            "alpha": 0.78,
            "corrected_item_total_correlation": {item_id: 0.46 for item_id in item_ids},
            "standard_error_of_measurement": 0.29,
        },
        "irt": {
            "sample": "confirmation_sample",
            "item_parameters": item_stats,
            "local_dependence": {"status": "not_available"},
            "response_pattern_fit": "Fitted graded-response model archived in session-bound run output.",
        },
        "dif": {"status": "completed", "analyses": [], "unresolved_practical_dif": False},
        "invariance": {"status": "not_estimable", "reason": "No grouping variable reached the preregistered minimum cell size."},
        "external_validity": {
            "convergent": {
                "ai_news_exposure_30d": {"n": 50, "coefficient": 0.31, "ci": [0.04, 0.54]},
            },
            "discriminant": {
                "baseline_general_anxiety_2item_mean": {"n": 50, "coefficient": 0.22, "ci": [-0.06, 0.47]},
            },
            "criterion": {
                "ai_information_avoidance_intention_6m": {
                    "status": "completed",
                    "n": 50,
                    "odds_ratio": 1.4,
                    "ci": [1.05, 1.9],
                },
            },
            "incremental_validity": {
                "status": "completed",
                "n": 50,
                "covariate_block": ["baseline_general_anxiety_2item_mean"],
                "adjusted_r_squared_change": 0.03,
                "standardized_coefficient": 0.19,
                "p_value": 0.02,
            },
        },
        "item_statistics": item_stats,
        "retention": {
            "retained_item_count": 4,
            "retained_item_ids": item_ids,
            "item_decisions": [
                {"item_id": item_id, "decision": "retain_pending_reviewer_confirmation"}
                for item_id in item_ids
            ],
        },
        "validation_gates": {
            "cfa_cfi": True,
            "cfa_tli": True,
            "cfa_rmsea": True,
            "cfa_srmr": True,
            "omega": True,
            "minimum_retained_items": True,
            "no_unresolved_meaningful_dif": True,
        },
        "decision": {
            "psychometric_decision": "observed_evidence_ready_for_manual_review",
            "scoring_eligible": False,
            "manual_dossier_promotion_permitted": False,
            "rationale": "This runner produces checksum-bound observed evidence. Scored release still requires manual dossier update, independent review, and a citable release manifest.",
        },
        "session_info": {
            "runtime": "R version 4.4.3",
            "text_sha256": _sha256("c"),
            "packages": [{"name": "psych", "version": "2.4.12"}],
            "session_info_text": "R version 4.4.3 with the frozen ANX-Bench psychometric package set recorded for reproducibility.",
        },
    }


class ObservedWave1ResultsContractTests(unittest.TestCase):
    def assert_schema_valid(self, results: dict) -> None:
        issues = []
        schema = json.loads((REPO_ROOT / "schema" / "observed_validation_results.schema.json").read_text(encoding="utf-8"))
        try:
            from jsonschema import Draft202012Validator
        except ModuleNotFoundError:
            issues.extend(
                issue.render()
                for issue in validate_observed_validation_results.validate_with_jsonschema(results, schema)
            )
            issues.extend(validate_observed_validation_results.validate_hashes(results))
            issues.extend(validate_observed_validation_results.validate_item_consistency(results))
        else:
            validator = Draft202012Validator(schema)
            issues.extend(error.message for error in validator.iter_errors(results))
            issues.extend(issue.render() for issue in validate_observed_validation_results.validate_hashes(results))
            issues.extend(issue.render() for issue in validate_observed_validation_results.validate_item_consistency(results))
        self.assertEqual([], issues)

    def assert_frozen_somatic_items_present(self, results: dict) -> None:
        self.assertEqual(FROZEN_SOMATIC_ITEM_IDS, set(results["frozen_item_ids"]))
        self.assertEqual(
            {item_id: "v0.2.0" for item_id in FROZEN_SOMATIC_ITEM_IDS},
            results["frozen_item_versions"],
        )
        self.assertEqual(FROZEN_SOMATIC_ITEM_IDS, {row["item_id"] for row in results["item_statistics"]})
        self.assertEqual(FROZEN_SOMATIC_ITEM_IDS, {row["item_id"] for row in results["irt"]["item_parameters"]})

    def test_minimal_contract_fixture_is_schema_valid(self) -> None:
        results = _minimal_observed_results()
        self.assert_schema_valid(results)
        self.assert_frozen_somatic_items_present(results)

    def test_observed_results_file_contract_when_present(self) -> None:
        results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        self.assert_schema_valid(results)
        self.assert_frozen_somatic_items_present(results)

    def test_observed_results_validator_command_passes_for_somatic_wave1(self) -> None:
        completed = subprocess.run(
            [
                "python3",
                "tools/validate_observed_validation_results.py",
                "validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json",
            ],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(
            0,
            completed.returncode,
            completed.stdout + completed.stderr,
        )


if __name__ == "__main__":
    unittest.main()
