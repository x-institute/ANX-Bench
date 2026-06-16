#!/usr/bin/env python3
"""Validate ANX-Bench v0.3.1 14-day test-retest evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path("schema/retest_evidence.schema.json")
ALLOWED_ITEM_IDS = {
    "sleep_disruption_ai_news",
    "body_vigilance_model_release",
    "background_dread_ai_progress",
    "avoidance_after_ai_capability_demo",
}
EXPECTED_ITEM_VERSIONS = {item_id: "v0.2.0" for item_id in ALLOWED_ITEM_IDS}
EXPECTED_BENCHMARK_VERSION = "v0.3.1"
EXPECTED_EVENT_ID = "no_event"


class RetestEvidenceError(Exception):
    """Raised when a retest evidence packet fails validation."""


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise RetestEvidenceError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RetestEvidenceError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(evidence_path: Path) -> Path:
    search_start = evidence_path.resolve().parent
    for candidate in (search_start, *search_start.parents):
        if (candidate / SCHEMA_PATH).is_file():
            return candidate
    return Path.cwd().resolve()


def validate_with_jsonschema(instance: Any, schema: dict[str, Any]) -> list[ValidationIssue]:
    try:
        from jsonschema import Draft202012Validator
    except ModuleNotFoundError:
        return validate_with_builtin_schema(instance, schema)

    validator = Draft202012Validator(schema)
    issues: list[ValidationIssue] = []
    for error in sorted(validator.iter_errors(instance), key=lambda err: list(err.path)):
        location = "/".join(str(part) for part in error.path) or "$"
        issues.append(ValidationIssue(location, error.message))
    return issues


def validate_with_builtin_schema(instance: Any, schema: dict[str, Any]) -> list[ValidationIssue]:
    """Validate the JSON Schema subset used by the retest evidence schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise RetestEvidenceError(f"unsupported external JSON Schema reference: {ref}")
        current: Any = schema
        for part in ref[2:].split("/"):
            current = current[part]
        return current

    def type_matches(value: Any, expected: str) -> bool:
        if expected == "boolean":
            return isinstance(value, bool)
        if expected == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if expected == "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if expected == "string":
            return isinstance(value, str)
        if expected == "array":
            return isinstance(value, list)
        if expected == "object":
            return isinstance(value, dict)
        if expected == "null":
            return value is None
        raise RetestEvidenceError(f"unsupported JSON Schema type: {expected}")

    def check(value: Any, subschema: dict[str, Any], path: str) -> None:
        if "$ref" in subschema:
            check(value, resolve_ref(subschema["$ref"]), path)
            return

        expected_type = subschema.get("type")
        if expected_type is not None:
            expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
            if not any(type_matches(value, candidate) for candidate in expected_types):
                issues.append(
                    ValidationIssue(
                        path,
                        f"expected type {' or '.join(expected_types)}, got {type(value).__name__}",
                    )
                )
                return

        if "const" in subschema and value != subschema["const"]:
            issues.append(ValidationIssue(path, f"expected constant {subschema['const']!r}"))
            return

        if "enum" in subschema and value not in subschema["enum"]:
            issues.append(ValidationIssue(path, f"value {value!r} is not in enum"))

        if isinstance(value, str):
            if "minLength" in subschema and len(value) < subschema["minLength"]:
                issues.append(ValidationIssue(path, "string is shorter than minLength"))
            if "pattern" in subschema and re.fullmatch(subschema["pattern"], value) is None:
                issues.append(ValidationIssue(path, "string does not match pattern"))
            if subschema.get("format") == "date":
                try:
                    date.fromisoformat(value)
                except ValueError:
                    issues.append(ValidationIssue(path, "string is not an ISO date"))

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in subschema and value < subschema["minimum"]:
                issues.append(ValidationIssue(path, "number is below minimum"))
            if "maximum" in subschema and value > subschema["maximum"]:
                issues.append(ValidationIssue(path, "number is above maximum"))

        if isinstance(value, list):
            if "minItems" in subschema and len(value) < subschema["minItems"]:
                issues.append(ValidationIssue(path, "array has too few items"))
            if "maxItems" in subschema and len(value) > subschema["maxItems"]:
                issues.append(ValidationIssue(path, "array has too many items"))
            if subschema.get("uniqueItems") is True and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
                issues.append(ValidationIssue(path, "array items are not unique"))
            if "items" in subschema:
                for index, item in enumerate(value):
                    check(item, subschema["items"], f"{path}/{index}")

        if isinstance(value, dict):
            for key in subschema.get("required", []):
                if key not in value:
                    issues.append(ValidationIssue(path, f"missing required property {key!r}"))

            properties = subschema.get("properties", {})
            for key, item in value.items():
                if key in properties:
                    check(item, properties[key], f"{path}/{key}")
                elif subschema.get("additionalProperties") is False:
                    issues.append(ValidationIssue(path, f"unexpected property {key!r}"))
                elif isinstance(subschema.get("additionalProperties"), dict):
                    check(item, subschema["additionalProperties"], f"{path}/{key}")

    check(instance, schema, "$")
    return issues


