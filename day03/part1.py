import argparse
import os

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class PartNumber:
    """Represents a single part number as part of a schematic"""

    def __init__(self, value: int, x1: int, x2: int, y: int):
        self._value = value
        self._x1 = x1
        self._x2 = x2
        self._y = y

    def __str__(self):
        return "{} <{!s}-{!s}, {!s}>".format(
            str(self._value), self._x1, self._x2, self._y
        )

    def __repr__(self):
        return str(self._value)

    def get_neighbors(self) -> list[tuple[int, int]]:
        result = [(self._x1 - 1, self._y), (self._x2 + 1, self._y)]
        for x in range(self._x1 - 1, self._x2 + 2):
            result.append((x, self._y - 1))
            result.append((x, self._y + 1))
        return result

    @property
    def value(self) -> int:
        return self._value


class EngineSchema:
    """Represents a schema for an engine."""

    def __init__(self, input: str):
        matrix = []
        lines = input.splitlines()
        self._height = len(lines)
        self._width = len(lines[0])
        for y in range(len(lines)):
            matrix.append([])
            line = lines[y]
            chars = list(line)
            for x in range(len(chars)):
                item = chars[x]
                matrix[y].append(self.parse_item(item))
        self._matrix = matrix

    def parse_item(self, item: str) -> str | None:
        if item == "." or is_number(item):
            return item
        return "*"

    def get_part_numbers(self) -> list[PartNumber]:
        result = []
        for y in range(len(self._matrix)):
            line = self._matrix[y]
            skip_list = []
            for x in range(len(self._matrix[y])):
                # skip items that are a part of a previous number
                if x in skip_list:
                    continue
                if is_number(line[x]):
                    part_number = line[x]
                    x2 = x + 1
                    # if we find a number, scan until the end
                    while x2 < len(line) and is_number(line[x2]):
                        skip_list.append(x2)
                        part_number += line[x2]
                        x2 += 1
                    p = PartNumber(int(part_number), x, x2 - 1, y)
                    if self.is_part_number(p):
                        result.append(p)
        return result

    def is_part_number(self, input: PartNumber) -> bool:
        neighbors = input.get_neighbors()
        neighbor_values = [self.get_item(n[0], n[1]) for n in neighbors]
        return "*" in neighbor_values

    def get_item(self, x, y) -> str | None:
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return None
        return self._matrix[y][x]


def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def solve(input: str) -> int:
    schema = EngineSchema(input)
    part_numbers = [p.value for p in schema.get_part_numbers()]
    return sum(part_numbers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 1 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
