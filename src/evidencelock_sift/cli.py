from __future__ import annotations

import argparse
import json
from pathlib import Path

from evidencelock_sift.agent.loop import run_case


def _run_case(args: argparse.Namespace) -> int:
    report = run_case(Path(args.case), Path(args.out))
    print(json.dumps({"case_id": report.case_id, "findings": len(report.findings)}, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evidencelock-sift")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run-case", help="run the EvidenceLock demo loop")
    run_parser.add_argument("--case", required=True, help="case manifest JSON")
    run_parser.add_argument("--out", required=True, help="output reports directory")
    run_parser.set_defaults(func=_run_case)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
