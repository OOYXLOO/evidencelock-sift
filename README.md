# EvidenceLock SIFT

EvidenceLock SIFT is a verifier-first DFIR triage agent for the FIND EVIL! hackathon. It is built for Protocol SIFT-style workflows where an AI agent can use incident-response tools, but every confirmed conclusion must remain tied to reproducible evidence, tool-call IDs, and integrity hashes.

In one sentence: it is a verifier-first custom MCP-style boundary for Protocol SIFT triage, not a prompt-only forensic chatbot.

The project does not try to be a broad forensic chatbot. It implements a narrow, auditable loop:

1. Load a case manifest and normalized Windows event evidence.
2. Hash every evidence artifact before analysis.
3. Search events through typed read-only tools.
4. Draft findings.
5. Verify every confirmed claim against evidence IDs and tool calls.
6. Correct unsupported claims or downgrade them to unresolved hypotheses.
7. Emit a structured report, accuracy report, and execution log.

## Why It Matters

Protocol SIFT demonstrates how AI agents can drive SIFT workstation tools through MCP. The risk is that an agent can still write a confident incident report from incomplete or hallucinated evidence. EvidenceLock makes the verifier a hard boundary: a finding cannot stay `confirmed` unless it includes evidence references and reproducible tool references.

## Quick Start

```powershell
git clone https://github.com/OOYXLOO/evidencelock-sift.git
cd evidencelock-sift
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python tools/judge_smoke_test.py
python -m evidencelock_sift.cli run-case --case examples/cases/windows_triage_case.json --out reports
python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .
```

Generated outputs:

- `reports/investigation_report.md`
- `reports/investigation_report.json`
- `reports/accuracy_report.md`
- `reports/timeline_report.md`
- `reports/analyst_handoff.md`
- `reports/agent_trace.md`
- `reports/execution_log.jsonl`
- `reports/integrity_manifest.json`
- `docs/demo-video/evidencelock-sift-demo.webm`

## Protocol SIFT Fit

EvidenceLock is designed to sit beside Protocol SIFT as a custom MCP-style tool boundary. Instead of exposing raw shell commands to the agent, it exposes typed functions such as `list_evidence`, `hash_evidence`, `parse_evtx`, `search_events`, `extract_event_evidence`, and `verify_report_claims`.

The current implementation runs without external dependencies for the demo. On a SIFT workstation it can be extended to call tools such as `EvtxECmd`, `mmls`, `fls`, `istat`, and `icat` through the same typed wrapper pattern.

See `docs/sift_compatibility_runbook.md` for the non-claiming migration path from this public vertical slice to SIFT-derived evidence and Sleuth Kit wrappers.

## Demo Scenario

The included synthetic Windows triage case contains three normalized events:

- A suspicious PowerShell process creation from a document process.
- A suspicious Windows service installation.
- A benign interactive logon.

The agent intentionally starts with an unsupported draft claim. The verifier rejects it because it has no evidence ID. The correction pass searches events, attaches exact event records, and produces confirmed findings only for the two supported behaviors.

## Judge Fast Path

If you only have a few minutes, inspect these artifacts:

- `docs/index.html`: static judge hub for GitHub Pages or local browser review.
- `docs/demo.html`: embedded browser playback page for the silent WebM demo.
- `docs/judging_guide.md`: FIND EVIL judging matrix, proof card, demo path, and limitations.
- `docs/judge_pack.md`: shortest judge path with requirements map, evidence links, and reproduction command.
- `docs/judge_scorecard.md`: direct map from FIND EVIL judging criteria to public evidence.
- `docs/evidencelock-sift-judge-deck.pptx`: editable 5-slide presentation deck for judge review and Devpost supporting links.
- `tools/judge_smoke_test.py`: one-command judge smoke test with exact expected checks, finding-to-evidence/tool proof trace, and negative-control status.
- `docs/fail_closed_negative_control.md`: negative-control case proving unsupported draft claims downgrade to unresolved.
- `docs/sift_compatibility_runbook.md`: non-claiming path for SIFT, EvtxECmd, Sleuth Kit, and Protocol SIFT-style MCP usage.
- `docs/required_components_checklist.md`: final submission checklist for the required FIND EVIL artifacts.
- `docs/proof-card.png`: visual proof trace for finding `F-001`.
- `docs/accuracy-card.png`: visual metrics and guardrail/bypass-test summary.
- `reports/execution_log.jsonl`: command IDs for hashing, parsing, searches, and both verifier passes.
- `reports/agent_trace.md`: annotated step-by-step trace over the execution log.
- `reports/investigation_report.md`: final confirmed findings with evidence and tool references.
- `reports/timeline_report.md`: timestamp-sorted event timeline for fast triage review.
- `reports/analyst_handoff.md`: analyst-ready response actions mapped to MITRE technique, evidence, and tool calls.
- `docs/mcp_tool_schema.json`: typed tool boundary, including `extract_event_evidence` and `verify_report_claims`.
- `reports/integrity_manifest.json`: SHA-256 hashes for the input evidence file and generated outputs.
- `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .`: verifies the evidence and output hashes still match.

## Safety Boundary

- Evidence inputs are read-only.
- Case manifest evidence paths must resolve under the case directory; path escapes such as `../outside.jsonl` are rejected before parsing.
- Output is limited to the chosen reports directory.
- Integrity manifests are verified with relative paths only; absolute paths and path escapes are reported as integrity issues.
- Finding status must be one of `confirmed`, `inferred`, `disproven`, or `unresolved`.
- Confirmed findings require evidence references and tool references.
- Tool failures are recorded in `execution_log.jsonl` and cannot be cited as proof.

## Submission Assets

See:

- `docs/architecture.md`
- `docs/index.html`
- `docs/accuracy-card.png`
- `docs/accuracy-card.svg`
- `docs/architecture.png`
- `docs/architecture.svg`
- `docs/dataset.md`
- `docs/demo_script.md`
- `docs/demo_recording.md`
- `docs/demo.html`
- `docs/demo-recording-page.html`
- `docs/devpost_field_pack.md`
- `docs/devpost_gallery_assets.md`
- `docs/devpost_submission.md`
- `docs/evidencelock-sift-judge-deck.pptx`
- `docs/judging_guide.md`
- `docs/judge_pack.md`
- `docs/judge_scorecard.md`
- `docs/fail_closed_negative_control.md`
- `docs/sift_compatibility_runbook.md`
- `docs/mcp_tool_schema.json`
- `docs/proof-card.png`
- `docs/proof-card.svg`
- `docs/required_components_checklist.md`
- `docs/submission_checklist.md`
- `docs/accuracy_method.md`
- `reports/analyst_handoff.md`
- `reports/agent_trace.md`
