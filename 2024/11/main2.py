from collections import deque
from math import log10


def blink(n: int, c: int) -> int:
    if c == 0:
        return 1

    if (n, c) in cache:
        return cache[(n, c)]

    count = 0

    if n == 0:
        count += blink(1, c - 1)
    elif int(log10(n)) % 2 == 1:
        s = str(n)
        half_len = int(len(s) / 2)
        left = int(s[:half_len])
        right = int(s[half_len:])
        count += blink(left, c - 1)
        count += blink(right, c - 1)
    else:
        count += blink(n * 2024, c - 1)

    cache[(n, c)] = count
    return count


cache = dict()

with open("input.txt") as f:
    input = f.read().strip()
    split = input.split(" ")
    count = 0
    for s in split:
        count += blink(int(s), 75)

    print(count)
