from __future__ import annotations

import argparse
import json
from pathlib import Path

from evidencelock_sift.agent.loop import run_case
from evidencelock_sift.integrity import verify_integrity_manifest


def _run_case(args: argparse.Namespace) -> int:
    report = run_case(Path(args.case), Path(args.out))
    print(json.dumps({"case_id": report.case_id, "findings": len(report.findings)}, sort_keys=True))
    return 0


def _verify_manifest(args: argparse.Namespace) -> int:
    issues = verify_integrity_manifest(Path(args.manifest), Path(args.repo_root) if args.repo_root else None)
    print(json.dumps({"issues": issues, "ok": not issues}, indent=2, sort_keys=True))
    return 1 if issues else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evidencelock-sift")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run-case", help="run the EvidenceLock demo loop")
    run_parser.add_argument("--case", required=True, help="case manifest JSON")
    run_parser.add_argument("--out", required=True, help="output reports directory")
    run_parser.set_defaults(func=_run_case)
    verify_parser = subparsers.add_parser("verify-manifest", help="verify evidence and output SHA-256 hashes")
    verify_parser.add_argument("--manifest", required=True, help="integrity manifest JSON")
    verify_parser.add_argument("--repo-root", help="repository root for relative evidence paths")
    verify_parser.set_defaults(func=_verify_manifest)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
