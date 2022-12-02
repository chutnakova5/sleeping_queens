from piles import DrawPile, DiscardPile
from cards import Card
from typing import List


class Game:
    def __init__(self):
        self.player = Player(self)
        self.draw_pile = DrawPile()
        self.discard_pile = DiscardPile()


class Player:
    def __init__(self, game: Game):
        self.game = game
        self.hand = Hand(self, game)


class PlayerState:
    def __init__(self, player: Player):
        self.player = player
        self.cards = []
        self.awoken_queens = []


class Hand:
    def __init__(self, player: Player, game: Game):
        self.player = player
        self.draw_pile = game.draw_pile
        self.discard_pile = game.discard_pile
        self.cards = []

    def draw(self, n: int):
        self.cards.extend(self.draw_pile.draw(n))

    def discard(self, cards: List[Card]):
        for c in cards:
            self.cards.remove(c)
        self.discard_pile.discard(cards)
