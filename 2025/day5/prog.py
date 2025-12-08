from pathlib import Path

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

type Input = tuple[list[tuple[int, int]], list[int]]


def parse_input(input: Path) -> Input:
    rranges, rids = open(input).read().split("\n\n")
    ranges = [
        (int(r.split("-")[0]), int(r.split("-")[1])) for r in rranges.splitlines()
    ]
    ids = [int(id) for id in rids.splitlines()]
    return ranges, ids


def part1(input: Input):
    ranges, ids = input
    c = 0
    for id in ids:
        for r in ranges:
            if r[0] <= id <= r[1]:
                c += 1
                break
    return c


def check_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    return (
        r1[0] - 1 <= r2[0] <= r1[1] + 1
        or r1[0] - 1 <= r2[1] <= r1[1] + 1
        or (r2[0] <= r1[0] and r2[1] >= r1[1])
    )


def part2(input: Input):
    ranges, _ = input
    ranges = sorted(ranges, key=lambda x: x[0])
    i = 0
    while i < len(ranges):
        lb, rb = ranges[i]
        to_del_ids: set[int] = set()
        j = i + 1
        while j < len(ranges):
            l2, r2 = ranges[j]
            if check_overlap((lb, rb), (l2, r2)):
                to_del_ids.add(j)
                lb, rb = (min(lb, l2), max(rb, r2))
            j += 1

        ranges[i] = (lb, rb)

        if len(to_del_ids):
            for id in sorted(to_del_ids, reverse=True):
                ranges.pop(id)
        else:
            i += 1

    return sum([r[1] - r[0] + 1 for r in ranges])


print("Part 1 (ex): ", part1(parse_input(example_path)))
assert part1(parse_input(example_path)) == 3
print("Part 1: ", part1(parse_input(input_path)))

print("Part 2 (ex): ", part2(parse_input(example_path)))
assert part2(parse_input(example_path)) == 14
print("Part 2: ", part2(parse_input(input_path)))
