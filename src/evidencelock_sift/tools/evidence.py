from __future__ import annotations

import hashlib
from pathlib import Path

from evidencelock_sift.schemas import EvidenceArtifact


def resolve_under(base_dir: Path, candidate: str | Path) -> Path:
    base = base_dir.resolve()
    resolved = (base / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate).resolve()
    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise ValueError(f"path escapes evidence root: {candidate}") from exc
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_evidence(path: Path, evidence_id: str | None = None, kind: str | None = None) -> EvidenceArtifact:
    if not path.is_file():
        raise FileNotFoundError(path)
    return EvidenceArtifact(
        evidence_id=evidence_id or path.stem,
        path=str(path),
        sha256=sha256_file(path),
        kind=kind or path.suffix.lstrip(".") or "file",
    )


def list_evidence(root: Path) -> list[EvidenceArtifact]:
    artifacts: list[EvidenceArtifact] = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            artifacts.append(hash_evidence(path, evidence_id=path.stem))
    return artifacts
