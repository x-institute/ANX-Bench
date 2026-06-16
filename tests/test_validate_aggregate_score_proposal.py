import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = REPO_ROOT / "proposals" / "v0.8" / "overall_anx_score_proposal.template.json"
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_aggregate_score_proposal.py"
BRIDGE_TEMPLATE_PATH = (
    REPO_ROOT / "validation" / "v0.7" / "cross_domain_bridge" / "wave7_bridge_evidence.template.json"
)

spec = importlib.util.spec_from_file_location("validate_aggregate_score_proposal", VALIDATOR_PATH)
validate_aggregate_score_proposal = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_aggregate_score_proposal"] = validate_aggregate_score_proposal
spec.loader.exec_module(validate_aggregate_score_proposal)


def _template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _passing_bridge() -> dict:
    bridge = json.loads(BRIDGE_TEMPLATE_PATH.read_text(encoding="utf-8"))
    bridge["evidence_id"] = "anx_us_2026w07_cross_domain_bridge_observed_pass"
    bridge["evidence_status"] = "observed"
    bridge["analytic_n"].update(
        {
            "achieved_eligible_n": 1538,
            "final_analytic_n": 1488,
            "independent_from_wave5_wave6": True,
            "decision": "pass",
        }
    )
    bridge["exclusion_flow"].update(
        {
            "started_n": 1680,
            "consented_eligible_n": 1538,
            "excluded_under_18_n": 8,
            "excluded_non_us_n": 11,
            "excluded_non_english_or_assisted_n": 4,
            "excluded_duplicate_n": 9,
            "excluded_vendor_fraud_n": 7,
            "excluded_attention_check_n": 29,
            "excluded_cross_domain_attribution_check_n": 18,
            "excluded_scenario_comprehension_n": 15,
            "excluded_fast_completion_n": 14,
            "excluded_excessive_anx_missingness_n": 10,
            "excluded_straightline_plus_quality_failure_n": 8,
            "excluded_withdrawal_n": 3,
            "excluded_nonunderstanding_n": 6,
            "total_excluded_n": 142,
            "non_exclusion_sensitivity_flags_retained": True,
            "reported_by_required_subgroups": True,
            "decision": "pass",
        }
    )
    bridge["factor_model_fit"].update(
        {
            "efa_primary_loading_min": 0.58,
            "efa_secondary_loading_abs_max": 0.22,
            "efa_parallel_analysis_factor_count": 3,
            "three_factor_interpretable": True,
            "correlated_three_factor_cfi": 0.966,
            "correlated_three_factor_rmsea": 0.047,
            "standardized_loading_min": 0.56,
            "unidimensional_model_not_sufficient": True,
            "decision": "pass",
        }
    )
    bridge["omega"].update(
        {
            "somatic_ambient_anxiety": 0.84,
            "economic_vocational_anxiety": 0.82,
            "epistemic_trust_anxiety": 0.81,
            "minimum_domain_omega": 0.81,
            "all_domains_at_or_above_0_70": True,
            "all_domains_at_or_above_0_80": True,
            "decision": "pass",
        }
    )
    bridge["irt_linking"].update(
        {
            "model_converged": True,
            "discrimination_min": 0.78,
            "threshold_ordering_violations": 0,
            "local_dependence_abs_max": 0.14,
            "anchor_drift_abs_mean_sd": 0.11,
            "linking_se_central_80_max": 0.09,
            "official_theta_scoring_introduced": False,
            "decision": "pass",
        }
    )
    bridge["dif"].update(
        {
            "max_fdr_q_for_flagged_items": 0.064,
            "max_pseudo_r2_delta": 0.012,
            "max_expected_score_difference_sd": 0.06,
            "rank_order_impact_detected": False,
            "material_unresolved_dif_item_count": 0,
            "decision": "pass",
        }
    )
    bridge["invariance"].update(
        {
            "configural_all_converged": True,
            "minimum_metric_delta_cfi": -0.006,
            "maximum_metric_delta_rmsea": 0.009,
            "minimum_scalar_delta_cfi": -0.008,
            "maximum_scalar_delta_rmsea": 0.011,
            "failed_key_comparison_count": 0,
            "irt_fallback_used": False,
            "irt_fallback_reviewer_approved": False,
            "decision": "pass",
        }
    )
    bridge["latent_correlations"].update(
        {
            "somatic_economic": 0.48,
            "somatic_epistemic": 0.54,
            "economic_epistemic": 0.62,
            "minimum_abs_pairwise": 0.48,
            "maximum_abs_pairwise": 0.62,
            "confidence_intervals_reported": True,
            "weight_and_exclusion_sensitivity_stable": True,
            "decision": "pass",
        }
    )
    bridge["bifactor_second_order_readiness"].update(
        {
            "model_converged": True,
            "omega_hierarchical": 0.56,
            "explained_common_variance": 0.53,
            "domain_specific_factors_retain_interpretable_variance": True,
            "overall_readiness_decision": "overall_readiness_review_supported",
        }
    )
    bridge["final_decision"] = {
        "bridge_decision": "bridge_supported_for_overall_readiness_review",
        "release_blocking": False,
        "later_proposal_permitted": True,
        "scoring_authorized": False,
        "decision_rationale": "All preregistered Wave 7 bridge gates pass. This permits only a later separately preregistered aggregate-score proposal and does not calculate or authorize a score.",
    }
    return bridge


