import re
import unittest
from dataclasses import dataclass


@dataclass
class Button:
    x: int
    y: int


@dataclass
class Machine:
    prize: tuple[int, int]
    a: Button
    b: Button


def parse_button(line: str) -> Button:
    pattern = r"Button (A|B): X\+(\d+), Y\+(\d+)"
    match = re.search(pattern, line)
    if not match:
        raise ValueError(f"wrong format: {line}")

    return Button(x=int(match.group(2)), y=int(match.group(3)))


def parse_prize(line: str) -> tuple[int, int]:
    pattern = r"Prize: X=(\d+), Y=(\d+)"
    match = re.search(pattern, line)
    if not match:
        raise ValueError(f"wrong format: {line}")

    return int(match.group(1)), int(match.group(2))


def calc_min_tokens(prizes: str) -> int:
    prizes = prizes.strip().split("\n")
    machines = [
        Machine(
            a=parse_button(prizes[i]),
            b=parse_button(prizes[i + 1]),
            prize=parse_prize(prizes[i + 2]),
        )
        for i in range(0, len(prizes), 4)
    ]

    def minimum_tokens(machine: Machine):
        cache = {}

        def new_seq_key(A_times: int, B_times: int) -> str:
            return f"A{A_times}B{B_times}"

        def _find_matches(A_times: int, B_times: int):
            nonlocal cache, machine

            if A_times > 100 or B_times > 100:
                return 0

            seq_key = new_seq_key(A_times, B_times)

            if cache.get(seq_key, -1) != -1:
                return cache[seq_key]

            x_sum = A_times * machine.a.x + B_times * machine.b.x
            y_sum = A_times * machine.a.y + B_times * machine.b.y
            if x_sum == machine.prize[0] and y_sum == machine.prize[1]:
                return A_times * 3 + B_times

            if x_sum > machine.prize[0] or y_sum > machine.prize[1]:
                return 0

            cache[new_seq_key(A_times, B_times + 1)] = _find_matches(
                A_times, B_times + 1
            )

            cache[new_seq_key(A_times + 1, B_times)] = _find_matches(
                A_times + 1, B_times
            )

            return 0

        cache["A1B0"] = _find_matches(1, 0)
        cache["A0B1"] = _find_matches(0, 1)

        return min(filter(lambda v: v != 0, cache.values()), default=0)

    return sum(map(minimum_tokens, machines))


class Test(unittest.TestCase):
    def test1_part1(self):
        data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

        self.assertEqual(calc_min_tokens(data), 480)


if __name__ == "__main__":
    # unittest.main()
    prizes = open("day13.txt", "r").read()
    print(calc_min_tokens(prizes))
