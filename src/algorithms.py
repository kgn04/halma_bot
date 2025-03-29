from src import config
from src.game_tree import PositionNode
from src.position_rating import rate_position


def minimax(
    position: PositionNode,
    to_move: str,
    depth: int = 0,
) -> int:
    if depth == config.MAX_DEPTH or position.winner != "0":
        return rate_position(
            position.board, config.TEAM_CONFIG[to_move]["distance_function"]
        )

    extreme_value = float("-inf") if to_move == "1" else float("inf")
    extreme_function = max if to_move == "1" else min

    for child in position.new_children:
        extreme_value = extreme_function(
            extreme_value,
            minimax(
                child,
                "2" if to_move == "1" else "1",
                depth + 1,
            ),
        )
    position.rating = extreme_value
    return extreme_value


def alpha_beta_pruning(
    position: PositionNode,
    to_move: str,
    depth: int = 0,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> int:
    if depth == config.MAX_DEPTH or position.winner != "0":
        return rate_position(
            position.board, config.TEAM_CONFIG[to_move]["distance_function"]
        )

    extreme_value = float("-inf") if to_move == "1" else float("inf")
    extreme_function = max if to_move == "1" else min

    for child in position.new_children:
        extreme_value = extreme_function(
            extreme_value,
            alpha_beta_pruning(
                child,
                "2" if to_move == "1" else "1",
                depth + 1,
                alpha,
                beta,
            ),
        )
        if to_move == "1":
            alpha = max(alpha, extreme_value)
        else:
            beta = min(beta, extreme_value)
        if beta <= alpha:
            break
    position.rating = extreme_value
    return extreme_value
