from typing import Any
from pathlib import Path

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

type Input = list[Any]


def parse_input(input: Path) -> Input:
    return [line for line in open(input).readlines()]


def part1(lines: Input):
    pass


def part2(lines: Input):
    pass


print("Part 1 (ex): ", part1(parse_input(example_path)))
assert part1(parse_input(example_path)) == True
print("Part 1: ", part1(parse_input(input_path)))

print("Part 2 (ex): ", part2(parse_input(example_path)))
assert part2(parse_input(example_path)) == True
print("Part 2: ", part2(parse_input(input_path)))
