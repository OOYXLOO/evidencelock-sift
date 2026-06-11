# Devpost Submission Draft

## Project Name

EvidenceLock SIFT: Verifier-First Protocol SIFT Triage

## Tagline

Verifier-first custom MCP-style boundary for Protocol SIFT triage: every confirmed finding must prove itself with evidence refs, tool-call logs, verifier correction, and integrity hashes.

## Built With

Python, Protocol SIFT design pattern, Model Context Protocol-style typed tools, Windows event triage, SHA-256 integrity manifest, Sleuth Kit wrapper pattern, HTML/CSS demo recording, browser MediaRecorder.

## What It Does

EvidenceLock SIFT is a defensive incident-response agent pattern for SANS SIFT / Protocol SIFT workflows. It lets an agent move quickly through evidence collection and report drafting, but it blocks the dangerous part: confident conclusions that are not tied to reproducible evidence.

Judge fast path: run one command, watch the first verifier pass reject an unsafe confirmed claim, inspect the corrected pass and `proof_trace` IDs, then verify the report hashes with the integrity manifest.

The demo implements a complete vertical slice:

- hashes the evidence artifact before analysis
- parses normalized Windows EVTX-style event records
- searches for suspicious process creation and service-installation events
- drafts an investigation report
- runs a verifier that rejects unsupported confirmed findings
- corrects the report by attaching exact evidence IDs and tool-call IDs
- emits `investigation_report.md`, `investigation_report.json`, `accuracy_report.md`, `timeline_report.md`, `execution_log.jsonl`, and `integrity_manifest.json`
- emits `analyst_handoff.md` with MITRE mapping, priority, and concrete response actions for each confirmed finding
- emits `agent_trace.md`, an annotated trace over the execution log that explains each tool call and correction decision

The first draft intentionally fails verification. The final report only keeps confirmed findings when they include evidence references and reproducible tool references.

## Inspiration

FIND EVIL asks builders to close the speed gap between AI-accelerated attackers and human responders. The speed problem is real, but a faster report is not helpful if it hallucinates. EvidenceLock focuses on the trust boundary: make the agent fast, but make every confirmed finding prove itself.

## How We Built It

I built the project as a small, auditable Python package instead of a broad chatbot. The core modules are:

- `tools/evidence.py`: read-only evidence listing and SHA-256 hashing
- `tools/evtx.py`: normalized EVTX JSONL/XML parsing and search
- `tools/sleuthkit.py`: optional SIFT/Sleuth Kit wrapper pattern
- `agent/verifier.py`: mechanical claim verification
- `agent/loop.py`: plan, collect, draft, verify, correct, final report
- `mcp_server.py`: MCP-style tool schema and tool-call boundary

The design keeps SIFT tools behind typed functions. On a full SIFT workstation, the same pattern can wrap EvtxECmd, mmls, fls, istat, icat, and other DFIR tools without giving the model unconstrained shell access.

## Challenges

The hard part was deciding what the agent is not allowed to do. It is easy to make a demo that always ends cleanly. It is more useful to make a demo that starts with an unsafe confirmed claim and then proves the verifier can catch it.

Another challenge was keeping the demo honest without redistributing third-party forensic images or private logs. The repository includes a synthetic normalized Windows mini-case and documents how the same schema maps to SIFT/EZ Tools exports, EVTX-ATTACK-SAMPLES, Digital Corpora, or NIST CFReDS data.

## Accomplishments

- The final report has two confirmed findings and zero final verifier issues.
- Every confirmed finding has an evidence ID, event record number, timestamp, and tool-call reference.
- The execution log shows the failed first verification pass and the successful corrected pass.
- The accuracy report includes a metrics table, tiny confusion matrix, before/after claim table, and bypass tests for unsupported claims, path escapes, tampered reports, and unsafe manifest paths.
- The judge smoke test returns JSON `ok: true` only after checking the rejected draft, corrected verifier, manifest, exact `F-001`/`F-002` evidence/tool-call proof trace, generated report set, negative-control manifest, and downgrade behavior.
- The timeline report gives judges a timestamp-sorted triage view before they inspect the full report.
- The analyst handoff converts confirmed findings into MITRE-mapped response actions, so the output is useful to a responder after verification.
- The integrity manifest records SHA-256 hashes for the input evidence file and generated outputs.
- The `verify-manifest` CLI command checks that evidence and output hashes still match and returns `"ok": true` for the published report set.
- The proof-card visual gives judges a one-screen trace from finding to evidence, tool call, verifier correction, and integrity hash.
- The project runs with the Python standard library for the demo path.
- The repository includes tests, reports, dataset documentation, architecture diagram, and a generated WebM demo asset.

