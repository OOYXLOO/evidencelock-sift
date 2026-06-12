# Devpost Field Pack

Use this pack to preserve or edit the submitted FIND EVIL Devpost entry.

## Project Name

EvidenceLock SIFT: Verifier-First Protocol SIFT Triage

## Tagline

Evidence-locked DFIR triage: agent speed with verifier-enforced proof.

## Built With

Python, Protocol SIFT design pattern, MCP-style typed tools, Windows event triage, SHA-256 integrity manifest, Sleuth Kit wrapper pattern, HTML/CSS demo recording, browser MediaRecorder.

## Project Links

- Devpost project: https://devpost.com/software/evidencelock-sift-verifier-first-protocol-triage
- Repository: https://github.com/OOYXLOO/evidencelock-sift
- Judge hub source: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/index.html
- Judge hub Pages URL: https://ooyxloo.github.io/evidencelock-sift/
- Official hosted demo video: https://vimeo.com/1200810741
- Final submit console: https://ooyxloo.github.io/evidencelock-sift/final_submit_console.html
- Embedded demo playback page: https://ooyxloo.github.io/evidencelock-sift/demo.html
- Preferred MP4 upload source, not the official Devpost video field: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/demo-video/evidencelock-sift-demo.mp4
- WebM backup upload source, not the official Devpost video field: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/demo-video/evidencelock-sift-demo.webm
- Official video field: https://vimeo.com/1200810741
- Presentation deck: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/evidencelock-sift-judge-deck.pptx
- Proof card PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/proof-card.png
- Architecture PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/architecture.png
- Accuracy card PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/accuracy-card.png
- Judge pack: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_pack.md
- Judge scorecard: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_scorecard.md
- Smoke proof snapshot: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/smoke_proof.md
- Human submission gate pack: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/human_submission_gate.md
- Stage One preflight: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/stage_one_preflight.md
- Final submission operator runbook: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/final_submission_operator_runbook.md
- Judge smoke test: https://github.com/OOYXLOO/evidencelock-sift/blob/main/tools/judge_smoke_test.py
- Judging guide: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/judging_guide.md
- Required components checklist: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/required_components_checklist.md
- Claim verification table: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/claim_verification_table.md
- Fail-closed negative control: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/fail_closed_negative_control.md
- SIFT compatibility runbook: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/sift_compatibility_runbook.md
- Public dataset / benchmark appendix: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/public_dataset_benchmark_appendix.md
- MCP-style tool schema: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/mcp_tool_schema.json
- Investigation report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/investigation_report.md
- Timeline report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/timeline_report.md
- Analyst handoff: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/analyst_handoff.md
- Agent trace: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/agent_trace.md
- Execution log: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/execution_log.jsonl
- Integrity manifest: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/integrity_manifest.json

## Gallery Upload Order

1. `docs/proof-card.png`
2. `docs/architecture.png`
3. `docs/accuracy-card.png`

## Short Description

EvidenceLock SIFT is a verifier-first incident-response agent pattern for SANS SIFT / Protocol SIFT workflows. It lets an agent move quickly through evidence collection and report drafting, but blocks the dangerous part: confident conclusions that are not tied to reproducible evidence.

Judge fast path: run one command, watch the first verifier pass reject an unsafe confirmed claim, inspect the corrected pass and `proof_trace` IDs, then verify the report hashes with the integrity manifest.

The demo runs a complete vertical slice on a synthetic Windows EVTX-style mini-case: hash evidence, parse/search normalized Windows event records, draft findings, reject unsupported confirmed claims, repair the report with evidence IDs and tool-call IDs, and emit an investigation report, timeline report, accuracy report, execution log, and integrity manifest.

## Judging Hook

The first report draft intentionally fails verification. The final report only keeps confirmed findings when they include evidence references and reproducible tool references. The proof-card image shows the whole chain: finding `F-001` -> event record `1024` -> `cmd-0003 search_events` -> failed verifier pass `cmd-0005` -> corrected verifier pass `cmd-0006` -> SHA-256 integrity manifest.

