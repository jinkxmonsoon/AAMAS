"""Validation helpers for representation-only redesigned CCT graph artifacts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from cctdiag.cct.causal_edges import FORBIDDEN_NOTE_TERMS, FORBIDDEN_OUTPUT_FIELDS
from cctdiag.cct.redesigned_builder import BASE_EDGE_TYPES, STRONG_CAUSAL_EDGE_TYPES

_ALLOWED_EDGE_TYPES = BASE_EDGE_TYPES | STRONG_CAUSAL_EDGE_TYPES


def redesigned_graph_leakage_findings(graphs: Sequence[Mapping[str, Any]]) -> list[str]:
    findings: list[str] = []
    for graph_index, graph in enumerate(graphs):
        for path, key, value in _walk(graph):
            if key in FORBIDDEN_OUTPUT_FIELDS:
                findings.append(f"graph[{graph_index}].{path}")
            if key == "extraction_notes":
                note = str(value).lower()
                for term in FORBIDDEN_NOTE_TERMS:
                    if term in note:
                        findings.append(f"graph[{graph_index}].{path}:{term}")
    return sorted(set(findings))


def validate_redesigned_graph(graph: Mapping[str, Any]) -> None:
    edge_types = {edge["edge_type"] for edge in graph.get("edges", [])}
    unknown = edge_types - _ALLOWED_EDGE_TYPES
    if unknown:
        raise ValueError("redesigned graph contains out-of-scope edge type(s): " + ", ".join(sorted(unknown)))
    findings = redesigned_graph_leakage_findings([graph])
    if findings:
        raise ValueError("redesigned graph leakage findings: " + ", ".join(findings))


def _walk(value: Any, path: str = ""):
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key)
            nested_path = f"{path}.{key_text}" if path else key_text
            yield nested_path, key_text, nested
            yield from _walk(nested, nested_path)
    elif isinstance(value, list | tuple):
        for index, item in enumerate(value):
            yield from _walk(item, f"{path}[{index}]")
