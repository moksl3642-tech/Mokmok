from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class RoundResult:
    round_no: int
    winner: str
    banker_cards: list[int]
    player_cards: list[int]
    created_at: datetime = field(default_factory=datetime.utcnow)
