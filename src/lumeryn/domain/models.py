"""Immutable, infrastructure-independent research contracts."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResearchQuery:
    text: str
    limit: int = 5

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("Research query must not be blank")
        if not 1 <= self.limit <= 100:
            raise ValueError("limit must be between 1 and 100")


@dataclass(frozen=True, slots=True)
class SearchHit:
    title: str
    url: str
    snippet: str
    provider: str


@dataclass(frozen=True, slots=True)
class ResearchSnapshot:
    query: str
    hits: tuple[SearchHit, ...]
    status: str = "RETRIEVED"

    # RETRIEVED means candidate documents were found, not verified AI answers.
