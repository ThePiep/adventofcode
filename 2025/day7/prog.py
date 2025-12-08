from functools import cache
from typing import Any
from pathlib import Path

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

type Input = list[Any]


def parse_input(input: Path) -> Input:
    return [line for line in open(input).readlines()]


def part1(lines: Input):
    count = 0
    lasers = set({lines[0].find("S")})
    for line in lines[1:]:
        to_remove: set[int] = set()
        to_add: set[int] = set()
        for laser in lasers:
            if line[laser] == "^":
                to_add.add(laser - 1)
                to_add.add(laser + 1)
                to_remove.add(laser)
                count += 1
        lasers -= to_remove
        lasers |= to_add
    print(lasers)
    return count


def part2(lines: Input):
    @cache
    def part2_rec(row: int, laser_pos: int, count: int) -> int:
        # print(len(lines))
        print(row)
        if row >= len(lines):
            return 1
        if lines[row][laser_pos] == "^":
            return part2_rec(row + 1, laser_pos=laser_pos - 1, count=count) + part2_rec(
                row + 1, laser_pos=laser_pos + 1, count=count
            )
        else:
            return part2_rec(row + 1, laser_pos=laser_pos, count=count)

    return part2_rec(1, lines[0].find("S"), 0)


print("Part 1 (ex): ", part1(parse_input(example_path)))
assert part1(parse_input(example_path)) == 21
print("Part 1: ", part1(parse_input(input_path)))

print("Part 2 (ex): ", part2(parse_input(example_path)))
# assert part2(parse_input(example_path)) == 40
print("Part 2: ", part2(parse_input(input_path)))
