from typing import Tuple

import numpy as np


def move_head(head_position: Tuple[int, int], direction: str) -> Tuple[int, int]:
    head_x, head_y = head_position
    if direction == "R":
        head_x += 1
    elif direction == "L":
        head_x -= 1
    elif direction == "U":
        head_y += 1
    elif direction == "D":
        head_y -= 1
    else:
        assert False  # something went wrong
    return head_x, head_y


def move_tail(head_position: Tuple[int, int], tail_position: Tuple[int, int]) -> Tuple[int, int]:
    head_x, head_y = head_position
    tail_x, tail_y = tail_position
    if abs(head_x - tail_x) > 1 or abs(head_y - tail_y) > 1:
        tail_x = tail_x + np.sign(head_x - tail_x)
        tail_y = tail_y + np.sign(head_y - tail_y)
    return tail_x, tail_y


with open("input.txt", "+r") as file:
    raw_input = file.read().split("\n")

commands = [(command.split(" ")[0], int(command.split(" ")[1])) for command in raw_input]

head_position = (0, 0)
tail_position = (0, 0)
tail_positions = set()
for direction, steps in commands:
    for step in range(steps):
        head_position = move_head(head_position=head_position, direction=direction)
        tail_position = move_tail(head_position=head_position, tail_position=tail_position)
        tail_positions.add(tuple(tail_position))

print(f"First star solution: {len(tail_positions)}")

rope_positions = [(0, 0)] * 10
long_tail_positions = set()
for direction, steps in commands:
    for step in range(steps):
        rope_positions[0] = move_head(head_position=rope_positions[0], direction=direction)
        for segment_index, segment in enumerate(rope_positions[1:], start=1):
            rope_positions[segment_index] = move_tail(
                head_position=rope_positions[segment_index - 1], tail_position=segment
            )
        long_tail_positions.add(rope_positions[-1])

print(f"Second star solution: {len(long_tail_positions)}")
