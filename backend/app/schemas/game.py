from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Winner = Literal["banker", "player", "tie"]


@dataclass(slots=True)
class PlayRoundRequest:
    banker_cards: list[int]
    player_cards: list[int]

    def __post_init__(self) -> None:
        if not 2 <= len(self.banker_cards) <= 3:
            raise ValueError("banker_cards phải có 2-3 lá")
        if not 2 <= len(self.player_cards) <= 3:
            raise ValueError("player_cards phải có 2-3 lá")


@dataclass(slots=True)
class PlayRoundResponse:
    round_no: int
    winner: Winner
    banker_points: int
    player_points: int
    created_at: datetime


@dataclass(slots=True)
class RoadmapResponse:
    sequence: list[Winner]


@dataclass(slots=True)
class StatisticsResponse:
    total_rounds: int
    banker_win_rate: float
    player_win_rate: float
    tie_rate: float


@dataclass(slots=True)
class ForecastResponse:
    next_bias: Winner
    confidence: float
