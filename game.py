from typing import Set, List, Optional
from cards import Card, Queen, QueenCollection
from player import Player
from positions import SleepingQueenPosition, AwokenQueenPosition, HandPosition, Position
from piles import DrawPile, DiscardPile


class GameState:
    number_of_players: int = 5
    on_turn: int
    sleeping_queens: Set[SleepingQueenPosition]
    awoken_queens: dict[AwokenQueenPosition, Queen]
    cards: dict[HandPosition, Optional[Card]]
    cards_discarded_last_turn: List[Card]


class Game:
    game_state = GameState()
    players: List[Player] = [Player() for _ in range(game_state.number_of_players)]
    draw_pile = DrawPile()
    discard_pile = DiscardPile()
    sleeping_queens = QueenCollection()

    def play(self, playerId: int, cards: List[Position]) -> Optional[GameState]:
        if playerId != self.game_state.on_turn:
            return
        player = self.players[playerId]
        result = player.play(cards)
        if result:
            self.game_state.on_turn = (self.game_state.on_turn + 1) % self.game_state.number_of_players
            return self.game_state
