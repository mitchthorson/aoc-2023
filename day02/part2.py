import argparse
import os
import re
from typing import TypedDict


class CubeSample(TypedDict):
    red: int
    green: int
    blue: int


class ParsedCubeGame(TypedDict):
    id: int
    samples: list[CubeSample]


class CubeGame:
    """A class that represents a single CubeGame, including the id and samples"""

    def __init__(self, input: str) -> None:
        parsed_game = self.parse(input)
        self._id = parsed_game["id"]
        self._samples = parsed_game["samples"]

    def parse(self, input: str) -> ParsedCubeGame:
        game_sample = input.split(":")
        id = int(game_sample[0].replace("Game ", ""))
        raw_samples = game_sample[1].split(";")
        return ParsedCubeGame(
            id=id, samples=[self.parse_sample(s) for s in raw_samples]
        )

    def parse_sample(self, input: str) -> CubeSample:
        trimmed = input.strip()
        result = CubeSample(red=0, green=0, blue=0)
        for item in trimmed.split(", "):
            # Define a pattern using a regular expression
            pattern = re.compile(r"(\d+) (\D+)")

            # Use the pattern to match and extract values
            match = pattern.match(item)

            if match:
                # Extract variables
                quantity = int(match.group(1))
                color = match.group(2)

                result[color] = quantity
            else:
                raise ValueError("Pattern not matched for sample: {}".format(item))
        return result

    def get_max_sample(self):
        result = CubeSample(red=0, green=0, blue=0)
        for sample in self.samples:
            for color in sample:
                if sample[color] > result[color]:
                    result[color] = sample[color]
        return result

    def check_sample(self, input: CubeSample) -> bool:
        max = self.get_max_sample()
        for color in input:
            if input[color] < max[color]:
                return False
        return True

    def get_max_sample_power(self):
        max = self.get_max_sample()
        return max["red"] * max["blue"] * max["green"]

    @property
    def id(self) -> int:
        return self._id

    @property
    def samples(self) -> list[CubeSample]:
        return self._samples


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def solve(input: str) -> int:
    input_games = input.splitlines()
    games = [CubeGame(g) for g in input_games]
    powers = [g.get_max_sample_power() for g in games]
    return sum(powers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 1 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
