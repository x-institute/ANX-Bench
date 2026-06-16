#!/usr/bin/env python3
"""Validate an ANX-Bench event registry.

The event-registry gate checks JSON Schema conformance and lifecycle rules
needed for event-study inference. Confirmatory use is allowed only for frozen
registries, and frozen registries must be locked before or explicitly after
outcome inspection under the schema's allowed post-lock status.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import validate_release


EVENT_REGISTRY_SCHEMA_PATH = Path("schema/event_registry.schema.json")
CONFIRMATORY_OUTCOME_STATUSES = {"not_inspected", "inspected_after_lock"}


class EventRegistryValidationError(Exception):
    """Raised when an event registry fails the validation gate."""


def _find_repo_root(registry_path: Path) -> Path:
    for start in (registry_path.resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / EVENT_REGISTRY_SCHEMA_PATH).is_file():
                return candidate
    return Path.cwd().resolve()


def _schema_issues(instance: Any, schema: dict[str, Any], schema_name: str) -> list[validate_release.ValidationIssue]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ModuleNotFoundError:
        return validate_release.validate_with_jsonschema(instance, schema, schema_name)

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues = []
    for error in sorted(validator.iter_errors(instance), key=lambda err: list(err.path)):
        location = "/".join(str(part) for part in error.path) or "$"
        issues.append(validate_release.ValidationIssue(f"{schema_name}:{location}", error.message))
    return issues


def _event_ids(registry: dict[str, Any]) -> list[str]:
    event_ids = []
    for event in registry.get("events", []):
        if isinstance(event, dict) and isinstance(event.get("event_id"), str):
            event_ids.append(event["event_id"])
    return event_ids


def _semantic_issues(registry: dict[str, Any], intended_use: str) -> list[validate_release.ValidationIssue]:
    issues: list[validate_release.ValidationIssue] = []
    status = registry.get("registry_status")
    outcome_status = registry.get("outcome_inspection_status")

    if intended_use == "confirmatory":
        if status == "template":
            issues.append(
                validate_release.ValidationIssue(
                    "registry_status",
                    "template registries cannot support confirmatory event-study claims",
                )
            )
        elif status != "frozen":
            issues.append(
                validate_release.ValidationIssue(
                    "registry_status",
                    "confirmatory event-study claims require registry_status 'frozen'",
                )
            )

    if status == "frozen":
        if outcome_status not in CONFIRMATORY_OUTCOME_STATUSES:
            issues.append(
                validate_release.ValidationIssue(
                    "outcome_inspection_status",
                    "frozen registries require outcome_inspection_status 'not_inspected' or 'inspected_after_lock'",
                )
            )
        if not isinstance(registry.get("registry_lock_date"), str):
            issues.append(
                validate_release.ValidationIssue(
                    "registry_lock_date",
                    "frozen registries require a non-null ISO registry_lock_date",
                )
            )

        for index, event in enumerate(registry.get("events", [])):
            if not isinstance(event, dict):
                continue
            event_path = f"events/{index}"
            category = event.get("category")
            if not isinstance(event.get("lock_date"), str):
                issues.append(
                    validate_release.ValidationIssue(
                        f"{event_path}/lock_date",
                        "frozen event records require a non-null ISO lock_date",
                    )
                )
            if category != "no_event":
                if event.get("baseline_window") is None:
                    issues.append(
                        validate_release.ValidationIssue(
                            f"{event_path}/baseline_window",
                            "event-study records require a baseline_window before freeze",
                        )
                    )
                if event.get("exposure_window") is None:
                    issues.append(
                        validate_release.ValidationIssue(
                            f"{event_path}/exposure_window",
                            "event-study records require an exposure_window before freeze",
                        )
                    )
                if not event.get("follow_up_windows"):
                    issues.append(
                        validate_release.ValidationIssue(
                            f"{event_path}/follow_up_windows",
                            "event-study records require at least one follow_up_window before freeze",
                        )
                    )

    event_ids = _event_ids(registry)
    if len(event_ids) != len(set(event_ids)):
        issues.append(validate_release.ValidationIssue("events", "event_id values must be unique"))

    return issues


def validate_event_registry(registry_path: Path, intended_use: str = "registry") -> None:
    if intended_use not in {"registry", "exploratory", "confirmatory"}:
        raise EventRegistryValidationError(
            "intended_use must be one of 'registry', 'exploratory', or 'confirmatory'"
        )

    registry_path = registry_path.resolve()
    root = _find_repo_root(registry_path)

    try:
        registry = validate_release.load_json(registry_path)
        schema = validate_release.load_json(root / EVENT_REGISTRY_SCHEMA_PATH)
    except validate_release.ReleaseValidationError as exc:
        raise EventRegistryValidationError(str(exc)) from exc

    issues = _schema_issues(registry, schema, str(EVENT_REGISTRY_SCHEMA_PATH))
    if isinstance(registry, dict):
        issues.extend(_semantic_issues(registry, intended_use))
    else:
        issues.append(validate_release.ValidationIssue("$", "event registry root must be an object"))

    if issues:
        rendered = "\n".join(issue.render() for issue in issues)
        raise EventRegistryValidationError(f"event registry validation failed:\n{rendered}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an ANX-Bench event registry.")
    parser.add_argument("registry_path", type=Path)
    parser.add_argument(
        "--intended-use",
        choices=["registry", "exploratory", "confirmatory"],
        default="registry",
        help="Use confirmatory to require a frozen registry eligible for confirmatory event-study claims.",
    )
    args = parser.parse_args(argv)

    try:
        validate_event_registry(args.registry_path, intended_use=args.intended_use)
    except EventRegistryValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"event registry validation passed: {args.registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
