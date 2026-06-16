import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import validate_event_registry  # noqa: E402


NO_EVENT_REGISTRIES = [
    "events/v0.2/anx_us_2026w02_somatic_event_registry.json",
    "events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json",
    "events/v0.5/anx_us_2026w05_economic_event_registry.json",
    "events/v0.6/anx_us_2026w06_epistemic_event_registry.json",
    "events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json",
]


def _write_registry(tmp_path: Path, registry: dict) -> Path:
    registry_path = tmp_path / "events" / "fixture_event_registry.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    return registry_path


def _valid_frozen_event_registry() -> dict:
    return {
        "$schema": "../schema/event_registry.schema.json",
        "registry_schema_version": "v0.1.0",
        "registry_version": "v0.4.0",
        "benchmark_release_line": "v0.4",
        "effective_benchmark_version": "v0.4.0",
        "wave_id": "anx_us_2026w04_somatic",
        "registry_status": "frozen",
        "registry_lock_date": "2026-06-20",
        "outcome_inspection_status": "not_inspected",
        "events": [
            {
                "event_id": "frontier_model_release_2026_06_20",
                "event_name": "Externally timestamped frontier model release",
                "category": "frontier_model_release",
                "event_description": "A qualifying externally timestamped AI capability release used here as a synthetic registry fixture for validator tests, with all event windows specified before outcome inspection.",
                "event_timestamp": "2026-06-20T15:00:00Z",
                "timestamp_source_url": "https://example.org/archive/frontier-model-release-2026-06-20",
                "timestamp_source_type": "official_release_note",
                "baseline_window": {
                    "window_id": "primary_baseline",
                    "start": "2026-06-06T15:00:00Z",
                    "end": "2026-06-19T15:00:00Z",
                    "inclusion_rule": "Include responses with timestamps at or after start and before end.",
                },
                "exposure_window": {
                    "window_id": "primary_exposure",
                    "start": "2026-06-20T15:00:00Z",
                    "end": "2026-06-21T15:00:00Z",
                    "inclusion_rule": "Include responses with timestamps at or after start and before end.",
                },
                "follow_up_windows": [
                    {
                        "window_id": "primary_follow_up",
                        "start": "2026-06-21T15:00:00Z",
                        "end": "2026-06-27T15:00:00Z",
                        "inclusion_rule": "Include responses with timestamps at or after start and before end.",
                    }
                ],
                "affected_domains": [
                    "somatic_ambient"
                ],
                "event_adjudication": {
                    "qualifies": True,
                    "severity_tier": "tier_2_moderate",
                    "capability_domain": "frontier_model_capability",
                    "public_reach_tier": "reach_3_general_public",
                    "novelty_tier": "novelty_2_distinct",
                    "affected_domain_rationale": "Coders prospectively mapped this synthetic frontier release to somatic_ambient because the source packet describes broad public AI capability news likely to affect background vigilance, sleep disruption, and bodily arousal before any ANX-Bench outcomes are inspected.",
                    "coder_ids": [
                        "coder_alpha",
                        "coder_beta"
                    ],
                    "coder_disagreements": "No material coder disagreements occurred for qualification, severity, public reach, novelty, or affected-domain mapping.",
                    "reconciliation_decision": "Both coders independently classified the synthetic event as confirmatory eligible at tier_2_moderate, so no third adjudicator was required.",
                    "source_count": 2,
                },
                "competing_events": [],
                "lock_date": "2026-06-20",
                "amendment_history": [],
            }
        ],
    }


class ValidateEventRegistryTests(unittest.TestCase):
    def test_current_no_event_registries_pass_confirmatory_gate(self) -> None:
        for relative_path in NO_EVENT_REGISTRIES:
            with self.subTest(relative_path=relative_path):
                validate_event_registry.validate_event_registry(
                    REPO_ROOT / relative_path,
                    intended_use="confirmatory",
                )

    def test_wave4_template_passes_registry_validation(self) -> None:
        validate_event_registry.validate_event_registry(
            REPO_ROOT / "events/v0.4/anx_us_2026w04_somatic_event_registry.template.json"
        )

    def test_accepts_no_event_template_with_empty_adjudication_placeholder(self) -> None:
        validate_event_registry.validate_event_registry(
            REPO_ROOT / "events/v0.4/anx_us_2026w04_somatic_event_registry.template.json"
        )

    def test_rejects_non_no_event_registry_lacking_adjudication_metadata(self) -> None:
        try:
            import jsonschema  # noqa: F401
        except ModuleNotFoundError:
            self.skipTest("jsonschema is required to exercise conditional event_adjudication schema rules")

        registry = _valid_frozen_event_registry()
        del registry["events"][0]["event_adjudication"]
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_registry(Path(tmpdir), registry)

            with self.assertRaisesRegex(
                validate_event_registry.EventRegistryValidationError,
                "event_adjudication",
            ):
                validate_event_registry.validate_event_registry(registry_path)

    def test_wave4_template_cannot_support_confirmatory_claims(self) -> None:
        with self.assertRaisesRegex(
            validate_event_registry.EventRegistryValidationError,
            "template registries cannot support confirmatory",
        ):
            validate_event_registry.validate_event_registry(
                REPO_ROOT / "events/v0.4/anx_us_2026w04_somatic_event_registry.template.json",
                intended_use="confirmatory",
            )

    def test_rejects_invalid_registry_status(self) -> None:
        registry = _valid_frozen_event_registry()
        registry["registry_status"] = "template_pending_event"
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_registry(Path(tmpdir), registry)

            with self.assertRaisesRegex(
                validate_event_registry.EventRegistryValidationError,
                "registry_status",
            ):
                validate_event_registry.validate_event_registry(registry_path)

    def test_rejects_missing_event_windows(self) -> None:
        registry = _valid_frozen_event_registry()
        event = registry["events"][0]
        event["baseline_window"] = None
        event["exposure_window"] = None
        event["follow_up_windows"] = []
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_registry(Path(tmpdir), registry)

            with self.assertRaisesRegex(
                validate_event_registry.EventRegistryValidationError,
                "baseline_window",
            ):
                validate_event_registry.validate_event_registry(registry_path, intended_use="confirmatory")

    def test_rejects_outcome_inspection_before_lock_for_frozen_registry(self) -> None:
        registry = copy.deepcopy(_valid_frozen_event_registry())
        registry["outcome_inspection_status"] = "exploratory_only"
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_path = _write_registry(Path(tmpdir), registry)

            with self.assertRaisesRegex(
                validate_event_registry.EventRegistryValidationError,
                "frozen registries require outcome_inspection_status",
            ):
                validate_event_registry.validate_event_registry(registry_path, intended_use="confirmatory")


if __name__ == "__main__":
    unittest.main()
