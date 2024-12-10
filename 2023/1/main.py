from typing import Callable

from aoc import try_or_default


sum = 0
with open("sample.txt") as f:
    lines = f.readlines()

    for l in lines:
        first = next(filter(str.isdigit, l))
        last = next(filter(str.isdigit, reversed(l)))
        sum += int(first + last)
    print(sum)


sum = 0
with open("input.txt") as f:
    lines = f.readlines()
    strs = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    for l in lines:
        _, first = min(
            try_or_default(lambda: (l.index(p), p), (999999999, "")) for p in strs
        )

        _, last = max(
            try_or_default(lambda: (l.rindex(p), p), (-999999999, "")) for p in strs
        )

        sum += strs[first] * 10 + strs[last]

    print(sum)
