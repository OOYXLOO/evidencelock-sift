from __future__ import annotations

from evidencelock_sift.schemas import EventRecord
from evidencelock_sift.schemas import Finding
from evidencelock_sift.schemas import VerificationIssue

ALLOWED_STATUSES = {"confirmed", "inferred", "disproven", "unresolved"}

def _produced_evidence_ids(entry: dict) -> set[str]:
    result = entry.get("result") or {}
    produced: set[str] = set()
    matches = result.get("matches")
    if isinstance(matches, list):
        produced.update(str(item) for item in matches)
    event = result.get("event")
    if isinstance(event, dict) and event.get("evidence_id"):
        produced.add(str(event["evidence_id"]))
    return produced

def verify_findings(
    findings: list[Finding],
    events: list[EventRecord],
    execution_log: list[dict] | None = None,
) -> list[VerificationIssue]:
    known_evidence_ids = {event.evidence_id for event in events}
    log_by_command = {
        str(entry.get("command_id")): entry
        for entry in (execution_log or [])
        if entry.get("command_id")
    }
    issues: list[VerificationIssue] = []
    for finding in findings:
        if finding.status not in ALLOWED_STATUSES:
            issues.append(
                VerificationIssue(
                    finding_id=finding.finding_id,
                    severity="error",
                    message=f"invalid status {finding.status!r}",
                )
            )
        if finding.status == "confirmed" and not finding.evidence_refs:
            issues.append(
                VerificationIssue(
                    finding_id=finding.finding_id,
                    severity="error",
                    message="confirmed finding has no evidence_refs",
                )
            )
        if finding.status == "confirmed" and not finding.tool_refs:
            issues.append(
                VerificationIssue(
                    finding_id=finding.finding_id,
                    severity="error",
                    message="confirmed finding has no tool_refs",
                )
            )

        produced_by_cited_tools: set[str] = set()
        for ref in finding.tool_refs:
            entry = log_by_command.get(ref.command_id)
            if execution_log is not None and entry is None:
                issues.append(
                    VerificationIssue(
                        finding_id=finding.finding_id,
                        severity="error",
                        message=f"unknown tool command_id {ref.command_id}",
                    )
                )
                continue
            if entry is None:
                continue
            if entry.get("status") != "success":
                issues.append(
                    VerificationIssue(
                        finding_id=finding.finding_id,
                        severity="error",
                        message=f"tool command_id {ref.command_id} did not succeed",
                    )
                )
            if entry.get("tool_name") != ref.tool_name:
                issues.append(
                    VerificationIssue(
                        finding_id=finding.finding_id,
                        severity="error",
                        message=f"tool command_id {ref.command_id} name mismatch",
                    )
                )
            if ref.args and entry.get("args") != ref.args:
                issues.append(
                    VerificationIssue(
                        finding_id=finding.finding_id,
                        severity="error",
                        message=f"tool command_id {ref.command_id} args mismatch",
                    )
                )
            produced_by_cited_tools.update(_produced_evidence_ids(entry))

        for ref in finding.evidence_refs:
            if ref.evidence_id not in known_evidence_ids:
                issues.append(
                    VerificationIssue(
                        finding_id=finding.finding_id,
                        severity="error",
                        message=f"unknown evidence_id {ref.evidence_id}",
                    )
                )
            if (
                finding.status == "confirmed"
                and execution_log is not None
                and finding.tool_refs
                and ref.evidence_id not in produced_by_cited_tools
            ):
                issues.append(
                    VerificationIssue(
                        finding_id=finding.finding_id,
                        severity="error",
                        message=f"evidence_id {ref.evidence_id} was not produced by cited tool_refs",
                    )
                )
        if finding.mitre_techniques and finding.status == "confirmed" and not finding.evidence_refs:
            issues.append(
                VerificationIssue(
                    finding_id=finding.finding_id,
                    severity="error",
                    message="MITRE-mapped confirmed finding lacks evidence",
                )
            )
    return issues
