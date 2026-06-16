import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import validate_analysis_plan  # noqa: E402
import validate_release  # noqa: E402


def _copy_plan_fixture(tmp_path: Path, plan_relative_path: str, release_relative_path: str) -> tuple[Path, Path]:
    plan = json.loads((REPO_ROOT / plan_relative_path).read_text(encoding="utf-8"))
    preregistration_path = plan["registration"]["preregistration_path"]
    required_paths = {
        "schema/psychometric_analysis_plan.schema.json",
        "schema/release.schema.json",
        plan_relative_path,
        release_relative_path,
        preregistration_path,
    }

    for relative_path in sorted(required_paths):
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    return tmp_path / plan_relative_path, tmp_path / release_relative_path


def _update_manifest_plan_checksum(manifest_path: Path, plan_relative_path: str) -> None:
    root = manifest_path.parents[2]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for record in manifest["checksums"]["files"]:
        if record["path"] == plan_relative_path:
            record["sha256"] = validate_release.sha256_file(root / plan_relative_path)
            break
    else:
        raise AssertionError(f"missing checksum record for {plan_relative_path}")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


class ValidateAnalysisPlanTests(unittest.TestCase):
    def test_v02_somatic_analysis_plan_passes_against_release_manifest(self) -> None:
        validate_analysis_plan.validate_analysis_plan(
            REPO_ROOT / "analysis/v0.2/somatic_ambient/wave1_analysis_plan.json",
            REPO_ROOT / "releases/v0.2.2/manifest.json",
        )

    def test_v05_economic_analysis_plan_passes_against_release_manifest(self) -> None:
        validate_analysis_plan.validate_analysis_plan(
            REPO_ROOT / "analysis/v0.5/economic_vocational/wave5_analysis_plan.json",
            REPO_ROOT / "releases/v0.5.0/manifest.json",
        )

    def test_v06_epistemic_analysis_plan_passes_against_release_manifest(self) -> None:
        validate_analysis_plan.validate_analysis_plan(
            REPO_ROOT / "analysis/v0.6/epistemic_trust/wave6_analysis_plan.json",
            REPO_ROOT / "releases/v0.6.0/manifest.json",
        )

    def test_rejects_item_set_mismatch_even_when_modified_plan_checksum_matches(self) -> None:
        plan_relative_path = "analysis/v0.5/economic_vocational/wave5_analysis_plan.json"
        release_relative_path = "releases/v0.5.0/manifest.json"
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path, manifest_path = _copy_plan_fixture(
                Path(tmpdir),
                plan_relative_path,
                release_relative_path,
            )
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            for input_record in plan["required_inputs"]:
                if input_record["input_id"] == "frozen_item_files":
                    input_record["required_fields"][-1] = "unregistered_economic_anxiety_item"
                    break
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
            _update_manifest_plan_checksum(manifest_path, plan_relative_path)

            with self.assertRaisesRegex(
                validate_analysis_plan.AnalysisPlanValidationError,
                "planned item IDs must equal the manifest frozen item set",
            ):
                validate_analysis_plan.validate_analysis_plan(plan_path, manifest_path)

    def test_rejects_plan_with_inspected_outcomes(self) -> None:
        plan_relative_path = "analysis/v0.6/epistemic_trust/wave6_analysis_plan.json"
        release_relative_path = "releases/v0.6.0/manifest.json"
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path, manifest_path = _copy_plan_fixture(
                Path(tmpdir),
                plan_relative_path,
                release_relative_path,
            )
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["registration"]["outcome_inspection_status"] = "inspected_after_freeze"
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
            _update_manifest_plan_checksum(manifest_path, plan_relative_path)

            with self.assertRaisesRegex(
                validate_analysis_plan.AnalysisPlanValidationError,
                "outcome_inspection_status",
            ):
                validate_analysis_plan.validate_analysis_plan(plan_path, manifest_path)


if __name__ == "__main__":
    unittest.main()
