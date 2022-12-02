from enum import Enum
from typing import List
from positions import Position

CardType = Enum('CardType', ['NUMBER', 'KING', 'KNIGHT', 'POTION', 'DRAGON', 'WAND'])


class Card:
    def __init__(self, card_type: CardType, value: int = 0):
        self.type = card_type
        self.value = value

    def __repr__(self):
        return self.type.name + (' ' + str(self.value))

    def get_points(self):
        return self.value


class Queen:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_points(self):
        return self.value


# c = Card(CardType.NUMBER, 7)
# print(c.get_points())


class QueenCollection:
    def __init__(self):
        self.queens: List[Queen] = []

    def addQueen(self, queen: Queen):
        self.queens.append(queen)

    def removeQueen(self, position: Position):
        self.queens.remove(position.position.card)
