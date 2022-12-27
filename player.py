from __future__ import annotations

from typing import List, Optional

from cards import Card, Queen, CardType
from positions import HandPosition, SleepingQueenPosition, AwokenQueenPosition, Position, QueenCollectionInterface
from hand import HandInterface
from evaluate import EvaluateAttackInterface, MoveQueenInterface


class PlayerState:
    def __init__(self) -> None:
        self.cards: List[Card] = []
        self.awoken_queens: List[Optional[Queen]] = []


class Player:
    def __init__(self, hand: HandInterface, awoken_queens: QueenCollectionInterface,
                 move_queen: MoveQueenInterface, eval_attack: EvaluateAttackInterface,
                 player_state: PlayerState) -> None:
        self.hand = hand
        self.awoken_queens = awoken_queens
        self.move_queen = move_queen
        self.evaluate = eval_attack.evaluate
        self.player_state = player_state
        self.picked_numbered_cards: List[Card] = []

    def update_player_state(self) -> None:
        self.player_state.cards = self.hand.get_cards()
        self.player_state.awoken_queens = self.awoken_queens.get_queens()

    def play(self, positions: List[Position]) -> Optional[bool]:
        from_hand: List[HandPosition] = [
            pos for pos in positions if type(pos) == HandPosition]
        sleeping_queens: List[SleepingQueenPosition] = [
            pos for pos in positions if type(pos) == SleepingQueenPosition]
        awoken_queens: List[AwokenQueenPosition] = [
            pos for pos in positions if type(pos) == AwokenQueenPosition]

        # attack on somebody else's awoken queen
        if len(awoken_queens) == 1 and len(from_hand) == 1 and not sleeping_queens:
            attack_pos = from_hand[0]
            target_pos = awoken_queens[0]
            result = self.evaluate(attack_pos, target_pos)
            if result is not None:
                self.hand.pick_cards(from_hand)
                self.hand.remove_picked_cards_and_redraw()
                self.update_player_state()
            return result

        # trying to wake up a sleeping queen using a king
        if len(sleeping_queens) == 1 and len(from_hand) == 1 and not awoken_queens:
            king = from_hand[0].get_card()
            target_queen = sleeping_queens[0]
            if king not in self.hand.get_cards():
                return None
            if king.get_type() == 'KING':
                self.move_queen.wake_up(target_queen)
                self.hand.pick_cards(from_hand)
                self.hand.remove_picked_cards_and_redraw()
                self.update_player_state()
                return True
            return None

        cards_from_hand = self.hand.pick_cards(from_hand)
        self.picked_numbered_cards.clear()
        for card in cards_from_hand or []:
            if card.type == CardType.NUMBER:
                self.picked_numbered_cards.append(card)
        if len(self.picked_numbered_cards) == len(positions):       # all picked cards are numbered
            if self.evaluate_numbered_cards():
                self.hand.remove_picked_cards_and_redraw()
                self.update_player_state()
                return True
        return None

    def evaluate_numbered_cards(self) -> bool:
        """
        Checks if current move is valid according to game rules.
        """
        cards = self.picked_numbered_cards
        count = len(cards)
        if count == 1 or (count == 2 and cards[0].get_points() == cards[1].get_points()):
            return True
        values = sorted(list(map(lambda x: x.get_points(), cards)))
        if sum(values[:-1], ) == values[-1]:
            return True
        return False

    def remove_queen(self, queen: Queen) -> None:
        self.awoken_queens.remove_queen(queen)

    def add_queen(self, queen: Queen) -> None:
        self.awoken_queens.add_queen(queen)

    def count_points(self) -> int:
        return self.awoken_queens.count_points()

    def count_queens(self) -> int:
        return self.awoken_queens.count_queens()

    def has_card_of_type(self, card_type: CardType) -> Optional[HandPosition]:
        return self.hand.has_card_of_type(card_type)
