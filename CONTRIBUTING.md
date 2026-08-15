# Contributing

Small, testable changes are preferred.

1. Open an issue for a new detector, file format, or change in report semantics.
2. Add a regression fixture that demonstrates the behavior.
3. Run `python -m unittest discover -s tests -v`.
4. Keep provider claims tied to a primary source and a verification date.

Detector integrations must document thresholds, supported inputs, and known failure modes. Do not present general AI-authorship estimates as watermark verification.

By participating, you agree to keep discussion focused on the code and evidence.
