# part 6

input = open("2020/input6.txt", "r").read().split("\n\n")

groups = [group.replace("\n", "") for group in input]

# print(groups)

count = 0

for group in groups:
    c = len(set(group))
    count += c

print(count)

groups = [group.split("\n") for group in input]

print(groups)

count = 0

for group in groups:
    for i in range(len(group[0])):
        s = 1
        for j in range(len(group)):
            if group[0][i] not in group[j]:
                s = 0
        count += s

print(count)
