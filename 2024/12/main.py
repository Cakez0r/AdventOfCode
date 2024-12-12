from functools import partial
from aoc import Direction, TextGrid, Point


grid = TextGrid.from_file("input.txt")
visited = set()
total_cost = 0
total_cost2 = 0


def same_region(g, p1, p2):
    return 1 if g[p1] == g[p2] else None


for y in range(grid.height):
    for x in range(grid.width):
        if (x, y) in visited:
            continue

        area = 0
        sides = list()
        perimiter = set()
        region = set()
        for rv, (rx, ry) in grid.dfs(
            (x, y),
            same_region,
            get_neighbours=partial(
                TextGrid.get_neighbours, directions=Direction.cardinal()
            ),
        ):
            visited.add((rx, ry))
            region.add((rx, ry))
            neighbours = grid.get_neighbours((rx, ry), include_none=True)
            for n in neighbours:
                perimiter.add(n)
                if grid[n] != rv:
                    if n[0] == rx or n[1] == ry:
                        sides.append(n)
            area += 1

        perimiter.difference_update(region)
        corners = 0
        for v in perimiter:
            for sd in Direction.cardinal():
                cd = Direction.cw(sd)
                p1 = cd[0].apply(v)
                p2 = cd[1].apply(v)
                p3 = cd[2].apply(v)
                if p1 in perimiter and p2 in region and p3 in perimiter:
                    corners += 1
                elif p1 in region and p2 in perimiter and p3 in region:
                    corners += 1
                elif p1 in region and p2 in region and p3 in region:
                    corners += 1

        total_cost += area * len(sides)
        total_cost2 += area * corners

        print(f"{grid[x,y]}: {area} * {corners} = {area*corners}")

print(total_cost)
print(total_cost2)
