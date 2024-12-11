import unittest

from day2 import get_levels


def count_safe(level, is_inc):
    idx = -1

    def _count_safe(level, is_inc):
        nonlocal idx
        for i, num in enumerate(level):
            if i == len(level) - 1:
                return 1

            step = level[i + 1] - num
            if step == 0:
                idx = i
                return 0

            if is_inc and (step < 0 or step > 3):
                idx = i
                return 0

            if not is_inc and (step > 0 or step < -3):
                idx = i
                return 0

    count = _count_safe(level, is_inc)
    if idx == -1:
        return count

    _idx = idx
    return max(
        _count_safe(level[:_idx] + level[_idx + 1 :], is_inc),
        _count_safe(level[: _idx + 1] + level[_idx + 2 :], is_inc),
    )


class TestCountSafe(unittest.TestCase):
    def test_safe_without_removing(self):
        self.assertEqual(count_safe([7, 6, 4, 2, 1], False), 1)
        self.assertEqual(count_safe([1, 3, 6, 7, 9], True), 1)

    def test_unsafe_regardless(self):
        self.assertEqual(count_safe([1, 2, 7, 8, 9], True), 0)
        self.assertEqual(count_safe([9, 7, 6, 2, 1], False), 0)

    def test_safe_by_removing(self):
        self.assertEqual(count_safe([1, 3, 2, 4, 5], True), 1)
        self.assertEqual(count_safe([8, 6, 4, 4, 1], False), 1)
        self.assertEqual(count_safe([1, 3, 2, 4, 5], False), 0)
        self.assertEqual(count_safe([8, 6, 4, 4, 1], True), 0)


if __name__ == "__main__":
    # unittest.main()

    levels = get_levels()

    valid_count = 0

    for level in levels:
        valid_count += max(
            count_safe(level.copy(), True), count_safe(level.copy(), False)
        )

    print(valid_count)
