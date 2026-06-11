# FIND EVIL Judging Guide

EvidenceLock SIFT is designed as verifier-first DFIR automation: the agent can move quickly, but a confirmed finding must prove itself with evidence references, tool-call references, and report integrity hashes.

## Judging Matrix

| FIND EVIL signal | EvidenceLock artifact |
| --- | --- |
| Autonomous execution | `src/evidencelock_sift/agent/loop.py` runs the full plan, collect, draft, verify, correct, and report loop with one command. |
| Incident-response accuracy | `reports/accuracy_report.md` shows the first verifier failure and the final zero-issue verification state. |
| Fast triage review | `reports/timeline_report.md` gives a timestamp-sorted view of the suspicious process, service install, and benign logon events. |
| Analyst handoff quality | `reports/analyst_handoff.md` maps confirmed findings to MITRE techniques, evidence IDs, tool-call IDs, priority, and response actions. |
| Constraint enforcement | `src/evidencelock_sift/agent/verifier.py` rejects confirmed findings without evidence/tool references; `run_case` rejects case-manifest evidence paths that escape the case directory. |
| Typed tool boundary | `docs/mcp_tool_schema.json` exposes the MCP-style tool contract, including `extract_event_evidence` and `verify_report_claims`. |
| Audit trail quality | `reports/execution_log.jsonl` records evidence hashing, parsing, searches, and both verifier iterations with command IDs. |
| Chain of custody | `reports/integrity_manifest.json` records the input evidence hash and hashes of generated reports/logs. |
| Tamper check | `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .` verifies the hashes still match and rejects unsafe absolute or escaping manifest paths. |
| Usability | `README.md` includes a standard-library quickstart and the demo uses a small reproducible Windows triage case. |
| Fast visual review | `docs/proof-card.svg` gives a one-screen trace from finding to evidence, tool call, verifier correction, and integrity hash; `docs/accuracy-card.svg` summarizes metrics and bypass tests. |

## Proof Card

Finding `F-001` is the best quick trace for judges:

- Claim: suspicious PowerShell encoded-command execution from a document process.
- Report location: `reports/investigation_report.md`, finding `F-001`.
- Evidence reference: `windows_triage_events:1024`, record `1024`, timestamp `2026-06-01T10:04:31Z`.
- Tool reference: `cmd-0003`, `search_events`, args `{"contains": "encodedcommand", "event_ids": ["4688"]}`.
- Audit log: `reports/execution_log.jsonl` records `cmd-0003` returning `windows_triage_events:1024`.
- Self-correction: `cmd-0005` rejects the first draft because it has no evidence or tool references; `cmd-0006` verifies the corrected report with zero issues.
- Integrity check: `reports/integrity_manifest.json` records the SHA-256 of the evidence file and generated outputs.

## Demo Video Plan

1. Open with the risk: AI DFIR is fast, but unverified findings can be dangerous.
2. Run `python -m evidencelock_sift.cli run-case --case examples/cases/windows_triage_case.json --out reports`.
3. Show `docs/proof-card.svg`: one confirmed finding traced to evidence, command, verifier result, and hash.
4. Show `docs/accuracy-card.svg`: 3 draft verifier issues, 0 final verifier issues, 2/2 expected behaviors, and 4 bypass checks.
5. Show `reports/timeline_report.md`: timestamp-sorted event triage.
6. Show `reports/analyst_handoff.md`: MITRE mapping, priority, and analyst response actions.
7. Show `execution_log.jsonl`: hash, parse, search, failed verifier pass, successful verifier pass.
8. Show `investigation_report.md`: each confirmed finding has evidence and tool-call references.
9. Show `integrity_manifest.json`: input and output hashes make tampering visible.
10. Run `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .`.
11. Close with `python -m unittest discover -s tests -v`.

## Limitations and Failure Modes

- The included data is a synthetic normalized Windows mini-case, not a full public disk image.
- The demo path focuses on EVTX-style event triage; SIFT/Sleuth Kit wrappers are included as an extension pattern, not a full disk-forensics pipeline.
- The verifier proves report support, not absolute incident truth. If evidence is missing, the correct behavior is to downgrade or reject the finding rather than invent certainty.
- The project intentionally chooses a narrow vertical slice because traceability and correctness matter more than a broad chatbot surface for this challenge.
