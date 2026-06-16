#!/usr/bin/env python3
"""Score ANX-Bench wave response JSONL files.

The scorer implements docs/scoring_spec.md: it validates respondent-item rows,
recomputes released item scores from item scoring keys, enforces release
manifest eligibility, and emits schema-valid score output JSON.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


WAVE_RESPONSE_SCHEMA_PATH = Path("schema/wave_response.schema.json")
SCORE_OUTPUT_SCHEMA_PATH = Path("schema/score_output.schema.json")
REGISTRY_PATH = Path("constructs/v0.1/registry.json")
CONFIDENCE_LEVEL = 0.95
Z_95 = 1.96


class ScoringError(Exception):
    """Raised when wave scoring cannot produce a reproducible output."""


@dataclass
class ItemAccumulator:
    item_id: str
    item_version: str
    domain: str
    construct_id: str
    official_scored: bool
    scoring_eligible: bool
    row_count: int = 0
    respondents: set[str] = field(default_factory=set)
    included_rows: list[dict[str, Any]] = field(default_factory=list)
    missingness_counts: Counter[str] = field(default_factory=Counter)
    exclusion_counts: Counter[str] = field(default_factory=Counter)
    scoring_ineligible_row_count: int = 0


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ScoringError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ScoringError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(manifest_path: Path) -> Path:
    search_start = manifest_path.resolve().parent
    for candidate in (search_start, *search_start.parents):
        if (candidate / WAVE_RESPONSE_SCHEMA_PATH).is_file() and (candidate / SCORE_OUTPUT_SCHEMA_PATH).is_file():
            return candidate
    return Path.cwd().resolve()


def repo_path(root: Path, relative_path: str) -> Path:
    candidate = root / relative_path
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ScoringError(f"path escapes repository root: {relative_path}") from exc
    return candidate


def validate_with_jsonschema(instance: Any, schema: dict[str, Any], label: str) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ModuleNotFoundError:
        validate_with_builtin_schema(instance, schema, label)
        return

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "$"
        raise ScoringError(f"{label}: schema validation failed at {location}: {first.message}")


def validate_with_builtin_schema(instance: Any, schema: dict[str, Any], label: str) -> None:
    """Validate the JSON Schema subset used by scorer input and output schemas."""

    issues: list[str] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise ScoringError(f"{label}: unsupported external JSON Schema reference: {ref}")
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
        raise ScoringError(f"{label}: unsupported JSON Schema type: {expected}")

    def check(value: Any, subschema: dict[str, Any], path: str) -> None:
        if "$ref" in subschema:
            check(value, resolve_ref(subschema["$ref"]), path)
            return

        if "allOf" in subschema:
            for child in subschema["allOf"]:
                check(value, child, path)

        if "oneOf" in subschema:
            match_count = 0
            for child in subschema["oneOf"]:
                before = len(issues)
                check(value, child, path)
                if len(issues) == before:
                    match_count += 1
                else:
                    del issues[before:]
            if match_count != 1:
                issues.append(f"{path}: value matches {match_count} oneOf branches")
            return

        if "not" in subschema:
            before = len(issues)
            check(value, subschema["not"], path)
            matched = len(issues) == before
            del issues[before:]
            if matched:
                issues.append(f"{path}: value matches disallowed schema")
            return

        if "if" in subschema:
            before = len(issues)
            check(value, subschema["if"], path)
            condition_matched = len(issues) == before
            del issues[before:]
            if condition_matched and "then" in subschema:
                check(value, subschema["then"], path)

        expected_type = subschema.get("type")
        if expected_type is not None:
            expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
            if not any(type_matches(value, candidate) for candidate in expected_types):
                issues.append(f"{path}: expected type {' or '.join(expected_types)}, got {type(value).__name__}")
                return

        if "const" in subschema and value != subschema["const"]:
            issues.append(f"{path}: expected constant {subschema['const']!r}")
            return

        if "enum" in subschema and value not in subschema["enum"]:
            issues.append(f"{path}: value {value!r} is not in enum")

        if isinstance(value, str):
            if "minLength" in subschema and len(value) < subschema["minLength"]:
                issues.append(f"{path}: string is shorter than minLength")
            if "maxLength" in subschema and len(value) > subschema["maxLength"]:
                issues.append(f"{path}: string is longer than maxLength")
            if "pattern" in subschema and re.fullmatch(subschema["pattern"], value) is None:
                issues.append(f"{path}: string does not match pattern")
            if subschema.get("format") == "date-time":
                try:
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    issues.append(f"{path}: string is not an ISO date-time")

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in subschema and value < subschema["minimum"]:
                issues.append(f"{path}: number is below minimum")
            if "maximum" in subschema and value > subschema["maximum"]:
                issues.append(f"{path}: number is above maximum")
            if "exclusiveMinimum" in subschema and value <= subschema["exclusiveMinimum"]:
                issues.append(f"{path}: number is not above exclusiveMinimum")

        if isinstance(value, list):
            if "minItems" in subschema and len(value) < subschema["minItems"]:
                issues.append(f"{path}: array has too few items")
            if subschema.get("uniqueItems"):
                encoded = [json.dumps(item, sort_keys=True) for item in value]
                if len(encoded) != len(set(encoded)):
                    issues.append(f"{path}: array items are not unique")
            if "items" in subschema:
                for index, item in enumerate(value):
                    check(item, subschema["items"], f"{path}/{index}")

        if isinstance(value, dict):
            for key in subschema.get("required", []):
                if key not in value:
                    issues.append(f"{path}: missing required property {key!r}")

            properties = subschema.get("properties", {})
            for key, item in value.items():
                if key in properties:
                    check(item, properties[key], f"{path}/{key}")
                elif subschema.get("additionalProperties") is False:
                    issues.append(f"{path}: unexpected property {key!r}")
                elif isinstance(subschema.get("additionalProperties"), dict):
                    check(item, subschema["additionalProperties"], f"{path}/{key}")

    check(instance, schema, "$")
    if issues:
        raise ScoringError(f"{label}: schema validation failed at {issues[0]}")


def read_jsonl(path: Path, schema: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    row = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise ScoringError(
                        f"{path}: line {line_number}: invalid JSON: column {exc.colno}: {exc.msg}"
                    ) from exc
                validate_with_jsonschema(row, schema, f"{path}: line {line_number}")
                rows.append(row)
    except FileNotFoundError as exc:
        raise ScoringError(f"missing wave response JSONL file: {path}") from exc
    return rows


def canonical_raw_key(raw_response: Any) -> str:
    if isinstance(raw_response, bool) or raw_response is None:
        raise ScoringError(f"raw_response cannot be scored: {raw_response!r}")
    return str(raw_response)


def ci_from_values(values: list[float], weights: list[float], method: str) -> dict[str, float | str]:
    if not values:
        raise ValueError("cannot compute confidence interval for empty values")
    weight_sum = sum(weights)
    mean = sum(weight * value for value, weight in zip(values, weights)) / weight_sum
    if len(values) < 2:
        standard_error = 0.0
    else:
        effective_n = (weight_sum**2) / sum(weight**2 for weight in weights)
        weighted_variance = sum(
            weight * ((value - mean) ** 2) for value, weight in zip(values, weights)
        ) / weight_sum
        standard_error = math.sqrt(weighted_variance / effective_n)
    lower = max(1.0, mean - Z_95 * standard_error)
    upper = min(5.0, mean + Z_95 * standard_error)
    return {
        "point_estimate": mean,
        "standard_error": standard_error,
        "confidence_level": CONFIDENCE_LEVEL,
        "ci_lower": lower,
        "ci_upper": upper,
        "ci_method": method,
    }


def null_ci() -> dict[str, None]:
    return {
        "point_estimate": None,
        "standard_error": None,
        "confidence_level": None,
        "ci_lower": None,
        "ci_upper": None,
        "ci_method": None,
    }


def load_release_context(root: Path, manifest_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest = load_json(manifest_path)
    items: dict[str, Any] = {}
    for manifest_item in manifest.get("frozen_item_set", {}).get("items", []):
        item = load_json(repo_path(root, manifest_item["path"]))
        item_id = manifest_item["item_id"]
        if item_id in items:
            raise ScoringError(f"duplicate frozen item_id in manifest: {item_id}")
        if item.get("item_id") != item_id:
            raise ScoringError(f"{manifest_item['path']}: item_id does not match manifest")
        if item.get("version") != manifest_item["item_version"]:
            raise ScoringError(f"{manifest_item['path']}: item version does not match manifest")
        items[item_id] = {
            "manifest": manifest_item,
            "item": item,
        }
    registry = load_json(root / REGISTRY_PATH)
    return manifest, items, registry


def validate_manifest_eligibility(manifest: dict[str, Any], items: dict[str, Any]) -> None:
    official_scored = set(manifest.get("official_scored_items", []))
    declared_count = manifest.get("scoring_eligibility", {}).get("official_scored_item_count")
    if declared_count != len(official_scored):
        raise ScoringError("scoring_eligibility.official_scored_item_count does not match official_scored_items")

    for item_id in official_scored:
        if item_id not in items:
            raise ScoringError(f"official scored item is not in frozen item set: {item_id}")
        manifest_item = items[item_id]["manifest"]
        item = items[item_id]["item"]
        gates = [
            manifest_item.get("release_status") == "approved_scored",
            manifest_item.get("validation", {}).get("scoring_eligible") is True,
            item.get("release_status") == "approved_scored",
            item.get("validation", {}).get("scoring_eligible") is True,
        ]
        if not all(gates):
            raise ScoringError(f"official scored item fails approved_scored eligibility gates: {item_id}")


def observed_row_score(row: dict[str, Any], item: dict[str, Any], line_label: str) -> float:
    scoring_key = item.get("scoring", {}).get("scoring_key", {})
    raw_key = canonical_raw_key(row["raw_response"])
    if raw_key not in scoring_key:
        raise ScoringError(f"{line_label}: raw_response {row['raw_response']!r} is not in scoring_key")
    expected = scoring_key[raw_key]
    if row["scored_value"] != expected:
        raise ScoringError(
            f"{line_label}: scored_value {row['scored_value']!r} does not match recomputed score {expected!r}"
        )
    return float(expected)


def counter_dict(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def score_wave(wave_path: Path, manifest_path: Path) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    root = find_repo_root(manifest_path)
    manifest, items, registry = load_release_context(root, manifest_path)
    validate_manifest_eligibility(manifest, items)

    wave_schema = load_json(root / WAVE_RESPONSE_SCHEMA_PATH)
    score_schema = load_json(root / SCORE_OUTPUT_SCHEMA_PATH)
    rows = read_jsonl(wave_path, wave_schema)

    benchmark_version = manifest["benchmark_version"]
    aggregate_permitted = manifest["scoring_eligibility"]["aggregate_scoring_permitted"]
    official_scored = set(manifest.get("official_scored_items", []))
    item_accumulators: dict[str, ItemAccumulator] = {}
    total_missingness: Counter[str] = Counter()
    total_exclusions: Counter[str] = Counter()
    respondents: set[str] = set()
    wave_ids: set[str] = set()
    included_row_count = 0
    scoring_ineligible_row_count = 0

    for manifest_item in manifest["frozen_item_set"]["items"]:
        item_id = manifest_item["item_id"]
        item = items[item_id]["item"]
        item_accumulators[item_id] = ItemAccumulator(
            item_id=item_id,
            item_version=manifest_item["item_version"],
            domain=manifest_item["domain"],
            construct_id=manifest_item["construct"],
            official_scored=item_id in official_scored,
            scoring_eligible=(
                manifest_item.get("release_status") == "approved_scored"
                and manifest_item.get("validation", {}).get("scoring_eligible") is True
                and item.get("release_status") == "approved_scored"
                and item.get("validation", {}).get("scoring_eligible") is True
            ),
        )

    for index, row in enumerate(rows, start=1):
        line_label = f"{wave_path}: line {index}"
        if row["benchmark_version"] != benchmark_version:
            raise ScoringError(
                f"{line_label}: benchmark_version {row['benchmark_version']!r} does not match manifest {benchmark_version!r}"
            )
        item_id = row["item_id"]
        if item_id not in items:
            raise ScoringError(f"{line_label}: item_id {item_id!r} is not in manifest frozen_item_set")

        context = items[item_id]
        manifest_item = context["manifest"]
        item = context["item"]
        if row["item_version"] != manifest_item["item_version"] or row["item_version"] != item["version"]:
            raise ScoringError(
                f"{line_label}: item_version {row['item_version']!r} does not match released item version {manifest_item['item_version']!r}"
            )

        if row["missingness_code"] == "observed":
            observed_row_score(row, item, line_label)

        acc = item_accumulators[item_id]
        acc.row_count += 1
        acc.respondents.add(row["respondent_id_hash"])
        acc.missingness_counts[row["missingness_code"]] += 1
        total_missingness[row["missingness_code"]] += 1
        respondents.add(row["respondent_id_hash"])
        wave_ids.add(row["wave_id"])

        for flag in row["exclusion_flags"]:
            acc.exclusion_counts[flag] += 1
            total_exclusions[flag] += 1

        row_is_includable = (
            aggregate_permitted
            and acc.official_scored
            and acc.scoring_eligible
            and row["missingness_code"] == "observed"
            and not row["exclusion_flags"]
        )
        if row_is_includable:
            acc.included_rows.append(row)
            included_row_count += 1
        else:
            acc.scoring_ineligible_row_count += 1
            scoring_ineligible_row_count += 1

    item_scores = [item_summary(acc) for acc in item_accumulators.values() if acc.row_count > 0]
    construct_scores: list[dict[str, Any]] = []
    domain_scores: list[dict[str, Any]] = []
    overall_score: dict[str, Any] | None = None

    if aggregate_permitted:
        construct_scores = aggregate_constructs(item_scores)
        domain_scores = aggregate_domains(construct_scores, registry)
        overall_score = aggregate_overall(domain_scores)

    output = {
        "schema_version": "v0.1.0",
        "benchmark_version": benchmark_version,
        "wave_ids": sorted(wave_ids),
        "manifest_path": manifest_path.relative_to(root).as_posix(),
        "input_path": str(wave_path),
        "aggregate_scoring_permitted": aggregate_permitted,
        "official_scored_item_count": len(official_scored),
        "row_count": len(rows),
        "unique_respondent_count": len(respondents),
        "included_row_count": included_row_count,
        "scoring_ineligible_row_count": scoring_ineligible_row_count,
        "missingness_counts": counter_dict(total_missingness),
        "exclusion_counts": counter_dict(total_exclusions),
        "item_scores": item_scores,
        "construct_scores": construct_scores,
        "domain_scores": domain_scores,
        "overall_score": overall_score,
    }
    validate_with_jsonschema(output, score_schema, "score_output.schema.json")
    return output


def item_summary(acc: ItemAccumulator) -> dict[str, Any]:
    included_respondents = {row["respondent_id_hash"] for row in acc.included_rows}
    contributing_weight_sum = sum(float(row["survey_weight"]) for row in acc.included_rows)
    if acc.included_rows:
        ci = ci_from_values(
            [float(row["scored_value"]) for row in acc.included_rows],
            [float(row["survey_weight"]) for row in acc.included_rows],
            "large_sample_weighted_mean",
        )
    else:
        ci = null_ci()

    return {
        "item_id": acc.item_id,
        "item_version": acc.item_version,
        "domain": acc.domain,
        "construct_id": acc.construct_id,
        "official_scored": acc.official_scored,
        "scoring_eligible": acc.scoring_eligible,
        "included_in_aggregate": bool(acc.included_rows),
        "row_count": acc.row_count,
        "unique_respondent_count": len(acc.respondents),
        "included_row_count": len(acc.included_rows),
        "included_unique_respondent_count": len(included_respondents),
        "missingness_counts": counter_dict(acc.missingness_counts),
        "exclusion_counts": counter_dict(acc.exclusion_counts),
        "scoring_ineligible_row_count": acc.scoring_ineligible_row_count,
        "contributing_weight_sum": contributing_weight_sum,
        **ci,
    }


def aggregate_constructs(item_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_construct: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in item_scores:
        if item["included_in_aggregate"] and item["point_estimate"] is not None:
            by_construct[item["construct_id"]].append(item)

    summaries = []
    for construct_id in sorted(by_construct):
        items = by_construct[construct_id]
        ci = ci_from_values(
            [item["point_estimate"] for item in items],
            [1.0 for _ in items],
            "equal_weighted_lower_level_scores",
        )
        summaries.append(
            {
                "id": construct_id,
                "domain": items[0]["domain"],
                "contributing_n": sum(item["included_unique_respondent_count"] for item in items),
                "contributing_weight_sum": sum(item["contributing_weight_sum"] for item in items),
                "contributing_item_count": len(items),
                "contributing_construct_count": 1,
                **ci,
            }
        )
    return summaries


def aggregate_domains(
    construct_scores: list[dict[str, Any]], registry: dict[str, Any]
) -> list[dict[str, Any]]:
    domain_order = [domain["domain_id"] for domain in registry.get("domains", [])]
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for construct in construct_scores:
        by_domain[construct["domain"]].append(construct)

    summaries = []
    for domain_id in domain_order:
        constructs = by_domain.get(domain_id, [])
        if not constructs:
            continue
        ci = ci_from_values(
            [construct["point_estimate"] for construct in constructs],
            [1.0 for _ in constructs],
            "equal_weighted_lower_level_scores",
        )
        summaries.append(
            {
                "id": domain_id,
                "domain": domain_id,
                "contributing_n": sum(construct["contributing_n"] for construct in constructs),
                "contributing_weight_sum": sum(construct["contributing_weight_sum"] for construct in constructs),
                "contributing_item_count": sum(construct["contributing_item_count"] for construct in constructs),
                "contributing_construct_count": len(constructs),
                **ci,
            }
        )
    return summaries


def aggregate_overall(domain_scores: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not domain_scores:
        return None
    ci = ci_from_values(
        [domain["point_estimate"] for domain in domain_scores],
        [1.0 for _ in domain_scores],
        "equal_weighted_lower_level_scores",
    )
    return {
        "contributing_n": sum(domain["contributing_n"] for domain in domain_scores),
        "contributing_weight_sum": sum(domain["contributing_weight_sum"] for domain in domain_scores),
        "contributing_domain_count": len(domain_scores),
        "contributing_construct_count": sum(domain["contributing_construct_count"] for domain in domain_scores),
        "contributing_item_count": sum(domain["contributing_item_count"] for domain in domain_scores),
        **ci,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score an ANX-Bench wave response JSONL file.")
    parser.add_argument("wave_jsonl", type=Path, help="Path to respondent-item wave response JSONL")
    parser.add_argument("manifest", type=Path, help="Path to releases/<version>/manifest.json")
    parser.add_argument("-o", "--output", type=Path, help="Write score output JSON to this path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        output = score_wave(args.wave_jsonl, args.manifest)
    except ScoringError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
