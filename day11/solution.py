from typing import Tuple, Generator, Sequence, Dict


class Monkey:
    def __init__(self, raw_monkey: str, divisor: int = 3):
        raw_rows = raw_monkey.split("\n")
        assert len(raw_rows) == 6
        self.name = int(raw_rows[0][:-1].split(" ")[-1])
        self.items = [int(item.rstrip(",")) for item in raw_rows[1].strip(" ").split(" ")[2:]]
        raw_operation = raw_rows[2].strip(" ").split(" ")[-2:]
        try:
            self.operator = raw_operation[0]
            self.coef = int(raw_operation[1])
        except ValueError:
            self.operator = "**"
            self.coef = 2
        self.divisor = divisor
        self.test = int(raw_rows[3].strip(" ").split(" ")[-1])
        self.target_passed = int(raw_rows[4].split(" ")[-1])
        self.target_failed = int(raw_rows[5].split(" ")[-1])

    def get_item(self, item: int):
        self.items.append(item)

    def inspect_item(self, item_value) -> Tuple[int, int]:
        """
        Returns (target_monkey, new_item_value)
        """
        if self.operator == "+":
            new_value = (item_value + self.coef) // self.divisor
        elif self.operator == "*":
            new_value = (item_value * self.coef) // self.divisor
        elif self.operator == "**":
            new_value = (item_value**self.coef) // self.divisor
        else:
            assert False
        target = self.target_failed if new_value % self.test else self.target_passed
        return target, new_value

    def inspect_items(self) -> Generator[Tuple[int, int], None, None]:
        items = self.items[:]

        def inspected_items():
            for item in items:
                yield self.inspect_item(item)

        self.items = []
        return inspected_items()


class MonkeyPack:
    def __init__(self, monkeys: Sequence[Monkey]):
        self.monkeys: Dict[int, Monkey] = {monkey.name: monkey for monkey in monkeys}
        self.inspections: Dict[int, int] = {name: 0 for name in self.monkeys.keys()}
        self.common_divisor = 1
        for monkey in self.monkeys.values():
            self.common_divisor *= monkey.test

    def play_a_round(self):
        names = list(self.monkeys.keys())
        names.sort()
        for name in names:
            for target, item in self.monkeys[name].inspect_items():
                self.inspections[name] += 1
                self.monkeys[target].get_item(item % self.common_divisor)

    def monkey_business(self) -> int:
        inspection_count = list(self.inspections.values())
        inspection_count.sort()
        return inspection_count[-1] * inspection_count[-2]


with open("input.txt", "+r") as file:
    raw_monkeys = file.read().split("\n\n")

pack = MonkeyPack([Monkey(raw_monkey) for raw_monkey in raw_monkeys])
for _ in range(20):
    pack.play_a_round()

solution_1 = pack.monkey_business()

print(f"First star solution: {solution_1}")

second_pack = MonkeyPack([Monkey(raw_monkey, divisor=1) for raw_monkey in raw_monkeys])
for _ in range(10_000):
    second_pack.play_a_round()

solution_2 = second_pack.monkey_business()

print(f"Second star solution: {solution_2}")
