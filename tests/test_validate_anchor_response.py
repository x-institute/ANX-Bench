import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import validate_anchor_response  # noqa: E402


RESPONDENT_ID = "a" * 64
DOMAINS = validate_anchor_response.DOMAINS
SEVERITY_ORDER = validate_anchor_response.SEVERITY_ORDER


def _domain_strata(values_by_domain: dict[str, dict[str, int | None]]) -> dict[str, str]:
    return {
        domain: validate_anchor_response._expected_domain_stratum(values)
        for domain, values in values_by_domain.items()
    }


def _rows(values_by_domain: dict[str, dict[str, int | None]]) -> list[dict[str, object]]:
    overall = validate_anchor_response._expected_overall_stratum(values_by_domain)
    strata = _domain_strata(values_by_domain)
    rows: list[dict[str, object]] = []
    for domain in DOMAINS:
        violation = validate_anchor_response._expected_domain_order_violation(values_by_domain[domain])
        for severity in SEVERITY_ORDER:
            raw_response = values_by_domain[domain][severity]
            rows.append(
                {
                    "wave_id": "anx_us_2026w08_full_domain_bridge",
                    "benchmark_version": "v0.8.0",
                    "respondent_id_hash": RESPONDENT_ID,
                    "anchor_id": f"anchor_{domain}_{severity}",
                    "domain": domain,
                    "intended_severity": severity,
                    "raw_response": raw_response,
                    "missingness_code": "observed" if raw_response is not None else "skipped_by_respondent",
                    "response_timestamp": "2026-06-16T18:30:00Z",
                    "survey_weight": 1.0,
                    "domain_order_violation": violation,
                    "domain_response_style_stratum": strata[domain],
                    "overall_response_style_stratum": overall,
                }
            )
    return rows


def _valid_values() -> dict[str, dict[str, int | None]]:
    return {domain: {"low": 2, "moderate": 3, "high": 4} for domain in DOMAINS}


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class ValidateAnchorResponseTests(unittest.TestCase):
    def test_valid_jsonl_anchor_export_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "anchors.jsonl"
            _write_jsonl(path, _rows(_valid_values()))

            validate_anchor_response.validate_anchor_response(path)

    def test_valid_csv_anchor_export_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "anchors.csv"
            _write_csv(path, _rows(_valid_values()))

            validate_anchor_response.validate_anchor_response(path)

    def test_nonmonotone_fixture_must_carry_derived_flags(self) -> None:
        values = _valid_values()
        values["somatic_ambient"] = {"low": 4, "moderate": 3, "high": 5}
        rows = _rows(values)
        for row in rows:
            if row["domain"] == "somatic_ambient":
                row["domain_order_violation"] = False
                row["domain_response_style_stratum"] = "calibrated_monotone"
            row["overall_response_style_stratum"] = "broadly_calibrated"

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nonmonotone_miscoded.jsonl"
            _write_jsonl(path, rows)

            with self.assertRaisesRegex(
                validate_anchor_response.AnchorResponseValidationError,
                "domain_order_violation|nonmonotone_any_domain",
            ):
                validate_anchor_response.validate_anchor_response(path)

    def test_incomplete_fixture_passes_when_missingness_and_strata_are_consistent(self) -> None:
        values = _valid_values()
        values["somatic_ambient"]["high"] = None
        values["economic_vocational"]["moderate"] = None

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "incomplete.jsonl"
            _write_jsonl(path, _rows(values))

            validate_anchor_response.validate_anchor_response(path)

    def test_missing_required_anchor_row_fails(self) -> None:
        rows = _rows(_valid_values())[:-1]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "missing_anchor.jsonl"
            _write_jsonl(path, rows)

            with self.assertRaisesRegex(
                validate_anchor_response.AnchorResponseValidationError,
                "missing required Wave 8 anchor rows",
            ):
                validate_anchor_response.validate_anchor_response(path)

    def test_invalid_anchor_id_fixture_fails(self) -> None:
        rows = _rows(_valid_values())
        rows[0]["anchor_id"] = "anchor_somatic_ambient_extreme"

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "invalid_anchor_id.jsonl"
            _write_jsonl(path, rows)

            with self.assertRaisesRegex(
                validate_anchor_response.AnchorResponseValidationError,
                "anchor_id|unknown Wave 8 anchor_id",
            ):
                validate_anchor_response.validate_anchor_response(path)


if __name__ == "__main__":
    unittest.main()
