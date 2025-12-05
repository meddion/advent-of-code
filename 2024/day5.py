import unittest


def count_middle_numbers(data: str) -> int:
    d = data.strip().split("\n")
    empty_idx = d.index("")

    rules = {}
    for r in d[:empty_idx]:
        first, second = r.split("|")
        first, second = int(first), int(second)
        if not rules.get(first):
            rules[first] = [second]
        else:
            rules[first].append(second)

    updates = [list(map(int, update.split(","))) for update in d[empty_idx + 1 :]]

    # Filter out correct updates
    valid_indices = []
    for j, update in enumerate(updates):
        is_valid = True
        for i, el in enumerate(update):
            if i == 0 or not rules.get(el):
                continue

            exists_before = any(r in update[: i + 1] for r in rules[el])
            if exists_before:
                is_valid = False
                break

        if is_valid:
            valid_indices.append(j)

    return sum(updates[i][len(updates[i]) // 2] for i in valid_indices)


class Test(unittest.TestCase):
    def test1(self):
        data = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
        self.assertEqual(count_middle_numbers(data), 143)


if __name__ == "__main__":
    # unittest.main()
    with open("day5.txt", "r") as f:
        data = f.read()

    print(count_middle_numbers(data))
