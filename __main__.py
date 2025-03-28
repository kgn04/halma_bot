from rich import print

import config

from game_tree import PositionNode


def main() -> None:
    with open(f"positions/pos{config.POSITION}.txt") as position_file:
        tree = PositionNode(
            [line[:-1].split(" ") for line in position_file], "1"
        )
    tree.root_initialization()
    rounds_count: int = 0

    while tree.winner == "0":
        to_move = "1" if rounds_count % 2 == 0 else "2"
        position_rating = config.TEAM_CONFIG[to_move]["algorithm"](
            tree, to_move
        )
        print("dupa ", position_rating)
        tree = tree.find_child_with_rating(position_rating)
        if config.VERBOSE:
            print(tree.as_table)
            winning = "1" if position_rating > 0 else "2" if position_rating < 0 else "0"
            print(f"RATING: [{config.TEAM_CONFIG[winning]["color"]}]{position_rating}\n")
        tree.find_new_moves()
        rounds_count += 1

    print(tree.winner, rounds_count)


if __name__ == "__main__":
    main()
