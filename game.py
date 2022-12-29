from __future__ import annotations

from typing import Set, List, Optional, TYPE_CHECKING
from random import shuffle

from cards import Queen
from player import Player
from positions import SleepingQueenPosition, AwokenQueenPosition, Position, QueenCollection
from piles import DrawingAndTrashPile

if TYPE_CHECKING:
    from interface import GameObservable


queen_info = {"Rose Queen": 5, "Cake Queen": 5, "Rainbow Queen": 5, "Starfish Queen": 5,
              "Moon Queen": 10, "Peacock Queen": 10, "Ladybug Queen": 10, "Sunflower Queen": 10,
              "Pancake Queen": 15, "Cat Queen": 15, "Dog Queen": 15, "Heart Queen": 20}


class GameState:
    def __init__(self, number_of_players: int, sleeping_queens: List[Queen]):
        self.number_of_players = number_of_players
        self.on_turn: int = 0
        self.awoken_queens: dict[AwokenQueenPosition, Queen] = {}
        self.sleeping_queens: Set[SleepingQueenPosition] = set()
        for queen in sleeping_queens:
            self.sleeping_queens.add(SleepingQueenPosition(queen))


class Game:
    def __init__(self, number_of_players: int, observable: GameObservable, pile: DrawingAndTrashPile,
                 sleeping_queens: QueenCollection, players: List[Player]) -> None:
        self.observable: GameObservable = observable
        self.pile: DrawingAndTrashPile = pile
        self.sleeping_queens: QueenCollection = sleeping_queens
        self.players: List[Player] = players
        queens: List[Queen] = self.generate_queens()
        self.game_state: GameState = GameState(number_of_players, queens)
        self.winner: Optional[Player] = None

    def update_game_state(self):
        pass

    def is_finished(self) -> Optional[int]:
        if self.get_number_of_players() in (2, 3):
            desired_points, desired_queens = 50, 5
        else:
            desired_points, desired_queens = 40, 4
        score = [player.count_points() for player in self.players]
        if self.sleeping_queens.is_empty():
            max_score = max(score)
            i = score.index(max_score)
            self.observable.notify_all(f"Game finished, winner: {i + 1}")
            self.winner = self.players[i]
            return max_score
        for i, player in enumerate(self.players):
            queen_count = player.count_queens()
            if score[i] >= desired_points or queen_count >= desired_queens:
                self.observable.notify_all(f"Game finished, winner: {i + 1}")
                self.winner = player
                return score[i]
        return None

    def play(self, playerId: int, cards: List[Position]) -> Optional[bool]:
        if playerId != self.game_state.on_turn:
            return None
        player = self.players[playerId]
        result = player.play(cards)
        if result:
            self.game_state.on_turn = (self.game_state.on_turn + 1) % self.get_number_of_players()
        return result

    def add_queen(self, queen: Queen) -> None:
        self.sleeping_queens.add_queen(queen)

    def remove_queen(self, queen: Queen) -> None:
        self.sleeping_queens.remove_queen(queen)

    def generate_queens(self) -> List[Queen]:
        queens: List[Queen] = []
        for name, value in queen_info.items():
            queens.append(Queen(name, value))
        shuffle(queens)
        for q in queens:
            self.add_queen(q)
        return queens

    def get_number_of_players(self):
        return self.game_state.number_of_players
