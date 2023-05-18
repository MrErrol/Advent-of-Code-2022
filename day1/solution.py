with open("input.txt", "+r") as file:
    data = file.read().rstrip("\n")

calories = [sum([int(cal) for cal in elf.split("\n")]) for elf in data.split("\n\n")]

print(f"First star solution: {max(calories)}")

calories.sort(reverse=True)

print(f"Second star solution: {sum(calories[:3])}")
