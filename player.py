from __future__ import annotations
from typing import List, Optional, Union, TYPE_CHECKING

from cards import Card, Queen
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
        self.awoken_queens = QueenCollection(self)
        self.move_queen = MoveQueen(self.awoken_queens, game.sleeping_queens)
        self.picked_numbered_cards: List[Card] = []

    def play(self, positions: List[Position]) -> Optional[bool]:
        from_hand: List[HandPosition] = [
            pos for pos in positions if type(pos) == HandPosition]
        sleeping_queens: List[SleepingQueenPosition] = [
            pos for pos in positions if type(pos) == SleepingQueenPosition]
        awoken_queens: List[AwokenQueenPosition] = [
            pos for pos in positions if type(pos) == AwokenQueenPosition]

        if len(awoken_queens) == 1 and len(from_hand) == 1 and not sleeping_queens:
            attack_pos = from_hand[0]
            target_pos = awoken_queens[0]
            target_player = target_pos.get_player()
            if target_player == self:
                return
            evaluate = EvaluateAttack(attack_pos, target_pos)
            if evaluate.result is True:
                self.hand.pickCards(from_hand)
                self.hand.removePickedCardsAndRedraw()
            return evaluate.result

        if len(sleeping_queens) == 1 and len(from_hand) == 1 and not awoken_queens:
            king = from_hand[0].get_card()
            target_queen = sleeping_queens[0]
            if king.get_type() == 'KING':
                result = self.move_queen.move(target_queen, self.awoken_queens)
                if result is True:
                    self.hand.pickCards(from_hand)
                    self.hand.removePickedCardsAndRedraw()
                return result
            return

        cards_from_hand = self.hand.pickCards(from_hand)
        self.picked_numbered_cards.clear()
        for card in cards_from_hand:
            if card.type == 'NUMBER':
                self.picked_numbered_cards.append(card)
        if len(self.picked_numbered_cards) == len(positions):       # all picked cards are numbered
            if self.evaluate_numbered_cards():
                self.hand.removePickedCardsAndRedraw()
                return True

    def evaluate_numbered_cards(self):
        cards = self.picked_numbered_cards
        count = len(cards)
        if count == 1 or (count == 2 and cards[0].get_points() == cards[1].get_points()):
            return True
        values = sorted(list(map(lambda x: x.value, cards)))
        if sum(values[:-1], ) == values[-1]:
            return True
        return False

    def remove_queen(self, queen: Queen):
        self.awoken_queens.remove_queen(queen)

    def add_queen(self, queen: Queen):
        self.awoken_queens.add_queen(queen)


class EvaluateAttack:
    def __init__(self, attacker: HandPosition, victim: AwokenQueenPosition):
        # self.attacker_hand = attacker.get_player().hand
        self.victim_hand = victim.get_player().hand

        # self.attacker_move = attacker.get_player().move_queen
        self.attacker_queens = attacker.get_player().awoken_queens
        self.victim_move = victim.get_player().move_queen

        self.attack_type = attacker.get_card().get_type()
        self.target_queen = victim

        self.result = self.evaluate()

    def evaluate(self):
        if self.attack_type == 'KNIGHT':
            if self.victim_hand.hasCardOfType('DRAGON'):
                self.victim_hand.removePickedCardsAndRedraw()
                return False
            else:
                self.victim_move.move(self.target_queen, self.attacker_queens)

        if self.attack_type == 'POTION':
            if self.victim_hand.hasCardOfType('WAND'):
                self.victim_hand.removePickedCardsAndRedraw()
                return False
            else:
                self.victim_move.move(self.target_queen)

        return True


class MoveQueen:
    def __init__(self, awoken_queens: QueenCollection, sleeping_queens: QueenCollection):
        self.awoken_queens = awoken_queens
        self.sleeping_queens = sleeping_queens

    def move(self, position: Position, destination: Optional[QueenCollection] = None) -> bool:
        if position is None and destination is None:
            return False

        if type(position) == SleepingQueenPosition:
            source = self.sleeping_queens
        else:
            source = self.awoken_queens

        if destination is None:
            destination = self.sleeping_queens

        card = position.get_card()
        if card not in source:
            return False
        source.remove_queen(card)
        destination.add_queen(card)
        return True
