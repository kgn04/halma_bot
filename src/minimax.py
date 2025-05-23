from typing import Callable

from src.game_tree import PositionNode
from src.position_rating import rate_position

__all__ = ["minimax"]

NODES_VISITED: int = 0


def minimax(
    position: PositionNode,
    to_move: str,
    distance_function: Callable,
    depth: int,
    max_depth: int,
    pruning: bool,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> int:
    global NODES_VISITED
    NODES_VISITED += 1

    if depth == max_depth or position.winner != "0":
        return rate_position(position.board, distance_function)

    maximizing: bool = to_move == "1"
    extreme_value = float("-inf") if maximizing else float("inf")
    extreme_function = max if maximizing else min

    for child in position.children:
        extreme_value = extreme_function(
            extreme_value,
            minimax(
                position=child,
                to_move="2" if maximizing else "1",
                distance_function=distance_function,
                depth=depth + 1,
                max_depth=max_depth,
                pruning=pruning,
                alpha=alpha,
                beta=beta,
            ),
        )
        if pruning:
            if maximizing:
                alpha = max(alpha, extreme_value)
            else:
                beta = min(beta, extreme_value)
            if beta <= alpha:
                break
    position.rating = extreme_value
    return extreme_value