## What We Learned

The most important lesson is that DFIR agents need verifiers as architecture, not just instructions. Prompting the model to be careful is not enough. EvidenceLock makes the verifier an explicit boundary between draft reasoning and published findings.

## What's Next

- Run the same verifier against SIFT workstation outputs from EvtxECmd and Sleuth Kit.
- Add a real MCP server transport around the current typed tool schema.
- Add timeline contradiction checks across event sources.
- Add a larger public benchmark from EVTX-ATTACK-SAMPLES or NIST CFReDS.
- Add report export templates compatible with Protocol SIFT case reporting.

## Judge Fast Path

- `docs/judging_guide.md`: FIND EVIL judging matrix, proof card, demo path, and limitations.
- `docs/judge_pack.md`: shortest judge path with requirements map, evidence links, and reproduction command.
- `docs/judge_scorecard.md`: direct map from FIND EVIL judging criteria to public evidence.
- `tools/judge_smoke_test.py`: one-command judge smoke test with exact expected checks and `proof_trace` evidence/tool-call IDs.
- `docs/fail_closed_negative_control.md`: negative-control case proving unsupported claims downgrade to unresolved.
- `docs/sift_compatibility_runbook.md`: non-claiming SIFT/Sleuth Kit migration path.
- `docs/required_components_checklist.md`: final submission checklist for the required FIND EVIL artifacts.
- `docs/proof-card.png`: visual proof trace for finding `F-001`.
- `docs/accuracy-card.png`: visual metrics and guardrail/bypass-test summary.
- `reports/execution_log.jsonl`: command IDs for hashing, parsing, searches, and both verifier passes.
- `reports/agent_trace.md`: annotated trace over the execution log and correction decision.
- `reports/investigation_report.md`: final confirmed findings with evidence and tool references.
- `reports/timeline_report.md`: timestamp-sorted event timeline for fast triage review.
- `reports/analyst_handoff.md`: MITRE, priority, evidence, tool-call, and response-action handoff.
- `reports/integrity_manifest.json`: SHA-256 hashes for the input evidence file and generated outputs.

## Links

- Repository: https://github.com/OOYXLOO/evidencelock-sift
- Demo WebM: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/demo-video/evidencelock-sift-demo.webm
- Presentation deck: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/evidencelock-sift-judge-deck.pptx
- Judge pack: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_pack.md
- Judge scorecard: https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_scorecard.md
- Judge smoke test: https://github.com/OOYXLOO/evidencelock-sift/blob/main/tools/judge_smoke_test.py
- Judging guide: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/judging_guide.md
- Devpost field pack: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/devpost_field_pack.md
- Required components checklist: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/required_components_checklist.md
- Fail-closed negative control: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/fail_closed_negative_control.md
- SIFT compatibility runbook: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/sift_compatibility_runbook.md
- MCP-style tool schema: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/mcp_tool_schema.json
- Proof card PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/proof-card.png
- Accuracy card PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/accuracy-card.png
- Proof card: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/proof-card.svg
- Accuracy card: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/accuracy-card.svg
- Architecture PNG: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/architecture.png
- Devpost gallery assets: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/devpost_gallery_assets.md
- Accuracy report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/accuracy_report.md
- Investigation report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/investigation_report.md
- Timeline report: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/timeline_report.md
- Analyst handoff: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/analyst_handoff.md
- Agent trace: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/agent_trace.md
- Integrity manifest: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/reports/integrity_manifest.json
- Architecture diagram: https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/architecture.svg

## Final Submission Reminder

Do not submit until the Devpost project draft exists, video URL requirements are satisfied, and all FIND EVIL additional-info fields are reviewed.
