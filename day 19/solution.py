from typing import Tuple, List

import numpy as np

with open("input.txt", "+r") as file:
    lines = file.read().split("\n")


class Resources:
    def __init__(self, ore: int, clay: int, obsidian: int, geode: int):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def __add__(self, other):
        return Resources(
            ore=self.ore + other.ore,
            clay=self.clay + other.clay,
            obsidian=self.obsidian + other.obsidian,
            geode=self.geode + other.geode,
        )

    def __sub__(self, other):
        return Resources(
            ore=self.ore - other.ore,
            clay=self.clay - other.clay,
            obsidian=self.obsidian - other.obsidian,
            geode=self.geode - other.geode,
        )

    def __le__(self, other):
        return (
            (self.ore <= other.ore)
            and (self.clay <= other.clay)
            and (self.obsidian <= other.obsidian)
            and (self.geode <= other.geode)
        )

    def __eq__(self, other):
        return (
            (self.ore == other.ore)
            and (self.clay == other.clay)
            and (self.obsidian == other.obsidian)
            and (self.geode == other.geode)
        )

    def __mul__(self, other: int):
        return Resources(
            ore=self.ore * other,
            clay=self.clay * other,
            obsidian=self.obsidian * other,
            geode=self.geode * other,
        )

    def as_list(self):
        return [self.ore, self.clay, self.obsidian, self.geode]


class Blueprint:
    def __init__(
        self, blue_id: int, ore_cost: int, clay_cost: int, obsidian_cost: Tuple[int, int], geode_cost: Tuple[int, int]
    ):
        self.blue_id = blue_id
        self.ore_cost = Resources(ore_cost, 0, 0, 0)
        self.clay_cost = Resources(clay_cost, 0, 0, 0)
        self.obsidian_cost = Resources(obsidian_cost[0], obsidian_cost[1], 0, 0)
        self.geode_cost = Resources(geode_cost[0], 0, geode_cost[1], 0)
        self.max_cost_ore = max([self.ore_cost.ore, self.clay_cost.ore, self.obsidian_cost.ore, self.geode_cost.ore])

    def get_cost(self, robot: Resources):
        if robot.ore:
            return self.ore_cost
        elif robot.clay:
            return self.clay_cost
        elif robot.obsidian:
            return self.obsidian_cost
        elif robot.geode:
            return self.geode_cost
        raise ValueError("wrong robot provided")

    @property
    def costs(self):
        return (
            (Resources(1, 0, 0, 0), self.ore_cost),
            (Resources(0, 1, 0, 0), self.clay_cost),
            (Resources(0, 0, 1, 0), self.obsidian_cost),
            (Resources(0, 0, 0, 1), self.geode_cost),
        )


def line_to_blueprint(line) -> Blueprint:
    numbers = [int(word) for word in line.replace(":", "").split(" ") if str.isdigit(word[0])]
    assert len(numbers) == 7
    return Blueprint(
        blue_id=numbers[0],
        ore_cost=numbers[1],
        clay_cost=numbers[2],
        obsidian_cost=(numbers[3], numbers[4]),
        geode_cost=(numbers[5], numbers[6]),
    )


class GameState:
    def __init__(self, time: int, ore: Resources, robots: Resources):
        self.time = time
        self.ore = ore
        self.robots = robots

    def __str__(self) -> str:
        return (
            f"Ore({self.ore.ore},{self.ore.clay},{self.ore.obsidian},{self.ore.geode}) "
            f"Robots({self.robots.ore},{self.robots.clay},{self.robots.obsidian},{self.robots.geode})"
        )


def useful_time(robot: Resources) -> int:
    if robot.ore:
        return 7
    if robot.clay:
        return 5
    if robot.obsidian:
        return 3
    if robot.geode:
        return 1
    raise ValueError


def can_produce(state: GameState, robot: Resources) -> bool:
    fail1 = robot.obsidian and not state.robots.clay
    fail2 = robot.geode and not state.robots.obsidian
    return not (fail1 or fail2)


