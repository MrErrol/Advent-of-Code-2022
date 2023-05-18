from typing import Tuple, Set, List


def generate_new_positions(position: Tuple[int, int], x_lim: int, y_lim: int) -> Set[Tuple[int, int]]:
    x, y = position
    proposed_positions = set()
    if x > 0:
        proposed_positions.add((x - 1, y))
    if x < x_lim - 1:
        proposed_positions.add((x + 1, y))
    if y > 0:
        proposed_positions.add((x, y - 1))
    if y < y_lim - 1:
        proposed_positions.add((x, y + 1))
    return proposed_positions


def find_distance_to_an_end(
    heightmap: List[List[int]],
    start_position: Tuple[int, int],
    end_position: Tuple[int, int],
    map_width: int,
    map_height: int,
) -> int:
    visited = [[0 for _ in row] for row in heightmap]
    start_x, start_y = start_position
    visited[start_y][start_x] = 1
    positions = [start_position]
    steps = 0
    finished = False
    while not finished:
        steps += 1
        new_positions = set()
        for x, y in positions:
            current_elevation = elevation[y][x]
            for new_x, new_y in generate_new_positions(position=(x, y), x_lim=map_width, y_lim=map_height):
                if visited[new_y][new_x]:
                    continue
                if elevation[new_y][new_x] > current_elevation + 1:
                    continue
                if (new_x, new_y) == end_position:
                    finished = True
                    break
                visited[new_y][new_x] = 1
                new_positions.add((new_x, new_y))
        positions = new_positions

    return steps


def find_distance_to_bottom(
    heightmap: List[List[int]],
    start_position: Tuple[int, int],
    map_width: int,
    map_height: int,
) -> int:
    visited = [[0 for _ in row] for row in heightmap]
    start_x, start_y = start_position
    visited[start_y][start_x] = 1
    positions = [start_position]
    steps = 0
    finished = False
    while not finished:
        steps += 1
        new_positions = set()
        for x, y in positions:
            current_elevation = elevation[y][x]
            for new_x, new_y in generate_new_positions(position=(x, y), x_lim=map_width, y_lim=map_height):
                if visited[new_y][new_x]:
                    continue
                new_elevation = elevation[new_y][new_x]
                if new_elevation < current_elevation - 1:
                    continue
                if new_elevation == ord("a"):
                    finished = True
                    break
                visited[new_y][new_x] = 1
                new_positions.add((new_x, new_y))
        positions = new_positions

    return steps


with open("input.txt") as file:
    raw_file = file.read()

start_elevation = ord("a")
end_elevation = ord("z")

elevation = [[ord(letter) for letter in row] for row in raw_file.split("\n")]
start_y = [ord("S") in row for row in elevation].index(True)
start_x = elevation[start_y].index(ord("S"))
end_y = [ord("E") in row for row in elevation].index(True)
end_x = elevation[end_y].index(ord("E"))
elevation[start_y][start_x] = start_elevation
elevation[end_y][end_x] = end_elevation

heightmap_height = len(elevation)
heightmap_width = len(elevation[0])
start_position = (start_x, start_y)

steps = find_distance_to_an_end(
    heightmap=elevation,
    start_position=start_position,
    end_position=(end_x, end_y),
    map_width=heightmap_width,
    map_height=heightmap_height,
)

print(f"First star solution: {steps}")

shortest_path = find_distance_to_bottom(
    heightmap=elevation, start_position=(end_x, end_y), map_width=heightmap_width, map_height=heightmap_height
)

print(f"Second star solution: {shortest_path}")
