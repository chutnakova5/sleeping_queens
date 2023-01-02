from typing import List, Optional
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from game import Game
from interface import GameAdaptor
from player import Player
from cards import Card, CardType, Queen
from positions import HandPosition, AwokenQueenPosition, SleepingQueenPosition, Position


class TestPlayerSolitary(TestCase):
    def setUp(self) -> None:
        self.cards_from_hand: List[Card] = [
            Card(CardType.NUMBER, 7), Card(CardType.NUMBER, 1), Card(CardType.NUMBER, 3),
            Card(CardType.NUMBER, 5), Card(CardType.NUMBER, 1)]
        mock_hand = Mock()
        self.player: Player = Player(mock_hand, Mock(), Mock(), Mock(), Mock())
        # self.playerID = 0

        self.numbers_ok1: List[Position] = [HandPosition(Card(CardType.NUMBER, 7), 0)]
        self.numbers_ok2: List[Position] = [
            HandPosition(Card(CardType.NUMBER, 1), 0), HandPosition(Card(CardType.NUMBER, 1), 0)]
        self.numbers_ok3: List[Position] = [
            HandPosition(Card(CardType.NUMBER, 5), 0), HandPosition(Card(CardType.NUMBER, 1), 0),
            HandPosition(Card(CardType.NUMBER, 7), 0), HandPosition(Card(CardType.NUMBER, 1), 0)]

        self.numbers_w1: List[Position] = [HandPosition(Card(CardType.NUMBER, 10), 0)]
        self.numbers_w2: List[Position] = [
            HandPosition(Card(CardType.NUMBER, 1), 0), HandPosition(Card(CardType.NUMBER, 3), 0)]
        self.numbers_w3: List[Position] = [
            HandPosition(Card(CardType.NUMBER, 3), 0), HandPosition(Card(CardType.NUMBER, 5), 0),
            HandPosition(Card(CardType.NUMBER, 1), 0)]
        self.numbers_w4: List[Position] = [
            HandPosition(Card(CardType.NUMBER, 5), 0), HandPosition(Card(CardType.KING, 0), 0)]

        self.cards_ok1: List[Position] = [
            HandPosition(Card(CardType.POTION, 0), 0), AwokenQueenPosition(Queen('Rose Queen', 5), 1)]
        self.cards_ok2: List[Position] = [
            HandPosition(Card(CardType.KING, 0), 0), SleepingQueenPosition(Queen('Rose Queen', 5))]
        self.cards_w1: List[Position] = [
            HandPosition(Card(CardType.KING, 0), 0), HandPosition(Card(CardType.POTION, 0), 1)]

    def set_cards_from_hand(self, positions):
        cards: List[Card] = [pos.get_card() for pos in positions if type(pos) == HandPosition]
        self.player.hand.get_cards = MagicMock(return_value=cards)
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
        self.player.evaluate = MagicMock(return_value=False)
        self.player.move_queen._move = MagicMock(return_value=False)
        self.set_cards_from_hand(self.cards_ok1)
        self.assertFalse(self.player.play(self.cards_ok1))

        self.player.evaluate = MagicMock(return_value=True)
        self.player.move_queen._move = MagicMock(return_value=True)

        self.set_cards_from_hand(self.cards_ok1)
        self.assertTrue(self.player.play(self.cards_ok1))
        self.set_cards_from_hand(self.cards_ok2)
        self.assertTrue(self.player.play(self.cards_ok2))

        self.set_cards_from_hand(self.cards_w1)
        self.assertFalse(self.player.play(self.cards_w1))


