# Devpost Field Pack

Use this pack after the FIND EVIL Devpost project draft is created.

## Project Name

EvidenceLock SIFT: Verifier-First Protocol SIFT Triage

## Tagline

Autonomous SIFT triage that proves every confirmed finding with evidence refs, tool-call logs, verifier corrections, and integrity hashes.

## Built With

Python, Protocol SIFT design pattern, MCP-style typed tools, Windows event triage, SHA-256 integrity manifest, Sleuth Kit wrapper pattern, HTML/CSS demo recording, browser MediaRecorder.

## Project Links

- Repository: https://github.com/OOYXLOO/evidencelock-sift
- Demo WebM: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/demo-video/evidencelock-sift-demo.webm
- Proof card PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/proof-card.png
- Architecture PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/architecture.png
- Judging guide: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/judging_guide.md
- Investigation report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/investigation_report.md
- Timeline report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/timeline_report.md
- Execution log: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/execution_log.jsonl
- Integrity manifest: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/integrity_manifest.json

## Gallery Upload Order

1. `docs/proof-card.png`
2. `docs/architecture.png`

## Short Description

EvidenceLock SIFT is a verifier-first incident-response agent pattern for SANS SIFT / Protocol SIFT workflows. It lets an agent move quickly through evidence collection and report drafting, but blocks the dangerous part: confident conclusions that are not tied to reproducible evidence.

The demo runs a complete vertical slice: hash evidence, parse/search normalized Windows event records, draft findings, reject unsupported confirmed claims, repair the report with evidence IDs and tool-call IDs, and emit an investigation report, timeline report, accuracy report, execution log, and integrity manifest.

## Judging Hook

The first report draft intentionally fails verification. The final report only keeps confirmed findings when they include evidence references and reproducible tool references. The proof-card image shows the whole chain: finding `F-001` -> event record `1024` -> `cmd-0003 search_events` -> failed verifier pass `cmd-0005` -> corrected verifier pass `cmd-0006` -> SHA-256 integrity manifest.

## Differentiators

- Built around Protocol SIFT-style typed tool boundaries, not a broad forensic chatbot.
- Designed to fail closed: missing evidence downgrades or rejects a finding instead of inventing certainty.
- Public artifacts are judge-verifiable: reports, execution logs, integrity manifest, proof card, architecture diagram, and tests.
- Demo path runs with the Python standard library, so judges can reproduce the vertical slice quickly.
- Integrity can be checked with `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .`, which returns `"ok": true` when evidence and report hashes still match.

## Final Submit Checks

- Confirm Devpost project belongs to FIND EVIL, not another hackathon.
- Upload `proof-card.png` first and `architecture.png` second.
- Run `python -m evidencelock_sift.cli verify-manifest --manifest reports/integrity_manifest.json --repo-root .` after any report regeneration.
- Use the hosted video field only if Devpost accepts the raw GitHub WebM; otherwise upload the WebM to a supported video host first.
- Do not add API keys, private logs, real incident data, payout details, tax data, KYC data, or private account information.
