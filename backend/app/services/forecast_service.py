from __future__ import annotations

from app.schemas.game import ForecastResponse, Winner


class ForecastEngine:
    def forecast(self, winners: list[Winner]) -> ForecastResponse:
        if not winners:
            return ForecastResponse(next_bias="tie", confidence=0.0)

        recent = winners[-6:]
        banker = recent.count("banker")
        player = recent.count("player")
        tie = recent.count("tie")
        total = len(recent)

        counts = {"banker": banker, "player": player, "tie": tie}
        bias = max(counts, key=counts.get)
        return ForecastResponse(next_bias=bias, confidence=counts[bias] / total)
