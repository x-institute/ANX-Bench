#!/usr/bin/env python3
"""Validate an ANX-Bench aggregate-score proposal.

The validator accepts a null preregistered template, but an observed proposal
must be backed by observed passing bridge evidence and must still leave
aggregate scoring disabled until a later release manifest authorizes it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path("schema/aggregate_score_proposal.schema.json")
EXPECTED_BRIDGE_PATH = "validation/v0.7/cross_domain_bridge/wave7_bridge_evidence.json"
REQUIRED_BLOCKED_USES = (
    "clinical",
    "individual",
    "policy",
    "employment",
    "national prevalence",
    "longitudinal",
    "event-study",
    "cross-national",
)
OVERBROAD_CLAIM_TERMS = (
    "clinical",
    "diagnosis",
    "individual",
    "policy decision",
    "policy-decision",
    "employment",
    "eligibility",
    "causal",
    "caused",
    "event-study",
    "event study",
    "longitudinal trend",
    "national prevalence",
    "cross-national",
    "validated overall anx score",
    "official overall anx score",
)


class AggregateScoreProposalError(Exception):
    """Raised when an aggregate-score proposal fails validation."""


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
        raise AggregateScoreProposalError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AggregateScoreProposalError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(proposal_path: Path) -> Path:
    search_start = proposal_path.resolve().parent
    for candidate in (search_start, *search_start.parents):
        if (candidate / SCHEMA_PATH).is_file():
            return candidate
    return Path.cwd().resolve()


def repo_path(root: Path, relative_path: str) -> Path:
    candidate = root / relative_path
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise AggregateScoreProposalError(f"path escapes repository root: {relative_path}") from exc
    return candidate


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
    """Validate the JSON Schema subset used by this proposal schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise AggregateScoreProposalError(f"unsupported external JSON Schema reference: {ref}")
        current: Any = schema
        for part in ref[2:].split("/"):
            current = current[part]
        return current

    def type_matches(value: Any, expected: str) -> bool:
        if expected == "null":
            return value is None
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
        raise AggregateScoreProposalError(f"unsupported JSON Schema type: {expected}")

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

        if isinstance(value, int) and not isinstance(value, bool):
            if "minimum" in subschema and value < subschema["minimum"]:
                issues.append(ValidationIssue(path, "number is below minimum"))

        if isinstance(value, list):
            if "minItems" in subschema and len(value) < subschema["minItems"]:
                issues.append(ValidationIssue(path, "array has too few items"))
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

    check(instance, schema, "$")
    return issues


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _contains_term(values: list[str], term: str) -> bool:
    return any(term in value.lower() for value in values)


