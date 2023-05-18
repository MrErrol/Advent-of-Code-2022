from collections import Counter
from typing import Tuple, Iterator

import numpy as np

with open("input.txt", "+r") as file:
    raw_lines = file.read().split("\n")

SIDE_SITES_CYCLE = (
    [(-1, -1), (0, -1), (1, -1)],  # North
    [(-1, 1), (0, 1), (1, 1)],  # South
    [(-1, -1), (-1, 0), (-1, 1)],  # West
    [(1, -1), (1, 0), (1, 1)],  # East
)

DIR_CYCLE = ((0, -1), (0, 1), (-1, 0), (1, 0))


def neighbours(position: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    for dx, dy in ((-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)):
        yield position[0] + dx, position[1] + dy


def elf_new_position(elf: Tuple[int, int], elves: dict, iter: int) -> Tuple[int, int]:
    if not any(neighbour in elves for neighbour in neighbours(elf)):
        return elf  # elf does not move

    for i in range(4):
        ind = (i + iter) % 4
        if not any((elf[0] + dx, elf[1] + dy) in elves for dx, dy in SIDE_SITES_CYCLE[ind]):
            dx, dy = DIR_CYCLE[ind]
            return elf[0] + dx, elf[1] + dy

    return elf


def count_empty_fields(elves: dict) -> int:
    positions = np.array(list(elves.keys()))
    upper_x, upper_y = positions.max(axis=0)
    lower_x, lower_y = positions.min(axis=0)
    return (upper_x - lower_x + 1) * (upper_y - lower_y + 1) - len(positions)


def print_elves(elves: dict):
    screen = [["." for _ in range(14)] for _ in range(14)]
    for elf in elves:
        screen[elf[1]][elf[0]] = "#"
    screen = "\n".join(["".join(row) for row in screen])
    print("\n" * 5)
    print(screen)


init_elves = set()
for y, row in enumerate(raw_lines):
    for x, tile in enumerate(row):
        if tile == "#":
            init_elves.add((x, y))


# Run 10 cycle simulation
elves = {elf: elf for elf in init_elves}
proposed_positions = Counter()
for i in range(10):
    # Finding new positions
    for elf in elves:
        new = elf_new_position(elf=elf, elves=elves, iter=i)
        elves[elf] = new
        proposed_positions.update([new])

    # Moving
    new_elves = {}
    for elf, new in elves.items():
        if proposed_positions[new] > 1:
            new_elves[elf] = elf
        else:
            new_elves[new] = new

    elves = new_elves
    proposed_positions.clear()

solution_1 = count_empty_fields(elves)

print(f"First star solution: {solution_1}")

# Full simulation
elves = {elf: elf for elf in init_elves}
proposed_positions = Counter()
cycles = 0
for cycle in range(0, 10**10):
    all_stay = True
    # Finding new positions
    for elf in elves:
        new = elf_new_position(elf=elf, elves=elves, iter=cycle)
        elves[elf] = new
        proposed_positions.update([new])

    # Moving
    new_elves = {}
    for elf, new in elves.items():
        if elf != new:
            all_stay = False
        if proposed_positions[new] > 1:
            new_elves[elf] = elf
        else:
            new_elves[new] = new

    if all_stay:
        cycles = cycle + 1
        break

    elves = new_elves
    proposed_positions.clear()

print(f"Second star solution: {cycles}")
