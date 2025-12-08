def parse_instr(filename: str):
    return [
        (line.strip()[0], int(line.strip()[1:])) for line in open(filename).readlines()
    ]


def part1(instr: list[tuple[str, int]]) -> int:
    p = 50
    c = 0
    for dir, num in instr:
        p = (p + (num if dir == "R" else -num)) % 100
        if p == 0:
            c += 1

    return c


def part2(instr: list[tuple[str, int]]) -> int:
    p = 50  # pointer
    c = 0  # count
    for dir, num in instr:
        c += num // 100  # add rotations
        num = num % 100
        cp = p
        np = p + (num if dir == "R" else -num)
        p = np % 100
        if (cp != 0 and np != p) or (p == 0 and cp != 0):
            c += 1
    return c


input = "2025/day1/input.txt"
example = "2025/day1/example.txt"

assert part1(parse_instr(example)) == 3
print(f"Part 1: {part1(parse_instr(input))}")

assert part2(parse_instr(example)) == 6
print(f"Part 2: {part2(parse_instr(input))}")
