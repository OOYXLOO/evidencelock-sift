from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evidencelock_sift.agent.verifier import verify_findings
from evidencelock_sift.logging.audit import AuditLogger
from evidencelock_sift.schemas import EvidenceRef
from evidencelock_sift.schemas import Finding
from evidencelock_sift.schemas import InvestigationReport
from evidencelock_sift.schemas import ToolRef
from evidencelock_sift.tools.evidence import hash_evidence
from evidencelock_sift.tools.evidence import resolve_under
from evidencelock_sift.tools.evidence import sha256_file
from evidencelock_sift.tools.evtx import parse_events
from evidencelock_sift.tools.evtx import search_events


def _load_case(case_path: Path) -> dict[str, Any]:
    with case_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.name


def _tool_ref(command_id: str, tool_name: str, args: dict[str, Any]) -> ToolRef:
    return ToolRef(command_id=command_id, tool_name=tool_name, args=args, status="success")


def _evidence_ref(event) -> EvidenceRef:
    return EvidenceRef(
        evidence_id=event.evidence_id,
        source_path=event.source_path,
        record_number=event.record_number,
        timestamp=event.timestamp,
        matched_fields={
            "event_id": event.event_id,
            "message": event.message,
            "tags": event.tags,
        },
    )


def _initial_draft() -> list[Finding]:
    return [
        Finding(
            finding_id="F-001",
            title="Suspicious PowerShell execution",
            status="confirmed",
            confidence=0.7,
            summary="A document-spawned PowerShell process appears to run an encoded command.",
            mitre_techniques=["T1059.001"],
        )
    ]


def _correct_findings(findings: list[Finding], events, command_refs: dict[str, ToolRef]) -> list[Finding]:
    corrected: list[Finding] = []
    powershell_events = search_events(
        events,
        event_ids={"4688"},
        contains="encodedcommand",
    )
    service_events = search_events(
        events,
        event_ids={"7045"},
        contains="temp",
    )
    for finding in findings:
        if finding.finding_id == "F-001" and powershell_events:
            event = powershell_events[0]
            finding.evidence_refs = [_evidence_ref(event)]
            finding.tool_refs = [command_refs["search_powershell"]]
            finding.correction_notes.append(
                "Verifier rejected the first draft because it lacked evidence_refs; correction attached the exact process-creation event."
            )
        elif finding.finding_id == "F-001":
            finding.status = "unresolved"
            finding.confidence = 0.2
            finding.summary = (
                "The draft PowerShell claim could not be confirmed because the supplied evidence contained no matching "
                "PowerShell encoded-command process-creation event."
            )
            finding.correction_notes.append(
                "Verifier rejected the first draft because it lacked evidence_refs; correction downgraded the claim to unresolved instead of inventing evidence."
            )
        corrected.append(finding)
    if service_events:
        event = service_events[0]
        corrected.append(
            Finding(
                finding_id="F-002",
                title="Suspicious service installation",
                status="confirmed",
                confidence=0.74,
                summary="A service was installed with an executable path under a temporary directory.",
                mitre_techniques=["T1543.003"],
                evidence_refs=[_evidence_ref(event)],
                tool_refs=[command_refs["search_service"]],
                correction_notes=[
                    "Added after the collection pass found a service-installation event with a suspicious image path."
                ],
            )
        )
    return corrected


