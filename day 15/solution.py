from copy import copy
from typing import Tuple, List, Optional


# noinspection PyTypeChecker
from tqdm import tqdm


def parse_line(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    def my_filter(letter: str):
        return str.isdigit(letter) or (letter == "-")

    sensor_str, beacon_str = line.split(":")
    sensor_position: Tuple[int, int] = tuple(
        [int("".join(filter(my_filter, string))) for string in sensor_str.split(",")]
    )
    beacon_position: Tuple[int, int] = tuple(
        [int("".join(filter(my_filter, string))) for string in beacon_str.split(",")]
    )
    return sensor_position, beacon_position


def manhattan(x: Tuple[int, int], y: Tuple[int, int]) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def scan_range_at_y(sensor, beacon, y):
    scan_range = manhattan(sensor, beacon)
    remained_range = scan_range - abs(sensor[1] - y)
    if remained_range < 0:
        return None
    return sensor[0] - remained_range, sensor[0] + remained_range


def squeeze_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    ranges.sort()
    if not ranges:
        return []
    new_ranges = [ranges[0]]
    for single_range in ranges[1:]:
        if single_range[0] > new_ranges[-1][1] + 1:
            new_ranges.append(single_range)
        else:
            last_range = copy(new_ranges[-1])
            new_ranges[-1] = (min(last_range[0], single_range[0]), max(last_range[1], single_range[1]))
    return new_ranges


def count_exclusions(ranges: List[Tuple[int, int]], sensor_dict: dict, y: int) -> int:
    full_length = sum([x2 - x1 + 1 for x1, x2 in ranges])
    obstacles_in_line = [sensor[0] for sensor in sensor_dict.keys() if sensor[1] == y] + [
        beacon[0] for beacon in set(sensor_dict.values()) if beacon[1] == y
    ]
    obstacle_in_range = [[line[0] <= obstacle <= line[1] for obstacle in obstacles_in_line] for line in ranges]
    return full_length - sum([sum(collisions) for collisions in obstacle_in_range])


def find_allowed_x(ranges: List[Tuple[int, int]], xmin, xmax) -> Optional[int]:
    lines_of_interest = [line for line in ranges if (line[0] <= xmax) and (xmin <= line[1])]
    if not lines_of_interest:
        return None
    if len(lines_of_interest) > 1:
        return lines_of_interest[0][1] + 1
    elif lines_of_interest[0][0] > xmin:
        return xmin
    elif lines_of_interest[0][1] < xmax:
        return xmax
    else:
        return None


with open("input.txt", "+r") as file:
    raw_lines = file.read().split("\n")

sensors = {sensor: beacon for sensor, beacon in map(parse_line, raw_lines)}

y1 = 2_000_000

ranges_at_given_y = [scan_range_at_y(sensor=sensor, beacon=beacon, y=y1) for sensor, beacon in sensors.items()]
ranges_at_given_y = [line for line in ranges_at_given_y if line is not None]
squeezed_ranges_at_given_y = squeeze_ranges(ranges_at_given_y)
exclusions = count_exclusions(ranges=squeezed_ranges_at_given_y, sensor_dict=sensors, y=y1)

print(f"First star solution: {exclusions}")

min_pos = 0
max_pos = 4_000_000

tuning_frequency = None

for y in tqdm(range(max_pos + 1)):
    ranges_at_given_y = [scan_range_at_y(sensor=sensor, beacon=beacon, y=y) for sensor, beacon in sensors.items()]
    ranges_at_given_y = [line for line in ranges_at_given_y if line is not None]
    squeezed_ranges_at_given_y = squeeze_ranges(ranges_at_given_y)
    option = find_allowed_x(xmin=min_pos, xmax=max_pos, ranges=squeezed_ranges_at_given_y)
    if option is not None:
        x_sol = option
        y_sol = y
        tuning_frequency = 4_000_000 * x_sol + y_sol
        break

print(f"Second star solution: {tuning_frequency}")

assert 1
