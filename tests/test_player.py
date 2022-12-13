from unittest import TestCase
from unittest.mock import Mock, MagicMock

from game import Game
from player import Player, EvaluateAttack
from cards import Card, CardType, Queen
from positions import HandPosition, AwokenQueenPosition, SleepingQueenPosition


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


class TestPlayerSociable(TestCase):
    def setUp(self):
        self.game = Game(5, Mock())
        self.player = Player(self.game)
        self.other_player = Player(self.game)
        self.player.hand.cards = [Card(CardType.NUMBER, 7), Card(CardType.NUMBER, 1),
                                  Card(CardType.NUMBER, 3), Card(CardType.NUMBER, 5),
                                  Card(CardType.NUMBER, 1)]
        self.other_player.cards = [Card(CardType.NUMBER, 3), Card(CardType.POTION, 0)]

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
        self.numbers_w5 = [HandPosition(Card(CardType.NUMBER, 1), self.player),
                           HandPosition(Card(CardType.NUMBER, 3), self.other_player)]

        self.cards_ok1 = [HandPosition(Card(CardType.POTION, 0), self.player),
                          AwokenQueenPosition(Queen('Rose Queen', 5), self.other_player)]
        self.cards_ok2 = [HandPosition(Card(CardType.KING, 0), self.player),
                          SleepingQueenPosition(Queen('Moon Queen', 10))]
        self.cards_w1 = [HandPosition(Card(CardType.POTION, 0), self.player),
                         AwokenQueenPosition(Queen('Rose Queen', 5), self.player)]
        self.cards_w2 = [HandPosition(Card(CardType.KING, 0), self.player),
                         HandPosition(Card(CardType.POTION, 0), self.other_player)]

    def test_awoken_queens(self):
        self.assertTrue(self.player.awoken_queens.queens == [])
        queen1 = Queen('Peacock Queen', 10)
        queen2 = Queen('Pancake Queen', 15)
        self.player.add_queen(queen1)
        self.assertEqual(self.player.awoken_queens.queens, [queen1])
        self.player.add_queen(queen2)
        queens = {pos.get_card() for pos in self.player.awoken_queens.get_queens()}
        self.assertSetEqual(queens, {queen1, queen2})
        self.player.remove_queen(queen1)
        self.assertEqual(self.player.awoken_queens.queens, [None, queen2])

    def test_move(self):
        self.assertFalse(self.player.awoken_queens.queens or self.other_player.awoken_queens.queens)
        queen1 = self.game.sleeping_queens.queens[0]
        queen2 = self.game.sleeping_queens.queens[7]
        self.player.move_queen.wake_up(SleepingQueenPosition(queen1))
        self.assertIsNone(self.game.sleeping_queens.queens[0])
        self.assertEqual(self.player.awoken_queens.queens, [queen1])
        self.player.move_queen.wake_up(SleepingQueenPosition(queen2))
        self.assertTrue(self.game.sleeping_queens.queens[0] is None
                        and self.game.sleeping_queens.queens[7] is None)
        self.assertTrue(len(self.game.sleeping_queens.get_queens()) == 10)

        self.player.move_queen.move_awoken(AwokenQueenPosition(queen2, self.player), self.other_player.awoken_queens)
        self.assertEqual(self.other_player.awoken_queens.queens, [queen2])
        self.assertEqual(self.player.awoken_queens.queens, [queen1, None])
        self.other_player.move_queen.move_awoken(AwokenQueenPosition(queen2, self.other_player), self.player.awoken_queens)
        self.assertEqual(self.player.awoken_queens.queens, [queen1, queen2])

    def test_move_fail(self):
        queen1 = self.game.sleeping_queens.queens[0]
        queen2 = self.game.sleeping_queens.queens[7]
        self.player.move_queen.wake_up(SleepingQueenPosition(queen1))
        self.assertFalse(self.player.move_queen.wake_up(SleepingQueenPosition(queen1)))
        self.assertFalse(self.player.move_queen.move_awoken(AwokenQueenPosition(queen2, self.other_player), self.player))

    def test_play(self):
        king1, knight1, knight11, potion1, dragon1 = (Card(CardType.KING), Card(CardType.KNIGHT), Card(CardType.KNIGHT),
                                                      Card(CardType.POTION), Card(CardType.DRAGON))
        self.player.hand.cards = [knight1, potion1, king1, dragon1, knight11]
        number2, potion2, king2, dragon2, wand2 = (Card(CardType.NUMBER, 2), Card(CardType.POTION), Card(CardType.KING),
                                                   Card(CardType.DRAGON), Card(CardType.WAND))
        self.other_player.hand.cards = [number2, potion2, king2, dragon2, wand2]

        self.player.hand.pile.draw_pile[-10:] = [Card(CardType.NUMBER, -1) for _ in range(10)]
        self.assertTrue(len(self.player.hand.pile.draw_pile) == 62 - self.game.get_number_of_players() * 5)

        queen1 = self.game.sleeping_queens.queens[0]
        queen2 = self.game.sleeping_queens.queens[10]
        self.assertTrue(self.player.play([HandPosition(king1, self.player), SleepingQueenPosition(queen1)]))

        self.assertIsNone(self.game.sleeping_queens.queens[0])
        self.assertFalse(self.player.play([HandPosition(king1, self.player), SleepingQueenPosition(queen1)]))
        self.other_player.play([HandPosition(king2, self.other_player), SleepingQueenPosition(queen2)])
        self.other_player.hand.cards = [number2, potion2, king2, dragon2, wand2]
        self.assertFalse(self.player.play([HandPosition(knight1, self.player),
                                           AwokenQueenPosition(queen2, self.other_player)]))
        self.assertTrue(self.player.play([HandPosition(knight11, self.player),
                                          AwokenQueenPosition(queen2, self.other_player)]))

    def test_play_numbered(self):
        cards = [Card(CardType.NUMBER, 7), Card(CardType.NUMBER, 1), Card(CardType.NUMBER, 3), Card(CardType.NUMBER, 5),
                 Card(CardType.NUMBER, 1)]
        self.player.hand.cards = cards[:]

        self.numbers_ok1 = [HandPosition(cards[0], self.player)]
        self.numbers_ok2 = [HandPosition(cards[1], self.player), HandPosition(cards[4], self.player)]
        self.numbers_ok3 = [HandPosition(cards[3], self.player), HandPosition(cards[1], self.player),
                            HandPosition(cards[0], self.player), HandPosition(cards[4], self.player)]
        self.numbers_w1 = [HandPosition(Card(CardType.NUMBER, 10), self.player)]
        self.numbers_w2 = [HandPosition(cards[1], self.player),
                           HandPosition(cards[2], self.player)]
        self.numbers_w3 = [HandPosition(cards[2], self.player),
                           HandPosition(cards[3], self.player),
                           HandPosition(cards[4], self.player)]
        self.numbers_w4 = [HandPosition(cards[3], self.player),
                           HandPosition(Card(CardType.KING, 0), self.player)]
        self.numbers_w5 = [HandPosition(cards[1], self.player),
                           HandPosition(cards[2], self.other_player)]

        self.assertTrue(self.player.play(self.numbers_ok1))
        self.player.hand.cards = cards[:]
        self.assertTrue(self.player.play(self.numbers_ok2))
        self.player.hand.cards = cards[:]
        self.assertTrue(self.player.play(self.numbers_ok3))
        self.player.hand.cards = cards[:]

        self.assertIsNone(self.player.play(self.numbers_w1))
        self.assertIsNone(self.player.play(self.numbers_w2))
        self.assertIsNone(self.player.play(self.numbers_w3))
        self.assertIsNone(self.player.play(self.numbers_w4))
        self.assertEqual(len(self.player.hand.cards), 5)
