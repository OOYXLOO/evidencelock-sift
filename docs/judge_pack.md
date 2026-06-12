# EvidenceLock SIFT Judge Pack

This is the fastest review path for the FIND EVIL! submission.

## One-Sentence Positioning

EvidenceLock SIFT is a verifier-first Protocol SIFT triage boundary: the agent can draft quickly, but a confirmed finding must prove itself with evidence IDs, tool-call IDs, verifier correction, and integrity hashes.

## Two-Minute Review Path

1. Open the static judge hub: [`docs/index.html`](index.html).
2. Watch the embedded demo page: [`docs/demo.html`](demo.html). Upload source: [`docs/demo-video/evidencelock-sift-demo.webm`](demo-video/evidencelock-sift-demo.webm).
3. The official Devpost video field must use a public YouTube, Vimeo, or Youku URL with audio narration; use the upload copy pack: [`docs/video_upload_pack.md`](video_upload_pack.md).
4. Open the 5-slide presentation deck: [`docs/evidencelock-sift-judge-deck.pptx`](evidencelock-sift-judge-deck.pptx).
5. Open the one-minute submission gate pack: [`docs/human_submission_gate.md`](human_submission_gate.md).
6. Check the Stage One preflight: [`docs/stage_one_preflight.md`](stage_one_preflight.md).
7. Open the proof trace: [`docs/proof-card.png`](proof-card.png).
8. Open the accuracy summary: [`docs/accuracy-card.png`](accuracy-card.png).
9. Read the judging criteria scorecard: [`docs/judge_scorecard.md`](judge_scorecard.md).
10. Run the smoke test: `python tools/judge_smoke_test.py`.
11. Check the before/after claim verification table: [`docs/claim_verification_table.md`](claim_verification_table.md).
12. Check the negative-control downgrade: [`docs/fail_closed_negative_control.md`](fail_closed_negative_control.md).
13. Check the SIFT compatibility runbook: [`docs/sift_compatibility_runbook.md`](sift_compatibility_runbook.md).
14. Read the annotated agent trace: [`reports/agent_trace.md`](../reports/agent_trace.md).
15. Read the final report: [`reports/investigation_report.md`](../reports/investigation_report.md).
16. Read the responder handoff: [`reports/analyst_handoff.md`](../reports/analyst_handoff.md).
17. Verify integrity: `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .`

## FIND EVIL Requirements Map

| Requirement | EvidenceLock artifact | Status |
| --- | --- | --- |
| Public repository | <https://github.com/OOYXLOO/evidencelock-sift> | Ready |
| Human submission gate pack | [`docs/human_submission_gate.md`](human_submission_gate.md) | Ready |
| Stage One preflight | [`docs/stage_one_preflight.md`](stage_one_preflight.md) | Ready; final Devpost URL and hosted video URL still require the human gate |
| Demo video | [`docs/demo.html`](demo.html), [`docs/demo-video/evidencelock-sift-demo.webm`](demo-video/evidencelock-sift-demo.webm) | Narrated upload source ready; final Devpost video URL must be public YouTube, Vimeo, or Youku |
| Hosted-video upload pack | [`docs/video_upload_pack.md`](video_upload_pack.md) | Ready; use for the required public video host upload |
| Presentation deck | [`docs/evidencelock-sift-judge-deck.pptx`](evidencelock-sift-judge-deck.pptx) | Ready |
| Architecture diagram | [`docs/architecture.png`](architecture.png), [`docs/architecture.md`](architecture.md) | Ready |
| Dataset description | [`docs/dataset.md`](dataset.md) | Ready |
| Public dataset / benchmark appendix | [`docs/public_dataset_benchmark_appendix.md`](public_dataset_benchmark_appendix.md) | Ready |
| Fail-closed negative control | [`docs/fail_closed_negative_control.md`](fail_closed_negative_control.md) | Ready |
| SIFT compatibility runbook | [`docs/sift_compatibility_runbook.md`](sift_compatibility_runbook.md) | Ready |
| Judging criteria scorecard | [`docs/judge_scorecard.md`](judge_scorecard.md) | Ready |
| Accuracy/evaluation | [`reports/accuracy_report.md`](../reports/accuracy_report.md), [`docs/accuracy_method.md`](accuracy_method.md) | Ready |
| Before/after claim verification | [`docs/claim_verification_table.md`](claim_verification_table.md) | Ready |
| Execution/tool-call log | [`reports/execution_log.jsonl`](../reports/execution_log.jsonl) | Ready |
| Annotated agent trace | [`reports/agent_trace.md`](../reports/agent_trace.md) | Ready |
| Integrity manifest | [`reports/integrity_manifest.json`](../reports/integrity_manifest.json) | Ready |
| Analyst-ready output | [`reports/analyst_handoff.md`](../reports/analyst_handoff.md) | Ready |
| MCP-style tool boundary | [`docs/mcp_tool_schema.json`](mcp_tool_schema.json) | Ready |
| One-command smoke test | [`tools/judge_smoke_test.py`](../tools/judge_smoke_test.py) | Ready |

