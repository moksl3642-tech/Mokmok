from __future__ import annotations

from fastapi import APIRouter, Depends

from app.db.unit_of_work import UnitOfWork
from app.schemas.game import (
    ForecastResponse,
    PlayRoundRequest,
    PlayRoundResponse,
    RoadmapResponse,
    StatisticsResponse,
)
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])
_STORAGE: list = []


def get_game_service() -> GameService:
    uow = UnitOfWork(storage=_STORAGE)
    return GameService(uow=uow)


@router.post("/rounds", response_model=PlayRoundResponse)
def play_round(payload: PlayRoundRequest, service: GameService = Depends(get_game_service)) -> PlayRoundResponse:
    return service.play_round(payload)


@router.get("/roadmap", response_model=RoadmapResponse)
def get_roadmap(service: GameService = Depends(get_game_service)) -> RoadmapResponse:
    return service.get_roadmap()


@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(service: GameService = Depends(get_game_service)) -> StatisticsResponse:
    return service.get_statistics()


@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(service: GameService = Depends(get_game_service)) -> ForecastResponse:
    return service.get_forecast()
