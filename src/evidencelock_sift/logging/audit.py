from __future__ import annotations

import json
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any


class AuditLogger:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._counter = 0
        self.entries: list[dict[str, Any]] = []

    def record(
        self,
        tool_name: str,
        args: dict[str, Any],
        status: str,
        result: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> str:
        self._counter += 1
        command_id = f"cmd-{self._counter:04d}"
        entry = {
            "command_id": command_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool_name": tool_name,
            "args": args,
            "status": status,
            "result": result or {},
            "error": error,
        }
        self.entries.append(entry)
        with self.output_path.open("ab") as handle:
            handle.write((json.dumps(entry, sort_keys=True) + "\n").encode("utf-8"))
        return command_id
