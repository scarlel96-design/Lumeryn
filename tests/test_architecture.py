"""Architecture contract tests; no optional runtime packages needed."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_architecture import scan


class ArchitectureTests(unittest.TestCase):
    def test_repository_respects_boundaries(self):
        self.assertEqual(scan(ROOT), [])

    def test_domain_cannot_import_vendor_client(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "src/lumeryn/domain"
            path.mkdir(parents=True)
            (path / "bad.py").write_text("import qdrant_client\n", encoding="utf-8")
            self.assertTrue(any("qdrant_client" in x for x in scan(Path(temp))))

    def test_application_cannot_import_infrastructure(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "src/lumeryn/application"
            path.mkdir(parents=True)
            (path / "bad.py").write_text("from lumeryn.infrastructure import anything\n", encoding="utf-8")
            self.assertTrue(any("infrastructure" in x for x in scan(Path(temp))))


if __name__ == "__main__":
    unittest.main()
