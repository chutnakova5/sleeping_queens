from random import shuffle
from typing import List, Callable

from cards import Card, CardType

number_of_cards = {
    CardType.NUMBER: 4, CardType.KING: 8, CardType.KNIGHT: 4, CardType.POTION: 4, CardType.DRAGON: 3, CardType.WAND: 3
}


class StrategyInterface:
    @staticmethod
    def not_enough_cards(to_discard: List[Card], draw_pile: List[Card], trash_pile: List[Card],
                         discard: Callable, draw: Callable) -> List[Card]:
        return [Card(CardType.NUMBER)]


class Strategy1(StrategyInterface):
    @staticmethod
    def not_enough_cards(to_discard: List[Card], draw_pile: List[Card], trash_pile: List[Card],
                         discard: Callable, draw: Callable) -> List[Card]:
        """
        Version 1:
        When there are not enough cards, the playerID throws his cards,
        draws what he can and then shuffles the discard pile and draw remaining cards.
        """
        in_draw_pile = len(draw_pile)
        discard(to_discard)
        to_draw = draw(in_draw_pile)
        shuffle(trash_pile)
        draw_pile[:] = trash_pile[:]
        trash_pile.clear()
        to_draw.extend(draw(len(to_discard) - in_draw_pile))
        return to_draw


class Strategy2(StrategyInterface):
    @staticmethod
    def not_enough_cards(to_discard: List[Card], draw_pile: List[Card], trash_pile: List[Card],
                         discard: Callable, draw: Callable) -> List[Card]:
        """
        Version 2:
        If there are not enough cards in the deck, shuffle the discard pile and put it under the deck,
        then discard used cards and draw cards.
        """
        shuffle(trash_pile)
        draw_pile[:] = trash_pile[:] + draw_pile[:]
        trash_pile.clear()
        discard(to_discard)
        return draw(len(to_discard))


class DrawingAndTrashPile:
    def __init__(self, strategy: StrategyInterface) -> None:
        self.draw_pile: List[Card] = []         # cards will be drawn from the end of list
        self.trash_pile: List[Card] = []

        for card_type in CardType:      # generating the deck of cards
            if card_type == CardType.NUMBER:
                self.draw_pile += [Card(card_type, i) for i in range(1, 11) for _ in range(number_of_cards[card_type])]
            else:
                self.draw_pile += [Card(card_type) for _ in range(number_of_cards[card_type])]
        shuffle(self.draw_pile)

    def __repr__(self):
        return ', '.join(map(str, self.draw_pile))

    def deal_cards(self, n: int) -> List[Card]:
        return self._draw(n)

    def discard_and_redraw(self, to_discard: List[Card]) -> List[Card]:
        """
        Puts cards from list to discard pile and takes the same number of cards from draw pile.
        """
        in_draw_pile = len(self.draw_pile)
        if len(to_discard) >= in_draw_pile:         # there are not enough cards in the draw pile
            return self.not_enough_cards(to_discard)
            # return self.not_enough_cards_v2(to_discard)
        self.discard(to_discard)
        return self._draw(len(to_discard))

    def not_enough_cards(self, to_discard: List[Card]) -> List[Card]:
        """
        Version 1:
        When there are not enough cards, the playerID throws his cards,
        draws what he can and then shuffles the discard pile and draw remaining cards.
        """
        in_draw_pile = len(self.draw_pile)
        self.discard(to_discard)
        to_draw = self._draw(in_draw_pile)
        shuffle(self.trash_pile)
        self.draw_pile = self.trash_pile[:]
        self.trash_pile.clear()
        to_draw.extend(self._draw(len(to_discard) - in_draw_pile))
        return to_draw

    def not_enough_cards_v2(self, to_discard: List[Card]) -> List[Card]:
        """
        Version 2:
        If there are not enough cards in the deck, shuffle the discard pile and put it under the deck,
        then discard used cards and draw cards.
        """
        shuffle(self.trash_pile)
        self.draw_pile = self.trash_pile[:] + self.draw_pile[:]
        self.trash_pile.clear()
        self.discard(to_discard)
        return self._draw(len(to_discard))

    def discard(self, to_discard: List[Card]):
        self.trash_pile.extend(to_discard)

    def _draw(self, n: int) -> List[Card]:
        to_draw = self.draw_pile[-n:]
        self.draw_pile = self.draw_pile[:-n]
        return to_draw
