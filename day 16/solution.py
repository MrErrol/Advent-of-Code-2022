import itertools
from copy import copy
from typing import Tuple, List

import igraph
from time import time

t0 = time()


def parse_line(line: str) -> Tuple[str, int, List[Tuple[str, str]]]:
    lline, rline = line.split(";")
    name = lline.split(" ")[1]
    flow = int(lline.split("=")[-1])
    others = [(name, other.rstrip(",")) for other in rline.split(" ")[5:]]
    return name, flow, others


with open("input.txt", "+r") as file:
    raw_lines = file.read().split("\n")

lines = [parse_line(line) for line in raw_lines]

name_to_index = {line[0]: ind for ind, line in enumerate(lines)}

edges = list(
    itertools.chain.from_iterable(
        [[(name_to_index[vertex[0]], name_to_index[vertex[1]]) for vertex in line[2]] for line in lines]
    )
)

n_vertices = len(lines)
graph = igraph.Graph(n_vertices, edges)
interesting_vertices = {line[0]: line[1] for line in lines if (line[1] != 0) or (line[0] == "AA")}

distances = {}
for name1 in interesting_vertices:
    for name2 in interesting_vertices:
        distances[(name1, name2)] = (
            len(graph.get_shortest_paths(name_to_index[name1], to=name_to_index[name2], output="vpath")[0]) - 1
        )


# Start searching
def find_best_path(vertices: dict, distances: dict, position: str, time: int, score: int) -> int:
    new_vertices = copy(vertices)
    new_vertices.pop(position)
    options = {}
    for vertex in new_vertices.keys():
        new_time = time - distances[(position, vertex)] - 1
        if new_time < 0:
            continue
        best_future = find_best_path(
            vertices=new_vertices,
            distances=distances,
            position=vertex,
            time=new_time,
            score=score + new_time * vertices[vertex],
        )
        options[vertex] = best_future
    if not options:
        return score
    return max(options.values())


max_pressure_released = find_best_path(
    vertices=interesting_vertices, distances=distances, position="AA", time=30, score=0
)


print(f"First star score: {max_pressure_released}")

# idea for second star taken from: https://github.com/btrotta/advent-of-code-2022/tree/main
# I tried to designed some pruning approach, yet it was still to time consuming

complete_paths = []
incomplete_paths = [[("AA", 26)]]
while incomplete_paths:
    new_incomplete = []
    for path in incomplete_paths:
        visited = {v for v, _ in path}
        current_position, current_time = path[-1]
        any_option = 0
        for vertex in interesting_vertices:
            if vertex in visited:
                continue
            time_cost = distances[(current_position, vertex)] + 1
            if  time_cost > current_time:
                continue
            any_option = 1
            new_incomplete.append(path + [(vertex, current_time - time_cost)])
        complete_paths.append(path)
    incomplete_paths = new_incomplete

def score_path(path: List) -> int:
    score = 0
    for v, time in path:
        score += interesting_vertices[v] * time
    return score

best_paths = {}
for path in complete_paths:
    visited = frozenset(v for v, _ in path[1:])  # ignore AA point
    score = score_path(path)
    if visited in best_paths.keys():
        best_paths[visited] = max([best_paths[visited], score])
    else:
        best_paths[visited] = score

best_option = 0
for path1, score1 in best_paths.items():
    for path2, score2 in best_paths.items():
        if not path1.intersection(path2):
            option = score1 + score2
            best_option = max([best_option, option])

print(f"Second star solution: {best_option}")
