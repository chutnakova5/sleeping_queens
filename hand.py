from typing import List, Optional
from cards import Card, CardType
from positions import HandPosition
from piles import DrawingAndTrashPile


class HandInterface:
    def pick_cards(self, positions: List[HandPosition]) -> Optional[List[Card]]:
        pass

    def remove_picked_cards_and_redraw(self) -> None:
        pass

    def draw_new_cards(self) -> None:
        pass

    def has_card_of_type(self, card_type: CardType) -> Optional[HandPosition]:
        pass

    def get_cards(self) -> List[Card]:
        return []

    def __contains__(self, item: Card) -> bool:
        return False


class Hand(HandInterface):
    """
    Stores cards, draws and discards.
    """
    def __init__(self, player_id: int, pile: DrawingAndTrashPile) -> None:
        self.playerID: int = player_id
        self.pile: DrawingAndTrashPile = pile
        self.cards: List[Card] = []
        self.picked_cards: List[Card] = []

    def pick_cards(self, positions: List[HandPosition]) -> Optional[List[Card]]:
        """
        Takes list of positions and creates list of cards that are in hand.
        This list is temporarily stored in self.picked_cards and returned.
        """
        self.picked_cards.clear()
        for hand_pos in positions:
            card = hand_pos.get_card()
            if card in self.cards:
                self.picked_cards.append(card)
            else:
                self.picked_cards.clear()
                return None
        return self.picked_cards

    def remove_picked_cards_and_redraw(self) -> None:
        for card in self.picked_cards:
            self.cards.remove(card)
        self.cards.extend(self.pile.discard_and_redraw(self.picked_cards))
        self.picked_cards.clear()

    def draw_new_cards(self) -> None:
        """
        Used at the beginning of game, draws 5 cards.
        """
        self.cards = self.pile.deal_cards(5)

    def has_card_of_type(self, card_type: CardType) -> Optional[HandPosition]:
        self.picked_cards.clear()
        for card in self.cards:
            if card_type == card.type:
                self.picked_cards.append(card)
                return HandPosition(card, self.playerID)
        return None

    def get_cards(self) -> List[Card]:
        return self.cards

    def __contains__(self, item: Card) -> bool:
        return item in self.cards
