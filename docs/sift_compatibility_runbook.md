# SIFT Compatibility Runbook

This runbook explains how the submitted EvidenceLock vertical slice maps onto a SIFT workstation or Protocol SIFT-style MCP environment. It is intentionally non-claiming: the public submission does not assert live SIFT workstation execution or full-disk processing.

## What Is Proven In This Submission

- A case manifest restricts which evidence files may be read.
- Evidence is hashed before analysis.
- Normalized Windows EVTX-style records are parsed and searched through typed tools.
- Confirmed findings must cite evidence IDs and tool-call IDs.
- Unsupported confirmed findings are rejected or downgraded before publication.
- Generated reports and logs are protected by `reports/integrity_manifest.json`.

## How To Attach Real SIFT Evidence

1. Export or collect public/non-sensitive artifacts on a SIFT workstation.
2. Keep raw evidence read-only and record its original path, acquisition note, and hash.
3. Convert selected EVTX records into the normalized JSONL schema used by `examples/cases/windows_triage_events.jsonl`.
4. Create a case manifest that points to the normalized export and lists expected behaviors only when ground truth is known.
5. Run:

```powershell
$env:PYTHONPATH="src"
python -m evidencelock_sift.cli run-case --case <case-manifest> --out reports-sift
python -m evidencelock_sift.cli verify-manifest --manifest reports-sift/integrity_manifest.json --repo-root .
```

## Tool Mapping

| SIFT / DFIR tool | EvidenceLock boundary | Purpose |
| --- | --- | --- |
| `EvtxECmd` export | `parse_evtx` / `search_events` after normalization | Event triage and exact evidence references |
| `fls` | `src/evidencelock_sift/tools/sleuthkit.py::run_tsk_fls` | Recursive file listing for disk images |
| `istat` | `src/evidencelock_sift/tools/sleuthkit.py::run_tsk_istat` | Inode metadata lookup |
| MCP client tool list | `docs/mcp_tool_schema.json` | Typed tool surface and allowlist |
| Report verifier | `verify_report_claims` | Reject unsupported confirmed findings |

## Acceptance Signals For A Future Live SIFT Run

- A public or redistributable case manifest points to normalized SIFT-derived artifacts.
- `execution_log.jsonl` records the hash, parse, search, verifier, and optional Sleuth Kit wrapper calls.
- `integrity_manifest.json` verifies the SIFT-derived normalized evidence and generated outputs.
- The final report contains no confirmed finding without evidence refs and tool refs.
- Any live-tool limitation is stated in the report boundary instead of being hidden.

## Boundary

The current checked-in result is a normalized EVTX-style mini-case and negative control. It is not a full SIFT image run, does not process a full disk image, does not redistribute third-party forensic images, and does not claim endpoint containment.
