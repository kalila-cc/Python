# -*- coding: utf-8 -*-

# author: cc
# time: 2020-09-13

from time import sleep

def get_func(description: str):
    if description == 'x-1':
        return [
            "001L1",
            "010Nq",
            "110Nq",
            "101L1"
            "1bbLq"
        ]
    elif description == 'x+1':
        return [
            "001Nq",
            "010L1",
            "101Nq",
            "110L1",
            "1bbNq"
        ]
    elif description == 'x+3':
        return [
            "001L1",
            "010L2",
            "101Nq",
            "110L1",
            "211L3",
            "200L3",
            "301Nq",
            "310L3"
        ]
    elif description == 'x*2':
        return [
            "000L0",
            "010L1",
            "111L1",
            "101L0",
            "0bbNq",
            "1bbNq"
        ]
    else:
        return []


def get_subscript(n: str):
    if n in '0123456789':
        return chr(8320 + int(n))
    return chr(8337)


def display(sub_order, num_list, index):
    sleep(0.8)
    if sub_order[-1] != "b":
        sub_order = sub_order[:-1] + "q" + sub_order[-1]
    print()
    print(" " + " ".join(num_list))
    print("  " * len(num_list[:-index]) + " ↑")
    print("  " * len(num_list[:-index]) + " q" + get_subscript(sub_order[0]))
    sub_order = get_subscript(sub_order[0]) + sub_order[1:-1] + (get_subscript(sub_order[-1]))
    print("\n execute : q{}".format(sub_order))


def main():
    desc = 'x*2'
    order_list = get_func(desc)
    num = str(bin(eval(input(f"Function S(x)={desc}.\nPlease input a number:\n"))))
    num_list = list("0b" + "0" * (5 - (len(num) - 3) % 4) + num[2:])
    i, end = 1, "0"
    s_dict = {"L": 1, "R": -1, "N": 0}
    while end != "q":
        for sub_order in order_list:
            if num_list[-i] == sub_order[1] and end == sub_order[0]:
                display(sub_order, num_list, i)
                num_list[-i] = sub_order[2]
                end = sub_order[4]
                display(sub_order, num_list, i)
                i += s_dict[sub_order[3]]
                break
    result = int(eval("".join(num_list)))
    print(f"\n\nThe result is {result}.")


if __name__ == '__main__':
    main()
