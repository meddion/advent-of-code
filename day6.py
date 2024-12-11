import unittest

from pandas import DataFrame


def count_positions(data: str) -> int:
    d = [list(row) for row in data.strip().split("\n")]
    df = DataFrame(d)
    n_rows, n_cols = df.shape
    start = df.stack().index[df.stack() == "^"][0]
    cur_dir = "^"

    def get_bedrock(s_range, last):
        l = s_range.index[s_range == "#"].tolist()
        return -1 if len(l) == 0 else l[-1 if last else 0]

    while True:
        if cur_dir == "^":
            s_range = df.iloc[: start[0], start[1]]
            bedrock = get_bedrock(s_range, True)

            if bedrock == -1:
                df.iloc[: start[0], start[1]] = "X"
                break

            df.iloc[bedrock + 1 : start[0] + 1, start[1]] = "X"
            start = (bedrock + 1, start[1])
            cur_dir = ">"
        elif cur_dir == ">":
            s_range = df.iloc[start[0], start[1] :]
            bedrock = get_bedrock(s_range, False)

            if bedrock == -1:
                df.iloc[start[0], start[1] :] = "X"
                break

            df.iloc[start[0], start[1] : bedrock] = "X"

            start = (start[0], bedrock - 1)
            cur_dir = "v"
        elif cur_dir == "<":
            s_range = df.iloc[start[0], : start[1]]
            bedrock = get_bedrock(s_range, True)

            if bedrock == -1:
                df.iloc[start[0], : start[1]] = "X"
                break

            df.iloc[start[0], bedrock + 1 : start[1]] = "X"

            start = (start[0], bedrock + 1)
            cur_dir = "^"
        else:
            s_range = df.iloc[start[0] :, start[1]]
            bedrock = get_bedrock(s_range, False)

            if bedrock == -1:
                df.iloc[start[0] :, start[1]] = "X"
                break

            df.iloc[start[0] : bedrock, start[1]] = "X"

            start = (bedrock - 1, start[1])
            cur_dir = "<"

    # Count all occurences of X

    return (df.values == "X").sum()


class Test(unittest.TestCase):
    def test(self):
        data = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
        self.assertEqual(count_positions(data), 41)


if __name__ == "__main__":
    # unittest.main()
    with open("day6.txt", "r") as f:
        data = f.read()

    print(count_positions(data))
