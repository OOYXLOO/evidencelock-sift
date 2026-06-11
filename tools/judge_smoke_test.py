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


def main() -> int:
    case_path = ROOT / "examples" / "cases" / "windows_triage_case.json"
    with tempfile.TemporaryDirectory(prefix="evidencelock-judge-") as tmp:
        out_dir = Path(tmp) / "reports"
        report = run_case(case_path, out_dir)
        manifest_path = out_dir / "integrity_manifest.json"
        manifest_issues = verify_integrity_manifest(manifest_path, ROOT)
        execution_log = _load_jsonl(out_dir / "execution_log.jsonl")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        first_verifier = next(entry for entry in execution_log if entry["tool_name"] == "verify_report_claims" and entry["args"]["iteration"] == 1)
        final_verifier = next(entry for entry in execution_log if entry["tool_name"] == "verify_report_claims" and entry["args"]["iteration"] == 2)
        output_names = {entry["path"] for entry in manifest["outputs"]}
        finding_ids = {finding.finding_id for finding in report.findings}

        checks = {
            "two_confirmed_findings": len(report.findings) == 2 and finding_ids == {"F-001", "F-002"},
            "draft_rejected_with_three_issues": first_verifier["status"] == "failed" and len(first_verifier["result"]["issues"]) == 3,
            "final_verifier_zero_issues": final_verifier["status"] == "success" and final_verifier["result"]["issues"] == [],
            "manifest_ok": manifest_issues == [],
            "agent_trace_hashed": "agent_trace.md" in output_names,
            "accuracy_report_hashed": "accuracy_report.md" in output_names,
        }
        ok = all(checks.values())
        result = {
            "ok": ok,
            "case_id": report.case_id,
            "checks": checks,
            "manifest_issues": manifest_issues,
            "expected_output_files": sorted(output_names),
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
