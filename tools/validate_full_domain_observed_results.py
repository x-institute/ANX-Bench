#!/usr/bin/env python3
"""Validate ANX-Bench Wave 8 full-domain observed results.

This validator is the first observed-evidence gate for promoting the frozen
v0.8.0 Wave 8 packet toward v0.8.1 bridge-readiness evidence. It validates the
observed ledger schema and enforces the non-template, no-event, no-scoring,
sample-size, timing, and frozen-item invariants that must be true before
content-validity or bridge-evidence review begins.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path("schema/full_domain_observed_results.schema.json")
EXPECTED_ITEM_IDS = [
    "sleep_disruption_ai_news",
    "body_vigilance_model_release",
    "background_dread_ai_progress",
    "avoidance_after_ai_capability_demo",
    "skill_obsolescence_software",
    "wage_pressure_customer_support",
    "retraining_pressure_accounting",
    "status_loss_creative_work",
    "deepfake_evidence_trust",
    "synthetic_news_provenance",
    "ai_expert_claim_conflict",
    "personalized_misinformation_targeting",
    "partner_ai_confidant_displacement",
    "friend_group_ai_mediation",
    "eldercare_ai_attachment_shift",
    "ai_personhood_boundary_uncertainty",
    "human_judgment_status_loss",
    "life_purpose_ai_substitution",
    "public_space_tracking",
    "workplace_behavior_scoring",
    "personalized_behavior_nudging",
    "autonomous_cyber_cascade",
    "biosecurity_protocol_misuse",
    "military_escalation_ai_advice",
]
EXPECTED_ITEM_VERSIONS = {
    "sleep_disruption_ai_news": "v0.2.0",
    "body_vigilance_model_release": "v0.2.0",
    "background_dread_ai_progress": "v0.2.0",
    "avoidance_after_ai_capability_demo": "v0.2.0",
    "skill_obsolescence_software": "v0.1.0",
    "wage_pressure_customer_support": "v0.1.0",
    "retraining_pressure_accounting": "v0.1.0",
    "status_loss_creative_work": "v0.1.0",
    "deepfake_evidence_trust": "v0.1.0",
    "synthetic_news_provenance": "v0.1.0",
    "ai_expert_claim_conflict": "v0.1.0",
    "personalized_misinformation_targeting": "v0.1.0",
    "partner_ai_confidant_displacement": "v0.8.0",
    "friend_group_ai_mediation": "v0.8.0",
    "eldercare_ai_attachment_shift": "v0.8.0",
    "ai_personhood_boundary_uncertainty": "v0.8.0",
    "human_judgment_status_loss": "v0.8.0",
    "life_purpose_ai_substitution": "v0.8.0",
    "public_space_tracking": "v0.8.0",
    "workplace_behavior_scoring": "v0.8.0",
    "personalized_behavior_nudging": "v0.8.0",
    "autonomous_cyber_cascade": "v0.8.0",
    "biosecurity_protocol_misuse": "v0.8.0",
    "military_escalation_ai_advice": "v0.8.0",
}
SCORING_FIELDS = (
    "new_domain_scores_authorized",
    "domain_score_claim_permitted",
    "cross_domain_score_authorized",
    "overall_anx_score_authorized",
    "aggregate_scoring_permitted",
    "event_study_claim_permitted",
    "trend_claim_permitted",
    "causal_capability_shock_claim_permitted",
    "subgroup_comparability_claim_permitted",
    "clinical_or_diagnostic_use_permitted",
    "individual_level_use_permitted",
    "policy_decision_ranking_permitted",
)


class FullDomainObservedResultsError(Exception):
    """Raised when the Wave 8 observed-results ledger fails validation."""


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
        raise FullDomainObservedResultsError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FullDomainObservedResultsError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(ledger_path: Path) -> Path:
    search_start = ledger_path.resolve().parent
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
    """Validate the JSON Schema subset used by the observed-results schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise FullDomainObservedResultsError(f"unsupported external JSON Schema reference: {ref}")
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
        raise FullDomainObservedResultsError(f"unsupported JSON Schema type: {expected}")

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
            if subschema.get("format") == "date-time":
                try:
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    issues.append(ValidationIssue(path, "string is not an ISO date-time"))

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


def parse_date(value: Any, path: str, issues: list[ValidationIssue]) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        issues.append(ValidationIssue(path, "must be an ISO date string"))
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        issues.append(ValidationIssue(path, "must be an ISO date"))
        return None
    if parsed > date.today():
        issues.append(ValidationIssue(path, "must not be in the future"))
    return parsed


def parse_timestamp(value: Any, path: str, issues: list[ValidationIssue]) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        issues.append(ValidationIssue(path, "must be an ISO 8601 UTC timestamp"))
        return None
    text = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        issues.append(ValidationIssue(path, "must be an ISO 8601 UTC timestamp"))
        return None
    if parsed.tzinfo is None:
        issues.append(ValidationIssue(path, "must include a timezone offset"))
        return None
    parsed_utc = parsed.astimezone(timezone.utc)
    if parsed_utc > datetime.now(timezone.utc):
        issues.append(ValidationIssue(path, "must not be in the future"))
    return parsed_utc


