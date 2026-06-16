import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_wave_packet.py"

spec = importlib.util.spec_from_file_location("validate_wave_packet", VALIDATOR_PATH)
validate_wave_packet = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["validate_wave_packet"] = validate_wave_packet
spec.loader.exec_module(validate_wave_packet)


WAVE_ID = "anx_us_2026w01"
SOMATIC_WAVE_ID = "anx_us_2026w02_somatic"
SOMATIC_RETEST_WAVE_ID = "anx_us_2026w03_somatic_retest"
EPISTEMIC_WAVE_ID = "anx_us_2026w06_epistemic"
BRIDGE_WAVE_ID = "anx_us_2026w07_cross_domain_bridge"
FULL_DOMAIN_BRIDGE_WAVE_ID = "anx_us_2026w08_full_domain_bridge"


def _copy_wave_packet_fixture(tmp_path: Path) -> Path:
    required_paths = [
        "docs/instruments/anx_us_2026w01_instrument.md",
        "docs/instruments/anx_us_2026w01_codebook.md",
        "docs/preregistrations/anx_us_2026w01_calibration.md",
        "releases/v0.1.0/manifest.json",
    ]
    manifest = json.loads((REPO_ROOT / "releases" / "v0.1.0" / "manifest.json").read_text(encoding="utf-8"))
    required_paths.extend(item["path"] for item in manifest["frozen_item_set"]["items"])
    for relative_path in required_paths:
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


def _copy_somatic_wave_packet_fixture(tmp_path: Path) -> Path:
    required_paths = [
        "docs/instruments/anx_us_2026w02_somatic_instrument.md",
        "docs/instruments/anx_us_2026w02_somatic_codebook.md",
        "docs/preregistrations/anx_us_2026w02_somatic_calibration.md",
        "events/v0.2/anx_us_2026w02_somatic_event_registry.json",
        "releases/v0.2.1/manifest.json",
    ]
    manifest = json.loads((REPO_ROOT / "releases" / "v0.2.1" / "manifest.json").read_text(encoding="utf-8"))
    required_paths.extend(item["path"] for item in manifest["frozen_item_set"]["items"])
    for relative_path in required_paths:
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


def _copy_bridge_wave_packet_fixture(tmp_path: Path) -> Path:
    required_paths = [
        "docs/instruments/anx_us_2026w07_cross_domain_bridge_instrument.md",
        "docs/instruments/anx_us_2026w07_cross_domain_bridge_codebook.md",
        "docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md",
        "events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json",
        "releases/v0.7.0/manifest.json",
    ]
    manifest = json.loads((REPO_ROOT / "releases" / "v0.7.0" / "manifest.json").read_text(encoding="utf-8"))
    required_paths.extend(item["path"] for item in manifest["frozen_item_set"]["items"])
    for relative_path in required_paths:
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


def _copy_full_domain_bridge_wave_packet_fixture(tmp_path: Path) -> Path:
    required_paths = [
        "docs/instruments/anx_us_2026w08_full_domain_bridge_instrument.md",
        "docs/instruments/anx_us_2026w08_full_domain_bridge_codebook.md",
        "docs/preregistrations/anx_us_2026w08_full_domain_bridge.md",
        "events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json",
        "releases/v0.8.0/manifest.json",
    ]
    manifest = json.loads((REPO_ROOT / "releases" / "v0.8.0" / "manifest.json").read_text(encoding="utf-8"))
    required_paths.extend(item["path"] for item in manifest["frozen_item_set"]["items"])
    for relative_path in required_paths:
        source = REPO_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


