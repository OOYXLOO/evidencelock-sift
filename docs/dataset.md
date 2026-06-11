# Dataset Documentation

## Included Demo Data

File: `examples/cases/windows_triage_events.jsonl`

Type: Synthetic normalized Windows event records.

Purpose: Demonstrate the EvidenceLock verifier loop without redistributing third-party forensic images or sensitive logs.

Expected behaviors:

- `F-001`: PowerShell encoded-command execution from a document parent process.
- `F-002`: Suspicious service installation from a temporary directory.

## Public Data Path for Full Evaluation

The same schema can be populated from:

- SIFT/EZ Tools EVTX exports produced from a SIFT workstation.
- `sbousseaden/EVTX-ATTACK-SAMPLES`, especially small Windows attack samples with documented MITRE tags.
- Digital Corpora or NIST CFReDS disk images when a disk artifact trace is needed.

Do not put private incident logs, customer data, credentials, tokens, or personal documents in this repository.
