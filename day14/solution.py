from copy import copy


def drop_sand(space: dict, bottom_line: int, drop_point=(500, 0)) -> dict:
    position = drop_point
    while True:
        proposition_1 = (position[0], position[1] + 1)
        proposition_2 = (position[0] - 1, position[1] + 1)
        proposition_3 = (position[0] + 1, position[1] + 1)
        if proposition_1 not in space:
            position = proposition_1
        elif proposition_2 not in space:
            position = proposition_2
        elif proposition_3 not in space:
            position = proposition_3
        else:
            space[position] = "O"
            if position == drop_point:
                raise EOFError("Drop point blocked!")
            break
        if position[1] > bottom_line:
            raise ValueError("Infinite drop!")
    return space


with open("input.txt", "+r") as file:
    raw_lines = file.read().split("\n")

lines = [[[int(position) for position in pair.split(",")] for pair in line.split(" -> ")] for line in raw_lines]

obstacles = dict()

for line in lines:
    for pair1, pair2 in zip(line, line[1:]):
        if pair1[0] == pair2[0]:
            x = pair1[0]
            start, stop = (pair1[1], pair2[1]) if (pair1[1] < pair2[1]) else (pair2[1], pair1[1])
            for y in range(start, stop + 1):
                obstacles[(x, y)] = "#"
        elif pair1[1] == pair2[1]:
            y = pair1[1]
            start, stop = (pair1[0], pair2[0]) if (pair1[0] < pair2[0]) else (pair2[0], pair1[0])
            for x in range(start, stop + 1):
                obstacles[(x, y)] = "#"
        else:
            raise ValueError("line of rocks is not aligned!")

bottom_line = max(key[1] for key in obstacles.keys())

sand_counter = 0
for sand_counter in range(1000000):
    try:
        obstacles = drop_sand(space=obstacles, bottom_line=bottom_line)
    except ValueError:
        break

first_solution = copy(sand_counter)

for x in range(500 - bottom_line - 50, 500 + bottom_line + 50):
    obstacles[(x, bottom_line + 2)] = "#"

for sand_counter in range(1, 1000000):
    try:
        obstacles = drop_sand(space=obstacles, bottom_line=bottom_line + 2)
    except EOFError:
        break


print(f"First star solution: {first_solution}")
print(f"Second star solution: {first_solution + sand_counter}")
