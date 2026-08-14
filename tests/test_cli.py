import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from textmark_audit.cli import main


class CliTests(unittest.TestCase):
    def test_scan_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("hello\u200bworld", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = main(["scan", str(path), "--json", "--fail-on", "warning"])
        payload = json.loads(output.getvalue())
        self.assertEqual(status, 1)
        self.assertEqual(payload["counts"]["warning"], 1)

    def test_claims_have_sources(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(["claims", "--json"])
        payload = json.loads(output.getvalue())
        self.assertEqual(status, 0)
        self.assertTrue(payload[0]["source"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
