# Methodology

AI Text Watermark Audit separates observable evidence from provider claims.

## Evidence levels

| Level | Meaning | Example |
| --- | --- | --- |
| Observable | Reproducible from the supplied bytes | A `U+200B` at byte position 41 |
| Externally verified | Confirmed by a documented detector | A signed provenance manifest that validates |
| Provider claim | Described by a primary source but not locally verifiable | Claude's unpublished text watermark detector |
| Unsupported inference | Style or probability presented as provenance | “This sounds like an LLM” |

The CLI reports the first three levels separately. It does not present unsupported inference as a watermark result.

## Unicode scan

Input is decoded as UTF-8 and inspected code point by code point. Each finding records:

- character index, line, and column;
- Unicode code point and official name;
- escaped representation;
- category and severity;
- a short interpretation.

The scanner also checks contiguous alphanumeric tokens for a mixture of Latin with Cyrillic or Greek scripts. This is a narrow confusable-character heuristic, not a general language detector.

## Comparison

`textmark compare` reports SHA-256 digests, sequence similarity, insertions, deletions, replacements, NFC canonical equivalence, and finding counts before and after an edit.

Similarity is descriptive. It is not a measure of meaning preservation and is not evidence that a watermark survived or disappeared.

## False positives

Zero-width joiners, variation selectors, non-breaking spaces, and bidirectional controls all have legitimate uses. Severity reflects review priority, not maliciousness or AI authorship.

Regression fixtures should include multilingual text, emoji sequences, mathematical notation, copied web content, and intentionally deceptive samples.

## Adding an official detector

A detector integration must document:

1. the provider or scheme;
2. detector version and source;
3. supported languages and minimum length;
4. decision threshold and output semantics;
5. known false positives and false negatives;
6. a reproducible fixture or public test vector.

Integrations that cannot meet these requirements should remain in the claim registry rather than returning a detection verdict.
