from unittest import TestCase
from unittest.mock import Mock, MagicMock

from player import Player, EvaluateAttack
from hand import Hand
from cards import Card, CardType, Queen
from positions import HandPosition, AwokenQueenPosition, SleepingQueenPosition
from piles import DrawingAndTrashPile
from game import Game


class TestPlayerSolitary(TestCase):
    def setUp(self) -> None:
        self.game = Mock()
        self.game.pile = Mock()
        self.player = Player(self.game)
        self.cards_from_hand = [Card(CardType.NUMBER, 7), Card(CardType.NUMBER, 1), Card(CardType.NUMBER, 3),
                                Card(CardType.NUMBER, 5), Card(CardType.NUMBER, 1)]
        self.player.hand = Mock()
        self.player.hand.cards = self.cards_from_hand
        self.player.hand.pick_cards = MagicMock(return_value=self.cards_from_hand)

        self.numbers_ok1 = [HandPosition(Card(CardType.NUMBER, 7), self.player)]
        self.numbers_ok2 = [HandPosition(Card(CardType.NUMBER, 1), self.player),
                            HandPosition(Card(CardType.NUMBER, 1), self.player)]
        self.numbers_ok3 = [HandPosition(Card(CardType.NUMBER, 5), self.player),
                            HandPosition(Card(CardType.NUMBER, 1), self.player),
                            HandPosition(Card(CardType.NUMBER, 7), self.player),
                            HandPosition(Card(CardType.NUMBER, 1), self.player)]

        self.numbers_w1 = [HandPosition(Card(CardType.NUMBER, 10), self.player)]
        self.numbers_w2 = [HandPosition(Card(CardType.NUMBER, 1), self.player),
                           HandPosition(Card(CardType.NUMBER, 3), self.player)]
        self.numbers_w3 = [HandPosition(Card(CardType.NUMBER, 3), self.player),
                           HandPosition(Card(CardType.NUMBER, 5), self.player),
                           HandPosition(Card(CardType.NUMBER, 1), self.player)]
        self.numbers_w4 = [HandPosition(Card(CardType.NUMBER, 5), self.player),
                           HandPosition(Card(CardType.KING, 0), self.player)]

        self.cards_ok1 = [HandPosition(Card(CardType.POTION, 0), self.player),
                          AwokenQueenPosition(Queen('Rose Queen', 5), Mock())]
        self.cards_ok2 = [HandPosition(Card(CardType.KING, 0), self.player),
                          SleepingQueenPosition(Queen('Rose Queen', 5))]
        self.cards_w1 = [HandPosition(Card(CardType.POTION, 0), self.player),
                         AwokenQueenPosition(Queen('Rose Queen', 5), self.player)]
        self.cards_w2 = [HandPosition(Card(CardType.KING, 0), self.player),
                         HandPosition(Card(CardType.POTION, 0), Mock())]

    def set_cards_from_hand(self, positions):
        cards = [pos.get_card() for pos in positions if type(pos) == HandPosition]
        self.player.hand.cards = cards
        self.player.hand.pick_cards = MagicMock(return_value=cards)

    def test_play_numbered(self):
        self.set_cards_from_hand(self.numbers_ok1)
        self.assertTrue(self.player.play(self.numbers_ok1))

        self.set_cards_from_hand(self.numbers_ok2)
        self.assertTrue(self.player.play(self.numbers_ok2))
        self.set_cards_from_hand(self.numbers_ok3)
        self.assertTrue(self.player.play(self.numbers_ok3))

        self.set_cards_from_hand([])
        self.assertIsNone(self.player.play(self.numbers_w1))
        self.set_cards_from_hand(self.numbers_w2)
        self.assertIsNone(self.player.play(self.numbers_w2))
        self.set_cards_from_hand(self.numbers_w3)
        self.assertIsNone(self.player.play(self.numbers_w3))
        self.set_cards_from_hand(self.numbers_w4)
        self.assertIsNone(self.player.play(self.numbers_w4))

    def test_play_attack(self):
        EvaluateAttack.evaluate = MagicMock(return_value=False)
        self.player.move_queen.move = MagicMock(return_value=False)

        self.assertFalse(self.player.play(self.cards_ok1))
        self.assertFalse(self.player.play(self.cards_ok2))

        EvaluateAttack.evaluate = MagicMock(return_value=True)
        self.player.move_queen.move = MagicMock(return_value=True)

        self.set_cards_from_hand(self.cards_ok1)
        self.assertTrue(self.player.play(self.cards_ok1))
        self.set_cards_from_hand(self.cards_ok2)
        self.assertTrue(self.player.play(self.cards_ok2))

        self.set_cards_from_hand(self.cards_w1)
        self.assertFalse(self.player.play(self.cards_w1))
        self.set_cards_from_hand(self.cards_ok2)
        self.assertFalse(self.player.play(self.cards_w2))
