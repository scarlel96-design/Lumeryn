"""Offline tests for the mandatory document preflight."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.verify_project import check, sha256


class DocumentGateTests(unittest.TestCase):
    def test_foundation_work_order(self):
        result = check(ROOT, "WO-AGENT-00")
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertEqual(len(result["master_sha256"]), 64)

    def test_invalid_work_order_id(self):
        result = check(ROOT, "../../oops")
        self.assertEqual(result["status"], "FAIL")

    def test_missing_documents(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self.assertEqual(check(Path(tempdir), "WO-AGENT-00")["status"], "FAIL")

    def test_stable_digest(self):
        with tempfile.TemporaryDirectory() as tempdir:
            test_file = Path(tempdir) / "x.txt"
            test_file.write_text("hello", encoding="utf-8")
            self.assertEqual(sha256(test_file), sha256(test_file))


if __name__ == "__main__":
    unittest.main()
