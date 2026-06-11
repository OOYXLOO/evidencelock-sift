from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from evidencelock_sift.schemas import EventRecord


def _stable_evidence_id(source_path: Path, record_number: str) -> str:
    return f"{source_path.stem}:{record_number}"


def _normalize_event(
    raw: dict[str, Any],
    source_path: Path,
    source_label: str | None = None,
) -> EventRecord:
    record_number = str(
        raw.get("record_number")
        or raw.get("EventRecordID")
        or raw.get("event_record_id")
        or raw.get("record")
        or "unknown"
    )
    event_id = str(raw.get("event_id") or raw.get("EventID") or raw.get("id") or "unknown")
    timestamp = str(raw.get("timestamp") or raw.get("TimeCreated") or raw.get("time") or "")
    channel = str(raw.get("channel") or raw.get("Channel") or "")
    host = str(raw.get("host") or raw.get("Computer") or "")
    message = str(raw.get("message") or raw.get("Message") or "")
    tags = [str(tag) for tag in raw.get("tags", [])]
    fields = {str(key): value for key, value in raw.items()}
    return EventRecord(
        evidence_id=str(raw.get("evidence_id") or _stable_evidence_id(source_path, record_number)),
        source_path=source_label or str(source_path),
        record_number=record_number,
        timestamp=timestamp,
        event_id=event_id,
        channel=channel,
        host=host,
        message=message,
        fields=fields,
        tags=tags,
    )


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def _load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("events"), list):
        return payload["events"]
    raise ValueError(f"expected a JSON event list in {path}")


def _load_xml(path: Path) -> list[dict[str, Any]]:
    root = ET.parse(path).getroot()
    events: list[dict[str, Any]] = []
    for index, event in enumerate(root.findall(".//Event"), start=1):
        payload: dict[str, Any] = {"record_number": str(index)}
        for element in event.iter():
            tag = element.tag.rsplit("}", 1)[-1]
            text = (element.text or "").strip()
            if text and tag not in payload:
                payload[tag] = text
            if tag == "EventID" and text:
                payload["event_id"] = text
        events.append(payload)
    return events


def parse_events(path: Path, source_label: str | None = None) -> list[EventRecord]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        raw_events = _load_jsonl(path)
    elif suffix == ".json":
        raw_events = _load_json(path)
    elif suffix == ".xml":
        raw_events = _load_xml(path)
    elif suffix == ".evtx":
        raise RuntimeError(
            "binary EVTX parsing is intentionally optional in this demo; "
            "export EVTX to JSONL/XML with SIFT/EZ Tools or add python-evtx on a SIFT workstation"
        )
    else:
        raise ValueError(f"unsupported event evidence format: {path.suffix}")
    return [_normalize_event(raw, path, source_label=source_label) for raw in raw_events]


def search_events(
    events: list[EventRecord],
    *,
    event_ids: set[str] | None = None,
    contains: str | None = None,
    tags: set[str] | None = None,
) -> list[EventRecord]:
    needle = contains.lower() if contains else None
    matches: list[EventRecord] = []
    for event in events:
        if event_ids and event.event_id not in event_ids:
            continue
        if tags and not tags.intersection(set(event.tags)):
            continue
        haystack = json.dumps(event.fields, sort_keys=True).lower()
        if needle and needle not in haystack:
            continue
        matches.append(event)
    return matches

def extract_event_evidence(events: list[EventRecord], evidence_id: str) -> EventRecord | None:
    for event in events:
        if event.evidence_id == evidence_id:
            return event
    return None
