import itertools


def priority(char: str) -> int:
    return ord(char) - 96 if char.islower() else ord(char) - 64 + 26


with open("input.txt", "+r") as file:
    raw_input = file.readlines()

rucksacks = [pack.rstrip("\n") for pack in raw_input]

items_duplicated = itertools.chain.from_iterable(
    [set(pack[: len(pack) // 2]).intersection(set(pack[len(pack) // 2 :])) for pack in rucksacks]
)

priorities = [priority(char) for char in items_duplicated]

print(f"First star solution: {sum(priorities)}")

# Second star
badges = [
    set(rucksacks[3 * i]).intersection(set(rucksacks[3 * i + 1])).intersection(set(rucksacks[3 * i + 2]))
    for i in range(len(rucksacks) // 3)
]

second_solution = sum([priority(char) for char in itertools.chain.from_iterable(badges)])

print(f"Second star solution: {second_solution}")
