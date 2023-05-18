from collections import defaultdict
from typing import List, Dict, Set

from dataclasses import dataclass

DIRECTIONS = {"<", ">", "^", "v"}


@dataclass(frozen=True)
class Position:
    x: int
    y: int


class Blizzard:
    def __init__(self, position: Position, dir: str):
        self.position: Position = position
        assert dir in DIRECTIONS
        self.raw_dir: str = dir


class Valley:
    def __init__(self, raw_map: List[str]):
        self.height = len(raw_map) - 2  # y dimension
        self.width = len(raw_map[0]) - 2  # x dimension
        self._blizzards = []
        self.iteration: int = 0
        for y, row in enumerate(raw_map, start=-1):
            for x, field in enumerate(row, start=-1):
                if field not in DIRECTIONS:
                    continue
                self._blizzards.append(Blizzard(position=Position(x=x, y=y), dir=field))
        self._map: Dict[Position, List[Blizzard]] = defaultdict(lambda: [])
        self._update_map()

    def _update_map(self):
        self._map = defaultdict(lambda: [])
        for blizzard in self._blizzards:
            self._map[blizzard.position].append(blizzard)

    def _move_blizzard(self, blizzard: Blizzard) -> Blizzard:
        if blizzard.raw_dir == ">":
            x = (blizzard.position.x + 1) % self.width
            y = blizzard.position.y
        elif blizzard.raw_dir == "<":
            x = (blizzard.position.x - 1) % self.width
            y = blizzard.position.y
        elif blizzard.raw_dir == "^":
            x = blizzard.position.x
            y = (blizzard.position.y - 1) % self.height
        elif blizzard.raw_dir == "v":
            x = blizzard.position.x
            y = (blizzard.position.y + 1) % self.height
        else:
            raise ValueError
        return Blizzard(position=Position(x=x, y=y), dir=blizzard.raw_dir)

    def move_blizzards(self):
        self._blizzards = [self._move_blizzard(blizzard) for blizzard in self._blizzards]
        self._update_map()
        self.iteration += 1

    def is_there_a_blizzard(self, position: Position) -> bool:
        return bool(self._map[position])

    def blizzards(self):
        for blizzard in self._blizzards:
            yield blizzard


class PathSeeker:
    def __init__(self, valley: Valley, start: Position, destination: Position):
        self.valley: Valley = valley
        self.start: Position = start
        self.destination: Position = destination
        self.positions: Set[Position] = {self.start}

    def _get_side_positions(self, position: Position) -> List[Position]:
        options = [
            Position(x=position.x, y=position.y),  # we can stay in place
            Position(x=position.x + 1, y=position.y),
            Position(x=position.x - 1, y=position.y),
            Position(x=position.x, y=position.y + 1),
            Position(x=position.x, y=position.y - 1),
        ]
        valid_options = [pos for pos in options if 0 <= pos.x < self.valley.width and 0 <= pos.y < self.valley.height]
        # 2 special cases outside of valley
        valid_options += [pos for pos in options if pos == self.start or pos == self.destination]
        return valid_options

    def make_search_step(self):
        self.valley.move_blizzards()
        new_positions = set()
        for position in self.positions:
            for option in self._get_side_positions(position):
                if self.valley.is_there_a_blizzard(option):
                    continue
                new_positions.add(option)
        self.positions = new_positions

    def destination_found(self) -> bool:
        return self.destination in self.positions

    def view_current_map(self) -> str:
        map = [["." for _ in range(self.valley.width)] for _ in range(self.valley.height)]
        for blizzard in self.valley.blizzards():
            state = map[blizzard.position.y][blizzard.position.x]
            if state == ".":
                map[blizzard.position.y][blizzard.position.x] = blizzard.raw_dir
            elif state in DIRECTIONS:
                map[blizzard.position.y][blizzard.position.x] = 2
            else:
                map[blizzard.position.y][blizzard.position.x] += 1

        map = [["#"] + [str(field) for field in row] + ["#"] for row in map]
        map = [["#" for _ in range(self.valley.width + 2)]] + map + [["#" for _ in range(self.valley.width + 2)]]
        map[0][self.start.x + 1] = "."
        map[-1][self.destination.x + 1] = "."
        for option in self.positions:
            if map[option.y + 1][option.x + 1] != ".":
                raise ValueError("Frozen!")
            map[option.y + 1][option.x + 1] = "@"
        map = "".join(["".join(row) + "\n" for row in map])
        return map

    def solve(self) -> int:
        while True:
            self.make_search_step()
            if self.destination_found():
                break
            if not self.valley.iteration % 50:
                print(f"Current search iteration: {self.valley.iteration}")
        return self.valley.iteration


if __name__ == "__main__":
    with open("input.txt", "+r") as file:
        raw_map = file.read().split("\n")

    start = Position(y=-1, x=raw_map[0].index(".") - 1)
    destination = Position(y=len(raw_map) - 2, x=raw_map[-1].index(".") - 1)

    valley = Valley(raw_map=raw_map)

    seeker = PathSeeker(valley=valley, start=start, destination=destination)
    there = seeker.solve()
    seeker = PathSeeker(valley=seeker.valley, start=destination, destination=start)
    back = seeker.solve()
    seeker = PathSeeker(valley=valley, start=start, destination=destination)
    there_again = seeker.solve()

    print(f"First star solution: {there}")
    print(f"Second star solution: {there_again}")
