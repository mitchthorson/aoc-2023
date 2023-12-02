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


number_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def is_text_number(input: str) -> bool:
    """Check if input is a text representation of a number"""
    return input in number_map.keys()


def convert_number(input: str) -> str:
    """Return numberic string replacement for a spelled out number"""
    return number_map[input]


def scan_line(line: list[str]) -> list[str]:
    """Extract numbers from a line of text"""
    results = []
    for start in range(len(line)):
        for end in range(start + 1, len(line) + 1):
            chunk = "".join(line[start:end])
            if is_text_number(chunk):
                results.append(convert_number(chunk))
            if is_number(chunk):
                results.append(chunk)
    return results


def solve(input: str) -> int:
    lines = list(filter(lambda l: len(l) > 0, input.splitlines()))
    line_nums = [scan_line(list(l)) for l in lines]
    return sum([get_value(l) for l in line_nums])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 2 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
