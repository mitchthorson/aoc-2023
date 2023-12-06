import argparse
import os
from typing import TypedDict

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class SeedMapRange(TypedDict):
    start_source: int
    start_dest: int
    length: int


class SeedMap:
    def __init__(self, input: str):
        _, input_ranges = input.split(":\n")
        self.ranges = []
        for in_range in input_ranges.splitlines():
            start_dest, start_source, length = list(map(int, in_range.split(" ")))
            self.ranges.append(
                SeedMapRange(
                    start_source=start_source, start_dest=start_dest, length=length
                )
            )

    def get_output(self, seed: int) -> int:
        for range in self.ranges:
            if (
                seed >= range["start_source"]
                and seed < range["start_source"] + range["length"]
            ):
                return range["start_dest"] + seed - range["start_source"]
        return seed


def solve(input: str) -> int:
    seeds, *seedmaps_in = input.split("\n\n")
    seedmaps = [SeedMap(sm) for sm in seedmaps_in]
    locations = []
    for seed in map(int, seeds.replace("seeds: ", "").split(" ")):
        next_input = seed
        for sm in seedmaps:
            next_input = sm.get_output(next_input)
        locations.append(next_input)

    return min(locations)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print("Part 1 answer: {!s}".format(solve(f.read())))


if __name__ == "__main__":
    main()
