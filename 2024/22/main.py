from collections import deque
from concurrent.futures import ProcessPoolExecutor


bitmask = 0b111111111111111111111111


def secret(n: int) -> int:
    n ^= n << 6
    n &= bitmask
    n ^= n >> 5
    n ^= n << 11
    n &= bitmask

    return n


def check_sequence(seq: tuple[int]) -> int:
    q = deque()
    total = 0
    for n in nums:
        s = n
        s_mod = s % 10
        for _ in range(2000):
            new_s = secret(s)
            new_s_mod = new_s % 10
            d = new_s_mod - s_mod
            s = new_s
            s_mod = new_s_mod
            q.append(d)
            if len(q) == 5:
                q.popleft()
            if len(q) == 4:
                match = True
                i = 0
                for n in q:
                    if n != seq[i]:
                        match = False
                        break
                    i += 1

                if match:
                    total += new_s_mod
                    break

    return total


with open("input.txt") as f:
    nums = [int(l.strip()) for l in f.readlines()]
    possible_sequences = set()

    q = deque()
    res = 0
    c = 0
    for n in nums:
        c += 1
        print(f"{c} / {len(nums)}")
        s = n
        for i in range(2000):
            new_s = secret(s)
            d = (new_s % 10) - (s % 10)
            s = new_s
            q.append(d)
            if len(q) == 5:
                q.popleft()
            if len(q) == 4:
                possible_sequences.add(tuple(q))

    best = 0
    c = 0
    with ProcessPoolExecutor() as pool:
        for res in pool.map(check_sequence, possible_sequences, chunksize=10):
            c += 1
            print(
                f"[{int((c/len(possible_sequences)*100))}%] {c} / {len(possible_sequences)}"
            )

            if res > best:
                print(f"New best: {res}")
                best = res

    print(best)
