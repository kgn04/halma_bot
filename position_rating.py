from math import sqrt
from typing import Callable, Final

import config

TARGET_INDEXES: Final[list[tuple[int, int]]] = [
    (x, y) for x in range(5) for y in range(5) if x + y <= 5
]


def rate_position(board: list[list[str]], distance_function: Callable) -> int | float:
    in_target_1 = sum(1 for x, y in TARGET_INDEXES if board[x][y] == "1")
    if in_target_1 == 19:
        return float("inf")

    in_target_2 = sum(
        1 for x, y in TARGET_INDEXES
        if board[config.BOARD_SIZE - 1 - x][config.BOARD_SIZE - 1 - y] == "2"
    )
    if in_target_2 == 19:
        return float("-inf")

    rating: int = 0
    for x in range(16):
        for y in range(16):
            if board[x][y] == "1":
                rating -= distance_function((x, y), (0, 0))
            elif board[x][y] == "2":
                rating += distance_function((x, y), (config.BOARD_SIZE - 1, config.BOARD_SIZE - 1))
    rating += in_target_1
    rating -= in_target_2
    return rating


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def chebyshev_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
