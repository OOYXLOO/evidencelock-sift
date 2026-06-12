from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evidencelock_sift.agent.loop import run_case
from evidencelock_sift.agent.verifier import verify_findings
from evidencelock_sift.integrity import verify_integrity_manifest
from evidencelock_sift.mcp_server import call_tool
from evidencelock_sift.mcp_server import TOOL_SCHEMAS
from evidencelock_sift.schemas import EvidenceRef
from evidencelock_sift.schemas import Finding
from evidencelock_sift.schemas import ToolRef
from evidencelock_sift.tools.evidence import hash_evidence
from evidencelock_sift.tools.evtx import extract_event_evidence
from evidencelock_sift.tools.evtx import parse_events
from evidencelock_sift.tools.evtx import search_events


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples" / "cases" / "windows_triage_case.json"
EVENTS = ROOT / "examples" / "cases" / "windows_triage_events.jsonl"
NEGATIVE_CASE = ROOT / "examples" / "cases" / "windows_negative_case.json"


class EvidenceLockTests(unittest.TestCase):
    def test_hash_evidence_returns_sha256(self) -> None:
        artifact = hash_evidence(EVENTS)
        self.assertTrue(artifact.sha256)
        self.assertEqual(artifact.kind, "jsonl")

    def test_parse_and_search_events(self) -> None:
        events = parse_events(EVENTS)
        matches = search_events(events, event_ids={"4688"}, contains="encodedcommand")
        self.assertEqual(len(events), 3)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].evidence_id, "windows_triage_events:1024")
        self.assertEqual(
            extract_event_evidence(events, "windows_triage_events:1024"),
            matches[0],
        )

    def test_verifier_rejects_confirmed_finding_without_evidence(self) -> None:
        events = parse_events(EVENTS)
        issues = verify_findings(
            [
                Finding(
                    finding_id="F-001",
                    title="Unsupported",
                    status="confirmed",
                    confidence=0.5,
                    summary="No evidence yet",
                )
            ],
            events,
        )
        self.assertTrue(any("no evidence_refs" in issue.message for issue in issues))

    def test_verifier_rejects_forged_tool_reference(self) -> None:
        events = parse_events(EVENTS)
        event = search_events(events, event_ids={"4688"}, contains="encodedcommand")[0]
        finding = Finding(
            finding_id="F-777",
            title="Forged proof trace",
            status="confirmed",
            confidence=0.9,
            summary="This cites a real evidence ID but a tool call that never produced it.",
            evidence_refs=[
                EvidenceRef(
                    evidence_id=event.evidence_id,
                    source_path=event.source_path,
                    record_number=event.record_number,
                    timestamp=event.timestamp,
                )
            ],
            tool_refs=[
                ToolRef(
                    command_id="cmd-9999",
                    tool_name="search_events",
                    args={"event_ids": ["4688"], "contains": "encodedcommand"},
                    status="success",
                )
            ],
        )
        issues = verify_findings(findings=[finding], events=events, execution_log=[])
        self.assertTrue(any("unknown tool command_id cmd-9999" in issue.message for issue in issues))

    def test_run_case_generates_self_corrected_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = run_case(CASE, tmp_path)
            report_md = tmp_path / "investigation_report.md"
            accuracy_md = tmp_path / "accuracy_report.md"
            execution_log = tmp_path / "execution_log.jsonl"
            integrity_manifest = tmp_path / "integrity_manifest.json"
            timeline_report = tmp_path / "timeline_report.md"
            analyst_handoff = tmp_path / "analyst_handoff.md"
            agent_trace = tmp_path / "agent_trace.md"

            self.assertEqual(len(report.findings), 2)
            self.assertEqual(report.verifier_issues, [])
            self.assertTrue(report_md.exists())
            self.assertTrue(accuracy_md.exists())
            self.assertTrue(execution_log.exists())
            self.assertTrue(integrity_manifest.exists())
            self.assertTrue(timeline_report.exists())
            self.assertTrue(analyst_handoff.exists())
            self.assertTrue(agent_trace.exists())
            self.assertIn(
                "Verifier rejected the first draft",
                report_md.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "windows_triage_events:1024",
                timeline_report.read_text(encoding="utf-8"),
            )
            handoff_text = analyst_handoff.read_text(encoding="utf-8")
            self.assertIn("Recommended Response Actions", handoff_text)
            self.assertIn("T1059.001", handoff_text)
            self.assertIn("T1543.003", handoff_text)
            trace_text = agent_trace.read_text(encoding="utf-8")
            self.assertIn("cmd-0005", trace_text)
            self.assertIn("token usage is not applicable", trace_text)
            self.assertIn(
                "Draft verifier issues: `3`",
                accuracy_md.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "| True positives | `2` |",
                accuracy_md.read_text(encoding="utf-8"),
            )
            manifest = json.loads(integrity_manifest.read_text(encoding="utf-8"))
            self.assertEqual(manifest["case_id"], "windows-triage-mini-001")
            self.assertEqual(manifest["evidence"][0]["sha256"], hash_evidence(EVENTS).sha256)
            self.assertIn("investigation_report.md", {entry["path"] for entry in manifest["outputs"]})
            self.assertIn("timeline_report.md", {entry["path"] for entry in manifest["outputs"]})
            self.assertIn("analyst_handoff.md", {entry["path"] for entry in manifest["outputs"]})
            self.assertIn("agent_trace.md", {entry["path"] for entry in manifest["outputs"]})

    def test_run_case_downgrades_unsupported_claim_when_evidence_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = run_case(NEGATIVE_CASE, tmp_path)
            accuracy_md = (tmp_path / "accuracy_report.md").read_text(encoding="utf-8")
            report_md = (tmp_path / "investigation_report.md").read_text(encoding="utf-8")
            agent_trace = (tmp_path / "agent_trace.md").read_text(encoding="utf-8")

            self.assertEqual(report.verifier_issues, [])
            self.assertEqual(len(report.findings), 1)
            finding = report.findings[0]
            self.assertEqual(finding.finding_id, "F-001")
            self.assertEqual(finding.status, "unresolved")
            self.assertEqual(finding.evidence_refs, [])
            self.assertEqual(finding.tool_refs, [])
            self.assertIn("downgraded the claim to unresolved", report_md)
            self.assertIn("| True positives | `0` |", accuracy_md)
            self.assertIn("| True negatives | `1` |", accuracy_md)
            self.assertIn("| False positives | `0` |", accuracy_md)
            self.assertIn("| Unsupported final confirmed claims | `0` |", accuracy_md)
            self.assertIn("`0` verifier issues", agent_trace)

    def test_run_case_rejects_evidence_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            case_dir = tmp_path / "case"
            case_dir.mkdir()
            outside = tmp_path / "outside.jsonl"
            outside.write_text(EVENTS.read_text(encoding="utf-8"), encoding="utf-8")
            case_path = case_dir / "case.json"
            case_path.write_text(
                json.dumps(
                    {
                        "case_id": "escape-demo",
                        "event_evidence": "../outside.jsonl",
                        "expected_findings": [],
                        "title": "Path escape demo",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "path escapes evidence root"):
                run_case(case_path, tmp_path / "reports")

    def test_integrity_manifest_verifies_and_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run_case(CASE, tmp_path)
            manifest_path = tmp_path / "integrity_manifest.json"

            self.assertEqual(verify_integrity_manifest(manifest_path, ROOT), [])

            report_md = tmp_path / "investigation_report.md"
            report_md.write_text(report_md.read_text(encoding="utf-8") + "\nTampered.\n", encoding="utf-8")
            issues = verify_integrity_manifest(manifest_path, ROOT)
            self.assertEqual(len(issues), 1)
            self.assertEqual(issues[0]["kind"], "output")
            self.assertEqual(issues[0]["issue"], "sha256 mismatch")


    def test_integrity_manifest_rejects_unsafe_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run_case(CASE, tmp_path)
            manifest_path = tmp_path / "integrity_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            manifest["outputs"][0]["path"] = "../outside.md"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            issues = verify_integrity_manifest(manifest_path, ROOT)
            self.assertEqual(issues[0]["kind"], "output")
            self.assertEqual(issues[0]["issue"], "path escapes base")

            manifest["outputs"][0]["path"] = str((tmp_path / "outside.md").resolve())
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            issues = verify_integrity_manifest(manifest_path, ROOT)
            self.assertEqual(issues[0]["kind"], "output")
            self.assertEqual(issues[0]["issue"], "absolute paths are not allowed")

    def test_mcp_style_tool_contract_exposes_verifier_boundary(self) -> None:
        tool_names = {tool["name"] for tool in TOOL_SCHEMAS}
        self.assertIn("extract_event_evidence", tool_names)
        self.assertIn("verify_report_claims", tool_names)

        extracted = call_tool(
            "extract_event_evidence",
            {"path": str(EVENTS), "evidence_id": "windows_triage_events:1024"},
        )
        self.assertEqual(extracted["event"]["record_number"], "1024")

        verification = call_tool(
            "verify_report_claims",
            {
                "path": str(EVENTS),
                "findings": [
                    {
                        "confidence": 0.9,
                        "finding_id": "F-009",
                        "status": "confirmed",
                        "summary": "Unsupported claim",
                        "title": "Unsupported claim",
                    }
                ],
            },
        )
        self.assertTrue(verification["issues"])

    def test_judge_pack_links_required_public_artifacts(self) -> None:
        judge_pack = (ROOT / "docs" / "judge_pack.md").read_text(encoding="utf-8")
        judge_hub = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

        required_fragments = [
            "EvidenceLock SIFT Judge Pack",
            "docs/index.html",
            "docs/demo.html",
            "docs/human_submission_gate.md",
            "docs/final_submit_console.html",
            "docs/stage_one_preflight.md",
            "docs/video_upload_pack.md",
            "docs/demo-video/evidencelock-sift-demo.mp4",
            "docs/demo-video/evidencelock-sift-demo.webm",
            "docs/evidencelock-sift-judge-deck.pptx",
            "reports/investigation_report.md",
            "reports/analyst_handoff.md",
            "reports/agent_trace.md",
            "reports/integrity_manifest.json",
            "judge_scorecard.md",
            "tools/judge_smoke_test.py",
            "fail_closed_negative_control.md",
            "sift_compatibility_runbook.md",
            "mcp_tool_schema.json",
            "verify-manifest",
            "T1059.001",
            "T1543.003",
            "Expected Smoke-Test Highlights",
            "draft_rejected_with_three_issues",
            "final_verifier_zero_issues",
            "windows_triage_events:1024",
            "cmd-0003 search_events",
            "windows_triage_events:2048",
            "cmd-0004 search_events",
            "negative_control_downgrades_to_unresolved",
            "YouTube, Vimeo, or Youku",
            "audio narration",
            "export PYTHONPATH=src",
        ]
        for fragment in required_fragments:
            self.assertIn(fragment, judge_pack)
        for path in [
            ROOT / "README.md",
            ROOT / "docs" / "final_submission_operator_runbook.md",
            ROOT / "docs" / "final_submit_console.html",
            ROOT / "docs" / "human_submission_gate.md",
            ROOT / "docs" / "stage_one_preflight.md",
            ROOT / "docs" / "required_components_checklist.md",
            ROOT / "docs" / "video_upload_pack.md",
            ROOT / "docs" / "demo_recording.md",
        ]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("YouTube", text, path.as_posix())
            self.assertIn("Vimeo", text, path.as_posix())
            self.assertIn("Youku", text, path.as_posix())
            self.assertNotIn("silent demo", text.lower(), path.as_posix())
        for fragment in [
            "EvidenceLock SIFT Judge Hub",
            "Verifier-first Protocol SIFT triage demo",
            "og:image",
            "demo.html",
            "evidencelock-sift-judge-deck.pptx",
            "judge_scorecard.md",
            "smoke_proof.md",
            "judge_smoke_test.py",
            "agent_trace.md",
            "human_submission_gate.md",
            "stage_one_preflight.md",
            "video_upload_pack.md",
            "fail_closed_negative_control.md",
            "sift_compatibility_runbook.md",
            "claim_verification_table.md",
            "public_dataset_benchmark_appendix.md",
            "raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/execution_log.jsonl",
            "raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/integrity_manifest.json",
            "github.com/OOYXLOO/evidencelock-sift/blob/main/reports/investigation_report.md",
            "exact finding proof traces",
            "proof_trace",
            "proof-card.png",
            "accuracy-card.png",
            "Smoke-Test Proof",
            "Smoke Proof",
            "Submission Record",
            "Final Submit Console",
            "final_submit_console.html",
            "Stage One Preflight",
            "Submitted on Devpost",
            "Hosted Video Live",
            "Honest scope",
            "draft is rejected",
            "negative_control_downgrades_to_unresolved: true",
        ]:
            self.assertIn(fragment, judge_hub)
        self.assertNotIn("../reports/", judge_hub)
        self.assertTrue((ROOT / "docs" / "demo.html").is_file())
        self.assertTrue((ROOT / "docs" / "human_submission_gate.md").is_file())
        self.assertTrue((ROOT / "docs" / "final_submit_console.html").is_file())
        self.assertTrue((ROOT / "docs" / "stage_one_preflight.md").is_file())
        self.assertTrue((ROOT / "docs" / "video_upload_pack.md").is_file())
        self.assertTrue((ROOT / "docs" / "demo-video" / "evidencelock-sift-demo.mp4").is_file())
        self.assertTrue((ROOT / "tools" / "record_demo_mp4.mjs").is_file())
        self.assertTrue((ROOT / "docs" / "evidencelock-sift-judge-deck.pptx").is_file())

    def test_judge_smoke_test_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "judge_smoke_test.py")],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertTrue(payload["checks"]["manifest_ok"])
        self.assertTrue(payload["checks"]["agent_trace_hashed"])
        self.assertTrue(payload["checks"]["f001_trace_matches_expected_ids"])
        self.assertTrue(payload["checks"]["f002_trace_matches_expected_ids"])
        self.assertTrue(payload["checks"]["negative_manifest_ok"])
        self.assertTrue(payload["checks"]["negative_control_downgrades_to_unresolved"])
        self.assertEqual(
            payload["proof_trace"]["F-001"]["evidence_ids"],
            ["windows_triage_events:1024"],
        )
        self.assertEqual(payload["proof_trace"]["F-001"]["tool_call_ids"], ["cmd-0003"])
        self.assertEqual(payload["negative_control"]["status"], "unresolved")
        self.assertEqual(payload["negative_control"]["evidence_ids"], [])
        self.assertEqual(payload["negative_control"]["tool_call_ids"], [])

if __name__ == "__main__":
    unittest.main()
