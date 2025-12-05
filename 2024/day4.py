from typing import List


def read_xmas() -> List[str]:
    with open("day4.txt") as f:
        return f.read().strip().splitlines()


def count_occurrences(data: List[str], substr: str) -> int:
    count = 0
    for line in data:
        start = 0
        while True:
            start = line.find(substr, start)
            if start == -1:
                break
            count += 1
            start += 1  # Move past the last found substring
    return count


def _get_diagonals(xmas):
    diagonals = []
    n_rows = len(xmas)
    n_cols = len(xmas[0])

    # Get diagonals starting from the first row
    for start_col in range(n_cols):
        diagonal = ""
        row, col = 0, start_col
        while row < n_rows and col < n_cols:
            diagonal += xmas[row][col]
            row += 1
            col += 1
        diagonals.append(diagonal)

    # Get diagonals starting from the first column (excluding the top-left)
    for start_row in range(1, n_rows):
        diagonal = ""
        row, col = start_col, 0
        while row < n_rows and col < n_cols:
            diagonal += xmas[row][col]
            row += 1
            col += 1
        diagonals.append(diagonal)

    return diagonals


def get_diagonals(xmas):
    diagonals = _get_diagonals(xmas)
    rev_xmas = [row[::-1] for row in xmas]
    rev_diagonals = _get_diagonals(rev_xmas)

    return diagonals + rev_diagonals


def get_vertical(xmas):
    verticals = []
    for colIdx in range(len(xmas[0])):
        vertical_str = ""
        for rowIdx in range(len(xmas)):
            vertical_str += xmas[rowIdx][colIdx]
        verticals.append(vertical_str)

    return verticals


import unittest


class Test(unittest.TestCase):
    def test2(self):
        data = """
XOOOSOOO
OMOOOAOO
OOAOOOMO
OOOSOOOX
OOOOOOOO""".strip().splitlines()
        self.assertEqual(count_xmas(data), 2)

    def test3(self):
        data = """
..X...
.SAMX.
.A..A.
XMAS.S
.X....""".strip().splitlines()
        self.assertEqual(count_xmas(data), 4)

    def test(self):
        data = """
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX""".strip().splitlines()
        self.assertEqual(count_xmas(data), 18)


def count_xmas(xmas):
    verticals = get_vertical(xmas)
    diagonals = get_diagonals(xmas)
    count = count_occurrences(xmas, "XMAS") + count_occurrences(xmas, "SAMX")
    count += count_occurrences(verticals, "XMAS") + count_occurrences(verticals, "SAMX")
    count += count_occurrences(diagonals, "XMAS") + count_occurrences(diagonals, "SAMX")

    return count


if __name__ == "__main__":
    unittest.main()
    xmas = read_xmas()
    count = count_xmas(xmas)
    print(count)
