from __future__ import annotations

from typing import Union, Optional, List, TYPE_CHECKING
from cards import Card, Queen

if TYPE_CHECKING:
    from player import Player


class SleepingQueenPosition:
    def __init__(self, card: Queen):
        self._card = card

    def getCard(self) -> Queen:
        return self._card


class AwokenQueenPosition:
    def __init__(self, card: Queen, player: Player):
        self._card = card
        self._player = player

    def getCard(self) -> Queen:
        return self._card

    def getPlayer(self) -> Player:
        return self._player


class HandPosition:
    def __init__(self, card: Card, player: Player):
        self._card = card
        self._player = player

    def getCard(self) -> Card:
        return self._card

    def getPlayer(self) -> Player:
        return self._player


class Position:
    def __init__(self, pos: Union[HandPosition, SleepingQueenPosition, AwokenQueenPosition]):
        self.position = pos

    def getCard(self) -> Union[Card, Queen]:
        return self.position.getCard()

    def getPlayer(self) -> Player:
        return self.position.getPlayer()


class QueenCollection:
    def __init__(self):
        self._queens: List[Queen] = []

    def addQueen(self, queen: Queen):
        self._queens.append(queen)

    def removeQueen(self, queen: Queen) -> Optional[Queen]:
        # queen = position.getCard()
        if queen in self._queens:
            self._queens.remove(queen)
            return queen

    def __contains__(self, item: Queen):
        return item in self._queens
