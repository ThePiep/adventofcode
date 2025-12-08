# part 1

input = open("2020/input2.txt", "r")

lines = input.readlines()

data = [line.strip().split() for line in lines]

count = 0

for d in data:
    l, h = [int(i) for i in d[0].split("-")]
    char = d[1][0]
    string = d[2]
    occ = string.count(char)
    if occ >= l and occ <= h:
        count += 1

print(count)


# part 2

count = 0

for d in data:
    p1, p2 = [int(i) - 1 for i in d[0].split("-")]
    char = d[1][0]
    string = d[2]
    s1 = char == string[p1]
    s2 = char == string[p2]
    if bool(s1) ^ bool(s2):
        count += 1


print(count)
