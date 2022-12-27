from typing import List, Optional

from cards import Queen
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
        player_index: int = int(player) - 1         # playerID n. 1 is at index 0 in the list of players
        player1: Player = self.game.players[player_index]
        positions: List[Position] = []
        commands: List[str] = cards.split()         # commands are separated by spaces
        for command in commands:
            card_type = command[0]
            if card_type == 'h':        # card from hand ... for example 'h3' means 3. card from playerID's hand
                card_num: int = int(command[1]) - 1
                card = player1.hand.get_cards()[card_num]
                card_pos = HandPosition(card, player_index)
                positions.append(card_pos)
            elif card_type == 'a':      # awoken queen ... for example 'a21' means 1. awoken queen from playerID 2
                player2_num: int = int(command[1]) - 1
                player2: Player = self.game.players[player2_num]
                a_queen_num: int = int(command[2]) - 1
                a_queen: Optional[Queen] = player2.awoken_queens[a_queen_num]
                if a_queen is None:
                    return None
                a_queen_pos = AwokenQueenPosition(a_queen, player2_num)
                positions.append(a_queen_pos)
            elif card_type == 's':      # sleeping queen ... for example 's8' means 8. sleeping queen
                s_queen_num: int = int(command[1]) - 1
                s_queen: Optional[Queen] = self.game.sleeping_queens[s_queen_num]
                if s_queen is None:
                    return None
                s_queen_pos: SleepingQueenPosition = SleepingQueenPosition(s_queen)
                positions.append(s_queen_pos)
        result = self.game.play(player_index, positions)
        if result is not None:
            self.game.update_game_state()
            self.finished = self.game.is_finished()
        return result


class GameObserver:
    def notify(self, message: str):
        pass


class GameObservable:
    def __init__(self, number_of_players) -> None:
        self.observers: List[Optional[GameObserver]] = [None for _ in range(number_of_players)]
        self.players: List[int] = []

    def add(self, observer: GameObserver) -> None:
        self.observers.append(observer)

    def add_player(self, player_id: int, observer: GameObserver) -> None:
        self.players.append(player_id)
        self.observers[player_id] = observer        # observer for each playerID will be at the same index as playerID

    def notify_all(self, message: str) -> None:
        for x in self.observers:
            if x:
                x.notify(message)
