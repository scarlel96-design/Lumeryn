"""Offline checks for local Markdown documentation links."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_docs_links import check_links


class DocLinkTests(unittest.TestCase):
    def test_repo_links(self):
        self.assertEqual(check_links(ROOT), [])

    def test_missing_local_target(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("[broken](docs/not-found.md)", encoding="utf-8")
            self.assertTrue(check_links(root))

    def test_existing_directory_link(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("[docs](docs/)", encoding="utf-8")
            self.assertEqual(check_links(root), [])

    def test_external_link_is_skipped(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("[site](https://example.org)", encoding="utf-8")
            self.assertEqual(check_links(root), [])


if __name__ == "__main__":
    unittest.main()
