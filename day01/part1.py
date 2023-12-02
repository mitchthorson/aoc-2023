import argparse
import os

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_value(line: list[str]) -> int:
    return int("".join([line[0], line[-1]]))


def solve(input: str) -> int:
    lines = input.splitlines()
    line_nums = list(
        filter(lambda l: len(l) > 0, [list(filter(is_number, list(l))) for l in lines])
    )
    return sum([get_value(l) for l in line_nums])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 1 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
