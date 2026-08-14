from __future__ import annotations

import hashlib
import unicodedata
from difflib import SequenceMatcher
from typing import Any

from .scanner import scan_text


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compare_text(before: str, after: str) -> dict[str, Any]:
    """Compare two text versions without making an authorship claim."""
    matcher = SequenceMatcher(a=before, b=after, autojunk=False)
    inserted = deleted = replaced_before = replaced_after = 0
    for operation, before_start, before_end, after_start, after_end in matcher.get_opcodes():
        if operation == "insert":
            inserted += after_end - after_start
        elif operation == "delete":
            deleted += before_end - before_start
        elif operation == "replace":
            replaced_before += before_end - before_start
            replaced_after += after_end - after_start

    before_report = scan_text(before)
    after_report = scan_text(after)
    return {
        "identical": before == after,
        "sha256_before": _digest(before),
        "sha256_after": _digest(after),
        "similarity": round(matcher.ratio(), 6),
        "characters_before": len(before),
        "characters_after": len(after),
        "inserted": inserted,
        "deleted": deleted,
        "replaced_before": replaced_before,
        "replaced_after": replaced_after,
        "canonical_equivalent": unicodedata.normalize("NFC", before)
        == unicodedata.normalize("NFC", after),
        "findings_before": before_report.counts,
        "findings_after": after_report.counts,
    }
