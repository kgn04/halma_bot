from typing import Final

from src import algorithms
from src import position_rating

TEAM_CONFIG: Final[dict[str, dict[str, ...]]] = {
    "1": {
        "algorithm": algorithms.alpha_beta_pruning,
        "distance_function": position_rating.euclidean_distance,
        "color": "purple",
    },
    "2": {
        "algorithm": algorithms.alpha_beta_pruning,
        "distance_function": position_rating.euclidean_distance,
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
