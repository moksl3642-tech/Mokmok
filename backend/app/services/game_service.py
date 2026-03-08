from __future__ import annotations

from app.db.unit_of_work import UnitOfWork
from app.models.game import RoundResult
from app.schemas.game import (
    ForecastResponse,
    PlayRoundRequest,
    PlayRoundResponse,
    RoadmapResponse,
    StatisticsResponse,
    Winner,
)
from app.services.baccarat_engine import BaccaratEngine
from app.services.forecast_service import ForecastEngine
from app.services.roadmap_engine import RoadmapEngine
from app.services.statistics_service import StatisticsEngine


class GameService:
    def __init__(
        self,
        uow: UnitOfWork,
        baccarat_engine: BaccaratEngine | None = None,
        roadmap_engine: RoadmapEngine | None = None,
        statistics_engine: StatisticsEngine | None = None,
        forecast_engine: ForecastEngine | None = None,
    ):
        self._uow = uow
        self._baccarat_engine = baccarat_engine or BaccaratEngine()
        self._roadmap_engine = roadmap_engine or RoadmapEngine()
        self._statistics_engine = statistics_engine or StatisticsEngine()
        self._forecast_engine = forecast_engine or ForecastEngine()

    def play_round(self, request: PlayRoundRequest) -> PlayRoundResponse:
        with self._uow as tx:
            winner = self._baccarat_engine.determine_winner(request.banker_cards, request.player_cards)
            result = RoundResult(
                round_no=tx.game_repository.next_round_no(),
                winner=winner,
                banker_cards=request.banker_cards,
                player_cards=request.player_cards,
            )
            tx.game_repository.add_round(result)
            tx.commit()

        return PlayRoundResponse(
            round_no=result.round_no,
            winner=result.winner,
            banker_points=self._baccarat_engine.point(result.banker_cards),
            player_points=self._baccarat_engine.point(result.player_cards),
            created_at=result.created_at,
        )

    def get_roadmap(self) -> RoadmapResponse:
        with self._uow as tx:
            winners = [round_result.winner for round_result in tx.game_repository.list_rounds()]
        sequence = self._roadmap_engine.build(winners)
        return RoadmapResponse(sequence=sequence)

    def get_statistics(self) -> StatisticsResponse:
        with self._uow as tx:
            winners: list[Winner] = [round_result.winner for round_result in tx.game_repository.list_rounds()]
        return self._statistics_engine.compute(winners)

    def get_forecast(self) -> ForecastResponse:
        with self._uow as tx:
            winners: list[Winner] = [round_result.winner for round_result in tx.game_repository.list_rounds()]
        return self._forecast_engine.forecast(winners)
