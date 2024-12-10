from aoc import TextGrid

grid = TextGrid.from_file("input.txt")


def get_weight(g, p1, p2):
    try:
        return (
            1
            if int(g[p2]) - int(g[p1]) == 1
            and abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]) == 1
            else None
        )
    except:
        return False


roots = grid.find_all("0")
count = 0
part2 = False
for r in roots:
    for v, (x, y) in grid.dfs(r, get_weight, acyclic=part2):
        if v == "9":
            count += 1

print(count)
