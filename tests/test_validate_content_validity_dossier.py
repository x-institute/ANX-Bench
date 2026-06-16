import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_content_validity_dossier.py"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "content_validity"
TEMPLATE_PATH = (
    REPO_ROOT
    / "validation"
    / "v0.7"
    / "cross_domain_bridge"
    / "content_validity_dossier.template.json"
)

spec = importlib.util.spec_from_file_location("validate_content_validity_dossier", VALIDATOR_PATH)
validate_content_validity_dossier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_content_validity_dossier"] = validate_content_validity_dossier
spec.loader.exec_module(validate_content_validity_dossier)


class ContentValidityDossierValidatorTests(unittest.TestCase):
    def assert_validates(self, path: Path) -> None:
        validate_content_validity_dossier.validate_content_validity_dossier(path, repo_root=REPO_ROOT)

    def assert_fails(self, path: Path, expected_text: str) -> None:
        with self.assertRaises(validate_content_validity_dossier.ContentValidityDossierError) as raised:
            validate_content_validity_dossier.validate_content_validity_dossier(path, repo_root=REPO_ROOT)
        self.assertIn(expected_text, str(raised.exception))

    def test_pending_template_validates_without_promotion(self) -> None:
        self.assert_validates(TEMPLATE_PATH)

    def test_under_review_dossier_validates_as_non_promoting(self) -> None:
        self.assert_validates(FIXTURE_DIR / "under_review_dossier.json")

    def test_failed_cvi_blocks_scored_promotion(self) -> None:
        self.assert_fails(FIXTURE_DIR / "fail_low_cvi_dossier.json", "overall_item_cvi")
        self.assert_fails(FIXTURE_DIR / "fail_low_cvi_dossier.json", "scored_promotion_eligible")

    def test_unresolved_ethics_and_overlap_flags_block_promotion(self) -> None:
        self.assert_fails(FIXTURE_DIR / "fail_unresolved_flags_dossier.json", "construct_overlap_resolved")
        self.assert_fails(FIXTURE_DIR / "fail_unresolved_flags_dossier.json", "harm_ethics_resolved")

    def test_valid_completed_dossier_passes_promotion_gate(self) -> None:
        self.assert_validates(FIXTURE_DIR / "valid_completed_dossier.json")


if __name__ == "__main__":
    unittest.main()
