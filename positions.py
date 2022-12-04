from __future__ import annotations

from typing import Union, Optional, List, Dict, TYPE_CHECKING
from cards import Card, Queen

if TYPE_CHECKING:
    from player import Player


class SleepingQueenPosition:
    def __init__(self, card: Queen):
        self._card = card

    def get_card(self) -> Queen:
        return self._card


class AwokenQueenPosition:
    def __init__(self, card: Queen, player: Player):
        self._card = card
        self._player = player

    def get_card(self) -> Queen:
        return self._card

    def get_player(self) -> Player:
        return self._player


class HandPosition:
    def __init__(self, card: Card, player: Player):
        self._card = card
        self._player = player

    def get_card(self) -> Card:
        return self._card

    def get_player(self) -> Player:
        return self._player


Position = Union[HandPosition, SleepingQueenPosition, AwokenQueenPosition]


class QueenCollection:
    def __init__(self, player: Optional[Player] = None):
        self._queens: List[Optional[Queen]] = []
        self.player = player

    def add_queen(self, queen: Queen):
        self._queens.append(queen)

    def remove_queen(self, queen: Queen) -> Optional[Queen]:
        if queen in self._queens:
            index: int = self._queens.index(queen)
            self._queens[index] = None
            self._queens.remove(queen)
            return queen

    def __contains__(self, item: Queen):
        return item in self._queens

    def __getitem__(self, index):
        return self._queens[index]

    def get_queens(self) -> Dict[Position, Queen]:
        dct: Dict[Position, Queen] = {}
        position = AwokenQueenPosition if self.player else SleepingQueenPosition
        for queen in self._queens:
            dct[position(queen, self.player)] = queen
        return dct
