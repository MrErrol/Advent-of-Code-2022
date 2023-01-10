from typing import List, Sequence


def parse_commands(commands: Sequence[str]) -> List[int]:
    X = 1
    historical_values = [X]
    for command in commands:
        if command[:4] == "noop":
            pass
        elif command[:4] == "addx":
            historical_values.append(X)
            X += int(command.split(" ")[-1])
        else:
            assert False, "parsing error"
        historical_values.append(X)
    return historical_values


def get_signal_strength(values: List[int]) -> int:
    return sum(values[i - 1] * i for i in range(20, 221, 40))


def render_image(values: List[int]) -> List[List[str]]:
    image = ""
    for row in range(6):
        displayed_row = ""
        for horizontal_position in range(40):
            register_index = 40 * row + horizontal_position
            register_value = values[register_index]
            displayed_row += "#" if abs(register_value - horizontal_position) < 2 else "."
        image += f"{displayed_row}\n"
    return image


with open("input.txt", "+r") as file:
    command_lines = file.read().split("\n")

register_values = parse_commands(command_lines)
solution_1 = get_signal_strength(register_values)

print(f"First star solution: {solution_1}")

rendered_image = render_image(register_values)

print(f"Rendered image: \n{rendered_image}")
