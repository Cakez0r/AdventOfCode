from collections import defaultdict
from itertools import combinations


g: dict[str, set[str]] = defaultdict(set)

with open("input.txt") as f:
    for l in f.readlines():
        l = l.strip()
        split = l.split("-")
        g[split[0]].add(split[1])
        g[split[1]].add(split[0])


# result = set()
# for c in combinations(g, 3):
#     if c[0][0] == "t" or c[1][0] == "t" or c[2][0] == "t":
#         if c[0] in g[c[1]] and c[1] in g[c[2]] and c[2] in g[c[0]]:
#             # print(c)
#             result.add(c)
# # part 1
# print(len(result))


def all_connected(c) -> bool:
    for c1 in c:
        for c2 in c:
            if c1 == c2:
                continue

            if c1 not in g[c2]:
                return False

    return True


c_min = 2
for c in sorted(g, key=lambda k: len(g[k]), reverse=True):
    c_all = list(g[c])
    c_all.append(c)
    c_len = len(c_all)
    for choose in range(c_min, len(c_all)):
        for c2 in combinations(c_all, choose):
            if all_connected(c2):
                if choose >= c_min:
                    c_min = choose + 1

                # Part 2
                print(",".join(sorted(c2)))
                break
