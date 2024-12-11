def get_lists():
    list1 = []
    list2 = []
    with open("day1.txt", "r") as f:
        for row in f.read().splitlines():
            num1, num2, *_ = row.split("   ")
            list1.append(int(num1))
            list2.append(int(num2))

    return list1, list2


if __name__ == "__main__":
    list1, list2 = get_lists()
    list1.sort()
    list2.sort()

    res = 0
    for el1, el2 in zip(list1, list2):
        res += abs(el1 - el2)

    print(res)
