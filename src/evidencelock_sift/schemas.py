from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(frozen=True)
class EvidenceArtifact:
    evidence_id: str
    path: str
    sha256: str
    kind: str


@dataclass(frozen=True)
class EventRecord:
    evidence_id: str
    source_path: str
    record_number: str
    timestamp: str
    event_id: str
    channel: str
    host: str
    message: str
    fields: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    source_path: str
    record_number: str
    timestamp: str
    matched_fields: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolRef:
    command_id: str
    tool_name: str
    args: dict[str, Any]
    status: str


@dataclass
class Finding:
    finding_id: str
    title: str
    status: str
    confidence: float
    summary: str
    mitre_techniques: list[str] = field(default_factory=list)
    evidence_refs: list[EvidenceRef] = field(default_factory=list)
    tool_refs: list[ToolRef] = field(default_factory=list)
    correction_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class VerificationIssue:
    finding_id: str
    severity: str
    message: str


@dataclass
class InvestigationReport:
    case_id: str
    title: str
    findings: list[Finding]
    verifier_iterations: int
    verifier_issues: list[VerificationIssue]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
