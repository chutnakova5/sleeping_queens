from unittest import TestCase
from unittest.mock import Mock, MagicMock

from player import Player, EvaluateAttack
from hand import Hand
from cards import Card, CardType, Queen
from positions import HandPosition, AwokenQueenPosition, SleepingQueenPosition
from piles import DrawingAndTrashPile
from game import Game


class TestHand(TestCase):
    def setUp(self) -> None:
        self.pile = DrawingAndTrashPile()
        self.fake_player = Mock()
        self.fake_pile = Mock()
        self.hand = Hand(self.fake_player, self.pile)

        self.cards_to_draw = [Card(CardType.NUMBER, 5), Card(CardType.NUMBER, 5), Card(CardType.NUMBER, 2),
                              Card(CardType.DRAGON, 0), Card(CardType.POTION, 0)]
        self.fake_pile.draw = MagicMock(return_value=self.cards_to_draw)
        self.fake_pile.discard_and_redraw = MagicMock(return_value=self.cards_to_draw[:3])
        self.fake_discard_pile = Mock()
        self.solitary_hand = Hand(self.fake_player, self.fake_pile)

        self.cards = [Card(CardType.KING, 0), Card(CardType.NUMBER, 8), Card(CardType.NUMBER, 8),
                      Card(CardType.WAND, 0), Card(CardType.NUMBER, 1)]

        self.assert_full_empty(self.pile)

    def assert_full_empty(self, pile):
        self.assertEqual(len(pile.draw_pile), 62)
        self.assertEqual(len(pile.trash_pile), 0)

    def test_card(self):
        c7 = Card(CardType.NUMBER, 7)
        queen = Queen('Sunflower Queen', 10)
        self.assertEqual(c7.get_points(), 7)
        self.assertEqual(c7.get_type(), 'NUMBER')
        self.assertEqual(queen.get_points(), 10)
        self.assertEqual(queen.get_points(), 10)

    def test_hand(self):
        self.solitary_hand.cards = self.cards
        self.assertEqual(self.solitary_hand.get_cards(), self.cards)

    def test_hand_pick(self):
        positions = [HandPosition(c, self.fake_player) for c in self.cards]
        self.solitary_hand.cards = self.cards
        self.solitary_hand.pick_cards(positions[:3])
        self.assertEqual(self.solitary_hand.picked_cards, self.cards[:3])
        self.assertIsNone(self.solitary_hand.pick_cards(
            positions[-2:] + [HandPosition(Card(CardType.DRAGON, 0), self.fake_player)]))
        self.assertEqual(self.solitary_hand.pick_cards(positions[-2:]), self.cards[-2:])

        new_cards = [Card(CardType.NUMBER, 1), Card(CardType.POTION, 0)]
        self.solitary_hand.pile.discard_and_redraw = MagicMock(return_value=new_cards)

        self.solitary_hand.remove_picked_cards_and_redraw()
        self.assertEqual(self.solitary_hand.picked_cards, [])
        self.assertEqual(self.solitary_hand.get_cards(), self.cards[:-2] + new_cards)

    def test_hand_remove_redraw(self):
        cards = [Card(CardType.NUMBER, 1), Card(CardType.POTION, 0), Card(CardType.NUMBER, 8),
                 Card(CardType.KNIGHT, 0), Card(CardType.NUMBER, 1)]
        positions = [HandPosition(c, self.fake_player) for c in cards]
        self.solitary_hand.cards = cards[:]
        self.solitary_hand.pick_cards([positions[0], positions[2], positions[4]])
        new_cards = [Card(CardType.KING, 0), Card(CardType.KNIGHT, 0)]
        self.solitary_hand.pile.discard_and_redraw = MagicMock(return_value=new_cards)
        self.solitary_hand.remove_picked_cards_and_redraw()
        self.assertEqual(self.solitary_hand.picked_cards, [])
        self.assertEqual(self.solitary_hand.get_cards(), [cards[1], cards[3]] + new_cards)

    def test_piles(self):
        cards_on_top = self.pile.draw_pile[-5:]
        cards = self.pile.deal_cards(5)
        self.assertEqual(cards_on_top, cards)
        self.assertEqual(len(self.pile.draw_pile), 62 - 5)

        self.pile.discard(cards)
        self.assertEqual(self.pile.trash_pile, cards)
        self.pile.deal_cards(62 - 5)
        self.assertEqual(self.pile.draw_pile, [])

    def test_discard_redraw(self):
        cards_on_top = self.pile.draw_pile[-5:]
        self.assertEqual(self.pile.discard_and_redraw(self.cards), cards_on_top)
        self.assertEqual(self.pile.trash_pile, self.cards)
        self.pile.deal_cards(len(self.pile.draw_pile) - 3)
        self.assertTrue(len(self.pile.draw_pile) == 3)
        three_cards = self.pile.draw_pile[:]
        self.assertEqual(self.pile.discard_and_redraw(self.cards)[:3], three_cards)
        self.assertTrue(self.pile.trash_pile == [])
        self.assertEqual(len(self.pile.draw_pile), 8)

    def test_draw(self):
        card = self.pile.draw_pile[-3]
        cards5 = self.pile.draw_pile[-5:]
        self.assertIsNone(self.hand.has_card_of_type(card.get_type()))
        self.assertEqual(self.hand.get_cards(), [])
        self.hand.draw_new_cards()
        from_hand = self.hand.has_card_of_type(card.get_type())
        self.assertEqual(from_hand.get_card().get_type(), card.get_type())
        self.assertEqual(self.hand.get_cards(), cards5)


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
        self.player.hand.cards = self.cards_from_hand
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
        self.game = Game()
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
        self.player.move_queen.move(SleepingQueenPosition(queen1), self.player.awoken_queens)
        self.assertIsNone(self.game.sleeping_queens.queens[0])
        self.assertEqual(self.player.awoken_queens.queens, [queen1])
        self.player.move_queen.move(SleepingQueenPosition(queen2), self.player.awoken_queens)
        self.assertTrue(self.game.sleeping_queens.queens[0] is None
                        and self.game.sleeping_queens.queens[7] is None)
        self.assertTrue(len(self.game.sleeping_queens.get_queens()) == 10)

        self.player.move_queen.move(AwokenQueenPosition(queen2, self.player), self.other_player.awoken_queens)
        self.assertEqual(self.other_player.awoken_queens.queens, [queen2])
        self.assertEqual(self.player.awoken_queens.queens, [queen1, None])
        self.other_player.move_queen.move(AwokenQueenPosition(queen2, self.other_player), self.player.awoken_queens)
        self.assertEqual(self.player.awoken_queens.queens, [queen1, queen2])

    def test_move_fail(self):
        queen1 = self.game.sleeping_queens.queens[0]
        queen2 = self.game.sleeping_queens.queens[7]
        self.player.move_queen.move(SleepingQueenPosition(queen1), self.player.awoken_queens)
        self.assertFalse(self.player.move_queen.move(SleepingQueenPosition(queen1), self.player.awoken_queens))
        self.assertFalse(self.player.move_queen.move())
        self.assertFalse(self.player.move_queen.move(AwokenQueenPosition(queen2, self.other_player), self.player))

    def test_play(self):
        king1, knight1, knight11, potion1, dragon1 = (Card(CardType.KING), Card(CardType.KNIGHT), Card(CardType.KNIGHT),
                                                      Card(CardType.POTION), Card(CardType.DRAGON))
        self.player.hand.cards = [knight1, potion1, king1, dragon1, knight11]
        number2, potion2, king2, dragon2, wand2 = (Card(CardType.NUMBER, 2), Card(CardType.POTION), Card(CardType.KING),
                                                   Card(CardType.DRAGON), Card(CardType.WAND))
        self.other_player.hand.cards = [number2, potion2, king2, dragon2, wand2]

        self.player.hand.pile.draw_pile[-10:] = [Card(CardType.NUMBER, -1) for i in range(10)]
        self.assertTrue(len(self.player.hand.pile.draw_pile) == 62 - self.game.game_state.number_of_players * 5)

        queen1 = self.game.sleeping_queens.queens[0]
        queen2 = self.game.sleeping_queens.queens[10]
        self.assertTrue(self.player.play([HandPosition(king1, self.player), SleepingQueenPosition(queen1)]))
        self.assertIsNone(self.game.sleeping_queens.queens[0])
        self.assertFalse(self.player.play([HandPosition(king1, self.player), SleepingQueenPosition(queen1)]))
        self.other_player.play([HandPosition(king2, self.other_player), SleepingQueenPosition(queen2)])
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
