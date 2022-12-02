from Piles import DrawPile, DiscardPile
from Cards import Card, CardType, Queen
from Positions import HandPosition, Position
from typing import List, Optional
from Game import Game


class PlayerState:
    def __init__(self):
        self.cards: dict[HandPosition, Optional[Card]] = {}
        self.awoken_queens: dict[int, Queen] = {}


class Player:
    def __init__(self):
        self.player_state = PlayerState()
        self.hand = Hand(self)
        self.picked_numbered_cards: List[Card] = []

    def evaluate_numbered_cards(self):
        for i in range(len(self.picked_numbered_cards)):
            other_cards = self.picked_numbered_cards[:i] + self.picked_numbered_cards[i:]
            sum_value = sum(map(lambda x: x.value, other_cards))
            card_value = self.picked_numbered_cards[i].value
            if card_value == sum_value:
                return True
        return False

    def play(self, positions: List[Position]) -> Optional[PlayerState]:
        from_hand: List[HandPosition] = []
        for pos in positions:
            if type(pos.position) == HandPosition:
                from_hand.append(pos.position)
            else:
                pass
        cards_from_hand: List[Card] = self.hand.pickCards(from_hand)
        self.picked_numbered_cards.clear()
        for card in cards_from_hand:
            if card.type == 'NUMBER':
                self.picked_numbered_cards.append(card)
        if len(self.picked_numbered_cards) == len(positions):       # vsetky zvolene karty su cisla
            if self.evaluate_numbered_cards():                      # splnene suctove pravidlo
                return self.player_state
            return
        elif len(self.picked_numbered_cards) != 0:                  # nejaky divny mix
            return


class Hand:
    def __init__(self, player: Player):
        self.player = player
        self.draw_pile = Game.draw_pile
        self.discard_pile = Game.discard_pile
        self.cards: List[HandPosition] = []
        self.picked_positions: List[HandPosition] = []

    def pickCards(self, positions: List[HandPosition]) -> Optional[List[Card]]:
        n = len(positions)
        self.picked_positions.clear()
        picked_cards: List[Card] = []
        for hand_pos in positions:
            self.picked_positions.append(hand_pos)
            card = hand_pos.getCard()
            picked_cards.append(card)
        return picked_cards

    def removePickedCardsAndRedraw(self):
        to_discard: List[Card] = []
        for hand_pos in self.picked_positions:
            card = hand_pos.getCard()
            if card.type in ('NUMBER',):            # musim pozriet pravidla
                to_discard.append(card)
            else:
                pass
            self.cards.remove(hand_pos)
        self.discard_pile.discard(to_discard)
        self.draw(len(self.picked_positions))
        self.picked_positions.clear()

    def draw(self, n: int):
        to_draw: List[Card] = self.draw_pile.draw(n)
        for card in to_draw:
            self.cards.append(HandPosition(card, self.player))

    def hasCardOfType(self, card_type: CardType) -> Optional[HandPosition]:
        for hp in self.cards:
            if card_type == hp.card.type:
                return hp

    def getCards(self) -> List[Card]:
        cards: List[Card] = []
        for hp in self.cards:
            cards.append(hp.card)
        return cards