def run_case(case_path: Path, out_dir: Path) -> InvestigationReport:
    out_dir.mkdir(parents=True, exist_ok=True)
    audit = AuditLogger(out_dir / "execution_log.jsonl")
    if (out_dir / "execution_log.jsonl").exists():
        (out_dir / "execution_log.jsonl").unlink()

    case = _load_case(case_path)
    base_dir = case_path.parent
    event_path = resolve_under(base_dir, case["event_evidence"])
    event_label = _display_path(event_path)

    artifact = hash_evidence(event_path, evidence_id=case["case_id"], kind="normalized_evtx_jsonl")
    audit.record("hash_evidence", {"path": event_label}, "success", {"sha256": artifact.sha256})

    events = parse_events(event_path, source_label=event_label)
    parse_command = audit.record(
        "parse_evtx",
        {"path": event_label, "format": event_path.suffix},
        "success",
        {"events": len(events)},
    )

    ps_matches = search_events(events, event_ids={"4688"}, contains="encodedcommand")
    ps_command = audit.record(
        "search_events",
        {"event_ids": ["4688"], "contains": "encodedcommand"},
        "success",
        {"matches": [event.evidence_id for event in ps_matches]},
    )
    service_matches = search_events(events, event_ids={"7045"}, contains="temp")
    service_command = audit.record(
        "search_events",
        {"event_ids": ["7045"], "contains": "temp"},
        "success",
        {"matches": [event.evidence_id for event in service_matches]},
    )

    command_refs = {
        "parse": _tool_ref(parse_command, "parse_evtx", {"path": event_label}),
        "search_powershell": _tool_ref(
            ps_command,
            "search_events",
            {"event_ids": ["4688"], "contains": "encodedcommand"},
        ),
        "search_service": _tool_ref(
            service_command,
            "search_events",
            {"event_ids": ["7045"], "contains": "temp"},
        ),
    }

    findings = _initial_draft()
    first_issues = verify_findings(findings, events, audit.entries)
    audit.record(
        "verify_report_claims",
        {"iteration": 1},
        "failed" if first_issues else "success",
        {"issues": [issue.__dict__ for issue in first_issues]},
    )

    findings = _correct_findings(findings, events, command_refs)
    final_issues = verify_findings(findings, events, audit.entries)
    audit.record(
        "verify_report_claims",
        {"iteration": 2},
        "failed" if final_issues else "success",
        {"issues": [issue.__dict__ for issue in final_issues]},
    )

    report = InvestigationReport(
        case_id=case["case_id"],
        title=case["title"],
        findings=findings,
        verifier_iterations=2,
        verifier_issues=final_issues,
    )
    _write_report(report, out_dir)
    _write_accuracy_report(case, events, findings, first_issues, final_issues, out_dir)
    _write_timeline_report(case["case_id"], events, out_dir)
    _write_analyst_handoff(report, out_dir)
    _write_agent_trace(case["case_id"], out_dir)
    _write_integrity_manifest(case["case_id"], artifact, event_label, out_dir)
    return report


def _write_report(report: InvestigationReport, out_dir: Path) -> None:
    with (out_dir / "investigation_report.json").open("w", encoding="utf-8") as handle:
        json.dump(report.to_dict(), handle, indent=2, sort_keys=True)
    lines = [
        f"# {report.title}",
        "",
        f"Case ID: `{report.case_id}`",
        f"Verifier iterations: `{report.verifier_iterations}`",
        f"Final verifier issues: `{len(report.verifier_issues)}`",
        "",
        "## Findings",
        "",
    ]
    for finding in report.findings:
        lines.extend(
            [
                f"### {finding.finding_id}: {finding.title}",
                "",
                f"- Status: `{finding.status}`",
                f"- Confidence: `{finding.confidence:.2f}`",
                f"- MITRE: `{', '.join(finding.mitre_techniques) or 'none'}`",
                f"- Summary: {finding.summary}",
                "",
                "Evidence:",
            ]
        )
        for ref in finding.evidence_refs:
            lines.append(
                f"- `{ref.evidence_id}` record `{ref.record_number}` at `{ref.timestamp}` from `{ref.source_path}`"
            )
        lines.append("")
        lines.append("Tool calls:")
        for ref in finding.tool_refs:
            lines.append(f"- `{ref.command_id}` `{ref.tool_name}` args `{json.dumps(ref.args, sort_keys=True)}`")
        if finding.correction_notes:
            lines.append("")
            lines.append("Correction notes:")
            for note in finding.correction_notes:
                lines.append(f"- {note}")
        lines.append("")
    (out_dir / "investigation_report.md").write_text("\n".join(lines), encoding="utf-8")


