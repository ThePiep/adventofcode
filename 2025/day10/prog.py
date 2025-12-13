from functools import cache
import itertools
from typing import Callable
from pathlib import Path
import heapq

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

Lights = int
Button = int
Buttons = list[Button]

Joltages = tuple[int, ...]

Button2 = tuple[int, ...]
Buttons2 = tuple[Button2, ...]


Line = tuple[Lights, Buttons, Joltages]
Line2 = tuple[Lights, Buttons2, Joltages]
Input = list[Line]
Input2 = list[Line2]

to_bin: Callable[[str], int] = lambda cstr: int(cstr, 2)
parse_lights: Callable[[str], Lights] = lambda cstr: int(
    "".join([("1" if c == "#" else "0") for c in cstr]), 2
)


def parse_button(cstr: str, length: int):
    positions = set(map(int, cstr[1:-1].split(",")))
    action: list[str] = ["0"] * (length)
    for pos in positions:
        action[pos] = "1"

    b = int("".join(action), 2)
    return b


def parse_button2(cstr: str) -> Button2:
    positions = tuple(map(int, cstr[1:-1].split(",")))
    return positions


# Experimentation with functional parsing, became troublesome when the input
# of part 2 had different requirements...
parse_buttons: Callable[[list[str], int], Buttons] = lambda cstr, length: list(
    map(lambda c: parse_button(c, length), cstr)
)
parse_buttons2: Callable[[list[str]], Buttons2] = lambda cstr: tuple(
    map(lambda c: parse_button2(c), cstr)
)
parse_joltage: Callable[[str], Joltages] = lambda cstr: tuple(
    map(int, cstr[1:-1].split(","))
)

parse_line: Callable[[tuple[str, list[str], str]], Line] = lambda t: (
    parse_lights(t[0]),
    parse_buttons(t[1], len(t[0])),
    parse_joltage(t[2]),
)

parse_line2: Callable[[tuple[str, list[str], str]], Line2] = lambda t: (
    parse_lights(t[0]),
    parse_buttons2(t[1]),
    parse_joltage(t[2]),
)


def parse_input(input: Path) -> Input:
    raw = [
        (l[0][1:-1], l[1:-1], l[-1])
        for l in [line.strip().split(" ") for line in open(input).readlines()]
    ]
    return list(map(parse_line, raw))


def parse_input2(input: Path) -> Input2:
    raw = [
        (l[0][1:-1], l[1:-1], l[-1])
        for l in [line.strip().split(" ") for line in open(input).readlines()]
    ]
    return list(map(parse_line2, raw))


def min_lights(goal: Lights, actions: Buttons) -> int:
    heap: list[tuple[int, Lights]] = []
    state: Lights = 0
    seen_states: set[Lights] = set([state])

    heapq.heappush(heap, (0, state))
    while len(heap) > 0:
        cost, state = heapq.heappop(heap)
        if state == goal:
            return cost

        for action in actions:
            new_state = state ^ action
            if not new_state in seen_states:
                seen_states.add(new_state)
                heapq.heappush(heap, (cost + 1, new_state))

    raise ValueError(f"No combination found: goal: {bin(goal)}")


def part1(lines: Input):
    c = 0
    for goal, actions, _joltages in lines:
        c += min_lights(goal, actions)
    return c


def convert_action(number: int, length: int) -> Button2:
    bits: list[int] = []
    num = bin(number)[2:]
    while len(num) < length:
        num = "0" + num
    for i, c in enumerate(num):
        if c == "1":
            bits.append(i)
    return tuple(bits)


@cache
def ways_to_reach_mask(actions: Buttons2, mask: tuple[bool, ...]) -> list[set[Button2]]:
    res: list[set[Button2]] = []

    state: list[bool] = [False] * len(mask)
    res: list[set[Button2]] = []
    for L in range(len(actions) + 1):
        for action in itertools.combinations(actions, r=L):
            new_state = state.copy()
            for a in action:
                for pos in a:
                    new_state[pos] = not new_state[pos]
            new_state = tuple(new_state)
            if new_state == mask:
                res.append(set(action))

    return res


def min_joltage(actions: Buttons2, goal: Joltages) -> int:
    goal_state: Joltages = (0,) * len(goal)

    @cache
    def _min_joltage_r(state: tuple[int, ...]) -> int:
        if state == goal_state:
            return 0
        if any([state[i] < 0 for i in range(len(state))]):
            return 1000000

        odd_mask = tuple(map(lambda x: (x % 2) == 1, state))

        ways: list[set[Button2]] = ways_to_reach_mask(actions, odd_mask)
        c = 1000000
        for way in ways:
            l = len(way)
            new_state = list(state)
            for action in way:
                for pos in action:
                    new_state[pos] -= 1
            new_state = tuple(new_state)
            c = min(c, l + 2 * _min_joltage_r(tuple(map(lambda x: x // 2, new_state))))
        return c

    return _min_joltage_r(goal)


def part2(lines: Input2):

    c = 0
    for i, (_goal, actions, joltages) in enumerate(lines[:]):
        add = min_joltage(actions, joltages)
        print(i, add)
        c += add
    return c


print("Part 1 (ex): ", part1(parse_input(example_path)))
assert part1(parse_input(example_path)) == 7
print("Part 1: ", part1(parse_input(input_path)))

"""
Although the algorithm should find the answer, the BFS and DPS methods might even be
too slow to find it in my lifetime... Will aim improve the solution using linear algebra
and Gaussian Elimination in the future.

EDIT: Implemented a divide and conquer approach, the goal of which is to reduce to even 
joltage levels and then divide by 2 to reduce the state space. This works fine and the 
underlying theory has many parallels with the Gaussian elimination approach.
"""
print("Part 2 (ex): ", part2(parse_input2(example_path)))
assert part2(parse_input2(example_path)) == 33
print("Part 2: ", part2(parse_input2(input_path)))
