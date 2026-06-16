#!/usr/bin/env python3
"""Validate ANX-Bench Wave 4 event-study evidence against the locked plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path("schema/event_study_evidence.schema.json")
PLAN_PATH = Path("analysis/v0.4/somatic_event_study/wave4_event_study_analysis_plan.json")
EXPECTED_ITEM_IDS = {
    "sleep_disruption_ai_news",
    "body_vigilance_model_release",
    "background_dread_ai_progress",
    "avoidance_after_ai_capability_demo",
}
EXPECTED_ITEM_VERSIONS = {item_id: "v0.2.0" for item_id in EXPECTED_ITEM_IDS}
PERMITTED_CLAIM_LANGUAGE = "event-associated somatic anxiety change"
DESCRIPTIVE_LANGUAGE = "descriptive monitoring only"
ZERO_SHA256 = "0" * 64
OVERBROAD_CLAIM_PATTERNS = (
    r"\bcause[sd]?\b",
    r"\bcausal\b",
    r"\boverall\s+anx\b",
    r"\banx-bench\s+score\b",
    r"\bclinical anxiety\b",
    r"\bdiagnos",
    r"\blong[- ]term\b",
    r"\bnational\b",
    r"\bpopulation-wide\b",
)


class EventStudyEvidenceError(Exception):
    """Raised when a Wave 4 event-study evidence packet fails validation."""


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
        raise EventStudyEvidenceError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EventStudyEvidenceError(
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
    """Validate the JSON Schema subset used by event_study_evidence.schema.json."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise EventStudyEvidenceError(f"unsupported external JSON Schema reference: {ref}")
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
        raise EventStudyEvidenceError(f"unsupported JSON Schema type: {expected}")

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


def _present(*values: Any) -> bool:
    return all(value is not None for value in values)


def _nonnull_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None and value != ZERO_SHA256


def _is_completed(evidence: dict[str, Any]) -> bool:
    primary = evidence.get("primary_estimate", {})
    samples = evidence.get("sample_counts", {})
    registry = evidence.get("registry_lock_proof", {})
    return any(
        value is not None
        for value in [
            evidence.get("locked_event_id"),
            registry.get("event_locked_before_outcome_inspection"),
            samples.get("baseline_primary_nominal_n"),
            samples.get("followup_primary_nominal_n"),
            primary.get("coefficient"),
            primary.get("p_value"),
            evidence.get("claim_decision", {}).get("claim_authorized"),
        ]
    )


def _check_exact_items(evidence: dict[str, Any], issues: list[ValidationIssue]) -> None:
    if set(evidence.get("frozen_item_ids", [])) != EXPECTED_ITEM_IDS:
        issues.append(ValidationIssue("frozen_item_ids", "must exactly match the approved v0.3.1 somatic item set"))
    versions = evidence.get("frozen_item_versions", {})
    if versions != EXPECTED_ITEM_VERSIONS:
        issues.append(ValidationIssue("frozen_item_versions", "must keep all v0.3.1 somatic source item versions at v0.2.0"))


def _check_plan_links(evidence: dict[str, Any], plan: dict[str, Any], issues: list[ValidationIssue]) -> None:
    if evidence.get("analysis_plan_schema_version") != plan.get("analysis_plan_schema_version"):
        issues.append(ValidationIssue("analysis_plan_schema_version", "must match the Wave 4 analysis plan version"))
    windows = evidence.get("analysis_windows", {})
    plan_windows = plan.get("analysis_windows", {})
    expected_windows = {
        "baseline_primary": plan_windows.get("baseline_primary"),
        "followup_primary": plan_windows.get("followup_primary"),
        "excluded_event_buffer": plan_windows.get("excluded_event_buffer"),
        "placebo_pretrend_early_pre": plan_windows.get("placebo_pretrend", {}).get("early_pre"),
        "placebo_pretrend_late_pre": plan_windows.get("placebo_pretrend", {}).get("late_pre"),
    }
    for key, expected in expected_windows.items():
        if windows.get(key) != expected:
            issues.append(ValidationIssue(f"analysis_windows/{key}", "must match the locked analysis plan"))


