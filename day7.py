import unittest
from itertools import product
from time import time


def generate_combinations(n):
    return list(product([0, 1], repeat=n))


def dict_from_data(data: str) -> dict:
    d = {}
    for row in data.strip().split("\n"):
        target, rest = row.split(":")
        target = int(target)
        nums = [int(num) for num in rest.strip().split(" ")]
        assert d.get(target) is None
        d[target] = nums

    return d


def calculate_calibration(data: str) -> int:
    d = dict_from_data(data)

    valid_targets = []
    # Naive approach 2^(len(nums)-1)
    for target in d.keys():
        nums = d[target]
        start_t = time()

        for comb in generate_combinations(len(nums) - 1):
            comp_target = nums[0]
            for i, op_code in enumerate(comb, 1):
                if op_code == 0:
                    comp_target *= nums[i]
                else:
                    comp_target += nums[i]

                if comp_target >= target and i != len(comb) - 1:
                    break

            if comp_target == target:
                valid_targets.append(target)
                break

        end_t = time()
        print(f"{target} took: {end_t - start_t}s")

    return sum(valid_targets)


class Test(unittest.TestCase):
    def test1(self):
        data = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
        self.assertEqual(calculate_calibration(data), 3749)


def print_stats(data: str):
    import statistics as stat

    d = dict_from_data(data)
    targets = d.keys()

    sizes = [len(nums) for nums in d.values()]
    print(f"Num of targets: {len(targets)}")
    print(f"Min={min(sizes)} Max={max(sizes)} median={stat.median(sizes)}")
    print(
        f"(2^n-1): Min={2**(min(sizes)-1)} Max={2**(max(sizes)-1)} median={2**(stat.median(sizes))}"
    )

    print(f"Median num of operations: {len(targets)*2**(stat.median(sizes))}")
    print(f"Max num of operations: {len(targets)*2**(max(sizes))}")


if __name__ == "__main__":
    # unittest.main()
    with open("day7.txt", "r") as f:
        data = f.read()

    # print_stats(data)
    print(calculate_calibration(data))
