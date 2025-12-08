# part 10

input = open("2020/einput10.txt", "r")

lines = input.readlines()
data = [line.strip() for line in lines]
print(data)

data_prev = data

width = len(data[0])
height = len(data)


def number_of_adjecent(x, y):
    return len(
        list(
            filter(
                lambda pos: is_occupied(x + pos[0], y + pos[1]),
                [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i or j],
            )
        )
    )


def is_occupied(x, y):
    if x < -1 or x >= height or y < 0 or y >= width:
        return False
    elif data_prev[x][y] == "#":
        return True
    else:
        return False


def print_data():
    for line in data:
        print(line)


def count_occupied():
    count = 0
    for line in data:
        count += line.count("#")
    return count


for k in range(5):
    data_prev = data.copy()
    for i in range(height):
        for j in range(width):
            # print(number_of_adjecent(i, j))
            if data_prev[i][j] == "L" and number_of_adjecent(i, j) == 0:
                # print('la')
                data[i] = data[i][:j] + "#" + data[i][j + 1 :]
            elif data_prev[i][j] == "#" and number_of_adjecent(i, j) > 3:
                data[i] = data[i][:j] + "L" + data[i][j + 1 :]
    print("-----")
    # print(data_prev)
    print_data()
    print(count_occupied())
