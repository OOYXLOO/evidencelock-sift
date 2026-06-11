# Architecture

EvidenceLock SIFT is a verifier-first DFIR agent pattern.

```text
Case manifest
  |
  v
Evidence allowlist and SHA-256 manifest
  |
  v
Typed DFIR tools
  - list_evidence
  - hash_evidence
  - parse_evtx
  - search_events
  - extract_event_evidence
  - verify_report_claims
  - optional Sleuth Kit wrappers on SIFT
  |
  v
Agent loop
  plan -> collect -> draft -> verify -> correct -> final
  |
  v
Verifier boundary
  confirmed finding requires evidence_refs + tool_refs
  |
  v
Reports
  - investigation_report.md/json
  - accuracy_report.md
  - execution_log.jsonl
```

The important boundary is the verifier. Prompting asks the agent to be careful, but the verifier enforces the rule mechanically. A claim can be unresolved, inferred, or disproven, but it cannot remain confirmed without reproducible evidence.

The public tool contract is exported in `docs/mcp_tool_schema.json` for judges who want to inspect the MCP-style boundary directly.
