"""Offline tests for mandatory project-document validation."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.verify_project import check, sha256, work_order_path


class DocumentGateTests(unittest.TestCase):
    def test_foundation_work_order(self):
        result = check(ROOT, "WO-AGENT-00")
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertEqual(len(result["master_sha256"]), 64)

    def test_invalid_work_order_id(self):
        for value in ("../../oops", "WO-AGENT-../x", "", "WO-AGENT-00/../../"):
            with self.subTest(value=value):
                self.assertIsNone(work_order_path(value))
                self.assertEqual(check(ROOT, value)["status"], "FAIL")

    def test_missing_work_order(self):
        self.assertEqual(check(ROOT, "WO-AGENT-99")["status"], "FAIL")

    def test_missing_documents(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self.assertEqual(check(Path(tempdir), "WO-AGENT-00")["status"], "FAIL")

    def test_duplicate_master_section_is_rejected(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            for name in (
                "AGENTS.md", "docs/MASTER_PLAN.md", "docs/PROJECT_STATE.md",
                "docs/WORK_ORDER_INDEX.md", "docs/ARCHITECTURE.md",
                "docs/ACCEPTANCE.md", "docs/REQUIREMENTS_TRACEABILITY.md",
                "docs/DECISIONS/ADR-0001-foundation.md",
                "docs/WORK_ORDERS/WO-AGENT-00.md",
            ):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            master = root / "docs/MASTER_PLAN.md"
            contents = master.read_text(encoding="utf-8")
            contents = contents.replace("## 3. 불변 설계 원칙", "## 2. 불변 설계 원칙")
            master.write_text(contents, encoding="utf-8")
            result = check(root, "WO-AGENT-00")
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any("contiguous" in msg for msg in result["errors"]))

    def test_stable_digest(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "file"
            path.write_bytes(b"hello")
            self.assertEqual(sha256(path), sha256(path))


if __name__ == "__main__":
    unittest.main()
