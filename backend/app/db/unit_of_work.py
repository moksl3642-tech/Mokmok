from __future__ import annotations

from contextlib import AbstractContextManager

from app.models.game import RoundResult
from app.repositories.game_repository import InMemoryGameRepository


class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """Transaction boundary cho service layer."""

    def __init__(self, storage: list[RoundResult] | None = None):
        self._storage = storage if storage is not None else []
        self._working: list[RoundResult] = []
        self.committed = False
        self.game_repository = InMemoryGameRepository(self._working)

    def __enter__(self) -> "UnitOfWork":
        self._working = list(self._storage)
        self.game_repository = InMemoryGameRepository(self._working)
        self.committed = False
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc:
            self.rollback()
            return
        if not self.committed:
            self.rollback()

    def commit(self) -> None:
        self._storage.clear()
        self._storage.extend(self._working)
        self.committed = True

    def rollback(self) -> None:
        self._working = list(self._storage)
        self.game_repository = InMemoryGameRepository(self._working)

    @property
    def storage(self) -> list[RoundResult]:
        return self._storage
