"""Offline Clean Architecture and import-cycle tests."""
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

    def test_relative_dependency_is_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "src/lumeryn/application"
            path.mkdir(parents=True)
            (path / "worker.py").write_text(
                "from ..infrastructure.network import adapter\n", encoding="utf-8"
            )
            self.assertTrue(any("infrastructure" in x for x in scan(root)))

    def test_import_cycle_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "src/lumeryn/domain"
            path.mkdir(parents=True)
            (path / "a.py").write_text(
                "from lumeryn.domain.b import helper\n", encoding="utf-8"
            )
            (path / "b.py").write_text(
                "from lumeryn.domain.a import helper\n", encoding="utf-8"
            )
            self.assertTrue(any("Import cycle" in x for x in scan(root)))


if __name__ == "__main__":
    unittest.main()
