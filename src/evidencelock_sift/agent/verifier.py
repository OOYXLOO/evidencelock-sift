from __future__ import annotations

from evidencelock_sift.schemas import EventRecord
from evidencelock_sift.schemas import Finding
from evidencelock_sift.schemas import VerificationIssue

ALLOWED_STATUSES = {"confirmed", "inferred", "disproven", "unresolved"}


def verify_findings(findings: list[Finding], events: list[EventRecord]) -> list[VerificationIssue]:
    known_evidence_ids = {event.evidence_id for event in events}
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
        for ref in finding.evidence_refs:
            if ref.evidence_id not in known_evidence_ids:
                issues.append(
                    VerificationIssue(
                        finding_id=finding.finding_id,
                        severity="error",
                        message=f"unknown evidence_id {ref.evidence_id}",
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