def _num(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def _all_present(*values: Any) -> bool:
    return all(value is not None for value in values)


def _check_label(path: str, observed: Any, expected: str | None, issues: list[ValidationIssue]) -> None:
    if expected is None:
        if observed is not None:
            issues.append(ValidationIssue(path, "decision must be null until all required observed results are present"))
    elif observed != expected:
        issues.append(ValidationIssue(path, f"decision must be {expected!r} from preregistered thresholds"))


def expected_icc_decision(evidence: dict[str, Any]) -> str | None:
    icc = evidence.get("icc_2_1", {})
    thresholds = evidence.get("thresholds", {}).get("construct", {})
    analytic_n = _int(icc.get("analytic_n"))
    estimate = _num(icc.get("estimate"))
    lower = _num(icc.get("ci_95_lower"))
    if not _all_present(analytic_n, estimate, lower):
        return None
    if (
        analytic_n >= thresholds["minimum_complete_pair_n"]
        and estimate >= thresholds["minimum_icc_2_1"]
        and lower >= thresholds["minimum_icc_95ci_lower"]
    ):
        return "pass"
    return "fail"


def expected_mean_change_decision(evidence: dict[str, Any]) -> str | None:
    mean_change = evidence.get("mean_change", {})
    thresholds = evidence.get("thresholds", {}).get("construct", {})
    change = _num(mean_change.get("weighted_mean_change"))
    lower = _num(mean_change.get("ci_95_lower"))
    upper = _num(mean_change.get("ci_95_upper"))
    srm = _num(mean_change.get("standardized_response_mean"))
    if not _all_present(change, lower, upper, srm):
        return None
    if (
        abs(change) <= thresholds["maximum_abs_weighted_mean_change"]
        and lower >= thresholds["mean_change_ci_low_minimum"]
        and upper <= thresholds["mean_change_ci_high_maximum"]
        and abs(srm) <= thresholds["maximum_abs_standardized_response_mean"]
    ):
        return "pass"
    return "fail"


def expected_item_decision(evidence: dict[str, Any], item: dict[str, Any]) -> str | None:
    thresholds = evidence.get("thresholds", {}).get("item", {})
    correlation = _num(item.get("unweighted_stability_correlation"))
    mean_change = _num(item.get("weighted_mean_change"))
    exact = _num(item.get("weighted_exact_agreement"))
    adjacent = _num(item.get("weighted_adjacent_agreement"))
    moved = _num(item.get("weighted_two_or_more_category_move_share"))
    missing = _num(item.get("missing_or_unusable_retest_rate"))
    if not _all_present(correlation, mean_change, exact, adjacent, moved, missing):
        return None
    agreement_passes = (
        exact >= thresholds["minimum_weighted_exact_agreement"]
        or adjacent >= thresholds["minimum_weighted_adjacent_agreement"]
    )
    if (
        correlation >= thresholds["minimum_unweighted_stability_correlation"]
        and abs(mean_change) <= thresholds["maximum_abs_weighted_mean_change"]
        and agreement_passes
        and moved <= thresholds["maximum_weighted_two_or_more_category_move_share"]
        and missing <= thresholds["maximum_missing_or_unusable_rate"]
    ):
        return "pass"
    return "fail"


def expected_attrition_decision(evidence: dict[str, Any]) -> str | None:
    attrition = evidence.get("attrition_diagnostics", {})
    thresholds = evidence.get("thresholds", {}).get("attrition", {})
    points = _num(attrition.get("wave1_construct_mean_difference_points"))
    sd = _num(attrition.get("wave1_construct_mean_difference_sd"))
    sensitive = attrition.get("attrition_sensitive")
    weighted = attrition.get("attrition_adjusted_weighting_applied")
    if not _all_present(points, sd) or sensitive is None or weighted is None:
        return None
    derived_sensitive = (
        abs(points) > thresholds["attrition_sensitive_mean_difference_greater_than_points"]
        or abs(sd) > thresholds["attrition_sensitive_mean_difference_greater_than_sd"]
    )
    if sensitive != derived_sensitive:
        return "fail"
    if derived_sensitive:
        return "caution" if weighted else "fail"
    return "pass"


def expected_invariance_decision(evidence: dict[str, Any]) -> str | None:
    invariance = evidence.get("longitudinal_invariance", {})
    thresholds = evidence.get("thresholds", {}).get("longitudinal_invariance", {})
    configural = invariance.get("configural_converged")
    one_factor = invariance.get("configural_one_factor_preserved")
    metric_cfi = _num(invariance.get("metric_delta_cfi"))
    metric_rmsea = _num(invariance.get("metric_delta_rmsea"))
    scalar_cfi = _num(invariance.get("scalar_delta_cfi"))
    scalar_rmsea = _num(invariance.get("scalar_delta_rmsea"))
    score_impact = _num(invariance.get("max_expected_construct_score_impact"))
    residual = _num(invariance.get("max_same_item_residual_correlation"))
    if not _all_present(configural, one_factor, metric_cfi, metric_rmsea, scalar_cfi, scalar_rmsea, score_impact, residual):
        return None
    if not configural or not one_factor:
        return "fail"
    if metric_cfi < thresholds["metric_delta_cfi_minimum"] or metric_rmsea > thresholds["metric_delta_rmsea_maximum"]:
        return "fail"
    scalar_passes = scalar_cfi >= thresholds["scalar_delta_cfi_minimum"] and scalar_rmsea <= thresholds["scalar_delta_rmsea_maximum"]
    drift_passes = (
        score_impact <= thresholds["maximum_expected_score_impact"]
        and residual <= thresholds["maximum_same_item_residual_correlation"]
    )
    if scalar_passes and drift_passes:
        return "pass"
    return "caution"


def expected_panel_conditioning_decision(evidence: dict[str, Any]) -> str | None:
    panel = evidence.get("panel_conditioning_sensitivity", {})
    thresholds = evidence.get("thresholds", {}).get("panel_conditioning", {})
    primary_icc_decision = expected_icc_decision(evidence)
    conditioning_icc = _num(panel.get("conditioning_excluded_icc"))
    mean_change_difference = _num(panel.get("absolute_mean_change_difference"))
    sensitive = panel.get("panel_conditioning_sensitive")
    if not _all_present(conditioning_icc, mean_change_difference) or sensitive is None:
        return None
    derived_sensitive = (
        (primary_icc_decision == "pass" and conditioning_icc < thresholds["minimum_conditioning_excluded_icc_if_primary_passes"])
        or mean_change_difference > thresholds["maximum_abs_weighted_mean_change_difference"]
    )
    if sensitive != derived_sensitive:
        return "fail"
    return "caution" if derived_sensitive else "pass"


def expected_construct_decision(evidence: dict[str, Any], component_decisions: dict[str, str | None]) -> str | None:
    required = [
        component_decisions["icc"],
        component_decisions["mean_change"],
        component_decisions["attrition"],
        component_decisions["invariance"],
        component_decisions["panel_conditioning"],
    ]
    if any(decision is None for decision in required):
        return None
    if any(decision == "fail" for decision in required):
        return "fail"
    if any(decision == "caution" for decision in required):
        return "caution"
    return "pass"


def expected_overall_decision(construct_decision: str | None, item_decisions: list[str | None]) -> str | None:
    if construct_decision is None or any(decision is None for decision in item_decisions):
        return None
    failed_items = sum(decision == "fail" for decision in item_decisions)
    if construct_decision == "fail" or failed_items >= 2:
        return "fail"
    if construct_decision == "caution" or failed_items == 1:
        return "caution"
    return "pass"


def validate_retest_evidence(evidence_path: Path, *, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(evidence_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    evidence = load_json(evidence_path)
    if not isinstance(evidence, dict):
        raise RetestEvidenceError("retest evidence root must be a JSON object")

    issues: list[ValidationIssue] = []
    issues.extend(validate_with_jsonschema(evidence, schema))
    issues.extend(validate_contract(evidence))
    issues.extend(validate_decisions(evidence))

    if issues:
        rendered = "\n".join(f"  - {issue.render()}" for issue in issues)
        raise RetestEvidenceError(f"retest evidence failed validation:\n{rendered}")


def validate_contract(evidence: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if evidence.get("benchmark_version") != EXPECTED_BENCHMARK_VERSION:
        issues.append(ValidationIssue("benchmark_version", "must be exactly v0.3.1"))
    if evidence.get("event_id") != EXPECTED_EVENT_ID:
        issues.append(ValidationIssue("event_id", "must be no_event for the preregistered retest"))

    evidence_date = evidence.get("evidence_date")
    if isinstance(evidence_date, str):
        try:
            parsed_date = date.fromisoformat(evidence_date)
        except ValueError:
            issues.append(ValidationIssue("evidence_date", "must be an ISO date"))
        else:
            if parsed_date > date.today():
                issues.append(ValidationIssue("evidence_date", "must not be in the future"))
    else:
        issues.append(ValidationIssue("evidence_date", "must be an ISO date string"))

    frozen_item_ids = evidence.get("frozen_item_ids")
    if set(frozen_item_ids or []) != ALLOWED_ITEM_IDS:
        issues.append(ValidationIssue("frozen_item_ids", "must exactly match the four approved v0.3.1 somatic items"))
    if evidence.get("frozen_item_versions") != EXPECTED_ITEM_VERSIONS:
        issues.append(ValidationIssue("frozen_item_versions", "must map every approved item to v0.2.0"))

    item_rows = evidence.get("item_stability", [])
    if isinstance(item_rows, list):
        row_ids = {row.get("item_id") for row in item_rows if isinstance(row, dict)}
        if row_ids != ALLOWED_ITEM_IDS:
            issues.append(ValidationIssue("item_stability", "must cover exactly the four approved item IDs"))

    restrictions = evidence.get("reporting_restrictions", {})
    for field in (
        "event_study_claim_permitted",
        "trend_claim_permitted",
        "causal_shock_claim_permitted",
        "longer_interval_longitudinal_claim_permitted",
    ):
        if isinstance(restrictions, dict) and restrictions.get(field) is not False:
            issues.append(ValidationIssue(f"reporting_restrictions/{field}", "must be false for retest evidence"))

    return issues


def validate_decisions(evidence: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    icc_decision = expected_icc_decision(evidence)
    mean_change_decision = expected_mean_change_decision(evidence)
    attrition_decision = expected_attrition_decision(evidence)
    invariance_decision = expected_invariance_decision(evidence)
    panel_decision = expected_panel_conditioning_decision(evidence)
    component_decisions = {
        "icc": icc_decision,
        "mean_change": mean_change_decision,
        "attrition": attrition_decision,
        "invariance": invariance_decision,
        "panel_conditioning": panel_decision,
    }

    _check_label("icc_2_1/decision", evidence.get("icc_2_1", {}).get("decision"), icc_decision, issues)
    _check_label("mean_change/decision", evidence.get("mean_change", {}).get("decision"), mean_change_decision, issues)
    _check_label(
        "attrition_diagnostics/decision",
        evidence.get("attrition_diagnostics", {}).get("decision"),
        attrition_decision,
        issues,
    )
    _check_label(
        "longitudinal_invariance/decision",
        evidence.get("longitudinal_invariance", {}).get("decision"),
        invariance_decision,
        issues,
    )
    _check_label(
        "panel_conditioning_sensitivity/decision",
        evidence.get("panel_conditioning_sensitivity", {}).get("decision"),
        panel_decision,
        issues,
    )

    item_decisions: list[str | None] = []
    for index, item in enumerate(evidence.get("item_stability", [])):
        if not isinstance(item, dict):
            continue
        decision = expected_item_decision(evidence, item)
        item_decisions.append(decision)
        _check_label(f"item_stability/{index}/decision", item.get("decision"), decision, issues)

    construct_decision = expected_construct_decision(evidence, component_decisions)
    overall_decision = expected_overall_decision(construct_decision, item_decisions)
    decision_table = evidence.get("decision_table", {})
    if isinstance(decision_table, dict):
        _check_label(
            "decision_table/construct_repeatability_decision",
            decision_table.get("construct_repeatability_decision"),
            construct_decision,
            issues,
        )
        _check_label(
            "decision_table/overall_retest_evidence_decision",
            decision_table.get("overall_retest_evidence_decision"),
            overall_decision,
            issues,
        )
        if overall_decision is None:
            if decision_table.get("claim_authorized") is not None:
                issues.append(ValidationIssue("decision_table/claim_authorized", "must be null until the overall decision is available"))
        else:
            expected_claim = overall_decision == "pass"
            if decision_table.get("claim_authorized") is not expected_claim:
                issues.append(ValidationIssue("decision_table/claim_authorized", f"must be {expected_claim} from the overall decision"))

        if all(decision is not None for decision in item_decisions):
            expected_failed = sum(decision == "fail" for decision in item_decisions)
            if decision_table.get("item_level_failed_item_count") != expected_failed:
                issues.append(
                    ValidationIssue(
                        "decision_table/item_level_failed_item_count",
                        f"must be {expected_failed} from item decisions",
                    )
                )
        elif decision_table.get("item_level_failed_item_count") is not None:
            issues.append(
                ValidationIssue(
                    "decision_table/item_level_failed_item_count",
                    "must be null until all item decisions are available",
                )
            )

    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_path", type=Path, help="Path to a retest evidence JSON artifact.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest ancestor containing schema/retest_evidence.schema.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_retest_evidence(args.evidence_path, repo_root=args.repo_root)
    except RetestEvidenceError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"retest evidence passed: {args.evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
