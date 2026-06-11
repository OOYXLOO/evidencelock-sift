from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evidencelock_sift.tools.evidence import sha256_file

def _resolve_manifest_path(base_dir: Path, value: str) -> tuple[Path, str | None]:
    path = Path(value)
    if path.is_absolute():
        return path, "absolute paths are not allowed"
    resolved = (base_dir / path).resolve()
    try:
        resolved.relative_to(base_dir.resolve())
    except ValueError:
        return resolved, "path escapes base"
    return resolved, None

def _check_entry(base_dir: Path, entry: dict[str, Any], label: str) -> dict[str, str] | None:
    path, path_issue = _resolve_manifest_path(base_dir, str(entry.get("path", "")))
    if path_issue:
        return {"path": str(path), "kind": label, "issue": path_issue}
    expected = str(entry.get("sha256", ""))
    if not expected:
        return {"path": str(path), "kind": label, "issue": "missing expected sha256"}
    if not path.is_file():
        return {"path": str(path), "kind": label, "issue": "file missing"}
    actual = sha256_file(path)
    if actual != expected:
        return {
            "path": str(path),
            "kind": label,
            "issue": "sha256 mismatch",
            "expected": expected,
            "actual": actual,
        }
    return None

def verify_integrity_manifest(manifest_path: Path, repo_root: Path | None = None) -> list[dict[str, str]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    repo_base = (repo_root or Path.cwd()).resolve()
    output_base = manifest_path.parent.resolve()
    issues: list[dict[str, str]] = []
    for entry in manifest.get("evidence", []):
        issue = _check_entry(repo_base, entry, "evidence")
        if issue:
            issues.append(issue)
    for entry in manifest.get("outputs", []):
        issue = _check_entry(output_base, entry, "output")
        if issue:
            issues.append(issue)
    return issues
