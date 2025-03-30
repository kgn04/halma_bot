import argparse
from collections import deque

from rich import print
from typing import Callable, Final

from src import constants
from src import position_rating
from src.algorithm import minimax
from src.game_tree import PositionNode

DISTANCE_FUNCTION_MAPPING: Final[dict[str, Callable]] = {
    "manhattan": position_rating.manhattan_distance,
    "chebyshev": position_rating.chebyshev_distance,
    "euclides": position_rating.euclidean_distance,
}


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print current board position and rating after each move",
    )
    parser.add_argument(
        "-p",
        "--position",
        type=int,
        help="position id from 'poitions' directory (1..101)",
        default=1,
    )
    parser.add_argument(
        "-md",
        "--max-depth",
        type=int,
        help="max game tree depth",
        required=True,
    )
    for i in range(1, 3):
        parser.add_argument(
            f"-p{i}",
            f"--prune{i}",
            action="store_true",
            help=f"use alpha beta pruning for player {i} moves.",
        )
        parser.add_argument(
            f"-d{i}",
            f"--distance{i}",
            choices=DISTANCE_FUNCTION_MAPPING.keys(),
            help=f"distance function for heuristics used by player {i}.",
            default="manhattan",
        )
    return parser.parse_args()


def main() -> None:
    arguments = _parse_arguments()
    with open(f"positions/pos{arguments.position}.txt") as position_file:
        current_position = PositionNode(
            [line[:-1].split(" ") for line in position_file], "1"
        )
    last_positions = deque([current_position.board], maxlen=10)
    rounds_count: int = 0

    while current_position.winner == "0":
        to_move = "1" if rounds_count % 2 == 0 else "2"
        rating: int | float = minimax(
            position=current_position,
            to_move=to_move,
            distance_function=DISTANCE_FUNCTION_MAPPING[
                getattr(arguments, f"distance{to_move}")
            ],
            depth=0,
            max_depth=arguments.max_depth,
            pruning=getattr(arguments, f"prune{to_move}"),
        )
        current_position = current_position.find_child_with_rating(rating)
        if arguments.verbose:
            print(current_position.as_table)
            winning = (
                "1"
                if current_position.rating > 0
                else "2" if current_position.rating < 0 else "0"
            )
            print(
                f"RATING: [{constants.COLOR[winning]}]{current_position.rating}\n"
            )
        if last_positions.count(current_position.board) == 2:
            print("[cyan]Position repeated 3 times. It's a draw.")
            return
        last_positions.append(current_position.board)
        rounds_count += 1

    print(f"[cyan]Player {current_position.winner} won after {rounds_count} rounds.")


if __name__ == "__main__":
    main()
