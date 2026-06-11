# EvidenceLock SIFT

EvidenceLock SIFT is a defensive DFIR agent pattern for the FIND EVIL! hackathon. It is built for Protocol SIFT-style workflows where an AI agent can use incident-response tools, but every conclusion must remain tied to reproducible evidence.

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
python -m evidencelock_sift.cli run-case --case examples/cases/windows_triage_case.json --out reports
```

Generated outputs:

- `reports/investigation_report.md`
- `reports/investigation_report.json`
- `reports/accuracy_report.md`
- `reports/execution_log.jsonl`
- `docs/demo-video/evidencelock-sift-demo.webm`

## Protocol SIFT Fit

EvidenceLock is designed to sit beside Protocol SIFT as a custom MCP-style tool boundary. Instead of exposing raw shell commands to the agent, it exposes typed functions such as `list_evidence`, `hash_evidence`, `parse_evtx`, `search_events`, `extract_event_evidence`, and `verify_report_claims`.

The current implementation runs without external dependencies for the demo. On a SIFT workstation it can be extended to call tools such as `EvtxECmd`, `mmls`, `fls`, `istat`, and `icat` through the same typed wrapper pattern.

## Demo Scenario

The included synthetic Windows triage case contains three normalized events:

- A suspicious PowerShell process creation from a document process.
- A suspicious Windows service installation.
- A benign interactive logon.

The agent intentionally starts with an unsupported draft claim. The verifier rejects it because it has no evidence ID. The correction pass searches events, attaches exact event records, and produces confirmed findings only for the two supported behaviors.

## Safety Boundary

- Evidence inputs are read-only.
- Output is limited to the chosen reports directory.
- Finding status must be one of `confirmed`, `inferred`, `disproven`, or `unresolved`.
- Confirmed findings require evidence references and tool references.
- Tool failures are recorded in `execution_log.jsonl` and cannot be cited as proof.

## Submission Assets

See:

- `docs/architecture.md`
- `docs/architecture.svg`
- `docs/dataset.md`
- `docs/demo_script.md`
- `docs/demo_recording.md`
- `docs/demo-recording-page.html`
- `docs/accuracy_method.md`
