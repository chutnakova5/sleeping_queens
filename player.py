from __future__ import annotations
from typing import List, Optional, Union, TYPE_CHECKING

from cards import Card, CardType, Queen
from positions import HandPosition, SleepingQueenPosition, AwokenQueenPosition, Position, QueenCollection
from hand import Hand
if TYPE_CHECKING:
    from game import Game


class PlayerState:
    def __init__(self):
        self.cards: dict[HandPosition, Optional[Card]] = {}
        self.awoken_queens: dict[int, Queen] = {}


class Player:
    def __init__(self, game):
        self.player_state = PlayerState()
        self.game = game
        self.hand = Hand(self)
        self.awoken_queens = QueenCollection()
        self.picked_numbered_cards: List[Card] = []

    def play(self, positions: List[Position]) -> Optional[PlayerState]:
        from_hand: List[HandPosition] = [
            pos.position for pos in positions if type(pos.position) == HandPosition]
        sleeping_queens: List[SleepingQueenPosition] = [
            pos.position for pos in positions if type(pos.position) == SleepingQueenPosition]
        awoken_queens: List[AwokenQueenPosition] = [
            pos.position for pos in positions if type(pos.position) == AwokenQueenPosition]

        if len(awoken_queens) == 1 and len(from_hand) == 1 and not sleeping_queens:
            attack_pos = from_hand[0]
            target_pos = awoken_queens[0]
            target_queen = target_pos.getCard()

            target_player = target_pos.getPlayer()
            target_player.evaluate_attack(target_queen, attack_pos)
            return self.player_state

        if len(sleeping_queens) == 1 and len(from_hand) == 1 and not awoken_queens:
            king = from_hand[0].getCard()
            target_queen = sleeping_queens[0]
            if king.get_type() == 'KING':
                MoveQueen(target_queen, self.game, self)
                return self.player_state
            return

        cards_from_hand = self.hand.pickCards(from_hand)
        self.picked_numbered_cards.clear()
        for card in cards_from_hand:  # evaluate numbered cards
            if card.type == 'NUMBER':
                self.picked_numbered_cards.append(card)
        if len(self.picked_numbered_cards) == len(positions):  # vsetky zvolene karty su cisla
            if self.evaluate_numbered_cards():
                self.hand.removePickedCardsAndRedraw()
                return self.player_state

    def evaluate_numbered_cards(self):
        cards = self.picked_numbered_cards
        count = len(cards)
        if count == 1 or (count == 2 and cards[0].get_points() == cards[1].get_points()):
            return True
        values = list(map(lambda x: x.value, cards))
        cards = sorted(cards, key=lambda x: x.value)
        if sum(cards[:-1]) == cards[-1]:
            return True
        # for i in range(count):
        #     other_cards = cards[:i] + cards[i:]
        #     sum_value = sum(map(lambda x: x.value, other_cards))
        #     card_value = cards[i].get_points()
        #     if card_value == sum_value:
        #         return True
        return False

    def evaluate_attack(self, target_queen: Queen, attack: HandPosition) -> Optional[bool]:
        if target_queen not in self.awoken_queens:  # invalid move
            return None

        if attack.getCard().get_type() == 'KNIGHT':
            if self.hand.hasCardOfType('DRAGON'):
                self.hand.removePickedCardsAndRedraw()
                return False
            else:
                MoveQueen(target_queen, self, attack.getPlayer())

        if attack.getCard().get_type() == 'POTION':
            if self.hand.hasCardOfType('WAND'):
                self.hand.removePickedCardsAndRedraw()
                return False
            else:
                MoveQueen(target_queen, self, self.game)
        return True

    def remove_queen(self, queen: Queen):
        self.awoken_queens.removeQueen(queen)

    def add_queen(self, queen: Queen):
        self.awoken_queens.addQueen(queen)


class MoveQueen:
    def __init__(self, queen, source: Union[Player, Game], destination: Union[Player, Game]):
        source.remove_queen(queen)
        destination.add_queen(queen)

