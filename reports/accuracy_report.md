# Accuracy Report

Case: `windows-triage-mini-001`

## Metrics

| Metric | Result |
| --- | ---: |
| Draft verifier issues | `3` |
| Final verifier issues | `0` |
| Hallucinated confirmed claims after final verification | `0` |
| Unsupported confirmed findings after final verification | `0` |
| Expected behaviors found | `2/2` |
| Expected behaviors missed | `0` |
| Confirmed findings with evidence refs | `2/2` |
| Confirmed findings with tool refs | `2/2` |
| Manifest verification | `ok after run` |

## Tiny Confusion Matrix

| Class | Count | Evidence |
| --- | ---: | --- |
| True positives | `2` | `F-001` PowerShell encoded command and `F-002` suspicious service installation |
| True negatives | `1` | benign interactive logon remains outside the final confirmed findings |
| False positives | `0` | verifier rejects unsupported final confirmed claims |
| False negatives | `0` | both expected behaviors are present in the final report |
| Unsupported final confirmed claims | `0` | final verifier issues are zero |

## Self-Correction Result

- Draft verifier issues: `3`
- Final verifier issues: `0`
- Hallucinated confirmed claims after final verification: `0`
- Unsupported confirmed findings after final verification: `0`

## Before / After Claims

| Stage | Finding | Status | Evidence refs | Tool refs | Verifier outcome |
| --- | --- | --- | ---: | ---: | --- |
| First draft | `F-001` suspicious PowerShell execution | `confirmed` | `0` | `0` | rejected: missing evidence and tool references |
| Corrected report | `F-001` suspicious PowerShell execution | `confirmed` | `1` | `1` | accepted |
| Corrected report | `F-002` suspicious service installation | `confirmed` | `1` | `1` | accepted |

## Guardrail / Bypass Tests

| Test | Expected result | Covered by |
| --- | --- | --- |
| Confirmed finding with no evidence refs | rejected | `test_verifier_rejects_confirmed_finding_without_evidence` |
| Case manifest path escape such as `../outside.jsonl` | rejected before parsing | `test_run_case_rejects_evidence_path_escape` |
| Tampered generated report after manifest creation | hash mismatch | `test_integrity_manifest_verifies_and_detects_tampering` |
| Unsafe manifest path such as absolute path or `../outside.md` | integrity issue | `test_integrity_manifest_rejects_unsafe_paths` |

## Expected Behaviors

- `F-001`
- `F-002`

## Method

The first draft is intentionally under-evidenced. The verifier requires confirmed findings to contain both evidence references and tool references. The correction pass either attaches exact event evidence or would downgrade the finding if evidence is unavailable.