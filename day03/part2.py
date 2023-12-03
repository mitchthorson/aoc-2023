import argparse
import os

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class Gear:
    def __init__(self, ratio: tuple[int, int]):
        self._ratio = ratio

    def __str__(self):
        return "{} <{}:{}>".format(self.ratio_value, self._ratio[0], self._ratio[1])

    @property
    def ratio_value(self) -> int:
        return self._ratio[0] * self._ratio[1]


class GearValue:
    """Represents a single gear number as part of a gear ratio"""

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

    def is_neighbor(self, point: tuple[int, int]) -> bool:
        x, y = point
        result = (
            x >= self._x1 - 1
            and x <= self._x2 + 1
            and y >= self._y - 1
            and y <= self._y + 1
        )
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
                matrix[y].append(item)
        self._matrix = matrix

    def get_numbers(self) -> list[GearValue]:
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
                    p = GearValue(int(part_number), x, x2 - 1, y)
                    result.append(p)
        return result

    def get_gears(self) -> list[Gear]:
        # get all of the numbers present in the schema
        numbers = self.get_numbers()
        # will hold each possible gear location
        gears = []
        for y in range(len(self._matrix)):
            for x in range(len(self._matrix[y])):
                if self.get_item(x, y) == "*":
                    point = (x, y)
                    gear_numbers = list(
                        filter(lambda num: num.is_neighbor(point), numbers)
                    )
                    if len(gear_numbers) == 2:
                        gear = Gear((gear_numbers[0].value, gear_numbers[1].value))
                        gears.append(gear)
        # print(possible_gears)
        return gears

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
    gears = schema.get_gears()
    gear_ratios = [g.ratio_value for g in gears]
    return sum(gear_ratios)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 1 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
