"""Thin research retrieval use case. No synthesis or model inference yet."""
from __future__ import annotations

from lumeryn.application.ports import SearchProvider
from lumeryn.domain.models import ResearchQuery, ResearchSnapshot


class RetrieveCandidates:
    def __init__(self, search_provider: SearchProvider) -> None:
        self._search_provider = search_provider

    async def execute(self, request: ResearchQuery) -> ResearchSnapshot:
        hits = await self._search_provider.search(request.text, limit=request.limit)
        return ResearchSnapshot(query=request.text, hits=tuple(hits[:request.limit]))
