from typing import Set, List, Optional

from cards import Card, Queen
from player import Player
from positions import SleepingQueenPosition, AwokenQueenPosition, HandPosition, Position, QueenCollection
from piles import DrawPile, DiscardPile


class GameState:
    number_of_players: int = 5
    on_turn: int
    sleeping_queens: Set[SleepingQueenPosition]
    awoken_queens: dict[AwokenQueenPosition, Queen]
    cards: dict[HandPosition, Optional[Card]]
    cards_discarded_last_turn: List[Card]


class Game:
    def __init__(self):
        self.game_state = GameState()
        self.players: List[Player] = [Player(self) for _ in range(self.game_state.number_of_players)]
        self.draw_pile = DrawPile()
        self.discard_pile = DiscardPile()
        self.sleeping_queens = QueenCollection()

        for player in self.players:
            player.hand.draw(5)

    def play(self, playerId: int, cards: List[Position]) -> Optional[GameState]:
        if playerId != self.game_state.on_turn:
            return
        player = self.players[playerId]
        result = player.play(cards)
        if result:
            self.game_state.on_turn = (self.game_state.on_turn + 1) % self.game_state.number_of_players
            return self.game_state

    def add_queen(self, queen: Queen):
        self.sleeping_queens.add_queen(queen)

    def remove_queen(self, queen: Queen):
        self.sleeping_queens.remove_queen(queen)
