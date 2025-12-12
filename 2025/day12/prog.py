from functools import cache
import itertools
from pathlib import Path

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"


type Perm = frozenset[tuple[int, int]]


class Box:

    def __init__(self, lines: list[str], id: int) -> None:
        self.lines = lines
        self.id = id
        self.permutations: set[Perm] = set()

        org: set[tuple[int, int]] = set()
        cx, cy = (1, 1)
        for dx, dy in itertools.product([-1, 0, 1], repeat=2):
            nx, ny = cx + dx, cy + dy
            if lines[ny][nx] == "#":
                org.add((dx, dy))
        self.original = frozenset(org)

        self._set_permutations()

    def _set_permutations(self) -> None:
        self.permutations.add(self.original)

        # reflections
        self.permutations.add(frozenset([(-x, y) for x, y in self.original]))
        self.permutations.add(frozenset([(x, -y) for x, y in self.original]))
        self.permutations.add(frozenset([(-x, -y) for x, y in self.original]))

        for perm in self.get_permutations().copy():
            current: set[tuple[int, int]] = set(perm)
            for _ in range(3):
                current = set([(y, -x) for x, y in current])
                self.permutations.add(frozenset(current))

    def get_permutations(self) -> set[Perm]:
        return self.permutations


type Combination = tuple[int, ...]
type Place = tuple[int, int, Combination]
type Input = tuple[list[Box], list[Place]]


def parse_input(input: Path) -> Input:
    *box_lines, place_lines = open(input).read().split("\n\n")

    boxes = [
        Box(b[1:], int(b[0][0])) for b in map(lambda x: str(x).split("\n"), box_lines)
    ]
    places = [
        (int(dim.split("x")[0]), int(dim[:-1].split("x")[1]), tuple(map(int, p)))
        for dim, *p in map(lambda x: x.split(" "), place_lines.strip().split("\n"))
    ]

    return (boxes, places)


def fits(state: str, perm: Perm, x: int, y: int, w: int) -> bool:
    for dx, dy in perm:
        nx, ny = x + dx, y + dy
        if state[nx + w * ny] != ".":
            return False
    return True


# This optimization massively reduces the state space, as taking the minimum will reduce
# equivalent states to a single representative.
def to_standard_perm(state: str, w: int, h: int) -> str:
    res: list[str] = []

    # reflections
    res.append(state)
    res.append(
        "".join([state[w - 1 - (i % w) + w * (i // w)] for i in range(len(state))])
    )
    res.append(
        "".join([state[(i % w) + w * (h - 1 - (i // w))] for i in range(len(state))])
    )
    res.append(
        "".join(
            [state[w - 1 - (i % w) + w * (h - 1 - (i // w))] for i in range(len(state))]
        )
    )
    return min(res)


def print_state(state: str, w: int) -> None:
    l = list((state[i : i + w] for i in range(0, len(state), w)))
    for i in l:
        print(i)


def has_comb(boxes: list[Box], place: Place) -> bool:
    w, h, comb = place
    s = "." * (h * w)
    total_boxes: int = sum(comb)
    box_order: list[Box] = []
    for i, box_count in enumerate(comb):
        box_order += [boxes[i]] * box_count

    @cache
    def has_comb_r(state: str) -> bool:
        num_placed: int = (len(state) - state.count(".")) // 7
        if num_placed == total_boxes:
            print(num_placed)
            print(print_state(state, w))
            return True

        box = box_order[num_placed]
        for x, y in itertools.product(range(1, w - 1), range(1, h - 1)):
            for perm in box.get_permutations():
                if fits(state, perm, x, y, w):
                    new_state = list(state)
                    for dx, dy in perm:
                        nx, ny = x + dx, y + dy
                        new_state[nx + w * ny] = "#"
                    new_state_str = to_standard_perm("".join(new_state), w, h)
                    if has_comb_r(new_state_str):
                        return True
        return False

    return has_comb_r(s)


def part1(input: Input):
    boxes, places = input

    c = 0
    for i, place in enumerate(places):
        w, h, comb = place
        if sum(comb) * 7 > (w) * (h):
            print(f"Impossible case {i}, count: {c}")
        else:
            res = has_comb(boxes, place)
            c += 1 if res else 0
            print(f"Result case {i}: {res}, count: {c}")
    return c


print("-" * 40)

part1_ex = part1(parse_input(example_path))
print("Part 1 (ex): ", part1_ex)
assert part1_ex == True
print("Part 1: ", part1(parse_input(input_path)))
print("-" * 40)
