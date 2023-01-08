from typing import Tuple


def get_command_from_line(line: str) -> Tuple[int, int, int]:
    words = line.split(" ")
    return (int(words[1]), int(words[3]), int(words[5]))


with open("input.txt", "+r") as file:
    raw_riddle = [line.rstrip("\n") for line in file.readlines()]

separator_position = raw_riddle.index("")

# Read stack
raw_stack = raw_riddle[:separator_position]
stack_max_len = max(len(line) for line in raw_stack)
raw_stack = [line.ljust(stack_max_len, " ") for line in raw_stack]
vertical_stack = [[line[4 * i + 1] for i in range(len(raw_stack[0]) // 4 + 1)] for line in raw_stack]
horizontal_stack = list(zip(*vertical_stack))
stack = {int(line[-1]): line[-2::-1] for line in horizontal_stack}
stack = {key: list(filter(lambda x: x != " ", value)) for key, value in stack.items()}
stack_copy = {key: value[:] for key, value in stack.items()}

# Read commands
raw_commands = raw_riddle[separator_position + 1 :]
move_commands = [get_command_from_line(line) for line in raw_commands]

# Modify stack
for (count, from_index, to_index) in move_commands:
    for _ in range(count):
        assert len(stack[from_index])
        stack[to_index].append(stack[from_index].pop(-1))

top_crates = "".join([stack[key + 1][-1] for key in range(len(stack))])

print(f"First star solution: {top_crates}")

stack, stack_copy = stack_copy, stack
# Modify stack for second star
for (count, from_index, to_index) in move_commands:
    stack[to_index] += stack[from_index][-count:]
    del stack[from_index][-count:]

top_crates_2 = "".join([stack[key + 1][-1] for key in range(len(stack))])

print(f"Second star solution: {top_crates_2}")
