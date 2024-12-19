from functools import partial
from aoc import Direction, TextGrid, Vector

W = 71
H = 71
C = 1024

grid = TextGrid(["." * W] * H, False)

with open("input.txt") as f:
    lines = [l.strip().split(",") for l in f.readlines()]
    coords = [Vector((int(l[0]), int(l[1]))) for l in lines]

    for i in range(C):
        grid[coords[i]] = "#"

    path = grid.shortest_path(
        (0, 0),
        (W - 1, H - 1),
        lambda g, p1, p2: 1 if g[p2] == "." else None,
        partial(TextGrid.get_neighbours, directions=Direction.cardinal()),
    )

    print(path[0])  # Part 1

    grid = TextGrid(["." * W] * H, False)
    for i in range(len(coords)):
        print(f"{i} / {len(coords)}")
        grid[coords[i]] = "#"
        path = grid.shortest_path(
            (0, 0),
            (W - 1, H - 1),
            lambda g, p1, p2: 1 if g[p2] == "." else None,
            partial(TextGrid.get_neighbours, directions=Direction.cardinal()),
        )

        if not path:
            print(f"*** {i}: {coords[i]} ***")
            break
