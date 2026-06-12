# Mini Windows EVTX triage with self-correction

Case ID: `windows-triage-mini-001`
Verifier iterations: `2`
Final verifier issues: `0`

## Findings

### F-001: Suspicious PowerShell execution

- Status: `confirmed`
- Confidence: `0.70`
- MITRE: `T1059.001`
- Summary: A document-spawned PowerShell process appears to run an encoded command.

Evidence:
- `windows_triage_events:1024` record `1024` at `2026-06-01T10:04:31Z` from `examples/cases/windows_triage_events.jsonl`
  - Key fields:
    - `event_id`: `4688`
    - `message`: `A new process has been created.`
    - `tags`: `['process_creation', 'powershell', 'T1059.001']`
    - `Image`: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
    - `CommandLine`: `powershell.exe -NoProfile -EncodedCommand SQBFAFgA`
    - `ParentImage`: `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`
    - `User`: `ACME\analyst`

Tool calls:
- `cmd-0003` `search_events` args `{"contains": "encodedcommand", "event_ids": ["4688"]}`

Correction notes:
- Verifier rejected the first draft because it lacked evidence_refs; correction attached the exact process-creation event.

### F-002: Suspicious service installation

- Status: `confirmed`
- Confidence: `0.74`
- MITRE: `T1543.003`
- Summary: A service was installed with an executable path under a temporary directory.

Evidence:
- `windows_triage_events:2048` record `2048` at `2026-06-01T10:07:09Z` from `examples/cases/windows_triage_events.jsonl`
  - Key fields:
    - `event_id`: `7045`
    - `message`: `A service was installed in the system.`
    - `tags`: `['service_install', 'persistence', 'T1543.003']`
    - `ServiceName`: `WinUpdateSvc`
    - `ImagePath`: `C:\Users\Public\Temp\winupdate.exe`
    - `AccountName`: `LocalSystem`

Tool calls:
- `cmd-0004` `search_events` args `{"contains": "temp", "event_ids": ["7045"]}`

Correction notes:
- Added after the collection pass found a service-installation event with a suspicious image path.
