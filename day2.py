def get_levels():
    with open("day2.txt", "r") as f:
        data = f.read().splitlines()
        return [[int(n) for n in row.split(" ")] for row in data]


if __name__ == "__main__":
    levels = get_levels()
    valid_count = 0

    for level in levels:
        is_inc = True
        for i, num in enumerate(level):
            if i == len(level) - 1:
                valid_count += 1
                break

            step = level[i + 1] - num
            if step == 0:
                break

            if i == 0 and step < 0:
                is_inc = False

            if is_inc and (step < 0 or step > 3):
                break

            if not is_inc and (step > 0 or step < -3):
                break

    print(valid_count)