def _expected_primary_decision(evidence: dict[str, Any], plan: dict[str, Any]) -> tuple[str | None, list[str]]:
    failures: list[str] = []
    minimum_n = plan["minimum_n"]
    thresholds = plan["pass_fail_claim_thresholds"]["primary_pass"]
    registry_thresholds = plan["pass_fail_claim_thresholds"]["event_registry_required"]

    locked_event_id = evidence.get("locked_event_id")
    registry = evidence.get("registry_lock_proof", {})
    samples = evidence.get("sample_counts", {})
    primary = evidence.get("primary_estimate", {})
    pretrend = evidence.get("pretrend_check", {})
    confounds = evidence.get("confounds", {})
    robustness = {check.get("check_id"): check for check in evidence.get("robustness_checks", [])}

    required_values = [
        locked_event_id,
        registry.get("event_locked_before_outcome_inspection"),
        registry.get("release_blocking_confound_present"),
        confounds.get("release_blocking_confound_present"),
        samples.get("baseline_primary_nominal_n"),
        samples.get("followup_primary_nominal_n"),
        samples.get("baseline_effective_weighted_n"),
        samples.get("followup_effective_weighted_n"),
        primary.get("coefficient"),
        primary.get("ci_95_lower"),
        primary.get("p_value"),
        pretrend.get("coefficient"),
        pretrend.get("p_value"),
    ]
    for check_id in ("unweighted_primary_model", "alternative_weight_trim", "narrow_followup_window"):
        required_values.append(robustness.get(check_id, {}).get("coefficient"))
    if not _present(*required_values):
        return None, []

    if locked_event_id == "no_event":
        failures.append("locked_event_id must identify a qualifying locked event, not no_event")
    if registry.get("event_locked_before_outcome_inspection") is not registry_thresholds["event_locked_before_outcome_inspection"]:
        failures.append("registry lock proof does not show pre-outcome event lock")
    if registry.get("registry_status") != "locked":
        failures.append("registry_status must be locked")
    if registry.get("outcome_inspection_status") not in {"not_inspected_at_lock", "not_inspected"}:
        failures.append("outcome inspection status must show no inspection at lock")
    if not _nonnull_sha256(registry.get("registry_sha256")):
        failures.append("registry_sha256 must be a nonzero SHA-256 digest")
    if not _nonnull_sha256(registry.get("event_record_sha256")):
        failures.append("event_record_sha256 must be a nonzero SHA-256 digest")
    if registry.get("release_blocking_confound_present") is not registry_thresholds["release_blocking_confound_present"]:
        failures.append("registry records a release-blocking confound")
    if confounds.get("release_blocking_confound_present") is not registry_thresholds["release_blocking_confound_present"]:
        failures.append("confound review records a release-blocking confound")

    n_checks = {
        "baseline_primary_nominal_n": minimum_n["baseline_primary_nominal"],
        "followup_primary_nominal_n": minimum_n["followup_primary_nominal"],
        "baseline_effective_weighted_n": minimum_n["baseline_effective_weighted"],
        "followup_effective_weighted_n": minimum_n["followup_effective_weighted"],
    }
    for key, minimum in n_checks.items():
        observed = _num(samples.get(key))
        if observed is None or observed < minimum:
            failures.append(f"{key} is below preregistered minimum {minimum}")

    coefficient = _num(primary.get("coefficient"))
    lower = _num(primary.get("ci_95_lower"))
    p_value = _num(primary.get("p_value"))
    if coefficient is None or coefficient < thresholds["minimum_coefficient_points"]:
        failures.append("primary coefficient is below the minimum event-associated change threshold")
    if thresholds["required_direction"] == "positive" and (coefficient is None or coefficient <= 0):
        failures.append("primary coefficient is not positive")
    if p_value is None or p_value > thresholds["maximum_p_value"]:
        failures.append("primary p-value exceeds the confirmatory threshold")
    if lower is None or lower < thresholds["minimum_confidence_interval_lower_bound"]:
        failures.append("primary confidence interval lower bound is below threshold")

    pretrend_coefficient = _num(pretrend.get("coefficient"))
    pretrend_p = _num(pretrend.get("p_value"))
    if pretrend_coefficient is None or abs(pretrend_coefficient) > thresholds["placebo_pretrend_max_abs_coefficient"]:
        failures.append("placebo pretrend coefficient exceeds the maximum absolute threshold")
    if thresholds["placebo_pretrend_must_be_nonsignificant"] and (pretrend_p is None or pretrend_p <= 0.05):
        failures.append("placebo pretrend is statistically significant")

    robustness_thresholds = {
        "unweighted_primary_model": thresholds["robustness_minimum_unweighted_coefficient"],
        "alternative_weight_trim": thresholds["robustness_minimum_weight_trim_coefficient"],
        "narrow_followup_window": thresholds["robustness_minimum_narrow_window_coefficient"],
    }
    for check_id, minimum in robustness_thresholds.items():
        coefficient = _num(robustness.get(check_id, {}).get("coefficient"))
        if coefficient is None or coefficient < minimum:
            failures.append(f"{check_id} coefficient is below robustness threshold {minimum}")

    return ("pass" if not failures else "descriptive_only"), failures


