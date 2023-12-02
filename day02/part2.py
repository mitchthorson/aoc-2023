import argparse
import os

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def solve(input: str) -> int:
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 2 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
