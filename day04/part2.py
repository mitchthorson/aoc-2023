import argparse
import os
from typing import TypedDict

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class ScratchGame(TypedDict):
    id: int
    winning_nums: list[int]
    my_nums: list[int]


def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def parse_game_id(input_id: str) -> int:
    return int(input_id.replace("Card ", "").strip())


def parse_game(game_input: str) -> ScratchGame:
    card_id, nums = game_input.split(": ")
    winning_nums, my_nums = map(
        lambda n: map(int, list(filter(is_number, n.split(" ")))), nums.split(" | ")
    )
    my_nums_list = list(my_nums)
    winning_nums_list = list(winning_nums)
    return ScratchGame(
        {
            "id": parse_game_id(card_id),
            "winning_nums": winning_nums_list,
            "my_nums": my_nums_list,
        }
    )


def get_game_winners(game_input: ScratchGame) -> list[int]:
    my_winners = []
    for check_num in game_input["my_nums"]:
        if check_num in game_input["winning_nums"]:
            my_winners.append(check_num)
    return my_winners


def solve(input: str) -> int:
    original_games = [parse_game(line) for line in input.splitlines()]
    game_copies = [1 for game in original_games]
    for i in range(len(original_games)):
        current_game = original_games[i]
        num_winners = len(get_game_winners(current_game))
        current_copy_count = game_copies[i]
        # add copies for each winner
        for j in range(i + 1, i + num_winners + 1):
            game_copies[j] += current_copy_count

    return sum(game_copies)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 1 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