def validate_contract(ledger: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if ledger.get("result_status") != "completed":
        issues.append(ValidationIssue("result_status", "must be completed; template ledgers cannot satisfy observed evidence"))
    if ledger.get("event_id") != "no_event":
        issues.append(ValidationIssue("event_id", "must remain no_event for Wave 8"))
    if ledger.get("frozen_item_ids") != EXPECTED_ITEM_IDS:
        issues.append(ValidationIssue("frozen_item_ids", "must exactly match the frozen 24-item Wave 8 allowlist and order"))
    if ledger.get("frozen_item_versions") != EXPECTED_ITEM_VERSIONS:
        issues.append(ValidationIssue("frozen_item_versions", "must exactly match the frozen Wave 8 item versions"))

    parse_date(ledger.get("evidence_date"), "evidence_date", issues)
    inspection = ledger.get("outcome_inspection", {})
    if isinstance(inspection, dict):
        locked_at = parse_timestamp(
            inspection.get("preregistered_inputs_locked_at_utc"),
            "outcome_inspection/preregistered_inputs_locked_at_utc",
            issues,
        )
        split_at = parse_timestamp(
            inspection.get("split_assignment_completed_at_utc"),
            "outcome_inspection/split_assignment_completed_at_utc",
            issues,
        )
        first_at = parse_timestamp(
            inspection.get("first_outcome_inspection_at_utc"),
            "outcome_inspection/first_outcome_inspection_at_utc",
            issues,
        )
        if first_at is None:
            issues.append(ValidationIssue("outcome_inspection/first_outcome_inspection_at_utc", "is required for observed ledgers"))
        if locked_at is not None and first_at is not None and locked_at > first_at:
            issues.append(ValidationIssue("outcome_inspection/preregistered_inputs_locked_at_utc", "must be no later than first outcome inspection"))
        if split_at is not None and first_at is not None and split_at > first_at:
            issues.append(ValidationIssue("outcome_inspection/split_assignment_completed_at_utc", "must be no later than first outcome inspection"))
        if inspection.get("assigned_before_outcome_inspection") is not True:
            issues.append(ValidationIssue("outcome_inspection/assigned_before_outcome_inspection", "must be true"))
        if inspection.get("no_post_hoc_threshold_or_claim_changes") is not True:
            issues.append(ValidationIssue("outcome_inspection/no_post_hoc_threshold_or_claim_changes", "must be true"))

    flow = ledger.get("sample_exclusion_flow", {})
    final_n = flow.get("final_analytic_n") if isinstance(flow, dict) else None
    if not isinstance(final_n, int) or isinstance(final_n, bool):
        issues.append(ValidationIssue("sample_exclusion_flow/final_analytic_n", "must be populated for observed ledgers"))
    elif final_n < 2000:
        issues.append(ValidationIssue("sample_exclusion_flow/final_analytic_n", "must be at least 2000"))

    split = ledger.get("split_ids", {})
    if isinstance(split, dict) and split.get("assigned_before_outcome_inspection") is not True:
        issues.append(ValidationIssue("split_ids/assigned_before_outcome_inspection", "must be true"))

    claim_limits = ledger.get("claim_limits", {})
    if isinstance(claim_limits, dict):
        if claim_limits.get("official_scored_items") != []:
            issues.append(ValidationIssue("claim_limits/official_scored_items", "must remain empty"))
        for field in SCORING_FIELDS:
            if claim_limits.get(field) is not False:
                issues.append(ValidationIssue(f"claim_limits/{field}", "must be false for observed Wave 8 ledgers"))

    irt = ledger.get("model_fit_outputs", {}).get("irt", {}) if isinstance(ledger.get("model_fit_outputs"), dict) else {}
    if isinstance(irt, dict) and irt.get("official_theta_scoring_introduced") is not False:
        issues.append(ValidationIssue("model_fit_outputs/irt/official_theta_scoring_introduced", "must be false"))

    for path, expected in (
        ("analyst_signoff/role", "analysis_lead"),
        ("reviewer_signoff/role", "independent_psychometric_reviewer"),
    ):
        current: Any = ledger
        for part in path.split("/"):
            current = current.get(part) if isinstance(current, dict) else None
        if current != expected:
            issues.append(ValidationIssue(path, f"must be {expected!r}"))

    for path in ("analyst_signoff/signed_at_utc", "reviewer_signoff/signed_at_utc"):
        current = ledger
        for part in path.split("/"):
            current = current.get(part) if isinstance(current, dict) else None
        if parse_timestamp(current, path, issues) is None:
            issues.append(ValidationIssue(path, "must be populated for observed ledgers"))

    return issues


def validate_full_domain_observed_results(ledger_path: Path, *, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(ledger_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    ledger = load_json(ledger_path)
    if not isinstance(ledger, dict):
        raise FullDomainObservedResultsError("full-domain observed results root must be a JSON object")

    issues: list[ValidationIssue] = []
    issues.extend(validate_with_jsonschema(ledger, schema))
    issues.extend(validate_contract(ledger))

    if issues:
        rendered = "\n".join(f"  - {issue.render()}" for issue in issues)
        raise FullDomainObservedResultsError(f"full-domain observed results failed validation:\n{rendered}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger_path", type=Path, help="Path to validation/v0.8/full_domain_bridge/observed_wave8_results.json.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest ancestor containing schema/full_domain_observed_results.schema.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_full_domain_observed_results(args.ledger_path, repo_root=args.repo_root)
    except FullDomainObservedResultsError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"full-domain observed results passed: {args.ledger_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
