from typing import List

from game import Game
from player import Player
from positions import Position, HandPosition, SleepingQueenPosition, AwokenQueenPosition


class GamePlayerInterface:
    def play(self, player: str, cards: str):
        pass


class GameAdaptor(GamePlayerInterface):
    def __init__(self):
        self.game = Game()
        self.observable = GameObservable()

    def play(self, player: str, cards: str):
        player_index: int = int(player) - 1
        player: Player = self.game.players[player_index]
        positions: List[Position] = []
        commands: List[str] = cards.split()
        for command in commands:
            card_type = command[0]
            if card_type == 'h':
                card_num: int = int(command[1])
                card_pos: HandPosition = player.hand.cards[card_num]
                positions.append(card_pos)
            elif card_type == 'a':
                player2_num: int = int(command[1]) - 1
                player2: Player = self.game.players[player2_num]
                queen_num: int = int(command[2]) - 1
                queen_pos: AwokenQueenPosition = player2.awoken_queens[queen_num]
                positions.append(queen_pos)
            elif card_type == 's':
                queen_num: int = int(command[1]) - 1
                queen_pos: SleepingQueenPosition = self.game.sleeping_queens[queen_num]
                positions.append(queen_pos)
        self.game.play(player_index, positions)


class GameFinishedStrategy:
    pass


class GameFinished(GameFinishedStrategy):
    pass


class GameObserver:
    def notify(self, message: str):
        pass


class GameObservable:
    def __init__(self):
        self.observers: List[GameObserver] = []
        self.players: List[int] = []

    def add(self, observer: GameObserver):
        self.observers.append(observer)

    def add_player(self, player_id: int, observer: GameObserver):
        self.players.append(player_id)

    def notify_all(self, message: str):
        pass
