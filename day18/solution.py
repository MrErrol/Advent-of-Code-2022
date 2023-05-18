from typing import Tuple, List, Set


with open("input.txt", "+r") as file:
    lines = file.read().split("\n")

lava = {tuple([int(num) for num in line.split(",")]) for line in lines}


def get_sides_neighbours(point: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    x, y, z = point
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def air_trapped(
    lava: Set[Tuple[int, int, int]],
    air: Tuple[int, int, int],
    limit: int,
    known_free=Set[Tuple[int, int, int]],
    known_trapped=Set[Tuple[int, int, int]],
) -> Tuple[Set[Tuple[int, int, int]], bool]:
    if air in known_free:
        return {air}, False
    if air in known_trapped:
        return {air}, True
    connected_air = {air}
    new_air = {air}
    while len(connected_air) < limit:
        discovered_air = set()
        for point in new_air:
            for neighbour in get_sides_neighbours(point):
                if neighbour in lava or neighbour in connected_air:
                    continue
                discovered_air.add(neighbour)
                connected_air.add(neighbour)
                if neighbour in known_free:
                    return discovered_air, False
                if neighbour in known_trapped:
                    return discovered_air, True
        new_air = discovered_air
        if not discovered_air:
            return connected_air, True
    return connected_air, False


free_sides = 0
for point in lava:
    for neighbour in get_sides_neighbours(point):
        if neighbour not in lava:
            free_sides += 1

print(f"First star solution {free_sides}")

estimate_of_max_volume_trapped = int((len(lines) // 6) ** (3 / 2))

really_free_sides = 0
free_air = set()
trapped_air = set()
for point in lava:
    for neighbour in get_sides_neighbours(point):
        if neighbour not in lava:
            discovered_air, trapped = air_trapped(
                lava=lava,
                air=neighbour,
                limit=estimate_of_max_volume_trapped * 2,
                known_free=free_air,
                known_trapped=trapped_air,
            )
            if trapped:
                trapped_air.update(discovered_air)
            else:
                free_air.update(discovered_air)
                really_free_sides += 1


print(f"Second star solution {really_free_sides}")

assert 1
