# part 1

input = open("2021/input1.txt", "r")

lines = input.readlines()

data = [int(line.strip()) for line in lines]

count = 0

prev = data[0]

for i in range(3, len(data)):
    if data[i] > data[i - 3]:
        count += 1

print(count)
