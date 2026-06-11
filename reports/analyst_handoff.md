# Analyst Handoff

Case ID: `windows-triage-mini-001`
Confirmed findings ready for analyst review: `2`

## Triage Summary

| Finding | MITRE | Confidence | Primary evidence | Tool call | Priority |
| --- | --- | ---: | --- | --- | --- |
| `F-001` Suspicious PowerShell execution | `T1059.001` | `0.70` | `windows_triage_events:1024` at `2026-06-01T10:04:31Z` | `cmd-0003` `search_events` | Medium |
| `F-002` Suspicious service installation | `T1543.003` | `0.74` | `windows_triage_events:2048` at `2026-06-01T10:07:09Z` | `cmd-0004` `search_events` | High |

## Recommended Response Actions

### F-001: Suspicious PowerShell execution

- Current status: `confirmed` with verifier-backed evidence and tool references.
- Analyst stance: treat as `confirmed` until new evidence disproves or downgrades it.
- Collect the parent document, child PowerShell command line, script block logs, and related process tree.
- Search the host and neighboring endpoints for the encoded command, parent process hash, and destination indicators.
- If the command decodes to payload retrieval or credential access, isolate the host before collecting volatile evidence.

### F-002: Suspicious service installation

- Current status: `confirmed` with verifier-backed evidence and tool references.
- Analyst stance: treat as `confirmed` until new evidence disproves or downgrades it.
- Export the service configuration, binary path, service account, creation time, and current service state.
- Hash and preserve the referenced service binary before removal; compare it against known-good baselines.
- Check persistence scope by searching for matching service names and temp-path binaries across the environment.

## Verification Boundary

- This handoff is generated from the corrected report, not the rejected first draft.
- Every confirmed item above must remain traceable to `reports/investigation_report.md`, `reports/execution_log.jsonl`, and `reports/integrity_manifest.json`.
- If a future analyst adds claims without evidence refs and tool refs, the verifier should reject or downgrade them before publication.