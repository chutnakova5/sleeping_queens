from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from cards import Card, CardType, Queen
from positions import HandPosition, Position

if TYPE_CHECKING:
    from player import Player


class Hand:
    def __init__(self, player: Player):
        self.player = player
        game = player.game
        self.draw_pile = game.draw_pile
        self.discard_pile = game.discard_pile
        self.cards: List[Card] = []
        self.picked_cards: List[Card] = []

    def pickCards(self, positions: List[HandPosition]) -> Optional[List[Card]]:
        self.picked_cards.clear()
        picked_cards: List[Card] = []
        for hand_pos in positions:
            if hand_pos in self.cards:
                self.picked_cards.append(hand_pos.get_card())
                card = hand_pos.get_card()
                picked_cards.append(card)
            else:
                self.picked_cards.clear()
                return
        return picked_cards

    def removePickedCardsAndRedraw(self):
        to_discard: List[Card] = []
        for card in self.picked_cards:
            to_discard.append(card)
            self.cards.remove(card)
        self.discard_pile.add(to_discard)
        self.draw(len(self.picked_cards))
        self.picked_cards.clear()

    def draw(self, n: int):
        to_draw: List[Card] = self.draw_pile.take(n)
        for card in to_draw:
            self.cards.append(card)

    def hasCardOfType(self, card_type: CardType) -> Optional[HandPosition]:
        self.picked_cards.clear()
        for card in self.cards:
            if card_type == card.type:
                self.picked_cards.append(card)
                return HandPosition(card, self.player)

    def getCards(self) -> List[Card]:
        cards: List[Card] = []
        for card in self.cards:
            cards.append(card)
        return cards
