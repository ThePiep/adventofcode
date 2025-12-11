from functools import cache
import math
from pathlib import Path

# from tqdm import tqdm

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"
example_path2 = abs_dir / "example2.txt"

Device = str
Input = dict[Device, list[Device]]


def parse_input(input: Path) -> Input:
    return {d[:-1]: ds for d, *ds in map(str.split, open(input))}


def part1(mapping: Input):
    c = 0
    stack = ["you"]
    while len(stack):
        dev = stack.pop()
        if dev == "out":
            c += 1
            continue
        for neigh in mapping[dev]:
            stack.append(neigh)

    return c


def is_reachable(mapping: Input, x: Device, y: Device):
    seen: set[Device] = set([x])
    stack = [x]
    while len(stack):
        current_device = stack.pop()
        if current_device == y:
            return True
        if current_device == "out":
            continue

        for neigh in mapping[current_device]:
            if neigh not in seen:
                seen.add(neigh)
                stack.append(neigh)

    return False


def part2(mapping: Input):
    order = ["svr", "fft", "dac", "out"]
    reach: dict[Device, set[Device]] = {
        d: set(
            filter(
                lambda x: is_reachable(mapping, x, d),
                set(mapping.keys()) | set(["out"]),
            )
        )
        for d in order[1:]
    }

    print("Reachability:", {k: len(v) for k, v in reach.items()})

    @cache
    def _find_r(org: Device, dest: Device) -> int:
        if org == dest:
            return 1
        return sum(
            map(
                lambda n: _find_r(n, dest),
                filter(lambda n: n in reach[dest], mapping[org]),
            )
        )

    res = [(f"{o} -> {d}", _find_r(o, d)) for o, d in zip(order, order[1:])]

    print("number of paths:", res)
    return math.prod(r for _, r in res)


print("-" * 40)

part1_ex = part1(parse_input(example_path))
print("Part 1 (ex): ", part1_ex)
assert part1_ex == 5
print("Part 1: ", part1(parse_input(input_path)))

print("-" * 40)

part2_ex = part2(parse_input(example_path2))
print("Part 2 (ex): ", part2_ex)
assert part2_ex == 2
print("Part 2: ", part2(parse_input(input_path)))

print("-" * 40)
