# part 1

input = open("./2020/input.txt", "r")

lines = input.readlines()


numbers = [int(line.strip()) for line in lines]

answers = []

for i, n1 in enumerate(numbers):
    for n2 in numbers[i:]:
        if n1 + n2 == 2020:
            answers.append(n1 * n2)
            print(answers)


# part 2
for i, n1 in enumerate(numbers):
    for j, n2 in enumerate(numbers[i:], start=i):
        for n3 in numbers[j:]:
            if n1 + n2 + n3 == 2020:
                answers.append(n1 * n2 * n3)
                print(answers)
