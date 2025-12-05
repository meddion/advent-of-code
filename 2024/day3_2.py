def load_instructs():
    with open("day3.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    inst = load_instructs()
    res_sum = 0
    i = 0
    is_disabled = False
    while i < len(inst):
        if inst[i : i + 7] == "don't()":
            is_disabled = True
            i += 7
            continue

        if inst[i : i + 4] == "do()":
            is_disabled = False
            i += 4
            continue

        if inst[i : i + 4] == "mul(":
            i += 4
            start = i
            is_numeric = True
            while inst[i] != ",":
                if not inst[start : i + 1].isnumeric():
                    is_numeric = False
                    break
                i += 1

            if not is_numeric:
                continue

            num1 = int(inst[start:i])

            i += 1
            start = i
            while inst[i] != ")":
                if not inst[start : i + 1].isnumeric():
                    is_numeric = False
                    break
                i += 1

            if not is_numeric:
                continue

            num2 = int(inst[start:i])

            if not is_disabled:
                print(f"mul({num1}, {num2})")
                res_sum += num1 * num2
        i += 1

    print(res_sum)
