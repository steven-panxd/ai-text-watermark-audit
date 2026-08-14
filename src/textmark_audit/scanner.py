from __future__ import annotations

import hashlib
import unicodedata

from .models import Finding, ScanReport


_BIDI_CONTROLS = {
    0x061C,
    0x200E,
    0x200F,
    0x202A,
    0x202B,
    0x202C,
    0x202D,
    0x202E,
    0x2066,
    0x2067,
    0x2068,
    0x2069,
}

_INVISIBLE_FORMATTING = {
    0x00AD: "soft hyphen",
    0x034F: "combining grapheme joiner",
    0x200B: "zero width space",
    0x200C: "zero width non-joiner",
    0x200D: "zero width joiner",
    0x2060: "word joiner",
    0xFEFF: "zero width no-break space or byte-order mark",
}

_UNUSUAL_SPACES = {
    0x00A0: "no-break space",
    0x2007: "figure space",
    0x202F: "narrow no-break space",
}


def _escaped(character: str) -> str:
    value = ord(character)
    return f"\\u{value:04x}" if value <= 0xFFFF else f"\\U{value:08x}"


def _script(character: str) -> str | None:
    if not unicodedata.category(character).startswith("L"):
        return None
    name = unicodedata.name(character, "")
    for script in ("LATIN", "CYRILLIC", "GREEK"):
        if name.startswith(script):
            return script
    return None


def _finding(
    *,
    category: str,
    severity: str,
    index: int,
    line: int,
    column: int,
    character: str,
    message: str,
) -> Finding:
    return Finding(
        category=category,
        severity=severity,
        index=index,
        line=line,
        column=column,
        codepoint=f"U+{ord(character):04X}",
        escaped=_escaped(character),
        name=unicodedata.name(character, "UNNAMED CHARACTER"),
        message=message,
    )


def _scan_characters(text: str) -> list[Finding]:
    findings: list[Finding] = []
    line = 1
    column = 1

    for index, character in enumerate(text):
        value = ord(character)
        if value in _BIDI_CONTROLS:
            findings.append(
                _finding(
                    category="bidi-control",
                    severity="critical",
                    index=index,
                    line=line,
                    column=column,
                    character=character,
                    message="Bidirectional control characters can change visual ordering.",
                )
            )
        elif 0xE0000 <= value <= 0xE007F:
            findings.append(
                _finding(
                    category="unicode-tag",
                    severity="critical",
                    index=index,
                    line=line,
                    column=column,
                    character=character,
                    message="Unicode tag characters are normally invisible in rendered text.",
                )
            )
        elif value in _INVISIBLE_FORMATTING:
            findings.append(
                _finding(
                    category="invisible-format",
                    severity="warning",
                    index=index,
                    line=line,
                    column=column,
                    character=character,
                    message=f"Contains {_INVISIBLE_FORMATTING[value]}.",
                )
            )
        elif value in _UNUSUAL_SPACES:
            findings.append(
                _finding(
                    category="unusual-space",
                    severity="info",
                    index=index,
                    line=line,
                    column=column,
                    character=character,
                    message=f"Contains {_UNUSUAL_SPACES[value]} instead of an ASCII space.",
                )
            )
        elif 0xFE00 <= value <= 0xFE0F or 0xE0100 <= value <= 0xE01EF:
            findings.append(
                _finding(
                    category="variation-selector",
                    severity="info",
                    index=index,
                    line=line,
                    column=column,
                    character=character,
                    message="Variation selectors may be legitimate but are usually invisible.",
                )
            )
        elif unicodedata.category(character) == "Cf":
            findings.append(
                _finding(
                    category="format-control",
                    severity="warning",
                    index=index,
                    line=line,
                    column=column,
                    character=character,
                    message="Contains an uncommon Unicode format control.",
                )
            )

        if character == "\n":
            line += 1
            column = 1
        else:
            column += 1

    return findings


def _scan_mixed_scripts(text: str) -> list[Finding]:
    findings: list[Finding] = []
    start = 0
    while start < len(text):
        if not (text[start].isalnum() or text[start] == "_"):
            start += 1
            continue
        end = start + 1
        while end < len(text) and (text[end].isalnum() or text[end] == "_"):
            end += 1
        token = text[start:end]
        scripts = {script for character in token if (script := _script(character))}
        if "LATIN" in scripts and scripts.intersection({"CYRILLIC", "GREEK"}):
            line = text.count("\n", 0, start) + 1
            previous_newline = text.rfind("\n", 0, start)
            column = start + 1 if previous_newline < 0 else start - previous_newline
            findings.append(
                Finding(
                    category="mixed-script-token",
                    severity="warning",
                    index=start,
                    line=line,
                    column=column,
                    codepoint="multiple",
                    escaped=token.encode("unicode_escape").decode("ascii"),
                    name="MIXED LATIN AND CYRILLIC/GREEK TOKEN",
                    message=f"Token {token!r} mixes visually confusable writing systems.",
                )
            )
        start = end
    return findings


def scan_text(text: str) -> ScanReport:
    """Inspect text for machine-readable Unicode signals and confusables."""
    encoded = text.encode("utf-8")
    findings = _scan_characters(text)
    findings.extend(_scan_mixed_scripts(text))
    findings.sort(key=lambda item: (item.index, item.category))
    return ScanReport(
        sha256=hashlib.sha256(encoded).hexdigest(),
        characters=len(text),
        bytes=len(encoded),
        words=len(text.split()),
        lines=text.count("\n") + (1 if text else 0),
        findings=tuple(findings),
    )
