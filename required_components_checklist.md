# FIND EVIL Required Components Checklist

Use this checklist before final Devpost submission. It maps the EvidenceLock SIFT package to the required FIND EVIL submission artifacts.

| Requirement | EvidenceLock artifact | Status |
| --- | --- | --- |
| Public repository | `https://github.com/OOYXLOO/evidencelock-sift` | ready |
| Open-source license | `LICENSE` | ready |
| One-page judge pack | `docs/judge_pack.md` | ready |
| Final submit operator runbook | `docs/final_submission_operator_runbook.md` | ready |
| Stage One preflight | `docs/stage_one_preflight.md` | ready; final Devpost URL and hosted video URL still require the human gate |
| Judging criteria scorecard | `docs/judge_scorecard.md` | ready |
| Presentation deck | `docs/evidencelock-sift-judge-deck.pptx` | ready |
| Demo video, five minutes or less | `docs/demo-video/evidencelock-sift-demo.webm` | ready; upload to a supported video host if Devpost does not accept raw GitHub WebM |
| Architecture / trust-boundary diagram | `docs/architecture.png`, `docs/architecture.md` | ready |
| Dataset documentation | `docs/dataset.md` | ready |
| Accuracy / evaluation report | `reports/accuracy_report.md`, `docs/accuracy_method.md` | ready |
| Execution logs / tool-call trace | `reports/execution_log.jsonl` | ready |
| Annotated agent trace | `reports/agent_trace.md` | ready |
| One-command proof-trace judge smoke test | `tools/judge_smoke_test.py` | ready |
| Fail-closed negative control | `docs/fail_closed_negative_control.md`, `examples/cases/windows_negative_case.json` | ready |
| SIFT compatibility runbook | `docs/sift_compatibility_runbook.md` | ready |
| Analyst-ready response handoff | `reports/analyst_handoff.md` | ready |
| Try-it-out / reproducibility path | `README.md` quick start and `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .` | ready |

## Submission Emphasis

- Run `docs/stage_one_preflight.md` after the Devpost project exists and before final submit. The organizer forum says Stage One is pass/fail and missing required components can eliminate the entry.
- Use `docs/final_submission_operator_runbook.md` during the final submit window so the video branch, gallery order, Additional info links, and no-go gate are all on one page.
- Lead with the verifier-first trust boundary: the agent can draft quickly, but confirmed findings must pass mechanical evidence and tool-reference checks.
- Include `docs/judge_pack.md` early in Additional info because it is the shortest route through the full evidence package.
- Include `docs/judge_scorecard.md` near the judge pack so reviewers can map each FIND EVIL criterion to evidence without hunting through the repo.
- Include `docs/evidencelock-sift-judge-deck.pptx` as a compact presentation layer after the judge hub and demo video.
- Include `tools/judge_smoke_test.py` and `reports/agent_trace.md` in Additional info because they shorten the path from claim to exact evidence/tool-call verification.
- Include `docs/fail_closed_negative_control.md` to show that no-evidence cases downgrade instead of becoming false positives.
- Include `docs/sift_compatibility_runbook.md` to show platform fit without claiming unproven live SIFT execution.
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
