#!/usr/bin/env python3
"""Validate an ANX-Bench frozen sampling and weighting plan."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import validate_release


SAMPLING_PLAN_SCHEMA_PATH = Path("schema/sampling_plan.schema.json")


class SamplingPlanValidationError(Exception):
    """Raised when a sampling plan fails the machine-validation gate."""


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError as exc:
        raise SamplingPlanValidationError(f"path is outside repository root: {path}") from exc


def _find_repo_root(plan_path: Path) -> Path:
    for start in (plan_path.resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / SAMPLING_PLAN_SCHEMA_PATH).is_file() and (
                candidate / validate_release.RELEASE_SCHEMA_PATH
            ).is_file():
                return candidate
    return Path.cwd().resolve()


def _has_nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def _claim_records(plan: dict[str, Any], claim_type: str) -> list[dict[str, Any]]:
    return [
        claim
        for claim in plan.get("claim_limits", [])
        if isinstance(claim, dict) and claim.get("claim_type") == claim_type
    ]


def _weighting_metadata_present(plan: dict[str, Any]) -> bool:
    weighting = plan.get("weighting_method")
    trim_bounds = plan.get("trim_bounds")
    if not isinstance(weighting, dict) or not isinstance(trim_bounds, dict):
        return False
    mapping = weighting.get("survey_weight_mapping")
    return (
        weighting.get("status") == "planned"
        and weighting.get("method") != "none"
        and _has_nonempty_list(weighting.get("construction_steps"))
        and isinstance(weighting.get("final_weight_variable"), str)
        and bool(weighting.get("final_weight_variable"))
        and isinstance(mapping, dict)
        and mapping.get("wave_response_field") == "survey_weight"
        and mapping.get("source_variable") == weighting.get("final_weight_variable")
        and isinstance(trim_bounds.get("lower"), (int, float))
        and isinstance(trim_bounds.get("upper"), (int, float))
        and trim_bounds.get("lower") < trim_bounds.get("upper")
    )


def _variance_metadata_present(plan: dict[str, Any]) -> bool:
    variance = plan.get("variance_design")
    if not isinstance(variance, dict):
        return False
    estimator = variance.get("estimator")
    return (
        isinstance(estimator, str)
        and estimator not in {"not_applicable", "model_based_only"}
        and isinstance(variance.get("primary_standard_error"), str)
        and len(variance["primary_standard_error"].strip()) >= 10
        and isinstance(variance.get("software"), str)
        and bool(variance["software"].strip())
    )


def _validate_sampling_semantics(plan: dict[str, Any], plan_path: Path, root: Path) -> list[validate_release.ValidationIssue]:
    issues: list[validate_release.ValidationIssue] = []
    relative_path = _relative_to_root(plan_path, root)

    if plan_path.name.endswith(".template.json"):
        issues.append(
            validate_release.ValidationIssue(
                "$",
                "template sampling plans cannot serve as frozen claim-bearing bridge artifacts; validate the non-template plan path",
            )
        )

    registration = plan.get("registration")
    if not isinstance(registration, dict):
        issues.append(validate_release.ValidationIssue("registration", "must be present for a frozen sampling plan"))
    else:
        if registration.get("sampling_plan_path") != relative_path:
            issues.append(
                validate_release.ValidationIssue(
                    "registration.sampling_plan_path",
                    f"must equal the validated plan path {relative_path!r}",
                )
            )
        if registration.get("authoritative_contract") is not True:
            issues.append(
                validate_release.ValidationIssue(
                    "registration.authoritative_contract",
                    "must be true before sampling metadata can support benchmark claims",
                )
            )
        if registration.get("freeze_status") != "frozen_before_fielding":
            issues.append(
                validate_release.ValidationIssue(
                    "registration.freeze_status",
                    "must be 'frozen_before_fielding'",
                )
            )
        if registration.get("outcome_inspection_status") != "not_inspected":
            issues.append(
                validate_release.ValidationIssue(
                    "registration.outcome_inspection_status",
                    "must be 'not_inspected'",
                )
            )
        preregistration_path = registration.get("preregistration_path")
        if isinstance(preregistration_path, str):
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

    target_population = plan.get("target_population")
    if not isinstance(target_population, dict):
        issues.append(validate_release.ValidationIssue("target_population", "missing target population metadata"))
    else:
        required_text_fields = ["description", "geography", "language"]
        for field in required_text_fields:
            if not isinstance(target_population.get(field), str) or not target_population[field].strip():
                issues.append(validate_release.ValidationIssue(f"target_population.{field}", "must be nonempty"))
        for field in ["inclusion_criteria", "exclusion_criteria", "coverage_limits"]:
            if not _has_nonempty_list(target_population.get(field)):
                issues.append(validate_release.ValidationIssue(f"target_population.{field}", "must be a nonempty list"))

    if not _weighting_metadata_present(plan):
        issues.append(
            validate_release.ValidationIssue(
                "weighting_method",
                "missing weight construction metadata, valid trim bounds, or final-weight mapping to survey_weight",
            )
        )

    population_claims = [
        claim for claim in _claim_records(plan, "population_estimate") if claim.get("status") != "blocked"
    ]
    if population_claims and not _weighting_metadata_present(plan):
        issues.append(
            validate_release.ValidationIssue(
                "claim_limits.population_estimate",
                "population claims require planned weighting metadata and final survey_weight mapping",
            )
        )
    if population_claims and not _variance_metadata_present(plan):
        issues.append(
            validate_release.ValidationIssue(
                "claim_limits.population_estimate",
                "population claims require variance metadata with an applicable standard-error estimator",
            )
        )

    return issues


def validate_sampling_plan(plan_path: Path) -> None:
    plan_path = plan_path.resolve()
    root = _find_repo_root(plan_path)

    try:
        plan = validate_release.load_json(plan_path)
        schema = validate_release.load_json(root / SAMPLING_PLAN_SCHEMA_PATH)
    except validate_release.ReleaseValidationError as exc:
        raise SamplingPlanValidationError(str(exc)) from exc

    issues: list[validate_release.ValidationIssue] = []
    issues.extend(
        validate_release.validate_with_jsonschema(
            plan,
            schema,
            str(SAMPLING_PLAN_SCHEMA_PATH),
        )
    )

    if isinstance(plan, dict):
        issues.extend(_validate_sampling_semantics(plan, plan_path, root))
    else:
        issues.append(validate_release.ValidationIssue("$", "sampling plan must be a JSON object"))

    if issues:
        rendered = "\n".join(f"- {issue.render()}" for issue in issues)
        raise SamplingPlanValidationError(
            f"sampling plan validation failed with {len(issues)} issue(s):\n{rendered}"
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an ANX-Bench sampling and weighting plan.")
    parser.add_argument("plan", type=Path, help="Path to sampling/.../*_sampling_plan*.json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        validate_sampling_plan(args.plan)
    except SamplingPlanValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Sampling plan validation passed: {args.plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
