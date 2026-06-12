from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidencelock_sift.agent.loop import run_case
from evidencelock_sift.integrity import verify_integrity_manifest


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _finding_proof(finding) -> dict:
    return {
        "status": finding.status,
        "evidence_ids": [ref.evidence_id for ref in finding.evidence_refs],
        "tool_call_ids": [ref.command_id for ref in finding.tool_refs],
        "tool_names": [ref.tool_name for ref in finding.tool_refs],
    }


def main() -> int:
    case_path = ROOT / "examples" / "cases" / "windows_triage_case.json"
    negative_case_path = ROOT / "examples" / "cases" / "windows_negative_case.json"
    with tempfile.TemporaryDirectory(prefix="evidencelock-judge-") as tmp:
        tmp_path = Path(tmp)
        out_dir = tmp_path / "reports"
        negative_out_dir = tmp_path / "negative-reports"
        report = run_case(case_path, out_dir)
        negative_report = run_case(negative_case_path, negative_out_dir)
        manifest_path = out_dir / "integrity_manifest.json"
        manifest_issues = verify_integrity_manifest(manifest_path, ROOT)
        execution_log = _load_jsonl(out_dir / "execution_log.jsonl")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        negative_manifest_issues = verify_integrity_manifest(
            negative_out_dir / "integrity_manifest.json",
            ROOT,
        )

        first_verifier = next(entry for entry in execution_log if entry["tool_name"] == "verify_report_claims" and entry["args"]["iteration"] == 1)
        final_verifier = next(entry for entry in execution_log if entry["tool_name"] == "verify_report_claims" and entry["args"]["iteration"] == 2)
        output_names = {entry["path"] for entry in manifest["outputs"]}
        finding_ids = {finding.finding_id for finding in report.findings}
        proof_trace = {finding.finding_id: _finding_proof(finding) for finding in report.findings}
        log_by_command = {entry["command_id"]: entry for entry in execution_log}
        negative_finding = negative_report.findings[0]
        expected_proof_results = {
            "F-001": ("cmd-0003", "search_events", ["windows_triage_events:1024"]),
            "F-002": ("cmd-0004", "search_events", ["windows_triage_events:2048"]),
        }
        proof_trace_tool_results_match = all(
            proof_trace.get(finding_id, {}).get("tool_call_ids") == [command_id]
            and log_by_command.get(command_id, {}).get("tool_name") == tool_name
            and log_by_command.get(command_id, {}).get("status") == "success"
            and log_by_command.get(command_id, {}).get("result", {}).get("matches") == evidence_ids
            and proof_trace.get(finding_id, {}).get("evidence_ids") == evidence_ids
            for finding_id, (command_id, tool_name, evidence_ids) in expected_proof_results.items()
        )

        checks = {
            "two_confirmed_findings": len(report.findings) == 2 and finding_ids == {"F-001", "F-002"},
            "f001_trace_matches_expected_ids": proof_trace.get("F-001") == {
                "status": "confirmed",
                "evidence_ids": ["windows_triage_events:1024"],
                "tool_call_ids": ["cmd-0003"],
                "tool_names": ["search_events"],
            },
            "f002_trace_matches_expected_ids": proof_trace.get("F-002") == {
                "status": "confirmed",
                "evidence_ids": ["windows_triage_events:2048"],
                "tool_call_ids": ["cmd-0004"],
                "tool_names": ["search_events"],
            },
            "draft_rejected_with_three_issues": first_verifier["status"] == "failed" and len(first_verifier["result"]["issues"]) == 3,
            "final_verifier_zero_issues": final_verifier["status"] == "success" and final_verifier["result"]["issues"] == [],
            "proof_trace_tool_results_match": proof_trace_tool_results_match,
            "manifest_ok": manifest_issues == [],
            "negative_manifest_ok": negative_manifest_issues == [],
            "agent_trace_hashed": "agent_trace.md" in output_names,
            "accuracy_report_hashed": "accuracy_report.md" in output_names,
            "negative_control_downgrades_to_unresolved": (
                len(negative_report.findings) == 1
                and negative_finding.finding_id == "F-001"
                and negative_finding.status == "unresolved"
                and not negative_finding.evidence_refs
                and not negative_finding.tool_refs
                and negative_report.verifier_issues == []
                and negative_manifest_issues == []
            ),
        }
        ok = all(checks.values())
        result = {
            "ok": ok,
            "case_id": report.case_id,
            "checks": checks,
            "manifest_issues": manifest_issues,
            "negative_control": {
                "case_id": negative_report.case_id,
                "finding_id": negative_finding.finding_id,
                "status": negative_finding.status,
                "evidence_ids": [ref.evidence_id for ref in negative_finding.evidence_refs],
                "tool_call_ids": [ref.command_id for ref in negative_finding.tool_refs],
                "manifest_issues": negative_manifest_issues,
            },
            "proof_trace": proof_trace,
            "expected_output_files": sorted(output_names),
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
