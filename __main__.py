from rich import print

from src import config

from src.game_tree import PositionNode


def main() -> None:
    with open(f"positions/pos{config.POSITION}.txt") as position_file:
        current_position = PositionNode(
            [line[:-1].split(" ") for line in position_file], "1"
        )
    rounds_count: int = 0

    while current_position.winner == "0":
        to_move = "1" if rounds_count % 2 == 0 else "2"
        position_rating = config.TEAM_CONFIG[to_move]["algorithm"](
            current_position, to_move
        )
        current_position = current_position.find_child_with_rating(
            position_rating
        )
        if config.VERBOSE:
            print(current_position.as_table)
            winning = (
                "1"
                if current_position.rating > 0
                else "2" if current_position.rating < 0 else "0"
            )
            print(
                f"RATING: [{config.TEAM_CONFIG[winning]["color"]}]{current_position.rating}\n"
            )
        rounds_count += 1

    print(current_position.winner, rounds_count)


if __name__ == "__main__":
    main()
