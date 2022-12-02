from typing import Set, List, Optional
from cards import Card, Queen, QueenCollection
from player import Player
from positions import SleepingQueenPosition, AwokenQueenPosition, HandPosition
from piles import DrawPile, DiscardPile


class Game:
    players: List[Player] = [Player() for _ in range(5)]
    on_turn: Player
    draw_pile = DrawPile()
    discard_pile = DiscardPile()
    sleeping_queens = QueenCollection()

    def play(self):
        pass


class GameState:
    number_of_players: int
    on_turn: int
    sleeping_queens: Set[SleepingQueenPosition]
    awoken_queens: dict[AwokenQueenPosition, Queen]
    cards: dict[HandPosition, Optional[Card]]
    cards_discarded_last_turn: List[Card]