## Expected Smoke-Test Highlights

`python tools/judge_smoke_test.py` should return `ok: true` only when these proof checks pass:

| Check | Expected value | Why it matters |
| --- | --- | --- |
| `draft_rejected_with_three_issues` | `true` | The first unsafe draft is not accepted as a confirmed incident report. |
| `final_verifier_zero_issues` | `true` | The corrected report has no verifier issues after evidence/tool refs are added. |
| `proof_trace.F-001` | `windows_triage_events:1024` + `cmd-0003 search_events` | PowerShell execution finding is locked to an evidence row and reproducible tool call. |
| `proof_trace.F-002` | `windows_triage_events:2048` + `cmd-0004 search_events` | Service-persistence finding is locked to an evidence row and reproducible tool call. |
| `manifest_ok` | `true` | Evidence and generated reports still match the integrity manifest. |
| `negative_control_downgrades_to_unresolved` | `true` | A no-evidence case downgrades to `unresolved` instead of becoming a false positive. |
| `negative_manifest_ok` | `true` | The negative-control evidence and outputs are also hash-verified. |

## What Judges Should Notice

- The first draft intentionally fails verification because it lacks evidence and tool references.
- The corrected report has 2 confirmed findings, 2/2 expected behaviors found, and 0 final verifier issues.
- The before/after claim table shows exactly what changed between the rejected draft and accepted report.
- `docs/judge_scorecard.md` maps the package to autonomous execution quality, IR accuracy, depth, constraint implementation, audit trail quality, and usability.
- `docs/evidencelock-sift-judge-deck.pptx` gives a 5-slide judge-ready presentation layer without adding any unproven live SIFT claims.
- `tools/judge_smoke_test.py` returns JSON with `ok: true` only when the rejected draft, corrected verifier, manifest check, generated outputs, and exact finding-to-evidence/tool IDs all match expectations.
- The smoke test also requires `negative_control_downgrades_to_unresolved: true` and `negative_manifest_ok: true`, proving no-evidence cases fail closed instead of becoming false positives.
- `docs/sift_compatibility_runbook.md` gives the exact non-claiming path from normalized EVTX exports to SIFT/Sleuth Kit wrapper evidence.
- `reports/agent_trace.md` annotates each tool call and makes clear that the deterministic local demo uses no external LLM call or API key.
- Confirmed finding `F-001` maps to MITRE `T1059.001` and cites event `windows_triage_events:1024` plus tool call `cmd-0003`.
- Confirmed finding `F-002` maps to MITRE `T1543.003` and cites event `windows_triage_events:2048` plus tool call `cmd-0004`.
- `reports/analyst_handoff.md` turns verified findings into response actions, so the output is useful after the proof step.
- `reports/integrity_manifest.json` hashes the input evidence and generated outputs so tampering is visible.

## Reproduce Locally

Linux / SIFT workstation shell:

```bash
git clone https://github.com/OOYXLOO/evidencelock-sift.git
cd evidencelock-sift
export PYTHONPATH=src
python3 -m unittest discover -s tests -v
python3 tools/judge_smoke_test.py
python3 -m evidencelock_sift.cli run-case --case examples/cases/windows_triage_case.json --out reports
python3 -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .
```

Windows PowerShell:

```powershell
git clone https://github.com/OOYXLOO/evidencelock-sift.git
cd evidencelock-sift
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python tools/judge_smoke_test.py
python -m evidencelock_sift.cli run-case --case examples/cases/windows_triage_case.json --out reports
python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .
```

Expected verification result:

```json
{
  "issues": [],
  "ok": true
}
```

## Honest Boundary

This is a narrow EVTX-style vertical slice and a custom MCP-style boundary for SIFT workflows. It does not claim full disk-forensics coverage, public-corpus benchmarking, or live SIFT workstation execution. The public-data extension path is documented in [`docs/public_dataset_benchmark_appendix.md`](public_dataset_benchmark_appendix.md). The point is the trust boundary: if evidence is missing, the correct behavior is to reject or downgrade the finding, not invent certainty.
