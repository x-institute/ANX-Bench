#!/usr/bin/env python3
"""Validate an ANX-Bench release manifest.

The release gate checks schema validity, item registry membership, scoring
eligibility, and SHA-256 integrity for the files that define a citable release.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


RELEASE_SCHEMA_PATH = Path("schema/release.schema.json")
ITEM_SCHEMA_PATH = Path("schema/item.schema.json")
VALIDATION_DOSSIER_SCHEMA_PATH = Path("schema/validation_dossier.schema.json")
PSYCHOMETRIC_EVIDENCE_SCHEMA_PATH = Path("schema/psychometric_evidence_manifest.schema.json")
PSYCHOMETRIC_ANALYSIS_PLAN_SCHEMA_PATH = Path("schema/psychometric_analysis_plan.schema.json")
BENCHMARK_VERSION_RE = re.compile(r"^v(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)$")


class ReleaseValidationError(Exception):
    """Raised when a release artifact fails the validation gate."""


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
        raise ReleaseValidationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReleaseValidationError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except FileNotFoundError as exc:
        raise ReleaseValidationError(f"missing file for checksum: {path}") from exc
    return digest.hexdigest()


def repo_path(root: Path, relative_path: str) -> Path:
    candidate = root / relative_path
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ReleaseValidationError(
            f"path escapes repository root and cannot be validated: {relative_path}"
        ) from exc
    return candidate


def find_repo_root(manifest_path: Path) -> Path:
    search_start = manifest_path.resolve().parent
    for candidate in (search_start, *search_start.parents):
        if (candidate / RELEASE_SCHEMA_PATH).is_file() and (candidate / ITEM_SCHEMA_PATH).is_file():
            return candidate
    return Path.cwd().resolve()


def validate_with_jsonschema(instance: Any, schema: dict[str, Any], schema_name: str) -> list[ValidationIssue]:
    try:
        from jsonschema import Draft202012Validator
    except ModuleNotFoundError:
        return validate_with_builtin_schema(instance, schema, schema_name)

    validator = Draft202012Validator(schema)
    issues = []
    for error in sorted(validator.iter_errors(instance), key=lambda err: list(err.path)):
        location = "/".join(str(part) for part in error.path) or "$"
        issues.append(ValidationIssue(f"{schema_name}:{location}", error.message))
    return issues


def validate_with_builtin_schema(
    instance: Any, schema: dict[str, Any], schema_name: str
) -> list[ValidationIssue]:
    """Validate the JSON Schema subset used by ANX-Bench repository schemas."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise ReleaseValidationError(f"unsupported external JSON Schema reference: {ref}")
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
            return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
        if expected == "string":
            return isinstance(value, str)
        if expected == "array":
            return isinstance(value, list)
        if expected == "object":
            return isinstance(value, dict)
        raise ReleaseValidationError(f"unsupported JSON Schema type: {expected}")

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
                        f"{schema_name}:{path}",
                        f"expected type {' or '.join(expected_types)}, got {type(value).__name__}",
                    )
                )
                return

        if "const" in subschema and value != subschema["const"]:
            issues.append(ValidationIssue(f"{schema_name}:{path}", f"expected constant {subschema['const']!r}"))
            return

        if "enum" in subschema and value not in subschema["enum"]:
            issues.append(ValidationIssue(f"{schema_name}:{path}", f"value {value!r} is not in enum"))

        if isinstance(value, str):
            if "minLength" in subschema and len(value) < subschema["minLength"]:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "string is shorter than minLength"))
            if "pattern" in subschema and re.fullmatch(subschema["pattern"], value) is None:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "string does not match pattern"))
            if subschema.get("format") == "date":
                try:
                    date.fromisoformat(value)
                except ValueError:
                    issues.append(ValidationIssue(f"{schema_name}:{path}", "string is not an ISO date"))

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in subschema and value < subschema["minimum"]:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "number is below minimum"))
            if "maximum" in subschema and value > subschema["maximum"]:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "number is above maximum"))

        if isinstance(value, list):
            if "minItems" in subschema and len(value) < subschema["minItems"]:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "array has too few items"))
            if "maxItems" in subschema and len(value) > subschema["maxItems"]:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "array has too many items"))
            if subschema.get("uniqueItems"):
                encoded = [json.dumps(item, sort_keys=True) for item in value]
                if len(encoded) != len(set(encoded)):
                    issues.append(ValidationIssue(f"{schema_name}:{path}", "array items are not unique"))
            if "items" in subschema:
                for index, item in enumerate(value):
                    check(item, subschema["items"], f"{path}/{index}")

        if isinstance(value, dict):
            required = subschema.get("required", [])
            for key in required:
                if key not in value:
                    issues.append(ValidationIssue(f"{schema_name}:{path}", f"missing required property {key!r}"))

            properties = subschema.get("properties", {})
            allowed = set(properties)
            for key, item in value.items():
                if "propertyNames" in subschema:
                    check(key, subschema["propertyNames"], f"{path}/{key}:propertyName")
                if key in properties:
                    check(item, properties[key], f"{path}/{key}")
                elif subschema.get("additionalProperties") is False:
                    issues.append(ValidationIssue(f"{schema_name}:{path}", f"unexpected property {key!r}"))
                elif isinstance(subschema.get("additionalProperties"), dict):
                    check(item, subschema["additionalProperties"], f"{path}/{key}")

            if "minProperties" in subschema and len(value) < subschema["minProperties"]:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "object has too few properties"))
            if "maxProperties" in subschema and len(value) > subschema["maxProperties"]:
                issues.append(ValidationIssue(f"{schema_name}:{path}", "object has too many properties"))

    check(instance, schema, "$")
    return issues


