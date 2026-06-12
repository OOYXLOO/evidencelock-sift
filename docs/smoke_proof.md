# EvidenceLock SIFT Smoke Proof

This is a checked-in snapshot of the judge smoke test for reviewers who want proof signals before running code.

Regenerate after report, evidence, or verifier changes:

```powershell
$env:PYTHONPATH="src"
python tools/judge_smoke_test.py
```

Linux / SIFT workstation equivalent:

```bash
export PYTHONPATH=src
python3 tools/judge_smoke_test.py
```

## Snapshot

Local verification on 2026-06-13 returned `ok: true`.

| Check | Result |
| --- | --- |
| `two_confirmed_findings` | `true` |
| `draft_rejected_with_three_issues` | `true` |
| `final_verifier_zero_issues` | `true` |
| `proof_trace_tool_results_match` | `true` |
| `manifest_ok` | `true` |
| `negative_control_downgrades_to_unresolved` | `true` |
| `negative_manifest_ok` | `true` |
| `accuracy_report_hashed` | `true` |
| `agent_trace_hashed` | `true` |

## Proof Trace

| Finding | Status | Evidence ID | Tool-call ID | Tool |
| --- | --- | --- | --- | --- |
| `F-001` | `confirmed` | `windows_triage_events:1024` | `cmd-0003` | `search_events` |
| `F-002` | `confirmed` | `windows_triage_events:2048` | `cmd-0004` | `search_events` |

Verifier invariant: a confirmed finding can only use a proof trace when the cited command ID exists, the tool name and args match, the tool status is `success`, and the cited evidence ID appears in that successful tool result.

## Negative Control

| Case | Finding | Status | Evidence IDs | Tool-call IDs |
| --- | --- | --- | --- | --- |
| `windows-negative-mini-001` | `F-001` | `unresolved` | none | none |

This proves the demo does not turn a no-evidence case into a confirmed false positive.

## Boundaries

- No account, API key, private log, or real victim data is required for this smoke path.
- The public demo is a synthetic Windows EVTX-style mini-case, not a claim of live full-disk SIFT execution.
- The official submitted video is hosted on Vimeo; FIND EVIL rules allow public YouTube, Vimeo, or Youku videos with audio narration.
