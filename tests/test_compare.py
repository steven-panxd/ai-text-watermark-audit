import unittest

from textmark_audit.compare import compare_text


class CompareTextTests(unittest.TestCase):
    def test_identical_text(self) -> None:
        result = compare_text("same", "same")
        self.assertTrue(result["identical"])
        self.assertEqual(result["similarity"], 1.0)

    def test_canonical_equivalence(self) -> None:
        result = compare_text("caf\u00e9", "cafe\u0301")
        self.assertFalse(result["identical"])
        self.assertTrue(result["canonical_equivalent"])

    def test_reports_signal_delta(self) -> None:
        result = compare_text("a\u200bb", "ab")
        self.assertEqual(result["findings_before"]["warning"], 1)
        self.assertEqual(result["findings_after"]["warning"], 0)


if __name__ == "__main__":
    unittest.main()
