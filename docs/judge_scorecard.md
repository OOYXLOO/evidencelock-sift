# EvidenceLock SIFT Judge Scorecard

This scorecard maps the public EvidenceLock package to the FIND EVIL judging criteria. It is designed as a fast pre-read before opening the full reports.

## Criteria Map

| FIND EVIL criterion | EvidenceLock answer | Primary proof |
| --- | --- | --- |
| Autonomous execution quality | One command runs the plan, collect, draft, verify, correct, and report loop. The first draft fails closed, then the corrected pass reaches zero verifier issues. | `reports/execution_log.jsonl`; `reports/accuracy_report.md` |
| IR accuracy | Confirmed findings are distinguished from unsupported claims. The final report keeps 2/2 expected behaviors and 0 final verifier issues. | `reports/investigation_report.md`; `docs/claim_verification_table.md` |
| Breadth and depth of analysis | The demo chooses depth over breadth: process creation, service-installation, benign-logon contrast, timeline ordering, MITRE mapping, and analyst handoff are all traced end to end. | `reports/timeline_report.md`; `reports/analyst_handoff.md` |
| Constraint implementation | Guardrails are architectural: typed tools, read-only evidence handling, verifier enforcement, path-escape rejection, and manifest path checks. | `docs/mcp_tool_schema.json`; `tests/test_evidencelock.py` |
| Audit trail quality | Every confirmed finding cites evidence IDs and tool-call IDs, and every generated report is tied to a SHA-256 integrity manifest. | `reports/execution_log.jsonl`; `reports/integrity_manifest.json` |
| Usability and documentation | Judges get a static hub, a two-minute judge pack, a one-command smoke test, gallery assets, and Devpost-ready field text. | `docs/index.html`; `docs/judge_pack.md`; `tools/judge_smoke_test.py` |

## Fast Verification Signals

- First verifier pass rejects 3 unsafe draft issues.
- Final verifier pass reports 0 issues.
- The report finds both expected suspicious behaviors.
- Confirmed finding `F-001` maps to event `windows_triage_events:1024` and tool call `cmd-0003`.
- Confirmed finding `F-002` maps to event `windows_triage_events:2048` and tool call `cmd-0004`.
- `verify-manifest` returns `{"ok": true}` for the published report set.
- `tools/judge_smoke_test.py` returns `{"ok": true}` only after checking the rejected draft, corrected verifier, generated trace, and manifest.
- The smoke test includes a negative-control case where unsupported `F-001` is downgraded to `unresolved`.
- `reports/agent_trace.md` annotates each execution-log tool call without claiming external LLM/API usage.
- Regression tests cover unsupported confirmed claims, evidence path escapes, tampered outputs, unsafe manifest paths, and MCP-style verifier tools.

## Honest Boundary

EvidenceLock currently demonstrates a narrow normalized Windows EVTX-style vertical slice and a custom MCP-style boundary for SIFT workflows. It does not claim live SIFT workstation execution, full disk-forensics coverage, real victim data, or endpoint containment. That boundary is intentional: the submitted value is a tested trust boundary that prevents unsupported confirmed findings from reaching an analyst-facing report.
