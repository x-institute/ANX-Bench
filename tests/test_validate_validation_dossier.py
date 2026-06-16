import importlib.util
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_validation_dossier.py"

spec = importlib.util.spec_from_file_location("validate_validation_dossier", VALIDATOR_PATH)
validate_validation_dossier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_validation_dossier"] = validate_validation_dossier
spec.loader.exec_module(validate_validation_dossier)


def _development_dossier() -> dict:
    path = REPO_ROOT / "validation" / "v0.2" / "somatic_ambient_anxiety" / "wave1_calibration_dossier.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _completed_evidence_record(sample: str, method: str, statistics: list[str]) -> dict:
    return {
        "status": "completed",
        "sample": sample,
        "method": method,
        "required_statistics": statistics,
        "decision_rule": "Evidence must satisfy the psychometric validation protocol threshold before approval.",
        "result_summary": "Completed numeric evidence is recorded in the structured results block.",
        "release_consequence": "Evidence supports the release decision stated in this dossier.",
    }


def _planned_evidence_record(sample: str, method: str, statistics: list[str]) -> dict:
    return {
        "status": "planned",
        "sample": sample,
        "method": method,
        "required_statistics": statistics,
        "decision_rule": "Evidence must satisfy the psychometric validation protocol threshold before approval.",
        "result_summary": "Statistic collection and analysis are planned; no scored-release evidence is claimed.",
        "release_consequence": "No scored release is permitted from planned evidence.",
    }


def _development_only_dossier() -> dict:
    dossier = _development_dossier()
    dossier["benchmark_version"] = "v9.9.9"
    dossier["dossier_status"] = "development_only"
    dossier["sample_provenance"]["development_pilot"]["status"] = "planned"
    dossier["sample_provenance"]["development_pilot"]["fielding_dates"] = "2024-01-10 to 2024-01-12"
    dossier["sample_provenance"]["development_pilot"]["analytic_n"] = 0
    dossier["sample_provenance"]["confirmation_sample"]["status"] = "planned"
    dossier["sample_provenance"]["confirmation_sample"]["fielding_dates"] = "2024-01-20 to 2024-01-24"
    dossier["sample_provenance"]["confirmation_sample"]["analytic_n"] = 0
    dossier["evidence"]["efa"] = _planned_evidence_record(
        "development_pilot",
        "Ordinal exploratory factor analysis planned for the development pilot.",
        ["parallel_analysis_factor_count", "primary_loading", "response_distribution"],
    )
    for family in ("cfa", "reliability", "irt", "dif", "invariance"):
        dossier["evidence"][family] = _planned_evidence_record(
            "confirmation_sample",
            f"Preregistered {family} analysis planned for the independent confirmation sample.",
            ["preregistered_statistic"],
        )
    dossier["evidence"]["external_validity"] = {
        family: _planned_evidence_record(
            "confirmation_sample",
            f"Preregistered {family} validity analysis planned for the confirmation sample.",
            ["coefficient", "confidence_interval", "direction"],
        )
        for family in ("convergent", "discriminant", "criterion", "incremental_validity")
    }
    for item in dossier["items"]:
        item["release_status"] = "development_only"
        item["psychometric_decision"] = "development_only"
        item["scoring_eligible"] = False
    for row in dossier["retention_table"]:
        row["observed_result"] = "No observed retention result is claimed before fielding and analysis."
        row["decision"] = "pending"
        row["rationale"] = "The item remains under development until planned fielding and preregistered validation analyses are complete."
    dossier.pop("results", None)
    dossier["decision"] = {
        "psychometric_decision": "development_only",
        "decision_date": "2024-01-05",
        "scoring_eligible": False,
        "approval_scope": "Development-only dossier retained for planned calibration work.",
        "rationale": "No scored release approval is claimed because the fielding, analysis, and statistic-level provenance remain planned.",
    }
    dossier["reviewer_signoff"] = {
        "reviewer": "ANX-Bench methods reviewer",
        "role": "Internal methods reviewer",
        "date": "2024-01-05",
        "conflicts": "None recorded",
        "signoff_status": "not_yet_reviewed",
        "notes": "Development dossier is allowed to pass structural validation without numeric scored-release evidence.",
    }
    return dossier


