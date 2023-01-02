from unittest import TestCase
from interface import GameAdaptor
from cards import Card, CardType


class TestAdaptor(TestCase):
    def test_build_game(self):
        for i in range(2, 6):
            adaptor = GameAdaptor(i)
            self.assertTrue(len(adaptor.game.players) == i)
        adaptor = GameAdaptor(4)
        self.assertTrue(len(adaptor.game.players[0].hand.get_cards()) == 5)

    def test_collections(self):
        adaptor = GameAdaptor(3)
        self.assertEqual(len(adaptor.game.sleeping_queens.get_queens()), 12)
        self.assertEqual(len(adaptor.game.players[0].awoken_queens.get_queens()), 0)


class TestPlay(TestCase):
    def setUp(self) -> None:
        self.adaptor = GameAdaptor(2)
        self.player1 = self.adaptor.game.players[0]
        self.player2 = self.adaptor.game.players[1]
        self.cards1 = [
            Card(CardType.NUMBER, 8), Card(CardType.NUMBER, 8), Card(CardType.NUMBER, 1),
            Card(CardType.DRAGON, 0), Card(CardType.KING, 0)]
        self.cards2 = [
            Card(CardType.NUMBER, 10), Card(CardType.NUMBER, 7), Card(CardType.NUMBER, 3),
            Card(CardType.KNIGHT, 0), Card(CardType.POTION, 0)]
        self.to_draw = [Card(CardType.NUMBER, 1) for _ in range(10)]
        self.adaptor.game.pile.draw_pile.extend(self.to_draw[:])
        self.player1.hand.set_cards(self.cards1[:])
        self.player2.hand.set_cards(self.cards2[:])

    def test_numbered(self):
        # 8 8 1 * *         ---         10 7 3 * *
        self.assertTrue(self.adaptor.game.game_state.on_turn == 0)
        self.assertIsNone(self.adaptor.play('2', 'h1 h2 h3'))

        self.assertIsNone(self.adaptor.play('1', 'h2 h3'))
        self.assertEqual(self.player1.hand.get_cards(), self.cards1)
        self.assertTrue(self.adaptor.game.game_state.on_turn == 0)
        self.assertTrue(self.adaptor.play('1', 'h1 h2'))
        # 1 * * * *
        self.assertEqual(self.player1.hand.get_cards(), self.cards1[2:] + self.to_draw[-2:])
        self.assertTrue(self.adaptor.game.game_state.on_turn == 1)

        self.to_draw = self.to_draw[:-2]
        self.assertTrue(self.adaptor.play('2', 'h1 h2 h3'))
        self.assertEqual(self.player2.hand.get_cards(), self.cards2[-2:] + self.to_draw[-3:])
        self.assertTrue(self.adaptor.game.game_state.on_turn == 0)
        self.assertTrue(self.adaptor.play('1', 'h1'))

    def test_king_knight(self):
        self.cards2[-1] = Card(CardType.KNIGHT, 0)
        self.player2.cards = self.cards2[:]
        # 8 8 1 dragon king         ---         10 7 3 knight knight
        self.assertTrue(self.adaptor.play('1', 'h5 s7'))
        # 8 8 1 dragon *
        self.assertEqual(self.adaptor.game.sleeping_queens.count_queens(), 11)
        self.assertEqual(self.adaptor.game.players[0].awoken_queens.count_queens(), 1)
        self.assertEqual(self.player1.hand.get_cards(), self.cards1[:4] + [self.to_draw[-1]])
        self.assertTrue(self.player1.hand.get_cards()[3].get_type() == 'DRAGON')
        self.assertFalse(self.adaptor.play('2', 'a11 h4'))
        # 8 8 1 * *         ---         10 7 3 * knight
        self.assertFalse(self.player1.hand.get_cards()[3].get_type() == 'DRAGON')
        self.assertEqual(self.adaptor.game.players[0].awoken_queens.count_queens(), 1)

        self.adaptor.play('1', 'h1')
        self.assertTrue(self.adaptor.play('2', 'a11 h4'))
        self.assertEqual(self.adaptor.game.players[0].awoken_queens.count_queens(), 0)
        self.assertEqual(self.adaptor.game.players[1].awoken_queens.count_queens(), 0)

    def test_potion(self):
        self.player1.hand.get_cards()[0] = self.cards1[0] = Card(CardType.WAND, 0)
        self.player2.hand.get_cards()[0] = self.cards2[0] = Card(CardType.POTION, 0)
        # wand 8 1 dragon king          ----        potion 7 3 knight potion
        self.adaptor.play('1', 'h5 s7')
        # 8 1 dragon king *             ---         7 3 knight potion *
        self.assertFalse(self.adaptor.play('2', 'h1 a11'))
        # 8 1 dragon king *             ---         7 3 knight potion *
        self.assertEqual(self.player2.hand.get_cards()[:-2], self.cards2[1:4])
        self.assertEqual(self.player1.hand.get_cards()[:-2], self.cards1[1:4])
        self.adaptor.play('1', 'h2 s7')
