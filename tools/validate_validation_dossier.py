#!/usr/bin/env python3
"""Validate an ANX-Bench psychometric validation dossier.

This gate combines JSON Schema validation with the release-blocking
psychometric thresholds in docs/psychometric_validation_protocol.md. Planned
development dossiers may pass without numeric results. Approval dossiers must
carry machine-checkable numeric evidence.
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


SCHEMA_PATH = Path("schema/validation_dossier.schema.json")
PROVENANCE_SCHEMA_PATH = Path("schema/evidence_provenance.schema.json")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


class DossierValidationError(Exception):
    """Raised when a validation dossier fails the approval gate."""


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
        raise DossierValidationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DossierValidationError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(dossier_path: Path) -> Path:
    search_start = dossier_path.resolve().parent
    for candidate in (search_start, *search_start.parents):
        if (candidate / SCHEMA_PATH).is_file() and (candidate / "docs/psychometric_validation_protocol.md").is_file():
            return candidate
    return Path.cwd().resolve()


def validate_with_jsonschema(instance: Any, schema: dict[str, Any]) -> list[ValidationIssue]:
    try:
        from jsonschema import Draft202012Validator
    except ModuleNotFoundError:
        return validate_with_builtin_schema(instance, schema)

    validator = Draft202012Validator(schema)
    issues = []
    for error in sorted(validator.iter_errors(instance), key=lambda err: list(err.path)):
        location = "/".join(str(part) for part in error.path) or "$"
        issues.append(ValidationIssue(location, error.message))
    return issues


def validate_with_builtin_schema(instance: Any, schema: dict[str, Any]) -> list[ValidationIssue]:
    """Validate the JSON Schema subset used by the validation dossier schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise DossierValidationError(f"unsupported external JSON Schema reference: {ref}")
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
            return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
        if expected == "string":
            return isinstance(value, str)
        if expected == "array":
            return isinstance(value, list)
        if expected == "object":
            return isinstance(value, dict)
        if expected == "null":
            return value is None
        raise DossierValidationError(f"unsupported JSON Schema type: {expected}")

    def check(value: Any, subschema: dict[str, Any], path: str, collect: list[ValidationIssue]) -> None:
        if "$ref" in subschema:
            check(value, resolve_ref(subschema["$ref"]), path, collect)
            return

        for branch in subschema.get("allOf", []):
            check(value, branch, path, collect)

        if "if" in subschema:
            probe: list[ValidationIssue] = []
            check(value, subschema["if"], path, probe)
            if not probe and "then" in subschema:
                check(value, subschema["then"], path, collect)

        expected_type = subschema.get("type")
        if expected_type is not None:
            expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
            if not any(type_matches(value, candidate) for candidate in expected_types):
                collect.append(
                    ValidationIssue(
                        path,
                        f"expected type {' or '.join(expected_types)}, got {type(value).__name__}",
                    )
                )
                return

        if "const" in subschema and value != subschema["const"]:
            collect.append(ValidationIssue(path, f"expected constant {subschema['const']!r}"))
            return

        if "enum" in subschema and value not in subschema["enum"]:
            collect.append(ValidationIssue(path, f"value {value!r} is not in enum"))

        if isinstance(value, str):
            if "minLength" in subschema and len(value) < subschema["minLength"]:
                collect.append(ValidationIssue(path, "string is shorter than minLength"))
            if "pattern" in subschema and re.fullmatch(subschema["pattern"], value) is None:
                collect.append(ValidationIssue(path, "string does not match pattern"))
            if subschema.get("format") == "date":
                try:
                    date.fromisoformat(value)
                except ValueError:
                    collect.append(ValidationIssue(path, "string is not an ISO date"))

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in subschema and value < subschema["minimum"]:
                collect.append(ValidationIssue(path, "number is below minimum"))
            if "maximum" in subschema and value > subschema["maximum"]:
                collect.append(ValidationIssue(path, "number is above maximum"))

        if isinstance(value, list):
            if "minItems" in subschema and len(value) < subschema["minItems"]:
                collect.append(ValidationIssue(path, "array has too few items"))
            if "items" in subschema:
                for index, item in enumerate(value):
                    check(item, subschema["items"], f"{path}/{index}", collect)

        if isinstance(value, dict):
            for key in subschema.get("required", []):
                if key not in value:
                    collect.append(ValidationIssue(path, f"missing required property {key!r}"))

            properties = subschema.get("properties", {})
            for key, item in value.items():
                if key in properties:
                    check(item, properties[key], f"{path}/{key}", collect)
                elif subschema.get("additionalProperties") is False:
                    collect.append(ValidationIssue(path, f"unexpected property {key!r}"))
                elif isinstance(subschema.get("additionalProperties"), dict):
                    check(item, subschema["additionalProperties"], f"{path}/{key}", collect)

    check(instance, schema, "$", issues)
    return issues


