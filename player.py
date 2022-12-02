from Piles import DrawPile, DiscardPile
from Cards import Card, CardType, Queen
from Positions import HandPosition
from typing import List, Optional
from Game import Game


class Player:
    def __init__(self):
        self.hand = Hand(self)

    def evaluate_numbered_cards(self):
        numbered_cards: List[Card] = list(filter(lambda x: x.type == 'NUMBER', self.hand.getCards()))
        numbered_cards.sort()
        # if len(set(numbered_cards)

    def play(self):
        pass


class PlayerState:
    def __init__(self, player: Player):
        self.player = player
        self.cards: dict[HandPosition, Optional[Card]] = {}
        self.awoken_queens: dict[int, Queen] = {}


class Hand:
    def __init__(self, player: Player):
        self.player = player
        self.draw_pile = Game.draw_pile
        self.discard_pile = Game.discard_pile
        self.cards: List[HandPosition] = []

    def pickCards(self, positions: List[HandPosition]) -> Optional[List[Card]]:
        n = len(positions)
        to_discard: List[Card] = []
        for hand_pos in positions:
            card = hand_pos.card
            to_discard.append(card)
            self.cards.remove(hand_pos)
        self.discard_pile.discard(to_discard)
        return to_discard

    def draw(self, n: int):
        to_draw: List[Card] = self.draw_pile.draw(n)
        for card in to_draw:
            self.cards.append(HandPosition(card))

    def hasCardOfType(self, card_type: CardType) -> Optional[HandPosition]:
        for hp in self.cards:
            if card_type == hp.card.type:
                return hp

    def getCards(self) -> List[Card]:
        cards: List[Card] = []
        for hp in self.cards:
            cards.append(hp.card)
        return cards
