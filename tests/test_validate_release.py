import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_release.py"

spec = importlib.util.spec_from_file_location("validate_release", VALIDATOR_PATH)
validate_release = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_release"] = validate_release
spec.loader.exec_module(validate_release)


def _copy_release_fixture(tmp_path: Path, release_version: str = "v0.1.0") -> Path:
    source_manifest_path = REPO_ROOT / "releases" / release_version / "manifest.json"
    manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    release_line = ".".join(release_version.split(".")[:2])

    required_paths = {
        "schema/release.schema.json",
        "schema/item.schema.json",
        f"constructs/{release_line}/registry.json",
        f"releases/{release_version}/manifest.json",
    }
    required_paths.update(record["path"] for record in manifest["checksums"]["files"])
    required_paths.update(item["path"] for item in manifest["frozen_item_set"]["items"])
    required_paths.update(document["path"] for document in manifest["methodology_documents"])
    for record in manifest["checksums"]["files"]:
        if record["path"].startswith("validation/") and record["path"].endswith(".json"):
            dossier = json.loads((REPO_ROOT / record["path"]).read_text(encoding="utf-8"))
            preregistration_path = dossier.get("preregistration_path")
            if isinstance(preregistration_path, str):
                required_paths.add(preregistration_path)

    for relative_path in sorted(required_paths):
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    fixture_manifest_path = tmp_path / "releases" / release_version / "manifest.json"
    manifest = json.loads(fixture_manifest_path.read_text(encoding="utf-8"))
    checksum_by_path = {}
    for record in manifest["checksums"]["files"]:
        checksum_by_path[record["path"]] = validate_release.sha256_file(tmp_path / record["path"])
        record["sha256"] = checksum_by_path[record["path"]]

    manifest["item_schema"]["sha256"] = checksum_by_path[manifest["item_schema"]["path"]]
    for document in manifest["methodology_documents"]:
        document["sha256"] = checksum_by_path[document["path"]]
    for item in manifest["frozen_item_set"]["items"]:
        item["sha256"] = checksum_by_path[item["path"]]

    fixture_manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return fixture_manifest_path


def _load_v030_manifest() -> dict:
    return json.loads((REPO_ROOT / "releases" / "v0.3.0" / "manifest.json").read_text(encoding="utf-8"))


def _load_v031_manifest() -> dict:
    return json.loads((REPO_ROOT / "releases" / "v0.3.1" / "manifest.json").read_text(encoding="utf-8"))


