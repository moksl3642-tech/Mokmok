from __future__ import annotations

from app.schemas.game import Winner


class BaccaratEngine:
    @staticmethod
    def point(cards: list[int]) -> int:
        return sum(card if card < 10 else 0 for card in cards) % 10

    def determine_winner(self, banker_cards: list[int], player_cards: list[int]) -> Winner:
        banker_points = self.point(banker_cards)
        player_points = self.point(player_cards)
        if banker_points > player_points:
            return "banker"
        if player_points > banker_points:
            return "player"
        return "tie"
