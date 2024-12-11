from functools import reduce

from day1 import get_lists

if __name__ == "__main__":
    list1, list2 = get_lists()

    list1_dict = {el: 0 for el in list1}
    for el2 in list2:
        if el2 in list1_dict:
            list1_dict[el2] += 1

    res = reduce(lambda acc, k: acc + k * list1_dict[k], list1_dict.keys(), 0)
    print(res)
