from __future__ import annotations

from app.schemas.game import StatisticsResponse, Winner


class StatisticsEngine:
    def compute(self, winners: list[Winner]) -> StatisticsResponse:
        total = len(winners)
        if total == 0:
            return StatisticsResponse(total_rounds=0, banker_win_rate=0.0, player_win_rate=0.0, tie_rate=0.0)

        banker = winners.count("banker")
        player = winners.count("player")
        tie = winners.count("tie")
        return StatisticsResponse(
            total_rounds=total,
            banker_win_rate=banker / total,
            player_win_rate=player / total,
            tie_rate=tie / total,
        )
