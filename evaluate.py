from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from cards import Queen, CardType
from positions import HandPosition, AwokenQueenPosition, Position, QueenCollectionInterface
if TYPE_CHECKING:
    from player import Player


class EvaluateAttackInterface:
    def evaluate(self, attacker_pos: HandPosition, victim_pos: AwokenQueenPosition) -> Optional[bool]:
        pass


class EvaluateAttack(EvaluateAttackInterface):
    def __init__(self, players: List[Player]) -> None:
        self.players: List[Player] = players

    def evaluate(self, attacker_pos: HandPosition, victim_pos: AwokenQueenPosition) -> Optional[bool]:
        """
        Decides whether attack was successful, plays defense card or calls methods to move queen.
        """
        attacker = self.players[attacker_pos.get_playerID()]
        victim = self.players[victim_pos.get_playerID()]

        if attacker_pos.get_type() == 'KNIGHT':
            if victim.has_card_of_type(CardType.DRAGON):           # victim plays a defense card
                victim.hand.remove_picked_cards_and_redraw()
                return False
            # moving queen to the attacker's collection
            victim.move_queen.move_awoken(victim_pos, attacker.awoken_queens)
            return True
        if attacker_pos.get_type() == 'POTION':
            if victim.has_card_of_type(CardType.WAND):             # victim plays a defense card
                victim.hand.remove_picked_cards_and_redraw()
                return False
            # moving queen to sleeping queens collection
            victim.move_queen.put_to_sleep(victim_pos)
            return True
        return None


class MoveQueenInterface:
    def move_awoken(self, position: Position, destination: QueenCollectionInterface) -> Optional[bool]:
        pass

    def wake_up(self, position: Position) -> Optional[bool]:
        pass

    def put_to_sleep(self, position: Position) -> Optional[bool]:
        pass


class MoveQueen(MoveQueenInterface):
    def __init__(self, awoken_queens: QueenCollectionInterface, sleeping_queens: QueenCollectionInterface) -> None:
        self.awoken_queens = awoken_queens
        self.sleeping_queens = sleeping_queens

    def move_awoken(self, position: Position, destination: QueenCollectionInterface) -> Optional[bool]:
        """
        Player calls this method to move his awoken queen to other playerID's collection.
        """
        return self._move(position.get_card(), self.awoken_queens, destination)

    def wake_up(self, position: Position) -> Optional[bool]:
        """
        Player calls this method to wake a sleeping queen and move it to his collection.
        """
        return self._move(position.get_card(), self.sleeping_queens, self.awoken_queens)

    def put_to_sleep(self, position: Position) -> Optional[bool]:
        """
        Player calls this method to put his awoken queen back to sleep.
        """
        return self._move(position.get_card(), self.awoken_queens, self.sleeping_queens)

    @staticmethod
    def _move(card: Queen, source: QueenCollectionInterface, destination: QueenCollectionInterface) -> Optional[bool]:
        """
        Moves queen from one QueenCollection to another.
        """
        if card not in source:
            return None
        source.remove_queen(card)
        destination.add_queen(card)
        return True
