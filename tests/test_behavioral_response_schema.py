import json
import unittest
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schema" / "behavioral_response.schema.json"


def _valid_row() -> dict:
    return {
        "wave_id": "anx_us_2026w02_somatic",
        "respondent_id": "a" * 64,
        "task_id": "revealed_ai_review_allocation_v1",
        "benchmark_version": "v0.2.3",
        "randomized_arm": "healthcare_triage",
        "allocation_mode": "real_bonus",
        "ai_only_review_cents": 35,
        "human_review_cents": 65,
        "allocation_total_cents": 100,
        "allocation_confirmed": True,
        "behavioral_comprehension_response": 1,
        "behavioral_comprehension_passed": True,
        "exclusion_flags": [],
        "missingness_code": "observed",
        "revealed_anxiety_score": 0.65,
    }


class BehavioralResponseSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        try:
            from jsonschema import Draft202012Validator
        except ModuleNotFoundError:
            cls.validator = None
        else:
            cls.validator = Draft202012Validator(cls.schema)

    def assert_schema_valid(self, row: dict) -> None:
        errors = self._schema_errors(row)
        self.assertEqual([], errors)

    def assert_schema_invalid(self, row: dict) -> None:
        errors = self._schema_errors(row)
        self.assertNotEqual([], errors)

    def _schema_errors(self, row: dict) -> list[str]:
        if self.validator is not None:
            return [error.message for error in self.validator.iter_errors(row)]

        errors = []
        required = set(self.schema["required"])
        missing = sorted(required - set(row))
        errors.extend(f"missing {field}" for field in missing)

        if set(row) - set(self.schema["properties"]):
            errors.append("additional properties")
        if row.get("task_id") != "revealed_ai_review_allocation_v1":
            errors.append("bad task_id")
        if row.get("randomized_arm") not in self.schema["properties"]["randomized_arm"]["enum"]:
            errors.append("bad randomized_arm")
        if row.get("allocation_mode") not in self.schema["properties"]["allocation_mode"]["enum"]:
            errors.append("bad allocation_mode")
        if row.get("missingness_code") not in self.schema["properties"]["missingness_code"]["enum"]:
            errors.append("bad missingness_code")

        if row.get("missingness_code") == "observed":
            if row.get("allocation_total_cents") != 100:
                errors.append("observed allocation total must equal 100")
            if row.get("allocation_confirmed") is not True:
                errors.append("observed allocation must be confirmed")
            if row.get("behavioral_comprehension_passed") is not True:
                errors.append("observed row must pass comprehension")
            if not isinstance(row.get("revealed_anxiety_score"), (int, float)):
                errors.append("observed row must have revealed score")
        else:
            if row.get("revealed_anxiety_score") is not None:
                errors.append("non-observed row must not have revealed score")

        return errors

    def test_valid_observed_behavioral_response_row(self) -> None:
        self.assert_schema_valid(_valid_row())

    def test_invalid_when_observed_allocation_total_is_bad(self) -> None:
        row = _valid_row()
        row["allocation_total_cents"] = 90

        self.assert_schema_invalid(row)

    def test_invalid_when_observed_comprehension_failed(self) -> None:
        row = _valid_row()
        row["behavioral_comprehension_response"] = 2
        row["behavioral_comprehension_passed"] = False
        row["exclusion_flags"] = ["behavioral_comprehension_failed"]

        self.assert_schema_invalid(row)

    def test_invalid_when_non_observed_missingness_has_score(self) -> None:
        row = deepcopy(_valid_row())
        row["ai_only_review_cents"] = None
        row["human_review_cents"] = None
        row["allocation_total_cents"] = None
        row["allocation_confirmed"] = False
        row["behavioral_comprehension_response"] = None
        row["behavioral_comprehension_passed"] = None
        row["exclusion_flags"] = ["behavioral_task_not_presented"]
        row["missingness_code"] = "not_presented_by_design"
        row["revealed_anxiety_score"] = 0.65

        self.assert_schema_invalid(row)


if __name__ == "__main__":
    unittest.main()
