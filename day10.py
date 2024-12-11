import unittest


def trailhead_scores_sum(data: str) -> int:
    trail_map = [
        list(map(int, filter(lambda x: x != " ", row)))
        for row in data.strip().split("\n")
    ]

    trailheads = {}
    for i, row in enumerate(trail_map):
        for j, num in enumerate(row):
            if num == 0:
                start_pos = (i, j)
                find_trailhead(trailheads, trail_map, start_pos, start_pos)

    # Calculate the scores
    return sum(len(unique_heads) for unique_heads in trailheads.values())


def find_trailhead(
    trailheads: dict,
    trail_map: list[int],
    start_pos: tuple[int, int],
    pos: tuple[int, int],
):
    if trail_map[pos[0]][pos[1]] == 9:
        trailheads.setdefault(start_pos, set()).add(pos)
        return

    for y, x in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        new_pos = (pos[0] + y, pos[1] + x)
        if (
            0 <= new_pos[0] < len(trail_map)
            and 0 <= new_pos[1] < len(trail_map[0])
            and trail_map[new_pos[0]][new_pos[1]] - trail_map[pos[0]][pos[1]] == 1
        ):
            find_trailhead(trailheads, trail_map, start_pos, new_pos)


class Test(unittest.TestCase):
    def test1(self):
        data = """
        0123
        1234
        8765
        9876"""
        self.assertEqual(trailhead_scores_sum(data), 1)

    def test2(self):
        data = """
        89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732
        """
        self.assertEqual(trailhead_scores_sum(data), 36)


if __name__ == "__main__":
    # unittest.main()
    data = open("day10.txt", "r").read()
    print(trailhead_scores_sum(data))
