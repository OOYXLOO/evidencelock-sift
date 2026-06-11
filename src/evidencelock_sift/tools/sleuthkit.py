from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _run_tool(tool_name: str, args: list[str], timeout: int = 30) -> dict[str, str | int]:
    executable = shutil.which(tool_name)
    if not executable:
        raise RuntimeError(f"{tool_name} was not found on PATH; run this on SIFT or install Sleuth Kit")
    completed = subprocess.run(
        [executable, *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def run_tsk_fls(image_path: Path, partition_offset: int | None = None) -> dict[str, str | int]:
    args = ["-r"]
    if partition_offset is not None:
        args.extend(["-o", str(partition_offset)])
    args.append(str(image_path))
    return _run_tool("fls", args)


def run_tsk_istat(image_path: Path, inode: str, partition_offset: int | None = None) -> dict[str, str | int]:
    args: list[str] = []
    if partition_offset is not None:
        args.extend(["-o", str(partition_offset)])
    args.extend([str(image_path), inode])
    return _run_tool("istat", args)
