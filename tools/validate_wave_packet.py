#!/usr/bin/env python3
"""Validate a frozen ANX-Bench wave packet.

The Wave 1 gate checks that the fielding instrument, wave codebook,
preregistration, and release manifest agree on the administered ANX item
set before the packet is fielded or cited.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_WAVE_ID = "anx_us_2026w01"
DEFAULT_RELEASE = "v0.1.0"
NO_EVENT_ID = "no_event"
BENCHMARK_VERSION_RE = re.compile(r"^v(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)$")


class WavePacketValidationError(Exception):
    """Raised when a wave packet fails the consistency gate."""


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


@dataclass(frozen=True)
class ItemRecord:
    item_id: str
    item_version: str
    domain: str
    construct_id: str

    def key(self) -> tuple[str, str, str, str]:
        return (self.item_id, self.item_version, self.domain, self.construct_id)


@dataclass(frozen=True)
class PacketPaths:
    instrument: Path
    codebook: Path
    preregistration: Path
    manifest: Path
    event_registry: Path | None = None


@dataclass(frozen=True)
class PacketConfig:
    wave_id: str
    default_release: str
    item_directory: str
    instrument_path: str
    codebook_path: str
    preregistration_path: str
    event_registry_path: str | None = None


PACKET_CONFIGS = {
    "anx_us_2026w01": PacketConfig(
        wave_id="anx_us_2026w01",
        default_release="v0.1.0",
        item_directory="items/v0.1",
        instrument_path="docs/instruments/anx_us_2026w01_instrument.md",
        codebook_path="docs/instruments/anx_us_2026w01_codebook.md",
        preregistration_path="docs/preregistrations/anx_us_2026w01_calibration.md",
    ),
    "anx_us_2026w02_somatic": PacketConfig(
        wave_id="anx_us_2026w02_somatic",
        default_release="v0.2.1",
        item_directory="items/v0.2",
        instrument_path="docs/instruments/anx_us_2026w02_somatic_instrument.md",
        codebook_path="docs/instruments/anx_us_2026w02_somatic_codebook.md",
        preregistration_path="docs/preregistrations/anx_us_2026w02_somatic_calibration.md",
        event_registry_path="events/v0.2/anx_us_2026w02_somatic_event_registry.json",
    ),
    "anx_us_2026w03_somatic_retest": PacketConfig(
        wave_id="anx_us_2026w03_somatic_retest",
        default_release="v0.3.1",
        item_directory="items/v0.2",
        instrument_path="docs/instruments/anx_us_2026w03_somatic_retest_instrument.md",
        codebook_path="docs/instruments/anx_us_2026w03_somatic_retest_codebook.md",
        preregistration_path="docs/preregistrations/anx_us_2026w03_somatic_retest.md",
        event_registry_path="events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json",
    ),
    "anx_us_2026w06_epistemic": PacketConfig(
        wave_id="anx_us_2026w06_epistemic",
        default_release="v0.6.0",
        item_directory="items/v0.1/epistemic",
        instrument_path="docs/instruments/anx_us_2026w06_epistemic_instrument.md",
        codebook_path="docs/instruments/anx_us_2026w06_epistemic_codebook.md",
        preregistration_path="docs/preregistrations/anx_us_2026w06_epistemic_calibration.md",
        event_registry_path="events/v0.6/anx_us_2026w06_epistemic_event_registry.json",
    ),
    "anx_us_2026w07_cross_domain_bridge": PacketConfig(
        wave_id="anx_us_2026w07_cross_domain_bridge",
        default_release="v0.7.0",
        item_directory="items",
        instrument_path="docs/instruments/anx_us_2026w07_cross_domain_bridge_instrument.md",
        codebook_path="docs/instruments/anx_us_2026w07_cross_domain_bridge_codebook.md",
        preregistration_path="docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md",
        event_registry_path="events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json",
    ),
    "anx_us_2026w08_full_domain_bridge": PacketConfig(
        wave_id="anx_us_2026w08_full_domain_bridge",
        default_release="v0.8.0",
        item_directory="items",
        instrument_path="docs/instruments/anx_us_2026w08_full_domain_bridge_instrument.md",
        codebook_path="docs/instruments/anx_us_2026w08_full_domain_bridge_codebook.md",
        preregistration_path="docs/preregistrations/anx_us_2026w08_full_domain_bridge.md",
        event_registry_path="events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json",
    ),
}


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise WavePacketValidationError(f"missing file: {path}") from exc


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise WavePacketValidationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WavePacketValidationError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def strip_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def parse_markdown_tables(text: str) -> list[list[dict[str, str]]]:
    tables: list[list[dict[str, str]]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.startswith("|"):
            index += 1
            continue
        if index + 1 >= len(lines) or not re.fullmatch(r"\|[\s:\-|]+\|", lines[index + 1]):
            index += 1
            continue

        headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
        index += 2
        rows: list[dict[str, str]] = []
        while index < len(lines) and lines[index].startswith("|"):
            cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells, strict=True)))
            index += 1
        tables.append(rows)
    return tables


def first_present(row: dict[str, str], candidates: tuple[str, ...]) -> str:
    for candidate in candidates:
        if candidate in row:
            return row[candidate]
    return ""


def records_from_table(rows: list[dict[str, str]]) -> list[ItemRecord] | None:
    if not rows:
        return None
    columns = set(rows[0])
    required_column_groups = [
        {"Domain"},
        {"Item ID"},
        {"Version", "Item version", "Item file version"},
        {"Construct ID"},
    ]
    if not all(columns & group for group in required_column_groups):
        return None
    records = []
    for row in rows:
        records.append(
            ItemRecord(
                item_id=strip_code(row["Item ID"]),
                item_version=strip_code(first_present(row, ("Version", "Item version", "Item file version"))),
                domain=strip_code(row["Domain"]),
                construct_id=strip_code(row["Construct ID"]),
            )
        )
    return records


def parse_control_value(text: str, label: str) -> str | None:
    pattern = rf"^- {re.escape(label)}:\s+`?([^`\n]+)`?\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if match is None:
        return None
    return match.group(1).strip()


def parse_instrument(path: Path, wave_id: str) -> tuple[str | None, str | None, int | None, list[str]]:
    text = load_text(path)
    observed_wave_id = parse_control_value(text, "Wave ID")
    release = parse_control_value(text, "Benchmark release")
    count_match = re.search(r"Present all (\d+|one|two|three|four|five|six|seven|eight|nine|ten) ANX item screens exactly once", text)
    count_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    if count_match:
        raw_count = count_match.group(1)
        expected_count = int(raw_count) if raw_count.isdigit() else count_words[raw_count]
    else:
        expected_count = None
    item_ids = re.findall(r"^#### Item Screen: `([^`]+)`", text, flags=re.MULTILINE)
    return observed_wave_id, release, expected_count, item_ids


def parse_preregistration(path: Path) -> list[ItemRecord]:
    text = load_text(path)
    for table in parse_markdown_tables(text):
        records = records_from_table(table)
        if records is not None:
            return records
    raise WavePacketValidationError(f"{path}: no administered item table with Domain, Item ID, Version, and Construct ID")


def parse_codebook(path: Path) -> tuple[str | None, str | None, list[ItemRecord]]:
    text = load_text(path)
    observed_wave_id = parse_control_value(text, "Wave ID")
    release = parse_control_value(text, "Benchmark release")
    for table in parse_markdown_tables(text):
        records = records_from_table(table)
        if records is not None:
            return observed_wave_id, release, records
    raise WavePacketValidationError(f"{path}: no Wave 1 administered ANX item allowlist table")


def parse_manifest(path: Path) -> tuple[str | None, str | None, int | None, list[ItemRecord]]:
    manifest = load_json(path)
    release = manifest.get("benchmark_version")
    frozen_item_set = manifest.get("frozen_item_set", {})
    item_directory = frozen_item_set.get("item_directory")
    item_count = frozen_item_set.get("item_count")
    records = []
    for item in frozen_item_set.get("items", []):
        records.append(
            ItemRecord(
                item_id=item.get("item_id", ""),
                item_version=item.get("item_version", ""),
                domain=item.get("domain", ""),
                construct_id=item.get("construct", ""),
            )
        )
    return release, item_directory, item_count, records


def manifest_checksum_entries(path: Path) -> dict[str, str]:
    manifest = load_json(path)
    entries: dict[str, str] = {}
    for file_entry in manifest.get("checksums", {}).get("files", []):
        if isinstance(file_entry, dict) and isinstance(file_entry.get("path"), str):
            entries[file_entry["path"]] = file_entry.get("sha256", "")
    return entries


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest_checksums(
    issues: list[ValidationIssue],
    root: Path,
    manifest_path: Path,
    required_artifacts: list[str],
) -> None:
    checksum_entries = manifest_checksum_entries(manifest_path)
    for relative_path in required_artifacts:
        expected_digest = checksum_entries.get(relative_path)
        if expected_digest is None:
            issues.append(ValidationIssue(str(manifest_path), f"missing checksum entry for {relative_path!r}"))
            continue
        actual_digest = sha256_file(root / relative_path)
        if expected_digest != actual_digest:
            issues.append(
                ValidationIssue(
                    str(manifest_path),
                    f"checksum mismatch for {relative_path!r}: manifest has {expected_digest!r}, file has {actual_digest!r}",
                )
            )


def validate_manifest_item_files(
    issues: list[ValidationIssue],
    root: Path,
    manifest_path: Path,
) -> None:
    manifest = load_json(manifest_path)
    for manifest_item in manifest.get("frozen_item_set", {}).get("items", []):
        item_path = root / manifest_item.get("path", "")
        item_data = load_json(item_path)
        expected_fields = {
            "item_id": item_data.get("item_id"),
            "item_version": item_data.get("version"),
            "domain": item_data.get("domain"),
            "construct": item_data.get("construct", {}).get("construct_id"),
        }
        for manifest_field, item_value in expected_fields.items():
            if manifest_item.get(manifest_field) != item_value:
                issues.append(
                    ValidationIssue(
                        str(item_path),
                        f"manifest {manifest_field}={manifest_item.get(manifest_field)!r} does not match item file value {item_value!r}",
                    )
                )


def packet_config(wave_id: str) -> PacketConfig:
    try:
        return PACKET_CONFIGS[wave_id]
    except KeyError as exc:
        raise WavePacketValidationError(
            f"unsupported wave_id {wave_id!r}; supported wave IDs are {sorted(PACKET_CONFIGS)}"
        ) from exc


def packet_paths(root: Path, wave_id: str, release: str) -> PacketPaths:
    config = packet_config(wave_id)
    if wave_id == "anx_us_2026w02_somatic" and release == "v0.2.2":
        return PacketPaths(
            instrument=root / "releases" / "v0.2.2" / "anx_us_2026w02_somatic_instrument.md",
            codebook=root / "releases" / "v0.2.2" / "anx_us_2026w02_somatic_codebook.md",
            preregistration=root
            / "releases"
            / "v0.2.2"
            / "anx_us_2026w02_somatic_calibration_preregistration.md",
            manifest=root / "releases" / release / "manifest.json",
            event_registry=root / config.event_registry_path if config.event_registry_path is not None else None,
        )
    event_registry = root / config.event_registry_path if config.event_registry_path is not None else None
    return PacketPaths(
        instrument=root / config.instrument_path,
        codebook=root / config.codebook_path,
        preregistration=root / config.preregistration_path,
        manifest=root / "releases" / release / "manifest.json",
        event_registry=event_registry,
    )


def benchmark_version_tuple(version: Any, field_name: str) -> tuple[int, int, int]:
    if not isinstance(version, str):
        raise WavePacketValidationError(f"{field_name} must be a semantic version string")
    match = BENCHMARK_VERSION_RE.fullmatch(version)
    if match is None:
        raise WavePacketValidationError(f"{field_name} is not a semantic release version: {version!r}")
    return (int(match.group("major")), int(match.group("minor")), int(match.group("patch")))


def is_same_line_not_later(effective_version: Any, requested_release: Any) -> bool:
    effective = benchmark_version_tuple(effective_version, "effective_benchmark_version")
    requested = benchmark_version_tuple(requested_release, "release")
    return effective[:2] == requested[:2] and effective <= requested


def compare_item_sets(
    issues: list[ValidationIssue],
    source_path: Path,
    source_records: list[ItemRecord],
    reference_path: Path,
    reference_records: list[ItemRecord],
) -> None:
    source_by_id = {record.item_id: record for record in source_records}
    reference_by_id = {record.item_id: record for record in reference_records}

    if len(source_by_id) != len(source_records):
        issues.append(ValidationIssue(str(source_path), "contains duplicate item IDs"))
    if set(source_by_id) != set(reference_by_id):
        missing = sorted(set(reference_by_id) - set(source_by_id))
        extra = sorted(set(source_by_id) - set(reference_by_id))
        details = []
        if missing:
            details.append(f"missing IDs {missing}")
        if extra:
            details.append(f"extra IDs {extra}")
        issues.append(
            ValidationIssue(
                str(source_path),
                f"item ID set differs from {reference_path}: " + "; ".join(details),
            )
        )

    for item_id in sorted(set(source_by_id) & set(reference_by_id)):
        source = source_by_id[item_id]
        reference = reference_by_id[item_id]
        if source.key() != reference.key():
            issues.append(
                ValidationIssue(
                    str(source_path),
                    f"{item_id} metadata differs from {reference_path}: "
                    f"got version={source.item_version!r}, domain={source.domain!r}, construct_id={source.construct_id!r}; "
                    f"expected version={reference.item_version!r}, domain={reference.domain!r}, construct_id={reference.construct_id!r}",
                )
            )


def validate_no_event_registry(
    issues: list[ValidationIssue],
    preregistration_text: str,
    codebook_text: str,
    event_registry_path: Path,
    expected_event_registry_reference: str,
    preregistration_path: Path,
    codebook_path: Path,
    wave_id: str,
    release: str,
) -> None:
    registry = load_json(event_registry_path)
    if expected_event_registry_reference not in preregistration_text:
        issues.append(
            ValidationIssue(
                str(preregistration_path),
                f"missing frozen event registry reference {expected_event_registry_reference!r}",
            )
        )
    if not any(phrase in preregistration_text for phrase in ("non-event calibration wave", "no-event", "not an event study")):
        issues.append(
            ValidationIssue(
                str(preregistration_path),
                "must state that this is a no-event or non-event wave",
            )
        )
    if "`event_id` | Constant `no_event`" not in codebook_text:
        issues.append(
            ValidationIssue(
                str(codebook_path),
                "event_id must map to constant no_event",
            )
        )
    if "retest" in wave_id and "`baseline_or_followup` | Constant `followup`" not in codebook_text:
        issues.append(
            ValidationIssue(
                str(codebook_path),
                "baseline_or_followup must map to constant followup",
            )
        )

    if registry.get("wave_id") != wave_id:
        issues.append(ValidationIssue(str(event_registry_path), f"wave_id is {registry.get('wave_id')!r}, expected {wave_id!r}"))
    if not is_same_line_not_later(registry.get("effective_benchmark_version"), release):
        issues.append(
            ValidationIssue(
                str(event_registry_path),
                f"effective_benchmark_version is {registry.get('effective_benchmark_version')!r}, expected same release line as {release!r} and not later",
            )
        )
    if registry.get("registry_status") != "frozen":
        issues.append(ValidationIssue(str(event_registry_path), "registry_status must be 'frozen'"))
    if registry.get("outcome_inspection_status") != "not_inspected":
        issues.append(ValidationIssue(str(event_registry_path), "outcome_inspection_status must be 'not_inspected'"))
    event_ids = [event.get("event_id") for event in registry.get("events", []) if isinstance(event, dict)]
    if event_ids != [NO_EVENT_ID]:
        issues.append(ValidationIssue(str(event_registry_path), f"events must contain only event_id {NO_EVENT_ID!r}"))


EXPECTED_WAVE7_DOMAIN_ORDERS = {
    "order_1": ("somatic_ambient", "economic_vocational", "epistemic"),
    "order_2": ("somatic_ambient", "epistemic", "economic_vocational"),
    "order_3": ("economic_vocational", "somatic_ambient", "epistemic"),
    "order_4": ("economic_vocational", "epistemic", "somatic_ambient"),
    "order_5": ("epistemic", "somatic_ambient", "economic_vocational"),
    "order_6": ("epistemic", "economic_vocational", "somatic_ambient"),
}

EXPECTED_WAVE8_DOMAIN_BLOCK_ORDER = (
    (
        "somatic_ambient",
        (
            "sleep_disruption_ai_news",
            "body_vigilance_model_release",
            "background_dread_ai_progress",
            "avoidance_after_ai_capability_demo",
        ),
    ),
    (
        "economic_vocational",
        (
            "skill_obsolescence_software",
            "wage_pressure_customer_support",
            "retraining_pressure_accounting",
            "status_loss_creative_work",
        ),
    ),
    (
        "epistemic",
        (
            "deepfake_evidence_trust",
            "synthetic_news_provenance",
            "ai_expert_claim_conflict",
            "personalized_misinformation_targeting",
        ),
    ),
    (
        "relational",
        (
            "partner_ai_confidant_displacement",
            "friend_group_ai_mediation",
            "eldercare_ai_attachment_shift",
        ),
    ),
    (
        "existential_identity",
        (
            "ai_personhood_boundary_uncertainty",
            "human_judgment_status_loss",
            "life_purpose_ai_substitution",
        ),
    ),
    (
        "autonomy_surveillance",
        (
            "public_space_tracking",
            "workplace_behavior_scoring",
            "personalized_behavior_nudging",
        ),
    ),
    (
        "safety_catastrophic",
        (
            "autonomous_cyber_cascade",
            "biosecurity_protocol_misuse",
            "military_escalation_ai_advice",
        ),
    ),
)


def parse_domain_order_tables(text: str) -> list[dict[str, tuple[str, str, str]]]:
    parsed_tables: list[dict[str, tuple[str, str, str]]] = []
    for table in parse_markdown_tables(text):
        if not table:
            continue
        columns = set(table[0])
        if not {"Order ID", "Block 1", "Block 2", "Block 3"} <= columns:
            continue
        parsed: dict[str, tuple[str, str, str]] = {}
        for row in table:
            parsed[strip_code(row["Order ID"])] = (
                strip_code(row["Block 1"]),
                strip_code(row["Block 2"]),
                strip_code(row["Block 3"]),
            )
        parsed_tables.append(parsed)
    return parsed_tables


def parse_wave8_domain_block_tables(text: str) -> list[tuple[tuple[str, tuple[str, ...]], ...]]:
    parsed_tables: list[tuple[tuple[str, tuple[str, ...]], ...]] = []
    for table in parse_markdown_tables(text):
        if not table:
            continue
        columns = set(table[0])
        if not {"Block position", "Domain", "Items randomized within block"} <= columns:
            continue
        rows = sorted(table, key=lambda row: int(strip_code(row["Block position"])))
        parsed_blocks = []
        for row in rows:
            item_ids = tuple(item.strip() for item in strip_code(row["Items randomized within block"]).split(","))
            parsed_blocks.append((strip_code(row["Domain"]), item_ids))
        parsed_tables.append(tuple(parsed_blocks))
    return parsed_tables


def validate_wave7_bridge_packet(
    issues: list[ValidationIssue],
    root: Path,
    paths: PacketPaths,
    instrument_text: str,
    codebook_text: str,
) -> None:
    required_artifacts = [
        "docs/instruments/anx_us_2026w07_cross_domain_bridge_instrument.md",
        "docs/instruments/anx_us_2026w07_cross_domain_bridge_codebook.md",
        "docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md",
        "events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json",
    ]
    validate_manifest_checksums(issues, root, paths.manifest, required_artifacts)

    for source_path, text in ((paths.instrument, instrument_text), (paths.codebook, codebook_text)):
        order_tables = parse_domain_order_tables(text)
        if not order_tables:
            issues.append(ValidationIssue(str(source_path), "missing six balanced domain-block orders table"))
            continue
        if not any(table == EXPECTED_WAVE7_DOMAIN_ORDERS for table in order_tables):
            issues.append(
                ValidationIssue(
                    str(source_path),
                    "domain-block order table must contain exactly the six balanced Wave 7 domain permutations",
                )
            )

    required_phrases = [
        "within each domain block",
        "randomize item screen order",
        "cross-domain attribution check",
        "988",
        "aggregate_scoring_permitted",
    ]
    combined_text_lower = f"{instrument_text}\n{codebook_text}".lower()
    for phrase in required_phrases:
        if phrase.lower() not in combined_text_lower:
            issues.append(ValidationIssue(str(paths.instrument), f"missing Wave 7 bridge requirement phrase {phrase!r}"))


def validate_wave8_full_domain_bridge_packet(
    issues: list[ValidationIssue],
    root: Path,
    paths: PacketPaths,
    instrument_text: str,
    codebook_text: str,
    preregistration_text: str,
    manifest_count: int | None,
    manifest_records: list[ItemRecord],
    codebook_records: list[ItemRecord],
    prereg_records: list[ItemRecord],
    instrument_item_ids: list[str],
) -> None:
    required_artifacts = [
        "docs/instruments/anx_us_2026w08_full_domain_bridge_instrument.md",
        "docs/preregistrations/anx_us_2026w08_full_domain_bridge.md",
        "events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json",
    ]
    validate_manifest_checksums(issues, root, paths.manifest, required_artifacts)

    expected_item_ids = [
        item_id
        for _domain, item_ids in EXPECTED_WAVE8_DOMAIN_BLOCK_ORDER
        for item_id in item_ids
    ]
    expected_domains = [
        domain
        for domain, item_ids in EXPECTED_WAVE8_DOMAIN_BLOCK_ORDER
        for _item_id in item_ids
    ]

    if manifest_count != 24:
        issues.append(ValidationIssue(str(paths.manifest), f"Wave 8 full-domain bridge must freeze exactly 24 items, got {manifest_count}"))
    for source_path, records in (
        (paths.manifest, manifest_records),
        (paths.codebook, codebook_records),
        (paths.preregistration, prereg_records),
    ):
        if len(records) != 24:
            issues.append(ValidationIssue(str(source_path), f"Wave 8 full-domain bridge must list exactly 24 administered items, got {len(records)}"))

    if instrument_item_ids != expected_item_ids:
        issues.append(
            ValidationIssue(
                str(paths.instrument),
                "Wave 8 item screen order must match the fixed seven domain-block sequence with within-block item allowlists",
            )
        )
    if [record.item_id for record in manifest_records] != expected_item_ids:
        issues.append(
            ValidationIssue(
                str(paths.manifest),
                "Wave 8 manifest item order must match the fixed seven domain-block sequence",
            )
        )
    if [record.domain for record in manifest_records] != expected_domains:
        issues.append(
            ValidationIssue(
                str(paths.manifest),
                "Wave 8 manifest domains must form exactly seven fixed domain blocks",
            )
        )

    block_tables = parse_wave8_domain_block_tables(instrument_text)
    if not block_tables:
        issues.append(ValidationIssue(str(paths.instrument), "missing fixed seven domain-block order table"))
    elif EXPECTED_WAVE8_DOMAIN_BLOCK_ORDER not in block_tables:
        issues.append(
            ValidationIssue(
                str(paths.instrument),
                "fixed domain-block order table must contain exactly the seven Wave 8 full-domain blocks",
            )
        )

    required_randomization_phrases = [
        "Items within each domain block are randomized independently",
        "uniform random permutation",
        "Randomize items within each domain block",
        "within_block_item_order",
    ]
    for phrase in required_randomization_phrases:
        if phrase not in instrument_text and phrase not in codebook_text:
            issues.append(ValidationIssue(str(paths.instrument), f"missing Wave 8 within-block randomization language {phrase!r}"))

    registry = load_json(paths.event_registry) if paths.event_registry is not None else {}
    event_ids = [event.get("event_id") for event in registry.get("events", []) if isinstance(event, dict)]
    if event_ids != [NO_EVENT_ID]:
        issues.append(ValidationIssue(str(paths.event_registry), f"Wave 8 event registry must contain exactly event_id {NO_EVENT_ID!r}"))
    if "`event_id` | Constant `no_event`" not in codebook_text:
        issues.append(ValidationIssue(str(paths.codebook), "Wave 8 codebook must map event_id to constant no_event"))
    if "`event_id: no_event`" not in preregistration_text:
        issues.append(ValidationIssue(str(paths.preregistration), "Wave 8 preregistration must state event_id: no_event"))

    manifest = load_json(paths.manifest)
    scoring_eligibility = manifest.get("scoring_eligibility", {})
    if scoring_eligibility.get("aggregate_scoring_permitted") is not False:
        issues.append(ValidationIssue(str(paths.manifest), "Wave 8 aggregate_scoring_permitted must be false"))


def validate_wave_packet(wave_id: str, root: Path | None = None, release: str = DEFAULT_RELEASE) -> None:
    root = Path.cwd().resolve() if root is None else root.resolve()
    config = packet_config(wave_id)
    if release == DEFAULT_RELEASE and config.default_release != DEFAULT_RELEASE:
        release = config.default_release
    paths = packet_paths(root, wave_id, release)

    issues: list[ValidationIssue] = []
    instrument_text = load_text(paths.instrument)
    preregistration_text = load_text(paths.preregistration)
    codebook_text = load_text(paths.codebook)
    instrument_wave_id, instrument_release, instrument_count, instrument_item_ids = parse_instrument(
        paths.instrument, wave_id
    )
    codebook_wave_id, codebook_release, codebook_records = parse_codebook(paths.codebook)
    prereg_records = parse_preregistration(paths.preregistration)
    manifest_release, manifest_item_directory, manifest_count, manifest_records = parse_manifest(paths.manifest)

    if instrument_wave_id != wave_id:
        issues.append(ValidationIssue(str(paths.instrument), f"Wave ID is {instrument_wave_id!r}, expected {wave_id!r}"))
    if codebook_wave_id != wave_id:
        issues.append(ValidationIssue(str(paths.codebook), f"Wave ID is {codebook_wave_id!r}, expected {wave_id!r}"))
    if instrument_release != manifest_release:
        issues.append(
            ValidationIssue(
                str(paths.instrument),
                f"Benchmark release {instrument_release!r} does not match manifest benchmark_version {manifest_release!r}",
            )
        )
    if codebook_release != manifest_release:
        issues.append(
            ValidationIssue(
                str(paths.codebook),
                f"Benchmark release {codebook_release!r} does not match manifest benchmark_version {manifest_release!r}",
            )
        )
    if manifest_release != release:
        issues.append(
            ValidationIssue(
                str(paths.manifest),
                f"benchmark_version {manifest_release!r} does not match requested release {release!r}",
            )
        )
    if manifest_item_directory != config.item_directory:
        issues.append(
            ValidationIssue(
                str(paths.manifest),
                f"frozen_item_set.item_directory is {manifest_item_directory!r}, expected {config.item_directory!r}",
            )
        )

    if manifest_count != len(manifest_records):
        issues.append(
            ValidationIssue(
                str(paths.manifest),
                f"frozen_item_set.item_count is {manifest_count}, but manifest lists {len(manifest_records)} items",
            )
        )
    if instrument_count != len(instrument_item_ids):
        issues.append(
            ValidationIssue(
                str(paths.instrument),
                f"randomization rule says {instrument_count} ANX items, but {len(instrument_item_ids)} Item Screen headings were found",
            )
        )
    if manifest_count is not None and instrument_count != manifest_count:
        issues.append(
            ValidationIssue(
                str(paths.instrument),
                f"instrument item count {instrument_count} does not match manifest item_count {manifest_count}",
            )
        )

    instrument_ids = set(instrument_item_ids)
    manifest_by_id = {record.item_id: record for record in manifest_records}
    instrument_records = [manifest_by_id[item_id] for item_id in instrument_item_ids if item_id in manifest_by_id]
    missing_from_manifest = sorted(instrument_ids - set(manifest_by_id))
    if missing_from_manifest:
        issues.append(
            ValidationIssue(
                str(paths.instrument),
                f"instrument includes item IDs not present in manifest: {missing_from_manifest}",
            )
        )

    compare_item_sets(issues, paths.preregistration, prereg_records, paths.manifest, manifest_records)
    compare_item_sets(issues, paths.codebook, codebook_records, paths.manifest, manifest_records)
    compare_item_sets(issues, paths.instrument, instrument_records, paths.manifest, manifest_records)
    validate_manifest_item_files(issues, root, paths.manifest)

    if paths.event_registry is not None:
        validate_no_event_registry(
            issues,
            preregistration_text,
            codebook_text,
            paths.event_registry,
            config.event_registry_path or "",
            paths.preregistration,
            paths.codebook,
            wave_id,
            release,
        )

    if wave_id == "anx_us_2026w07_cross_domain_bridge":
        validate_wave7_bridge_packet(issues, root, paths, instrument_text, codebook_text)
    if wave_id == "anx_us_2026w08_full_domain_bridge":
        validate_wave8_full_domain_bridge_packet(
            issues,
            root,
            paths,
            instrument_text,
            codebook_text,
            preregistration_text,
            manifest_count,
            manifest_records,
            codebook_records,
            prereg_records,
            instrument_item_ids,
        )

    if issues:
        rendered = "\n".join(f"- {issue.render()}" for issue in issues)
        raise WavePacketValidationError(f"wave packet validation failed with {len(issues)} issue(s):\n{rendered}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an ANX-Bench frozen wave packet.")
    parser.add_argument("wave_id", help="Wave identifier, for example anx_us_2026w01")
    parser.add_argument(
        "--release",
        default=DEFAULT_RELEASE,
        help=f"Benchmark release directory under releases/; default: {DEFAULT_RELEASE}",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_wave_packet(args.wave_id, root=args.root, release=args.release)
    except WavePacketValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"wave packet validation passed: {args.wave_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
