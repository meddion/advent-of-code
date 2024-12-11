import unittest


def sum_of_box_coordinates(data: str) -> int:
    rows = [row.strip() for row in data.strip().split("\n")]
    idx = rows.index("")
    arena, moves = [list(row) for row in rows[:idx]], "".join(rows[idx + 1 :])

    A_height = len(arena) - 1
    A_width = len(arena[0]) - 1
    robot_cord = None
    for i in range(1, A_height):
        for j in range(1, A_width):
            if rows[i][j] == "@":
                robot_cord = [i, j]
                break

    for move in moves:
        i, j = robot_cord
        match move:
            case "^":
                i -= 1
                while i > 1 and arena[i][j] == "O":
                    i -= 1

                if i < 1 or arena[i][j] != ".":
                    continue

                for k in range(i, robot_cord[0]):
                    arena[k][j] = arena[k + 1][j]

                arena[robot_cord[0]][j] = "."
                robot_cord[0] -= 1

            case "v":
                i += 1
                while i < A_height and arena[i][j] == "O":
                    i += 1

                if i == A_height or arena[i][j] != ".":
                    continue

                for k in range(i, robot_cord[0], -1):
                    arena[k][j] = arena[k - 1][j]

                arena[robot_cord[0]][j] = "."
                robot_cord[0] += 1

            case ">":
                j += 1
                while j < A_width and arena[i][j] == "O":
                    j += 1

                if j == A_width or arena[i][j] != ".":
                    continue

                for k in range(j, robot_cord[1], -1):
                    arena[i][k] = arena[i][k - 1]

                arena[i][robot_cord[1]] = "."
                robot_cord[1] += 1
            case "<":
                j -= 1
                while j > 1 and arena[i][j] == "O":
                    j -= 1

                if j < 1 or arena[i][j] != ".":
                    continue

                for k in range(j, robot_cord[1]):
                    arena[i][k] = arena[i][k + 1]

                arena[i][robot_cord[1]] = "."
                robot_cord[1] -= 1

    # Calc sum of box coordinates
    res_sum = 0
    for i in range(1, A_height):
        for j in range(1, A_width):
            if arena[i][j] == "O":
                res_sum += i * 100 + j

    return res_sum


class Test(unittest.TestCase):
    def test0_part1(self):
        # self.skipTest()

        data = """
        ########
        #..O.O.#
        ##@.O..#
        #...O..#
        #.#.O..#
        #...O..#
        #......#
        ########

        <^^>>>vv<v>>v<<
        """

        self.assertEqual(sum_of_box_coordinates(data), 2028)

    def test1_part1(self):
        data = """
        ##########
        #..O..O.O#
        #......O.#
        #.OO..O.O#
        #..O@..O.#
        #O#..O...#
        #O..O..O.#
        #.OO.O.OO#
        #....O...#
        ##########

        <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
        vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
        ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
        <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
        ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
        ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
        >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
        <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
        ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
        v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
        """

        self.assertEqual(sum_of_box_coordinates(data), 10092)


if __name__ == "__main__":
    # unittest.main()
    with open("day15.txt", "r") as f:
        data = f.read()
    print(sum_of_box_coordinates(data))
