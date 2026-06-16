import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCORER_PATH = REPO_ROOT / "tools" / "score_wave.py"

spec = importlib.util.spec_from_file_location("score_wave", SCORER_PATH)
score_wave = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["score_wave"] = score_wave
spec.loader.exec_module(score_wave)


def _copy_scoring_fixture(tmp_path: Path) -> Path:
    source_manifest_path = REPO_ROOT / "releases" / "v0.1.0" / "manifest.json"
    manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    required_paths = {
        "schema/wave_response.schema.json",
        "schema/score_output.schema.json",
        "constructs/v0.1/registry.json",
        "releases/v0.1.0/manifest.json",
    }
    required_paths.update(item["path"] for item in manifest["frozen_item_set"]["items"])
    for relative_path in sorted(required_paths):
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path / "releases" / "v0.1.0" / "manifest.json"


def _copy_scoring_fixture_for_release(tmp_path: Path, release_version: str) -> Path:
    source_manifest_path = REPO_ROOT / "releases" / release_version / "manifest.json"
    manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    release_line = ".".join(release_version.split(".")[:2])
    required_paths = {
        "schema/wave_response.schema.json",
        "schema/score_output.schema.json",
        "constructs/v0.1/registry.json",
        f"releases/{release_version}/manifest.json",
    }
    registry_path = f"constructs/{release_line}/registry.json"
    if (REPO_ROOT / registry_path).is_file():
        required_paths.add(registry_path)
    required_paths.update(item["path"] for item in manifest["frozen_item_set"]["items"])
    for relative_path in sorted(required_paths):
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path / "releases" / release_version / "manifest.json"


def _row(**overrides):
    base = {
        "wave_id": "anx_us_2026w01",
        "benchmark_version": "v0.1.0",
        "item_id": "skill_obsolescence_software",
        "item_version": "v0.1.0",
        "respondent_id_hash": "a" * 64,
        "raw_response": 4,
        "scored_value": 4,
        "response_timestamp": "2026-06-15T12:00:00Z",
        "administration_mode": "web",
        "language": "en-US",
        "survey_weight": 1.0,
        "exclusion_flags": [],
        "missingness_code": "observed",
    }
    base.update(overrides)
    return base


def _somatic_row(item_id: str, respondent: str, response: int, **overrides):
    base = {
        "wave_id": "anx_us_2026w03",
        "benchmark_version": "v0.3.1",
        "item_id": item_id,
        "item_version": "v0.2.0",
        "respondent_id_hash": respondent * 64,
        "raw_response": response,
        "scored_value": response,
        "response_timestamp": "2026-06-23T12:00:00Z",
        "administration_mode": "web",
        "language": "en-US",
        "survey_weight": 1.0,
        "exclusion_flags": [],
        "missingness_code": "observed",
    }
    base.update(overrides)
    return base


def _write_jsonl(path: Path, rows: list[dict]) -> Path:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


