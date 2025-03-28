from typing import Final

import algorithms
import position_rating

TEAM_CONFIG: Final[dict[str, dict[str, ...]]] = {
    "1": {
        "algorithm": algorithms.minimax,
        "distance_function": position_rating.chebyshev_distance,
        "color": "purple",
    },
    "2": {
        "algorithm": algorithms.minimax,
        "distance_function": position_rating.chebyshev_distance,
        "color": "blue",
    },
    "0": {
        "color": "white",
    },
}

MAX_DEPTH: Final[int] = 2
POSITION: Final[int] = 52
VERBOSE: Final[bool] = True
BOARD_SIZE: Final[int] = 16
MOVEMENT_VECTORS: Final[list[tuple[int, int]]] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, -1),
    (0, 1),
]