from __future__ import annotations

from typing import Union, Optional, List, TYPE_CHECKING
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
    def __init__(self):
        self._queens: List[Queen] = []

    def add_queen(self, queen: Queen):
        self._queens.append(queen)

    def remove_queen(self, queen: Queen) -> Optional[Queen]:
        # queen = position.getCard()
        if queen in self._queens:
            self._queens.remove(queen)
            return queen

    def __contains__(self, item: Queen):
        return item in self._queens