def _set_checksum(manifest_path: Path, relative_path: str) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = validate_release.sha256_file(manifest_path.parents[2] / relative_path)
    for record in manifest["checksums"]["files"]:
        if record["path"] == relative_path:
            record["sha256"] = digest
            break
    else:
        raise AssertionError(f"missing checksum record for {relative_path}")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _promote_v030_fixture_to_scored(manifest_path: Path) -> None:
    root = manifest_path.parents[2]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item_ids = [item["item_id"] for item in manifest["frozen_item_set"]["items"]]
    manifest["release_date"] = "2026-06-15"
    manifest["release_status"] = "citable"
    manifest["release_label"] = "ANX-Bench v0.3.0 scored somatic and ambient anxiety release"
    manifest["official_scored_items"] = item_ids
    manifest["scoring_eligibility"]["official_scored_item_count"] = len(item_ids)
    manifest["scoring_eligibility"]["aggregate_scoring_permitted"] = True

    for manifest_item in manifest["frozen_item_set"]["items"]:
        manifest_item["release_status"] = "approved_scored"
        manifest_item["validation"]["scoring_eligible"] = True
        item_path = root / manifest_item["path"]
        item = json.loads(item_path.read_text(encoding="utf-8"))
        item["release_status"] = "approved_scored"
        item["validation"]["psychometric_decision"] = "approved_scored"
        item["validation"]["decision_date"] = "2026-06-15"
        item["validation"]["scoring_eligible"] = True
        item_path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
        manifest_item["sha256"] = validate_release.sha256_file(item_path)

    dossier_relative_path = "validation/v0.2/somatic_ambient_anxiety/wave1_calibration_dossier.json"
    dossier_path = root / dossier_relative_path
    dossier = json.loads(dossier_path.read_text(encoding="utf-8"))
    dossier["dossier_status"] = "approved_scored"
    dossier["decision"]["psychometric_decision"] = "approved_scored"
    dossier["decision"]["decision_date"] = "2026-06-15"
    dossier["decision"]["scoring_eligible"] = True
    for dossier_item in dossier["items"]:
        dossier_item["release_status"] = "approved_scored"
        dossier_item["psychometric_decision"] = "approved_scored"
        dossier_item["scoring_eligible"] = True
    dossier_path.write_text(json.dumps(dossier, indent=2) + "\n", encoding="utf-8")

    checksum_updates = {
        dossier_relative_path: validate_release.sha256_file(dossier_path),
        **{
            item["path"]: validate_release.sha256_file(root / item["path"])
            for item in manifest["frozen_item_set"]["items"]
        },
    }
    for record in manifest["checksums"]["files"]:
        if record["path"] in checksum_updates:
            record["sha256"] = checksum_updates[record["path"]]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _iter_named_hash_fields(value: object, path: str = "$") -> list[tuple[str, str]]:
    hashes: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            child_path = f"{path}/{key}"
            if (key == "sha256" or key.endswith("_sha256")) and isinstance(item, str):
                hashes.append((child_path, item))
            hashes.extend(_iter_named_hash_fields(item, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hashes.extend(_iter_named_hash_fields(item, f"{path}/{index}"))
    return hashes


def _assert_citable_somatic_release_references_observed_results(manifest_path: Path) -> None:
    root = manifest_path.parents[2]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("release_status") != "citable":
        return

    somatic_scored_items = [
        item
        for item in manifest["frozen_item_set"]["items"]
        if item["construct"] == "somatic_ambient_anxiety" and item["item_id"] in manifest["official_scored_items"]
    ]
    if not somatic_scored_items:
        return

    observed_path = "validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json"
    evidence_path = "validation/v0.2/somatic_ambient_anxiety/wave1_evidence_manifest.json"
    zero_hash = "0" * 64
    checksum_by_path = {record["path"]: record["sha256"] for record in manifest["checksums"]["files"]}

    assert observed_path in checksum_by_path, "citable somatic release must checksum observed_wave1_results.json"
    assert checksum_by_path[observed_path] != zero_hash, "observed results checksum must not be a zero placeholder"
    assert (root / observed_path).is_file(), "observed results artifact must exist in the release fixture"

    evidence_manifest = json.loads((root / evidence_path).read_text(encoding="utf-8"))
    output_artifacts = {
        artifact["path"]: artifact
        for artifact in evidence_manifest["output_artifact_hashes"]
        if isinstance(artifact, dict) and "path" in artifact
    }
    assert observed_path in output_artifacts, "evidence manifest must reference observed_wave1_results.json"
    assert output_artifacts[observed_path]["sha256"] == checksum_by_path[observed_path]

    zero_hash_paths = [
        field_path
        for field_path, digest in _iter_named_hash_fields(evidence_manifest)
        if digest == zero_hash
    ]
    assert zero_hash_paths == [], "citable somatic evidence manifest contains zero placeholder hashes"


class ValidateReleaseTests(unittest.TestCase):
    def test_v010_manifest_passes_release_gate_in_clean_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = _copy_release_fixture(Path(tmpdir))

            validate_release.validate_release(manifest_path)

    def test_v030_manifest_freezes_provisional_somatic_scoring_candidate(self) -> None:
        manifest = _load_v030_manifest()

        self.assertEqual("v0.3.0", manifest["benchmark_version"])
        self.assertEqual("frozen_candidate", manifest["release_status"])
        self.assertIn("provisional scoring candidate", manifest["release_label"])
        self.assertFalse(manifest["scoring_eligibility"]["aggregate_scoring_permitted"])
        self.assertEqual(0, manifest["scoring_eligibility"]["official_scored_item_count"])
        self.assertEqual([], manifest["official_scored_items"])

        checksum_by_path = {record["path"]: record["sha256"] for record in manifest["checksums"]["files"]}
        self.assertIn("constructs/v0.3/registry.json", checksum_by_path)
        self.assertIn(
            "validation/v0.2/somatic_ambient_anxiety/wave1_calibration_dossier.json",
            checksum_by_path,
        )
        self.assertIn("docs/releases/v0.3.0_scoring_note.md", checksum_by_path)

        for item in manifest["frozen_item_set"]["items"]:
            self.assertEqual("development_only", item["release_status"])
            self.assertFalse(item["validation"]["scoring_eligible"])
            self.assertEqual(item["sha256"], checksum_by_path[item["path"]])

    def test_v030_release_defining_checksums_match_working_tree(self) -> None:
        manifest = _load_v030_manifest()

        for record in manifest["checksums"]["files"]:
            if record["path"].startswith("validation/v0.2/somatic_ambient_anxiety/") or record[
                "path"
            ].startswith("items/v0.2/somatic_ambient/"):
                continue
            self.assertEqual(validate_release.sha256_file(REPO_ROOT / record["path"]), record["sha256"], record["path"])

    def test_v031_release_validator_command_passes_for_scored_somatic_release(self) -> None:
        completed = subprocess.run(
            ["python3", "tools/validate_release.py", "releases/v0.3.1/manifest.json"],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_v031_release_is_narrow_somatic_ambient_scored_release(self) -> None:
        manifest = _load_v031_manifest()

        self.assertEqual("v0.3.1", manifest["benchmark_version"])
        self.assertEqual("citable", manifest["release_status"])
        self.assertEqual(
            {
                "sleep_disruption_ai_news",
                "body_vigilance_model_release",
                "background_dread_ai_progress",
                "avoidance_after_ai_capability_demo",
            },
            set(manifest["official_scored_items"]),
        )
        self.assertTrue(manifest["scoring_eligibility"]["aggregate_scoring_permitted"])
        self.assertIn("limited to the four retained", manifest["scoring_eligibility"]["eligibility_rule"])
        self.assertIn("does not permit an overall ANX score", manifest["scoring_eligibility"]["eligibility_rule"])

        checksum_by_path = {record["path"]: record["sha256"] for record in manifest["checksums"]["files"]}
        self.assertIn(
            "validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json",
            checksum_by_path,
        )
        self.assertNotEqual(
            "0" * 64,
            checksum_by_path["validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json"],
        )
        for item in manifest["frozen_item_set"]["items"]:
            self.assertEqual("somatic_ambient_anxiety", item["construct"])
            self.assertEqual("approved_scored", item["release_status"])
            self.assertTrue(item["validation"]["scoring_eligible"])

    def test_epistemic_items_share_schema_valid_calibration_dossier(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path)

            validate_release.validate_release(manifest_path)

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            epistemic_items = [
                item for item in manifest["frozen_item_set"]["items"] if item["domain"] == "epistemic"
            ]
            self.assertEqual(
                {
                    "ai_expert_claim_conflict",
                    "deepfake_evidence_trust",
                    "personalized_misinformation_targeting",
                    "synthetic_news_provenance",
                },
                {item["item_id"] for item in epistemic_items},
            )

            dossier_relative_path = (
                "validation/v0.1/epistemic_trust_anxiety/wave1_calibration_dossier.json"
            )
            dossier = json.loads((tmp_path / dossier_relative_path).read_text(encoding="utf-8"))
            self.assertEqual("epistemic_trust_anxiety", dossier["construct"]["construct_id"])
            self.assertEqual(
                {item["item_id"] for item in epistemic_items},
                {item["item_id"] for item in dossier["items"]},
            )

            for manifest_item in epistemic_items:
                item = json.loads((tmp_path / manifest_item["path"]).read_text(encoding="utf-8"))
                self.assertEqual("epistemic_trust_anxiety", item["construct"]["construct_id"])
                self.assertEqual(dossier_relative_path, item["validation"]["dossier_path"])
                self.assertFalse(item["validation"]["scoring_eligible"])

    def test_release_gate_fails_on_checksum_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path)
            item_path = (
                tmp_path
                / "items"
                / "v0.1"
                / "economic_vocational"
                / "job_displacement_radiology.json"
            )
            item_data = json.loads(item_path.read_text(encoding="utf-8"))
            item_data["scenario_text"] = (
                item_data["scenario_text"] + " This unregistered edit changes the frozen file."
            )
            item_path.write_text(json.dumps(item_data, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(validate_release.ReleaseValidationError, "sha256 mismatch"):
                validate_release.validate_release(manifest_path)

    def test_scored_release_gate_fails_without_evidence_provenance_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path, "v0.3.0")
            evidence_relative_path = (
                "validation/v0.2/somatic_ambient_anxiety/wave1_evidence_manifest.json"
            )
            _promote_v030_fixture_to_scored(manifest_path)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["checksums"]["files"] = [
                record
                for record in manifest["checksums"]["files"]
                if record["path"] != evidence_relative_path
            ]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_release.ReleaseValidationError,
                "missing checksums.files entry for psychometric evidence manifest",
            ):
                validate_release.validate_release(manifest_path)

    def test_scored_release_gate_fails_on_stale_evidence_manifest_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path, "v0.3.0")
            evidence_relative_path = (
                "validation/v0.2/somatic_ambient_anxiety/wave1_evidence_manifest.json"
            )
            _promote_v030_fixture_to_scored(manifest_path)
            evidence_path = tmp_path / evidence_relative_path
            evidence_manifest = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence_manifest["provenance_assertion"] += (
                " This unregistered edit changes the frozen scored-release evidence provenance."
            )
            evidence_path.write_text(json.dumps(evidence_manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(validate_release.ReleaseValidationError, "sha256 mismatch"):
                validate_release.validate_release(manifest_path)

    def test_citable_somatic_release_fixture_requires_observed_results_and_nonzero_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path, "v0.3.0")
            _promote_v030_fixture_to_scored(manifest_path)

            with self.assertRaisesRegex(
                AssertionError,
                "citable somatic release must checksum observed_wave1_results.json",
            ):
                _assert_citable_somatic_release_references_observed_results(manifest_path)

            observed_path = "validation/v0.2/somatic_ambient_anxiety/observed_wave1_results.json"
            evidence_path = "validation/v0.2/somatic_ambient_anxiety/wave1_evidence_manifest.json"
            observed_file = tmp_path / observed_path
            observed_file.write_text(
                json.dumps(
                    {
                        "artifact": "minimal observed-results fixture for release-reference assertion",
                        "input_data_sha256": "1" * 64,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            observed_sha256 = validate_release.sha256_file(observed_file)

            evidence_manifest_path = tmp_path / evidence_path
            evidence_manifest = json.loads(evidence_manifest_path.read_text(encoding="utf-8"))
            evidence_manifest["raw_restricted_dataset_hash"]["sha256"] = "2" * 64
            evidence_manifest["analysis_script_hash"]["sha256"] = "3" * 64
            evidence_manifest["software_session_lock"]["session_info_sha256"] = "4" * 64
            for artifact in evidence_manifest["output_artifact_hashes"]:
                if artifact["path"] == observed_path:
                    artifact["sha256"] = observed_sha256
            evidence_manifest_path.write_text(json.dumps(evidence_manifest, indent=2) + "\n", encoding="utf-8")

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["checksums"]["files"].append({"path": observed_path, "sha256": observed_sha256})
            for record in manifest["checksums"]["files"]:
                if record["path"] == evidence_path:
                    record["sha256"] = validate_release.sha256_file(evidence_manifest_path)
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            _assert_citable_somatic_release_references_observed_results(manifest_path)

    def test_v030_registry_documents_somatic_candidate_requirements(self) -> None:
        registry = json.loads((REPO_ROOT / "constructs" / "v0.3" / "registry.json").read_text(encoding="utf-8"))
        construct = next(
            item for item in registry["constructs"] if item["construct_id"] == "somatic_ambient_anxiety"
        )

        self.assertEqual("approved_construct_score", construct["intended_aggregation_level"])
        self.assertEqual(4, construct["minimum_retained_items"])
        self.assertEqual(
            {
                "sleep_disruption_ai_news",
                "body_vigilance_model_release",
                "background_dread_ai_progress",
                "avoidance_after_ai_capability_demo",
            },
            set(construct["allowed_item_ids"]),
        )
        scoring_rule = construct["validation_requirements"]["scoring_rule"]
        self.assertIn("four retained approved_scored item versions", scoring_rule)
        self.assertIn("docs/releases/v0.3.0_scoring_note.md", scoring_rule)

    def test_v031_dossier_and_items_agree_on_scored_somatic_status(self) -> None:
        manifest = _load_v031_manifest()
        dossier_path = REPO_ROOT / "validation" / "v0.2" / "somatic_ambient_anxiety" / "wave1_calibration_dossier.json"
        dossier = json.loads(dossier_path.read_text(encoding="utf-8"))

        self.assertEqual("approved_scored", dossier["dossier_status"])
        self.assertEqual("approved_scored", dossier["decision"]["psychometric_decision"])
        self.assertTrue(dossier["decision"]["scoring_eligible"])
        self.assertEqual(1109, dossier["results"]["analytic_n"])
        self.assertEqual("fielded", dossier["sample_provenance"]["development_pilot"]["status"])
        self.assertEqual("fielded", dossier["sample_provenance"]["confirmation_sample"]["status"])

        dossier_items = {item["item_id"]: item for item in dossier["items"]}
        for manifest_item in manifest["frozen_item_set"]["items"]:
            item = json.loads((REPO_ROOT / manifest_item["path"]).read_text(encoding="utf-8"))
            dossier_item = dossier_items[manifest_item["item_id"]]
            self.assertEqual("approved_scored", item["release_status"])
            self.assertTrue(item["validation"]["scoring_eligible"])
            self.assertEqual("approved_scored", dossier_item["release_status"])
            self.assertTrue(dossier_item["scoring_eligible"])

    def test_future_dated_completed_dossier_cannot_authorize_scored_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path, "v0.3.0")
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            item_ids = [item["item_id"] for item in manifest["frozen_item_set"]["items"]]
            manifest["release_status"] = "citable"
            manifest["release_label"] = "ANX-Bench v0.3.0 scored somatic and ambient anxiety release"
            manifest["official_scored_items"] = item_ids
            manifest["scoring_eligibility"]["official_scored_item_count"] = len(item_ids)
            manifest["scoring_eligibility"]["aggregate_scoring_permitted"] = True

            for manifest_item in manifest["frozen_item_set"]["items"]:
                manifest_item["release_status"] = "approved_scored"
                manifest_item["validation"]["scoring_eligible"] = True
                item_path = tmp_path / manifest_item["path"]
                item = json.loads(item_path.read_text(encoding="utf-8"))
                item["release_status"] = "approved_scored"
                item["validation"]["psychometric_decision"] = "approved_scored"
                item["validation"]["decision_date"] = "2026-06-23"
                item["validation"]["scoring_eligible"] = True
                item_path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
                manifest_item["sha256"] = validate_release.sha256_file(item_path)

            dossier_relative_path = (
                "validation/v0.2/somatic_ambient_anxiety/wave1_calibration_dossier.json"
            )
            dossier_path = tmp_path / dossier_relative_path
            dossier = json.loads(dossier_path.read_text(encoding="utf-8"))
            dossier["dossier_status"] = "approved_scored"
            dossier["sample_provenance"]["development_pilot"]["status"] = "fielded"
            dossier["sample_provenance"]["development_pilot"]["fielding_dates"] = "2026-06-16 to 2026-06-18"
            dossier["sample_provenance"]["confirmation_sample"]["status"] = "fielded"
            dossier["sample_provenance"]["confirmation_sample"]["fielding_dates"] = "2026-06-19 to 2026-06-23"
            dossier["decision"]["psychometric_decision"] = "approved_scored"
            dossier["decision"]["decision_date"] = "2026-06-23"
            dossier["decision"]["scoring_eligible"] = True
            for dossier_item in dossier["items"]:
                dossier_item["release_status"] = "approved_scored"
                dossier_item["psychometric_decision"] = "approved_scored"
                dossier_item["scoring_eligible"] = True
            dossier_path.write_text(json.dumps(dossier, indent=2) + "\n", encoding="utf-8")

            checksum_updates = {
                dossier_relative_path: validate_release.sha256_file(dossier_path),
                **{
                    item["path"]: validate_release.sha256_file(tmp_path / item["path"])
                    for item in manifest["frozen_item_set"]["items"]
                },
            }
            for record in manifest["checksums"]["files"]:
                if record["path"] in checksum_updates:
                    record["sha256"] = checksum_updates[record["path"]]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_release.ReleaseValidationError,
                "future-dated scored-release evidence date 2026-06-23",
            ):
                validate_release.validate_release(
                    manifest_path,
                    validation_run_date=validate_release.date.fromisoformat("2026-06-15"),
                )

    def test_future_dated_citable_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path, "v0.1.0")

            with self.assertRaisesRegex(
                validate_release.ReleaseValidationError,
                "future-dated citable release date 2026-06-15",
            ):
                validate_release.validate_release(
                    manifest_path,
                    validation_run_date=validate_release.date.fromisoformat("2026-06-14"),
                )

    def test_current_scored_somatic_manifest_passes_release_gate_in_clean_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = _copy_release_fixture(Path(tmpdir), "v0.3.1")

            validate_release.validate_release(
                manifest_path,
                validation_run_date=validate_release.date.fromisoformat("2026-06-16"),
            )

    def test_release_gate_fails_when_referenced_dossier_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path)
            dossier_path = (
                tmp_path
                / "validation"
                / "v0.1"
                / "economic_vocational_anxiety"
                / "wave1_calibration_dossier.json"
            )
            dossier_path.unlink()

            with self.assertRaisesRegex(validate_release.ReleaseValidationError, "missing file"):
                validate_release.validate_release(manifest_path)

    def test_release_gate_fails_when_referenced_dossier_json_is_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path)
            dossier_relative_path = (
                "validation/v0.1/economic_vocational_anxiety/wave1_calibration_dossier.json"
            )
            dossier_path = tmp_path / dossier_relative_path
            dossier_path.write_text('{"dossier_schema_version": "v0.1.0",\n', encoding="utf-8")
            _set_checksum(manifest_path, dossier_relative_path)

            with self.assertRaisesRegex(validate_release.ReleaseValidationError, "invalid JSON"):
                validate_release.validate_release(manifest_path)

    def test_release_gate_fails_when_dossier_item_version_is_inconsistent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_release_fixture(tmp_path)
            dossier_relative_path = (
                "validation/v0.1/economic_vocational_anxiety/wave1_calibration_dossier.json"
            )
            dossier_path = tmp_path / dossier_relative_path
            dossier = json.loads(dossier_path.read_text(encoding="utf-8"))
            for item in dossier["items"]:
                if item["item_id"] == "skill_obsolescence_software":
                    item["item_version"] = "v0.1.1"
            dossier_path.write_text(json.dumps(dossier, indent=2) + "\n", encoding="utf-8")
            _set_checksum(manifest_path, dossier_relative_path)

            with self.assertRaisesRegex(validate_release.ReleaseValidationError, "does not include item_id"):
                validate_release.validate_release(manifest_path)


if __name__ == "__main__":
    unittest.main()
