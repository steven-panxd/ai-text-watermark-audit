# Examples

These fixtures make the scanner behavior easy to see in a terminal, a README, or a launch post.

## Clean text

```bash
textmark scan examples/clean.txt
```

Expected result: no findings.

## Hidden zero-width character

```bash
textmark scan examples/hidden-zero-width.txt
```

Expected result: one warning for a zero width space.

## Compare versions

```bash
textmark compare examples/clean.txt examples/hidden-zero-width.txt
```

Expected result: the files are not identical, and the second version has one additional finding.

## Good share copy

"I built a local-first text forensics CLI that checks for invisible Unicode signals and tracks public AI watermark claims. It does not claim to detect Claude's unpublished statistical watermark; it shows what can be verified from the bytes you provide."
