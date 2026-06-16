import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import validate_sampling_plan  # noqa: E402


PLAN_RELATIVE_PATH = "sampling/v0.7/anx_us_2026w07_cross_domain_bridge_sampling_plan.json"
TEMPLATE_PLAN_RELATIVE_PATH = "sampling/v0.7/anx_us_2026w07_cross_domain_bridge_sampling_plan.template.json"


def _copy_plan_fixture(tmp_path: Path) -> Path:
    required_paths = {
        "schema/sampling_plan.schema.json",
        "schema/release.schema.json",
        "schema/item.schema.json",
        "docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md",
        PLAN_RELATIVE_PATH
    }
    for relative_path in sorted(required_paths):
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path / PLAN_RELATIVE_PATH


class ValidateSamplingPlanTests(unittest.TestCase):
    def test_wave7_sampling_plan_passes(self) -> None:
        validate_sampling_plan.validate_sampling_plan(REPO_ROOT / PLAN_RELATIVE_PATH)

    def test_wave7_sampling_plan_template_is_not_claim_bearing(self) -> None:
        with self.assertRaisesRegex(
            validate_sampling_plan.SamplingPlanValidationError,
            "template sampling plans cannot serve as frozen claim-bearing bridge artifacts",
        ):
            validate_sampling_plan.validate_sampling_plan(REPO_ROOT / TEMPLATE_PLAN_RELATIVE_PATH)

    def test_rejects_missing_target_population(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = _copy_plan_fixture(Path(tmpdir))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            del plan["target_population"]
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_sampling_plan.SamplingPlanValidationError,
                "target_population|target population",
            ):
                validate_sampling_plan.validate_sampling_plan(plan_path)

    def test_rejects_missing_weight_construction(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = _copy_plan_fixture(Path(tmpdir))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["weighting_method"]["construction_steps"] = []
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_sampling_plan.SamplingPlanValidationError,
                "weight construction",
            ):
                validate_sampling_plan.validate_sampling_plan(plan_path)

    def test_rejects_population_claim_without_variance_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = _copy_plan_fixture(Path(tmpdir))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["variance_design"]["estimator"] = "not_applicable"
            plan["variance_design"]["primary_standard_error"] = "No standard errors planned."
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_sampling_plan.SamplingPlanValidationError,
                "population claims require variance metadata",
            ):
                validate_sampling_plan.validate_sampling_plan(plan_path)

    def test_rejects_population_claim_without_survey_weight_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = _copy_plan_fixture(Path(tmpdir))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["weighting_method"]["survey_weight_mapping"]["wave_response_field"] = "final_weight"
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_sampling_plan.SamplingPlanValidationError,
                "survey_weight",
            ):
                validate_sampling_plan.validate_sampling_plan(plan_path)


if __name__ == "__main__":
    unittest.main()
