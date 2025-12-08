type Input = list[list[int]]


def parse_input(input: str) -> Input:
    return [list(map(int, bank.strip())) for bank in open(input).readlines()]


def part1(banks: Input):
    c = 0
    for bank in banks:
        fd: int = max(bank[:-1])
        sd: int = max(bank[bank.index(fd) + 1 :])
        c += int(f"{fd}{sd}")
    return c


def part2(banks: Input):
    c = 0
    for bank in banks:
        digits: list[int] = []
        prev_index = 0
        for i in range(12):
            subset = bank[prev_index : len(bank) - 12 + i + 1]
            digit = max(subset)
            digits.append(digit)
            prev_index += subset.index(digit) + 1
        value = int("".join(list(map(str, digits))))
        c += value
    return c


assert part1(parse_input("2025/day3/example.txt")) == 357
print("Part 1: ", part1(parse_input("2025/day3/input.txt")))

assert part2(parse_input("2025/day3/example.txt")) == 3121910778619
print("Part 2: ", part2(parse_input("2025/day3/input.txt")))
