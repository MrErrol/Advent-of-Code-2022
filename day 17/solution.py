from typing import Tuple

import numpy as np

with open("input.txt", "+r") as file:
    wind_cycle = file.read()

map_width = 7

shapes = [
    np.array([[1, 1, 1, 1]]),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
    np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]]),  # - reversed due to inverted coordinate system
    np.array([[1], [1], [1], [1]]),
    np.array([[1, 1], [1, 1]]),
]


def get_highest_empty_level(map: np.ndarray, previous: int) -> int:
    map_overpart = map[previous:previous+4]
    if map_overpart.sum().sum() == 0:
        return previous
    return previous + 4 - map_overpart.sum(axis=1)[::-1].astype(bool).argmax()


def is_wall_collision(shape: np.ndarray, block_x: int, direction: str) -> bool:
    if direction == ">":
        return shape.shape[1] + block_x == map_width
    elif direction == "<":
        return block_x == 0
    else:
        raise ValueError("wrong direction provided")


def is_tower_collision(shape: np.ndarray, block_x: int, block_y: int, map: np.ndarray) -> bool:
    if block_y < 0:
        # ground collision
        return True
    for y_shape, row in enumerate(shape):
        for x_shape, filled in enumerate(row):
            if filled and map[block_y + y_shape][block_x + x_shape]:
                return True  # collision!
    return False


def put_block_on_map(shape: np.ndarray, block_x: int, block_y: int, map: np.ndarray) -> np.ndarray:
    for y_shape, row in enumerate(shape):
        for x_shape, filled in enumerate(row):
            if filled:
                map[block_y + y_shape][block_x + x_shape] = 1
    return map

def find_period_and_gains(states) -> Tuple[int, int, int]:
    simple_state_reversed = [(block, app) for _, block, app, _ in states[::-1]]
    state = simple_state_reversed[0]
    simple_state_reversed = simple_state_reversed[1 :]
    period = simple_state_reversed.index(state) + 1
    assert simple_state_reversed[2 * period] == simple_state_reversed[period]
    gain_on_period = states[-1][3] - states[-1 - period][3]
    blocks_on_period = states[-1][0] - states[-1 - period][0]
    return period, gain_on_period, blocks_on_period


def run_simulation(rocks_to_drop):
    end_of_wind_states = []
    map = np.zeros((rocks_to_drop * 20, map_width))
    solution = -1
    current_block = 0
    highest_empty_level = 0
    block_x = 2
    block_y = 3
    time_from_appearance = 0
    for time in range(rocks_to_drop * 100):
        if not time % len(wind_cycle):
            end_of_wind_states.append((current_block, current_block % len(shapes), time_from_appearance, highest_empty_level))
        block = shapes[current_block % len(shapes)]
        time_from_appearance += 1
        # push block
        direction = wind_cycle[time % len(wind_cycle)]
        new_x = block_x
        if not is_wall_collision(shape=block, block_x=block_x, direction=direction):
            new_x = block_x + 1 if direction == ">" else block_x - 1
        if not is_tower_collision(shape=block, block_x=new_x, block_y=block_y, map=map):
            block_x = new_x
        # try to drop a block
        if is_tower_collision(shape=block, block_x=block_x, block_y=block_y - 1, map=map):
            map = put_block_on_map(shape=block, block_x=block_x, block_y=block_y, map=map)
            highest_empty_level = get_highest_empty_level(map, previous=highest_empty_level)
            current_block += 1
            block_y = highest_empty_level + 3
            block_x = 2
            time_from_appearance = 0
            if current_block == rocks_to_drop:
                solution = highest_empty_level
                break
            continue
        block_y -= 1

    return solution, end_of_wind_states

solution_1, _ = run_simulation(rocks_to_drop=2022)

print(f"First star solution: {solution_1}")

all_rocks = 1_000_000_000_000

# initial run for guessed amount of rocks to find periodicity
_, end_of_wind_states = run_simulation(rocks_to_drop=10000)
_, height_gain, blocks_gain = find_period_and_gains(end_of_wind_states)

# proper two stage calculation of part 2
blocks_to_simulate = all_rocks % blocks_gain  + 2 * blocks_gain  # additional periods to get rid of initial condition
height_1, _ = run_simulation(rocks_to_drop=blocks_to_simulate)
height_2 = (all_rocks - blocks_to_simulate) * height_gain // blocks_gain
solution_2 = height_1 + height_2

print(f"Second star solution: {solution_2}")
