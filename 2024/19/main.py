from functools import cache


stripes = []
designs = []

with open("input_stripes.txt") as f:
    stripes = f.read().strip().split(", ")

with open("input_designs.txt") as f:
    designs = [l.strip() for l in f.readlines()]

max_len = max(len(s) for s in stripes)
stripes_by_len: list[set] = [set()] * (max_len + 1)

for s in stripes:
    stripes_by_len[len(s)].add(s)


@cache
def total_possible_combos(s: str, c: int) -> int:
    global stripes_by_len
    if not s:
        return 1

    if c == 0:
        return 0

    sub = s[:c]
    if sub in stripes_by_len[c]:
        next_s = s[c:]
        next_c = min(len(stripes_by_len) - 1, len(next_s))
        return total_possible_combos(next_s, next_c) + total_possible_combos(s, c - 1)
    else:
        return total_possible_combos(s, c - 1)


def is_design_possible(s: str, sbl: list[set], c: int) -> bool:
    if not s:
        return True

    if c == 0:
        return False

    sub = s[:c]
    if sub in sbl[c]:
        next_s = s[c:]
        next_c = min(len(sbl) - 1, len(next_s))
        return is_design_possible(next_s, sbl, next_c) or is_design_possible(
            s, sbl, c - 1
        )
    else:
        return is_design_possible(s, sbl, c - 1)


total_possible = 0
for d in designs:
    if is_design_possible(d, stripes_by_len, max_len):
        total_possible += 1
print(total_possible)

total = 0
for d in designs:
    total += total_possible_combos(d, max_len)
print(total)