def approval_status(dossier: dict[str, Any]) -> str:
    status = dossier.get("dossier_status")
    decision = dossier.get("decision", {}).get("psychometric_decision")
    if status == "approved_scored" or decision == "approved_scored":
        return "approved_scored"
    if status == "approved_item_level_only" or decision == "approved_item_level_only":
        return "approved_item_level_only"
    return "not_approved"


def _num(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def _ci_excludes_zero(result: dict[str, Any]) -> bool:
    low = _num(result.get("ci_low"))
    high = _num(result.get("ci_high"))
    if low is None or high is None:
        return False
    return low > 0 or high < 0


def _parse_date(value: Any, path: str, issues: list[ValidationIssue]) -> date | None:
    if not isinstance(value, str):
        issues.append(ValidationIssue(path, "date value must be an ISO date string"))
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        issues.append(ValidationIssue(path, "date value must be an ISO date string"))
        return None


def _dates_in_text(value: Any) -> list[date]:
    if not isinstance(value, str):
        return []
    parsed: list[date] = []
    for match in ISO_DATE_RE.findall(value):
        try:
            parsed.append(date.fromisoformat(match))
        except ValueError:
            continue
    return parsed


def _resolve_dossier_reference(repo_root: Path, dossier_path: Path, reference: str) -> Path:
    local_path = dossier_path.resolve().parent / reference
    if local_path.is_file():
        return local_path
    return repo_root / reference


def _release_manifest_path(repo_root: Path, benchmark_version: Any) -> Path | None:
    if not isinstance(benchmark_version, str) or not benchmark_version.startswith("v"):
        return None
    candidate = repo_root / "releases" / benchmark_version / "manifest.json"
    if candidate.is_file():
        return candidate
    return None


def validate_temporal_gate(repo_root: Path, dossier: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    validation_date = _parse_date(dossier.get("decision", {}).get("decision_date"), "decision/decision_date", issues)

    if validation_date is not None:
        for sample_name, sample in dossier.get("sample_provenance", {}).items():
            if not isinstance(sample, dict) or sample.get("status") != "fielded":
                continue
            fielding_dates = _dates_in_text(sample.get("fielding_dates"))
            if not fielding_dates:
                issues.append(
                    ValidationIssue(
                        f"sample_provenance/{sample_name}/fielding_dates",
                        "fielded samples require explicit ISO fielding dates",
                    )
                )
                continue
            for fielding_date in fielding_dates:
                if fielding_date > validation_date:
                    issues.append(
                        ValidationIssue(
                            f"sample_provenance/{sample_name}/fielding_dates",
                            "fielding dates cannot be after the validation decision date",
                        )
                    )
                    break

    manifest_path = _release_manifest_path(repo_root, dossier.get("benchmark_version"))
    if manifest_path is not None:
        manifest = load_json(manifest_path)
        if isinstance(manifest, dict):
            release_date = _parse_date(manifest.get("release_date"), f"{manifest_path}/release_date", issues)
            if release_date is not None and release_date > date.today():
                issues.append(
                    ValidationIssue(
                        f"{manifest_path}/release_date",
                        "release date cannot be after today",
                    )
                )
    return issues


def _completed_evidence_families(dossier: dict[str, Any]) -> set[str]:
    evidence = dossier.get("evidence", {})
    if not isinstance(evidence, dict):
        return set()

    families: set[str] = set()
    for family, record in evidence.items():
        if family == "external_validity" and isinstance(record, dict):
            if any(isinstance(child, dict) and child.get("status") == "completed" for child in record.values()):
                families.add("external_validity")
            continue
        if isinstance(record, dict) and record.get("status") == "completed":
            families.add(str(family))
    if isinstance(dossier.get("results"), dict):
        families.add("retention")
    return families


def _has_valid_checksum(artifact: Any) -> bool:
    return isinstance(artifact, dict) and isinstance(artifact.get("sha256"), str) and SHA256_RE.fullmatch(artifact["sha256"])


def _statistic_is_signed(statistic: dict[str, Any]) -> bool:
    signoff = statistic.get("signoff")
    if not isinstance(signoff, dict):
        return False
    return (
        signoff.get("signature_status") == "signed"
        and isinstance(signoff.get("signer"), str)
        and bool(signoff["signer"].strip())
        and isinstance(signoff.get("role"), str)
        and bool(signoff["role"].strip())
        and isinstance(signoff.get("signed_date"), str)
    )


def validate_evidence_provenance(
    repo_root: Path,
    dossier_path: Path,
    dossier: dict[str, Any],
    provenance_schema: dict[str, Any],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    provenance_reference = dossier.get("evidence_provenance_path")
    completed_families = _completed_evidence_families(dossier)
    status = approval_status(dossier)

    if not isinstance(provenance_reference, str) or not provenance_reference:
        if status == "approved_scored" or completed_families:
            return [ValidationIssue("evidence_provenance_path", "completed or approved dossiers require evidence provenance")]
        return []

    provenance_path = _resolve_dossier_reference(repo_root, dossier_path, provenance_reference)
    try:
        provenance = load_json(provenance_path)
    except DossierValidationError as exc:
        if status == "approved_scored" or completed_families:
            return [ValidationIssue("evidence_provenance_path", str(exc))]
        return []

    if not isinstance(provenance, dict):
        issues.append(ValidationIssue("evidence_provenance_path", "provenance root must be a JSON object"))
        return issues

    for issue in validate_with_jsonschema(provenance, provenance_schema):
        issues.append(ValidationIssue(f"evidence_provenance/{issue.path}", issue.message))

    validation_date = _parse_date(dossier.get("decision", {}).get("decision_date"), "decision/decision_date", issues)
    today = date.today()
    if provenance.get("evidence_status") != "observed_data" and status == "approved_scored":
        issues.append(
            ValidationIssue(
                "evidence_provenance/evidence_status",
                "approved_scored dossiers require observed-data provenance, not placeholder provenance",
            )
        )

    for index, window in enumerate(provenance.get("fielding_windows", [])):
        if not isinstance(window, dict):
            continue
        window_path = f"evidence_provenance/fielding_windows/{index}"
        if status == "approved_scored" and window.get("status") == "planned_or_placeholder":
            issues.append(ValidationIssue(f"{window_path}/status", "approved_scored dossiers cannot use planned fielding provenance"))
        for key in ("observed_start_date", "observed_end_date"):
            if window.get(key) is None:
                if status == "approved_scored" and window.get("status") != "not_applicable":
                    issues.append(ValidationIssue(f"{window_path}/{key}", "approved_scored fielding windows require observed dates"))
                continue
            observed_date = _parse_date(window.get(key), f"{window_path}/{key}", issues)
            if observed_date is not None and validation_date is not None and observed_date > validation_date:
                issues.append(ValidationIssue(f"{window_path}/{key}", "observed fielding date cannot be after validation date"))
            if observed_date is not None and observed_date > today:
                issues.append(ValidationIssue(f"{window_path}/{key}", "observed fielding date cannot be after today"))

    observed_families: set[str] = set()
    for index, statistic in enumerate(provenance.get("validation_statistics", [])):
        if not isinstance(statistic, dict):
            continue
        stat_path = f"evidence_provenance/validation_statistics/{index}"
        family = statistic.get("analysis_family")
        if statistic.get("evidence_status") == "observed_data" and isinstance(family, str):
            observed_families.add(family)

        if status == "approved_scored" and statistic.get("evidence_status") != "observed_data":
            issues.append(ValidationIssue(f"{stat_path}/evidence_status", "approved_scored statistics require observed-data provenance"))

        if statistic.get("evidence_status") == "observed_data" or status == "approved_scored":
            for artifact_index, artifact in enumerate(statistic.get("data_artifacts", [])):
                if not _has_valid_checksum(artifact):
                    issues.append(ValidationIssue(f"{stat_path}/data_artifacts/{artifact_index}/sha256", "missing valid SHA-256 checksum"))
            for script_index, script in enumerate(statistic.get("analysis_scripts", [])):
                if not _has_valid_checksum(script):
                    issues.append(ValidationIssue(f"{stat_path}/analysis_scripts/{script_index}/sha256", "missing valid SHA-256 checksum"))
            if not _statistic_is_signed(statistic):
                issues.append(ValidationIssue(f"{stat_path}/signoff", "observed statistics require signer, role, signed_date, and signed status"))

        signoff = statistic.get("signoff")
        if isinstance(signoff, dict) and signoff.get("signed_date") is not None:
            signed_date = _parse_date(signoff.get("signed_date"), f"{stat_path}/signoff/signed_date", issues)
            if signed_date is not None and signed_date > today:
                issues.append(ValidationIssue(f"{stat_path}/signoff/signed_date", "signed date cannot be after today"))
            if signed_date is not None and validation_date is not None and signed_date > validation_date:
                issues.append(ValidationIssue(f"{stat_path}/signoff/signed_date", "signed date cannot be after validation date"))

    for family in sorted(completed_families):
        if family not in observed_families:
            issues.append(
                ValidationIssue(
                    "evidence_provenance/validation_statistics",
                    f"completed evidence family {family!r} requires observed-data provenance",
                )
            )

    return issues


def validate_thresholds(dossier: dict[str, Any]) -> list[ValidationIssue]:
    status = approval_status(dossier)
    if status == "not_approved":
        return []

    issues: list[ValidationIssue] = []
    results = dossier.get("results")
    if not isinstance(results, dict):
        return [ValidationIssue("results", "approval dossiers require structured numeric results")]

    confirmation = dossier.get("sample_provenance", {}).get("confirmation_sample", {})
    confirmation_n = confirmation.get("analytic_n")
    result_n = results.get("analytic_n")
    if not isinstance(confirmation_n, int) or confirmation_n < 1000:
        issues.append(
            ValidationIssue(
                "sample_provenance/confirmation_sample/analytic_n",
                "approved dossiers require independent confirmation analytic_n >= 1000",
            )
        )
    if not isinstance(result_n, int) or result_n != confirmation_n:
        issues.append(
            ValidationIssue(
                "results/analytic_n",
                "results analytic_n must equal confirmation_sample analytic_n",
            )
        )

    if status == "approved_scored":
        retained_item_count = results.get("retained_item_count")
        if not isinstance(retained_item_count, int) or retained_item_count < 3:
            issues.append(
                ValidationIssue(
                    "results/retained_item_count",
                    "approved_scored construct scoring requires at least 3 retained items",
                )
            )

    reliability = results.get("reliability", {})
    omega = _num(reliability.get("omega"))
    if omega is None or omega < 0.70:
        issues.append(ValidationIssue("results/reliability/omega", "omega must be >= 0.70"))

    cfa = results.get("cfa_fit", {})
    cfa_bounds = [
        ("cfi", ">=", 0.90),
        ("tli", ">=", 0.90),
        ("rmsea", "<=", 0.08),
        ("srmr", "<=", 0.08),
    ]
    for key, operator, threshold in cfa_bounds:
        value = _num(cfa.get(key))
        failed = value is None or (operator == ">=" and value < threshold) or (operator == "<=" and value > threshold)
        if failed:
            issues.append(ValidationIssue(f"results/cfa_fit/{key}", f"CFA {key} must be {operator} {threshold}"))

    retained_item_ids: set[str] = set()
    for index, item in enumerate(results.get("item_statistics", [])):
        if not isinstance(item, dict) or item.get("retained") is not True:
            continue
        item_path = f"results/item_statistics/{index}"
        item_id = item.get("item_id")
        if isinstance(item_id, str):
            retained_item_ids.add(item_id)

        loading = _num(item.get("primary_loading"))
        if loading is None or loading < 0.50:
            issues.append(ValidationIssue(f"{item_path}/primary_loading", "retained items require loading >= 0.50"))

        item_total = _num(item.get("corrected_item_total_correlation"))
        if item_total is None or item_total < 0.30:
            issues.append(
                ValidationIssue(
                    f"{item_path}/corrected_item_total_correlation",
                    "retained items require corrected item-total correlation >= 0.30",
                )
            )

        for key in ("floor_rate", "ceiling_rate"):
            value = _num(item.get(key))
            if value is None or value > 0.70:
                issues.append(ValidationIssue(f"{item_path}/{key}", f"{key} must be <= 0.70"))
        for key in ("adjacent_floor_rate", "adjacent_ceiling_rate"):
            value = _num(item.get(key))
            if value is None or value > 0.85:
                issues.append(ValidationIssue(f"{item_path}/{key}", f"{key} must be <= 0.85"))
        missing = _num(item.get("missing_rate"))
        if missing is None or missing > 0.10:
            issues.append(ValidationIssue(f"{item_path}/missing_rate", "confirmation missing rate must be <= 0.10"))

    if status == "approved_scored" and len(retained_item_ids) < 3:
        issues.append(
            ValidationIssue(
                "results/item_statistics",
                "approved_scored construct scoring requires at least 3 retained item statistics",
            )
        )

    dif = results.get("dif", {})
    if dif.get("unresolved_practical_dif") is True:
        issues.append(ValidationIssue("results/dif/unresolved_practical_dif", "no unresolved practical DIF is allowed"))
    for index, analysis in enumerate(dif.get("analyses", [])):
        if not isinstance(analysis, dict):
            continue
        if (
            analysis.get("statistically_supported") is True
            and analysis.get("practically_meaningful") is True
            and analysis.get("resolved") is not True
        ):
            issues.append(
                ValidationIssue(
                    f"results/dif/analyses/{index}",
                    "statistically supported and practically meaningful DIF must be resolved before approval",
                )
            )

    invariance = results.get("invariance", {})
    for key in ("metric_delta_cfi", "scalar_delta_cfi"):
        value = _num(invariance.get(key))
        if value is None or value < -0.010:
            issues.append(ValidationIssue(f"results/invariance/{key}", f"{key} must be >= -0.010"))
    for key in ("metric_delta_rmsea", "scalar_delta_rmsea"):
        value = _num(invariance.get(key))
        if value is None or value > 0.015:
            issues.append(ValidationIssue(f"results/invariance/{key}", f"{key} must be <= 0.015"))

    external = results.get("external_validity", {})
    convergent = external.get("convergent", {})
    if convergent.get("direction_matches") is not True or convergent.get("passes_threshold") is not True:
        issues.append(ValidationIssue("results/external_validity/convergent", "convergent validity must pass"))
    convergent_coef = abs(_num(convergent.get("coefficient")) or 0.0)
    if convergent_coef < 0.30 or not _ci_excludes_zero(convergent):
        issues.append(
            ValidationIssue(
                "results/external_validity/convergent/coefficient",
                "convergent coefficient must be at least 0.30 in absolute value with CI excluding zero",
            )
        )

    discriminant = external.get("discriminant", {})
    discriminant_coef = abs(_num(discriminant.get("coefficient")) or 0.0)
    if discriminant.get("passes_threshold") is not True or discriminant_coef >= 0.80:
        issues.append(
            ValidationIssue(
                "results/external_validity/discriminant/coefficient",
                "discriminant validity requires construct association below 0.80 and passing threshold",
            )
        )

    criterion = external.get("criterion", {})
    if criterion.get("direction_matches") is not True or criterion.get("passes_threshold") is not True:
        issues.append(ValidationIssue("results/external_validity/criterion", "criterion validity must pass"))

    incremental = external.get("incremental_validity", {})
    if incremental.get("direction_matches") is not True or incremental.get("passes_threshold") is not True:
        issues.append(ValidationIssue("results/external_validity/incremental_validity", "incremental validity must pass"))
    metric = incremental.get("coefficient_metric")
    coefficient = _num(incremental.get("coefficient"))
    if metric in {"adjusted_r2_delta", "pseudo_r2_delta"} and (coefficient is None or coefficient < 0.01):
        issues.append(
            ValidationIssue(
                "results/external_validity/incremental_validity/coefficient",
                "incremental R-squared delta must be >= 0.01",
            )
        )
    if metric == "odds_ratio" and (coefficient is None or coefficient < 1.20):
        issues.append(
            ValidationIssue(
                "results/external_validity/incremental_validity/coefficient",
                "incremental odds ratio must be >= 1.20 per standard deviation",
            )
        )

    return issues


def validate_dossier(dossier_path: Path) -> None:
    repo_root = find_repo_root(dossier_path)
    dossier = load_json(dossier_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    provenance_schema = load_json(repo_root / PROVENANCE_SCHEMA_PATH)

    if not isinstance(dossier, dict):
        raise DossierValidationError("dossier root must be a JSON object")

    issues = validate_with_jsonschema(dossier, schema)
    issues.extend(validate_temporal_gate(repo_root, dossier))
    issues.extend(validate_evidence_provenance(repo_root, dossier_path, dossier, provenance_schema))
    issues.extend(validate_thresholds(dossier))
    if issues:
        rendered = "\n".join(f"- {issue.render()}" for issue in issues)
        raise DossierValidationError(f"validation dossier failed:\n{rendered}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path, help="Path to validation dossier JSON")
    args = parser.parse_args(argv)

    try:
        validate_dossier(args.dossier)
    except DossierValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"validation dossier passed: {args.dossier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
