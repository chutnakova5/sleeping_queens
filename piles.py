from random import shuffle
from typing import List

from cards import Card, CardType, Queen

number_of_cards = {
    CardType.NUMBER: 4, CardType.KING: 8, CardType.KNIGHT: 4, CardType.POTION: 4, CardType.DRAGON: 3, CardType.WAND: 3
}

queen_info = {"Rose Queen": 5, "Cake Queen": 5, "Rainbow Queen": 5, "Starfish Queen": 5,
              "Moon Queen": 10, "Peacock Queen": 10, "Ladybug Queen": 10, "Sunflower Queen": 10,
              "Pancake Queen": 15, "Cat Queen": 15, "Dog Queen": 15, "Heart Queen": 20}

queens = []
for name, value in queen_info.items():
    queens.append(Queen(name, value))
shuffle(queens)


class DrawPile:
    def __init__(self):
        self._cards = []
        for card_type in CardType:
            if card_type == CardType.NUMBER:
                self._cards += [Card(card_type, i) for i in range(1, 11) for _ in range(number_of_cards[card_type])]
            else:
                self._cards += [Card(card_type) for _ in range(number_of_cards[card_type])]
        shuffle(self._cards)

    def __repr__(self):
        return ', '.join(map(str, self._cards))

    def take(self, n: int) -> List[Card]:
        to_draw = self._cards[-n:]
        self._cards = self._cards[:-n]
        return to_draw


class DiscardPile:
    def __init__(self):
        self._cards = []

    def __repr__(self):
        return ', '.join(map(str, self._cards))

    def add(self, to_discard: List[Card]):
        self._cards.extend(to_discard)


# a = DrawPile()
# print(a)
# b = DiscardPile()
# cards = a.draw(3)
# print(cards)
# b.discard(cards)
# print(b)