def _approved_scored_dossier() -> dict:
    dossier = _development_dossier()
    dossier["benchmark_version"] = "v9.9.9"
    dossier["evidence_provenance_path"] = "wave1_evidence_provenance.json"
    dossier["dossier_status"] = "approved_scored"
    dossier["sample_provenance"]["development_pilot"]["status"] = "fielded"
    dossier["sample_provenance"]["development_pilot"]["fielding_dates"] = "2024-01-10 to 2024-01-12"
    dossier["sample_provenance"]["development_pilot"]["analytic_n"] = 524
    dossier["sample_provenance"]["confirmation_sample"]["status"] = "fielded"
    dossier["sample_provenance"]["confirmation_sample"]["fielding_dates"] = "2024-01-20 to 2024-01-24"
    dossier["sample_provenance"]["confirmation_sample"]["analytic_n"] = 1042
    dossier["evidence"]["cfa"] = _completed_evidence_record(
        "confirmation_sample",
        "Ordinal CFA with WLSMV estimator for the retained one-factor model.",
        ["cfi", "tli", "rmsea", "srmr", "standardized_loading"],
    )
    dossier["evidence"]["reliability"] = _completed_evidence_record(
        "confirmation_sample",
        "Ordinal omega and alpha with corrected item-total correlations.",
        ["omega", "alpha", "corrected_item_total_correlation", "standard_error_of_measurement"],
    )
    dossier["evidence"]["dif"] = _completed_evidence_record(
        "confirmation_sample",
        "Ordinal logistic DIF screening with multiplicity correction.",
        ["delta_pseudo_r2", "statistical_support", "practical_significance", "resolution"],
    )
    dossier["evidence"]["invariance"] = _completed_evidence_record(
        "confirmation_sample",
        "Multi-group CFA sequence for configural, metric, and scalar invariance.",
        ["metric_delta_cfi", "metric_delta_rmsea", "scalar_delta_cfi", "scalar_delta_rmsea"],
    )
    dossier["evidence"]["external_validity"] = {
        "convergent": _completed_evidence_record(
            "confirmation_sample",
            "Preregistered correlation with AI-specific anxiety comparator.",
            ["coefficient", "confidence_interval", "direction"],
        ),
        "discriminant": _completed_evidence_record(
            "confirmation_sample",
            "Latent construct correlation with general anxiety and adjacent ANX constructs.",
            ["coefficient", "confidence_interval", "factor_separability"],
        ),
        "criterion": _completed_evidence_record(
            "confirmation_sample",
            "Preregistered association with AI avoidance intention.",
            ["coefficient", "confidence_interval", "direction"],
        ),
        "incremental_validity": _completed_evidence_record(
            "confirmation_sample",
            "Incremental prediction after demographics, AI exposure, and general anxiety.",
            ["adjusted_r2_delta", "confidence_interval", "covariate_block"],
        ),
    }
    for item in dossier["items"]:
        item["release_status"] = "approved_scored"
        item["psychometric_decision"] = "approved_scored"
        item["scoring_eligible"] = True
    for row in dossier["retention_table"]:
        row["criterion"] = "Retained confirmation psychometric evidence"
        row["observed_result"] = "Retained item satisfies loading, item-total, response distribution, missingness, DIF, and invariance checks."
        row["threshold"] = "Retained scored items must pass all machine-checkable ANX-Bench psychometric thresholds."
        row["decision"] = "retain"
        row["rationale"] = "The retained item contributes distinct construct coverage and passes the structured numeric approval evidence gate."
    dossier["decision"] = {
        "psychometric_decision": "approved_scored",
        "decision_date": "2024-02-01",
        "scoring_eligible": True,
        "approval_scope": "Approved for construct, domain, longitudinal, and event-study scoring subject to the frozen release manifest.",
        "rationale": "Independent confirmation evidence satisfies the ANX-Bench psychometric validation protocol and supports scored use of the retained construct.",
    }
    dossier["reviewer_signoff"] = {
        "reviewer": "Independent ANX-Bench psychometric reviewer",
        "role": "Independent psychometric reviewer",
        "date": "2024-02-01",
        "conflicts": "None recorded",
        "signoff_status": "signed_off",
        "notes": "Reviewer signoff confirms that the structured numeric evidence and release decision are aligned.",
    }
    dossier["results"] = {
        "analytic_n": 1042,
        "retained_item_count": 4,
        "cfa_fit": {
            "sample": "confirmation_sample",
            "model": "One-factor somatic and ambient anxiety model with four ordinal indicators.",
            "cfi": 0.956,
            "tli": 0.948,
            "rmsea": 0.052,
            "srmr": 0.041,
        },
        "reliability": {
            "sample": "confirmation_sample",
            "omega": 0.82,
            "alpha": 0.79,
            "standard_error_of_measurement": 0.28,
        },
        "item_statistics": [
            {
                "item_id": item["item_id"],
                "retained": True,
                "primary_loading": 0.62,
                "max_cross_loading": 0.18,
                "corrected_item_total_correlation": 0.46,
                "floor_rate": 0.21,
                "ceiling_rate": 0.12,
                "adjacent_floor_rate": 0.43,
                "adjacent_ceiling_rate": 0.31,
                "missing_rate": 0.03,
            }
            for item in dossier["items"]
        ],
        "dif": {
            "unresolved_practical_dif": False,
            "analyses": [
                {
                    "item_id": dossier["items"][0]["item_id"],
                    "grouping_variable": "gender",
                    "method": "Ordinal logistic DIF with Benjamini-Hochberg correction.",
                    "effect_size_metric": "delta_pseudo_r2",
                    "effect_size": 0.006,
                    "practical_threshold": 0.02,
                    "statistically_supported": False,
                    "practically_meaningful": False,
                    "resolved": True,
                }
            ],
        },
        "invariance": {
            "method": "Multi-group ordinal CFA",
            "comparison_scope": "Age, gender, education, and prior AI exposure groups in the confirmation sample.",
            "metric_delta_cfi": -0.006,
            "metric_delta_rmsea": 0.006,
            "scalar_delta_cfi": -0.008,
            "scalar_delta_rmsea": 0.007,
        },
        "external_validity": {
            "convergent": {
                "variable": "tech_ai_anxiety_comparator_mean",
                "coefficient_metric": "r",
                "coefficient": 0.44,
                "ci_low": 0.38,
                "ci_high": 0.50,
                "direction_matches": True,
                "passes_threshold": True,
            },
            "discriminant": {
                "variable": "general_anxiety_2item_mean",
                "coefficient_metric": "latent_correlation",
                "coefficient": 0.42,
                "ci_low": 0.34,
                "ci_high": 0.50,
                "direction_matches": True,
                "passes_threshold": True,
            },
            "criterion": {
                "variable": "ai_avoidance_intention_6m",
                "coefficient_metric": "standardized_beta",
                "coefficient": 0.26,
                "ci_low": 0.17,
                "ci_high": 0.35,
                "direction_matches": True,
                "passes_threshold": True,
            },
            "incremental_validity": {
                "variable": "ai_avoidance_intention_6m",
                "coefficient_metric": "adjusted_r2_delta",
                "coefficient": 0.023,
                "ci_low": 0.014,
                "ci_high": 0.034,
                "direction_matches": True,
                "passes_threshold": True,
            },
        },
    }
    return dossier


