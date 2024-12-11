import unittest
from collections.abc import Iterator
from enum import Enum
from heapq import heappop, heappush

# sys.setrecursionlimit(2_500)


class Dir(Enum):
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4


INF = 2**63 - 1


def find_char(maze: list[list[str]], char: str) -> tuple[int, int]:
    def _index(list: list, char: str) -> int:
        try:
            return list.index(char)
        except ValueError:
            return -1

    start_cord = None
    for i in range(1, len(maze) - 1):
        if (j := _index(maze[i], char)) != -1:
            start_cord = (i, j)

    assert start_cord is not None

    return start_cord


def parse_maze_str(maze: str) -> list[list[str]]:
    return [
        list(filter(lambda char: char != " ", row)) for row in maze.strip().split("\n")
    ]


def best_path_recursive(maze: str) -> int:
    maze = parse_maze_str(maze)
    best_score = INF

    def pos_hash(pos):
        return pos[0] * 1000 + pos[1]

    def next_step(
        explored_cords: set,
        score: int,
        pos: tuple[int, int],
        dir: Dir,
    ):
        nonlocal maze, best_score

        if maze[pos[0]][pos[1]] == "E":
            best_score = min(best_score, score)
            return

        for step, new_dir in [
            ((-1, 0), Dir.UP),
            ((1, 0), Dir.DOWN),
            ((0, -1), Dir.LEFT),
            ((0, 1), Dir.RIGHT),
        ]:
            n_cord = (pos[0] + step[0], pos[1] + step[1])
            if (
                n_cord[0] < 1
                or n_cord[0] > len(maze) - 1
                or n_cord[1] < 1
                or n_cord[1] > len(maze[0]) - 1
                or pos_hash(n_cord) in explored_cords
                or maze[n_cord[0]][n_cord[1]] == "#"
            ):
                continue

            match abs(dir.value - new_dir.value):
                case 0:
                    cost = 1
                case 2:
                    cost = 2001
                case _:
                    cost = 1001

            new_score = score + cost
            if new_score > best_score:
                continue

            exp_cords = explored_cords.copy()
            exp_cords.add(pos_hash(pos))

            next_step(exp_cords, new_score, n_cord, new_dir)

    start_cord = find_char(maze, "S")
    next_step(set(), 0, start_cord, Dir.RIGHT)

    return best_score


def neighbors(maze: list[list[str]], pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
    for step, n_dir in [
        ((-1, 0), Dir.UP),
        ((1, 0), Dir.DOWN),
        ((0, -1), Dir.LEFT),
        ((0, 1), Dir.RIGHT),
    ]:
        n_cord = (pos[0] + step[0], pos[1] + step[1])
        if (
            n_cord[0] < 1
            or n_cord[0] > len(maze) - 1
            or n_cord[1] < 1
            or n_cord[1] > len(maze[0]) - 1
            or maze[n_cord[0]][n_cord[1]] == "#"
        ):
            continue

        yield n_cord, n_dir


def score(dir: Dir, n_dir: Dir) -> int:
    match abs(dir.value - n_dir.value):
        case 0:
            cost = 1
        case 2:
            cost = 2001
        case _:
            cost = 1001

    return cost


def best_path_dijkstra(maze_str: str) -> int:
    maze = parse_maze_str(maze_str)
    start_pos, end_pos = find_char(maze, "S"), find_char(maze, "E")
    scores, prev = {start_pos: 0}, {}

    positions = []
    heappush(positions, (0, start_pos, Dir.RIGHT))
    while positions:
        _, cur_pos, cur_dir = heappop(positions)
        if (
            cur_pos == end_pos
        ):  # Perhaps a shorter path wasn't explored yet, keep checking...
            continue

        for n_pos, n_dir in neighbors(maze, cur_pos):
            alt = scores[cur_pos] + score(cur_dir, n_dir)
            if alt < scores.get(n_pos, INF):
                scores[n_pos] = alt
                prev[n_pos] = cur_pos  # For debugging
                # Optimizarion: something like Q.decrease_priority(v, alt)
                heappush(positions, (alt, n_pos, n_dir))

    return scores[end_pos]


class Test(unittest.TestCase):
    def test1_part1(self):
        maze = """
        ###############
        #.......#....E#
        #.#.###.#.###.#
        #.....#.#...#.#
        #.###.#####.#.#
        #.#.#.......#.#
        #.#.#####.###.#
        #...........#.#
        ###.#.#####.#.#
        #...#.....#.#.#
        #.#.#.###.#.#.#
        #.....#...#.#.#
        #.###.#.#.#.#.#
        #S..#.....#...#
        ###############
        """
        self.assertEqual(best_path_recursive(maze), 7036)
        self.assertEqual(best_path_dijkstra(maze), 7036)


if __name__ == "__main__":
    # unittest.main()
    with open("day16.txt", "r") as f:
        maze = f.read()
    print(best_path_dijkstra(maze))
