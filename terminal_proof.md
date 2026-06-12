# EvidenceLock SIFT Terminal Proof

Captured: 2026-06-13

Purpose: give judges a public terminal-style proof path without requiring an account, API key, private incident log, or live SIFT workstation. This complements the hosted demo video by showing the exact command outputs that verify the submitted vertical slice.

## Commands

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python tools/judge_smoke_test.py
python -m evidencelock_sift.cli verify-manifest --manifest reports\integrity_manifest.json --repo-root .
python -m compileall -q src tests tools
```

## Observed Results

| Command | Result | Judge signal |
| --- | --- | --- |
| `python -m unittest discover -s tests -v` | `Ran 15 tests ... OK` | Unit tests cover parser/search behavior, verifier rejection, forged proof rejection, negative control, manifest tamper detection, public artifact links, and judge smoke. |
| `python tools/judge_smoke_test.py` | JSON payload with `"ok": true` | The rejected draft, corrected proof trace, manifest check, and negative control all pass together. |
| `python -m evidencelock_sift.cli verify-manifest --manifest reports\integrity_manifest.json --repo-root .` | `{ "issues": [], "ok": true }` | Checked-in evidence and generated outputs still match the SHA-256 manifest. |
| `python -m compileall -q src tests tools` | exit code `0` | Public Python sources compile. |

## Smoke Output Highlights

```json
{
  "case_id": "windows-triage-mini-001",
  "checks": {
    "draft_rejected_with_three_issues": true,
    "final_verifier_zero_issues": true,
    "proof_trace_tool_results_match": true,
    "manifest_ok": true,
    "negative_control_downgrades_to_unresolved": true,
    "negative_manifest_ok": true
  },
  "proof_trace": {
    "F-001": {
      "status": "confirmed",
      "evidence_ids": ["windows_triage_events:1024"],
      "tool_call_ids": ["cmd-0003"],
      "tool_names": ["search_events"]
    },
    "F-002": {
      "status": "confirmed",
      "evidence_ids": ["windows_triage_events:2048"],
      "tool_call_ids": ["cmd-0004"],
      "tool_names": ["search_events"]
    }
  },
  "negative_control": {
    "case_id": "windows-negative-mini-001",
    "finding_id": "F-001",
    "status": "unresolved",
    "evidence_ids": [],
    "tool_call_ids": []
  },
  "ok": true
}
```

## What This Proves

- The verifier rejects an unsupported confirmed draft before it reaches the final report.
- The corrected findings cite exact evidence IDs and exact successful tool-call IDs.
- `proof_trace_tool_results_match: true` means the cited commands actually produced the cited evidence IDs.
- The negative control downgrades an unsupported claim to `unresolved`, with no evidence refs and no tool refs.
- The checked-in report set verifies against `reports/integrity_manifest.json`.

## Honest Boundary

This is public terminal evidence for a synthetic Windows EVTX-style mini-case. It does not claim live victim data, full-disk SIFT workstation execution, public-corpus benchmarking, or endpoint containment. The SIFT migration path remains documented in `docs/sift_compatibility_runbook.md`.
