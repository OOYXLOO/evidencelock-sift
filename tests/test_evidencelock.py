from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evidencelock_sift.agent.loop import run_case
from evidencelock_sift.agent.verifier import verify_findings
from evidencelock_sift.schemas import Finding
from evidencelock_sift.tools.evidence import hash_evidence
from evidencelock_sift.tools.evtx import parse_events
from evidencelock_sift.tools.evtx import search_events


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples" / "cases" / "windows_triage_case.json"
EVENTS = ROOT / "examples" / "cases" / "windows_triage_events.jsonl"


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

    def test_run_case_generates_self_corrected_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = run_case(CASE, tmp_path)
            report_md = tmp_path / "investigation_report.md"
            accuracy_md = tmp_path / "accuracy_report.md"
            execution_log = tmp_path / "execution_log.jsonl"
            integrity_manifest = tmp_path / "integrity_manifest.json"

            self.assertEqual(len(report.findings), 2)
            self.assertEqual(report.verifier_issues, [])
            self.assertTrue(report_md.exists())
            self.assertTrue(accuracy_md.exists())
            self.assertTrue(execution_log.exists())
            self.assertTrue(integrity_manifest.exists())
            self.assertIn(
                "Verifier rejected the first draft",
                report_md.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Draft verifier issues: `3`",
                accuracy_md.read_text(encoding="utf-8"),
            )
            manifest = json.loads(integrity_manifest.read_text(encoding="utf-8"))
            self.assertEqual(manifest["case_id"], "windows-triage-mini-001")
            self.assertEqual(manifest["evidence"][0]["sha256"], hash_evidence(EVENTS).sha256)
            self.assertIn("investigation_report.md", {entry["path"] for entry in manifest["outputs"]})


if __name__ == "__main__":
    unittest.main()
