from game_tree import PositionNode
from typing import Callable
from sys import maxsize
from strategies import strategy


def minimax(position: PositionNode, max_depth: int, distance_function: Callable, depth=0, to_move='1') -> int:
    if depth == max_depth:
        return strategy(position.position, distance_function)

    extreme_value = -1 * maxsize if to_move == '1' else maxsize
    extreme_function = max if to_move == '1' else min

    for child in position.children:
        extreme_value = extreme_function(
            extreme_value,
            minimax(child, max_depth, distance_function, depth+1, '2' if to_move == '1' else '1')
        )
    return extreme_value


def alpha_beta_pruning(position: PositionNode, max_depth: int, distance_function: Callable, depth=0,to_move='1', alpha=-1*maxsize, beta=maxsize) -> int:
    if depth == max_depth:
        return strategy(position.position, distance_function)

    extreme_value = -1 * maxsize if to_move == '1' else maxsize
    extreme_function = max if to_move == '1' else min

    for i, child in enumerate(position.children):
        extreme_value = extreme_function(
            extreme_value,
            alpha_beta_pruning(child, max_depth, distance_function, depth+1, '2' if to_move == '1' else '1', alpha, beta)
        )
        if to_move == '1':
            alpha = max(alpha, extreme_value)
        else:
            beta = min(beta, extreme_value)
        if beta <= alpha:
            break
    position.rating = extreme_value
    return extreme_value
