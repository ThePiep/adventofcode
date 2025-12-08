from tqdm import tqdm


def parse_input(filename: str):
    return [
        tuple(map(int, range.split("-")))
        for range in open(filename).read().strip().split(",")
    ]

def has_double_repeated(id: int):
    str_rep = str(id)
    l = len(str_rep)
    if len(str_rep) % 2 != 0:
        return False

    left, right = str_rep[: l // 2], str_rep[l // 2 :]

    return left == right


def has_sequence_repeated(id: int):
    str_rep = str(id)
    l = len(str_rep)
    for i in range(l):
        if l % (i + 1) == 0:
            n = i + 1
            sections = [str_rep[i : i + n] for i in range(0, l, n)]
            if len(sections) > 1 and all(
                [(pair[0] == pair[1]) for pair in zip(sections, sections[1:])]
            ):
                return True

    return False


def part1(ranges: list[tuple[int, ...]]):
    c = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            if has_double_repeated(i):
                c += i
    return c


def part2(ranges: list[tuple[int, ...]]):
    c = 0
    for r in tqdm(ranges):
        for i in range(r[0], r[1] + 1):
            if has_sequence_repeated(i):
                c += i
    return c


assert part1(parse_input("2025/day2/example.txt")) == 1227775554, "Fail example part 1"
print("Part 1: ", part1(parse_input("2025/day2/input.txt")))
assert part2(parse_input("2025/day2/example.txt")) == 4174379265, "Fail example part 2"
print("Part 2: ", part2(parse_input("2025/day2/input.txt")))
