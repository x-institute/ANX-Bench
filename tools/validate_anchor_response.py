#!/usr/bin/env python3
"""Validate Wave 8 non-scored anchor response exports."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import validate_release


ANCHOR_RESPONSE_SCHEMA_PATH = Path("schema/anchor_response.schema.json")
WAVE_ID = "anx_us_2026w08_full_domain_bridge"
BENCHMARK_VERSION = "v0.8.0"
SEVERITY_ORDER = ("low", "moderate", "high")
DOMAINS = (
    "somatic_ambient",
    "economic_vocational",
    "epistemic",
    "relational",
    "existential_identity",
    "autonomy_surveillance",
    "safety_catastrophic",
)
EXPECTED_ANCHORS = {
    f"anchor_{domain}_{severity}": (domain, severity)
    for domain in DOMAINS
    for severity in SEVERITY_ORDER
}
NON_OBSERVED_MISSINGNESS = {
    "skipped_by_respondent",
    "survey_breakoff",
    "technical_failure",
    "removed_by_quality_control",
    "not_scored_excluded_respondent",
    "not_scored_item_ineligible",
    "item_not_administered_by_design",
}


class AnchorResponseValidationError(Exception):
    """Raised when an anchor response export fails validation."""


def _find_repo_root(anchor_path: Path) -> Path:
    for start in (anchor_path.resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / ANCHOR_RESPONSE_SCHEMA_PATH).is_file():
                return candidate
    return Path.cwd().resolve()


def _csv_scalar(value: str) -> Any:
    stripped = value.strip()
    if stripped == "":
        return None
    lowered = stripped.lower()
    if lowered in {"null", "none"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if stripped.isdigit():
        return int(stripped)
    try:
        return float(stripped)
    except ValueError:
        return stripped


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise AnchorResponseValidationError(
                    f"invalid JSONL in {path}: line {line_number}, column {exc.colno}: {exc.msg}"
                ) from exc
            if not isinstance(row, dict):
                raise AnchorResponseValidationError(f"line {line_number}: anchor response row must be a JSON object")
            rows.append(row)
    return rows


def _load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{key: _csv_scalar(value or "") for key, value in row.items()} for row in reader]


def load_anchor_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return _load_jsonl(path)
    if suffix == ".csv":
        return _load_csv(path)
    raise AnchorResponseValidationError("anchor export must be a .jsonl or .csv file")


def _expected_domain_order_violation(values: dict[str, int | None]) -> bool | None:
    observed = {severity: value for severity, value in values.items() if value is not None}
    if len(observed) < 2:
        return None
    for earlier, later in (("low", "moderate"), ("moderate", "high"), ("low", "high")):
        if earlier in observed and later in observed and observed[earlier] > observed[later]:
            return True
    return False


def _expected_domain_stratum(values: dict[str, int | None]) -> str:
    violation = _expected_domain_order_violation(values)
    observed_values = [values[severity] for severity in SEVERITY_ORDER]
    if violation is True:
        return "nonmonotone"
    if any(value is None for value in observed_values):
        return "incomplete"
    low, _moderate, high = observed_values
    assert low is not None and high is not None
    if all(value in {1, 2} for value in observed_values):
        return "compressed_low"
    if all(value in {4, 5} for value in observed_values):
        return "compressed_high"
    if high - low >= 2:
        return "calibrated_monotone"
    return "weakly_monotone_compressed"


def _expected_overall_stratum(domain_values: dict[str, dict[str, int | None]]) -> str:
    domain_strata = {domain: _expected_domain_stratum(values) for domain, values in domain_values.items()}
    if any(stratum == "nonmonotone" for stratum in domain_strata.values()):
        return "nonmonotone_any_domain"

    complete_domains = [
        domain
        for domain, values in domain_values.items()
        if all(values[severity] is not None for severity in SEVERITY_ORDER)
    ]
    if len(complete_domains) < 6:
        return "anchor_incomplete"

    strata = [domain_strata[domain] for domain in complete_domains]
    if sum(stratum == "calibrated_monotone" for stratum in strata) >= 5:
        return "broadly_calibrated"

    high_values = [domain_values[domain]["high"] for domain in complete_domains]
    low_values = [domain_values[domain]["low"] for domain in complete_domains]
    if (
        sum(stratum in {"compressed_low", "weakly_monotone_compressed"} for stratum in strata) >= 5
        and statistics.median(value for value in high_values if value is not None) <= 3
    ):
        return "globally_compressed_low"
    if (
        sum(stratum in {"compressed_high", "weakly_monotone_compressed"} for stratum in strata) >= 5
        and statistics.median(value for value in low_values if value is not None) >= 3
    ):
        return "globally_compressed_high"
    return "mixed_response_style"


def _valid_datetime(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return parsed.utcoffset() is not None and parsed.utcoffset().total_seconds() == 0


def _check_row_semantics(row: dict[str, Any], index: int) -> list[validate_release.ValidationIssue]:
    issues: list[validate_release.ValidationIssue] = []
    prefix = f"rows/{index}"

    if row.get("wave_id") != WAVE_ID:
        issues.append(validate_release.ValidationIssue(f"{prefix}/wave_id", f"must equal {WAVE_ID!r}"))
    if row.get("benchmark_version") != BENCHMARK_VERSION:
        issues.append(
            validate_release.ValidationIssue(f"{prefix}/benchmark_version", f"must equal {BENCHMARK_VERSION!r}")
        )

    anchor_id = row.get("anchor_id")
    expected = EXPECTED_ANCHORS.get(anchor_id)
    if expected is None:
        issues.append(validate_release.ValidationIssue(f"{prefix}/anchor_id", f"unknown Wave 8 anchor_id {anchor_id!r}"))
    else:
        expected_domain, expected_severity = expected
        if row.get("domain") != expected_domain:
            issues.append(validate_release.ValidationIssue(f"{prefix}/domain", "does not match anchor_id"))
        if row.get("intended_severity") != expected_severity:
            issues.append(validate_release.ValidationIssue(f"{prefix}/intended_severity", "does not match anchor_id"))

    missingness_code = row.get("missingness_code")
    raw_response = row.get("raw_response")
    if missingness_code == "observed" and raw_response is None:
        issues.append(validate_release.ValidationIssue(f"{prefix}/raw_response", "observed rows require raw_response"))
    if missingness_code in NON_OBSERVED_MISSINGNESS and raw_response is not None:
        issues.append(
            validate_release.ValidationIssue(
                f"{prefix}/raw_response", "non-observed missingness codes require null raw_response"
            )
        )
    if not _valid_datetime(row.get("response_timestamp")):
        issues.append(validate_release.ValidationIssue(f"{prefix}/response_timestamp", "must be an ISO 8601 date-time"))
    return issues


def _validate_respondent(rows: list[dict[str, Any]], respondent_id: str) -> list[validate_release.ValidationIssue]:
    issues: list[validate_release.ValidationIssue] = []
    by_anchor: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_anchor[str(row.get("anchor_id"))].append(row)

    missing = sorted(set(EXPECTED_ANCHORS) - set(by_anchor))
    duplicates = sorted(anchor_id for anchor_id, anchor_rows in by_anchor.items() if len(anchor_rows) > 1)
    if missing:
        issues.append(
            validate_release.ValidationIssue(
                f"respondents/{respondent_id}/anchor_id",
                f"missing required Wave 8 anchor rows: {', '.join(missing)}",
            )
        )
    if duplicates:
        issues.append(
            validate_release.ValidationIssue(
                f"respondents/{respondent_id}/anchor_id",
                f"duplicate anchor rows: {', '.join(duplicates)}",
            )
        )

    domain_values = {
        domain: {severity: None for severity in SEVERITY_ORDER}
        for domain in DOMAINS
    }
    for anchor_id, anchor_rows in by_anchor.items():
        if anchor_id not in EXPECTED_ANCHORS or len(anchor_rows) != 1:
            continue
        domain, severity = EXPECTED_ANCHORS[anchor_id]
        raw_response = anchor_rows[0].get("raw_response")
        domain_values[domain][severity] = raw_response if isinstance(raw_response, int) else None

    expected_overall = _expected_overall_stratum(domain_values)
    for domain, values in domain_values.items():
        expected_violation = _expected_domain_order_violation(values)
        expected_domain_stratum = _expected_domain_stratum(values)
        for severity in SEVERITY_ORDER:
            row = by_anchor.get(f"anchor_{domain}_{severity}", [{}])[0]
            if not row:
                continue
            row_label = f"respondents/{respondent_id}/anchor_{domain}_{severity}"
            if row.get("domain_order_violation") != expected_violation:
                issues.append(
                    validate_release.ValidationIssue(
                        f"{row_label}/domain_order_violation",
                        f"expected {expected_violation!r} from observed anchor ratings",
                    )
                )
            if row.get("domain_response_style_stratum") != expected_domain_stratum:
                issues.append(
                    validate_release.ValidationIssue(
                        f"{row_label}/domain_response_style_stratum",
                        f"expected {expected_domain_stratum!r} from observed anchor ratings",
                    )
                )
            if row.get("overall_response_style_stratum") != expected_overall:
                issues.append(
                    validate_release.ValidationIssue(
                        f"{row_label}/overall_response_style_stratum",
                        f"expected {expected_overall!r} from all domain anchor ratings",
                    )
                )
    return issues


def validate_anchor_response(anchor_path: Path) -> None:
    anchor_path = anchor_path.resolve()
    root = _find_repo_root(anchor_path)
    try:
        rows = load_anchor_rows(anchor_path)
        schema = validate_release.load_json(root / ANCHOR_RESPONSE_SCHEMA_PATH)
    except (OSError, validate_release.ReleaseValidationError) as exc:
        raise AnchorResponseValidationError(str(exc)) from exc

    issues: list[validate_release.ValidationIssue] = []
    if not rows:
        issues.append(validate_release.ValidationIssue("$", "anchor export must contain at least one row"))

    by_respondent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(rows):
        issues.extend(validate_release.validate_with_jsonschema(row, schema, str(ANCHOR_RESPONSE_SCHEMA_PATH)))
        if isinstance(row, dict):
            issues.extend(_check_row_semantics(row, index))
            respondent_id = row.get("respondent_id_hash")
            if isinstance(respondent_id, str):
                by_respondent[respondent_id].append(row)
        else:
            issues.append(validate_release.ValidationIssue(f"rows/{index}", "anchor response row must be an object"))

    for respondent_id, respondent_rows in sorted(by_respondent.items()):
        issues.extend(_validate_respondent(respondent_rows, respondent_id))

    if issues:
        rendered = "\n".join(f"- {issue.render()}" for issue in issues)
        raise AnchorResponseValidationError(
            f"anchor response validation failed with {len(issues)} issue(s):\n{rendered}"
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Wave 8 ANX-Bench non-scored anchor export.")
    parser.add_argument("anchor_export", type=Path, help="Path to a JSONL or CSV anchor export")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_anchor_response(args.anchor_export)
    except AnchorResponseValidationError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"validated anchor response export: {args.anchor_export}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
