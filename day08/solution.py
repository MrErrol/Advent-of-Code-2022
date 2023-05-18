import numpy as np


def is_visible(trees: np.array, i: int, j: int) -> bool:
    vision_lines = [trees[i, :j], trees[i, j + 1 :], trees[:i, j], trees[i + 1 :, j]]
    if any(not len(line) for line in vision_lines):
        return True  # the tree is on the edge
    height = trees[i, j]
    is_visible = any(max(line) < height for line in vision_lines)
    return is_visible


def length_of_view(line: np.array, height: int) -> int:
    if not len(line):
        return 0
    try:
        lower_trees = list(line < height).index(0)
        return lower_trees + 1
    except ValueError:
        return len(line)


def scenic_score(trees: np.array, i: int, j: int) -> int:
    vision_lines = [trees[i, :j][::-1], trees[i, j + 1 :], trees[:i, j][::-1], trees[i + 1 :, j]]
    lengths_of_view = [length_of_view(line, trees[i, j]) for line in vision_lines]
    return lengths_of_view[0] * lengths_of_view[1] * lengths_of_view[2] * lengths_of_view[3]


with open("input.txt", "+r") as file:
    raw_input = file.read()

trees = np.array([[int(height) for height in row] for row in raw_input.split("\n")])
is_visible = [[is_visible(trees, i, j) for j, _ in enumerate(trees[0])] for i, _ in enumerate(trees)]

solution_1 = sum([sum(line) for line in is_visible])

print(f"First star solution: {solution_1}")

scenic_scores = [[scenic_score(trees, i, j) for j, _ in enumerate(trees[0])] for i, _ in enumerate(trees)]
solution_2 = max(max(line) for line in scenic_scores)

print(f"Second star solution: {solution_2}")
