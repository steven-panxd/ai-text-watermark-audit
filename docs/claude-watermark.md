# Does Claude watermark generated text?

Yes, for supported models. Anthropic says Claude models launched on or after 2 August 2026 support machine-readable marking at launch. It is working to add marking to models released before that date.

This answer was last verified on 14 August 2026 against Anthropic's official documentation.

## What Anthropic has confirmed

Anthropic describes an imperceptible watermark woven directly into generated text at the model level. It says the mark:

- does not change the meaning, quality, or readability of a response;
- travels with copied and pasted text;
- may persist through some editing;
- applies worldwide when a supported model is used;
- can appear across Claude, Claude Code, Claude Platform, Cowork, Tag, and supported cloud partners.

Anthropic also says signed C2PA provenance metadata will be attached to supported generated file types such as SVG, PNG, and JPEG.

## What remains unknown

Anthropic has not yet published the promised third-party detector or detailed technical documentation. Its public article does not provide a local test, public key, token list, confidence threshold, or API endpoint for verifying the text watermark.

For that reason, this project does not label text as carrying a Claude statistical watermark. `textmark scan` examines observable Unicode and formatting signals only.

## Can hidden Unicode identify Claude text?

No. Hidden Unicode may be suspicious in context, but it is not the model-level technique Anthropic has publicly described. Invisible characters can also be introduced by editors, websites, typography, emoji composition, or malicious text manipulation.

## Can a Claude watermark prove authorship?

No. Anthropic states that a detected mark would indicate that content may have been processed by Claude. Claude could have been used only to proofread, translate, summarize, or format material written elsewhere.

Likewise, failure to detect a mark would not prove human authorship. Short passages, older models, unsupported surfaces, substantial edits, or mixed text can all prevent reliable detection.

## Sources

- Anthropic, [How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)
- European Commission, [Code of Practice on Transparency of AI-generated Content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)
