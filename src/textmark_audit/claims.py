from __future__ import annotations

from typing import Any


CLAIMS: tuple[dict[str, Any], ...] = (
    {
        "provider": "Anthropic",
        "system": "Claude",
        "mark": "embedded text watermark",
        "status": "supported-models-only",
        "effective_date": "2026-08-02",
        "verified_at": "2026-08-14",
        "official_detector": "not-publicly-documented",
        "summary": (
            "Claude models launched on or after 2026-08-02 support marking at "
            "launch. Anthropic says older models are being updated."
        ),
        "source": (
            "https://support.claude.com/en/articles/"
            "16266773-how-claude-marks-ai-generated-content"
        ),
    },
)


def get_claims() -> tuple[dict[str, Any], ...]:
    return CLAIMS
