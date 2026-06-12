# FIND EVIL Final Submission Operator Runbook

Use this only after the account owner has passed Devpost human verification and the FIND EVIL project draft exists. It is a last-mile checklist for the final 10 minutes before submit.

Public deadline check: the FIND EVIL Devpost page exposes `2026-06-15T23:45:00-04:00`, which is `2026-06-16 11:45 GMT+8`. Do not wait for the final hour.

## One Screen Summary

| Field | Value |
| --- | --- |
| Project name | `EvidenceLock SIFT: Verifier-First Protocol SIFT Triage` |
| Tagline | `Verifier-first custom MCP-style boundary for Protocol SIFT triage: every confirmed finding must prove itself with evidence refs, tool-call logs, verifier correction, and integrity hashes.` |
| Try it out | `https://ooyxloo.github.io/evidencelock-sift/` |
| Repository | `https://github.com/OOYXLOO/evidencelock-sift` |
| Supporting demo page | `https://ooyxloo.github.io/evidencelock-sift/demo.html` |
| Judge pack | `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_pack.md` |
| Scorecard | `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_scorecard.md` |
| Stage One preflight | `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/stage_one_preflight.md` |
| Deck | `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/evidencelock-sift-judge-deck.pptx` |
| Video upload pack | `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/video_upload_pack.md` |

## Gallery Order

1. `docs/proof-card.png`
2. `docs/architecture.png`
3. `docs/accuracy-card.png`

## Video Branch

Use the raw WebM only as the upload source if Devpost requires a hosted provider:

```text
docs/demo-video/evidencelock-sift-demo.webm
```

If Devpost accepts a raw URL in the video field, use:

```text
https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/demo-video/evidencelock-sift-demo.webm
```

If Devpost rejects raw GitHub video URLs, upload the WebM to YouTube, Vimeo, or Youku, then paste that hosted URL into the video field. Keep `https://ooyxloo.github.io/evidencelock-sift/demo.html` as a supporting project link either way.

Use `docs/video_upload_pack.md` for the exact hosted-video title, description, tags, settings, and logged-out playback checks. Do not use a private video URL.

## Additional Info Must Include

Paste the short description and judging hook from `docs/devpost_field_pack.md`, then include these links near the top:

- Judge hub: `https://ooyxloo.github.io/evidencelock-sift/`
- Embedded demo: `https://ooyxloo.github.io/evidencelock-sift/demo.html`
- Judge pack: `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_pack.md`
- Judge scorecard: `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_scorecard.md`
- Stage One preflight: `https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/stage_one_preflight.md`
- Smoke test: `https://github.com/OOYXLOO/evidencelock-sift/blob/main/tools/judge_smoke_test.py`
- Agent trace: `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/agent_trace.md`
- Accuracy report: `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/accuracy_report.md`
- Analyst handoff: `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/analyst_handoff.md`
- Integrity manifest: `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/integrity_manifest.json`
- SIFT compatibility runbook: `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/sift_compatibility_runbook.md`
- Fail-closed negative control: `https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/fail_closed_negative_control.md`

## Run Before Final Submit

From the repo root:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python tools/judge_smoke_test.py
python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .
```

Expected smoke highlights:

- `draft_rejected_with_three_issues: true`
- `final_verifier_zero_issues: true`
- `manifest_ok: true`
- `negative_control_downgrades_to_unresolved: true`
- `negative_manifest_ok: true`
- `F-001`: `windows_triage_events:1024` plus `cmd-0003 search_events`
- `F-002`: `windows_triage_events:2048` plus `cmd-0004 search_events`

## Final No-Go Gate

Do not press final submit if any item is true:

- The project URL is not under FIND EVIL.
- The project was imported from `prizepilot-qwen-cloud`.
- The project page is `https://devpost.com/software/evidence-locked-dfir-agent`; that is a competitor project, not this submission.
- The video field is empty or points to a private/unaccepted video.
- The hosted video is still processing or fails in a logged-out browser.
- The repo is private or the MIT license is not visible.
- Additional info omits the judge pack, scorecard, smoke test, Stage One preflight, or honest scope boundary.
- The text claims live full-disk SIFT execution, real victim data, or live external LLM/API usage.
- Any password, OTP, API key, private log, payout, bank, tax, KYC, or identity document is present.

## Final Success Signal

After submit, save the real Devpost project URL and a public video URL in the local money-goal handoff. The goal is still not complete until a prize, bounty, or claimable payout is verified.
