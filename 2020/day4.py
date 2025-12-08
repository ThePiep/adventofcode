# part 4

input = open("2020/input4.txt", "r")

lines = input.readlines()

documents = []
document = ""

valid_count = 0

for line in lines:
    if line == "\n":
        documents.append(document)
        print(document)
        document = ""
    else:
        document += " " + line.strip() + " "
documents.append(document)


for doc in documents:
    if all(
        [
            ident in doc
            for ident in ["byr:", "iyr:", "eyr:", "hgt:", "hcl:", "ecl:", "pid:"]
        ]
    ):
        valid_count += 1
        print(doc)

print(documents)

print(valid_count)
