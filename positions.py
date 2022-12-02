from cards import Card, Queen
from player import Player
from typing import Union


class SleepingQueenPosition:
    def __init__(self, card: Queen):
        self.card = card

    def getCard(self) -> Queen:
        return self.card


class AwokenQueenPosition:
    def __init__(self, card: Queen, player: Player):
        self.card = card
        self.player = player

    def getCard(self) -> Queen:
        return self.card

    def getPlayer(self) -> Player:
        return self.player


class HandPosition:
    def __init__(self, card: Card, player: Player):
        self.card = card
        self.player = player

    def getCard(self) -> Card:
        return self.card

    def getPlayer(self) -> Player:
        return self.player


class Position:
    def __init__(self, pos: Union[HandPosition, SleepingQueenPosition, AwokenQueenPosition]):
        self.position = pos
