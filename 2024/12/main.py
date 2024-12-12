from aoc import Direction, TextGrid, Point


# 0 = 80
# 2 = 1206
# 3 = 436
# 4 = 236
# 5 = 368
# 6 = 368
grid = TextGrid.from_file("input.txt")

visited = set()


def same_region(g, p1, p2):
    return 1 if g[p1] == g[p2] else None


dirs = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]


def get_neighbours(grid: TextGrid, p: Point):
    return [d.apply(p) for d in dirs]


total_cost = 0
total_cost2 = 0
for y in range(grid.height):
    for x in range(grid.width):
        if (x, y) in visited:
            continue

        area = 0
        sides = list()
        perimiter = set()
        region = set()
        for rv, (rx, ry) in grid.dfs(
            (x, y), same_region, get_neighbours=get_neighbours
        ):
            visited.add((rx, ry))
            region.add((rx, ry))
            neighbours = grid.adjacent_neighbours((rx, ry), True)
            for n in neighbours:
                perimiter.add(n)
                if grid[n] != rv:
                    if n[0] == rx or n[1] == ry:
                        sides.append(n)
            area += 1

        perimiter.difference_update(region)
        corners = 0
        for v in perimiter:
            for sd in dirs:
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