class ValidateWavePacketTests(unittest.TestCase):
    def test_current_wave1_packet_passes_consistency_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_wave_packet_fixture(Path(tmpdir))

            validate_wave_packet.validate_wave_packet(WAVE_ID, root=fixture_root)

    def test_wave_packet_gate_fails_on_item_count_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_wave_packet_fixture(Path(tmpdir))
            manifest_path = fixture_root / "releases" / "v0.1.0" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["frozen_item_set"]["item_count"] = 13
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "item_count|item count",
            ):
                validate_wave_packet.validate_wave_packet(WAVE_ID, root=fixture_root)

    def test_wave_packet_gate_fails_on_item_id_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_wave_packet_fixture(Path(tmpdir))
            codebook_path = fixture_root / "docs" / "instruments" / "anx_us_2026w01_codebook.md"
            codebook = codebook_path.read_text(encoding="utf-8")
            codebook = codebook.replace(
                "`synthetic_news_provenance` | `v0.1.0` | `epistemic_trust_anxiety`",
                "`synthetic_news_origin_drift` | `v0.1.0` | `epistemic_trust_anxiety`",
            )
            codebook_path.write_text(codebook, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "item ID set differs",
            ):
                validate_wave_packet.validate_wave_packet(WAVE_ID, root=fixture_root)

    def test_v021_somatic_packet_passes_consistency_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_somatic_wave_packet_fixture(Path(tmpdir))

            validate_wave_packet.validate_wave_packet(
                SOMATIC_WAVE_ID,
                root=fixture_root,
                release="v0.2.1",
            )

    def test_v022_anchored_somatic_packet_passes_command(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "tools/validate_wave_packet.py",
                SOMATIC_WAVE_ID,
                "--release",
                "v0.2.2",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("wave packet validation passed", result.stdout)

    def test_v031_somatic_retest_packet_passes_command(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "tools/validate_wave_packet.py",
                SOMATIC_RETEST_WAVE_ID,
                "--release",
                "v0.3.1",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("wave packet validation passed", result.stdout)

    def test_v060_epistemic_packet_passes_command(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "tools/validate_wave_packet.py",
                EPISTEMIC_WAVE_ID,
                "--release",
                "v0.6.0",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("wave packet validation passed", result.stdout)

    def test_v070_cross_domain_bridge_packet_passes_command(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "tools/validate_wave_packet.py",
                BRIDGE_WAVE_ID,
                "--release",
                "v0.7.0",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("wave packet validation passed", result.stdout)

    def test_v080_full_domain_bridge_packet_passes_command(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "tools/validate_wave_packet.py",
                FULL_DOMAIN_BRIDGE_WAVE_ID,
                "--release",
                "v0.8.0",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("wave packet validation passed", result.stdout)

    def test_v070_cross_domain_bridge_fails_on_item_id_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_bridge_wave_packet_fixture(Path(tmpdir))
            codebook_path = (
                fixture_root
                / "docs"
                / "instruments"
                / "anx_us_2026w07_cross_domain_bridge_codebook.md"
            )
            codebook = codebook_path.read_text(encoding="utf-8").replace(
                "`synthetic_news_provenance` | `v0.1.0` | `items/v0.1/epistemic/synthetic_news_provenance.json`",
                "`synthetic_news_origin_drift` | `v0.1.0` | `items/v0.1/epistemic/synthetic_news_provenance.json`",
            )
            codebook_path.write_text(codebook, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "item ID set differs",
            ):
                validate_wave_packet.validate_wave_packet(
                    BRIDGE_WAVE_ID,
                    root=fixture_root,
                    release="v0.7.0",
                )

    def test_v070_cross_domain_bridge_fails_on_item_version_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_bridge_wave_packet_fixture(Path(tmpdir))
            codebook_path = (
                fixture_root
                / "docs"
                / "instruments"
                / "anx_us_2026w07_cross_domain_bridge_codebook.md"
            )
            codebook = codebook_path.read_text(encoding="utf-8").replace(
                "`sleep_disruption_ai_news` | `v0.2.0`",
                "`sleep_disruption_ai_news` | `v0.2.1`",
            )
            codebook_path.write_text(codebook, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "metadata differs|version",
            ):
                validate_wave_packet.validate_wave_packet(
                    BRIDGE_WAVE_ID,
                    root=fixture_root,
                    release="v0.7.0",
                )

    def test_v070_cross_domain_bridge_fails_on_block_order_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_bridge_wave_packet_fixture(Path(tmpdir))
            instrument_path = (
                fixture_root
                / "docs"
                / "instruments"
                / "anx_us_2026w07_cross_domain_bridge_instrument.md"
            )
            instrument = instrument_path.read_text(encoding="utf-8").replace(
                "| `order_6` | `epistemic` | `economic_vocational` | `somatic_ambient` |",
                "| `order_6` | `epistemic` | `somatic_ambient` | `economic_vocational` |",
                1,
            )
            instrument_path.write_text(instrument, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "domain-block order",
            ):
                validate_wave_packet.validate_wave_packet(
                    BRIDGE_WAVE_ID,
                    root=fixture_root,
                    release="v0.7.0",
                )

    def test_v080_full_domain_bridge_fails_on_item_id_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_full_domain_bridge_wave_packet_fixture(Path(tmpdir))
            codebook_path = (
                fixture_root
                / "docs"
                / "instruments"
                / "anx_us_2026w08_full_domain_bridge_codebook.md"
            )
            codebook = codebook_path.read_text(encoding="utf-8").replace(
                "| epistemic | synthetic_news_provenance | v0.1.0 |",
                "| epistemic | synthetic_news_origin_drift | v0.1.0 |",
                1,
            )
            codebook_path.write_text(codebook, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "item ID set differs",
            ):
                validate_wave_packet.validate_wave_packet(
                    FULL_DOMAIN_BRIDGE_WAVE_ID,
                    root=fixture_root,
                    release="v0.8.0",
                )

    def test_v080_full_domain_bridge_fails_on_item_version_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_full_domain_bridge_wave_packet_fixture(Path(tmpdir))
            codebook_path = (
                fixture_root
                / "docs"
                / "instruments"
                / "anx_us_2026w08_full_domain_bridge_codebook.md"
            )
            codebook = codebook_path.read_text(encoding="utf-8").replace(
                "| relational | partner_ai_confidant_displacement | v0.8.0 |",
                "| relational | partner_ai_confidant_displacement | v0.8.1 |",
                1,
            )
            codebook_path.write_text(codebook, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "metadata differs|version",
            ):
                validate_wave_packet.validate_wave_packet(
                    FULL_DOMAIN_BRIDGE_WAVE_ID,
                    root=fixture_root,
                    release="v0.8.0",
                )

    def test_v080_full_domain_bridge_fails_without_no_event_registry_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_full_domain_bridge_wave_packet_fixture(Path(tmpdir))
            preregistration_path = (
                fixture_root
                / "docs"
                / "preregistrations"
                / "anx_us_2026w08_full_domain_bridge.md"
            )
            preregistration = preregistration_path.read_text(encoding="utf-8").replace(
                "events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json",
                "events/v0.8/removed_registry_reference.json",
                1,
            )
            preregistration_path.write_text(preregistration, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "missing frozen event registry reference",
            ):
                validate_wave_packet.validate_wave_packet(
                    FULL_DOMAIN_BRIDGE_WAVE_ID,
                    root=fixture_root,
                    release="v0.8.0",
                )

    def test_v080_full_domain_bridge_fails_on_fixed_domain_block_order_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_full_domain_bridge_wave_packet_fixture(Path(tmpdir))
            instrument_path = (
                fixture_root
                / "docs"
                / "instruments"
                / "anx_us_2026w08_full_domain_bridge_instrument.md"
            )
            instrument = instrument_path.read_text(encoding="utf-8").replace(
                "| 4 | relational | partner_ai_confidant_displacement, friend_group_ai_mediation, eldercare_ai_attachment_shift |",
                "| 4 | existential_identity | partner_ai_confidant_displacement, friend_group_ai_mediation, eldercare_ai_attachment_shift |",
                1,
            )
            instrument_path.write_text(instrument, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "domain-block order",
            ):
                validate_wave_packet.validate_wave_packet(
                    FULL_DOMAIN_BRIDGE_WAVE_ID,
                    root=fixture_root,
                    release="v0.8.0",
                )

    def test_v021_somatic_packet_fails_on_release_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_somatic_wave_packet_fixture(Path(tmpdir))
            manifest_path = fixture_root / "releases" / "v0.2.1" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["benchmark_version"] = "v0.2.0"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "benchmark_version|Benchmark release",
            ):
                validate_wave_packet.validate_wave_packet(
                    SOMATIC_WAVE_ID,
                    root=fixture_root,
                    release="v0.2.1",
                )

    def test_v021_somatic_packet_fails_on_item_metadata_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_somatic_wave_packet_fixture(Path(tmpdir))
            manifest_path = fixture_root / "releases" / "v0.2.1" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["frozen_item_set"]["items"][0]["construct"] = "somatic_ambient_drift"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "metadata differs",
            ):
                validate_wave_packet.validate_wave_packet(
                    SOMATIC_WAVE_ID,
                    root=fixture_root,
                    release="v0.2.1",
                )

    def test_v021_somatic_packet_fails_without_event_registry_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = _copy_somatic_wave_packet_fixture(Path(tmpdir))
            preregistration_path = (
                fixture_root
                / "docs"
                / "preregistrations"
                / "anx_us_2026w02_somatic_calibration.md"
            )
            preregistration = preregistration_path.read_text(encoding="utf-8").replace(
                "events/v0.2/anx_us_2026w02_somatic_event_registry.json",
                "events/v0.2/removed_registry_reference.json",
            )
            preregistration_path.write_text(preregistration, encoding="utf-8")

            with self.assertRaisesRegex(
                validate_wave_packet.WavePacketValidationError,
                "missing frozen event registry reference",
            ):
                validate_wave_packet.validate_wave_packet(
                    SOMATIC_WAVE_ID,
                    root=fixture_root,
                    release="v0.2.1",
                )


if __name__ == "__main__":
    unittest.main()