def _check_decisions(evidence: dict[str, Any], expected: str | None, failures: list[str], issues: list[ValidationIssue]) -> None:
    primary = evidence.get("primary_estimate", {})
    pretrend = evidence.get("pretrend_check", {})
    claim = evidence.get("claim_decision", {})

    if expected is None:
        if primary.get("decision") is not None:
            issues.append(ValidationIssue("primary_estimate/decision", "must be null until required observed evidence is complete"))
        if pretrend.get("decision") is not None:
            issues.append(ValidationIssue("pretrend_check/decision", "must be null until required observed evidence is complete"))
        if claim.get("primary_threshold_decision") is not None:
            issues.append(ValidationIssue("claim_decision/primary_threshold_decision", "must be null until required observed evidence is complete"))
        if claim.get("claim_authorized") is not None:
            issues.append(ValidationIssue("claim_decision/claim_authorized", "must be null until required observed evidence is complete"))
        if claim.get("authorized_claim_language") is not None:
            issues.append(ValidationIssue("claim_decision/authorized_claim_language", "must be null until required observed evidence is complete"))
        return

    expected_primary_label = "pass" if expected == "pass" else "fail"
    if primary.get("decision") != expected_primary_label:
        issues.append(ValidationIssue("primary_estimate/decision", f"must be {expected_primary_label!r} from locked thresholds"))

    expected_pretrend_label = "pass" if not any("pretrend" in failure for failure in failures) else "fail"
    if pretrend.get("decision") != expected_pretrend_label:
        issues.append(ValidationIssue("pretrend_check/decision", f"must be {expected_pretrend_label!r} from locked thresholds"))

    if claim.get("primary_threshold_decision") != expected:
        issues.append(ValidationIssue("claim_decision/primary_threshold_decision", f"must be {expected!r} from locked thresholds"))
    expected_authorized = expected == "pass"
    if claim.get("claim_authorized") is not expected_authorized:
        issues.append(ValidationIssue("claim_decision/claim_authorized", f"must be {expected_authorized!r} from locked thresholds"))
    expected_language = PERMITTED_CLAIM_LANGUAGE if expected_authorized else DESCRIPTIVE_LANGUAGE
    if claim.get("authorized_claim_language") != expected_language:
        issues.append(ValidationIssue("claim_decision/authorized_claim_language", f"must be {expected_language!r}"))
    if expected == "descriptive_only" and claim.get("claim_authorized") is True:
        for failure in failures:
            issues.append(ValidationIssue("event_study_gate", failure))


def _check_robustness_ids(evidence: dict[str, Any], plan: dict[str, Any], issues: list[ValidationIssue]) -> None:
    expected_ids = [check["check_id"] for check in plan["robustness_checks"]]
    observed_ids = [check.get("check_id") for check in evidence.get("robustness_checks", [])]
    if observed_ids != expected_ids:
        issues.append(ValidationIssue("robustness_checks", "must list locked robustness checks in analysis-plan order"))


def _check_claim_text(evidence: dict[str, Any], issues: list[ValidationIssue]) -> None:
    text = evidence.get("reported_claim_text")
    claim = evidence.get("claim_decision", {})
    if text is None:
        return
    normalized = text.lower()
    for pattern in OVERBROAD_CLAIM_PATTERNS:
        if re.search(pattern, normalized):
            issues.append(ValidationIssue("reported_claim_text", "contains overbroad or blocked claim language"))
            break
    if claim.get("claim_authorized") is True and PERMITTED_CLAIM_LANGUAGE not in normalized:
        issues.append(ValidationIssue("reported_claim_text", "must use the permitted event-associated somatic anxiety change language"))


def validate_event_study_evidence(evidence_path: Path, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(evidence_path)
    evidence = load_json(evidence_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    plan = load_json(repo_root / PLAN_PATH)

    issues = validate_with_jsonschema(evidence, schema)
    if isinstance(evidence, dict):
        _check_exact_items(evidence, issues)
        _check_plan_links(evidence, plan, issues)
        _check_robustness_ids(evidence, plan, issues)
        expected, failures = _expected_primary_decision(evidence, plan)
        _check_decisions(evidence, expected, failures, issues)
        _check_claim_text(evidence, issues)

        if _is_completed(evidence) and expected is None:
            issues.append(ValidationIssue("$", "completed evidence is missing required event-study gate fields"))

    if issues:
        rendered = "\n".join(issue.render() for issue in issues)
        raise EventStudyEvidenceError(f"event-study evidence validation failed:\n{rendered}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_path", type=Path, help="Path to a Wave 4 event-study evidence JSON artifact")
    args = parser.parse_args(argv)

    try:
        validate_event_study_evidence(args.evidence_path)
    except EventStudyEvidenceError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
