#!/usr/bin/env python3
"""Validate ANX-Bench Wave 7 cross-domain bridge evidence.

The Wave 7 bridge can support only a later aggregate-score proposal. This
validator enforces the preregistered pass and block rules and rejects any
evidence artifact that directly authorizes an overall ANX, cross-domain, or
domain-combined score.
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


SCHEMA_PATH = Path("schema/cross_domain_bridge_evidence.schema.json")
EXPECTED_ITEMS = {
    "sleep_disruption_ai_news",
    "body_vigilance_model_release",
    "background_dread_ai_progress",
    "avoidance_after_ai_capability_demo",
    "skill_obsolescence_software",
    "wage_pressure_customer_support",
    "retraining_pressure_accounting",
    "status_loss_creative_work",
    "deepfake_evidence_trust",
    "synthetic_news_provenance",
    "ai_expert_claim_conflict",
    "personalized_misinformation_targeting",
}
EXPECTED_VERSIONS = {
    "sleep_disruption_ai_news": "v0.2.0",
    "body_vigilance_model_release": "v0.2.0",
    "background_dread_ai_progress": "v0.2.0",
    "avoidance_after_ai_capability_demo": "v0.2.0",
    "skill_obsolescence_software": "v0.1.0",
    "wage_pressure_customer_support": "v0.1.0",
    "retraining_pressure_accounting": "v0.1.0",
    "status_loss_creative_work": "v0.1.0",
    "deepfake_evidence_trust": "v0.1.0",
    "synthetic_news_provenance": "v0.1.0",
    "ai_expert_claim_conflict": "v0.1.0",
    "personalized_misinformation_targeting": "v0.1.0",
}
BLOCKED_TERMS = (
    "authorizes scoring",
    "scoring authorized",
    "official overall anx score",
    "official cross-domain score",
    "official cross domain score",
    "official domain-combined score",
    "official domain combined score",
)


class CrossDomainBridgeEvidenceError(Exception):
    """Raised when the Wave 7 bridge evidence artifact fails validation."""


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
        raise CrossDomainBridgeEvidenceError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CrossDomainBridgeEvidenceError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def find_repo_root(evidence_path: Path) -> Path:
    search_start = evidence_path.resolve().parent
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
    """Validate the JSON Schema subset used by the bridge evidence schema."""

    issues: list[ValidationIssue] = []

    def resolve_ref(ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise CrossDomainBridgeEvidenceError(f"unsupported external JSON Schema reference: {ref}")
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
        raise CrossDomainBridgeEvidenceError(f"unsupported JSON Schema type: {expected}")

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


def _num(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def _present(*values: Any) -> bool:
    return all(value is not None for value in values)


def _check_label(path: str, observed: Any, expected: str | None, issues: list[ValidationIssue]) -> None:
    if expected is None:
        if observed is not None:
            issues.append(ValidationIssue(path, "decision must be null until all required observed results are present"))
    elif observed != expected:
        issues.append(ValidationIssue(path, f"decision must be {expected!r} from preregistered thresholds"))


def expected_analytic_n(evidence: dict[str, Any]) -> str | None:
    analytic = evidence.get("analytic_n", {})
    n = _int(analytic.get("final_analytic_n"))
    independent = analytic.get("independent_from_wave5_wave6")
    minimum = evidence.get("thresholds", {}).get("minimum_analytic_n")
    if not _present(n, independent, minimum):
        return None
    return "pass" if n >= minimum and independent is True else "block"


def expected_exclusion_flow(evidence: dict[str, Any]) -> str | None:
    flow = evidence.get("exclusion_flow", {})
    total = _int(flow.get("total_excluded_n"))
    retained = flow.get("non_exclusion_sensitivity_flags_retained")
    subgroup = flow.get("reported_by_required_subgroups")
    if not _present(total, retained, subgroup):
        return None
    return "pass" if retained is True and subgroup is True else "block"


def expected_factor_model(evidence: dict[str, Any]) -> str | None:
    fit = evidence.get("factor_model_fit", {})
    thresholds = evidence.get("thresholds", {}).get("factor_model", {})
    primary = _num(fit.get("efa_primary_loading_min"))
    secondary = _num(fit.get("efa_secondary_loading_abs_max"))
    factor_count = _int(fit.get("efa_parallel_analysis_factor_count"))
    interpretable = fit.get("three_factor_interpretable")
    cfi = _num(fit.get("correlated_three_factor_cfi"))
    rmsea = _num(fit.get("correlated_three_factor_rmsea"))
    loading = _num(fit.get("standardized_loading_min"))
    not_unidim = fit.get("unidimensional_model_not_sufficient")
    if not _present(primary, secondary, factor_count, interpretable, cfi, rmsea, loading, not_unidim):
        return None
    passes = (
        primary >= thresholds["minimum_primary_loading"]
        and secondary <= thresholds["maximum_secondary_loading"]
        and factor_count in (2, 3)
        and interpretable is True
        and cfi >= thresholds["minimum_correlated_three_factor_cfi"]
        and rmsea <= thresholds["maximum_correlated_three_factor_rmsea"]
        and loading >= thresholds["minimum_standardized_loading"]
        and not_unidim is True
    )
    return "pass" if passes else "block"


def expected_omega(evidence: dict[str, Any]) -> str | None:
    omega = evidence.get("omega", {})
    threshold = evidence.get("thresholds", {}).get("omega", {}).get("minimum_domain_omega")
    values = [
        _num(omega.get("somatic_ambient_anxiety")),
        _num(omega.get("economic_vocational_anxiety")),
        _num(omega.get("epistemic_trust_anxiety")),
    ]
    minimum = _num(omega.get("minimum_domain_omega"))
    all_70 = omega.get("all_domains_at_or_above_0_70")
    all_80 = omega.get("all_domains_at_or_above_0_80")
    if not _present(*values, minimum, all_70, all_80, threshold):
        return None
    expected_minimum = min(values)
    if abs(minimum - expected_minimum) > 1e-9:
        return "block"
    if all_70 != all(value >= 0.70 for value in values):
        return "block"
    if all_80 != all(value >= 0.80 for value in values):
        return "block"
    return "pass" if minimum >= threshold else "block"


def expected_irt(evidence: dict[str, Any]) -> str | None:
    irt = evidence.get("irt_linking", {})
    thresholds = evidence.get("thresholds", {}).get("irt_linking", {})
    converged = irt.get("model_converged")
    discrimination = _num(irt.get("discrimination_min"))
    violations = _int(irt.get("threshold_ordering_violations"))
    local = _num(irt.get("local_dependence_abs_max"))
    drift = _num(irt.get("anchor_drift_abs_mean_sd"))
    se = _num(irt.get("linking_se_central_80_max"))
    theta_scoring = irt.get("official_theta_scoring_introduced")
    if not _present(converged, discrimination, violations, local, drift, se, theta_scoring):
        return None
    passes = (
        converged is True
        and discrimination >= thresholds["minimum_discrimination"]
        and violations == thresholds["maximum_threshold_ordering_violations"]
        and local < thresholds["maximum_local_dependence_abs"]
        and drift <= thresholds["maximum_anchor_drift_abs_mean_sd"]
        and se <= thresholds["maximum_linking_se_central_80"]
        and theta_scoring is False
    )
    return "pass" if passes else "block"


def expected_dif(evidence: dict[str, Any]) -> str | None:
    dif = evidence.get("dif", {})
    material_count = _int(dif.get("material_unresolved_dif_item_count"))
    rank = dif.get("rank_order_impact_detected")
    q = _num(dif.get("max_fdr_q_for_flagged_items"))
    r2 = _num(dif.get("max_pseudo_r2_delta"))
    expected_score = _num(dif.get("max_expected_score_difference_sd"))
    if not _present(material_count, rank, q, r2, expected_score):
        return None
    return "pass" if material_count == 0 and rank is False else "block"


def expected_invariance(evidence: dict[str, Any]) -> str | None:
    inv = evidence.get("invariance", {})
    thresholds = evidence.get("thresholds", {}).get("invariance", {})
    configural = inv.get("configural_all_converged")
    metric_cfi = _num(inv.get("minimum_metric_delta_cfi"))
    metric_rmsea = _num(inv.get("maximum_metric_delta_rmsea"))
    scalar_cfi = _num(inv.get("minimum_scalar_delta_cfi"))
    scalar_rmsea = _num(inv.get("maximum_scalar_delta_rmsea"))
    failed = _int(inv.get("failed_key_comparison_count"))
    fallback = inv.get("irt_fallback_used")
    approved = inv.get("irt_fallback_reviewer_approved")
    if not _present(configural, metric_cfi, metric_rmsea, scalar_cfi, scalar_rmsea, failed, fallback, approved):
        return None
    primary_pass = (
        configural is True
        and metric_cfi >= thresholds["minimum_metric_delta_cfi"]
        and metric_rmsea <= thresholds["maximum_metric_delta_rmsea"]
        and scalar_cfi >= thresholds["minimum_scalar_delta_cfi"]
        and scalar_rmsea <= thresholds["maximum_scalar_delta_rmsea"]
        and failed == 0
    )
    fallback_pass = fallback is True and approved is True and failed == 0
    return "pass" if primary_pass or fallback_pass else "block"


def expected_latent_correlations(evidence: dict[str, Any]) -> str | None:
    corr = evidence.get("latent_correlations", {})
    lower = evidence.get("thresholds", {}).get("latent_correlations", {}).get("minimum_abs_pairwise")
    upper = evidence.get("thresholds", {}).get("latent_correlations", {}).get("maximum_abs_pairwise")
    values = [
        _num(corr.get("somatic_economic")),
        _num(corr.get("somatic_epistemic")),
        _num(corr.get("economic_epistemic")),
    ]
    minimum = _num(corr.get("minimum_abs_pairwise"))
    maximum = _num(corr.get("maximum_abs_pairwise"))
    ci = corr.get("confidence_intervals_reported")
    stable = corr.get("weight_and_exclusion_sensitivity_stable")
    if not _present(*values, minimum, maximum, ci, stable, lower, upper):
        return None
    abs_values = [abs(value) for value in values]
    if abs(minimum - min(abs_values)) > 1e-9 or abs(maximum - max(abs_values)) > 1e-9:
        return "block"
    passes = minimum >= lower and maximum <= upper and ci is True and stable is True
    return "pass" if passes else "block"


def expected_general_readiness(evidence: dict[str, Any]) -> str | None:
    readiness = evidence.get("bifactor_second_order_readiness", {})
    thresholds = evidence.get("thresholds", {}).get("general_factor", {})
    converged = readiness.get("model_converged")
    omega_h = _num(readiness.get("omega_hierarchical"))
    ecv = _num(readiness.get("explained_common_variance"))
    specific = readiness.get("domain_specific_factors_retain_interpretable_variance")
    if not _present(converged, omega_h, ecv, specific):
        return None
    if (
        converged is True
        and omega_h >= thresholds["minimum_omega_hierarchical"]
        and ecv >= thresholds["minimum_explained_common_variance"]
        and specific is True
    ):
        return "overall_readiness_review_supported"
    if specific is True:
        return "domain_only"
    return "blocked"


def expected_final_decision(evidence: dict[str, Any], gate_decisions: list[str | None], general: str | None) -> str | None:
    if any(decision is None for decision in gate_decisions) or general is None:
        return None
    if any(decision == "block" for decision in gate_decisions) or general == "blocked":
        return "blocked"
    if general == "domain_only":
        return "bridge_supported_domain_only"
    return "bridge_supported_for_overall_readiness_review"


def validate_contract(evidence: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    evidence_date = evidence.get("evidence_date")
    if isinstance(evidence_date, str):
        try:
            parsed = date.fromisoformat(evidence_date)
        except ValueError:
            issues.append(ValidationIssue("evidence_date", "must be an ISO date"))
        else:
            if parsed > date.today():
                issues.append(ValidationIssue("evidence_date", "must not be in the future"))

    if set(evidence.get("frozen_item_ids") or []) != EXPECTED_ITEMS:
        issues.append(ValidationIssue("frozen_item_ids", "must exactly match the 12 frozen Wave 7 bridge items"))
    if evidence.get("frozen_item_versions") != EXPECTED_VERSIONS:
        issues.append(ValidationIssue("frozen_item_versions", "must preserve somatic v0.2.0 and economic/epistemic v0.1.0 item versions"))
    if evidence.get("event_id") != "no_event":
        issues.append(ValidationIssue("event_id", "must remain no_event; Wave 7 is not an event study"))

    scoring = evidence.get("scoring_authorization", {})
    if isinstance(scoring, dict):
        if scoring.get("official_scored_items") != []:
            issues.append(ValidationIssue("scoring_authorization/official_scored_items", "must be empty for bridge evidence"))
        for field in (
            "aggregate_scoring_permitted",
            "cross_domain_score_authorized",
            "overall_anx_score_authorized",
            "domain_combined_score_authorized",
            "event_study_claim_permitted",
            "trend_claim_permitted",
            "individual_level_use_permitted",
            "policy_decision_ranking_permitted",
        ):
            if scoring.get(field) is not False:
                issues.append(ValidationIssue(f"scoring_authorization/{field}", "must be false for bridge evidence"))

    rationale = evidence.get("final_decision", {}).get("decision_rationale", "")
    if isinstance(rationale, str):
        lowered = rationale.lower()
        for term in BLOCKED_TERMS:
            if term in lowered:
                issues.append(ValidationIssue("final_decision/decision_rationale", "must not claim scoring authorization"))
                break

    return issues


def validate_decisions(evidence: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    analytic = expected_analytic_n(evidence)
    exclusion = expected_exclusion_flow(evidence)
    factor = expected_factor_model(evidence)
    omega = expected_omega(evidence)
    irt = expected_irt(evidence)
    dif = expected_dif(evidence)
    invariance = expected_invariance(evidence)
    correlations = expected_latent_correlations(evidence)
    general = expected_general_readiness(evidence)

    _check_label("analytic_n/decision", evidence.get("analytic_n", {}).get("decision"), analytic, issues)
    _check_label("exclusion_flow/decision", evidence.get("exclusion_flow", {}).get("decision"), exclusion, issues)
    _check_label("factor_model_fit/decision", evidence.get("factor_model_fit", {}).get("decision"), factor, issues)
    _check_label("omega/decision", evidence.get("omega", {}).get("decision"), omega, issues)
    _check_label("irt_linking/decision", evidence.get("irt_linking", {}).get("decision"), irt, issues)
    _check_label("dif/decision", evidence.get("dif", {}).get("decision"), dif, issues)
    _check_label("invariance/decision", evidence.get("invariance", {}).get("decision"), invariance, issues)
    _check_label("latent_correlations/decision", evidence.get("latent_correlations", {}).get("decision"), correlations, issues)

    readiness = evidence.get("bifactor_second_order_readiness", {})
    if general is None:
        if readiness.get("overall_readiness_decision") is not None:
            issues.append(
                ValidationIssue(
                    "bifactor_second_order_readiness/overall_readiness_decision",
                    "decision must be null until all required observed results are present",
                )
            )
    elif readiness.get("overall_readiness_decision") != general:
        issues.append(
            ValidationIssue(
                "bifactor_second_order_readiness/overall_readiness_decision",
                f"decision must be {general!r} from preregistered thresholds",
            )
        )

    gate_decisions = [analytic, exclusion, factor, omega, irt, dif, invariance, correlations]
    final = expected_final_decision(evidence, gate_decisions, general)
    decision = evidence.get("final_decision", {})
    if isinstance(decision, dict):
        if final is None:
            if decision.get("bridge_decision") is not None:
                issues.append(ValidationIssue("final_decision/bridge_decision", "must be null until all gate decisions are available"))
            if decision.get("release_blocking") is not None:
                issues.append(ValidationIssue("final_decision/release_blocking", "must be null until all gate decisions are available"))
            if decision.get("later_proposal_permitted") is not None:
                issues.append(ValidationIssue("final_decision/later_proposal_permitted", "must be null until all gate decisions are available"))
            if decision.get("scoring_authorized") is not None:
                issues.append(ValidationIssue("final_decision/scoring_authorized", "must be null until all gate decisions are available"))
        else:
            if decision.get("bridge_decision") != final:
                issues.append(ValidationIssue("final_decision/bridge_decision", f"must be {final!r} from gate decisions"))
            expected_release_blocking = final == "blocked"
            if decision.get("release_blocking") is not expected_release_blocking:
                issues.append(ValidationIssue("final_decision/release_blocking", f"must be {expected_release_blocking} from gate decisions"))
            expected_later_proposal = final == "bridge_supported_for_overall_readiness_review"
            if decision.get("later_proposal_permitted") is not expected_later_proposal:
                issues.append(
                    ValidationIssue(
                        "final_decision/later_proposal_permitted",
                        f"must be {expected_later_proposal} from the bridge decision",
                    )
                )
            if decision.get("scoring_authorized") is not False:
                issues.append(ValidationIssue("final_decision/scoring_authorized", "must always be false for Wave 7 bridge evidence"))

    return issues


def validate_cross_domain_bridge_evidence(evidence_path: Path, *, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(evidence_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    evidence = load_json(evidence_path)
    if not isinstance(evidence, dict):
        raise CrossDomainBridgeEvidenceError("cross-domain bridge evidence root must be a JSON object")

    issues: list[ValidationIssue] = []
    issues.extend(validate_with_jsonschema(evidence, schema))
    issues.extend(validate_contract(evidence))
    issues.extend(validate_decisions(evidence))

    if issues:
        rendered = "\n".join(f"  - {issue.render()}" for issue in issues)
        raise CrossDomainBridgeEvidenceError(f"cross-domain bridge evidence failed validation:\n{rendered}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_path", type=Path, help="Path to a Wave 7 bridge evidence JSON artifact.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest ancestor containing schema/cross_domain_bridge_evidence.schema.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_cross_domain_bridge_evidence(args.evidence_path, repo_root=args.repo_root)
    except CrossDomainBridgeEvidenceError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"cross-domain bridge evidence passed: {args.evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
