from typing import Callable
from game_tree import PositionNode


def play(position: PositionNode, max_depth: int, algorithm1: Callable, algorithm2: Callable,
         distance1: Callable, distance2: Callable, verbose=False) -> tuple[str, int]:
    position.root_initialization(max_depth)

    rounds_count = 0

    while position.winner() == '0':
        if rounds_count % 2 == 0:
            position_rating = algorithm1(position, max_depth, distance1)
        else:
            position_rating = algorithm2(position, max_depth, distance2, to_move='2')
        position = position.find_child_with_rating(position_rating)
        if verbose:
            print(f'{position}  - {position_rating}')
        position.root_initialization(max_depth)
        rounds_count += 1

    return position.winner(), rounds_count
