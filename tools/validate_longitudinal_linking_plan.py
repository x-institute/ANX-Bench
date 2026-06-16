#!/usr/bin/env python3
"""Validate an ANX-Bench longitudinal linking and equating plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path("schema/longitudinal_linking_plan.schema.json")
LONGITUDINAL_CLAIM_RE = re.compile(
    r"\b(longitudinal|trend|cross[- ]release|event[- ]study|causal|capability[- ]shock|increased|decreased|changed over time)\b",
    re.IGNORECASE,
)


class LongitudinalLinkingPlanError(Exception):
    """Raised when a linking plan cannot be validated."""


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
        raise LongitudinalLinkingPlanError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise LongitudinalLinkingPlanError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(plan_path: Path) -> Path:
    for candidate in (plan_path.resolve().parent, *plan_path.resolve().parents):
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
    """Validate the JSON Schema subset used by the linking-plan schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise LongitudinalLinkingPlanError(f"unsupported external JSON Schema reference: {ref}")
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
        raise LongitudinalLinkingPlanError(f"unsupported JSON Schema type: {expected}")

    def check(value: Any, subschema: dict[str, Any], path: str) -> None:
        if "$ref" in subschema:
            check(value, resolve_ref(subschema["$ref"]), path)
            return

        expected_type = subschema.get("type")
        if expected_type is not None:
            expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
            if not any(type_matches(value, candidate) for candidate in expected_types):
                issues.append(ValidationIssue(path, f"expected type {' or '.join(expected_types)}, got {type(value).__name__}"))
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


def _repo_file(root: Path, relative_path: str) -> Path:
    if relative_path.startswith("/") or ".." in Path(relative_path).parts:
        raise LongitudinalLinkingPlanError(f"unsafe repository path: {relative_path}")
    return root / relative_path