class ScoreWaveTests(unittest.TestCase):
    def test_v010_development_rows_validate_but_do_not_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_scoring_fixture(tmp_path)
            wave_path = _write_jsonl(
                tmp_path / "wave.jsonl",
                [
                    _row(respondent_id_hash="a" * 64, raw_response=4, scored_value=4),
                    _row(respondent_id_hash="b" * 64, raw_response="2", scored_value=2),
                ],
            )

            output = score_wave.score_wave(wave_path, manifest_path)

            self.assertFalse(output["aggregate_scoring_permitted"])
            self.assertEqual(output["official_scored_item_count"], 0)
            self.assertEqual(output["overall_score"], None)
            self.assertEqual(output["construct_scores"], [])
            self.assertEqual(output["domain_scores"], [])
            self.assertEqual(output["row_count"], 2)
            self.assertEqual(output["included_row_count"], 0)
            self.assertEqual(output["scoring_ineligible_row_count"], 2)
            item_score = output["item_scores"][0]
            self.assertEqual(item_score["item_id"], "skill_obsolescence_software")
            self.assertFalse(item_score["official_scored"])
            self.assertFalse(item_score["scoring_eligible"])
            self.assertFalse(item_score["included_in_aggregate"])
            self.assertEqual(item_score["point_estimate"], None)

    def test_wrong_benchmark_version_is_fatal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_scoring_fixture(tmp_path)
            wave_path = _write_jsonl(tmp_path / "wave.jsonl", [_row(benchmark_version="v0.1.1")])

            with self.assertRaisesRegex(score_wave.ScoringError, "benchmark_version"):
                score_wave.score_wave(wave_path, manifest_path)

    def test_item_version_mismatch_is_fatal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_scoring_fixture(tmp_path)
            wave_path = _write_jsonl(tmp_path / "wave.jsonl", [_row(item_version="v0.1.1")])

            with self.assertRaisesRegex(score_wave.ScoringError, "item_version"):
                score_wave.score_wave(wave_path, manifest_path)

    def test_invalid_raw_scored_mapping_is_fatal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_scoring_fixture(tmp_path)
            wave_path = _write_jsonl(tmp_path / "wave.jsonl", [_row(raw_response=5, scored_value=4)])

            with self.assertRaisesRegex(score_wave.ScoringError, "does not match recomputed score"):
                score_wave.score_wave(wave_path, manifest_path)

    def test_excluded_rows_are_counted_but_never_contribute(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_scoring_fixture(tmp_path)
            wave_path = _write_jsonl(
                tmp_path / "wave.jsonl",
                [
                    _row(
                        exclusion_flags=["attention_check_failed"],
                        missingness_code="observed",
                        raw_response=5,
                        scored_value=5,
                    )
                ],
            )

            output = score_wave.score_wave(wave_path, manifest_path)

            self.assertEqual(output["included_row_count"], 0)
            self.assertEqual(output["exclusion_counts"], {"attention_check_failed": 1})
            self.assertEqual(output["item_scores"][0]["included_row_count"], 0)
            self.assertEqual(output["item_scores"][0]["exclusion_counts"], {"attention_check_failed": 1})
            self.assertEqual(output["item_scores"][0]["point_estimate"], None)

    def test_v031_scored_somatic_wave_produces_construct_and_domain_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_scoring_fixture_for_release(tmp_path, "v0.3.1")
            wave_path = _write_jsonl(
                tmp_path / "wave.jsonl",
                [
                    _somatic_row("sleep_disruption_ai_news", "a", 4),
                    _somatic_row("body_vigilance_model_release", "a", 3),
                    _somatic_row("background_dread_ai_progress", "a", 5),
                    _somatic_row("avoidance_after_ai_capability_demo", "a", 4),
                    _somatic_row("sleep_disruption_ai_news", "b", 2),
                    _somatic_row("body_vigilance_model_release", "b", 2),
                    _somatic_row("background_dread_ai_progress", "b", 3),
                    _somatic_row("avoidance_after_ai_capability_demo", "b", 2),
                ],
            )

            output = score_wave.score_wave(wave_path, manifest_path)

            self.assertTrue(output["aggregate_scoring_permitted"])
            self.assertEqual(4, output["official_scored_item_count"])
            self.assertEqual(8, output["included_row_count"])
            self.assertEqual(0, output["scoring_ineligible_row_count"])
            self.assertEqual(1, len(output["construct_scores"]))
            self.assertEqual("somatic_ambient_anxiety", output["construct_scores"][0]["id"])
            self.assertIsNotNone(output["construct_scores"][0]["point_estimate"])
            self.assertEqual(1, len(output["domain_scores"]))
            self.assertEqual("somatic_ambient", output["domain_scores"][0]["id"])
            self.assertIsNotNone(output["domain_scores"][0]["point_estimate"])

    def test_v031_non_official_rows_do_not_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            manifest_path = _copy_scoring_fixture_for_release(tmp_path, "v0.3.1")
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["official_scored_items"].remove("avoidance_after_ai_capability_demo")
            manifest["scoring_eligibility"]["official_scored_item_count"] = 3
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            wave_path = _write_jsonl(
                tmp_path / "wave.jsonl",
                [
                    _somatic_row("sleep_disruption_ai_news", "a", 4),
                    _somatic_row("body_vigilance_model_release", "a", 3),
                    _somatic_row("background_dread_ai_progress", "a", 5),
                    _somatic_row("avoidance_after_ai_capability_demo", "a", 4),
                ],
            )

            output = score_wave.score_wave(wave_path, manifest_path)

            omitted = next(
                item for item in output["item_scores"] if item["item_id"] == "avoidance_after_ai_capability_demo"
            )
            self.assertFalse(omitted["official_scored"])
            self.assertTrue(omitted["scoring_eligible"])
            self.assertFalse(omitted["included_in_aggregate"])
            self.assertEqual(3, output["included_row_count"])


if __name__ == "__main__":
    unittest.main()
