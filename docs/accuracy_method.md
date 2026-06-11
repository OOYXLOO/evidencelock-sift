# Accuracy Method

EvidenceLock reports accuracy by checking the claims it allows into the final report.

Metrics used in the demo:

- Draft verifier issues: unsupported confirmed claims before correction.
- Final verifier issues: unsupported confirmed claims after correction.
- Hallucinated confirmed claims: confirmed findings with no valid evidence ID.
- Tool trace coverage: confirmed findings with at least one tool call reference.
- Expected behavior coverage: whether the known mini-case behaviors are found.

The demo is intentionally honest: the first draft fails verification. That failure is a feature because it proves the verifier can catch a confident but unsupported claim before publication.
