# EvidenceLock SIFT Human Submission Gate

This page is now a completed human-gate record. The FIND EVIL Devpost project and hosted Vimeo video are live; use this only if a post-submit edit must preserve the same fields.

For the final 10-minute submit flow, use `docs/final_submit_console.html` and `docs/final_submission_operator_runbook.md` after this one-minute field order.

## One-Minute Field Order

1. Open the submitted FIND EVIL project: `https://devpost.com/software/evidencelock-sift-verifier-first-protocol-triage`.
2. Use project name: `EvidenceLock SIFT: Verifier-First Protocol SIFT Triage`.
3. Use tagline: `Verifier-first custom MCP-style boundary for Protocol SIFT triage: every confirmed finding must prove itself with evidence refs, tool-call logs, verifier correction, and integrity hashes.`
4. Use try-it-out link: `https://ooyxloo.github.io/evidencelock-sift/`.
5. Use repository link: `https://github.com/OOYXLOO/evidencelock-sift`.
6. Add demo playback link: `https://ooyxloo.github.io/evidencelock-sift/demo.html`.
7. Add judge pack link: `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_pack.md`.
8. Add deck link: `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/evidencelock-sift-judge-deck.pptx`.
9. Upload gallery images in this order: `docs/proof-card.png`, `docs/architecture.png`, `docs/accuracy-card.png`.
10. Official FIND EVIL rules allow a public YouTube, Vimeo, or Youku video with audio narration; this submission uses Vimeo. Keep the official hosted video field as `https://vimeo.com/1200810741` and keep `demo.html` as a supporting link. Use the MP4/WebM backups only if a future edit requires re-uploading.
11. Open `docs/final_submission_operator_runbook.md` for the archived no-go gate, video branch, and deadline time-zone record.
12. Open `docs/final_submit_console.html` if you want copy-ready fields in one browser page.
13. Run the Stage One preflight from `docs/stage_one_preflight.md` before final submit.

## Copy Blocks

### Project Name

```text
EvidenceLock SIFT: Verifier-First Protocol SIFT Triage
```

### Tagline

```text
Verifier-first custom MCP-style boundary for Protocol SIFT triage: every confirmed finding must prove itself with evidence refs, tool-call logs, verifier correction, and integrity hashes.
```

### Short Description

```text
EvidenceLock SIFT is a verifier-first incident-response agent pattern for SANS SIFT / Protocol SIFT workflows. It lets an agent move quickly through evidence collection and report drafting, but blocks the dangerous part: confident conclusions that are not tied to reproducible evidence.

Judge fast path: run one command, watch the first verifier pass reject an unsafe confirmed claim, inspect the corrected pass and proof_trace IDs, then verify the report hashes with the integrity manifest.
```

### Judging Hook

```text
The first report draft intentionally fails verification. The final report only keeps confirmed findings when they include evidence references and reproducible tool references. The proof-card image shows the whole chain: finding F-001 -> event record 1024 -> cmd-0003 search_events -> failed verifier pass cmd-0005 -> corrected verifier pass cmd-0006 -> SHA-256 integrity manifest.
```

## Final Safety Checks

- The organizer forum says Stage One is pass/fail; missing required components can eliminate the submission after the deadline. Use `docs/stage_one_preflight.md` before final submit.
- Confirm the Devpost target is FIND EVIL, not the Qwen project and not another competitor's project.
- Do not import `prizepilot-qwen-cloud` into FIND EVIL.
- Do not treat `https://devpost.com/software/evidence-locked-dfir-agent` as ours; it is a competitor project.
- Verify the hosted Vimeo video has audio narration and works in a logged-out browser before any future Devpost edit.
- Do not paste private logs, real victim data, passwords, API keys, payout details, tax data, KYC data, or bank/card data.
- State the honest boundary: synthetic Windows EVTX-style vertical slice, no live SIFT workstation claim, no full-disk processing claim, no real victim data claim.

## Verification Commands

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python tools/judge_smoke_test.py
python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .
```

Linux / SIFT workstation equivalent:

```bash
export PYTHONPATH=src
python3 -m unittest discover -s tests -v
python3 tools/judge_smoke_test.py
python3 -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .
```

Expected smoke-test highlights:

- `draft_rejected_with_three_issues: true`
- `final_verifier_zero_issues: true`
- `manifest_ok: true`
- `negative_control_downgrades_to_unresolved: true`
- `negative_manifest_ok: true`
- `F-001`: `windows_triage_events:1024` + `cmd-0003 search_events`
- `F-002`: `windows_triage_events:2048` + `cmd-0004 search_events`
