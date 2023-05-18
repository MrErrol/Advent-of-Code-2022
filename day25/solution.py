with open("input.txt") as file:
    lines = file.read().split("\n")

SYMBOL_TO_DIGIT = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
DIGIT_TO_SYMBOL = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}


def snafu_to_decimal(snafu: str) -> int:
    if snafu == "":
        return 0
    symbol = snafu[0]
    return SYMBOL_TO_DIGIT[symbol] * 5 ** (len(snafu) - 1) + snafu_to_decimal(snafu[1:])


def decimal_to_snafu(number: int) -> str:
    if number == 0:
        return ""
    remainder = number % 5
    if remainder > 2:
        remainder = remainder - 5
    return decimal_to_snafu((number - remainder) // 5) + DIGIT_TO_SYMBOL[remainder]


assert snafu_to_decimal("1=0") == 15
assert decimal_to_snafu(15) == "1=0"

fuel_needs = [snafu_to_decimal(line) for line in lines]
solution_1 = decimal_to_snafu(sum(fuel_needs))

print(f"First star solution: {solution_1}")
