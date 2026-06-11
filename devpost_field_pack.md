# Devpost Field Pack

Use this pack after the FIND EVIL Devpost project draft is created.

## Project Name

EvidenceLock SIFT: Verifier-First Protocol SIFT Triage

## Tagline

Verifier-first custom MCP-style boundary for Protocol SIFT triage: every confirmed finding must prove itself with evidence refs, tool-call logs, verifier correction, and integrity hashes.

## Built With

Python, Protocol SIFT design pattern, MCP-style typed tools, Windows event triage, SHA-256 integrity manifest, Sleuth Kit wrapper pattern, HTML/CSS demo recording, browser MediaRecorder.

## Project Links

- Repository: https://github.com/OOYXLOO/evidencelock-sift
- Demo WebM: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/demo-video/evidencelock-sift-demo.webm
- Proof card PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/proof-card.png
- Architecture PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/architecture.png
- Accuracy card PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/accuracy-card.png
- Judging guide: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/judging_guide.md
- Required components checklist: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/required_components_checklist.md
- MCP-style tool schema: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/mcp_tool_schema.json
- Investigation report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/investigation_report.md
- Timeline report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/timeline_report.md
- Analyst handoff: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/analyst_handoff.md
- Execution log: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/execution_log.jsonl
- Integrity manifest: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/integrity_manifest.json

## Gallery Upload Order

1. `docs/proof-card.png`
2. `docs/architecture.png`
3. `docs/accuracy-card.png`

## Short Description

EvidenceLock SIFT is a verifier-first incident-response agent pattern for SANS SIFT / Protocol SIFT workflows. It lets an agent move quickly through evidence collection and report drafting, but blocks the dangerous part: confident conclusions that are not tied to reproducible evidence.

Judge fast path: run one command, watch the first verifier pass reject an unsafe confirmed claim, inspect the corrected pass, then verify the report hashes with the integrity manifest.

The demo runs a complete vertical slice: hash evidence, parse/search normalized Windows event records, draft findings, reject unsupported confirmed claims, repair the report with evidence IDs and tool-call IDs, and emit an investigation report, timeline report, accuracy report, execution log, and integrity manifest.

## Judging Hook

The first report draft intentionally fails verification. The final report only keeps confirmed findings when they include evidence references and reproducible tool references. The proof-card image shows the whole chain: finding `F-001` -> event record `1024` -> `cmd-0003 search_events` -> failed verifier pass `cmd-0005` -> corrected verifier pass `cmd-0006` -> SHA-256 integrity manifest.

## Differentiators

- Built around Protocol SIFT-style typed tool boundaries, not a broad forensic chatbot.
- Public `docs/mcp_tool_schema.json` exposes the typed boundary, including `extract_event_evidence` and `verify_report_claims`.
- Designed to fail closed: missing evidence downgrades or rejects a finding instead of inventing certainty.
- Public artifacts are judge-verifiable: reports, execution logs, integrity manifest, proof card, architecture diagram, and tests.
- Gallery assets include a proof chain, trust-boundary diagram, and accuracy/bypass-test card.
- Demo path runs with the Python standard library, so judges can reproduce the vertical slice quickly.
- Integrity can be checked with `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .`, which returns `"ok": true` when evidence and report hashes still match.
- Accuracy evidence includes a metrics table, before/after claim table, and bypass tests for unsupported claims, path escapes, tampered reports, and unsafe manifest paths.
- Analyst handoff maps confirmed findings to MITRE techniques, primary evidence, command IDs, priority, and concrete response actions.

## Final Submit Checks

- Confirm Devpost project belongs to FIND EVIL, not another hackathon.
- Upload `proof-card.png` first and `architecture.png` second.
- Run `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .` after any report regeneration.
- Use the hosted video field only if Devpost accepts the raw GitHub WebM; otherwise upload the WebM to a supported video host first.
- Do not add API keys, private logs, real incident data, payout details, tax data, KYC data, or private account information.
