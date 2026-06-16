#!/usr/bin/env python3
"""Validate an ANX-Bench content-validity dossier.

The content-validity gate precedes psychometric promotion. This validator
checks the dossier schema and independently recomputes reviewer independence,
rating completeness, item-level CVI, S-CVI/Ave, facet coverage, unresolved
flags, promotion flags, and signoff consistency before any item set can move
toward scored use.
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


SCHEMA_PATH = Path("schema/content_validity_dossier.schema.json")
CRITERIA = ("relevance", "clarity", "facet_fit", "ethical_acceptability")
PROMOTION_DECISION = "approved_for_psychometric_promotion_review"
NONPROMOTING_DECISIONS = {"not_reviewed", "approved_for_development_only", "blocked"}
ITEM_CVI_THRESHOLD = 0.78
SCALE_CVI_THRESHOLD = 0.90
MINIMUM_INDEPENDENT_REVIEWERS = 3
PROMOTION_READY_STATUSES = {"completed"}
NONPROMOTION_STATUSES = {"preregistered_template", "in_review", "superseded", "blocked"}
OPEN_FLAGS = {"unresolved", "pending_review"}


class ContentValidityDossierError(Exception):
    """Raised when a content-validity dossier fails validation."""


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
        raise ContentValidityDossierError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContentValidityDossierError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(dossier_path: Path) -> Path:
    search_start = dossier_path.resolve().parent
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
    """Validate the JSON Schema subset used by the content-validity schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise ContentValidityDossierError(f"unsupported external JSON Schema reference: {ref}")
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
        raise ContentValidityDossierError(f"unsupported JSON Schema type: {expected}")

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
            if subschema.get("uniqueItems") is True and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
                collect.append(ValidationIssue(path, "array items are not unique"))
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


