from typing import Final

BOARD_SIZE: Final[int] = 16
COLOR: Final[dict[str, str]] = {
    "1": "purple",
    "2": "blue",
    "0": "white",
}
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