Expected smoke-test highlights: `draft_rejected_with_three_issues: true`, `final_verifier_zero_issues: true`, `manifest_ok: true`, `negative_control_downgrades_to_unresolved: true`, and exact proof traces for `F-001` (`windows_triage_events:1024` + `cmd-0003 search_events`) and `F-002` (`windows_triage_events:2048` + `cmd-0004 search_events`).

## Differentiators

- Built around Protocol SIFT-style typed tool boundaries, not a broad forensic chatbot.
- Public `docs/mcp_tool_schema.json` exposes the typed boundary, including `extract_event_evidence` and `verify_report_claims`.
- Designed to fail closed: missing evidence downgrades or rejects a finding instead of inventing certainty.
- Public artifacts are judge-verifiable: reports, execution logs, integrity manifest, proof card, architecture diagram, and tests.
- The judge pack gives a two-minute review path, requirements map, reproduction command, and honest boundary in one GitHub-rendered page.
- The editable presentation deck gives a compact 5-slide judge path: verifier boundary, proof chain, architecture, evaluation, and Devpost close.
- The judge scorecard maps the package directly to the FIND EVIL criteria: autonomous execution quality, IR accuracy, depth, constraint implementation, audit trail quality, and usability.
- The judge smoke test gives reviewers one command that returns JSON `ok: true` only if the rejected draft, corrected verifier, manifest check, generated outputs, and exact `F-001`/`F-002` evidence/tool-call IDs match expectations.
- `docs/smoke_proof.md` gives reviewers a checked-in `ok: true` smoke snapshot before they decide whether to run the command locally.
- The smoke test also runs a negative-control case and requires `negative_control_downgrades_to_unresolved: true` plus `negative_manifest_ok: true`.
- The SIFT compatibility runbook gives a concrete, non-claiming migration path for EvtxECmd exports, Sleuth Kit wrappers, typed MCP tools, and integrity manifests.
- The annotated agent trace explains each execution-log tool call and states that the deterministic demo uses no external LLM call, private data, or API key.
- The static judge hub gives a browser-first review path for Devpost `Try it out`, and `demo.html` lets judges play the WebM in-page before opening raw artifacts.
- A concise before/after claim-verification table shows the rejected draft claim, corrected final claim, and artifact that proves each result.
- The public dataset appendix explains the synthetic mini-case honestly and gives a compatible path for EVTX-ATTACK-SAMPLES, NIST CFReDS, or Digital Corpora extension work.
- Gallery assets include a proof chain, trust-boundary diagram, and accuracy/bypass-test card.
- Demo path runs with the Python standard library, so judges can reproduce the vertical slice quickly.
- Integrity can be checked with `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .`, which returns `"ok": true` when evidence and report hashes still match.
- Accuracy evidence includes a metrics table, before/after claim table, and bypass tests for unsupported claims, path escapes, tampered reports, and unsafe manifest paths.
- Analyst handoff maps confirmed findings to MITRE techniques, primary evidence, command IDs, priority, and concrete response actions.

## Post-Submit Checks

- Devpost project is `https://devpost.com/software/evidencelock-sift-verifier-first-protocol-triage`.
- Official video field is `https://vimeo.com/1200810741`.
- Keep the one-minute human submission gate pack as a completed record: `docs/human_submission_gate.md`.
- Use the final submit console only if Devpost fields need a post-submit edit: `docs/final_submit_console.html`.
- Keep the Stage One preflight updated with the final URLs: `docs/stage_one_preflight.md`.
- Confirm Devpost project belongs to FIND EVIL, not another hackathon.
- Do not import `prizepilot-qwen-cloud` into FIND EVIL.
- Do not treat `https://devpost.com/software/evidence-locked-dfir-agent` as ours; it is a competitor project.
- Use `https://ooyxloo.github.io/evidencelock-sift/` as the `Try it out` link.
- Keep `https://ooyxloo.github.io/evidencelock-sift/demo.html` in supporting links near the Vimeo field as the embedded playback backup.
- Upload `proof-card.png` first and `architecture.png` second.
- Run `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .` after any report regeneration.
- Include the presentation deck link in supporting links after the judge hub and demo video.
- Do not use a raw GitHub video file as the official video field; the official field should be a public YouTube, Vimeo, or Youku URL with audible narration.
- Do not add API keys, private logs, real incident data, payout details, tax data, KYC data, or private account information.