def _observed_statistic(statistic_id: str, pointer: str, family: str) -> dict:
    return {
        "statistic_id": statistic_id,
        "dossier_json_pointer": pointer,
        "analysis_family": family,
        "evidence_status": "observed_data",
        "fielding_samples": [
            "confirmation_sample"
        ],
        "data_artifacts": [
            {
                "path": f"restricted://fixture/outputs/{statistic_id}.json",
                "sha256": "a" * 64,
                "description": "Observed derived validation output for the fixture statistic.",
            }
        ],
        "analysis_scripts": [
            {
                "path": "restricted://fixture/scripts/reproduce_validation_fixture.R",
                "sha256": "b" * 64,
                "description": "Frozen fixture script that reproduces the statistic from observed data.",
            }
        ],
        "signoff": {
            "signer": "Independent ANX-Bench psychometric reviewer",
            "role": "Independent psychometric reviewer",
            "signed_date": "2024-02-01",
            "signature_status": "signed",
        },
        "provenance_note": "Fixture statistic is treated as observed because it has data and script checksums plus signed statistic-level provenance.",
    }


def _observed_provenance() -> dict:
    return {
        "$schema": str(REPO_ROOT / "schema" / "evidence_provenance.schema.json"),
        "provenance_schema_version": "v0.1.0",
        "provenance_id": "fixture_observed_evidence_provenance",
        "validation_dossier_path": "wave1_calibration_dossier.json",
        "benchmark_version": "v9.9.9",
        "construct_id": "somatic_ambient_anxiety",
        "evidence_status": "observed_data",
        "validation_date": "2024-02-01",
        "fielding_windows": [
            {
                "sample": "development_pilot",
                "status": "observed_data",
                "planned_start_date": "2024-01-10",
                "planned_end_date": "2024-01-12",
                "observed_start_date": "2024-01-10",
                "observed_end_date": "2024-01-12",
                "fielding_date_source": "Fixture pilot dates are bound to the observed sample-flow artifact.",
            },
            {
                "sample": "confirmation_sample",
                "status": "observed_data",
                "planned_start_date": "2024-01-20",
                "planned_end_date": "2024-01-24",
                "observed_start_date": "2024-01-20",
                "observed_end_date": "2024-01-24",
                "fielding_date_source": "Fixture confirmation dates are bound to the observed sample-flow artifact.",
            },
        ],
        "validation_statistics": [
            _observed_statistic("retention_fixture", "/results/retained_item_count", "retention"),
            _observed_statistic("cfa_fixture", "/results/cfa_fit", "cfa"),
            _observed_statistic("reliability_fixture", "/results/reliability", "reliability"),
            _observed_statistic("dif_fixture", "/results/dif", "dif"),
            _observed_statistic("invariance_fixture", "/results/invariance", "invariance"),
            _observed_statistic("external_validity_fixture", "/results/external_validity", "external_validity"),
            _observed_statistic("irt_fixture", "/evidence/irt/result_summary", "irt"),
            _observed_statistic("efa_fixture", "/evidence/efa/result_summary", "efa"),
        ],
        "provenance_assertion": "The fixture represents observed-data evidence because each validation statistic is bound to fielding dates, data artifacts, analysis scripts, checksums, and statistic-level signoff.",
    }


