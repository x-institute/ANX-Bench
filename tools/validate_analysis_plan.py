#!/usr/bin/env python3
"""Validate an ANX-Bench psychometric analysis plan.

The analysis-plan gate validates the plan JSON against the repository schema
and then checks the release-bound preregistration, freeze status, benchmark
version, checksum coverage, and planned item set.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import validate_release


ANALYSIS_PLAN_SCHEMA_PATH = Path("schema/psychometric_analysis_plan.schema.json")


class AnalysisPlanValidationError(Exception):
    """Raised when an analysis plan fails the machine-validation gate."""


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError as exc:
        raise AnalysisPlanValidationError(f"path is outside repository root: {path}") from exc


def _find_repo_root(plan_path: Path, release_path: Path) -> Path:
    for start in (release_path.resolve().parent, plan_path.resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / ANALYSIS_PLAN_SCHEMA_PATH).is_file() and (
                candidate / validate_release.RELEASE_SCHEMA_PATH
            ).is_file():
                return candidate
    return validate_release.find_repo_root(release_path)


def _analysis_plan_item_ids(plan: dict[str, Any], manifest: dict[str, Any]) -> set[str]:
    item_directory = manifest.get("frozen_item_set", {}).get("item_directory")
    candidates: list[dict[str, Any]] = []

    for input_record in plan.get("required_inputs", []):
        if not isinstance(input_record, dict):
            continue
        input_id = input_record.get("input_id")
        input_path = input_record.get("path")
        if input_id in {"item_files", "frozen_item_files"}:
            candidates.append(input_record)
            continue
        if isinstance(item_directory, str) and isinstance(input_path, str):
            if input_path == item_directory or input_path.startswith(f"{item_directory}/"):
                candidates.append(input_record)

    item_id_sets = []
    for candidate in candidates:
        required_fields = candidate.get("required_fields")
        if isinstance(required_fields, list) and all(isinstance(field, str) for field in required_fields):
            item_id_sets.append(set(required_fields))

    if len(item_id_sets) != 1:
        raise AnalysisPlanValidationError(
            "analysis plan must contain exactly one item-file required_inputs record with planned item IDs"
        )
    return item_id_sets[0]


def _checksum_records(manifest: dict[str, Any]) -> dict[str, str]:
    try:
        return validate_release.checksum_records(manifest)
    except validate_release.ReleaseValidationError as exc:
        raise AnalysisPlanValidationError(str(exc)) from exc


def validate_analysis_plan(plan_path: Path, release_path: Path) -> None:
    plan_path = plan_path.resolve()
    release_path = release_path.resolve()
    root = _find_repo_root(plan_path, release_path)

    try:
        plan = validate_release.load_json(plan_path)
        manifest = validate_release.load_json(release_path)
        schema = validate_release.load_json(root / ANALYSIS_PLAN_SCHEMA_PATH)
    except validate_release.ReleaseValidationError as exc:
        raise AnalysisPlanValidationError(str(exc)) from exc

    issues: list[validate_release.ValidationIssue] = []
    plan_relative_path = _relative_to_root(plan_path, root)

    issues.extend(
        validate_release.validate_with_jsonschema(
            plan,
            schema,
            str(ANALYSIS_PLAN_SCHEMA_PATH),
        )
    )

    registration = plan.get("registration", {})
    registration_is_object = isinstance(registration, dict)
    preregistration_path = registration.get("preregistration_path") if registration_is_object else None
    if not isinstance(preregistration_path, str):
        issues.append(
            validate_release.ValidationIssue(
                "registration.preregistration_path",
                "must be a repository-relative preregistration path",
            )
        )
    else:
        try:
            preregistration_file = validate_release.repo_path(root, preregistration_path)
        except validate_release.ReleaseValidationError as exc:
            issues.append(validate_release.ValidationIssue("registration.preregistration_path", str(exc)))
        else:
            if not preregistration_file.is_file():
                issues.append(
                    validate_release.ValidationIssue(
                        "registration.preregistration_path",
                        f"preregistration file does not exist: {preregistration_path}",
                    )
                )

    analysis_plan_path = registration.get("analysis_plan_path") if registration_is_object else None
    if analysis_plan_path != plan_relative_path:
        issues.append(
            validate_release.ValidationIssue(
                "registration.analysis_plan_path",
                f"must equal the validated plan path {plan_relative_path!r}",
            )
        )

    authoritative_contract = registration.get("authoritative_contract") if registration_is_object else None
    if authoritative_contract is not True:
        issues.append(
            validate_release.ValidationIssue(
                "registration.authoritative_contract",
                "must be true for a release-bound calibration analysis plan",
            )
        )

    outcome_inspection_status = registration.get("outcome_inspection_status") if registration_is_object else None
    if outcome_inspection_status != "not_inspected":
        issues.append(
            validate_release.ValidationIssue(
                "registration.outcome_inspection_status",
                "must be 'not_inspected' before the plan can freeze a calibration release",
            )
        )

    if plan.get("benchmark_version") != manifest.get("benchmark_version"):
        issues.append(
            validate_release.ValidationIssue(
                "benchmark_version",
                f"plan benchmark_version={plan.get('benchmark_version')!r} does not match release benchmark_version={manifest.get('benchmark_version')!r}",
            )
        )

    records = _checksum_records(manifest)
    schema_record = records.get(str(ANALYSIS_PLAN_SCHEMA_PATH))
    if schema_record is None:
        issues.append(
            validate_release.ValidationIssue(
                str(ANALYSIS_PLAN_SCHEMA_PATH),
                "release manifest must checksum the psychometric analysis plan schema",
            )
        )
    else:
        actual_schema_sha = validate_release.sha256_file(root / ANALYSIS_PLAN_SCHEMA_PATH)
        if schema_record != actual_schema_sha:
            issues.append(
                validate_release.ValidationIssue(
                    str(ANALYSIS_PLAN_SCHEMA_PATH),
                    f"sha256 mismatch: expected {schema_record}, got {actual_schema_sha}",
                )
            )

    plan_record = records.get(plan_relative_path)
    if plan_record is None:
        issues.append(
            validate_release.ValidationIssue(
                plan_relative_path,
                "release manifest must checksum the validated analysis plan",
            )
        )
    else:
        actual_plan_sha = validate_release.sha256_file(plan_path)
        if plan_record != actual_plan_sha:
            issues.append(
                validate_release.ValidationIssue(
                    plan_relative_path,
                    f"sha256 mismatch: expected {plan_record}, got {actual_plan_sha}",
                )
            )

    try:
        planned_item_ids = _analysis_plan_item_ids(plan, manifest)
    except AnalysisPlanValidationError as exc:
        issues.append(validate_release.ValidationIssue("required_inputs", str(exc)))
    else:
        manifest_item_ids = {
            item.get("item_id")
            for item in manifest.get("frozen_item_set", {}).get("items", [])
            if isinstance(item, dict)
        }
        if not all(isinstance(item_id, str) for item_id in manifest_item_ids):
            issues.append(
                validate_release.ValidationIssue(
                    "frozen_item_set.items",
                    "all frozen manifest items must contain string item_id values",
                )
            )
        elif planned_item_ids != manifest_item_ids:
            missing = sorted(manifest_item_ids - planned_item_ids)
            extra = sorted(planned_item_ids - manifest_item_ids)
            details = []
            if missing:
                details.append("missing from plan: " + ", ".join(missing))
            if extra:
                details.append("not in manifest: " + ", ".join(extra))
            issues.append(
                validate_release.ValidationIssue(
                    "required_inputs.item_files.required_fields",
                    "planned item IDs must equal the manifest frozen item set"
                    + (f" ({'; '.join(details)})" if details else ""),
                )
            )

    if issues:
        rendered = "\n".join(f"- {issue.render()}" for issue in issues)
        raise AnalysisPlanValidationError(
            f"analysis plan validation failed with {len(issues)} issue(s):\n{rendered}"
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an ANX-Bench psychometric analysis plan.")
    parser.add_argument("plan", type=Path, help="Path to analysis/.../*_analysis_plan.json")
    parser.add_argument(
        "--release",
        required=True,
        type=Path,
        help="Path to releases/<version>/manifest.json that freezes this plan",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_analysis_plan(args.plan, args.release)
    except AnalysisPlanValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"analysis plan validation passed: {args.plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
