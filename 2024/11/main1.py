from collections import deque


def blink(q: deque) -> deque:
    new_q = deque()
    for i in q:
        if i == "0":
            new_q.append("1")
        elif len(i) % 2 == 0:
            left = i[: int(len(i) / 2)]
            right = i[int(len(i) / 2) :]
            new_q.append(str(int(left)))
            new_q.append(str(int(right)))
        else:
            new_q.append(str(int(i) * 2024))

    return new_q


with open("sample.txt") as f:
    input = f.read().strip()
    split = input.split(" ")
    q = deque(split)
    for i in range(25):
        q = blink(q)
        print(i, ": ", len(q))
