from functools import reduce
from pathlib import Path
from tqdm import tqdm

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

type Cord = tuple[int, int, int]
type Cords = list[Cord]


def parse_input(input: Path) -> Cords:
    return [
        (scord[0], scord[1], scord[2])
        for scord in [
            list(map(int, cord.strip().split(","))) for cord in open(input).readlines()
        ]
    ]


def dist(cord1: Cord, cord2: Cord) -> float:
    return (
        (cord1[0] - cord2[0]) ** 2
        + (cord1[1] - cord2[1]) ** 2
        + (cord1[2] - cord2[2]) ** 2
    )


def part1(cords: Cords, n: int):
    store: list[tuple[float, Cord, Cord]] = []
    for i, cord1 in tqdm(enumerate(cords), desc="Building distance store"):
        for _, cord2 in enumerate(cords[i + 1 :]):
            d = dist(cord1, cord2)
            # bisect.insort_right(store, (d, cord1, cord2), key=lambda x: x[0])
            store.append((d, cord1, cord2))
    store.sort(key=lambda x: x[0])

    sets: list[set[Cord]] = [set({cord}) for cord in cords]
    for _, cord1, cord2 in tqdm(store[:n], desc="Building components"):
        set1, set2 = None, None
        for s in sets:
            set1 = s if cord1 in s else set1
            set2 = s if cord2 in s else set2
        if set1 is None or set2 is None:
            raise Exception("set not found")
        if set1 & set2 == set():
            set1 |= set2
            sets.remove(set2)

    lens = sorted([len(s) for s in sets], reverse=True)
    return reduce(lambda a, b: a * b, lens[:3], 1)


def part2(cords: Cords):
    store: list[tuple[float, Cord, Cord]] = []
    for i, cord1 in tqdm(
        enumerate(cords), total=len(cords), desc="Building distance store"
    ):
        for _, cord2 in enumerate(cords[i + 1 :]):
            d = dist(cord1, cord2)
            # bisect.insort_right(store, (d, cord1, cord2), key=lambda x: x[0])
            store.append((d, cord1, cord2))
    store.sort(key=lambda x: x[0])

    sets: list[set[Cord]] = [set({cord}) for cord in cords]
    i = 0
    last_cord: tuple[Cord, Cord] = ((0, 0, 0), (0, 0, 0))
    while len(sets) > 1:
        _, cord1, cord2 = store[i]
        last_cord = (cord1, cord2)
        set1, set2 = None, None
        for s in sets:
            set1 = s if cord1 in s else set1
            set2 = s if cord2 in s else set2
        if set1 is None or set2 is None:
            raise Exception("set not found")
        if set1 & set2 == set():
            set1 |= set2
            sets.remove(set2)
        i += 1

    return last_cord[0][0] * last_cord[1][0]


print("Part 1 (ex): ", part1(parse_input(example_path), 10))
assert part1(parse_input(example_path), 10) == 40
print("Part 1: ", part1(parse_input(input_path), 1000))

print("Part 2 (ex): ", part2(parse_input(example_path)))
assert part2(parse_input(example_path)) == 25272
print("Part 2: ", part2(parse_input(input_path)))
