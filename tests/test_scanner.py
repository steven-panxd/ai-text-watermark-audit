import unittest

from textmark_audit.scanner import scan_text


class ScanTextTests(unittest.TestCase):
    def test_clean_text_has_no_findings(self) -> None:
        report = scan_text("A plain sentence.\n普通的一句话。")
        self.assertEqual(report.findings, ())
        self.assertEqual(report.lines, 2)

    def test_zero_width_space_is_reported_with_position(self) -> None:
        report = scan_text("safe\u200btext")
        finding = report.findings[0]
        self.assertEqual(finding.category, "invisible-format")
        self.assertEqual(finding.codepoint, "U+200B")
        self.assertEqual((finding.line, finding.column), (1, 5))

    def test_bidi_override_is_critical(self) -> None:
        report = scan_text("report\u202egnp.exe")
        self.assertEqual(report.counts["critical"], 1)
        self.assertEqual(report.findings[0].category, "bidi-control")

    def test_mixed_latin_and_cyrillic_token_is_reported(self) -> None:
        report = scan_text("p\u0430ypal")
        categories = {finding.category for finding in report.findings}
        self.assertIn("mixed-script-token", categories)

    def test_chinese_and_latin_are_not_treated_as_confusables(self) -> None:
        report = scan_text("Claude文本watermark")
        self.assertFalse(
            any(finding.category == "mixed-script-token" for finding in report.findings)
        )


if __name__ == "__main__":
    unittest.main()
