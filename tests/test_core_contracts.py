"""Offline tests for the initial architecture contracts."""
from __future__ import annotations

import asyncio
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lumeryn.application.research import RetrieveCandidates
from lumeryn.domain.models import ResearchQuery, SearchHit


class FakeSearchProvider:
    async def search(self, query: str, *, limit: int):
        return [SearchHit("Title", "https://example.org/", query, "fake")]


class CoreContractTests(unittest.TestCase):
    def test_empty_question_is_rejected(self):
        with self.assertRaises(ValueError):
            ResearchQuery("  ")

    def test_limit_is_bounded(self):
        for limit in (0, 101):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                ResearchQuery("question", limit)

    def test_retrieve_candidates_uses_port(self):
        output = asyncio.run(RetrieveCandidates(FakeSearchProvider()).execute(ResearchQuery("search")))
        self.assertEqual(output.status, "RETRIEVED")
        self.assertEqual(len(output.hits), 1)
        self.assertEqual(output.hits[0].provider, "fake")


if __name__ == "__main__":
    unittest.main()
