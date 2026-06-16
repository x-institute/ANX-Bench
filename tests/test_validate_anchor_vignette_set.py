import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import validate_anchor_vignette_set  # noqa: E402


SOMATIC_ANCHORS = REPO_ROOT / "anchors" / "v0.2" / "somatic_ambient" / "response_scale_vignettes.json"
WAVE8_ANCHORS = REPO_ROOT / "anchors" / "v0.8" / "full_domain_bridge" / "response_scale_vignettes.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_fixture(tmpdir: str, payload: dict) -> Path:
    path = Path(tmpdir) / "response_scale_vignettes.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


class ValidateAnchorVignetteSetTests(unittest.TestCase):
    def test_v02_somatic_anchor_set_passes(self) -> None:
        validate_anchor_vignette_set.validate_anchor_vignette_set(SOMATIC_ANCHORS)

    def test_v08_full_domain_anchor_set_passes(self) -> None:
        validate_anchor_vignette_set.validate_anchor_vignette_set(WAVE8_ANCHORS)

    def test_duplicate_vignette_ids_fail(self) -> None:
        payload = _load(SOMATIC_ANCHORS)
        payload["vignettes"][1]["vignette_id"] = payload["vignettes"][0]["vignette_id"]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = _write_fixture(tmpdir, payload)
            with self.assertRaisesRegex(
                validate_anchor_vignette_set.AnchorVignetteSetValidationError,
                "duplicate vignette_id",
            ):
                validate_anchor_vignette_set.validate_anchor_vignette_set(path)

    def test_wave8_missing_domain_anchor_fails(self) -> None:
        payload = _load(WAVE8_ANCHORS)
        payload["vignettes"] = [
            vignette
            for vignette in payload["vignettes"]
            if vignette["vignette_id"] != "anchor_epistemic_high"
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = _write_fixture(tmpdir, payload)
            with self.assertRaisesRegex(
                validate_anchor_vignette_set.AnchorVignetteSetValidationError,
                "missing required Wave 8 anchors",
            ):
                validate_anchor_vignette_set.validate_anchor_vignette_set(path)

    def test_vignette_id_must_match_declared_domain_and_severity(self) -> None:
        payload = _load(WAVE8_ANCHORS)
        payload["vignettes"][3]["target_domain"] = "epistemic"

        with tempfile.TemporaryDirectory() as tmpdir:
            path = _write_fixture(tmpdir, payload)
            with self.assertRaisesRegex(
                validate_anchor_vignette_set.AnchorVignetteSetValidationError,
                "declared domain|must equal",
            ):
                validate_anchor_vignette_set.validate_anchor_vignette_set(path)


if __name__ == "__main__":
    unittest.main()
