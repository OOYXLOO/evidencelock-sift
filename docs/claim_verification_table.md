# Claim Verification Table

This table is the short judge-facing version of `reports/accuracy_report.md`.
It describes what the demo proves in the checked-in mini-case, and where each claim can be verified.

| Claim | Before verifier/correction | After verifier/correction | Verification artifact |
| --- | --- | --- | --- |
| Confirmed findings must cite evidence | First draft marks `F-001` confirmed with `0` evidence refs; verifier rejects it. | Final report has `2/2` confirmed findings with evidence refs. | `reports/accuracy_report.md`, `reports/execution_log.jsonl`, `reports/investigation_report.md` |
| Confirmed findings must cite reproducible tool calls | First draft marks `F-001` confirmed with `0` tool refs; verifier rejects it. | `F-001` cites `cmd-0003`; `F-002` cites `cmd-0004`. | `reports/accuracy_report.md`, `reports/execution_log.jsonl` |
| MITRE-mapped claims cannot stand without evidence | First draft maps `F-001` to `T1059.001` without evidence; verifier reports an error. | `F-001` maps to `T1059.001` with event `windows_triage_events:1024`; `F-002` maps to `T1543.003` with event `windows_triage_events:2048`. | `reports/investigation_report.md`, `reports/investigation_report.json` |
| The verifier loop fails closed on unsupported confirmed claims | Verifier pass `cmd-0005` returns `3` issues and fails. | Verifier pass `cmd-0006` returns `0` issues and succeeds. | `reports/execution_log.jsonl` |
| Published outputs are tamper-evident | No integrity claim is accepted until evidence and report hashes are recorded. | `verify-manifest` returns `{"ok": true, "issues": []}` when checked against the published manifest. | `reports/integrity_manifest.json`; `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .` |
| Demo coverage is intentionally narrow | No full-disk or live SIFT workstation execution is claimed. | The checked-in demo proves a normalized Windows EVTX-style vertical slice with verifier correction and hash checks. | `docs/dataset.md`, `docs/public_dataset_benchmark_appendix.md` |

Scope note: this package demonstrates the trust boundary for a small synthetic Windows triage case. It does not claim that full SIFT disk analysis, live incident response, or public-corpus benchmarking has already been run.
