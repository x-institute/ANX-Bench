import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROVENANCE_TEMPLATE_PATH = (
    REPO_ROOT
    / "validation"
    / "v0.8"
    / "full_domain_bridge"
    / "wave8_evidence_provenance.template.json"
)
MANIFEST_TEMPLATE_PATH = (
    REPO_ROOT
    / "validation"
    / "v0.8"
    / "full_domain_bridge"
    / "wave8_evidence_manifest.template.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_ref(schema: dict, ref: str) -> dict:
    node = schema
    for part in ref.removeprefix("#/").split("/"):
        node = node[part]
    return node


def _type_matches(instance: object, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(instance, dict)
    if expected_type == "array":
        return isinstance(instance, list)
    if expected_type == "string":
        return isinstance(instance, str)
    if expected_type == "null":
        return instance is None
    if expected_type == "boolean":
        return isinstance(instance, bool)
    return True


def _schema_errors(instance: object, node: dict, root_schema: dict, path: str = "$") -> list[str]:
    if "$ref" in node:
        return _schema_errors(instance, _resolve_ref(root_schema, node["$ref"]), root_schema, path)

    if "anyOf" in node:
        if any(not _schema_errors(instance, option, root_schema, path) for option in node["anyOf"]):
            return []
        return [f"{path}: did not match any allowed schema"]

    errors: list[str] = []
    expected_type = node.get("type")
    if isinstance(expected_type, list):
        if not any(_type_matches(instance, item) for item in expected_type):
            errors.append(f"{path}: expected one of {expected_type}")
            return errors
    elif isinstance(expected_type, str) and not _type_matches(instance, expected_type):
        errors.append(f"{path}: expected {expected_type}")
        return errors

    if "const" in node and instance != node["const"]:
        errors.append(f"{path}: expected const {node['const']!r}")
    if "enum" in node and instance not in node["enum"]:
        errors.append(f"{path}: expected enum member")
    if isinstance(instance, str):
        if "minLength" in node and len(instance) < node["minLength"]:
            errors.append(f"{path}: shorter than minLength")
        if "pattern" in node and not re.fullmatch(node["pattern"], instance):
            errors.append(f"{path}: does not match {node['pattern']}")
    if isinstance(instance, list):
        if "minItems" in node and len(instance) < node["minItems"]:
            errors.append(f"{path}: fewer than minItems")
        item_schema = node.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                errors.extend(_schema_errors(item, item_schema, root_schema, f"{path}/{index}"))
    if isinstance(instance, dict):
        required = node.get("required", [])
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required key {key}")
        properties = node.get("properties", {})
        if node.get("additionalProperties") is False:
            extra = set(instance) - set(properties)
            if extra:
                errors.append(f"{path}: unexpected keys {sorted(extra)}")
        for key, child_schema in properties.items():
            if key in instance:
                errors.extend(_schema_errors(instance[key], child_schema, root_schema, f"{path}/{key}"))
    return errors


class Wave8EvidenceTemplateTests(unittest.TestCase):
    def assert_schema_validates(self, instance: dict, schema_path: Path) -> None:
        schema = _load(schema_path)
        self.assertEqual([], _schema_errors(instance, schema, schema))

    def test_wave8_evidence_provenance_template_schema_validates_as_placeholder(self) -> None:
        provenance = _load(PROVENANCE_TEMPLATE_PATH)
        self.assert_schema_validates(provenance, REPO_ROOT / "schema" / "evidence_provenance.schema.json")

        self.assertEqual("planned_or_placeholder", provenance["evidence_status"])
        self.assertEqual(
            {
                "sample_exclusions",
                "split_assignment",
                "efa",
                "cfa",
                "omega",
                "irt",
                "dif",
                "invariance",
                "latent_correlations",
                "somatic_anchor_drift",
                "final_bridge_decision",
            },
            {record["analysis_family"] for record in provenance["validation_statistics"]},
        )
        for record in provenance["validation_statistics"]:
            self.assertEqual("planned_or_placeholder", record["evidence_status"])
            self.assertEqual("unsigned_placeholder", record["signoff"]["signature_status"])
            self.assertIn("Template record only", record["provenance_note"])
            self.assertIsNone(record["signoff"]["signed_date"])
            self.assertTrue(any(artifact["sha256"] is None for artifact in record["data_artifacts"]))
            self.assertTrue(any(script["sha256"] is None for script in record["analysis_scripts"]))

        assertion = provenance["provenance_assertion"].lower()
        self.assertIn("planned_or_placeholder", assertion)
        self.assertIn("no observed citable evidence", assertion)
        self.assertIn("cannot support", assertion)

    def test_wave8_evidence_manifest_template_schema_validates_as_non_citable_placeholder(self) -> None:
        manifest = _load(MANIFEST_TEMPLATE_PATH)
        self.assert_schema_validates(
            manifest,
            REPO_ROOT / "schema" / "psychometric_evidence_manifest.schema.json",
        )

        zero_hash = "0" * 64
        self.assertEqual(zero_hash, manifest["raw_restricted_dataset_hash"]["sha256"])
        self.assertEqual(zero_hash, manifest["analysis_script_hash"]["sha256"])
        self.assertEqual(zero_hash, manifest["software_session_lock"]["session_info_sha256"])
        self.assertIn("placeholder", manifest["analyst"]["name"])

        artifact_ids = {artifact["artifact_id"] for artifact in manifest["output_artifact_hashes"]}
        for artifact in manifest["output_artifact_hashes"]:
            self.assertEqual(zero_hash, artifact["sha256"])
            description = artifact["description"].lower()
            for required_binding in (
                "restricted",
                "split-file hash",
                "software lock",
                "analyst signoff",
                "reviewer signoff",
                "output hash",
            ):
                self.assertIn(required_binding, description)

        self.assertEqual(
            {
                "sample_exclusions_gate",
                "split_assignment_gate",
                "efa_gate",
                "cfa_gate",
                "omega_gate",
                "irt_gate",
                "dif_gate",
                "invariance_gate",
                "latent_correlations_gate",
                "somatic_anchor_drift_gate",
                "final_bridge_decision_gate",
            },
            {record["statistic_id"] for record in manifest["reported_statistic_map"]},
        )
        for record in manifest["reported_statistic_map"]:
            self.assertIn(record["artifact_id"], artifact_ids)
            self.assertIn("planned_or_placeholder", record["reported_value"])
            self.assertIn("--split", record["reproduction_command"])
            self.assertIn("--session-lock", record["reproduction_command"])

        assertion = manifest["provenance_assertion"].lower()
        self.assertIn("planned_or_placeholder only", assertion)
        self.assertIn("no observed citable evidence", assertion)
        self.assertIn("cannot authorize", assertion)


if __name__ == "__main__":
    unittest.main()
