# Public Dataset and Benchmark Appendix

## What Is Included Now

The checked-in evaluation uses a synthetic mini-case:

- Case: `windows-triage-mini-001`
- Evidence file: `examples/cases/windows_triage_events.jsonl`
- Format: normalized Windows EVTX-style JSONL records
- Expected behaviors: `F-001` PowerShell encoded-command execution and `F-002` suspicious service installation

The synthetic case is deliberately small so judges can reproduce the verifier loop quickly without downloading forensic images, redistributing third-party logs, or handling private incident data.

## What The Current Results Mean

The current benchmark answers one narrow question: when the agent draft contains unsupported confirmed claims, does EvidenceLock reject them until they are backed by evidence IDs and tool-call IDs?

In the checked-in run, the answer is yes:

- First verifier pass: `3` issues on an under-evidenced confirmed claim.
- Final verifier pass: `0` issues.
- Expected behaviors found: `2/2`.
- Confirmed findings with evidence refs: `2/2`.
- Confirmed findings with tool refs: `2/2`.
- Manifest verification: passes against the checked-in evidence and generated reports.

These numbers are not presented as broad forensic accuracy on real-world corpora. They are a reproducible guardrail result for the included mini-case.

## Optional Public EVTX Extension Path

A larger public benchmark can be built without changing the trust boundary:

1. Select public Windows event samples with clear ground truth, such as small entries from `sbousseaden/EVTX-ATTACK-SAMPLES`.
2. Convert selected EVTX records into the same normalized JSONL fields used by `examples/cases/windows_triage_events.jsonl`.
3. Add a case manifest that lists expected behaviors and permitted evidence paths.
4. Run `python -m evidencelock_sift.cli run-case --case <case-manifest> --out reports`.
5. Compare expected behaviors found, verifier issues, confirmed findings with evidence refs, confirmed findings with tool refs, and manifest integrity.

## Optional NIST-Compatible Extension Path

For disk-image oriented evaluation, the same report and verification model can be applied to public NIST CFReDS or Digital Corpora images:

1. Extract relevant artifacts on a SIFT workstation or equivalent forensic environment.
2. Normalize the selected event or timeline artifacts into the EvidenceLock JSONL evidence schema.
3. Preserve source provenance in each record so final findings can cite the original public image and extracted artifact.
4. Run the EvidenceLock case through the same verifier and manifest commands.
5. Publish only public-data references, normalized non-sensitive excerpts, command IDs, and hashes that are safe to redistribute.

No checked-in artifact currently proves live SIFT workstation execution or full-disk processing. This appendix documents the compatible path for that next benchmark, not a completed result.