def checksum_records(manifest: dict[str, Any]) -> dict[str, str]:
    records: dict[str, str] = {}
    for record in manifest.get("checksums", {}).get("files", []):
        path = record["path"]
        if path in records:
            raise ReleaseValidationError(f"duplicate checksum record for {path}")
        records[path] = record["sha256"]
    return records


def active_dossier_path(value: Any) -> str | None:
    if value in (None, "not_available"):
        return None
    if not isinstance(value, str) or not value.endswith(".json"):
        return ""
    return value


def release_line_from_version(version: Any) -> str:
    if not isinstance(version, str):
        raise ReleaseValidationError("benchmark_version must be a semantic version string")
    match = BENCHMARK_VERSION_RE.fullmatch(version)
    if match is None:
        raise ReleaseValidationError(f"benchmark_version is not a semantic release version: {version!r}")
    return f"v{match.group('major')}.{match.group('minor')}"


def benchmark_version_tuple(version: Any, field_name: str) -> tuple[int, int, int]:
    if not isinstance(version, str):
        raise ReleaseValidationError(f"{field_name} must be a semantic version string")
    match = BENCHMARK_VERSION_RE.fullmatch(version)
    if match is None:
        raise ReleaseValidationError(f"{field_name} is not a semantic release version: {version!r}")
    return (int(match.group("major")), int(match.group("minor")), int(match.group("patch")))


def is_same_line_not_later(effective_version: Any, manifest_version: Any) -> bool:
    effective = benchmark_version_tuple(effective_version, "effective_benchmark_version")
    manifest = benchmark_version_tuple(manifest_version, "benchmark_version")
    return effective[:2] == manifest[:2] and effective <= manifest


def is_validation_dossier_checksum_path(path: str) -> bool:
    return path.startswith("validation/") and path.endswith(".json")


def evidence_manifest_path_for_dossier(dossier_path: str) -> str:
    if dossier_path.endswith("_calibration_dossier.json"):
        return dossier_path.removesuffix("_calibration_dossier.json") + "_evidence_manifest.json"
    path = Path(dossier_path)
    return str(path.with_name(path.stem + "_evidence_manifest.json"))


def is_analysis_plan_checksum_path(path: str) -> bool:
    return path.startswith("analysis/") and path.endswith("_analysis_plan.json")


def is_calibration_release(manifest: dict[str, Any], checksum_paths: set[str]) -> bool:
    label = manifest.get("release_label")
    return (
        any(is_analysis_plan_checksum_path(path) for path in checksum_paths)
        or (isinstance(label, str) and "calibration" in label.lower())
    )


