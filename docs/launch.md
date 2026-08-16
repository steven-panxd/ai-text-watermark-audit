# Launch Notes

Use this page when sharing AI Text Watermark Audit in public communities. Keep the positioning sharp, honest, and easy to test.

## One-liner

AI Text Watermark Audit is a local CLI for finding invisible Unicode signals in text and tracking sourced AI text watermark claims.

## Short post

I published `ai-text-watermark-audit`, a small local-first CLI for text forensics around AI watermark claims.

It can scan UTF-8 files for zero-width characters, bidi controls, Unicode tag characters, unusual spaces, variation selectors, and narrow mixed-script confusables. It also has a `claims` command that tracks public provider statements, starting with Claude.

Important limitation: it does not claim to detect or remove Claude's unpublished statistical watermark. It separates what is observable from the supplied bytes from what currently requires an official detector.

Install:

```bash
pipx install ai-text-watermark-audit
textmark scan draft.txt
textmark claims
```

Repo: https://github.com/steven-panxd/ai-text-watermark-audit
PyPI: https://pypi.org/project/ai-text-watermark-audit/

## Community-specific angles

- Hacker News: emphasize the distinction between observable Unicode signals and private statistical watermarks.
- Reddit security/dev communities: lead with local-only scanning, no network calls, and clear false-positive language.
- X/LinkedIn: show the one-command demo and the Claude status caveat.
- Chinese developer communities: use "AI 文本水印审计" and "不可见 Unicode 扫描" rather than "去水印".

## GitHub Topics

Suggested topics:

`ai-watermark`, `claude`, `llm-watermark`, `text-forensics`, `unicode-security`, `unicode`, `cli`, `python`, `ai-safety`, `digital-forensics`

## Guardrails

- Do not claim the tool detects Claude-generated text.
- Do not claim a clean scan proves human authorship.
- Do not market it as a watermark remover.
- Do not imply affiliation with Anthropic or any model provider.
