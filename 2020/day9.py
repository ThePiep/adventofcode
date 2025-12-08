# part 9

input = open("2020/input9.txt", "r")

lines = input.readlines()
# print(lines)
data = [int(line.strip()) for line in lines]
print(data)

preamble = 25
invalid = 0

for i in range(preamble, len(data)):
    valid = False
    for j in range(i - preamble, i):
        for k in range(j + 1, i):
            if data[j] + data[k] == data[i]:
                valid = True
                print(data[i], data[j], data[k])
                break
        if valid:
            break
    if not valid:
        print("invalid")
        print(data[i])
        invalid = data[i]
        break

combination = []

for i in range(len(data)):
    count = data[i]
    found = False
    for j in range(i + 1, len(data)):
        count += data[j]
        # print(count)
        if count > invalid:
            break
        elif count == invalid:
            found = True
            combination = data[i : j + 1]
            break
    print(found)
    if found:
        print(combination)
        break

print(min(combination), max(combination))
print(min(combination) + max(combination))
