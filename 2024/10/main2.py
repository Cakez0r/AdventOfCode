from aoc import TextGrid

grid = TextGrid.from_file("input.txt")


def connected(g, x, y):
    try:
        return int(g[y]) - int(g[x]) == 1 and abs(y[0] - x[0]) + abs(y[1] - x[1]) == 1
    except:
        return False


roots = grid.find_all("0")
count = 0
part2 = False
for r in roots:
    for x, y, v in grid.dfs(*r, connected, acyclic=part2):
        if v == "9":
            count += 1

print(count)
