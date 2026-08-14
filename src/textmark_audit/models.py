from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Finding:
    category: str
    severity: str
    index: int
    line: int
    column: int
    codepoint: str
    escaped: str
    name: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ScanReport:
    sha256: str
    characters: int
    bytes: int
    words: int
    lines: int
    findings: tuple[Finding, ...]

    @property
    def counts(self) -> dict[str, int]:
        counts = {"critical": 0, "warning": 0, "info": 0}
        for finding in self.findings:
            counts[finding.severity] += 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "sha256": self.sha256,
            "characters": self.characters,
            "bytes": self.bytes,
            "words": self.words,
            "lines": self.lines,
            "counts": self.counts,
            "findings": [finding.to_dict() for finding in self.findings],
        }