def _manifest_items(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items = manifest.get("frozen_item_set", {}).get("items", [])
    if not isinstance(items, list):
        return {}
    return {item.get("item_id"): item for item in items if isinstance(item, dict) and item.get("item_id")}


def _check_path_exists(root: Path, repo_path: str, path_label: str, issues: list[ValidationIssue]) -> None:
    if not _repo_file(root, repo_path).is_file():
        issues.append(ValidationIssue(path_label, f"referenced path does not exist: {repo_path}"))


def _check_release_ref(root: Path, plan: dict[str, Any], key: str, issues: list[ValidationIssue]) -> dict[str, Any]:
    release = plan.get(key, {})
    manifest_path = release.get("manifest_path")
    if not isinstance(manifest_path, str):
        issues.append(ValidationIssue(key, "missing manifest_path"))
        return {}
    _check_path_exists(root, manifest_path, f"{key}/manifest_path", issues)
    if not _repo_file(root, manifest_path).is_file():
        return {}
    manifest = load_json(_repo_file(root, manifest_path))
    expected_version = release.get("benchmark_version")
    observed_version = manifest.get("benchmark_version")
    if observed_version != expected_version:
        issues.append(
            ValidationIssue(
                f"{key}/benchmark_version",
                f"manifest benchmark_version {observed_version!r} does not match plan {expected_version!r}",
            )
        )
    return manifest if isinstance(manifest, dict) else {}


def _check_item_ref(
    root: Path,
    item_ref: dict[str, Any],
    manifest_items: dict[str, dict[str, Any]],
    path_label: str,
    issues: list[ValidationIssue],
) -> None:
    item_id = item_ref.get("item_id")
    item_version = item_ref.get("item_version")
    item_path = item_ref.get("item_path")
    manifest_item = manifest_items.get(item_id)
    if manifest_item is None:
        issues.append(ValidationIssue(f"{path_label}/item_id", f"anchor item {item_id!r} is absent from referenced release manifest"))
        return
    if manifest_item.get("item_version") != item_version:
        issues.append(
            ValidationIssue(
                f"{path_label}/item_version",
                f"plan item_version {item_version!r} does not match manifest {manifest_item.get('item_version')!r}",
            )
        )
    if manifest_item.get("path") != item_path:
        issues.append(
            ValidationIssue(
                f"{path_label}/item_path",
                f"plan item_path {item_path!r} does not match manifest {manifest_item.get('path')!r}",
            )
        )
    if isinstance(item_path, str):
        _check_path_exists(root, item_path, f"{path_label}/item_path", issues)
        if _repo_file(root, item_path).is_file():
            item_json = load_json(_repo_file(root, item_path))
            if item_json.get("item_id") != item_id:
                issues.append(ValidationIssue(f"{path_label}/item_id", "item file item_id does not match plan"))
            if item_json.get("version") != item_version:
                issues.append(ValidationIssue(f"{path_label}/item_version", "item file version does not match plan"))


def validate_repository_contract(plan: dict[str, Any], root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    source_manifest = _check_release_ref(root, plan, "source_release", issues)
    target_manifest = _check_release_ref(root, plan, "target_release", issues)
    source_items = _manifest_items(source_manifest)
    target_items = _manifest_items(target_manifest)

    for index, prereg_path in enumerate(plan.get("preregistration_paths", [])):
        if isinstance(prereg_path, str):
            _check_path_exists(root, prereg_path, f"preregistration_paths/{index}", issues)

    sampling_plan = plan.get("bridge_sample", {}).get("sampling_plan_path")
    if isinstance(sampling_plan, str):
        _check_path_exists(root, sampling_plan, "bridge_sample/sampling_plan_path", issues)

    anchors = plan.get("anchor_items", [])
    overlap = plan.get("minimum_overlap_rules", {})
    minimum_anchor_count = overlap.get("minimum_anchor_items_total")
    if isinstance(minimum_anchor_count, int) and isinstance(anchors, list) and len(anchors) < minimum_anchor_count:
        issues.append(
            ValidationIssue(
                "anchor_items",
                f"anchor count {len(anchors)} is below minimum_anchor_items_total {minimum_anchor_count}",
            )
        )

    seen_anchor_ids: set[str] = set()
    for index, anchor in enumerate(anchors if isinstance(anchors, list) else []):
        if not isinstance(anchor, dict):
            continue
        anchor_id = anchor.get("anchor_id")
        if anchor_id in seen_anchor_ids:
            issues.append(ValidationIssue(f"anchor_items/{index}/anchor_id", f"duplicate anchor_id {anchor_id!r}"))
        seen_anchor_ids.add(anchor_id)
        if anchor_id != anchor.get("source", {}).get("item_id") or anchor_id != anchor.get("target", {}).get("item_id"):
            issues.append(ValidationIssue(f"anchor_items/{index}/anchor_id", "anchor_id must match source and target item_id"))
        _check_item_ref(root, anchor.get("source", {}), source_items, f"anchor_items/{index}/source", issues)
        _check_item_ref(root, anchor.get("target", {}), target_items, f"anchor_items/{index}/target", issues)

        continuity = anchor.get("item_version_continuity")
        source_version = anchor.get("source", {}).get("item_version")
        target_version = anchor.get("target", {}).get("item_version")
        bridge_evidence_path = anchor.get("bridge_evidence_path")
        if continuity == "identical_item_version" and source_version != target_version:
            issues.append(ValidationIssue(f"anchor_items/{index}/item_version_continuity", "identical continuity requires matching source and target item versions"))
        if continuity == "changed_item_version_requires_bridge_evidence":
            if not isinstance(bridge_evidence_path, str):
                issues.append(ValidationIssue(f"anchor_items/{index}/bridge_evidence_path", "changed item versions require observed bridge evidence"))
            elif not _repo_file(root, bridge_evidence_path).is_file():
                issues.append(ValidationIssue(f"anchor_items/{index}/bridge_evidence_path", f"bridge evidence path does not exist: {bridge_evidence_path}"))

    plan_status = plan.get("plan_status")
    permitted_claims = plan.get("claim_authorization", {}).get("permitted_claims", [])
    if plan_status != "observed_passed":
        for index, claim in enumerate(permitted_claims if isinstance(permitted_claims, list) else []):
            if isinstance(claim, str) and LONGITUDINAL_CLAIM_RE.search(claim) and not re.search(r"\b(no|not|non-scored|not authorized|blocked)\b", claim, re.IGNORECASE):
                issues.append(
                    ValidationIssue(
                        f"claim_authorization/permitted_claims/{index}",
                        "unauthorized longitudinal, trend, cross-release, event-study, or causal claim before observed linking evidence passes",
                    )
                )

    target_statuses = plan.get("domain_scoring_status", [])
    if plan_status != "observed_passed":
        for index, status in enumerate(target_statuses if isinstance(target_statuses, list) else []):
            if isinstance(status, dict) and status.get("score_status") == "linked_scored":
                issues.append(ValidationIssue(f"domain_scoring_status/{index}/score_status", "linked scoring requires observed_passed linking evidence"))

    return issues


def validate_plan(plan_path: Path) -> list[ValidationIssue]:
    root = find_repo_root(plan_path)
    plan = load_json(plan_path)
    schema = load_json(root / SCHEMA_PATH)
    issues = validate_with_jsonschema(plan, schema)
    if issues:
        return issues
    return validate_repository_contract(plan, root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to a longitudinal linking plan JSON file")
    args = parser.parse_args(argv)

    try:
        issues = validate_plan(args.plan)
    except LongitudinalLinkingPlanError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if issues:
        for issue in issues:
            print(issue.render(), file=sys.stderr)
        return 1

    print(f"validated longitudinal linking plan: {args.plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
