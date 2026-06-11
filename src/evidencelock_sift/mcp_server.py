from __future__ import annotations

import json
from pathlib import Path

from evidencelock_sift.agent.verifier import verify_findings
from evidencelock_sift.schemas import EvidenceRef
from evidencelock_sift.schemas import Finding
from evidencelock_sift.schemas import ToolRef
from evidencelock_sift.tools.evidence import hash_evidence
from evidencelock_sift.tools.evidence import list_evidence
from evidencelock_sift.tools.evtx import extract_event_evidence
from evidencelock_sift.tools.evtx import parse_events
from evidencelock_sift.tools.evtx import search_events


TOOL_SCHEMAS = [
    {
        "name": "list_evidence",
        "description": "List and hash read-only evidence artifacts under an evidence root.",
        "input_schema": {"type": "object", "properties": {"root": {"type": "string"}}, "required": ["root"]},
    },
    {
        "name": "hash_evidence",
        "description": "Return SHA-256 and metadata for one evidence artifact.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    },
    {
        "name": "parse_evtx",
        "description": "Parse normalized EVTX JSONL/XML exports into evidence-linked event records.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    },
    {
        "name": "search_events",
        "description": "Search parsed event records by event ID, substring, or tag.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "event_ids": {"type": "array", "items": {"type": "string"}},
                "contains": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["path"],
        },
    },
    {
        "name": "extract_event_evidence",
        "description": "Return the exact event record for an evidence ID so reports can cite concrete evidence.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}, "evidence_id": {"type": "string"}},
            "required": ["path", "evidence_id"],
        },
    },
    {
        "name": "verify_report_claims",
        "description": "Reject confirmed findings that lack valid evidence references or tool-call references.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "findings": {"type": "array", "items": {"type": "object"}},
            },
            "required": ["path", "findings"],
        },
    },
]


def _finding_from_dict(payload: dict) -> Finding:
    evidence_refs = [EvidenceRef(**ref) for ref in payload.get("evidence_refs", [])]
    tool_refs = [ToolRef(**ref) for ref in payload.get("tool_refs", [])]
    return Finding(
        finding_id=str(payload["finding_id"]),
        title=str(payload["title"]),
        status=str(payload["status"]),
        confidence=float(payload["confidence"]),
        summary=str(payload["summary"]),
        mitre_techniques=[str(item) for item in payload.get("mitre_techniques", [])],
        evidence_refs=evidence_refs,
        tool_refs=tool_refs,
        correction_notes=[str(item) for item in payload.get("correction_notes", [])],
    )


def call_tool(name: str, args: dict) -> dict:
    if name == "list_evidence":
        return {"artifacts": [artifact.__dict__ for artifact in list_evidence(Path(args["root"]))]}
    if name == "hash_evidence":
        return hash_evidence(Path(args["path"])).__dict__
    if name == "parse_evtx":
        return {"events": [event.__dict__ for event in parse_events(Path(args["path"]))]}
    if name == "search_events":
        events = parse_events(Path(args["path"]))
        matches = search_events(
            events,
            event_ids=set(args.get("event_ids") or []) or None,
            contains=args.get("contains"),
            tags=set(args.get("tags") or []) or None,
        )
        return {"matches": [event.__dict__ for event in matches]}
    if name == "extract_event_evidence":
        events = parse_events(Path(args["path"]))
        event = extract_event_evidence(events, str(args["evidence_id"]))
        return {"event": event.__dict__ if event else None}
    if name == "verify_report_claims":
        events = parse_events(Path(args["path"]))
        findings = [_finding_from_dict(finding) for finding in args["findings"]]
        return {"issues": [issue.__dict__ for issue in verify_findings(findings, events)]}
    raise ValueError(f"unknown tool {name}")


def main() -> int:
    print(json.dumps({"tools": TOOL_SCHEMAS}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