ISO_DATE_RE = re.compile(r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b")


def parse_iso_dates(value: Any) -> list[date]:
    if not isinstance(value, str):
        return []
    parsed: list[date] = []
    for match in ISO_DATE_RE.findall(value):
        try:
            parsed.append(date.fromisoformat(match))
        except ValueError:
            continue
    return parsed


def is_planned_marker(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.lower()
    return "planned" in normalized or "pending" in normalized or "provisional" in normalized


def scored_release_requested(manifest: dict[str, Any], listed_items: list[dict[str, Any]]) -> bool:
    if manifest.get("scoring_eligibility", {}).get("aggregate_scoring_permitted") is True:
        return True
    if manifest.get("official_scored_items"):
        return True
    return any(
        item.get("release_status") == "approved_scored"
        or item.get("validation", {}).get("scoring_eligible") is True
        for item in listed_items
    )


def add_future_date_issue(
    issues: list[ValidationIssue],
    path: str,
    field: str,
    value: Any,
    validation_run_date: date,
    planned: bool,
) -> None:
    if planned:
        return
    future_dates = [candidate for candidate in parse_iso_dates(value) if candidate > validation_run_date]
    if future_dates:
        latest = max(future_dates).isoformat()
        issues.append(
            ValidationIssue(
                f"{path}:{field}",
                f"future-dated scored-release evidence date {latest} is later than validation run date {validation_run_date.isoformat()} and is not explicitly marked planned",
            )
        )


def require_checksum_record(
    records: dict[str, str], path: str, expected_sha: str | None, role: str, issues: list[ValidationIssue]
) -> None:
    if path not in records:
        issues.append(ValidationIssue(path, f"missing checksums.files entry for {role}"))
        return
    if expected_sha is not None and records[path] != expected_sha:
        issues.append(
            ValidationIssue(
                path,
                f"{role} sha256 differs between manifest section ({expected_sha}) and checksums.files ({records[path]})",
            )
        )


def validate_release(manifest_path: Path, validation_run_date: date | None = None) -> None:
    manifest_path = manifest_path.resolve()
    root = find_repo_root(manifest_path)
    validation_run_date = validation_run_date or date.today()

    manifest = load_json(manifest_path)
    release_schema = load_json(root / RELEASE_SCHEMA_PATH)
    item_schema = load_json(root / ITEM_SCHEMA_PATH)

    issues: list[ValidationIssue] = []
    manifest_for_schema = dict(manifest)
    manifest_for_schema.pop("$schema", None)
    issues.extend(validate_with_jsonschema(manifest_for_schema, release_schema, "release.schema.json"))

    release_line = release_line_from_version(manifest.get("benchmark_version"))
    required_registry_path = Path("constructs") / release_line / "registry.json"
    registry = load_json(root / required_registry_path)
    if registry.get("benchmark_release_line") != release_line:
        issues.append(
            ValidationIssue(
                str(required_registry_path),
                f"benchmark_release_line={registry.get('benchmark_release_line')!r} does not match manifest release line {release_line!r}",
            )
        )
    if not is_same_line_not_later(registry.get("effective_benchmark_version"), manifest.get("benchmark_version")):
        issues.append(
            ValidationIssue(
                str(required_registry_path),
                f"effective_benchmark_version={registry.get('effective_benchmark_version')!r} must be in the same release line as manifest benchmark_version={manifest.get('benchmark_version')!r} and must not be later",
            )
        )

    registry_by_construct = {
        construct["construct_id"]: construct for construct in registry.get("constructs", [])
    }

    listed_items = manifest.get("frozen_item_set", {}).get("items", [])
    is_scored_release = scored_release_requested(manifest, listed_items)
    release_status = manifest.get("release_status")
    manifest_relative_path = str(manifest_path.relative_to(root)) if manifest_path.is_relative_to(root) else str(manifest_path)
    if release_status == "citable":
        release_date_value = manifest.get("release_date")
        try:
            release_date = date.fromisoformat(release_date_value) if isinstance(release_date_value, str) else None
        except ValueError:
            release_date = None
        if release_date is not None and release_date > validation_run_date:
            issues.append(
                ValidationIssue(
                    f"{manifest_relative_path}:release_date",
                    f"future-dated citable release date {release_date.isoformat()} is later than validation run date {validation_run_date.isoformat()}",
                )
            )
    if release_status == "frozen_candidate":
        candidate_scored_items = sorted(manifest.get("official_scored_items", []))
        candidate_scoring_eligible_items = sorted(
            item.get("item_id", "<unknown>")
            for item in listed_items
            if item.get("release_status") == "approved_scored"
            or item.get("validation", {}).get("scoring_eligible") is True
        )
        if candidate_scored_items:
            issues.append(
                ValidationIssue(
                    "official_scored_items",
                    "frozen_candidate manifests must not list official scored items",
                )
            )
        if manifest.get("scoring_eligibility", {}).get("aggregate_scoring_permitted") is True:
            issues.append(
                ValidationIssue(
                    "scoring_eligibility.aggregate_scoring_permitted",
                    "frozen_candidate manifests must not enable aggregate scoring",
                )
            )
        if candidate_scoring_eligible_items:
            issues.append(
                ValidationIssue(
                    "frozen_item_set.items",
                    "frozen_candidate manifests must not contain approved_scored or scoring-eligible items: "
                    + ", ".join(candidate_scoring_eligible_items),
                )
            )
    if is_scored_release:
        manifest_planned = is_planned_marker(manifest.get("release_label"))
        add_future_date_issue(
            issues,
            manifest_relative_path,
            "release_date",
            manifest.get("release_date"),
            validation_run_date,
            manifest_planned,
        )
    item_directory = manifest.get("frozen_item_set", {}).get("item_directory")
    expected_item_directory = f"items/{release_line}"
    if item_directory != expected_item_directory:
        retained_scored_item_directory = (
            manifest.get("scoring_eligibility", {}).get("aggregate_scoring_permitted") is True
            and isinstance(item_directory, str)
            and bool(listed_items)
            and all(
                item.get("release_status") == "approved_scored"
                and isinstance(item.get("path"), str)
                and item["path"].startswith(f"{item_directory}/")
                for item in listed_items
            )
        )
        provisional_candidate_item_directory = (
            not is_scored_release
            and is_planned_marker(manifest.get("release_label"))
            and isinstance(item_directory, str)
            and bool(listed_items)
            and all(
                isinstance(item.get("path"), str)
                and item["path"].startswith(f"{item_directory}/")
                for item in listed_items
            )
        )
        if not retained_scored_item_directory and not provisional_candidate_item_directory:
            issues.append(
                ValidationIssue(
                    "frozen_item_set.item_directory",
                    f"item_directory={item_directory!r} does not match benchmark release line directory {expected_item_directory!r}",
                )
            )
    if manifest.get("frozen_item_set", {}).get("item_count") != len(listed_items):
        issues.append(
            ValidationIssue(
                "frozen_item_set.item_count",
                "item_count does not equal the number of frozen_item_set.items entries",
            )
        )

    records = checksum_records(manifest)
    item_schema_record = manifest.get("item_schema", {})
    if "path" in item_schema_record:
        require_checksum_record(
            records,
            item_schema_record["path"],
            item_schema_record.get("sha256"),
            "item schema",
            issues,
        )

    require_checksum_record(records, str(required_registry_path), None, "construct registry", issues)
    require_checksum_record(
        records,
        str(VALIDATION_DOSSIER_SCHEMA_PATH),
        None,
        "validation dossier schema",
        issues,
    )
    if is_calibration_release(manifest, set(records)):
        require_checksum_record(
            records,
            str(PSYCHOMETRIC_ANALYSIS_PLAN_SCHEMA_PATH),
            None,
            "psychometric analysis plan schema",
            issues,
        )
    if manifest.get("scoring_eligibility", {}).get("aggregate_scoring_permitted") is True:
        evidence_schema = load_json(root / PSYCHOMETRIC_EVIDENCE_SCHEMA_PATH)
        require_checksum_record(
            records,
            str(PSYCHOMETRIC_EVIDENCE_SCHEMA_PATH),
            None,
            "psychometric evidence manifest schema",
            issues,
        )

    for document in manifest.get("methodology_documents", []):
        require_checksum_record(
            records,
            document["path"],
            document.get("sha256"),
            f"{document['document_type']} document",
            issues,
        )

    for record_path, expected in records.items():
        actual = sha256_file(repo_path(root, record_path))
        if actual != expected:
            issues.append(ValidationIssue(record_path, f"sha256 mismatch: expected {expected}, got {actual}"))

    dossier_cache: dict[str, dict[str, Any]] = {}
    for dossier_path in sorted(path for path in records if is_validation_dossier_checksum_path(path)):
        if dossier_path.endswith("_evidence_manifest.json"):
            continue
        dossier = load_json(repo_path(root, dossier_path))
        dossier_cache[dossier_path] = dossier
        if is_scored_release:
            dossier_planned = is_planned_marker(dossier.get("dossier_status"))
            for sample_name, sample in dossier.get("sample_provenance", {}).items():
                if not isinstance(sample, dict):
                    continue
                sample_planned = dossier_planned or is_planned_marker(sample.get("status")) or is_planned_marker(
                    sample.get("fielding_dates")
                )
                add_future_date_issue(
                    issues,
                    dossier_path,
                    f"sample_provenance.{sample_name}.fielding_dates",
                    sample.get("fielding_dates"),
                    validation_run_date,
                    sample_planned,
                )
            decision = dossier.get("decision", {})
            if isinstance(decision, dict):
                decision_planned = dossier_planned or is_planned_marker(decision.get("psychometric_decision"))
                add_future_date_issue(
                    issues,
                    dossier_path,
                    "decision.decision_date",
                    decision.get("decision_date"),
                    validation_run_date,
                    decision_planned,
                )

    item_by_id: dict[str, dict[str, Any]] = {}
    for manifest_item in listed_items:
        item_path = manifest_item["path"]
        if isinstance(item_directory, str) and not item_path.startswith(f"{item_directory}/"):
            issues.append(
                ValidationIssue(
                    item_path,
                    f"frozen item path must be under frozen_item_set.item_directory {item_directory!r}",
                )
            )
        item_data = load_json(repo_path(root, item_path))
        issues.extend(validate_with_jsonschema(item_data, item_schema, item_path))

        item_id = item_data.get("item_id")
        if item_id in item_by_id:
            issues.append(ValidationIssue(item_path, f"duplicate frozen item_id {item_id!r}"))
        item_by_id[item_id] = item_data

        require_checksum_record(records, item_path, manifest_item.get("sha256"), "frozen item", issues)

        expected_fields = {
            "item_id": item_data.get("item_id"),
            "item_version": item_data.get("version"),
            "domain": item_data.get("domain"),
            "construct": item_data.get("construct", {}).get("construct_id"),
            "release_status": item_data.get("release_status"),
        }
        for manifest_field, item_value in expected_fields.items():
            if manifest_item.get(manifest_field) != item_value:
                issues.append(
                    ValidationIssue(
                        item_path,
                        f"manifest {manifest_field}={manifest_item.get(manifest_field)!r} does not match item value {item_value!r}",
                    )
                )

        manifest_eligible = manifest_item.get("validation", {}).get("scoring_eligible")
        item_eligible = item_data.get("validation", {}).get("scoring_eligible")
        if manifest_eligible != item_eligible:
            issues.append(
                ValidationIssue(
                    item_path,
                    f"manifest validation.scoring_eligible={manifest_eligible!r} does not match item value {item_eligible!r}",
                )
            )

        raw_dossier_path = item_data.get("validation", {}).get("dossier_path")
        dossier_path = active_dossier_path(raw_dossier_path)
        if dossier_path == "":
            issues.append(
                ValidationIssue(
                    item_path,
                    f"validation.dossier_path must be a repository-relative JSON path, null, or 'not_available'; got {raw_dossier_path!r}",
                )
            )
        elif dossier_path is None:
            if item_data.get("release_status") in ("approved_item_level_only", "approved_scored") or item_eligible:
                issues.append(
                    ValidationIssue(
                        item_path,
                        "scored or item-level approval requires validation.dossier_path to reference a dossier JSON file",
                    )
                )
        else:
            require_checksum_record(records, dossier_path, None, "validation dossier", issues)
            if dossier_path not in dossier_cache:
                dossier = load_json(repo_path(root, dossier_path))
                dossier_cache[dossier_path] = dossier
            dossier = dossier_cache[dossier_path]
            dossier_items = {
                (entry.get("item_id"), entry.get("item_version")): entry
                for entry in dossier.get("items", [])
                if isinstance(entry, dict)
            }
            dossier_item = dossier_items.get((item_data.get("item_id"), item_data.get("version")))
            if dossier_item is None:
                issues.append(
                    ValidationIssue(
                        item_path,
                        f"dossier {dossier_path} does not include item_id={item_data.get('item_id')!r} with item_version={item_data.get('version')!r}",
                    )
                )
            else:
                consistency_checks = {
                    "item_path": item_path,
                    "release_status": item_data.get("release_status"),
                    "psychometric_decision": item_data.get("validation", {}).get("psychometric_decision"),
                    "scoring_eligible": item_eligible,
                }
                for field, item_value in consistency_checks.items():
                    if dossier_item.get(field) != item_value:
                        issues.append(
                            ValidationIssue(
                                item_path,
                                f"dossier {dossier_path} {field}={dossier_item.get(field)!r} does not match item value {item_value!r}",
                            )
                        )

            if dossier.get("domain") != item_data.get("domain"):
                issues.append(
                    ValidationIssue(
                        item_path,
                        f"dossier {dossier_path} domain={dossier.get('domain')!r} does not match item domain={item_data.get('domain')!r}",
                    )
                )
            if dossier.get("construct", {}).get("construct_id") != item_data.get("construct", {}).get("construct_id"):
                issues.append(
                    ValidationIssue(
                        item_path,
                        f"dossier {dossier_path} construct_id={dossier.get('construct', {}).get('construct_id')!r} does not match item construct_id={item_data.get('construct', {}).get('construct_id')!r}",
                    )
                )
            item_preregistration_path = item_data.get("validation", {}).get("preregistration_path")
            dossier_preregistration_path = dossier.get("preregistration_path")
            requires_exact_preregistration_match = (
                item_data.get("release_status") in ("approved_item_level_only", "approved_scored")
                or item_eligible is True
            )
            if requires_exact_preregistration_match and dossier_preregistration_path != item_preregistration_path:
                issues.append(
                    ValidationIssue(
                        item_path,
                        f"dossier {dossier_path} preregistration_path={dossier_preregistration_path!r} does not match item validation.preregistration_path={item_preregistration_path!r}",
                    )
                )
            preregistration_path = item_preregistration_path
            if preregistration_path in (None, "not_available"):
                issues.append(
                    ValidationIssue(
                        item_path,
                        "validation.preregistration_path must reference the preregistration used by the validation dossier",
                    )
                )
            elif not repo_path(root, preregistration_path).is_file():
                issues.append(
                    ValidationIssue(
                        item_path,
                        f"validation.preregistration_path does not exist: {preregistration_path}",
                    )
                )
            if isinstance(dossier_preregistration_path, str) and not repo_path(root, dossier_preregistration_path).is_file():
                issues.append(
                    ValidationIssue(
                        item_path,
                        f"dossier {dossier_path} preregistration_path does not exist: {dossier_preregistration_path}",
                    )
                )

        construct_id = item_data.get("construct", {}).get("construct_id")
        construct = registry_by_construct.get(construct_id)
        if construct is None:
            issues.append(ValidationIssue(item_path, f"construct_id {construct_id!r} is not in construct registry"))
        elif item_data.get("item_id") not in construct.get("allowed_item_ids", []):
            issues.append(
                ValidationIssue(
                    item_path,
                    f"item_id {item_data.get('item_id')!r} is not allowed for construct_id {construct_id!r}",
                )
            )

    official_scored = manifest.get("official_scored_items", [])
    duplicate_official_scored = sorted(
        item_id for item_id in set(official_scored) if official_scored.count(item_id) > 1
    )
    for item_id in duplicate_official_scored:
        issues.append(ValidationIssue("official_scored_items", f"duplicate official scored item_id {item_id!r}"))

    if manifest.get("scoring_eligibility", {}).get("official_scored_item_count") != len(official_scored):
        issues.append(
            ValidationIssue(
                "scoring_eligibility.official_scored_item_count",
                "does not equal the number of official_scored_items entries",
            )
        )

    for item_id in official_scored:
        item = item_by_id.get(item_id)
        if item is None:
            issues.append(ValidationIssue("official_scored_items", f"{item_id!r} is not in the frozen item set"))
            continue
        if item.get("release_status") != "approved_scored":
            issues.append(
                ValidationIssue(item_id, "official scored item must have release_status == 'approved_scored'")
            )
        if item.get("validation", {}).get("scoring_eligible") is not True:
            issues.append(
                ValidationIssue(item_id, "official scored item must have validation.scoring_eligible == true")
            )

    official_scored_set = set(official_scored)
    for item_id, item in item_by_id.items():
        if item.get("release_status") == "approved_scored" or item.get("validation", {}).get("scoring_eligible"):
            if item_id not in official_scored_set:
                issues.append(
                    ValidationIssue(
                        item_id,
                        "scoring-eligible or approved-scored frozen item must be listed in official_scored_items",
                    )
                )

    if manifest.get("scoring_eligibility", {}).get("aggregate_scoring_permitted") is True:
        scored_dossier_paths = sorted(
            path
            for path in {
                active_dossier_path(item.get("validation", {}).get("dossier_path"))
                for item in item_by_id.values()
                if item.get("release_status") == "approved_scored"
                or item.get("validation", {}).get("scoring_eligible") is True
            }
            if path
        )
        for dossier_path in scored_dossier_paths:
            if not dossier_path:
                continue
            dossier = dossier_cache.get(dossier_path)
            if dossier is None:
                dossier = load_json(repo_path(root, dossier_path))
                dossier_cache[dossier_path] = dossier

            if not (
                dossier.get("dossier_status") == "approved_scored"
                or dossier.get("decision", {}).get("scoring_eligible") is True
                or dossier.get("decision", {}).get("psychometric_decision") == "approved_scored"
            ):
                continue

            evidence_path = evidence_manifest_path_for_dossier(dossier_path)
            require_checksum_record(records, evidence_path, None, "psychometric evidence manifest", issues)
            try:
                evidence_manifest = load_json(repo_path(root, evidence_path))
            except ReleaseValidationError as exc:
                issues.append(ValidationIssue(evidence_path, str(exc)))
                continue

            issues.extend(validate_with_jsonschema(evidence_manifest, evidence_schema, evidence_path))
            evidence_checks = {
                "validation_dossier_path": dossier_path,
                "preregistration_path": dossier.get("preregistration_path"),
                "benchmark_version": manifest.get("benchmark_version"),
                "construct_id": dossier.get("construct", {}).get("construct_id"),
            }
            for field, expected in evidence_checks.items():
                if evidence_manifest.get(field) != expected:
                    issues.append(
                        ValidationIssue(
                            evidence_path,
                            f"{field}={evidence_manifest.get(field)!r} does not match required value {expected!r}",
                        )
                    )

            artifact_ids = {
                artifact.get("artifact_id")
                for artifact in evidence_manifest.get("output_artifact_hashes", [])
                if isinstance(artifact, dict)
            }
            for mapped_statistic in evidence_manifest.get("reported_statistic_map", []):
                if not isinstance(mapped_statistic, dict):
                    continue
                artifact_id = mapped_statistic.get("artifact_id")
                if artifact_id not in artifact_ids:
                    issues.append(
                        ValidationIssue(
                            evidence_path,
                            f"reported_statistic_map statistic_id={mapped_statistic.get('statistic_id')!r} references unknown artifact_id {artifact_id!r}",
                        )
                    )

    if issues:
        rendered = "\n".join(f"- {issue.render()}" for issue in issues)
        raise ReleaseValidationError(f"release validation failed with {len(issues)} issue(s):\n{rendered}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an ANX-Bench release manifest.")
    parser.add_argument("manifest", type=Path, help="Path to releases/<version>/manifest.json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_release(args.manifest)
    except ReleaseValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"release validation passed: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