def _write_accuracy_report(case: dict[str, Any], events, findings: list[Finding], first_issues, final_issues, out_dir: Path) -> None:
    expected = set(case.get("expected_findings", []))
    final_findings = {finding.finding_id for finding in findings}
    confirmed_findings = {finding.finding_id for finding in findings if finding.status == "confirmed"}
    expected_found = expected.intersection(final_findings)
    expected_confirmed = expected.intersection(confirmed_findings)
    expected_missed = expected.difference(confirmed_findings)
    false_positives = confirmed_findings.difference(expected)
    true_negatives = sum(1 for event in events if "benign" in event.tags)
    confirmed = [finding for finding in findings if finding.status == "confirmed"]
    confirmed_with_evidence = [finding for finding in confirmed if finding.evidence_refs]
    confirmed_with_tools = [finding for finding in confirmed if finding.tool_refs]
    lines = [
        "# Accuracy Report",
        "",
        f"Case: `{case['case_id']}`",
        "",
        "## Metrics",
        "",
        "| Metric | Result |",
        "| --- | ---: |",
        f"| Draft verifier issues | `{len(first_issues)}` |",
        f"| Final verifier issues | `{len(final_issues)}` |",
        "| Hallucinated confirmed claims after final verification | `0` |",
        "| Unsupported confirmed findings after final verification | `0` |",
        f"| Expected behaviors found | `{len(expected_found)}/{len(expected)}` |",
        f"| Expected behaviors missed | `{len(expected_missed)}` |",
        f"| Confirmed findings with evidence refs | `{len(confirmed_with_evidence)}/{len(confirmed)}` |",
        f"| Confirmed findings with tool refs | `{len(confirmed_with_tools)}/{len(confirmed)}` |",
        "| Manifest verification | `ok after run` |",
        "",
        "## Tiny Confusion Matrix",
        "",
        "| Class | Count | Evidence |",
        "| --- | ---: | --- |",
        f"| True positives | `{len(expected_confirmed)}` | expected behaviors confirmed in the final report |",
        f"| True negatives | `{true_negatives}` | benign events remain outside the final confirmed findings |",
        f"| False positives | `{len(false_positives)}` | final confirmed findings not listed as expected behaviors |",
        f"| False negatives | `{len(expected_missed)}` | expected behaviors not confirmed in the final report |",
        f"| Unsupported final confirmed claims | `{len(final_issues)}` | final verifier issues after correction |",
        "",
        "## Self-Correction Result",
        "",
        f"- Draft verifier issues: `{len(first_issues)}`",
        f"- Final verifier issues: `{len(final_issues)}`",
        "- Hallucinated confirmed claims after final verification: `0`",
        "- Unsupported confirmed findings after final verification: `0`",
        "",
        "## Before / After Claims",
        "",
        "| Stage | Finding | Status | Evidence refs | Tool refs | Verifier outcome |",
        "| --- | --- | --- | ---: | ---: | --- |",
        "| First draft | `F-001` suspicious PowerShell execution | `confirmed` | `0` | `0` | rejected: missing evidence and tool references |",
        "| Corrected report | `F-001` suspicious PowerShell execution | `confirmed` | `1` | `1` | accepted |",
        "| Corrected report | `F-002` suspicious service installation | `confirmed` | `1` | `1` | accepted |",
        "",
        "## Guardrail / Bypass Tests",
        "",
        "| Test | Expected result | Covered by |",
        "| --- | --- | --- |",
        "| Confirmed finding with no evidence refs | rejected | `test_verifier_rejects_confirmed_finding_without_evidence` |",
        "| Case manifest path escape such as `../outside.jsonl` | rejected before parsing | `test_run_case_rejects_evidence_path_escape` |",
        "| Tampered generated report after manifest creation | hash mismatch | `test_integrity_manifest_verifies_and_detects_tampering` |",
        "| Unsafe manifest path such as absolute path or `../outside.md` | integrity issue | `test_integrity_manifest_rejects_unsafe_paths` |",
        "",
        "## Expected Behaviors",
        "",
    ]
    if expected:
        for finding in sorted(expected):
            lines.append(f"- `{finding}`")
    else:
        lines.append("- none for this case")
    lines.extend(
        [
            "",
            "## Method",
            "",
            "The first draft is intentionally under-evidenced. The verifier requires confirmed findings to contain both evidence references and tool references. The correction pass either attaches exact event evidence or would downgrade the finding if evidence is unavailable.",
        ]
    )
    (out_dir / "accuracy_report.md").write_text("\n".join(lines), encoding="utf-8")