def _num(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _close(observed: Any, expected: float | None, tolerance: float = 0.005) -> bool:
    observed_num = _num(observed)
    if expected is None:
        return observed is None
    return observed_num is not None and abs(observed_num - expected) <= tolerance


def _retained_item_ids(dossier: dict[str, Any]) -> set[str]:
    retained = set(dossier.get("item_ids", []))
    for decision in dossier.get("revision_decisions", []):
        item_id = decision.get("item_id")
        if decision.get("decision") == "exclude" and isinstance(item_id, str):
            retained.discard(item_id)
    for item in dossier.get("item_reviews", []):
        item_id = item.get("item_id")
        if item.get("required_revision") == "exclude" and isinstance(item_id, str):
            retained.discard(item_id)
    return retained


def _rating_is_complete(rating: dict[str, Any]) -> bool:
    return all(isinstance(rating.get(criterion), int) and not isinstance(rating.get(criterion), bool) for criterion in CRITERIA)


def _criterion_cvi(ratings: list[dict[str, Any]], criterion: str) -> float | None:
    if not ratings or any(not isinstance(rating.get(criterion), int) for rating in ratings):
        return None
    acceptable = sum(1 for rating in ratings if rating[criterion] >= 3)
    return acceptable / len(ratings)


def _flag_is_open(value: Any) -> bool:
    return value in OPEN_FLAGS


def validate_content_validity_rules(dossier: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    status = dossier.get("dossier_status")
    eligibility = dossier.get("promotion_eligibility", {})
    signoff = dossier.get("signoff", {})
    reviewer_panel = dossier.get("reviewer_panel", {})
    reviewers = reviewer_panel.get("reviewers", [])
    if not isinstance(reviewers, list):
        reviewers = []

    reviewer_ids = [reviewer.get("reviewer_id") for reviewer in reviewers if isinstance(reviewer, dict)]
    if len(reviewer_ids) != len(set(reviewer_ids)):
        issues.append(ValidationIssue("reviewer_panel/reviewers", "reviewer_id values must be unique"))

    independent_reviewers = {
        reviewer.get("reviewer_id")
        for reviewer in reviewers
        if isinstance(reviewer, dict) and reviewer.get("independent") is True
    }
    completed_independent_reviewers = {
        reviewer.get("reviewer_id")
        for reviewer in reviewers
        if isinstance(reviewer, dict)
        and reviewer.get("independent") is True
        and reviewer.get("review_completed") is True
    }

    if reviewer_panel.get("reviewer_count") != len(reviewers):
        issues.append(ValidationIssue("reviewer_panel/reviewer_count", "must equal the number of listed reviewers"))
    if reviewer_panel.get("independent_reviewer_count") != len(independent_reviewers):
        issues.append(
            ValidationIssue("reviewer_panel/independent_reviewer_count", "must equal the number of listed independent reviewers")
        )

    has_minimum_independent = len(completed_independent_reviewers) >= MINIMUM_INDEPENDENT_REVIEWERS
    promotion_claimed = eligibility.get("scored_promotion_eligible") is True or signoff.get("content_validity_decision") == PROMOTION_DECISION

    if status in NONPROMOTION_STATUSES and promotion_claimed:
        issues.append(ValidationIssue("dossier_status", "non-completed dossiers cannot claim scored-promotion eligibility"))
    if status in PROMOTION_READY_STATUSES and not promotion_claimed:
        issues.append(ValidationIssue("promotion_eligibility/scored_promotion_eligible", "completed dossiers must record the scored-promotion decision"))

    reviewer_id_set = set(reviewer_ids)
    retained_ids = _retained_item_ids(dossier)
    item_ids = set(dossier.get("item_ids", []))
    reviewed_ids = {item.get("item_id") for item in dossier.get("item_reviews", []) if isinstance(item, dict)}
    if reviewed_ids != item_ids:
        issues.append(ValidationIssue("item_reviews", "item_reviews must cover exactly the dossier item_ids"))

    computed_overall: dict[str, float] = {}
    unresolved_counts = {
        "construct_overlap": 0,
        "reading_level": 0,
        "harm_ethics": 0,
    }

    for index, item in enumerate(dossier.get("item_reviews", [])):
        if not isinstance(item, dict):
            continue
        item_path = f"item_reviews/{index}"
        item_id = item.get("item_id")
        ratings = item.get("reviewer_ratings", [])
        if not isinstance(ratings, list):
            continue

        seen_rating_ids: set[str] = set()
        independent_ratings: dict[str, dict[str, Any]] = {}
        for rating_index, rating in enumerate(ratings):
            if not isinstance(rating, dict):
                continue
            rating_id = rating.get("reviewer_id")
            rating_path = f"{item_path}/reviewer_ratings/{rating_index}"
            if rating_id not in reviewer_id_set:
                issues.append(ValidationIssue(f"{rating_path}/reviewer_id", "must reference a listed reviewer"))
            if rating_id in seen_rating_ids:
                issues.append(ValidationIssue(f"{rating_path}/reviewer_id", "duplicate reviewer rating for item"))
            seen_rating_ids.add(rating_id)
            if rating_id in completed_independent_reviewers:
                independent_ratings[rating_id] = rating

        complete_required = promotion_claimed or status == "completed"
        if complete_required:
            missing = sorted(completed_independent_reviewers - set(independent_ratings))
            if missing:
                issues.append(ValidationIssue(f"{item_path}/reviewer_ratings", f"missing completed independent reviewer ratings: {', '.join(missing)}"))
            for rating_id, rating in sorted(independent_ratings.items()):
                if not _rating_is_complete(rating):
                    issues.append(ValidationIssue(f"{item_path}/reviewer_ratings/{rating_id}", "all four criterion ratings are required"))

        cvi_source = [independent_ratings[reviewer_id] for reviewer_id in sorted(independent_ratings)]
        criterion_values = {criterion: _criterion_cvi(cvi_source, criterion) for criterion in CRITERIA}
        for criterion, expected in criterion_values.items():
            observed = item.get("criterion_cvi", {}).get(criterion)
            if not _close(observed, expected):
                issues.append(ValidationIssue(f"{item_path}/criterion_cvi/{criterion}", f"must equal recomputed I-CVI {expected}"))

        overall_expected = None if any(value is None for value in criterion_values.values()) else min(value for value in criterion_values.values() if value is not None)
        if not _close(item.get("overall_item_cvi"), overall_expected):
            issues.append(ValidationIssue(f"{item_path}/overall_item_cvi", f"must equal the minimum criterion I-CVI {overall_expected}"))
        if isinstance(item_id, str) and item_id in retained_ids and overall_expected is not None:
            computed_overall[item_id] = overall_expected

        if isinstance(item_id, str) and item_id in retained_ids:
            if _flag_is_open(item.get("construct_overlap_flag")):
                unresolved_counts["construct_overlap"] += 1
            if _flag_is_open(item.get("reading_level_flag")):
                unresolved_counts["reading_level"] += 1
            if _flag_is_open(item.get("harm_ethics_flag")):
                unresolved_counts["harm_ethics"] += 1

    scale = dossier.get("scale_level_cvi", {})
    retained_values = [computed_overall[item_id] for item_id in sorted(retained_ids) if item_id in computed_overall]
    scale_expected = sum(retained_values) / len(retained_values) if retained_values and len(retained_values) == len(retained_ids) else None
    if not _close(scale.get("scale_cvi_average"), scale_expected):
        issues.append(ValidationIssue("scale_level_cvi/scale_cvi_average", f"must equal recomputed S-CVI/Ave {scale_expected}"))

    universal_expected = None
    if retained_values and len(retained_values) == len(retained_ids):
        universal_expected = sum(1 for value in retained_values if value == 1.0) / len(retained_values)
    if not _close(scale.get("scale_cvi_universal_agreement"), universal_expected):
        issues.append(
            ValidationIssue("scale_level_cvi/scale_cvi_universal_agreement", f"must equal recomputed S-CVI/UA {universal_expected}")
        )

    required_facets_covered = True
    facet_ids = {facet.get("facet_id") for facet in dossier.get("domain_facets", []) if isinstance(facet, dict)}
    for index, item in enumerate(dossier.get("item_reviews", [])):
        primary = item.get("primary_facet_id") if isinstance(item, dict) else None
        if primary not in facet_ids:
            issues.append(ValidationIssue(f"item_reviews/{index}/primary_facet_id", "must reference a declared domain facet"))

    for index, facet in enumerate(dossier.get("domain_facets", [])):
        if not isinstance(facet, dict) or facet.get("required_for_scored_promotion") is not True:
            continue
        mapped_ids = [item_id for item_id in facet.get("mapped_item_ids", []) if isinstance(item_id, str)]
        for item_id in mapped_ids:
            if item_id not in item_ids:
                issues.append(ValidationIssue(f"domain_facets/{index}/mapped_item_ids", f"unknown item_id {item_id!r}"))
        covered = any(
            item_id in retained_ids
            and computed_overall.get(item_id, -1) >= ITEM_CVI_THRESHOLD
            and not any(
                _flag_is_open(item.get(flag))
                for item in dossier.get("item_reviews", [])
                if isinstance(item, dict) and item.get("item_id") == item_id
                for flag in ("construct_overlap_flag", "reading_level_flag", "harm_ethics_flag")
            )
            for item_id in mapped_ids
        )
        if not covered:
            required_facets_covered = False
            if promotion_claimed:
                issues.append(ValidationIssue(f"domain_facets/{index}", "required facet lacks a retained item passing CVI and flag rules"))

    count_paths = {
        "construct_overlap": "unresolved_construct_overlap_count",
        "reading_level": "unresolved_reading_level_count",
        "harm_ethics": "unresolved_harm_ethics_count",
    }
    for key, field in count_paths.items():
        if scale.get(field) != unresolved_counts[key]:
            issues.append(ValidationIssue(f"scale_level_cvi/{field}", f"must equal recomputed unresolved count {unresolved_counts[key]}"))

    all_item_cvi_met = bool(retained_ids) and len(computed_overall) == len(retained_ids) and all(value >= ITEM_CVI_THRESHOLD for value in computed_overall.values())
    scale_cvi_met = scale_expected is not None and scale_expected >= SCALE_CVI_THRESHOLD
    construct_overlap_resolved = unresolved_counts["construct_overlap"] == 0
    reading_level_resolved = unresolved_counts["reading_level"] == 0
    harm_ethics_resolved = unresolved_counts["harm_ethics"] == 0
    computed_eligible = (
        status == "completed"
        and has_minimum_independent
        and all_item_cvi_met
        and scale_cvi_met
        and required_facets_covered
        and construct_overlap_resolved
        and reading_level_resolved
        and harm_ethics_resolved
    )

    expected_flags = {
        "minimum_independent_reviewers_met": has_minimum_independent,
        "all_item_cvi_thresholds_met": all_item_cvi_met,
        "scale_cvi_threshold_met": scale_cvi_met,
        "construct_overlap_resolved": construct_overlap_resolved,
        "reading_level_resolved": reading_level_resolved,
        "harm_ethics_resolved": harm_ethics_resolved,
        "scored_promotion_eligible": computed_eligible,
    }
    for field, expected in expected_flags.items():
        if eligibility.get(field) is not expected:
            issues.append(ValidationIssue(f"promotion_eligibility/{field}", f"must be {expected} from recomputed content-validity rules"))

    if scale.get("all_required_facets_covered") is not required_facets_covered:
        issues.append(
            ValidationIssue("scale_level_cvi/all_required_facets_covered", f"must be {required_facets_covered} from retained facet coverage")
        )

    decision = signoff.get("content_validity_decision")
    if computed_eligible and decision != PROMOTION_DECISION:
        issues.append(ValidationIssue("signoff/content_validity_decision", f"must be {PROMOTION_DECISION!r} for scored-promotion eligibility"))
    if not computed_eligible and decision == PROMOTION_DECISION:
        issues.append(ValidationIssue("signoff/content_validity_decision", "cannot approve psychometric promotion when recomputed rules fail"))
    if decision not in NONPROMOTING_DECISIONS and decision != PROMOTION_DECISION:
        issues.append(ValidationIssue("signoff/content_validity_decision", "unknown content-validity decision"))
    if computed_eligible and not signoff.get("signed_by"):
        issues.append(ValidationIssue("signoff/signed_by", "promotion approval requires at least one signer"))
    if computed_eligible and signoff.get("signed_date") is None:
        issues.append(ValidationIssue("signoff/signed_date", "promotion approval requires a signed date"))

    return issues


def validate_content_validity_dossier(dossier_path: Path, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(dossier_path)
    dossier = load_json(dossier_path)
    schema = load_json(repo_root / SCHEMA_PATH)

    issues = validate_with_jsonschema(dossier, schema)
    if isinstance(dossier, dict):
        issues.extend(validate_content_validity_rules(dossier))
    else:
        issues.append(ValidationIssue("$", "dossier must be a JSON object"))

    if issues:
        rendered = "\n".join(f"- {issue.render()}" for issue in issues)
        raise ContentValidityDossierError(f"content-validity dossier validation failed:\n{rendered}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path, help="Path to a content-validity dossier JSON file")
    args = parser.parse_args(argv)

    try:
        validate_content_validity_dossier(args.dossier)
    except ContentValidityDossierError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"OK: {args.dossier} passes the content-validity dossier gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