def _observed_proposal() -> dict:
    proposal = _template()
    proposal["proposal_status"] = "observed_proposal"
    proposal["source_bridge_evidence"].update(
        {
            "bridge_evidence_id": "anx_us_2026w07_cross_domain_bridge_observed_pass",
            "bridge_evidence_status": "observed",
            "bridge_decision": "bridge_supported_for_overall_readiness_review",
            "bridge_scoring_authorized": False,
        }
    )
    for construct in proposal["contributing_constructs"]:
        construct["source_release"] = "v0.8.0 scored-source approval candidate"
        construct["source_construct_approval"] = {
            "approval_status": "approved_scored",
            "approved_for_aggregate_source": True,
            "approval_artifact_path": f"validation/v0.8/{construct['construct_id']}/source_construct_approval.json",
            "approval_date": "2026-06-16",
        }
    for item in proposal["contributing_items"]:
        item["source_item_status"] = "approved_scored"
        item["scoring_key_version_locked"] = True
    proposal["scoring_model"].update(
        {
            "model_family": "Equal-domain aggregate over approved source construct scores, with domain estimates kept reportable beside the overall estimate.",
            "estimand": "Mean overall AI anxiety response across the approved somatic, economic-vocational, and epistemic source constructs in the specified US English adult online target population.",
            "score_scale": "One to five response-scale metric after source construct scoring; higher values indicate greater AI-related anxiety.",
            "aggregation_sequence": [
                "score approved items under locked source scoring keys",
                "estimate approved source construct means",
                "combine one approved construct per domain",
                "average domain estimates with preregistered equal weights"
            ],
            "source_score_inputs": [
                "somatic_ambient_anxiety",
                "economic_vocational_anxiety",
                "epistemic_trust_anxiety"
            ],
        }
    )
    proposal["scoring_model"]["release_authorization"]["release_manifest_path"] = "releases/v0.8.0/manifest.json"
    proposal["weights"] = {
        "construct_weighting": "One approved source construct contributes within each included domain; no construct enters twice.",
        "domain_weighting": "Equal domain weights across somatic_ambient, economic_vocational, and epistemic domains.",
        "population_weighting": "Use the release-approved survey weight calibrated to age group, gender, race and ethnicity, education, Census region, AI exposure, and employment margins when stable.",
        "sensitivity_weights": [
            "unweighted source construct estimates",
            "trimmed survey weights at the 1st and 99th percentiles",
            "post-stratification weights excluding AI exposure margins"
        ],
    }
    proposal["missingness_rules"] = {
        "unit_missingness_rule": "Respondents excluded by preregistered quality-control rules do not contribute scored values but remain in exclusion counts.",
        "item_missingness_rule": "Observed source item values contribute only when missingness_code is observed, exclusion_flags is empty, and the source scoring key reproduces the scored value.",
        "construct_missingness_rule": "A source construct score is computed only when the release-approved minimum retained item count is observed for that respondent or aggregate estimator.",
        "imputation_rule": "No item-level imputation is permitted for the confirmatory aggregate score; sensitivity analyses may describe but not replace the primary complete-observed rule.",
        "missingness_reporting": "Report item, construct, domain, and overall denominators, missingness codes, exclusion counts, and weighted denominator changes.",
    }
    proposal["uncertainty_reporting"] = {
        "standard_error_method": "Primary standard errors use the release-approved survey design estimator with strata, clusters, and calibrated weights when available.",
        "confidence_interval_method": "Report 95 percent confidence intervals for item, construct, domain, and overall estimates.",
        "design_effect_reporting": "Report design effects and effective sample sizes for each domain and the overall estimate.",
        "bootstrap_or_replication_plan": "Replicate-weight or bootstrap intervals are archived as sensitivity outputs when the survey vendor provides design inputs.",
        "minimum_reported_fields": [
            "point_estimate",
            "standard_error",
            "confidence_level",
            "ci_lower",
            "ci_upper",
            "ci_method",
            "contributing_n",
            "contributing_weight_sum"
        ],
    }
    proposal["invariance_dif_limits"] = {
        "required_invariance_level": "Scalar or threshold invariance is required for every subgroup, domain, and wave comparison named in the claim.",
        "failed_comparison_rule": "Any failed key comparison is removed from the permitted claim set unless a preregistered IRT linking fallback is reviewer-approved.",
        "unresolved_dif_rule": "Any unresolved statistically supported and practically meaningful DIF in a retained item blocks aggregate use of that item and affected construct.",
        "affected_claim_limitation": "Claims are limited to groups, domains, and time windows with passed invariance and no unresolved material DIF.",
        "observed_unresolved_material_dif_item_count": 0,
        "observed_failed_key_invariance_comparison_count": 0,
    }
    proposal["claim_scope"] = {
        "population_scope": "US English adult online panel respondents covered by the release sampling and weighting frame.",
        "construct_scope": "Overall AI anxiety response over the approved somatic, economic-vocational, and epistemic source constructs only.",
        "time_scope": "Single release-wave descriptive estimate unless a later longitudinal protocol is approved.",
        "permitted_claims": [
            "Report a preregistered descriptive aggregate estimate for the approved source constructs in the specified release population.",
            "Report domain estimates beside the aggregate estimate to preserve construct interpretation."
        ],
        "explicit_claim_limits": [
            "The score is not a clinical measure.",
            "The score is not valid for individual-level decisions.",
            "The score is not a national prevalence estimate beyond the stated sampling frame.",
            "The score is not an event-study or longitudinal trend outcome without later preregistration."
        ],
        "prohibited_claims_acknowledged": True,
    }
    proposal["reviewer_signoff"] = {
        "psychometric_reviewer": "Independent psychometric reviewer",
        "release_reviewer": "Independent release reviewer",
        "signed_date": "2026-06-16",
        "decision": "proposal_ready_for_release_review",
        "signoff_statement": "The observed proposal is ready for release review only; scoring remains disabled until a later manifest approval.",
    }
    return proposal


