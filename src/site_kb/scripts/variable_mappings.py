"""Apply reviewed source-to-ontology crosswalks without rewriting source identities."""

from copy import deepcopy
from pathlib import Path
import yaml


def read_mappings(directory: Path) -> list[dict]:
    """Load reusable assertions; full LinkML validation runs in validate-db."""
    mappings = []
    relations = {}
    for path in sorted(directory.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict) or set(data) != {"mappings"} or not isinstance(data["mappings"], list):
            raise ValueError(f"{path}: expected a mappings list")
        for mapping in data["mappings"]:
            if not isinstance(mapping, dict):
                raise ValueError(f"{path}: mapping must be an object")
            for key in ("source", "source_id"):
                if not isinstance(mapping.get(key), str) or not mapping[key].strip():
                    raise ValueError(f"{path}: mapping requires {key}")
            target = mapping.get("target")
            if not isinstance(target, dict) or any(not isinstance(target.get(k), str) or not target[k].strip() for k in ("id", "label")):
                raise ValueError(f"{path}: mapping target requires id and label")
            if mapping.get("relation") not in {"EXACT", "CLOSE", "BROAD", "NARROW", "RELATED"}:
                raise ValueError(f"{path}: unsupported mapping relation")
            if mapping.get("origin") not in {"SOURCE", "CURATED"}:
                raise ValueError(f"{path}: unsupported mapping origin")
            evidence = mapping.get("evidence")
            if not isinstance(evidence, list) or not evidence or any(not isinstance(v, str) or not v for v in evidence):
                raise ValueError(f"{path}: mapping requires evidence URLs")
            key = (mapping["source"], mapping["source_id"], target["id"], mapping["origin"])
            if key in relations and relations[key] != mapping["relation"]:
                raise ValueError(f"{path}: conflicting relations for {key}")
            relations[key] = mapping["relation"]
            if mapping not in mappings:
                mappings.append(mapping)
    return mappings


def apply_mappings(sites: dict[str, dict], mappings: list[dict]) -> None:
    by_source = {}
    for mapping in mappings:
        by_source.setdefault((mapping["source"], mapping["source_id"]), []).append(mapping)
    for site in sites.values():
        for variable in site.get("variables", []):
            for source in variable.get("source_variables", []):
                for mapping in by_source.get((source["source"], source.get("source_id")), []):
                    assertions = variable.setdefault("mappings", [])
                    if mapping not in assertions:
                        assertions.append(deepcopy(mapping))
            # Do not promote a mapping to term: even an exactMatch is an assertion
            # with provenance, not permission to overwrite a primary curator choice.
