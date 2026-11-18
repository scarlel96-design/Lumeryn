"""Abstract ports implemented by infrastructure adapters."""
from __future__ import annotations

from typing import Protocol, Sequence

from lumeryn.domain.models import SearchHit


class SearchProvider(Protocol):
    async def search(self, query: str, *, limit: int) -> Sequence[SearchHit]:
        """Return candidate hits. Implementations perform their own IO."""
        ...
