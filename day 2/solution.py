with open("input.txt", "+r") as file:
    raw_input = file.readlines()

data = [s.rstrip("\n").replace(" ", "") for s in raw_input]
# rock = 0, paper = 1, scissors = 2
elf_mapping = {"A": 0, "B": 1, "C": 2}
my_mapping = {"X": 0, "Y": 1, "Z": 2}
pairs = [(elf_mapping[s[0]], my_mapping[s[1]]) for s in data]
score = (
    sum([pair[1] + 1 for pair in pairs]) + 3 * len(pairs) + 3 * sum([(pair[1] - pair[0] + 1) % 3 - 1 for pair in pairs])
)

print(f"First star solution: {score}")

# Second star
my_mapping = {"X": -1, "Y": 0, "Z": 1}
new_pairs = [(elf_mapping[s[0]], my_mapping[s[1]]) for s in data]
# new_pairs = new_pairs[:1]
true_score = (
    sum([(pair[0] + pair[1]) % 3 + 1 for pair in new_pairs])
    + 3 * len(new_pairs)
    + 3 * sum([pair[1] for pair in new_pairs])
)

print(f"Second star solution: {true_score}")
