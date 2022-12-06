from enum import Enum


CardType = Enum('CardType', ['NUMBER', 'KING', 'KNIGHT', 'POTION', 'DRAGON', 'WAND'])


class Card:
    def __init__(self, card_type: CardType, value: int = 0):
        self.type = card_type
        self._value = value

    def __repr__(self):
        return self.type.name + ' ' + str(self._value)

    def get_points(self):
        return self._value

    def get_type(self):
        return self.type.name


class Queen:
    def __init__(self, name, value):
        self.name = name
        self._value = value

    def get_points(self):
        return self._value

    def __repr__(self):
        return self.name + ' ' + str(self._value)
