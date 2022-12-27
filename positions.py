from __future__ import annotations

from typing import Union, Optional, List
from cards import Card, Queen


class SleepingQueenPosition:
    def __init__(self, card: Queen, playerID: Optional[int] = None) -> None:
        self._card = card

    def get_card(self) -> Queen:
        return self._card


class AwokenQueenPosition:
    def __init__(self, card: Queen, playerID: int) -> None:
        self._card = card
        self._playerID = playerID

    def get_card(self) -> Queen:
        return self._card

    def get_playerID(self) -> int:
        return self._playerID


class HandPosition:
    def __init__(self, card: Card, playerID: int) -> None:
        self._card = card
        self._playerID = playerID

    def get_card(self) -> Card:
        return self._card

    def get_playerID(self) -> int:
        return self._playerID

    def get_type(self) -> str:
        return self._card.get_type()


Position = Union[HandPosition, SleepingQueenPosition, AwokenQueenPosition]


class QueenCollectionInterface:
    def add_queen(self, queen: Queen) -> None:
        pass

    def remove_queen(self, queen: Queen) -> Optional[Queen]:
        pass

    def __contains__(self, item: Union[Card, Queen]) -> bool:
        return False

    def __getitem__(self, index: int) -> Optional[Queen]:
        return Queen('', 0)

    def get_queens(self) -> List[Optional[Queen]]:
        return []

    def count_queens(self) -> int:
        return 0

    def count_points(self) -> int:
        return 0

    def is_empty(self) -> bool:
        return True


class QueenCollection(QueenCollectionInterface):
    def __init__(self, playerID: Optional[int] = None) -> None:
        self.queens: List[Optional[Queen]] = []
        self.playerID = playerID

    def add_queen(self, queen: Queen) -> None:
        for i in range(len(self.queens)):
            if self.queens[i] is None:
                self.queens[i] = queen
                return
        self.queens.append(queen)

    def remove_queen(self, queen: Queen) -> Optional[Queen]:
        if queen in self.queens:
            index: int = self.queens.index(queen)
            self.queens[index] = None
            return queen
        return None

    def __contains__(self, item: Union[Card, Queen]) -> bool:
        return item in self.queens

    def __getitem__(self, index: int) -> Optional[Queen]:
        return self.queens[index]

    def get_queens(self) -> List[Optional[Queen]]:
        return self.queens

    def count_queens(self) -> int:
        return sum(map(lambda x: x is not None, self.queens))

    def count_points(self) -> int:
        return sum([queen.get_points() for queen in self.queens if queen])

    def is_empty(self):
        return self.queens == [None for _ in range(len(self.queens))]
