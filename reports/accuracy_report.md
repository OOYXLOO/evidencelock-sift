# Accuracy Report

Case: `windows-triage-mini-001`

## Self-Correction Result

- Draft verifier issues: `3`
- Final verifier issues: `0`
- Hallucinated confirmed claims after final verification: `0`
- Unsupported confirmed findings after final verification: `0`

## Expected Behaviors

- `F-001`
- `F-002`

## Method

The first draft is intentionally under-evidenced. The verifier requires confirmed findings to contain both evidence references and tool references. The correction pass either attaches exact event evidence or would downgrade the finding if evidence is unavailable.