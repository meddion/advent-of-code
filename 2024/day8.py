import unittest


def count_unique_antinodes(data: str) -> int:
    # Parse the input into a grid and extract antenna positions
    matrix = [list(row) for row in data.strip().split("\n")]
    antennas = {}
    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            if char.isalpha() or char.isnumeric():
                antennas.setdefault(char, []).append((j, i))

    unique_antinodes = set()  # Track unique antinode positions

    def calculate_antinode(c1, c2):
        # Check if c1 and c2 form a valid pair with distance conditions
        dx = c2[0] - c1[0]
        dy = c2[1] - c1[1]

        # Generate the two possible antinodes
        antinode1 = (c1[0] - dx, c1[1] - dy)
        antinode2 = (c2[0] + dx, c2[1] + dy)

        return [antinode1, antinode2]

    for cords in antennas.values():
        n = len(cords)
        for i in range(n):
            for j in range(i + 1, n):
                c1, c2 = cords[i], cords[j]
                # Add valid antinodes to the set
                for antinode in calculate_antinode(c1, c2):
                    if 0 <= antinode[0] < len(matrix[0]) and 0 <= antinode[1] < len(
                        matrix
                    ):
                        unique_antinodes.add(antinode)

    return len(unique_antinodes)


class Test(unittest.TestCase):
    def test(self):
        data = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
        self.assertEqual(count_unique_antinodes(data), 14)


if __name__ == "__main__":
    # unittest.main()

    with open("day8.txt", "r") as f:
        data = f.read()

    print(count_unique_antinodes(data))
