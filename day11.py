import unittest


def count_stones(stones: str, blink_times: int) -> int:
    stones = stones.split(" ")
    for _ in range(blink_times):
        i = 0
        while i < len(stones):
            if stones[i] == "0":
                stones[i] = "1"
            elif len(stones[i]) % 2 == 0:
                mid = len(stones[i]) // 2
                first_part, second_part = stones[i][:mid], stones[i][mid:]
                second_part = second_part.lstrip("0")
                if second_part == "":
                    second_part = "0"

                stones[i] = first_part
                stones.insert(i + 1, second_part)
                i += 1
            else:
                stones[i] = str(int(stones[i]) * 2024)

            i += 1

    return len(stones)


class Test(unittest.TestCase):
    def test1(self):
        stones = "125 17"
        self.assertEqual(count_stones(stones, 6), 22)
        self.assertEqual(count_stones(stones, 25), 55312)


if __name__ == "__main__":
    # unittest.main()
    stones = "0 7 198844 5687836 58 2478 25475 894"
    print(count_stones(stones, 25))
