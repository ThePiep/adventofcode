import itertools
import os

abs_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(abs_dir, "input.txt")
example_path = os.path.join(abs_dir, "example.txt")


type Input = list[str]


def parse_input(input: str) -> Input:
    return [row.strip() for row in open(input).readlines()]


DIRECTIONS: list[tuple[int, int]] = [
    (x, y) for x, y in itertools.product([-1, 0, 1], repeat=2) if x or y
]
print(DIRECTIONS)


def part1(lines: Input):
    d: dict[tuple[int, int], int] = {}
    for x, y in [(x, y) for x in range(len(lines[0])) for y in range(len(lines))]:
        if lines[y][x] == "@":
            d[(x, y)] = 0

    for x, y in d.keys():
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if d.get((nx, ny)) is not None:
                d[(nx, ny)] += 1

    return len(list(filter(lambda x: x < 4, d.values())))


def part2(lines: Input):
    d: dict[tuple[int, int], int] = {}
    for x, y in [(x, y) for x in range(len(lines[0])) for y in range(len(lines))]:
        if lines[y][x] == "@":
            d[(x, y)] = 0

    for x, y in d.keys():
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if d.get((nx, ny)) is not None:
                d[(nx, ny)] += 1
    or_len = len(d)

    done = False
    while not done:
        to_pop: list[tuple[int, int]] = []
        for x, y in list(d.keys()):
            if d[(x, y)] < 4:
                to_pop.append((x, y))
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if d.get((nx, ny)) is not None:
                        d[(nx, ny)] -= 1
        for key in to_pop:
            d.pop(key)
        if not len(to_pop):
            done = True
    return or_len - len(d)


print("Part 1 (ex): ", part1(parse_input(example_path)))
assert part1(parse_input(example_path)) == 13
print("Part 1: ", part1(parse_input(input_path)))

print("Part 2 (ex): ", part2(parse_input(example_path)))
assert part2(parse_input(example_path)) == 43
print("Part 2: ", part2(parse_input(input_path)))
