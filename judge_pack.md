# EvidenceLock SIFT Judge Pack

This is the fastest review path for the FIND EVIL! submission.

## One-Sentence Positioning

EvidenceLock SIFT is a verifier-first Protocol SIFT triage boundary: the agent can draft quickly, but a confirmed finding must prove itself with evidence IDs, tool-call IDs, verifier correction, and integrity hashes.

## Two-Minute Review Path

1. Open the static judge hub: [`docs/index.html`](index.html).
2. Watch or skim the demo asset: [`docs/demo-video/evidencelock-sift-demo.webm`](demo-video/evidencelock-sift-demo.webm).
3. Open the proof trace: [`docs/proof-card.png`](proof-card.png).
4. Open the accuracy summary: [`docs/accuracy-card.png`](accuracy-card.png).
5. Read the judging criteria scorecard: [`docs/judge_scorecard.md`](judge_scorecard.md).
6. Check the before/after claim verification table: [`docs/claim_verification_table.md`](claim_verification_table.md).
7. Read the final report: [`reports/investigation_report.md`](../reports/investigation_report.md).
8. Read the responder handoff: [`reports/analyst_handoff.md`](../reports/analyst_handoff.md).
9. Verify integrity: `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .`

## FIND EVIL Requirements Map

| Requirement | EvidenceLock artifact | Status |
| --- | --- | --- |
| Public repository | <https://github.com/OOYXLOO/evidencelock-sift> | Ready |
| Demo video | [`docs/demo-video/evidencelock-sift-demo.webm`](demo-video/evidencelock-sift-demo.webm) | Ready |
| Architecture diagram | [`docs/architecture.png`](architecture.png), [`docs/architecture.md`](architecture.md) | Ready |
| Dataset description | [`docs/dataset.md`](dataset.md) | Ready |
| Public dataset / benchmark appendix | [`docs/public_dataset_benchmark_appendix.md`](public_dataset_benchmark_appendix.md) | Ready |
| Judging criteria scorecard | [`docs/judge_scorecard.md`](judge_scorecard.md) | Ready |
| Accuracy/evaluation | [`reports/accuracy_report.md`](../reports/accuracy_report.md), [`docs/accuracy_method.md`](accuracy_method.md) | Ready |
| Before/after claim verification | [`docs/claim_verification_table.md`](claim_verification_table.md) | Ready |
| Execution/tool-call log | [`reports/execution_log.jsonl`](../reports/execution_log.jsonl) | Ready |
| Integrity manifest | [`reports/integrity_manifest.json`](../reports/integrity_manifest.json) | Ready |
| Analyst-ready output | [`reports/analyst_handoff.md`](../reports/analyst_handoff.md) | Ready |
| MCP-style tool boundary | [`docs/mcp_tool_schema.json`](mcp_tool_schema.json) | Ready |

## What Judges Should Notice

- The first draft intentionally fails verification because it lacks evidence and tool references.
- The corrected report has 2 confirmed findings, 2/2 expected behaviors found, and 0 final verifier issues.
- The before/after claim table shows exactly what changed between the rejected draft and accepted report.
- `docs/judge_scorecard.md` maps the package to autonomous execution quality, IR accuracy, depth, constraint implementation, audit trail quality, and usability.
- Confirmed finding `F-001` maps to MITRE `T1059.001` and cites event `windows_triage_events:1024` plus tool call `cmd-0003`.
- Confirmed finding `F-002` maps to MITRE `T1543.003` and cites event `windows_triage_events:2048` plus tool call `cmd-0004`.
- `reports/analyst_handoff.md` turns verified findings into response actions, so the output is useful after the proof step.
- `reports/integrity_manifest.json` hashes the input evidence and generated outputs so tampering is visible.

## Reproduce Locally

```powershell
git clone https://github.com/OOYXLOO/evidencelock-sift.git
cd evidencelock-sift
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
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
