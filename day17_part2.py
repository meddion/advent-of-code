def program(A):
    B = A % 8  # Equal to taking 3 lowest bits
    B ^= 2  # Xor the 3 bits with 0b010 (flips the values)
    C = A // 2**B  # Equal to shifting A to the right B times (B is 3 bits: 0-7)
    B ^= C  # XOR the first 3 bits of C and store to B (B is 3 bits long)
    B ^= 7  # XOR with 0b111, transform first 3 bits
    B %= 8  # Equal to taking 3 lowest bits
    # Equal to shifting A to the right 3 times (int division),
    # taking the first 3 bits away. Making the initial A 16 * 3 = 48 bit long
    A //= 8

    return B, A


if __name__ == "__main__":
    exp_program = [2, 4, 1, 2, 7, 5, 4, 3, 0, 3, 1, 7, 5, 5, 3, 0]
    A = 0
    for B_exp in reversed(exp_program):
        A = A << 3
        for i in range(8):
            B_ret, A_ret = program(A + i)
            if B_ret == B_exp:
                A = A + i
                break

    print(A)

    # for A_init in range(8**15, 8**16):
    #     i = 0
    #     A = A_init
    #     while i < len(exp_program) and A != 0:
    #         B, A = program(A)
    #         if B != exp_program[i]:
    #             break

    #         if A == 0:
    #             print("Result: ", A_init)

    #         i += 1
