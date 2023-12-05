import argparse
import os

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def solve(input: str) -> int:
    card_scores = []
    for line in input.splitlines():
        my_winners = []
        card_id, nums = line.split(": ")
        winning_nums, my_nums = map(lambda n: map(int, list(filter(is_number, n.split(" ")))), nums.split(" | "))
        my_nums_list = list(my_nums)
        winning_nums_list = list(winning_nums)
        for check_num in list(my_nums_list):
            if check_num in winning_nums_list:
                my_winners.append(check_num)
        game_score = 0
        print("Total matches: {}".format(len(my_winners)))
        for i in range(len(my_winners)):
            if i == 0:
                game_score = 1
            else:
                game_score = game_score * 2
        print("Final game score is: {}".format(game_score))
        card_scores.append(int(game_score))
    return sum(card_scores)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 1 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