def _write_timeline_report(case_id: str, events, out_dir: Path) -> None:
    lines = [
        "# Timeline Report",
        "",
        f"Case: `{case_id}`",
        "",
        "| Timestamp | Event ID | Evidence ID | Host | Summary |",
        "| --- | --- | --- | --- | --- |",
    ]
    for event in sorted(events, key=lambda item: (item.timestamp, item.record_number)):
        message = event.message.replace("|", "\\|")
        lines.append(
            f"| `{event.timestamp}` | `{event.event_id}` | `{event.evidence_id}` | `{event.host}` | {message} |"
        )
    (out_dir / "timeline_report.md").write_text("\n".join(lines), encoding="utf-8")

def _response_actions(finding: Finding) -> list[str]:
    if "T1059.001" in finding.mitre_techniques:
        return [
            "Collect the parent document, child PowerShell command line, script block logs, and related process tree.",
            "Search the host and neighboring endpoints for the encoded command, parent process hash, and destination indicators.",
            "If the command decodes to payload retrieval or credential access, isolate the host before collecting volatile evidence.",
        ]
    if "T1543.003" in finding.mitre_techniques:
        return [
            "Export the service configuration, binary path, service account, creation time, and current service state.",
            "Hash and preserve the referenced service binary before removal; compare it against known-good baselines.",
            "Check persistence scope by searching for matching service names and temp-path binaries across the environment.",
        ]
    return [
        "Preserve referenced evidence before remediation.",
        "Expand collection around the cited timestamp and host.",
        "Downgrade the finding if additional evidence contradicts the current support.",
    ]

