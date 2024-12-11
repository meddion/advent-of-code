import unittest


def count_checksums(disk: list[str | int]) -> int:
    start, end = 0, len(disk) - 1
    while True:
        while start < len(disk) and disk[start] != ".":
            start += 1

        while end >= 0 and disk[end] == ".":
            end -= 1

        if start >= end:
            break

        disk[start] = disk[end]
        disk[end] = "."
        end -= 1
        start += 1

    return sum(i * int(el) for i, el in enumerate(disk) if el != ".")


def expand_compact_disk(compact: str) -> list[str]:
    disk = []
    j = 0
    for i, el in enumerate(compact):
        num = int(el)
        if i % 2 == 1:
            disk.extend(num * ["."])
        else:
            disk.extend(num * [j])
            j += 1

    return disk


class Test(unittest.TestCase):
    def test(self):
        data = list("00...111...2...333.44.5555.6666.777.888899")
        self.assertEqual(count_checksums(data), 1928)


if __name__ == "__main__":
    # unittest.main()
    comp_disk = open("day9.txt", "r").read().strip()
    disk = expand_compact_disk(comp_disk)
    print(count_checksums(disk))
