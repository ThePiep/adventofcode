from functools import reduce
import heapq
from pathlib import Path
from tqdm import tqdm

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

type Cord = tuple[int, int, int]
type Cords = list[Cord]


def parse_input(input: Path) -> Cords:
    return [
        (c[0], c[1], c[2])
        for c in [
            list(map(int, cord.strip().split(","))) for cord in open(input).readlines()
        ]
    ]


def dist(cord1: Cord, cord2: Cord) -> int:
    return (
        (cord1[0] - cord2[0]) ** 2
        + (cord1[1] - cord2[1]) ** 2
        + (cord1[2] - cord2[2]) ** 2
    )


def uf_find(uf: dict[Cord, Cord], cord: Cord) -> Cord:
    if cord == uf[cord]:
        return cord
    uf[cord] = uf_find(uf, uf[cord])
    return uf[cord]


def uf_combine(uf: dict[Cord, Cord], cord1: Cord, cord2: Cord) -> None:
    uf[uf_find(uf, cord1)] = uf_find(uf, cord2)


def sort_by_dist(cords: Cords):
    store: list[tuple[float, Cord, Cord]] = []
    for i, cord1 in tqdm(enumerate(cords), desc="Building distance store"):
        for _, cord2 in enumerate(cords[i + 1 :]):
            d = dist(cord1, cord2)
            heapq.heappush(store, (d, cord1, cord2))
    return store


def part1(cords: Cords, n: int):
    store = sort_by_dist(cords)

    UF: dict[Cord, Cord] = {i: i for i in cords}  # union-find structure
    for _, cord1, cord2 in heapq.nsmallest(n, store):
        if uf_find(UF, cord1) != uf_find(UF, cord2):
            uf_combine(UF, cord1, cord2)

    D: dict[Cord, set[Cord]] = {}
    for x in cords:
        if uf_find(UF, x) not in D:
            D[uf_find(UF, x)] = set()
        D[uf_find(UF, x)].add(x)

    lens = sorted([len(v) for v in D.values()], reverse=True)
    return reduce(lambda a, b: a * b, lens[:3], 1)


def part2(cords: Cords):
    store = sort_by_dist(cords)
    UF: dict[Cord, Cord] = {i: i for i in cords}  # union-find structure
    con = 0
    _, cord1, cord2 = store[0]
    while con < len(cords) - 1:
        _, cord1, cord2 = heapq.heappop(store)
        if uf_find(UF, cord1) != uf_find(UF, cord2):
            uf_combine(UF, cord1, cord2)
            con += 1
    return cord1[0] * cord2[0]


print("Part 1 (ex): ", part1(parse_input(example_path), 10))
assert part1(parse_input(example_path), 10) == 40
print("Part 1: ", part1(parse_input(input_path), 1000))


print("Part 2 (ex): ", part2(parse_input(example_path)))
assert part2(parse_input(example_path)) == 25272
print("Part 2: ", part2(parse_input(input_path)))
