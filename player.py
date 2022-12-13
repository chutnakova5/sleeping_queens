from typing import List, Optional

from cards import Card, Queen, CardType
from positions import HandPosition, SleepingQueenPosition, AwokenQueenPosition, Position, QueenCollection
from hand import Hand


class PlayerState:
    def __init__(self) -> None:
        self.cards: dict[HandPosition, Optional[Card]] = {}
        self.awoken_queens: dict[int, Queen] = {}


class Player:
    def __init__(self, game) -> None:
        self.player_state = PlayerState()
        self.game = game
        self.hand = Hand(self, game.pile)
        self.awoken_queens = QueenCollection(self)
        self.move_queen = MoveQueen(self.awoken_queens, game.sleeping_queens)
        self.picked_numbered_cards: List[Card] = []

    def update_player_state(self) -> None:
        dictionary = {}
        for x in self.hand.cards:
            dictionary[HandPosition(x, self)] = x
        self.player_state.cards = dictionary
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
            target_player = target_pos.get_player()
            if target_player == self:
                return
            evaluate = EvaluateAttack(attack_pos, target_pos)
            if evaluate.result is not None:
                self.hand.pick_cards(from_hand)
                self.hand.remove_picked_cards_and_redraw()
                self.update_player_state()
            return evaluate.result

        # trying to wake up a sleeping queen using king
        if len(sleeping_queens) == 1 and len(from_hand) == 1 and not awoken_queens:
            king = from_hand[0].get_card()
            target_queen = sleeping_queens[0]
            if king not in self.hand.cards:
                return
            if king.get_type() == 'KING':
                self.move_queen.wake_up(target_queen)
                self.hand.pick_cards(from_hand)
                self.hand.remove_picked_cards_and_redraw()
                self.update_player_state()
                return True
            return

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
        return sum([queen.get_points() for queen in self.awoken_queens if queen])

    def count_queens(self) -> int:
        return sum(map(lambda x: x is not None, self.awoken_queens))

    def has_card_of_type(self, card_type: CardType) -> Optional[HandPosition]:
        return self.hand.has_card_of_type(card_type)


class EvaluateAttack:
    def __init__(self, attacker: HandPosition, victim: AwokenQueenPosition) -> None:
        self.victim = victim.get_player()
        self.victim_move = victim.get_player().move_queen
        self.target_queen = victim

        self.attacker_queens = attacker.get_player().awoken_queens
        self.attack_type = attacker.get_type()

        self.result = self.evaluate()

    def evaluate(self) -> Optional[bool]:
        """
        Decides whether attack was successful, plays defense card or calls methods to move queen.
        """
        if self.target_queen.get_card() not in self.victim_move.awoken_queens:
            return None

        if self.attack_type == 'KNIGHT':
            if self.victim.has_card_of_type('DRAGON'):           # victim plays a defense card
                self.victim.hand.remove_picked_cards_and_redraw()
                return False
            else:                                               # moving queen to the attacker's collection
                self.victim_move.move_awoken(self.target_queen, self.attacker_queens)
                return True

        if self.attack_type == 'POTION':
            if self.victim.has_card_of_type('WAND'):            # victim plays a defense card
                self.victim.hand.remove_picked_cards_and_redraw()
                return False
            else:                                               # moving queen to sleeping queens collection
                self.victim_move.put_to_sleep(self.target_queen)
                return True


class MoveQueen:
    def __init__(self, awoken_queens: QueenCollection, sleeping_queens: QueenCollection) -> None:
        self.awoken_queens = awoken_queens
        self.sleeping_queens = sleeping_queens

    def move_awoken(self, position: Position, destination: QueenCollection) -> Optional[bool]:
        """
        Player calls this method to move his awoken queen to other player's collection.
        """
        return self.move(position.get_card(), self.awoken_queens, destination)

    def wake_up(self, position: Position) -> Optional[bool]:
        """
        Player calls this method to wake a sleeping queen and move it to his collection.
        """
        return self.move(position.get_card(), self.sleeping_queens, self.awoken_queens)

    def put_to_sleep(self, position: Position) -> Optional[bool]:
        """
        Player calls this method to put his awoken queen back to sleep.
        """
        return self.move(position.get_card(), self.awoken_queens, self.sleeping_queens)

    @staticmethod
    def move(card: Queen, source: QueenCollection, destination: QueenCollection) -> Optional[bool]:
        """
        Moves queen from one QueenCollection to another.
        """
        if card not in source:
            return None
        source.remove_queen(card)
        destination.add_queen(card)
        return True
