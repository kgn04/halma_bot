import argparse
from collections import deque

from rich import print
from typing import Callable, Final

from src import constants, minimax, position_rating, PositionNode

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
        help="position id from 'positions' directory (1..101)",
        default=1,
    )
    parser.add_argument(
        "-md",
        "--max-depth",
        type=int,
        help="max game tree depth",
        required=True,
    )
    parser.add_argument(
        "-rl",
        "--rounds-limit",
        type=int,
        help="draw after playing that many rounds",
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


def main(arguments: argparse.Namespace) -> tuple[str, int]:
    with open(f"positions/pos{arguments.position}.txt") as position_file:
        current_position = PositionNode(
            [line[:-1].split(" ") for line in position_file], "1"
        )
    last_positions = deque([current_position.board], maxlen=10)
    rounds_count: int = 0

    while current_position.winner == "0":
        rounds_count += 1
        to_move = "1" if rounds_count % 2 == 1 else "2"
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
                f"Rating: [{constants.COLOR[winning]}]{current_position.rating}[/]\n"
                f" Round: {rounds_count}\n"
            )
        if last_positions.count(current_position.board) == 2:
            print("[cyan]Position repeated 3 times.")
            return "0", rounds_count
        last_positions.append(current_position.board)
        if (
            arguments.rounds_limit is not None
            and rounds_count == arguments.rounds_limit
        ):
            print("[cyan]Rounds limit reached.")
            return "0", rounds_count

    return current_position.winner, rounds_count


if __name__ == "__main__":
    positional_arguments: argparse.Namespace = _parse_arguments()
    winner, rounds = main(positional_arguments)
    if winner == "0":
        print(f"[cyan]Draw after {rounds} rounds.")
    else:
        print(f"[cyan]Player {winner} won after {rounds} rounds.")
