from typing import Callable
from pathlib import Path
import heapq
from tqdm import tqdm

abs_dir = Path(__file__).parent
input_path = abs_dir / "input.txt"
example_path = abs_dir / "example.txt"

Lights = int
Button = int
Buttons = list[Button]
Joltages = tuple[int, ...]

Line = tuple[Lights, Buttons, Joltages]
Input = list[Line]

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


parse_buttons: Callable[[list[str], int], Buttons] = lambda cstr, length: list(
    map(lambda c: parse_button(c, length), cstr)
)
parse_joltage: Callable[[str], Joltages] = lambda cstr: tuple(
    map(int, cstr[1:-1].split(","))
)

parse_line: Callable[[tuple[str, list[str], str]], Line] = lambda t: (
    parse_lights(t[0]),
    parse_buttons(t[1], len(t[0])),
    parse_joltage(t[2]),
)


def parse_input(input: Path) -> Input:
    raw = [
        (l[0][1:-1], l[1:-1], l[-1])
        for l in [line.strip().split(" ") for line in open(input).readlines()]
    ]
    return list(map(parse_line, raw))


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
    for goal, actions, _joltages in tqdm(lines):
        c += min_lights(goal, actions)

    return c


ButtonC = list[int]
ButtonsC = list[ButtonC]


def min_joltage(actions: ButtonsC, goal: Joltages) -> int:
    heap: list[tuple[int, Joltages]] = []
    floor: Joltages = tuple([0] * len(goal))
    state: Joltages = goal
    seen_states: set[tuple[int, ...]] = set([tuple(state)])
    max_cost = 0

    heapq.heappush(heap, (0, state))
    while len(heap) > 0:
        cost, state = heapq.heappop(heap)
        max_cost = max(cost, max_cost)
        if state == floor:
            return cost

        for action in list(sorted(actions, key=len, reverse=True)):
            new_state = list(state)
            for pos in action:
                new_state[pos] -= 1
            new_state = tuple(new_state)
            if not new_state in seen_states and all(
                [new_state[i] >= floor[i] for i in range(len(state))]
            ):
                seen_states.add(new_state)
                heapq.heappush(heap, (cost + 1, new_state))

    raise ValueError(f"No combination found: goal: {goal}")


def convert_action(number: int, length: int) -> ButtonC:
    bits: list[int] = []
    num = bin(number)[2:]
    while len(num) < length:
        num = "0" + num
    for i, c in enumerate(num):
        if c == "1":
            bits.append(i)
    return bits


def part2(lines: Input):
    c = 0
    i = 0
    for _goal, actions, joltages in lines[:]:
        # print(_goal)
        actions_c = list(map(lambda a: convert_action(a, len(joltages)), actions))
        add = min_joltage(actions_c, joltages)
        # print(i, add)
        c += add
        i += 1

    return c


print("Part 1 (ex): ", part1(parse_input(example_path)))
assert part1(parse_input(example_path)) == 7
print("Part 1: ", part1(parse_input(input_path)))

print("Part 2 (ex): ", part2(parse_input(example_path)))
assert part2(parse_input(example_path)) == 33
"""
Although the algorithm should find the answer, the BFS and DPS methods might even be
too slow to find it in my lifetime... Will aim improve the solution using linear algebra
and Gaussian Elimination in the future.
"""
print("Part 2: ", part2(parse_input(input_path)))
