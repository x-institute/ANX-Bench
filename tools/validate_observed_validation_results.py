#!/usr/bin/env python3
"""Validate checksum-bound observed psychometric validation results.

The observed results file is the canonical statistic source for a scored
promotion dossier. This gate validates the JSON artifact against the formal
schema and rejects zero-filled checksum placeholders anywhere in the result.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path("schema/observed_validation_results.schema.json")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
ZERO_SHA256 = "0" * 64


class ObservedValidationResultsError(Exception):
    """Raised when observed validation results fail the release-blocking gate."""


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
        raise ObservedValidationResultsError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ObservedValidationResultsError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(results_path: Path) -> Path:
    search_start = results_path.resolve().parent
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
    """Validate the JSON Schema subset used by the observed results schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise ObservedValidationResultsError(f"unsupported external JSON Schema reference: {ref}")
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
        raise ObservedValidationResultsError(f"unsupported JSON Schema type: {expected}")

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
            if "minProperties" in subschema and len(value) < subschema["minProperties"]:
                issues.append(ValidationIssue(path, "object has too few properties"))

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


def iter_sha256_fields(value: Any, path: str = "$") -> list[tuple[str, str]]:
    hashes: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            child_path = f"{path}/{key}"
            if key == "sha256" or key.endswith("_sha256"):
                if isinstance(item, str):
                    hashes.append((child_path, item))
            hashes.extend(iter_sha256_fields(item, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hashes.extend(iter_sha256_fields(item, f"{path}/{index}"))
    return hashes


def validate_hashes(results: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    observed_hashes = iter_sha256_fields(results)
    if not observed_hashes:
        issues.append(ValidationIssue("$", "observed results must contain checksum fields"))
    for path, value in observed_hashes:
        if not SHA256_RE.fullmatch(value):
            issues.append(ValidationIssue(path, "value is not a lowercase SHA-256 digest"))
        elif value == ZERO_SHA256:
            issues.append(ValidationIssue(path, "zero-filled SHA-256 placeholder is release-blocking"))
    return issues


def validate_item_consistency(results: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    frozen_ids = results.get("frozen_item_ids")
    frozen_versions = results.get("frozen_item_versions")
    item_statistics = results.get("item_statistics")
    irt_parameters = results.get("irt", {}).get("item_parameters") if isinstance(results.get("irt"), dict) else None
    retained_ids = results.get("retention", {}).get("retained_item_ids") if isinstance(results.get("retention"), dict) else None

    if isinstance(frozen_ids, list):
        frozen_set = set(frozen_ids)
        if len(frozen_set) != len(frozen_ids):
            issues.append(ValidationIssue("frozen_item_ids", "item IDs must be unique"))
    else:
        return issues

    if isinstance(frozen_versions, dict) and set(frozen_versions) != frozen_set:
        issues.append(ValidationIssue("frozen_item_versions", "version map keys must exactly match frozen_item_ids"))

    if isinstance(item_statistics, list):
        statistic_ids = {row.get("item_id") for row in item_statistics if isinstance(row, dict)}
        if statistic_ids != frozen_set:
            issues.append(ValidationIssue("item_statistics", "item statistics must cover exactly the frozen item IDs"))

    if isinstance(irt_parameters, list):
        irt_ids = {row.get("item_id") for row in irt_parameters if isinstance(row, dict)}
        if irt_ids != frozen_set:
            issues.append(ValidationIssue("irt/item_parameters", "IRT parameters must cover exactly the frozen item IDs"))

    if isinstance(retained_ids, list) and not set(retained_ids).issubset(frozen_set):
        issues.append(ValidationIssue("retention/retained_item_ids", "retained items must be a subset of frozen_item_ids"))

    return issues


def validate_observed_validation_results(results_path: Path, *, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(results_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    results = load_json(results_path)
    if not isinstance(results, dict):
        raise ObservedValidationResultsError("observed validation results root must be a JSON object")

    issues: list[ValidationIssue] = []
    issues.extend(validate_with_jsonschema(results, schema))
    issues.extend(validate_hashes(results))
    issues.extend(validate_item_consistency(results))

    if issues:
        rendered = "\n".join(f"  - {issue.render()}" for issue in issues)
        raise ObservedValidationResultsError(f"observed validation results failed validation:\n{rendered}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "results_path",
        type=Path,
        help="Path to observed_wave1_results.json or another observed validation results artifact.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest ancestor containing the observed validation results schema.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_observed_validation_results(args.results_path, repo_root=args.repo_root)
    except ObservedValidationResultsError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"observed validation results passed: {args.results_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
