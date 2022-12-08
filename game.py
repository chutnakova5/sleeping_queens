from typing import Set, List, Optional
from random import shuffle

from cards import Card, Queen
from player import Player
from positions import SleepingQueenPosition, AwokenQueenPosition, HandPosition, Position, QueenCollection
from piles import DrawingAndTrashPile
# from interface import GameObservable


queen_info = {"Rose Queen": 5, "Cake Queen": 5, "Rainbow Queen": 5, "Starfish Queen": 5,
              "Moon Queen": 10, "Peacock Queen": 10, "Ladybug Queen": 10, "Sunflower Queen": 10,
              "Pancake Queen": 15, "Cat Queen": 15, "Dog Queen": 15, "Heart Queen": 20}


class GameState:
    number_of_players: int = 5
    on_turn: int
    sleeping_queens: Set[SleepingQueenPosition]
    awoken_queens: dict[AwokenQueenPosition, Queen]
    cards: dict[HandPosition, Optional[Card]]
    cards_discarded_last_turn: List[Card]


class Game:
    def __init__(self) -> None:
        # self.observable = GameObservable()
        self.game_state = GameState()
        self.pile = DrawingAndTrashPile()
        self.sleeping_queens = QueenCollection()
        self.generate_queens()
        self.players: List[Player] = [Player(self) for _ in range(self.game_state.number_of_players)]

        for player in self.players:
            player.hand.draw_new_cards()

    def is_finished(self) -> Optional[int]:
        for player in self.players:
            score = sum([queen.get_points() for queen in player.awoken_queens])
            if score >= 50:
                # self.observable.notify_all("Game finished")
                return score
            queen_count = 0
            for queen in player.awoken_queens:
                if queen:
                    queen_count += 1
            if queen_count >= 5:
                # self.observable.notify_all("Game finished")
                return score

    def play(self, playerId: int, cards: List[Position]) -> Optional[GameState]:
        if playerId != self.game_state.on_turn:
            return
        player = self.players[playerId]
        result = player.play(cards)
        if result:
            self.game_state.on_turn = (self.game_state.on_turn + 1) % self.game_state.number_of_players
            return self.game_state

    def add_queen(self, queen: Queen) -> None:
        self.sleeping_queens.add_queen(queen)

    def remove_queen(self, queen: Queen) -> None:
        self.sleeping_queens.remove_queen(queen)

    def generate_queens(self) -> None:
        for name, value in queen_info.items():
            self.add_queen(Queen(name, value))
