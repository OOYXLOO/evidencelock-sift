# FIND EVIL Required Components Checklist

Use this checklist before final Devpost submission. It maps the EvidenceLock SIFT package to the required FIND EVIL submission artifacts.

| Requirement | EvidenceLock artifact | Status |
| --- | --- | --- |
| Public repository | `https://github.com/OOYXLOO/evidencelock-sift` | ready |
| Open-source license | `LICENSE` | ready |
| One-page judge pack | `docs/judge_pack.md` | ready |
| Judging criteria scorecard | `docs/judge_scorecard.md` | ready |
| Demo video, five minutes or less | `docs/demo-video/evidencelock-sift-demo.webm` | ready; upload to a supported video host if Devpost does not accept raw GitHub WebM |
| Architecture / trust-boundary diagram | `docs/architecture.png`, `docs/architecture.md` | ready |
| Dataset documentation | `docs/dataset.md` | ready |
| Accuracy / evaluation report | `reports/accuracy_report.md`, `docs/accuracy_method.md` | ready |
| Execution logs / tool-call trace | `reports/execution_log.jsonl` | ready |
| Annotated agent trace | `reports/agent_trace.md` | ready |
| One-command judge smoke test | `tools/judge_smoke_test.py` | ready |
| Analyst-ready response handoff | `reports/analyst_handoff.md` | ready |
| Try-it-out / reproducibility path | `README.md` quick start and `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .` | ready |

## Submission Emphasis

- Lead with the verifier-first trust boundary: the agent can draft quickly, but confirmed findings must pass mechanical evidence and tool-reference checks.
- Include `docs/judge_pack.md` early in Additional info because it is the shortest route through the full evidence package.
- Include `docs/judge_scorecard.md` near the judge pack so reviewers can map each FIND EVIL criterion to evidence without hunting through the repo.
- Include `tools/judge_smoke_test.py` and `reports/agent_trace.md` in Additional info because they shorten the path from claim to verification.
- Show the self-correction sequence early: first draft rejected, corrected report accepted.
- Use `docs/proof-card.png` as the first gallery image because it compresses the whole proof chain into one screen.
- Use `docs/accuracy-card.png` as the third gallery image to show metrics and bypass tests without making judges open a Markdown report first.
- Link `reports/analyst_handoff.md` to show the final report is actionable for a responder, not just verifiable for a developer.
- State the honest boundary: this is a narrow EVTX-style vertical slice and a SIFT/MCP wrapper pattern, not a claim of full disk-forensics coverage.
- Include the manifest verification command so judges can validate that evidence and generated outputs still match the published hashes.

## Final No-Go Items

- Do not submit a project attached to the wrong hackathon.
- Do not claim live SIFT workstation execution unless a live SIFT transcript has been added.
- Do not include private incident data, credentials, API keys, account tokens, payout data, tax data, KYC data, or identity documents.
- Do not rely on a raw WebM URL if Devpost requires a hosted video provider; upload the existing WebM to an allowed host first.
