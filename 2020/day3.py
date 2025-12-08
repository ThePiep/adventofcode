# part 2

input = open("2020/input3.txt", "r")

lines = input.readlines()
data = [line.strip() for line in lines]

width = len(data[0])
count = 0
y = 0

for row in data:
    if row[y] == "#":
        count += 1
    y = (y + 7) % width


def count_trees(skip_x, skip_y):
    count = 0
    x = 0
    for i, row in enumerate(data):
        if ((i) % (skip_y)) == 0:
            if row[x] == "#":
                count += 1
            x = (x + skip_x) % width

    print(count)
    return count


ans = (
    count_trees(1, 1)
    * count_trees(3, 1)
    * count_trees(5, 1)
    * count_trees(7, 1)
    * count_trees(1, 2)
)
print(ans)
