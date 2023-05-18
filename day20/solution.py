from collections import deque
from copy import copy

with open("input.txt", "+r") as file:
    raw_lines = file.read().split("\n")

all_lines = [int(line) for line in raw_lines]
numbered_lines = [(ind, number) for ind, number in enumerate(all_lines)]

def mix(original_lines: deque, to_mix: deque) -> deque:
    N = len(original_lines)
    for pair in original_lines:
        position = to_mix.index(pair)
        to_mix.remove(pair)
        new_position = (position + pair[1]) % (N - 1)
        # weird boundary rules
        if new_position == 0 and pair[1] < 0:
            new_position = N
        if new_position == N - 1 and pair[1] > 0:
            new_position = 0
        # finally insert element
        to_mix.insert(new_position, pair)
    return to_mix


def get_score(mixed: deque) -> int:
    zero_position = [val for _, val in mixed].index(0)
    size = len(mixed)
    return sum([mixed[(zero_position + ind) % size][1] for ind in [1000, 2000, 3000]])

original = deque(numbered_lines)
to_mix = deque(numbered_lines)
mixed = mix(original_lines=original, to_mix=to_mix)
solution_1 = get_score(mixed)

print(f"First star solution: {solution_1}")

key = 811589153
long_lines = deque([(ind, val * key) for ind, val in numbered_lines])
long_to_mix = copy(long_lines)

for _ in range(10):
    long_to_mix = mix(original_lines=long_lines, to_mix=long_to_mix)

solution_2 = get_score(long_to_mix)

print(f"Second star solution: {solution_2}")
