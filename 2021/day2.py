# part 2

input = open("2021/input2.txt", "r")


lines = [line.strip() for line in input.readlines()]


depth = 0
hor = 0
aim = 0

for line in lines:
    if line[0] == "f":
        hor += int(line[len(line) - 1])
        depth += aim * int(line[len(line) - 1])
    elif line[0] == "d":
        aim += int(line[len(line) - 1])
    elif line[0] == "u":
        aim -= int(line[len(line) - 1])

print(depth, hor)
print(depth * hor)