class TestPlayerSociable(TestCase):
    def setUp(self):
        adaptor = GameAdaptor(2)
        self.game: Game = adaptor.game
        self.player: Player = self.game.players[0]
        self.other_player: Player = self.game.players[1]
        cards: List[Card] = [
            Card(CardType.NUMBER, 7), Card(CardType.NUMBER, 1), Card(CardType.NUMBER, 3), Card(CardType.NUMBER, 5),
            Card(CardType.NUMBER, 1)]
        self.player.hand.set_cards(cards[:])

        self.numbers_ok1: List[Position] = [HandPosition(cards[0], 0)]
        self.numbers_ok2: List[Position] = [HandPosition(cards[1], 0), HandPosition(cards[4], 0)]
        self.numbers_ok3: List[Position] = [
            HandPosition(cards[3], 0), HandPosition(cards[1], 0), HandPosition(cards[0], 0), HandPosition(cards[4], 0)]
        self.numbers_w1: List[Position] = [HandPosition(Card(CardType.NUMBER, 10), 0)]
        self.numbers_w2: List[Position] = [HandPosition(cards[1], 0), HandPosition(cards[2], 0)]
        self.numbers_w3: List[Position] = [
            HandPosition(cards[2], 0), HandPosition(cards[3], 0), HandPosition(cards[4], 0)]
        self.numbers_w4: List[Position] = [HandPosition(cards[3], 0), HandPosition(Card(CardType.KING, 0), 0)]
        self.numbers_w5: List[Position] = [HandPosition(cards[1], 0), HandPosition(cards[2], 1)]

        self.cards_ok1: List[Position] = [
            HandPosition(Card(CardType.POTION, 0), 0), AwokenQueenPosition(Queen('Rose Queen', 5), 1)]
        self.cards_ok2: List[Position] = [
            HandPosition(Card(CardType.KING, 0), 0), SleepingQueenPosition(Queen('Moon Queen', 10))]
        self.cards_w1: List[Position] = [
            HandPosition(Card(CardType.KING, 0), 0), HandPosition(Card(CardType.POTION, 0), 1)]

    def test_awoken_queens(self):
        self.assertTrue(self.player.awoken_queens.get_queens() == [])
        queen1: Queen = Queen('Peacock Queen', 10)
        queen2: Queen = Queen('Pancake Queen', 15)
        self.player.add_queen(queen1)
        self.assertEqual(self.player.awoken_queens.get_queens(), [queen1])
        self.player.add_queen(queen2)
        queens: List[Optional[Queen]] = self.player.awoken_queens.get_queens()
        self.assertEqual(queens, [queen1, queen2])
        self.player.remove_queen(queen1)
        self.assertEqual(self.player.awoken_queens.get_queens(), [None, queen2])

    def test_move(self):
        self.assertFalse(self.player.awoken_queens.get_queens() or self.other_player.awoken_queens.get_queens())
        queen1: Queen = self.game.sleeping_queens.queens[0]
        queen2: Queen = self.game.sleeping_queens.queens[7]
        self.player.move_queen.wake_up(SleepingQueenPosition(queen1))
        self.assertIsNone(self.game.sleeping_queens.queens[0])
        self.assertEqual(self.player.awoken_queens.get_queens(), [queen1])
        self.player.move_queen.wake_up(SleepingQueenPosition(queen2))
        self.assertTrue(self.game.sleeping_queens.queens[0] is None
                        and self.game.sleeping_queens.queens[7] is None)
        self.assertEqual(self.game.sleeping_queens.count_queens(), 10)

        self.player.move_queen.move_awoken(AwokenQueenPosition(queen2, 0), self.other_player.awoken_queens)
        self.assertEqual(self.other_player.awoken_queens.get_queens(), [queen2])
        self.assertEqual(self.player.awoken_queens.get_queens(), [queen1, None])
        self.other_player.move_queen.move_awoken(AwokenQueenPosition(queen2, 1), self.player.awoken_queens)
        self.assertEqual(self.player.awoken_queens.get_queens(), [queen1, queen2])

    def test_move_fail(self):
        queen1: Queen = self.game.sleeping_queens.queens[0]
        queen2: Queen = self.game.sleeping_queens.queens[7]
        self.player.move_queen.wake_up(SleepingQueenPosition(queen1))
        self.assertFalse(self.player.move_queen.wake_up(SleepingQueenPosition(queen1)))
        self.assertFalse(self.player.move_queen.move_awoken(AwokenQueenPosition(queen2, 1), self.player.awoken_queens))

    def test_play(self):
        king1, knight1, knight11, potion1, dragon1 = (
            Card(CardType.KING), Card(CardType.KNIGHT), Card(CardType.KNIGHT), Card(CardType.POTION),
            Card(CardType.DRAGON))
        self.player.hand.set_cards([knight1, potion1, king1, dragon1, knight11])
        number2, potion2, king2, dragon2, wand2 = (Card(CardType.NUMBER, 2), Card(CardType.POTION), Card(CardType.KING),
                                                   Card(CardType.DRAGON), Card(CardType.WAND))
        self.other_player.hand.set_cards([number2, potion2, king2, dragon2, wand2])

        self.game.pile.draw_pile[-10:] = [Card(CardType.NUMBER, -1) for _ in range(10)]
        self.assertTrue(len(self.game.pile.draw_pile) == 62 - self.game.get_number_of_players() * 5)

        queen1: Queen = self.game.sleeping_queens.queens[0]
        queen2: Queen = self.game.sleeping_queens.queens[10]
        self.assertTrue(self.player.play([HandPosition(king1, 0), SleepingQueenPosition(queen1)]))

        self.assertIsNone(self.game.sleeping_queens.queens[0])
        self.assertFalse(self.player.play([HandPosition(king1, 0), SleepingQueenPosition(queen1)]))
        self.other_player.play([HandPosition(king2, 1), SleepingQueenPosition(queen2)])
        self.other_player.hand.set_cards([number2, potion2, king2, dragon2, wand2])
        self.assertFalse(self.player.play([HandPosition(knight1, 0), AwokenQueenPosition(queen2, 1)]))
        self.assertTrue(self.player.play([HandPosition(knight11, 0), AwokenQueenPosition(queen2, 1)]))

    def test_play_numbered(self):
        cards: List[Card] = self.player.hand.get_cards()[:]

        self.assertTrue(self.player.play(self.numbers_ok1))
        self.player.hand.set_cards(cards[:])
        self.assertTrue(self.player.play(self.numbers_ok2))
        self.player.hand.set_cards(cards[:])
        self.assertTrue(self.player.play(self.numbers_ok3))
        self.player.hand.set_cards(cards[:])

        self.assertIsNone(self.player.play(self.numbers_w1))
        self.assertIsNone(self.player.play(self.numbers_w2))
        self.assertIsNone(self.player.play(self.numbers_w3))
        self.assertIsNone(self.player.play(self.numbers_w4))
        self.assertEqual(len(self.player.hand.get_cards()), 5)
