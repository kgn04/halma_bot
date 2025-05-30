import copy

from random import shuffle
from rich.table import Table
from typing import Final, Generator

from src import constants

__all__ = ["PositionNode"]

MOVEMENT_VECTORS: Final[dict[str, list[tuple[int, int]]]] = {
    "1": copy.deepcopy(constants.MOVEMENT_VECTORS),
    "2": copy.deepcopy(constants.MOVEMENT_VECTORS),
}
MOVEMENT_VECTORS["1"].remove((1, 1))
MOVEMENT_VECTORS["1"].remove((0, 1))
MOVEMENT_VECTORS["1"].remove((1, 0))

MOVEMENT_VECTORS["2"].remove((-1, -1))
MOVEMENT_VECTORS["2"].remove((0, -1))
MOVEMENT_VECTORS["2"].remove((-1, 0))


class PositionNode:
    def __init__(
        self,
        board: list[list[str]],
        to_move: str,
        last_move: tuple[tuple[int, int], tuple[int, int]] = None,
    ):
        self.board: list[list[str]] = board
        self.rating: int | float = 0.0
        self._to_move: str = to_move
        self._children: list[PositionNode] = []
        self._children_positions: list[list[list[str]]] = []
        self._last_move: tuple[tuple[int, int], tuple[int, int]] = last_move

    @property
    def winner(self) -> str:
        count_1, count_2 = 0, 0
        for i in range(5):
            for j in range(5):
                if i + j <= 5:
                    if self.board[i][j] == "1":
                        count_1 += 1
                    if (
                        self.board[constants.BOARD_SIZE - 1 - i][
                            constants.BOARD_SIZE - 1 - j
                        ]
                        == "2"
                    ):
                        count_2 += 1
        return "1" if count_1 == 19 else "2" if count_2 == 19 else "0"

    @property
    def as_table(self) -> Table:
        table: Table = Table(show_header=False, show_lines=True)
        for i, row in enumerate(self.board):
            new_row: list[str] = []
            for j, x in enumerate(row):
                color: str = constants.COLOR[x]
                x = " " if x == "0" else x
                if self._last_move:
                    color = (
                        "green"
                        if (i, j) == self._last_move[1]
                        else "red" if (i, j) == self._last_move[0] else color
                    )
                    x = "X" if color == "red" else x
                new_row.append(f"[bold {color}]{x}[/]")
            table.add_row(*new_row)
        return table

    @property
    def children(self) -> Generator["PositionNode", None, None]:
        for x in range(constants.BOARD_SIZE):
            for y in range(constants.BOARD_SIZE):
                if self.board[x][y] == self._to_move:
                    for dx, dy in MOVEMENT_VECTORS[self._to_move]:
                        new_x, new_y = x + dx, y + dy
                        if (
                            0 <= new_x < constants.BOARD_SIZE
                            and 0 <= new_y < constants.BOARD_SIZE
                            and self.board[new_x][new_y] == "0"
                        ):
                            new_position = self._new_position_board(
                                self.board, x, y, new_x, new_y
                            )
                            yield self._add_new_child(
                                new_position, x, y, new_x, new_y
                            )
                    yield from self._find_jump_move(x, y, self.board)

    def _new_position_board(
        self,
        board: list[list[str]],
        old_x: int,
        old_y: int,
        new_x: int,
        new_y: int,
    ) -> list[list[str]]:
        new_position_board = copy.deepcopy(board)
        new_position_board[new_x][new_y] = self._to_move
        new_position_board[old_x][old_y] = "0"
        return new_position_board

    def _add_new_child(
        self,
        position: list[list[str]],
        old_x: int,
        old_y: int,
        new_x: int,
        new_y: int,
    ) -> "PositionNode":
        new_child = PositionNode(
            position,
            to_move="1" if self._to_move == "2" else "2",
            last_move=((old_x, old_y), (new_x, new_y)),
        )
        self._children.append(new_child)
        self._children_positions.append(position)
        return new_child

    def _find_jump_move(
        self, x: int, y: int, position: list[list[str]]
    ) -> Generator["PositionNode", None, None]:
        for dx, dy in MOVEMENT_VECTORS[self._to_move]:
            new_x, new_y = x + 2 * dx, y + 2 * dy
            if (
                0 <= new_x < constants.BOARD_SIZE
                and 0 <= new_y < constants.BOARD_SIZE
                and self.board[x + dx][y + dy] != "0"
                and self.board[new_x][new_y] == "0"
            ):
                new_position = self._new_position_board(
                    position, x, y, new_x, new_y
                )
                if new_position not in self._children_positions:
                    yield self._add_new_child(new_position, x, y, new_x, new_y)
                    yield from self._find_jump_move(new_x, new_y, new_position)

    def find_child_with_rating(self, rating: int) -> "PositionNode":
        shuffle(self._children)
        return next(
            child
            for child in self._children
            if child.rating == rating or child.winner != "0"
        )
