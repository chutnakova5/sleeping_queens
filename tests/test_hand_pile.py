from unittest import TestCase
from unittest.mock import Mock, MagicMock

from hand import Hand
from cards import Card, CardType, Queen
from positions import HandPosition
from piles import DrawingAndTrashPile


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