def _template_contract_issues(proposal: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    bridge = proposal.get("source_bridge_evidence", {})
    if bridge.get("bridge_evidence_path") != EXPECTED_BRIDGE_PATH:
        issues.append(
            ValidationIssue(
                "source_bridge_evidence/bridge_evidence_path",
                f"must be {EXPECTED_BRIDGE_PATH!r} for the v0.8 overall-score template",
            )
        )
    if proposal.get("scoring_authorized") is not False:
        issues.append(ValidationIssue("scoring_authorized", "must remain false in the preregistered template"))
    if proposal.get("scoring_model", {}).get("release_authorization", {}).get("scoring_authorized") is not False:
        issues.append(
            ValidationIssue(
                "scoring_model/release_authorization/scoring_authorized",
                "must remain false in the preregistered template",
            )
        )
    return issues


def _bridge_issues(proposal: dict[str, Any], repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    bridge_ref = proposal.get("source_bridge_evidence", {})
    bridge_path = bridge_ref.get("bridge_evidence_path")
    if bridge_path != EXPECTED_BRIDGE_PATH:
        issues.append(
            ValidationIssue(
                "source_bridge_evidence/bridge_evidence_path",
                f"must reference {EXPECTED_BRIDGE_PATH!r}",
            )
        )
        return issues
    if not isinstance(bridge_path, str):
        issues.append(ValidationIssue("source_bridge_evidence/bridge_evidence_path", "must be a repository path"))
        return issues

    bridge = load_json(repo_path(repo_root, bridge_path))
    if bridge.get("evidence_status") != "observed":
        issues.append(ValidationIssue("source_bridge_evidence/bridge_evidence_status", "bridge evidence must be observed"))
    final = bridge.get("final_decision", {})
    if final.get("bridge_decision") != "bridge_supported_for_overall_readiness_review":
        issues.append(
            ValidationIssue(
                "source_bridge_evidence/bridge_decision",
                "bridge evidence must pass as bridge_supported_for_overall_readiness_review",
            )
        )
    if final.get("later_proposal_permitted") is not True:
        issues.append(
            ValidationIssue(
                "source_bridge_evidence/later_proposal_permitted",
                "bridge evidence must explicitly permit a later proposal",
            )
        )
    if final.get("scoring_authorized") is not False:
        issues.append(
            ValidationIssue(
                "source_bridge_evidence/bridge_scoring_authorized",
                "bridge evidence must not authorize scoring",
            )
        )
    if bridge_ref.get("bridge_evidence_status") != bridge.get("evidence_status"):
        issues.append(ValidationIssue("source_bridge_evidence/bridge_evidence_status", "must match source bridge evidence"))
    if bridge_ref.get("bridge_decision") != final.get("bridge_decision"):
        issues.append(ValidationIssue("source_bridge_evidence/bridge_decision", "must match source bridge evidence"))
    if bridge_ref.get("bridge_scoring_authorized") != final.get("scoring_authorized"):
        issues.append(ValidationIssue("source_bridge_evidence/bridge_scoring_authorized", "must match source bridge evidence"))
    return issues


def _observed_contract_issues(proposal: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if proposal.get("scoring_authorized") is not False:
        issues.append(ValidationIssue("scoring_authorized", "aggregate scoring remains blocked until release approval"))
    release_auth = proposal.get("scoring_model", {}).get("release_authorization", {})
    if release_auth.get("scoring_authorized") is not False:
        issues.append(
            ValidationIssue(
                "scoring_model/release_authorization/scoring_authorized",
                "proposal review cannot authorize scoring",
            )
        )
    if release_auth.get("release_approval_required") is not True:
        issues.append(
            ValidationIssue(
                "scoring_model/release_authorization/release_approval_required",
                "must require a later release approval",
            )
        )

    for index, construct in enumerate(proposal.get("contributing_constructs", [])):
        approval = construct.get("source_construct_approval", {})
        if approval.get("approval_status") != "approved_scored":
            issues.append(
                ValidationIssue(
                    f"contributing_constructs/{index}/source_construct_approval/approval_status",
                    "source construct must be approved_scored",
                )
            )
        if approval.get("approved_for_aggregate_source") is not True:
            issues.append(
                ValidationIssue(
                    f"contributing_constructs/{index}/source_construct_approval/approved_for_aggregate_source",
                    "source construct must be approved for aggregate-source use",
                )
            )
        if not _nonempty_text(approval.get("approval_artifact_path")):
            issues.append(
                ValidationIssue(
                    f"contributing_constructs/{index}/source_construct_approval/approval_artifact_path",
                    "source construct approval artifact is required",
                )
            )

    for index, item in enumerate(proposal.get("contributing_items", [])):
        if item.get("source_item_status") != "approved_scored":
            issues.append(
                ValidationIssue(f"contributing_items/{index}/source_item_status", "source item must be approved_scored")
            )
        if item.get("scoring_key_version_locked") is not True:
            issues.append(
                ValidationIssue(
                    f"contributing_items/{index}/scoring_key_version_locked",
                    "source item scoring key must be version-locked",
                )
            )

    dif_limits = proposal.get("invariance_dif_limits", {})
    if dif_limits.get("observed_unresolved_material_dif_item_count") != 0:
        issues.append(
            ValidationIssue(
                "invariance_dif_limits/observed_unresolved_material_dif_item_count",
                "unresolved material DIF blocks aggregate proposal approval",
            )
        )
    if dif_limits.get("observed_failed_key_invariance_comparison_count") != 0:
        issues.append(
            ValidationIssue(
                "invariance_dif_limits/observed_failed_key_invariance_comparison_count",
                "failed key invariance comparisons must be resolved or excluded from claims",
            )
        )
    for field in (
        "required_invariance_level",
        "failed_comparison_rule",
        "unresolved_dif_rule",
        "affected_claim_limitation",
    ):
        if not _nonempty_text(dif_limits.get(field)):
            issues.append(ValidationIssue(f"invariance_dif_limits/{field}", "must be explicit"))

    claim_scope = proposal.get("claim_scope", {})
    if claim_scope.get("prohibited_claims_acknowledged") is not True:
        issues.append(ValidationIssue("claim_scope/prohibited_claims_acknowledged", "must be true"))
    for field in ("population_scope", "construct_scope", "time_scope"):
        if not _nonempty_text(claim_scope.get(field)):
            issues.append(ValidationIssue(f"claim_scope/{field}", "must be explicit"))
    if not claim_scope.get("explicit_claim_limits"):
        issues.append(ValidationIssue("claim_scope/explicit_claim_limits", "claim limits must be explicit"))
    permitted_claims = [claim for claim in claim_scope.get("permitted_claims", []) if isinstance(claim, str)]
    for claim in permitted_claims:
        lowered = claim.lower()
        for term in OVERBROAD_CLAIM_TERMS:
            if term in lowered:
                issues.append(ValidationIssue("claim_scope/permitted_claims", f"overbroad claim includes blocked term {term!r}"))
                break

    blocked_uses = [use for use in proposal.get("blocked_uses", []) if isinstance(use, str)]
    for term in REQUIRED_BLOCKED_USES:
        if not _contains_term(blocked_uses, term):
            issues.append(ValidationIssue("blocked_uses", f"must explicitly block {term!r} use"))

    signoff = proposal.get("reviewer_signoff", {})
    if signoff.get("decision") != "proposal_ready_for_release_review":
        issues.append(ValidationIssue("reviewer_signoff/decision", "observed proposals require reviewer approval"))
    for field in ("psychometric_reviewer", "release_reviewer", "signed_date", "signoff_statement"):
        if not _nonempty_text(signoff.get(field)):
            issues.append(ValidationIssue(f"reviewer_signoff/{field}", "reviewer signoff field is required"))

    return issues


def validate_aggregate_score_proposal(proposal_path: Path, *, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(proposal_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    proposal = load_json(proposal_path)
    if not isinstance(proposal, dict):
        raise AggregateScoreProposalError("aggregate-score proposal root must be a JSON object")

    issues: list[ValidationIssue] = []
    issues.extend(validate_with_jsonschema(proposal, schema))

    status = proposal.get("proposal_status")
    if status == "preregistered_template":
        issues.extend(_template_contract_issues(proposal))
    elif status == "observed_proposal":
        issues.extend(_bridge_issues(proposal, repo_root))
        issues.extend(_observed_contract_issues(proposal))
    else:
        issues.append(ValidationIssue("proposal_status", "only preregistered_template and observed_proposal are validatable states"))

    if issues:
        rendered = "\n".join(f"  - {issue.render()}" for issue in issues)
        raise AggregateScoreProposalError(f"aggregate-score proposal failed validation:\n{rendered}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal_path", type=Path, help="Path to an aggregate-score proposal JSON artifact.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest ancestor containing schema/aggregate_score_proposal.schema.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_aggregate_score_proposal(args.proposal_path, repo_root=args.repo_root)
    except AggregateScoreProposalError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"aggregate-score proposal passed: {args.proposal_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
