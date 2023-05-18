def left_inside_right(left_interval, right_interval) -> bool:
    return (left_interval[0] >= right_interval[0]) and (left_interval[1] <= right_interval[1])


def one_inside_another(left_interval, right_interval) -> bool:
    return left_inside_right(left_interval, right_interval) or left_inside_right(right_interval, left_interval)


def any_overlap(left_interval, right_interval) -> bool:
    """
    Return True if there is any overlap between intervals.
    """
    separate = (left_interval[1] < right_interval[0]) or (right_interval[1] < left_interval[0])
    return not separate


with open("input.txt") as file:
    raw_riddle = file.read().split("\n")

intervals = [[[int(position) for position in pair.split("-")] for pair in row.split(",")] for row in raw_riddle]
sum_contained = sum([one_inside_another(left_interval, right_interval) for left_interval, right_interval in intervals])

print(f"First star solution: {sum_contained}")

sum_overlapping = sum([any_overlap(left_interval, right_interval) for left_interval, right_interval in intervals])

print(f"Second star solution: {sum_overlapping}")