def _placeholder_provenance() -> dict:
    provenance = _observed_provenance()
    provenance["evidence_status"] = "planned_or_placeholder"
    for statistic in provenance["validation_statistics"]:
        statistic["evidence_status"] = "planned_or_placeholder"
        statistic["signoff"] = {
            "signer": None,
            "role": None,
            "signed_date": None,
            "signature_status": "unsigned_placeholder",
        }
    return provenance


def _write_dossier(tmp_path: Path, dossier: dict) -> Path:
    path = tmp_path / "wave1_calibration_dossier.json"
    path.write_text(json.dumps(dossier, indent=2) + "\n", encoding="utf-8")
    return path


def _write_provenance(tmp_path: Path, provenance: dict) -> Path:
    path = tmp_path / "wave1_evidence_provenance.json"
    path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return path


class ValidateValidationDossierTests(unittest.TestCase):
    def test_planned_development_dossier_passes_without_numeric_results(self) -> None:
        dossier = _development_only_dossier()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = _write_dossier(Path(tmpdir), dossier)

            validate_validation_dossier.validate_dossier(path)

    def test_approved_scored_missing_numeric_evidence_fails(self) -> None:
        dossier = _development_dossier()
        dossier["benchmark_version"] = "v9.9.9"
        dossier["evidence_provenance_path"] = "wave1_evidence_provenance.json"
        dossier["dossier_status"] = "approved_scored"
        dossier["decision"]["psychometric_decision"] = "approved_scored"
        dossier["decision"]["scoring_eligible"] = True
        dossier["decision"]["decision_date"] = "2024-02-01"
        dossier.pop("results", None)

        with tempfile.TemporaryDirectory() as tmpdir:
            _write_provenance(Path(tmpdir), _observed_provenance())
            path = _write_dossier(Path(tmpdir), dossier)
            with self.assertRaisesRegex(
                validate_validation_dossier.DossierValidationError,
                "results",
            ):
                validate_validation_dossier.validate_dossier(path)

    def test_threshold_violation_dossier_fails(self) -> None:
        dossier = _approved_scored_dossier()
        violating = deepcopy(dossier)
        violating["results"]["reliability"]["omega"] = 0.66
        violating["results"]["cfa_fit"]["cfi"] = 0.88
        violating["results"]["item_statistics"][0]["primary_loading"] = 0.39
        violating["results"]["dif"]["unresolved_practical_dif"] = True
        violating["results"]["invariance"]["scalar_delta_cfi"] = -0.021

        with tempfile.TemporaryDirectory() as tmpdir:
            _write_provenance(Path(tmpdir), _observed_provenance())
            path = _write_dossier(Path(tmpdir), violating)
            with self.assertRaisesRegex(
                validate_validation_dossier.DossierValidationError,
                "omega must be >= 0.70",
            ):
                validate_validation_dossier.validate_dossier(path)

    def test_forward_dated_fielding_fails(self) -> None:
        dossier = _approved_scored_dossier()
        dossier["sample_provenance"]["confirmation_sample"]["fielding_dates"] = "2024-02-03 to 2024-02-05"

        with tempfile.TemporaryDirectory() as tmpdir:
            _write_provenance(Path(tmpdir), _observed_provenance())
            path = _write_dossier(Path(tmpdir), dossier)
            with self.assertRaisesRegex(
                validate_validation_dossier.DossierValidationError,
                "fielding dates cannot be after the validation decision date",
            ):
                validate_validation_dossier.validate_dossier(path)

    def test_placeholder_evidence_blocks_approved_scored(self) -> None:
        dossier = _approved_scored_dossier()

        with tempfile.TemporaryDirectory() as tmpdir:
            _write_provenance(Path(tmpdir), _placeholder_provenance())
            path = _write_dossier(Path(tmpdir), dossier)
            with self.assertRaisesRegex(
                validate_validation_dossier.DossierValidationError,
                "placeholder provenance",
            ):
                validate_validation_dossier.validate_dossier(path)

    def test_missing_provenance_checksums_fail(self) -> None:
        dossier = _approved_scored_dossier()
        provenance = _observed_provenance()
        provenance["validation_statistics"][0]["data_artifacts"][0]["sha256"] = None

        with tempfile.TemporaryDirectory() as tmpdir:
            _write_provenance(Path(tmpdir), provenance)
            path = _write_dossier(Path(tmpdir), dossier)
            with self.assertRaisesRegex(
                validate_validation_dossier.DossierValidationError,
                "missing valid SHA-256 checksum",
            ):
                validate_validation_dossier.validate_dossier(path)

    def test_valid_observed_evidence_fixture_passes(self) -> None:
        dossier = _approved_scored_dossier()

        with tempfile.TemporaryDirectory() as tmpdir:
            _write_provenance(Path(tmpdir), _observed_provenance())
            path = _write_dossier(Path(tmpdir), dossier)

            validate_validation_dossier.validate_dossier(path)


if __name__ == "__main__":
    unittest.main()
