# Fail-Closed Negative Control

EvidenceLock includes a negative-control case to prove that an unsupported draft claim is downgraded instead of being confirmed.

## Case

- Manifest: `examples/cases/windows_negative_case.json`
- Evidence: `examples/cases/windows_negative_events.jsonl`
- Expected confirmed findings: none
- Included event: one benign interactive logon tagged `benign`

## What Should Happen

The agent still starts with the same unsafe draft claim for suspicious encoded-command PowerShell activity. Because the negative-control evidence contains no matching process-creation event, the correction pass must downgrade `F-001` to `unresolved` with no evidence refs and no tool refs.

Expected result:

- `F-001` status becomes `unresolved`.
- Final verifier issues remain `0`.
- False positives remain `0`.
- The benign logon is counted as a true negative.
- The smoke test only returns `ok: true` when this downgrade behavior is present.

## Run It

```powershell
$env:PYTHONPATH="src"
python -m evidencelock_sift.cli run-case --case examples/cases/windows_negative_case.json --out reports-negative
python -m evidencelock_sift.cli verify-manifest --manifest reports-negative/integrity_manifest.json --repo-root .
python tools/judge_smoke_test.py
```

The smoke test includes `negative_control_downgrades_to_unresolved: true` in its JSON checks.
