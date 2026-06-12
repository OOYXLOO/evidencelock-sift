# FIND EVIL Stage One Preflight

Use this before the final Devpost submit button. The public organizer forum says Stage One is pass/fail and missing required components can eliminate a submission after the deadline.

Organizer forum topic:
`https://findevil.devpost.com/forum_topics/44065-submission-checks-make-sure-your-entry-wont-be-disqualified`

## Status

| Check | EvidenceLock status | Required final action |
| --- | --- | --- |
| FIND EVIL Devpost project URL | Not available until the Devpost project draft is created | Complete Devpost human verification / project creation, then paste the final Devpost project URL into the official check prompt |
| Public code repository | `https://github.com/OOYXLOO/evidencelock-sift` | Confirm the repo is public and the MIT license is visible |
| Public demo video URL | Local WebM and public playback page exist | Upload `docs/demo-video/evidencelock-sift-demo.webm` to YouTube, Vimeo, or Youku if Devpost does not accept the raw GitHub WebM as the official video field |
| Try-it-out / local run path | `https://ooyxloo.github.io/evidencelock-sift/` and README quick start | Use the GitHub Pages judge hub as the Devpost try-it-out link |
| Setup instructions | `README.md` quick start | Keep the standard-library Python path visible in the README |
| Architecture diagram | `docs/architecture.png` and `docs/architecture.md` | Upload `docs/architecture.png` second in Devpost gallery |
| Evidence dataset documentation | `docs/dataset.md` and `docs/public_dataset_benchmark_appendix.md` | Include both links in Additional info |
| Accuracy report | `reports/accuracy_report.md` and `docs/accuracy_method.md` | Include the accuracy report link in Additional info |
| Self-correction proof | `tools/judge_smoke_test.py`, `reports/agent_trace.md`, `docs/proof-card.png` | Put the proof-card gallery image first and include the smoke-test highlights |
| SIFT / Protocol SIFT fit | `docs/sift_compatibility_runbook.md` and `docs/mcp_tool_schema.json` | State the honest boundary: SIFT-compatible wrapper pattern, not a live full-disk SIFT claim |
| Open-source license | `LICENSE` | Do not remove or rename |

## Official Check Input Template

After the Devpost project exists and the hosted video URL is available, paste this into the official submission-check assistant together with the organizer prompt:

```text
Public GitHub repository URL:
https://github.com/OOYXLOO/evidencelock-sift

Devpost project page URL:
[PASTE FINAL FIND EVIL DEVPOST PROJECT URL HERE]

Demo video URL:
[PASTE YOUTUBE / VIMEO / YOUKU URL HERE]

Try-it-out URL:
https://ooyxloo.github.io/evidencelock-sift/

Judge hub:
https://ooyxloo.github.io/evidencelock-sift/

Embedded demo playback page:
https://ooyxloo.github.io/evidencelock-sift/demo.html

Judge pack:
https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_pack.md

Stage One preflight:
https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/stage_one_preflight.md
```

## Do Not Submit Until These Are True

- The Devpost URL is a FIND EVIL project owned by `OOYXLOO`.
- The video URL is public and hosted on a provider accepted by the rules if the Devpost video field requires one.
- The project is not imported from `prizepilot-qwen-cloud`.
- The project is not confused with the competitor page `https://devpost.com/software/evidence-locked-dfir-agent`.
- The final Additional info includes the judge pack, scorecard, smoke-test highlights, negative control, SIFT compatibility runbook, accuracy report, analyst handoff, and integrity manifest.
