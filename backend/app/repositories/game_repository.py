from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from app.models.game import RoundResult


class GameRepository(Protocol):
    def add_round(self, result: RoundResult) -> None:
        ...

    def list_rounds(self) -> Sequence[RoundResult]:
        ...

    def next_round_no(self) -> int:
        ...


class InMemoryGameRepository(GameRepository):
    """Repository chỉ giữ trách nhiệm truy cập/lưu dữ liệu."""

    def __init__(self, storage: list[RoundResult]):
        self._storage = storage

    def add_round(self, result: RoundResult) -> None:
        self._storage.append(result)

    def list_rounds(self) -> Sequence[RoundResult]:
        return tuple(self._storage)

    def next_round_no(self) -> int:
        return len(self._storage) + 1
