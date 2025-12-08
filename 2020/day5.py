# part 5

input = open("2020/input5.txt", "r")

lines = input.readlines()
data = [line.strip() for line in lines]
print(data)
max_id = 0
id_list = []


for l in data:
    line = list(l)
    # print(line)
    for i in range(len(line)):
        if line[i] == "B" or line[i] == "R":
            line[i] = 1
        else:
            line[i] = 0
    print(line)
    row = (
        (line[6] * (2**0))
        + (line[5] * (2**1))
        + (line[4] * (2**2))
        + (line[3] * (2**3))
        + (line[2] * (2**4))
        + (line[1] * (2**5))
        + (line[0] * (2**6))
    )
    column = (line[9] * (2**0)) + (line[8] * (2**1)) + (line[7] * (2**2))
    print(row, column)
    id = row * 8 + column
    print(id)
    if id > max_id:
        max_id = id
    id_list.append(id)

id_list.sort()
for i in range(len(id_list)):
    if id_list[i] != (id_list[i + 1] - 1):
        print(id_list[i], id_list[i + 1])
        print(id_list[i] + 1)
