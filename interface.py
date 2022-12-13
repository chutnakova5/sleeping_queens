from typing import List, Optional

from game import Game
from player import Player
from positions import Position, HandPosition, SleepingQueenPosition, AwokenQueenPosition


class GamePlayerInterface:
    def play(self, player: str, cards: str):
        pass


class GameAdaptor(GamePlayerInterface):
    """
    Composes game and its components.
    """
    def __init__(self, number_of_players: int):
        self.observable = GameObservable(number_of_players)
        self.game = Game(number_of_players, self.observable)
        self.finished: Optional[int] = None

    def play(self, player: str, cards: str):
        """
        Evaluates commands from the input and calls method play with correct card positions.
        """
        player_index: int = int(player) - 1         # player n. 1 is at index 0 in the list of players
        player: Player = self.game.players[player_index]
        positions: List[Position] = []
        commands: List[str] = cards.split()         # commands are separated by spaces
        for command in commands:
            card_type = command[0]
            if card_type == 'h':        # card from hand ... for example 'h3' means 3. card from player's hand
                card_num: int = int(command[1]) - 1
                card_pos = HandPosition(player.hand.cards[card_num], player)
                positions.append(card_pos)
            elif card_type == 'a':      # awoken queen ... for example 'a21' means 1. awoken queen from player 2
                player2_num: int = int(command[1]) - 1
                player2: Player = self.game.players[player2_num]
                queen_num: int = int(command[2]) - 1
                queen_pos = AwokenQueenPosition(player2.awoken_queens[queen_num], player2)
                positions.append(queen_pos)
            elif card_type == 's':      # sleeping queen ... for example 's8' means 8. sleeping queen
                queen_num: int = int(command[1]) - 1
                queen_pos = SleepingQueenPosition(self.game.sleeping_queens[queen_num])
                positions.append(queen_pos)
        result = self.game.play(player_index, positions)
        if result is not None:
            self.game.update_game_state()
            self.finished = self.game.is_finished()
        return result


class GameObserver:
    def notify(self, message: str):
        pass


class GameObservable:
    def __init__(self, number_of_players):
        self.observers: List[Optional[GameObserver]] = [None for _ in range(number_of_players)]
        self.players: List[int] = []

    def add(self, observer: GameObserver):
        self.observers.append(observer)

    def add_player(self, player_id: int, observer: GameObserver):
        self.players.append(player_id)
        self.observers[player_id] = observer        # observer for each player will be at the same index as player

    def notify_all(self, message: str):
        for x in self.observers:
            x.notify(message)
