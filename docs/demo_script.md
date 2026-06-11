# Demo Script

Target length: under 5 minutes.

1. Open with the FIND EVIL problem: AI can move faster than human responders, but an AI report is dangerous if it cannot prove each claim.
2. Show `python -m evidencelock_sift.cli run-case --case examples/cases/windows_triage_case.json --out reports`.
3. Open `reports/execution_log.jsonl` and point out `hash_evidence`, `parse_evtx`, `search_events`, and two verification passes.
4. Show the first verifier pass failed because `F-001` was confirmed without evidence.
5. Show the final report where `F-001` and `F-002` each include evidence IDs, record numbers, timestamps, and tool calls.
6. Close with the Protocol SIFT fit: the same typed tools can wrap SIFT workstation binaries, but the verifier remains the guardrail.
