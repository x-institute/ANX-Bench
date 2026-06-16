#!/usr/bin/env python3
"""Validate ANX-Bench Wave 8 full-domain bridge evidence.

The Wave 8 bridge can support only a bounded full-domain bridge-readiness
decision. This validator enforces the preregistered Wave 8 pass and block
rules and rejects any evidence artifact that authorizes scored items, domain
scores, cross-domain scores, overall ANX, trend, event-study, clinical, or
policy claims.
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


SCHEMA_PATH = Path("schema/full_domain_bridge_evidence.schema.json")
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
    "partner_ai_confidant_displacement",
    "friend_group_ai_mediation",
    "eldercare_ai_attachment_shift",
    "ai_personhood_boundary_uncertainty",
    "human_judgment_status_loss",
    "life_purpose_ai_substitution",
    "public_space_tracking",
    "workplace_behavior_scoring",
    "personalized_behavior_nudging",
    "autonomous_cyber_cascade",
    "biosecurity_protocol_misuse",
    "military_escalation_ai_advice",
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
    "partner_ai_confidant_displacement": "v0.8.0",
    "friend_group_ai_mediation": "v0.8.0",
    "eldercare_ai_attachment_shift": "v0.8.0",
    "ai_personhood_boundary_uncertainty": "v0.8.0",
    "human_judgment_status_loss": "v0.8.0",
    "life_purpose_ai_substitution": "v0.8.0",
    "public_space_tracking": "v0.8.0",
    "workplace_behavior_scoring": "v0.8.0",
    "personalized_behavior_nudging": "v0.8.0",
    "autonomous_cyber_cascade": "v0.8.0",
    "biosecurity_protocol_misuse": "v0.8.0",
    "military_escalation_ai_advice": "v0.8.0",
}
EXPECTED_DOMAINS = {
    "somatic_ambient",
    "economic_vocational",
    "epistemic",
    "relational",
    "existential_identity",
    "autonomy_surveillance",
    "safety_catastrophic",
}
AUTHORIZED_CLAIM_PATTERNS = (
    r"\bauthori[sz](?:e|es|ed|ation)\b.*\b(scored item|domain score|cross[- ]domain score|overall anx|trend|event[- ]study|clinical|diagnostic|policy)\b",
    r"\bpermit(?:s|ted)?\b.*\b(scored item|domain score|cross[- ]domain score|overall anx|trend|event[- ]study|clinical|diagnostic|policy)\b",
    r"\bofficial\b.*\b(domain score|cross[- ]domain score|overall anx|trend|event[- ]study|clinical|diagnostic|policy)\b",
)


class FullDomainBridgeEvidenceError(Exception):
    """Raised when the Wave 8 bridge evidence artifact fails validation."""


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
        raise FullDomainBridgeEvidenceError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FullDomainBridgeEvidenceError(
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
            raise FullDomainBridgeEvidenceError(f"unsupported external JSON Schema reference: {ref}")
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
        raise FullDomainBridgeEvidenceError(f"unsupported JSON Schema type: {expected}")

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
    started = _int(analytic.get("started_n"))
    eligible = _int(analytic.get("achieved_eligible_n"))
    final = _int(analytic.get("final_analytic_n"))
    minimum = _int(analytic.get("minimum_n")) or _int(evidence.get("thresholds", {}).get("minimum_analytic_n"))
    if not _present(started, eligible, final, minimum):
        return None
    return "pass" if started >= eligible >= final and final >= minimum else "block"


def expected_exclusion_flow(evidence: dict[str, Any]) -> str | None:
    flow = evidence.get("exclusion_flow", {})
    total = _int(flow.get("total_excluded_n"))
    subgroup = flow.get("reported_by_required_subgroups")
    components = [
        _int(flow.get("declined_or_withdrawn_n")),
        _int(flow.get("under_18_n")),
        _int(flow.get("non_us_n")),
        _int(flow.get("non_english_or_assisted_n")),
        _int(flow.get("duplicate_n")),
        _int(flow.get("vendor_fraud_n")),
        _int(flow.get("attention_check_failed_n")),
        _int(flow.get("scenario_comprehension_failed_n")),
        _int(flow.get("full_domain_attribution_failed_n")),
        _int(flow.get("fast_completion_n")),
        _int(flow.get("excessive_anx_missingness_n")),
        _int(flow.get("straightline_plus_quality_failure_n")),
        _int(flow.get("nonunderstanding_n")),
        _int(flow.get("platform_order_error_n")),
    ]
    if not _present(total, subgroup, *components):
        return None
    return "pass" if total == sum(components) and subgroup is True else "block"


def expected_split_sample(evidence: dict[str, Any]) -> str | None:
    split = evidence.get("split_sample", {})
    final = _int(evidence.get("analytic_n", {}).get("final_analytic_n"))
    randomized = split.get("randomized_before_outcome_inspection")
    stratified = split.get("stratified_by_sample_source_device_order")
    efa_n = _int(split.get("efa_n"))
    cfa_n = _int(split.get("cfa_n"))
    descriptive = split.get("full_sample_reported_as_descriptive_only")
    if not _present(final, randomized, stratified, efa_n, cfa_n, descriptive):
        return None
    passes = (
        randomized is True
        and stratified is True
        and descriptive is True
        and efa_n + cfa_n == final
        and abs(efa_n - cfa_n) <= 1
    )
    return "pass" if passes else "block"


def expected_domain_gate(gate: dict[str, Any], threshold: float) -> str | None:
    retained = _int(gate.get("retained_item_count"))
    minimum = _int(gate.get("minimum_required_items"))
    omega = _num(gate.get("omega"))
    discriminations = gate.get("all_item_discriminations_at_or_above_0_65")
    dif_count = _int(gate.get("unresolved_material_dif_item_count"))
    invariance = gate.get("invariance_supported_for_key_groups")
    if not _present(retained, minimum, omega, discriminations, dif_count, invariance, threshold):
        return None
    passes = retained >= minimum and omega >= threshold and discriminations is True and dif_count == 0 and invariance is True
    return "pass" if passes else "block"


def expected_efa(evidence: dict[str, Any]) -> str | None:
    efa = evidence.get("efa", {})
    thresholds = evidence.get("thresholds", {})
    factor_count = _int(efa.get("parallel_analysis_factor_count"))
    interpretable = efa.get("seven_domain_solution_interpretable")
    primary = _num(efa.get("minimum_primary_loading"))
    cross = _num(efa.get("maximum_cross_loading"))
    gap = _num(efa.get("minimum_primary_cross_loading_gap"))
    heywood = _int(efa.get("heywood_case_count"))
    unordered = _int(efa.get("unordered_threshold_item_count"))
    residual = _num(efa.get("maximum_residual_local_dependence"))
    if not _present(factor_count, interpretable, primary, cross, gap, heywood, unordered, residual):
        return None
    passes = (
        factor_count == 7
        and interpretable is True
        and primary >= thresholds["efa_min_primary_loading"]
        and cross < thresholds["efa_max_cross_loading"]
        and gap >= thresholds["efa_min_primary_cross_loading_gap"]
        and heywood == 0
        and unordered == 0
        and residual <= thresholds["max_residual_local_dependence"]
    )
    return "pass" if passes else "block"


def expected_cfa(evidence: dict[str, Any]) -> str | None:
    cfa = evidence.get("cfa", {})
    thresholds = evidence.get("thresholds", {})
    cfi = _num(cfa.get("correlated_seven_factor_cfi"))
    tli = _num(cfa.get("correlated_seven_factor_tli"))
    rmsea = _num(cfa.get("correlated_seven_factor_rmsea"))
    rmsea_upper = _num(cfa.get("rmsea_upper_90"))
    srmr = _num(cfa.get("srmr"))
    loading = _num(cfa.get("minimum_standardized_loading"))
    exception = cfa.get("single_low_loading_exception_used")
    rationale = cfa.get("single_low_loading_exception_rationale_documented")
    residual = _num(cfa.get("maximum_abs_residual_correlation"))
    better_unidim = cfa.get("better_than_unidimensional")
    better_collapsed = cfa.get("better_than_collapsed_domain_models")
    if not _present(cfi, tli, rmsea, rmsea_upper, srmr, loading, exception, rationale, residual, better_unidim, better_collapsed):
        return None
    loading_ok = loading >= thresholds["cfa_min_standardized_loading"] or (
        exception is True and rationale is True and loading >= thresholds["efa_min_primary_loading"]
    )
    passes = (
        cfi >= thresholds["cfa_min_cfi"]
        and tli >= thresholds["cfa_min_tli"]
        and rmsea <= thresholds["cfa_max_rmsea"]
        and rmsea_upper <= thresholds["cfa_max_rmsea_upper_90"]
        and srmr <= thresholds["cfa_max_srmr"]
        and loading_ok
        and residual <= thresholds["max_residual_local_dependence"]
        and better_unidim is True
        and better_collapsed is True
    )
    return "pass" if passes else "block"


def expected_omega(evidence: dict[str, Any]) -> str | None:
    omega = evidence.get("omega", {})
    threshold = evidence.get("thresholds", {}).get("omega_min_domain")
    domain_values = omega.get("domain_omega", {})
    if not isinstance(domain_values, dict) or set(domain_values) != EXPECTED_DOMAINS:
        return "block"
    values = [_num(value) for value in domain_values.values()]
    minimum = _num(omega.get("minimum_domain_omega"))
    all_70 = omega.get("all_domains_at_or_above_0_70")
    all_80 = omega.get("all_domains_at_or_above_0_80")
    if not _present(*values, minimum, all_70, all_80, threshold):
        return None
    expected_minimum = min(value for value in values if value is not None)
    if abs(minimum - expected_minimum) > 1e-9:
        return "block"
    if all_70 != all(value >= 0.70 for value in values if value is not None):
        return "block"
    if all_80 != all(value >= 0.80 for value in values if value is not None):
        return "block"
    return "pass" if minimum >= threshold else "block"


def expected_irt(evidence: dict[str, Any]) -> str | None:
    irt = evidence.get("irt", {})
    thresholds = evidence.get("thresholds", {})
    converged = irt.get("model_converged")
    discrimination = _num(irt.get("minimum_discrimination"))
    violations = _int(irt.get("monotonic_threshold_violations"))
    local = irt.get("material_local_dependence_detected")
    stable = irt.get("central_80_information_stable")
    se = _num(irt.get("maximum_linking_se"))
    theta_scoring = irt.get("official_theta_scoring_introduced")
    if not _present(converged, discrimination, violations, local, stable, se, theta_scoring):
        return None
    passes = (
        converged is True
        and discrimination >= thresholds["irt_min_discrimination"]
        and violations == 0
        and local is False
        and stable is True
        and se <= thresholds["irt_max_linking_se"]
        and theta_scoring is False
    )
    return "pass" if passes else "block"


def expected_dif(evidence: dict[str, Any]) -> str | None:
    dif = evidence.get("dif", {})
    material_count = _int(dif.get("material_unresolved_dif_item_count"))
    rank = dif.get("rank_order_impact_detected")
    threshold = dif.get("threshold_shift_material_impact_detected")
    q = _num(dif.get("max_fdr_q_for_flagged_items"))
    r2 = _num(dif.get("max_pseudo_r2_delta"))
    expected_score = _num(dif.get("max_expected_score_difference_sd"))
    if not _present(material_count, rank, threshold, q, r2, expected_score):
        return None
    return "pass" if material_count == 0 and rank is False and threshold is False else "block"


def expected_invariance(evidence: dict[str, Any]) -> str | None:
    inv = evidence.get("invariance", {})
    thresholds = evidence.get("thresholds", {})
    configural = inv.get("configural_all_converged")
    metric_cfi = _num(inv.get("minimum_metric_delta_cfi"))
    metric_rmsea = _num(inv.get("maximum_metric_delta_rmsea"))
    scalar_cfi = _num(inv.get("minimum_scalar_or_threshold_delta_cfi"))
    scalar_rmsea = _num(inv.get("maximum_scalar_or_threshold_delta_rmsea"))
    partial = inv.get("partial_invariance_used")
    documented = inv.get("partial_invariance_documented_before_interpretation")
    changed = inv.get("domain_ordering_changed_by_noninvariance")
    failed = _int(inv.get("failed_key_comparison_count"))
    if not _present(configural, metric_cfi, metric_rmsea, scalar_cfi, scalar_rmsea, partial, documented, changed, failed):
        return None
    partial_ok = partial is False or documented is True
    passes = (
        configural is True
        and metric_cfi >= thresholds["invariance_min_delta_cfi"]
        and metric_rmsea <= thresholds["invariance_max_delta_rmsea"]
        and scalar_cfi >= thresholds["invariance_min_delta_cfi"]
        and scalar_rmsea <= thresholds["invariance_max_delta_rmsea"]
        and partial_ok
        and changed is False
        and failed == 0
    )
    return "pass" if passes else "block"


def expected_latent_correlations(evidence: dict[str, Any]) -> str | None:
    corr = evidence.get("latent_correlations", {})
    thresholds = evidence.get("thresholds", {})
    values_by_pair = corr.get("pairwise_domain_correlations", {})
    if not isinstance(values_by_pair, dict) or len(values_by_pair) != 21:
        return "block"
    values = [_num(value) for value in values_by_pair.values()]
    minimum = _num(corr.get("minimum_abs_pairwise"))
    maximum = _num(corr.get("maximum_abs_pairwise"))
    ci = corr.get("confidence_intervals_reported")
    coherent = corr.get("positive_theoretically_coherent")
    stable = corr.get("weight_and_exclusion_sensitivity_stable")
    if not _present(*values, minimum, maximum, ci, coherent, stable):
        return None
    abs_values = [abs(value) for value in values if value is not None]
    if abs(minimum - min(abs_values)) > 1e-9 or abs(maximum - max(abs_values)) > 1e-9:
        return "block"
    passes = (
        minimum >= thresholds["latent_correlation_min_abs"]
        and maximum <= thresholds["latent_correlation_max_abs"]
        and ci is True
        and coherent is True
        and stable is True
    )
    return "pass" if passes else "block"


def expected_somatic_anchor_drift(evidence: dict[str, Any]) -> str | None:
    drift = evidence.get("somatic_anchor_drift", {})
    thresholds = evidence.get("thresholds", {})
    mean = _num(drift.get("mean_abs_drift_sd"))
    max_item = _num(drift.get("max_single_item_abs_drift_sd"))
    blocked = drift.get("source_anchor_use_blocked")
    if not _present(mean, max_item, blocked):
        return None
    passes = (
        mean <= thresholds["somatic_anchor_max_mean_drift_sd"]
        and max_item <= thresholds["somatic_anchor_max_single_item_drift_sd"]
        and blocked is False
    )
    return "pass" if passes else "block"


def expected_aggregate_readiness(evidence: dict[str, Any]) -> str | None:
    readiness = evidence.get("aggregate_readiness", {})
    thresholds = evidence.get("thresholds", {})
    omega_h = _num(readiness.get("omega_hierarchical"))
    ecv = _num(readiness.get("explained_common_variance"))
    specific = readiness.get("domain_specific_factors_retain_interpretable_variance")
    if not _present(omega_h, ecv, specific):
        return None
    if specific is not True:
        return "blocked"
    if omega_h >= thresholds["general_factor_min_omega_h"] and ecv >= thresholds["general_factor_min_ecv"]:
        return "later_aggregate_readiness_review_supported"
    return "domain_only"


def expected_final_decision(
    analytic: str | None,
    gate_decisions: list[str | None],
    readiness: str | None,
) -> str | None:
    if analytic is None or any(decision is None for decision in gate_decisions) or readiness is None:
        return None
    if analytic == "block":
        return "blocked_underpowered"
    if any(decision == "block" for decision in gate_decisions) or readiness == "blocked":
        return "blocked_psychometric"
    if readiness == "domain_only":
        return "bridge_supported_domain_only"
    return "bridge_supported_for_later_aggregate_readiness_review"


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
        issues.append(ValidationIssue("frozen_item_ids", "must exactly match the 24 frozen Wave 8 bridge items"))
    if evidence.get("frozen_item_versions") != EXPECTED_VERSIONS:
        issues.append(ValidationIssue("frozen_item_versions", "must preserve the frozen Wave 8 item versions"))
    if evidence.get("event_id") != "no_event":
        issues.append(ValidationIssue("event_id", "must remain no_event; Wave 8 is not an event study"))

    scoring = evidence.get("scoring_authorization", {})
    if isinstance(scoring, dict):
        if scoring.get("official_scored_items") != []:
            issues.append(ValidationIssue("scoring_authorization/official_scored_items", "must be empty for bridge evidence"))
        for field in (
            "new_domain_scores_authorized",
            "aggregate_scoring_permitted",
            "cross_domain_score_authorized",
            "overall_anx_score_authorized",
            "event_study_claim_permitted",
            "trend_claim_permitted",
            "causal_claim_permitted",
            "clinical_or_diagnostic_use_permitted",
            "individual_level_use_permitted",
            "policy_decision_ranking_permitted",
        ):
            if scoring.get(field) is not False:
                issues.append(ValidationIssue(f"scoring_authorization/{field}", "must be false for bridge evidence"))

    if evidence.get("final_decision", {}).get("scoring_authorized") not in (False, None):
        issues.append(ValidationIssue("final_decision/scoring_authorized", "must be false or null for Wave 8 bridge evidence"))

    if evidence.get("evidence_status") == "observed":
        strings: list[tuple[str, str]] = []

        def collect(value: Any, path: str) -> None:
            if isinstance(value, str):
                strings.append((path, value))
            elif isinstance(value, dict):
                for key, item in value.items():
                    collect(item, f"{path}/{key}")
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    collect(item, f"{path}/{index}")

        collect(evidence, "$")
        for path, value in strings:
            lowered = value.lower()
            if any(re.search(pattern, lowered) for pattern in AUTHORIZED_CLAIM_PATTERNS):
                issues.append(ValidationIssue(path, "observed bridge evidence must not authorize scoring or downstream claims"))

    return issues


def validate_decisions(evidence: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    analytic = expected_analytic_n(evidence)
    exclusion = expected_exclusion_flow(evidence)
    split = expected_split_sample(evidence)
    efa = expected_efa(evidence)
    cfa = expected_cfa(evidence)
    omega = expected_omega(evidence)
    irt = expected_irt(evidence)
    dif = expected_dif(evidence)
    invariance = expected_invariance(evidence)
    correlations = expected_latent_correlations(evidence)
    drift = expected_somatic_anchor_drift(evidence)
    readiness = expected_aggregate_readiness(evidence)

    _check_label("analytic_n/decision", evidence.get("analytic_n", {}).get("decision"), analytic, issues)
    _check_label("exclusion_flow/decision", evidence.get("exclusion_flow", {}).get("decision"), exclusion, issues)
    _check_label("split_sample/decision", evidence.get("split_sample", {}).get("decision"), split, issues)
    for index, gate in enumerate(evidence.get("domain_gates", []) if isinstance(evidence.get("domain_gates"), list) else []):
        if isinstance(gate, dict):
            expected = expected_domain_gate(gate, evidence.get("thresholds", {}).get("omega_min_domain"))
            _check_label(f"domain_gates/{index}/decision", gate.get("decision"), expected, issues)
    _check_label("efa/decision", evidence.get("efa", {}).get("decision"), efa, issues)
    _check_label("cfa/decision", evidence.get("cfa", {}).get("decision"), cfa, issues)
    _check_label("omega/decision", evidence.get("omega", {}).get("decision"), omega, issues)
    _check_label("irt/decision", evidence.get("irt", {}).get("decision"), irt, issues)
    _check_label("dif/decision", evidence.get("dif", {}).get("decision"), dif, issues)
    _check_label("invariance/decision", evidence.get("invariance", {}).get("decision"), invariance, issues)
    _check_label("latent_correlations/decision", evidence.get("latent_correlations", {}).get("decision"), correlations, issues)
    _check_label("somatic_anchor_drift/decision", evidence.get("somatic_anchor_drift", {}).get("decision"), drift, issues)

    if readiness is None:
        if evidence.get("aggregate_readiness", {}).get("readiness_label") is not None:
            issues.append(ValidationIssue("aggregate_readiness/readiness_label", "must be null until all required observed results are present"))
    elif evidence.get("aggregate_readiness", {}).get("readiness_label") != readiness:
        issues.append(
            ValidationIssue(
                "aggregate_readiness/readiness_label",
                f"decision must be {readiness!r} from preregistered thresholds",
            )
        )

    gate_decisions = [exclusion, split, *[
        expected_domain_gate(gate, evidence.get("thresholds", {}).get("omega_min_domain"))
        for gate in evidence.get("domain_gates", [])
        if isinstance(gate, dict)
    ], efa, cfa, omega, irt, dif, invariance, correlations, drift]
    final = expected_final_decision(analytic, gate_decisions, readiness)
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
            expected_release_blocking = final in ("blocked_underpowered", "blocked_psychometric")
            if decision.get("release_blocking") is not expected_release_blocking:
                issues.append(ValidationIssue("final_decision/release_blocking", f"must be {expected_release_blocking} from gate decisions"))
            expected_later_proposal = final == "bridge_supported_for_later_aggregate_readiness_review"
            if decision.get("later_proposal_permitted") is not expected_later_proposal:
                issues.append(
                    ValidationIssue(
                        "final_decision/later_proposal_permitted",
                        f"must be {expected_later_proposal} from the bridge decision",
                    )
                )
            if decision.get("scoring_authorized") is not False:
                issues.append(ValidationIssue("final_decision/scoring_authorized", "must always be false for Wave 8 bridge evidence"))

    return issues


def validate_full_domain_bridge_evidence(evidence_path: Path, *, repo_root: Path | None = None) -> None:
    repo_root = repo_root or find_repo_root(evidence_path)
    schema = load_json(repo_root / SCHEMA_PATH)
    evidence = load_json(evidence_path)
    if not isinstance(evidence, dict):
        raise FullDomainBridgeEvidenceError("full-domain bridge evidence root must be a JSON object")

    issues: list[ValidationIssue] = []
    issues.extend(validate_with_jsonschema(evidence, schema))
    issues.extend(validate_contract(evidence))
    issues.extend(validate_decisions(evidence))

    if issues:
        rendered = "\n".join(f"  - {issue.render()}" for issue in issues)
        raise FullDomainBridgeEvidenceError(f"full-domain bridge evidence failed validation:\n{rendered}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_path", type=Path, help="Path to a Wave 8 full-domain bridge evidence JSON artifact.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the nearest ancestor containing schema/full_domain_bridge_evidence.schema.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_full_domain_bridge_evidence(args.evidence_path, repo_root=args.repo_root)
    except FullDomainBridgeEvidenceError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"full-domain bridge evidence passed: {args.evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