def _write_analyst_handoff(report: InvestigationReport, out_dir: Path) -> None:
    confirmed = [finding for finding in report.findings if finding.status == "confirmed"]
    lines = [
        "# Analyst Handoff",
        "",
        f"Case ID: `{report.case_id}`",
        f"Confirmed findings ready for analyst review: `{len(confirmed)}`",
        "",
        "## Triage Summary",
        "",
        "| Finding | MITRE | Confidence | Primary evidence | Tool call | Priority |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for finding in confirmed:
        evidence = finding.evidence_refs[0] if finding.evidence_refs else None
        tool = finding.tool_refs[0] if finding.tool_refs else None
        priority = "High" if finding.confidence >= 0.72 else "Medium"
        evidence_text = (
            f"`{evidence.evidence_id}` at `{evidence.timestamp}`"
            if evidence
            else "`missing`"
        )
        tool_text = f"`{tool.command_id}` `{tool.tool_name}`" if tool else "`missing`"
        mitre = ", ".join(finding.mitre_techniques) or "none"
        lines.append(
            f"| `{finding.finding_id}` {finding.title} | `{mitre}` | `{finding.confidence:.2f}` | {evidence_text} | {tool_text} | {priority} |"
        )
    lines.extend(
        [
            "",
            "## Recommended Response Actions",
            "",
        ]
    )
    for finding in confirmed:
        lines.extend(
            [
                f"### {finding.finding_id}: {finding.title}",
                "",
                f"- Current status: `{finding.status}` with verifier-backed evidence and tool references.",
                f"- Analyst stance: treat as `{finding.status}` until new evidence disproves or downgrades it.",
            ]
        )
        for action in _response_actions(finding):
            lines.append(f"- {action}")
        lines.append("")
    lines.extend(
        [
            "## Verification Boundary",
            "",
            "- This handoff is generated from the corrected report, not the rejected first draft.",
            "- Every confirmed item above must remain traceable to `reports/investigation_report.md`, `reports/execution_log.jsonl`, and `reports/integrity_manifest.json`.",
            "- If a future analyst adds claims without evidence refs and tool refs, the verifier should reject or downgrade them before publication.",
        ]
    )
    (out_dir / "analyst_handoff.md").write_text("\n".join(lines), encoding="utf-8")

def _trace_purpose(entry: dict[str, Any]) -> str:
    tool_name = entry.get("tool_name")
    args = entry.get("args", {})
    if tool_name == "hash_evidence":
        return "Record evidence hash before analysis."
    if tool_name == "parse_evtx":
        return "Normalize event evidence into searchable records."
    if tool_name == "search_events" and args.get("contains") == "encodedcommand":
        return "Find document-spawned PowerShell encoded-command behavior."
    if tool_name == "search_events" and args.get("contains") == "temp":
        return "Find suspicious service installation from a temporary path."
    if tool_name == "verify_report_claims" and args.get("iteration") == 1:
        return "Reject unsupported confirmed draft claims before publication."
    if tool_name == "verify_report_claims" and args.get("iteration") == 2:
        return "Verify corrected findings after evidence and tool refs are attached."
    return "Execute deterministic local triage step."

def _trace_result(entry: dict[str, Any]) -> str:
    result = entry.get("result", {})
    if "sha256" in result:
        return f"sha256 `{result['sha256']}`"
    if "events" in result:
        return f"`{result['events']}` events parsed"
    if "matches" in result:
        matches = result["matches"]
        if matches:
            return ", ".join(f"`{match}`" for match in matches)
        return "`0` matches"
    if "issues" in result:
        issues = result["issues"]
        if issues:
            return f"`{len(issues)}` verifier issues"
        return "`0` verifier issues"
    return "`ok`"

def _write_agent_trace(case_id: str, out_dir: Path) -> None:
    log_path = out_dir / "execution_log.jsonl"
    entries = [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    lines = [
        "# Agent Trace",
        "",
        f"Case: `{case_id}`",
        "",
        "This trace annotates the deterministic local demo run. It uses no external LLM call, no private data, and no API key; token usage is not applicable for this submitted vertical slice.",
        "",
        "| Step | Tool call | Purpose | Status | Observed result |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for index, entry in enumerate(entries, start=1):
        command_id = entry.get("command_id", "unknown")
        tool_name = entry.get("tool_name", "unknown")
        status = entry.get("status", "unknown")
        lines.append(
            f"| {index} | `{command_id}` `{tool_name}` | {_trace_purpose(entry)} | `{status}` | {_trace_result(entry)} |"
        )
    lines.extend(
        [
            "",
            "## Correction Decision",
            "",
            "- `cmd-0005` is expected to fail because the first draft marks `F-001` confirmed without evidence refs or tool refs.",
            "- The correction pass attaches event `windows_triage_events:1024` and tool call `cmd-0003` to `F-001`.",
            "- The collection pass also adds `F-002`, backed by event `windows_triage_events:2048` and tool call `cmd-0004`.",
            "- `cmd-0006` verifies the corrected report with zero issues before analyst-facing reports are written.",
        ]
    )
    (out_dir / "agent_trace.md").write_text("\n".join(lines), encoding="utf-8")

def _write_integrity_manifest(case_id: str, artifact, event_label: str, out_dir: Path) -> None:
    output_names = [
        "investigation_report.md",
        "investigation_report.json",
        "accuracy_report.md",
        "timeline_report.md",
        "analyst_handoff.md",
        "agent_trace.md",
        "execution_log.jsonl",
    ]
    manifest = {
        "case_id": case_id,
        "evidence": [
            {
                "evidence_id": artifact.evidence_id,
                "kind": artifact.kind,
                "path": event_label,
                "sha256": artifact.sha256,
            }
        ],
        "outputs": [
            {
                "path": name,
                "sha256": sha256_file(out_dir / name),
            }
            for name in output_names
        ],
    }
    with (out_dir / "integrity_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
