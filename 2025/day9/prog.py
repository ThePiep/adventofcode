import math
from pathlib import Path
from typing import Any, Callable
from tqdm import tqdm
from itertools import combinations

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

type Tile = tuple[int, int]
type Tiles = list[Tile]


# Experimenting with lambda functions, the typing is awkwardly long and can not be defined
# when writing the lambda inline...
split: Callable[[str], list[str]] = lambda x: x.strip().split(",")
to_tuple: Callable[[list[str]], tuple[Any, Any]] = lambda x: (int(x[0]), int(x[1]))


def parse_input(input: Path) -> Tiles:
    return list(
        map(
            to_tuple,
            map(split, open(input).readlines()),
        )
    )


def size(t1: Tile, t2: Tile):
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def part1(tiles: Tiles):
    s = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            ns = size(tiles[i], tiles[j])
            s = max(s, ns)
    return s


def __get_neighbors(tiles: Tiles, tile: Tile) -> tuple[set[Tile], set[Tile]]:
    hor = set(filter(lambda t: t[1] == tile[1] and t != tile, tiles))
    vert = set(filter(lambda t: t[0] == tile[0] and t != tile, tiles))
    return (hor, vert)


# A script that builds the loop given unordered input, I wrote this
# before I figured out that the input was ordered...
def __build_loop(tiles: Tiles) -> dict[Tile, Tile]:
    # find first tile
    ft = None  # first tile
    i = 0
    while not ft and i < len(tiles):
        hor, vert = __get_neighbors(tiles, tiles[i])
        if len(hor) == 1 and len(vert) == 1:
            ft = tiles[i]
        i += 1
    if ft == None:
        raise ValueError("Panic!")

    route: dict[Tile, Tile] = {}  # Map to next tile in route
    ct = ft  # current tile
    while len(route) < len(tiles):
        seen = set(route.keys())
        if len(seen) > 2:
            seen.remove(ft)
        # while prev != ft:
        hor, vert = __get_neighbors(tiles, ct)
        dhor: set[Tile] = hor - seen
        dvert: set[Tile] = vert - seen
        if len(dhor) >= 1 and len(dvert) != 1:
            print("hor")
            route[ct] = list(sorted(dhor, key=lambda t: abs(t[0] - ct[0])))[0]
            ct = route[ct]
        elif len(dvert) >= 1:
            print("ver")
            route[ct] = list(sorted(dvert, key=lambda t: abs(t[1] - ct[1])))[0]
            ct = route[ct]

        else:
            raise ValueError(
                "Panic!", ft, ct, ("vert", vert, dvert), ("hor", hor, dhor), route, seen
            )
    return route


def falls_in(t: Tile, t1: Tile, t2: Tile):
    min_x, max_x = min(t1[0], t2[0]), max(t1[0], t2[0])
    min_y, max_y = min(t1[1], t2[1]), max(t1[1], t2[1])
    return min_x < t[0] < max_x and min_y < t[1] < max_y


def on_edge(t: Tile, t1: Tile, t2: Tile):
    min_x, max_x = min(t1[0], t2[0]), max(t1[0], t2[0])
    min_y, max_y = min(t1[1], t2[1]), max(t1[1], t2[1])
    return (
        (t[0] == min_x or t[0] == max_x)
        and min_y < t[1] < max_y
        or (t[0] == min_x or t[0] == max_x)
        and min_y < t[1] < max_y
    )


def points_inward_on_edge(tiles: Tiles, t: Tile, t1: Tile, t2: Tile):
    min_x, max_x = min(t1[0], t2[0]), max(t1[0], t2[0])
    min_y, max_y = min(t1[1], t2[1]), max(t1[1], t2[1])
    idx = tiles.index(t)

    prev = tiles[idx - 1]
    next = tiles[(idx + 1) % len(tiles)]

    points_left = prev[0] < t[0] or next[0] < t[0]
    points_right = prev[0] > t[0] or next[0] > t[0]
    points_down = prev[1] < t[1] or next[1] < t[1]
    points_up = prev[1] > t[1] or next[1] > t[1]

    assert (
        len(
            list(
                filter(lambda x: x, [points_left, points_right, points_down, points_up])
            )
        )
        == 2
    )

    if t[0] == min_x and min_y < t[1] < max_y:
        if points_right:
            return True
    if t[0] == max_x and min_y < t[1] < max_y:
        if points_left:
            return True
    if t[1] == min_y and min_x < t[0] < max_x:
        if points_up:
            return True
    if t[1] == max_y and min_x < t[0] < max_x:
        if points_down:
            return True
    return False


def passes_through(line: tuple[Tile, Tile], t1: Tile, t2: Tile):
    min_x, max_x = min(t1[0], t2[0]), max(t1[0], t2[0])
    min_y, max_y = min(t1[1], t2[1]), max(t1[1], t2[1])
    c1, c2 = line
    if c1[0] == c2[0]:
        y_start = min(c1[1], c2[1])
        y_end = max(c1[1], c2[1])
        if y_start < min_y and y_end > max_y:
            return True

    if c1[1] == c2[1]:
        x_start = min(c1[0], c2[0])
        x_end = max(c1[0], c2[0])
        if x_start < min_x and x_end > max_x:
            return True
    return False


def is_valid(tiles: Tiles, edges: list[tuple[Tile, Tile]], t1: Tile, t2: Tile):
    for i1, i2 in edges:
        if i1 == t1 or i1 == t2:
            continue
        if falls_in(i1, t1, t2):
            # print("false falls in!")
            return False
        if points_inward_on_edge(tiles, i1, t1, t2):
            return False
        if passes_through((i1, i2), t1, t2):
            # print("pass through!")
            return False

    return True


def part2(tiles: Tiles):
    s = 0
    edges = list(zip(tiles, tiles[1:] + [tiles[0]]))
    for i, j in tqdm(
        combinations(range(len(tiles)), 2), total=math.comb(len(tiles), 2)
    ):
        ns = size(tiles[i], tiles[j])
        if ns > s and is_valid(tiles, edges, tiles[i], tiles[j]):
            s = ns
            print("\n Improved size:", s, i, j, tiles[i], tiles[0])
    return s


print("Part 1 (ex): ", part1(parse_input(example_path)))
assert part1(parse_input(example_path)) == 50
print("Part 1: ", part1(parse_input(input_path)))

print("Part 2 (ex): ", part2(parse_input(example_path)))
# assert part2(parse_input(example_path)) == 24
print("Part 2: ", part2(parse_input(input_path)))
