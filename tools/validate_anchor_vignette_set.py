#!/usr/bin/env python3
"""Validate ANX-Bench non-scored anchoring vignette sets."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import validate_release


ANCHOR_VIGNETTE_SCHEMA_PATH = Path("schema/anchor_vignette.schema.json")
SEVERITY_ORDER = ("low", "moderate", "high")
SEVERITY_RANK = {"low": 1, "moderate": 2, "high": 3}
FULL_DOMAIN_WAVE8_RELEASE_LINE = "v0.8"
FULL_DOMAIN_WAVE8_DOMAINS = (
    "somatic_ambient",
    "economic_vocational",
    "epistemic",
    "relational",
    "existential_identity",
    "autonomy_surveillance",
    "safety_catastrophic",
)
EXPECTED_WAVE8_ANCHORS = {
    f"anchor_{domain}_{severity}": (domain, severity)
    for domain in FULL_DOMAIN_WAVE8_DOMAINS
    for severity in SEVERITY_ORDER
}


class AnchorVignetteSetValidationError(Exception):
    """Raised when an anchor vignette set fails validation."""


def _find_repo_root(anchor_path: Path) -> Path:
    for start in (anchor_path.resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / ANCHOR_VIGNETTE_SCHEMA_PATH).is_file():
                return candidate
    return Path.cwd().resolve()


def _load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise AnchorVignetteSetValidationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AnchorVignetteSetValidationError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def _anchor_id_for(domain: str, severity: str) -> str:
    return f"anchor_{domain}_{severity}"


def _construct_matches_domain(domain: str, construct: Any) -> bool:
    return isinstance(construct, str) and construct.startswith(f"{domain}_")


def _semantic_issues(anchor_set: dict[str, Any]) -> list[validate_release.ValidationIssue]:
    issues: list[validate_release.ValidationIssue] = []
    vignettes = anchor_set.get("vignettes", [])
    if not isinstance(vignettes, list):
        return issues

    ids = [vignette.get("vignette_id") for vignette in vignettes if isinstance(vignette, dict)]
    for vignette_id, count in Counter(ids).items():
        if count > 1:
            issues.append(
                validate_release.ValidationIssue("vignettes", f"duplicate vignette_id {vignette_id!r}")
            )

    expected_order = list(anchor_set.get("expected_ordering", {}).get("severity_order", []))
    if expected_order and expected_order != list(SEVERITY_ORDER) and expected_order != ids:
        issues.append(
            validate_release.ValidationIssue(
                "expected_ordering/severity_order",
                "must equal ['low', 'moderate', 'high'] or the exact vignette_id order",
            )
        )

    seen_by_domain: dict[str, set[str]] = defaultdict(set)
    for index, vignette in enumerate(vignettes):
        if not isinstance(vignette, dict):
            continue
        prefix = f"vignettes/{index}"
        domain = vignette.get("target_domain")
        construct = vignette.get("target_construct")
        severity = vignette.get("intended_severity_band")
        vignette_id = vignette.get("vignette_id")

        if isinstance(domain, str) and not _construct_matches_domain(domain, construct):
            issues.append(
                validate_release.ValidationIssue(
                    f"{prefix}/target_construct", "must use the target_domain as its construct prefix"
                )
            )
        if isinstance(domain, str) and isinstance(severity, str):
            expected_id = _anchor_id_for(domain, severity)
            if vignette_id != expected_id:
                issues.append(
                    validate_release.ValidationIssue(
                        f"{prefix}/vignette_id", f"must equal {expected_id!r} for its declared domain and severity"
                    )
                )
            seen_by_domain[domain].add(severity)
        if severity in SEVERITY_RANK and vignette.get("expected_rank") != SEVERITY_RANK[severity]:
            issues.append(
                validate_release.ValidationIssue(
                    f"{prefix}/expected_rank", f"must equal {SEVERITY_RANK[severity]} for {severity!r} severity"
                )
            )

    if anchor_set.get("benchmark_release_line") == FULL_DOMAIN_WAVE8_RELEASE_LINE:
        observed = {
            vignette.get("vignette_id"): (vignette.get("target_domain"), vignette.get("intended_severity_band"))
            for vignette in vignettes
            if isinstance(vignette, dict)
        }
        missing = sorted(set(EXPECTED_WAVE8_ANCHORS) - set(observed))
        unexpected = sorted(set(observed) - set(EXPECTED_WAVE8_ANCHORS))
        if missing:
            issues.append(
                validate_release.ValidationIssue(
                    "vignettes", "missing required Wave 8 anchors: " + ", ".join(missing)
                )
            )
        if unexpected:
            issues.append(
                validate_release.ValidationIssue(
                    "vignettes", "unexpected Wave 8 anchors: " + ", ".join(unexpected)
                )
            )
        for anchor_id, expected in EXPECTED_WAVE8_ANCHORS.items():
            if anchor_id in observed and observed[anchor_id] != expected:
                issues.append(
                    validate_release.ValidationIssue(
                        f"vignettes/{anchor_id}", "declared domain or severity does not match anchor_id"
                    )
                )
        for domain in FULL_DOMAIN_WAVE8_DOMAINS:
            observed_severities = seen_by_domain.get(domain, set())
            if observed_severities != set(SEVERITY_ORDER):
                issues.append(
                    validate_release.ValidationIssue(
                        f"vignettes/{domain}",
                        "Wave 8 requires exactly one low, moderate, and high anchor for this domain",
                    )
                )
    return issues


def validate_anchor_vignette_set(path: Path) -> None:
    repo_root = _find_repo_root(path)
    anchor_set = _load_json(path)
    schema = _load_json(repo_root / ANCHOR_VIGNETTE_SCHEMA_PATH)

    issues = validate_release.validate_with_jsonschema(
        anchor_set, schema, str(ANCHOR_VIGNETTE_SCHEMA_PATH)
    )
    if isinstance(anchor_set, dict):
        issues.extend(_semantic_issues(anchor_set))
    else:
        issues.append(validate_release.ValidationIssue("$", "anchor vignette set must be a JSON object"))

    if issues:
        rendered = "\n".join(issue.render() for issue in issues)
        raise AnchorVignetteSetValidationError(f"anchor vignette set validation failed for {path}:\n{rendered}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to an anchor vignette set JSON file")
    args = parser.parse_args(argv)

    try:
        validate_anchor_vignette_set(args.path)
    except AnchorVignetteSetValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Anchor vignette set validation passed: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
