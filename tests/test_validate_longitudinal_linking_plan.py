import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = REPO_ROOT / "linking" / "v0.8" / "anx_us_2026w08_full_domain_linking_plan.template.json"
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_longitudinal_linking_plan.py"

spec = importlib.util.spec_from_file_location("validate_longitudinal_linking_plan", VALIDATOR_PATH)
validate_longitudinal_linking_plan = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_longitudinal_linking_plan"] = validate_longitudinal_linking_plan
spec.loader.exec_module(validate_longitudinal_linking_plan)


def _template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _write_temp(payload: dict) -> Path:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False, dir=REPO_ROOT)
    with handle:
        json.dump(payload, handle)
    return Path(handle.name)


class LongitudinalLinkingPlanValidatorTests(unittest.TestCase):
    def test_wave8_template_passes(self) -> None:
        issues = validate_longitudinal_linking_plan.validate_plan(TEMPLATE_PATH)
        self.assertEqual([], issues)

    def test_missing_anchors_fail_minimum_overlap(self) -> None:
        plan = _template()
        plan["anchor_items"] = plan["anchor_items"][:2]
        path = _write_temp(plan)
        try:
            issues = validate_longitudinal_linking_plan.validate_plan(path)
        finally:
            path.unlink(missing_ok=True)
        rendered = "\n".join(issue.render() for issue in issues)
        self.assertIn("anchor_items", rendered)

    def test_changed_item_version_without_bridge_evidence_fails(self) -> None:
        plan = _template()
        plan["anchor_items"][0]["target"]["item_version"] = "v0.8.0"
        plan["anchor_items"][0]["item_version_continuity"] = "changed_item_version_requires_bridge_evidence"
        plan["anchor_items"][0]["bridge_evidence_path"] = None
        path = _write_temp(plan)
        try:
            issues = validate_longitudinal_linking_plan.validate_plan(path)
        finally:
            path.unlink(missing_ok=True)
        rendered = "\n".join(issue.render() for issue in issues)
        self.assertIn("changed item versions require observed bridge evidence", rendered)

    def test_unauthorized_longitudinal_claim_fails(self) -> None:
        plan = _template()
        plan["claim_authorization"]["permitted_claims"].append("Wave 8 shows a longitudinal increase in somatic AI anxiety relative to v0.3.1.")
        path = _write_temp(plan)
        try:
            issues = validate_longitudinal_linking_plan.validate_plan(path)
        finally:
            path.unlink(missing_ok=True)
        rendered = "\n".join(issue.render() for issue in issues)
        self.assertIn("unauthorized longitudinal", rendered)


if __name__ == "__main__":
    unittest.main()