def _copy_minimal_repo(tmp_path: Path) -> Path:
    for relative_path in (
        "schema/aggregate_score_proposal.schema.json",
        "schema/cross_domain_bridge_evidence.schema.json",
        "proposals/v0.8/overall_anx_score_proposal.template.json",
        "validation/v0.7/cross_domain_bridge/wave7_bridge_evidence.template.json",
    ):
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


class AggregateScoreProposalValidatorTests(unittest.TestCase):
    def assert_validates(self, proposal_path: Path, repo_root: Path) -> None:
        validate_aggregate_score_proposal.validate_aggregate_score_proposal(proposal_path, repo_root=repo_root)

    def assert_fails(self, proposal_path: Path, repo_root: Path, expected_text: str) -> None:
        with self.assertRaises(validate_aggregate_score_proposal.AggregateScoreProposalError) as raised:
            validate_aggregate_score_proposal.validate_aggregate_score_proposal(proposal_path, repo_root=repo_root)
        self.assertIn(expected_text, str(raised.exception))

    def test_pass_template_validates_without_observed_bridge_file(self) -> None:
        self.assert_validates(TEMPLATE_PATH, REPO_ROOT)

    def test_missing_bridge_rejects_observed_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = _copy_minimal_repo(Path(tmpdir))
            proposal_path = root / "proposals" / "v0.8" / "observed.json"
            _write_json(proposal_path, _observed_proposal())

            self.assert_fails(proposal_path, root, "missing file")

    def test_premature_scoring_rejects_observed_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = _copy_minimal_repo(Path(tmpdir))
            _write_json(root / "validation" / "v0.7" / "cross_domain_bridge" / "wave7_bridge_evidence.json", _passing_bridge())
            proposal = _observed_proposal()
            proposal["scoring_authorized"] = True
            proposal["scoring_model"]["release_authorization"]["scoring_authorized"] = True
            proposal_path = root / "proposals" / "v0.8" / "observed.json"
            _write_json(proposal_path, proposal)

            self.assert_fails(proposal_path, root, "scoring_authorized")

    def test_unresolved_dif_rejects_observed_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = _copy_minimal_repo(Path(tmpdir))
            _write_json(root / "validation" / "v0.7" / "cross_domain_bridge" / "wave7_bridge_evidence.json", _passing_bridge())
            proposal = _observed_proposal()
            proposal["invariance_dif_limits"]["observed_unresolved_material_dif_item_count"] = 1
            proposal_path = root / "proposals" / "v0.8" / "observed.json"
            _write_json(proposal_path, proposal)

            self.assert_fails(proposal_path, root, "unresolved material DIF")

    def test_overbroad_claim_rejects_observed_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = _copy_minimal_repo(Path(tmpdir))
            _write_json(root / "validation" / "v0.7" / "cross_domain_bridge" / "wave7_bridge_evidence.json", _passing_bridge())
            proposal = _observed_proposal()
            proposal["claim_scope"]["permitted_claims"].append(
                "Use the official overall ANX score for national prevalence and policy-decision ranking."
            )
            proposal_path = root / "proposals" / "v0.8" / "observed.json"
            _write_json(proposal_path, proposal)

            self.assert_fails(proposal_path, root, "overbroad claim")


if __name__ == "__main__":
    unittest.main()
