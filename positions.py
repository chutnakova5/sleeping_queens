from __future__ import annotations

from typing import Union, Optional, List, Dict, TYPE_CHECKING
from cards import Card, Queen

if TYPE_CHECKING:
    from player import Player


class SleepingQueenPosition:
    def __init__(self, card: Queen, player: None = None) -> None:
        self._card = card

    def get_card(self) -> Queen:
        return self._card


class AwokenQueenPosition:
    def __init__(self, card: Queen, player: Player) -> None:
        self._card = card
        self._player = player

    def get_card(self) -> Queen:
        return self._card

    def get_player(self) -> Player:
        return self._player


class HandPosition:
    def __init__(self, card: Card, player: Player) -> None:
        self._card = card
        self._player = player

    def get_card(self) -> Card:
        return self._card

    def get_player(self) -> Player:
        return self._player


Position = Union[HandPosition, SleepingQueenPosition, AwokenQueenPosition]


class QueenCollection:
    def __init__(self, player: Optional[Player] = None) -> None:
        self.queens: List[Optional[Queen]] = []
        self.player = player

    def add_queen(self, queen: Queen) -> None:
        for i in range(len(self.queens)):
            if self.queens[i] is None:
                self.queens[i] = queen
                return
        self.queens.append(queen)

    def remove_queen(self, queen: Queen) -> Optional[Queen]:
        if queen in self.queens:
            index: int = self.queens.index(queen)
            self.queens[index] = None
            return queen

    def __contains__(self, item: Queen) -> bool:
        return item in self.queens

    def __getitem__(self, index) -> Queen:
        return self.queens[index]

    def get_queens(self) -> Dict[Position, Queen]:
        dct: Dict[Position, Queen] = {}
        position = AwokenQueenPosition if self.player else SleepingQueenPosition
        for queen in self.queens:
            if queen:
                dct[position(queen, self.player)] = queen
        return dct