def time_to_produce(state: GameState, cost: Resources) -> int:
    if cost <= state.ore:
        return 1
    turns_to_wait = max(
        [
            np.ceil((ore_cost - reserve) / speed)
            for ore_cost, reserve, speed in zip(cost.as_list(), state.ore.as_list(), state.robots.as_list())
            if ore_cost > 0
        ]
    )
    return turns_to_wait + 1


def minimal_time_to_earn_resources_no_robots(needed: int) -> int:
    if needed == 0:
        return 0
    elif needed == 1:
        return 1
    elif needed <= 3:
        return 2
    elif needed <= 6:
        return 3
    elif needed <= 10:
        return 4
    elif needed <= 15:
        return 5
    elif needed <= 21:
        return 6
    ValueError("can be expanded")


def minimal_time_to_get_first_robot(robot: Resources, blue: Blueprint) -> int:
    if robot.geode:
        return 1
    if robot.obsidian:
        return 2 + minimal_time_to_earn_resources_no_robots(blue.get_cost(robot).obsidian)
    if robot.clay:
        return (
            3
            + minimal_time_to_earn_resources_no_robots(blue.get_cost(Resources(0, 0, 0, 1)).obsidian)
            + minimal_time_to_earn_resources_no_robots(blue.get_cost(Resources(0, 0, 1, 0)).clay)
        )
    return 0


def will_surely_fail(state: GameState, blue: Blueprint) -> int:
    if state.robots.ore > blue.max_cost_ore:
        return True
    if state.robots.clay > blue.obsidian_cost.clay:
        return True
    if state.robots.obsidian > blue.geode_cost.obsidian:
        return True
    if state.time > 12:
        return False
    if state.robots.clay == 0:
        if state.time < minimal_time_to_get_first_robot(robot=Resources(0, 1, 0, 0), blue=blue):
            return True
    if state.robots.obsidian == 0:
        if state.time < minimal_time_to_get_first_robot(robot=Resources(0, 0, 1, 0), blue=blue):
            return True
    if state.robots.geode == 0:
        if state.time < minimal_time_to_get_first_robot(robot=Resources(0, 0, 0, 1), blue=blue):
            return True
    return False


def score_blueprint(blue: Blueprint, game_state: GameState) -> int:
    incomplete_states: List[GameState] = [game_state]
    best_solution_yet = 0
    while incomplete_states:
        new_states = []
        for state in incomplete_states:
            options = []
            for robot, robot_cost in blue.costs:
                if not can_produce(state, robot):
                    continue
                ttp = time_to_produce(state=state, cost=robot_cost)
                if state.time - ttp < useful_time(robot):
                    continue
                options.append(
                    GameState(
                        time=state.time - ttp,
                        ore=state.ore + state.robots * ttp - robot_cost,
                        robots=state.robots + robot,
                    )
                )
            new_states += options
            if not options and state.robots.geode:
                score = state.ore.geode + state.time * state.robots.geode
                best_solution_yet = max([score, best_solution_yet])
        incomplete_states = [state for state in new_states if not will_surely_fail(state=state, blue=blue)]
    return best_solution_yet


blueprints = [line_to_blueprint(line) for line in lines]

best_geodes = [
    score_blueprint(blue=blue, game_state=GameState(time=24, ore=Resources(0, 0, 0, 0), robots=Resources(1, 0, 0, 0)))
    for blue in blueprints
]

total = sum([score * blue.blue_id for score, blue in zip(best_geodes, blueprints)])

print(f"First star solution: {total}")

# Second star takes around 150 seconds

best_geodes = [
    score_blueprint(blue=blue, game_state=GameState(time=32, ore=Resources(0, 0, 0, 0), robots=Resources(1, 0, 0, 0)))
    for blue in blueprints[:3]
]

final_score = best_geodes[0] * best_geodes[1] * best_geodes[2]

print(f"Second star solution: {final_score}")
