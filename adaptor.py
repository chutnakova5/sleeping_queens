from typing import List, Optional

from cards import Queen
from evaluate import MoveQueen, EvaluateAttack
from game import Game
from hand import Hand
from player import Player, PlayerState
from positions import Position, HandPosition, SleepingQueenPosition, AwokenQueenPosition, QueenCollection
from piles import DrawingAndTrashPile, Strategy1


class GamePlayerInterface:
    def play(self, player: str, cards: str):
        pass


class GameAdaptor(GamePlayerInterface):
    """
    Composes game and its components.
    """
    def __init__(self, number_of_players: int):
        self.observable = GameObservable(number_of_players)
        pile = DrawingAndTrashPile(Strategy1())
        sleeping_queens = QueenCollection()
        if number_of_players not in range(2, 6):
            number_of_players = 2
        players: List[Player] = []
        for i in range(number_of_players):
            hand = Hand(i, pile)
            awoken_queens = QueenCollection(i)
            move_queen = MoveQueen(awoken_queens, sleeping_queens)
            eval_attack = EvaluateAttack(players)
            player_state = PlayerState()
            players.append(Player(hand, awoken_queens, move_queen, eval_attack, player_state))
            hand.draw_new_cards()
        self.game = Game(number_of_players, self.observable, pile, sleeping_queens, players, GameFinished())
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


class GameFinishedStrategy:
    @staticmethod
    def is_finished(game) -> Optional[int]:
        pass


class GameFinished(GameFinishedStrategy):
    @staticmethod
    def is_finished(game) -> Optional[int]:
        if game.get_number_of_players() in (2, 3):
            desired_points, desired_queens = 50, 5
        else:
            desired_points, desired_queens = 40, 4
        score = [player.count_points() for player in game.players]
        if game.sleeping_queens.is_empty():
            max_score = max(score)
            i = score.index(max_score)
            game.observable.notify_all(f"Game finished, winner: {i + 1}")
            game.winner = game.players[i]
            return max_score
        for i, player in enumerate(game.players):
            queen_count = player.count_queens()
            if score[i] >= desired_points or queen_count >= desired_queens:
                game.observable.notify_all(f"Game finished, winner: {i + 1}")
                game.winner = player
                return score[i]
        return None
