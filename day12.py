import unittest


def part1_fence_price(garden: str):
    garden = [
        list(filter(lambda c: c != " ", row)) for row in garden.strip().split("\n")
    ]

    def get_dimensions(
        init_cord: tuple[int, int], target_plant: str
    ) -> tuple[int, int]:
        nonlocal garden

        area = 0
        perimeter = 0

        stack: list[tuple[int, int]] = [init_cord]
        while len(stack) != 0:
            cord = stack.pop()

            if garden[cord[0]][cord[1]] != target_plant:
                continue

            area += 1
            garden[cord[0]][cord[1]] = "#"

            for step in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_cord = (cord[0] + step[0], cord[1] + step[1])
                if (
                    0 > next_cord[0]
                    or next_cord[0] >= len(garden)
                    or 0 > next_cord[1]
                    or next_cord[1] >= len(garden[0])
                    or garden[next_cord[0]][next_cord[1]] != target_plant
                ):
                    perimeter += 1
                    continue

                stack.append(next_cord)
                perimeter -= 1  # To cancel out the previous perimeter += 1

        return (area, perimeter)

    sum = 0
    for i, row in enumerate(garden):
        for j, plant in enumerate(row):
            if plant == "#":
                continue

            area, perimeter = get_dimensions((i, j), plant)
            sum += area * perimeter

    return sum


def part2_fence_price(garden: str):
    garden = [
        list(filter(lambda c: c != " ", row)) for row in garden.strip().split("\n")
    ]

    def get_dimensions(
        init_cord: tuple[int, int], target_plant: str
    ) -> tuple[int, int]:
        nonlocal garden

        area = 0
        horizontal_nodes = {}
        vertical_nodes = {}
        stack: list[tuple[int, int]] = [init_cord]
        while len(stack) != 0:
            cord = stack.pop()

            if garden[cord[0]][cord[1]] != target_plant:
                continue

            area += 1
            garden[cord[0]][cord[1]] = "#"
            horizontal_nodes.setdefault(cord[0], []).append(cord[1])
            vertical_nodes.setdefault(cord[1], []).append(cord[0])

            for step in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_cord = (cord[0] + step[0], cord[1] + step[1])
                if (
                    0 > next_cord[0]
                    or next_cord[0] >= len(garden)
                    or 0 > next_cord[1]
                    or next_cord[1] >= len(garden[0])
                    or garden[next_cord[0]][next_cord[1]] != target_plant
                ):
                    continue

                stack.append(next_cord)

        def count_sides(nodes: list[list[int]]) -> int:
            sides = 1
            prev_val = nodes[0][0]
            for row in nodes[1:]:
                if row[0] != prev_val:
                    sides += 2
                    prev_val = row[0]

            return sides

        h_nodes = [sorted(values) for values in horizontal_nodes.values()]
        sides = count_sides(h_nodes)
        h_nodes_rev = [list(reversed(n)) for n in h_nodes]
        sides += count_sides(h_nodes_rev)
        v_nodes = [sorted(values) for values in vertical_nodes.values()]
        sides += count_sides(v_nodes)
        v_nodes_rev = [list(reversed(n)) for n in v_nodes]
        sides += count_sides(v_nodes_rev)

        return (area, sides)

    sum = 0
    for i, row in enumerate(garden):
        for j, plant in enumerate(row):
            if plant == "#":
                continue

            area, perimeter = get_dimensions((i, j), plant)
            sum += area * perimeter

    return sum


class Test(unittest.TestCase):
    def test1_part1(self):
        garden = """
        AAAA
        BBCD
        BBCC
        EEEC
        """
        self.assertEqual(part1_fence_price(garden), 140)

    def test2_part1(self):
        garden = """
            RRRRIICCFF
            RRRRIICCCF
            VVRRRCCFFF
            VVRCCCJFFF
            VVVVCJJCFE
            VVIVCCJJEE
            VVIIICJJEE
            MIIIIIJJEE
            MIIISIJEEE
            MMMISSJEEE
            """
        self.assertEqual(part1_fence_price(garden), 1930)

    def test1_part2(self):
        garden = """
        AAAA
        BBCD
        BBCC
        EEEC
        """
        self.assertEqual(part2_fence_price(garden), 80)

    def test2_part2(self):
        garden = """
        EEEEE
        EXXXX
        EEEEE
        EXXXX
        EEEEE
        """
        self.assertEqual(part2_fence_price(garden), 236)

    def test3_part2(self):
        garden = """
        AAAAAA
        AAABBA
        AAABBA
        ABBAAA
        ABBAAA
        AAAAAA
        """
        self.assertEqual(part2_fence_price(garden), 368)


if __name__ == "__main__":
    unittest.main()

    with open("day12.txt") as f:
        data = f.read()

    print("Part 1:", part1_fence_price(data))
    print("Part 2:", part2_fence_price(data))
