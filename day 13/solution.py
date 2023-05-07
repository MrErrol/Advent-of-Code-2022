import itertools
from functools import cmp_to_key
from typing import Union, List
import json

def compare_values(left: Union[int, List], right: Union[int, List]) -> int:
    """
    1 - order is right
    0 - not conclusive
    -1 - order is wrong
    """
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        if left > right:
            return -1
        return 0
    if isinstance(left, list) and isinstance(right, list):
        for i in range(max([len(left), len(right)])):
            if i + 1 > len(left):
                return 1
            if i + 1 > len(right):
                return -1
            try:
                result = compare_values(left[i], right[i])
            except IndexError:
                assert 1
            if result != 0:
                return result
        return 0
    if isinstance(left, int):
        return compare_values([left], right)
    if isinstance(right, int):
        return compare_values(left, [right])

    assert False, "Something went wrong"

with open("input.txt", "+r") as file:
    raw_pairs = file.read().split("\n\n")

pairs = [[json.loads(packet) for packet in raw_pair.split("\n")] for raw_pair in raw_pairs]

indices_in_order = []
for ind, (left, right) in enumerate(pairs, start=1):
    in_order = compare_values(left, right)
    assert in_order != 0, "comparison should always distinguish"
    if in_order == 1:
        indices_in_order.append(ind)

print(f"First star solution: {sum(indices_in_order)}")

new_packets = [[[2]], [[6]]]
packets = list(itertools.chain.from_iterable(pairs)) + new_packets

# I defined my function opposite way than convention
packets = sorted(packets, key=cmp_to_key(lambda x, y: compare_values(y, x)))

ind1 = packets.index(new_packets[0]) + 1
ind2 = packets.index(new_packets[1]) + 1

print(f"Second star solution: {ind1 * ind2}")
