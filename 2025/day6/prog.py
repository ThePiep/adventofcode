from itertools import zip_longest
from pathlib import Path

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

type Input = list[tuple[list[int], str]]
type InputRep = list[tuple[list[int], str, bool]]


def parse_example(input: Path) -> Input:
    output2d = [
        list(filter(lambda x: len(x) > 0, line.strip().split(" ")))
        for line in open(input).readlines()
    ]
    ops = list(
        map(
            lambda x: ([int(x[0]), int(x[1]), int(x[2])], str(x[3])),
            zip(*output2d),
        )
    )
    return ops


def parse_input(input: Path) -> Input:
    output2d = [
        list(filter(lambda x: len(x) > 0, line.strip().split(" ")))
        for line in open(input).readlines()
    ]
    operations = list(
        map(
            lambda x: ([int(x[0]), int(x[1]), int(x[2]), int(x[3])], str(x[4])),
            zip(*output2d),
        )
    )
    return operations


def part1(ops: Input):
    total = 0
    for op in ops:
        operant = op[1]
        subtotal: int = 0 if operant == "+" else 1
        for i in range(0, len(op[0])):
            if operant == "+":
                subtotal += op[0][i]
            if operant == "*":
                subtotal *= op[0][i]
        total += subtotal

    return total


# TODO: This should just have been a new parse function...
def ops_repair(ops: Input, path: Path) -> Input:
    lines = [line for line in open(path)]
    x = 0
    is_rev: list[bool] = []
    for i in range(len(ops)):
        width = max(len(str(num)) for num in ops[i][0])
        found_blank = False
        for line in lines[:-1]:
            if line[x] == " ":
                found_blank = True
        is_rev.append(found_blank)
        x += width + 1

    new_ops: Input = [
        (
            [
                int(str("".join(zipper)))
                for zipper in zip_longest(
                    *[
                        list(str(num))[::-1] if is_rev[i] else list(str(num))
                        for num in nums
                    ],
                    fillvalue="",
                )
            ],
            op,
        )
        for i, (nums, op) in enumerate(ops)
    ]
    return new_ops


def part2(ops: Input):
    total = 0
    for op in ops:
        operant = op[1]
        subtotal: int = 0 if operant == "+" else 1
        for i in range(0, len(op[0])):
            if operant == "+":
                subtotal += op[0][i]
            if operant == "*":
                subtotal *= op[0][i]
        total += subtotal

    return total


# print("Part 1 (ex): ", part1(parse_example(example_path)))
# assert part1(parse_example(example_path)) == 4277556
# print("Part 1: ", part1(parse_input(input_path)))

print("Part 2 (ex): ", part2(ops_repair(parse_example(example_path), example_path)))
assert part2(ops_repair(parse_example(example_path), example_path)) == 3263827
print("Part 2: ", part2(ops_repair(parse_input(input_path), input_path)))
