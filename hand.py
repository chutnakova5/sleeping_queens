from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from cards import Card, CardType, Queen
from positions import HandPosition, Position
from piles import DrawingAndTrashPile

if TYPE_CHECKING:
    from player import Player


class Hand:
    def __init__(self, player: Player, pile: DrawingAndTrashPile):
        self.player = player
        # game = player.game
        self.pile = pile
        self.cards: List[Card] = []
        self.picked_cards: List[Card] = []

    def pick_cards(self, positions: List[HandPosition]) -> Optional[List[Card]]:
        self.picked_cards.clear()
        for hand_pos in positions:
            card = hand_pos.get_card()
            player = hand_pos.get_player()
            if card in self.cards and player == self.player:
                self.picked_cards.append(card)
            else:
                self.picked_cards.clear()
                return
        return self.picked_cards

    def remove_picked_cards_and_redraw(self) -> None:
        for card in self.picked_cards:
            self.cards.remove(card)
        self.cards.extend(self.pile.discard_and_redraw(self.picked_cards))
        self.picked_cards.clear()

    def draw_new_cards(self) -> None:
        self.cards: List[Card] = self.pile.deal_cards(5)

    def has_card_of_type(self, card_type: CardType) -> Optional[HandPosition]:
        self.picked_cards.clear()
        for card in self.cards:
            if card_type == card.type.name:
                self.picked_cards.append(card)
                return HandPosition(card, self.player)

    def get_cards(self) -> List[Card]:
        return self.cards

    def __contains__(self, item: Card) -> bool:
        return item in self.cards
