from copy import deepcopy
from typing import Optional, Dict, List

from scipy.optimize import bisect

with open("input.txt", "+r") as file:
    raw_lines = file.read().split("\n")


class Monkey(object):
    def __init__(self, name, **kwargs):
        self.name: str = name
        self.value: Optional[float] = kwargs.get("value")
        self.left: Optional[str] = kwargs.get("left")
        self.right: Optional[str] = kwargs.get("right")
        self.operation: Optional[str] = kwargs.get("operation")

    @property
    def is_known(self) -> bool:
        return self.value is not None

    def can_calculate(self, database: Dict[str, Optional[int]]) -> bool:
        return (self.left in database) and (self.right in database)

    def calculate(self, database: Dict[str, Optional[int]]) -> Optional[float]:
        if self.is_known:
            return self.value
        if not self.can_calculate(database):
            return None
        if self.operation == "+":
            self.value = database[self.left] + database[self.right]
        elif self.operation == "-":
            self.value = database[self.left] - database[self.right]
        elif self.operation == "*":
            self.value = database[self.left] * database[self.right]
        elif self.operation == "/":
            self.value = database[self.left] / database[self.right]
        return self.value

    @classmethod
    def from_line(self, line: str):
        name = line[:4]
        description = line[6:]
        try:
            value = int(description)
            return Monkey(name=name, value=value)
        except ValueError:
            left, operator, right = description.split(" ")
            return Monkey(name=name, left=left, operation=operator, right=right)

    @classmethod
    def advanced_from_line(self, line: str):
        name = line[:4]
        description = line[6:]
        try:
            value = int(description)
            return Monkey(name=name, value=value)
        except ValueError:
            left, operator, right = description.split(" ")
            if name == "root":
                operator = "-"
            return Monkey(name=name, left=left, operation=operator, right=right)

    def __str__(self):
        if self.value is not None:
            return f"Monkey({self.value})"
        return f"Monkey({self.left}{self.operation}{self.right})"

def solve_monkeys(monkeys: List[Monkey]) -> dict:
    unknown_monkeys = monkeys
    database = {}
    while unknown_monkeys:
        still_to_do: List[Monkey] = []
        for monkey in unknown_monkeys:
            if monkey.is_known:
                database[monkey.name] = monkey.value
            elif monkey.can_calculate(database):
                database[monkey.name] = monkey.calculate(database)
            else:
                still_to_do.append(monkey)
        unknown_monkeys = still_to_do
    return database

def get_root_difference(monkeys: List[Monkey], human: int) -> int:
    solved = solve_monkeys(deepcopy(monkeys) + [Monkey(name="humn", value=human)])
    return solved["root"]

unknown_monkeys: List[Monkey]  = [Monkey.from_line(line) for line in raw_lines]
solved = solve_monkeys(unknown_monkeys)
solution_1 = solved["root"]

print(f"First star solution: {int(solution_1)}")

correct_monkeys: List[Monkey] = [Monkey.advanced_from_line(line) for line in raw_lines if line[:4] != "humn"]

# one needs to make b manually high enough to get negative value from provided lambda function
approx: float = bisect(lambda h: get_root_difference(correct_monkeys, human=h), a=0, b=10_000_000_000_000, maxiter=100)

left_guess = int(approx)
if get_root_difference(deepcopy(correct_monkeys), left_guess) == 0:
    solution_2 = left_guess
elif get_root_difference(deepcopy(correct_monkeys), left_guess+1) == 0:
    solution_2 = left_guess + 1
else:
    solution_2 = None

if solution_2 is not None:
    print(f"Second star solution: {solution_2}")