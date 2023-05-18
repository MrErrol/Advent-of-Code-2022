from typing import List, Tuple

with open("input.txt", "+r") as file:
    raw_map, raw_commands = file.read().split("\n\n")

DIRECTIONS = [">", "v", "<", "^"]


def parse_commands(commands: str) -> List:
    parsed = []
    buffer = ""
    for letter in commands:
        if not letter.isdigit():
            if buffer:
                parsed.append(int(buffer))
                buffer = ""
            parsed.append(letter)
        else:
            buffer += letter
    if buffer:
        parsed.append(int(buffer))
    return parsed


def rotate(current_dir: str, rotation_dir: str) -> str:
    if rotation_dir == "R":
        return DIRECTIONS[(DIRECTIONS.index(current_dir) + 1) % 4]
    elif rotation_dir == "L":
        return DIRECTIONS[(DIRECTIONS.index(current_dir) - 1) % 4]
    raise ValueError


def position_ahead(maze, dir, x, y) -> Tuple[int, int, str]:
    if dir == ">":
        newy = y
        newx = (x + 1) % len(maze[0])
        if maze[newy][newx] == " ":
            newx = min([maze[y].index("."), maze[y].index("#")])
    elif dir == "<":
        newy = y
        newx = (x - 1) % len(maze[0])
        if maze[newy][newx] == " ":
            reversed_row = maze[y][::-1]
            newx = len(reversed_row) - 1 - min([reversed_row.index("."), reversed_row.index("#")])
    elif dir == "v":
        newx = x
        newy = (y + 1) % len(maze)
        if maze[newy][newx] == " ":
            col = [row[x] for row in maze]
            newy = min([col.index("."), col.index("#")])
    elif dir == "^":
        newx = x
        newy = (y - 1) % len(maze)
        if maze[newy][newx] == " ":
            reversed_col = [row[x] for row in maze][::-1]
            newy = len(reversed_col) - 1 - min([reversed_col.index("."), reversed_col.index("#")])
    else:
        raise ValueError
    return newx, newy, maze[newy][newx]


def folded_position_ahead(maze, dir, x, y) -> Tuple[int, int, str, str]:
    if dir == ">":
        newy = y
        newx = x + 1
        newdir = ">"
        if newx == len(maze[0]) or maze[newy][newx] == " ":
            if y < 50:
                newx = 99
                newy = 149 - y
                newdir = "<"
            elif 50 <= y < 100:
                newx = 99 + (y - 49)
                newy = 49
                newdir = "^"
            elif 100 <= y < 150:
                newx = 149
                newy = 149 - y
                newdir = "<"
            elif 150 <= y < 200:
                newx = 49 + (y - 149)
                newy = 149
                newdir = "^"

    elif dir == "<":
        newy = y
        newx = x - 1
        newdir = "<"
        if newx < 0 or maze[newy][newx] == " ":
            if 0 <= y < 50:
                newx = 0
                newy = 149 - y
                newdir = ">"
            elif 50 <= y < 100:
                newx = y - 50
                newy = 100
                newdir = "v"
            elif 100 <= y < 150:
                newx = 50
                newy = 149 - y
                newdir = ">"
            elif 150 <= y < 200:
                newx = y - 100
                newy = 0
                newdir = "v"

    elif dir == "v":
        newx = x
        newy = y + 1
        newdir = "v"
        if newy == len(maze) or maze[newy][newx] == " ":
            if 0 <= x < 50:
                newx = 100 + x
                newy = 0
                newdir = "v"
            elif 50 <= x < 100:
                newx = 49
                newy = 150 + (x - 50)
                newdir = "<"
            elif 100 <= x < 150:
                newx = 99
                newy = 50 + (x - 100)
                newdir = "<"

    elif dir == "^":
        newx = x
        newy = y - 1
        newdir = "^"
        if newy < 0 or maze[newy][newx] == " ":
            if 0 <= x < 50:
                newx = 50
                newy = 50 + x
                newdir = ">"
            elif 50 <= x < 100:
                newx = 0
                newy = 100 + x
                newdir = ">"
            elif 100 <= x < 150:
                newx = x - 100
                newy = 199
                newdir = "^"
    else:
        raise ValueError

    return newx, newy, newdir, maze[newy][newx]


# parse input
commands = parse_commands(raw_commands)
maze = [list(row) for row in raw_map.split("\n")]
max_row_len = max(len(row) for row in maze)
maze = [row + [" "] * (max_row_len - len(row)) for row in maze]

# init position
x = maze[0].index(".")
y = 0
dir = ">"

# traverse
for command in commands:
    if isinstance(command, str):
        dir = rotate(dir, rotation_dir=command)
        continue
    for _ in range(command):
        new_x, new_y, tile = position_ahead(maze=maze, dir=dir, x=x, y=y)
        if tile == ".":
            x, y = new_x, new_y
        elif tile == "#":
            break
        else:
            raise ValueError

dir_score = {">": 0, "v": 1, "<": 2, "^": 3}
final_password = 1000 * (y + 1) + 4 * (x + 1) + dir_score[dir]

print(f"First star solution :{final_password}")

# Cube path

# Tests of folding
assert folded_position_ahead(maze, "<", x=50, y=0)[:3] == (0, 149, ">")
assert folded_position_ahead(maze, "<", x=0, y=149)[:3] == (50, 0, ">")
assert folded_position_ahead(maze, "<", x=50, y=49)[:3] == (0, 100, ">")
assert folded_position_ahead(maze, "<", x=0, y=100)[:3] == (50, 49, ">")

assert folded_position_ahead(maze, "<", x=50, y=50)[:3] == (0, 100, "v")
assert folded_position_ahead(maze, "^", x=0, y=100)[:3] == (50, 50, ">")
assert folded_position_ahead(maze, "<", x=50, y=99)[:3] == (49, 100, "v")
assert folded_position_ahead(maze, "^", x=49, y=100)[:3] == (50, 99, ">")

assert folded_position_ahead(maze, "<", x=0, y=150)[:3] == (50, 0, "v")
assert folded_position_ahead(maze, "^", x=50, y=0)[:3] == (0, 150, ">")


assert folded_position_ahead(maze, ">", x=149, y=0)[:3] == (99, 149, "<")
assert folded_position_ahead(maze, ">", x=99, y=149)[:3] == (149, 0, "<")

assert folded_position_ahead(maze, ">", x=99, y=50)[:3] == (100, 49, "^")
assert folded_position_ahead(maze, "v", x=100, y=49)[:3] == (99, 50, "<")

assert folded_position_ahead(maze, ">", x=49, y=150)[:3] == (50, 149, "^")
assert folded_position_ahead(maze, "v", x=50, y=149)[:3] == (49, 150, "<")


assert folded_position_ahead(maze, "v", x=0, y=199)[:3] == (100, 0, "v")
assert folded_position_ahead(maze, "^", x=100, y=0)[:3] == (0, 199, "^")


# init position
x = maze[0].index(".")
y = 0
dir = ">"

# traverse
for command in commands:
    if isinstance(command, str):
        dir = rotate(dir, rotation_dir=command)
        continue
    for _ in range(command):
        new_x, new_y, new_dir, tile = folded_position_ahead(maze=maze, dir=dir, x=x, y=y)
        if tile == ".":
            x, y, dir = new_x, new_y, new_dir
        elif tile == "#":
            break
        else:
            raise ValueError

folded_final_password = 1000 * (y + 1) + 4 * (x + 1) + dir_score[dir]

print(f"Second star solution :{folded_final_password}")
