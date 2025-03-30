from math import sqrt
from typing import Callable, Final

from src import constants

TARGET_INDEXES_1: Final[set[tuple[int, int]]] = set(
    (x, y) for x in range(5) for y in range(5) if x + y <= 5
)

TARGET_INDEXES_2: Final[set[tuple[int, int]]] = set(
    (constants.BOARD_SIZE - 1 - x, constants.BOARD_SIZE - 1 - y)
    for x in range(5) for y in range(5) if x + y <= 5
)
CORNER_1: Final[tuple[int, int]] = (0, 0)
CORNER_2: Final[tuple[int, int]] = (constants.BOARD_SIZE - 1, constants.BOARD_SIZE - 1)


def rate_position(
    board: list[list[str]], distance_function: Callable
) -> int | float:
    rating: int = 0
    in_target_1, in_target_2 = 0, 0
    for x in range(constants.BOARD_SIZE):
        for y in range(constants.BOARD_SIZE):
            if board[x][y] == "1":
                if (x, y) in TARGET_INDEXES_1:
                    in_target_1 += 1
                rating -= distance_function((x, y), CORNER_1)
                rating += distance_function((x, y), CORNER_2)
            elif board[x][y] == "2":
                if (x, y) in TARGET_INDEXES_2:
                    in_target_1 += 1
                rating += distance_function((x, y), CORNER_2)
                rating -= distance_function((x, y), CORNER_1)
    rating += in_target_1
    rating -= in_target_2
    return float("inf") if in_target_1 == 19 else float("-inf") if in_target_2 == 19 else rating


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def chebyshev_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
