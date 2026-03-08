from app.db.unit_of_work import UnitOfWork
from app.models.game import RoundResult
from app.schemas.game import PlayRoundRequest
from app.services.game_service import GameService


def test_play_round_persists_when_committed() -> None:
    storage = []
    service = GameService(uow=UnitOfWork(storage=storage))

    result = service.play_round(PlayRoundRequest(banker_cards=[8, 1], player_cards=[2, 2]))

    assert result.round_no == 1
    assert len(storage) == 1


def test_statistics_and_forecast_use_service_logic() -> None:
    storage = []
    service = GameService(uow=UnitOfWork(storage=storage))

    service.play_round(PlayRoundRequest(banker_cards=[8, 1], player_cards=[2, 2]))
    service.play_round(PlayRoundRequest(banker_cards=[2, 2], player_cards=[9, 9]))

    stats = service.get_statistics()
    forecast = service.get_forecast()

    assert stats.total_rounds == 2
    assert stats.banker_win_rate == 0.5
    assert stats.player_win_rate == 0.5
    assert forecast.next_bias in {"banker", "player", "tie"}


def test_uow_rolls_back_without_commit() -> None:
    storage = []
    uow = UnitOfWork(storage=storage)

    with uow as tx:
        tx.game_repository.add_round(
            RoundResult(round_no=1, winner="banker", banker_cards=[1, 9], player_cards=[3, 4])
        )

    assert storage == []
