from math import sqrt
from typing import Callable
from sys import maxsize

TARGET_INDEXES = [
    (x, y)
    for x in range(5)
    for y in range(5)
    if x + y <= 5
]


def strategy(position: list[list[str]], distance_function: Callable):
    in_target_1 = sum([1 if position[x][y] == '1' else 0 for x, y in TARGET_INDEXES])
    if in_target_1 == 19:
        return maxsize
    in_target_2 = sum([1 if position[15 - x][15 - y] == '2' else 0 for x, y in TARGET_INDEXES])
    if in_target_2 == 19:
        return -1 * maxsize
    profit = 0
    for x in range(16):
        for y in range(16):
            if position[x][y] == '1':
                if in_target_1 == 18:
                    if (x, y) not in TARGET_INDEXES:
                        profit -= distance_function(
                            (x, y), [(i, j) for i, j in TARGET_INDEXES if position[i][j] != '1'][0]
                        )
                else:
                    profit -= distance_function((x, y), (0, 0))
            elif position[x][y] == '2':
                if in_target_2 == 18:
                    if (15-x, 15-y) not in TARGET_INDEXES:
                        profit += distance_function(
                            (x, y), [(15-i, 15-j) for i, j in TARGET_INDEXES if position[15-i][15-j] != '2'][0]
                        )
                else:
                    profit += distance_function((x, y), (15, 15))
    profit += in_target_1
    profit -= in_target_2
    return profit


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def chebyshev_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
