from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from aoc import Direction, TextGrid, Point


grid = TextGrid.from_file("input.txt")
CHEAT_LENGTH = 20


def get_weight(g, p1, p2):
    return manhattan_distance(p1, p2) if g[p2] != "#" else None


def manhattan_distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def manhattan_heuristic(g, p1, p2):
    return manhattan_distance(p1, p2)


def get_cardinal_neighbours(g: TextGrid, p):
    return g.get_neighbours(p, Direction.cardinal())


def all_connected(g: TextGrid, p1: Point, p2: Point):
    return 1


def get_cheatable_neighbours(g: TextGrid, p1: Point, known_cheats: set[Point, Point]):
    neighbours = []
    for x in range(-CHEAT_LENGTH, CHEAT_LENGTH + 1):
        for y in range(-CHEAT_LENGTH, CHEAT_LENGTH + 1):
            p2 = (p1[0] + x, p1[1] + y)
            if (p1, p2) in known_cheats or (p2, p1) in known_cheats or p1 == p2:
                continue

            if manhattan_distance(p1, p2) <= CHEAT_LENGTH and (
                g[p2] == "." or g[p2] == "E" or g[p2] == "S"
            ):
                # This check does make things a bit faster, but doesn't move the needle that much
                # sp = g.shortest_path(p1, p2, all_connected, get_cardinal_neighbours)
                # if sp and len(sp[1]) > 1 and g[sp[1][0]] == "#":
                #     neighbours.append(p2)

                neighbours.append(p2)

    return neighbours


def get_neighbours_with_cheat(g: TextGrid, p1: Point, cheat_p1: Point, cheat_p2: Point):
    neighbours = g.get_neighbours(p1, Direction.cardinal())

    if p1 == cheat_p1:
        neighbours.append(cheat_p2)

    elif p1 == cheat_p2:
        neighbours.append(cheat_p1)

    return neighbours


def find_cheats(g: TextGrid) -> Counter:
    count = Counter()
    start = g.find("S")
    end = g.find("E")

    walls = set(g.find_all("#"))

    try:
        for i in range(g.width):
            walls.remove((i, 0))
            walls.remove((i, g.height - 1))

        for i in range(g.height):
            walls.remove((0, i))
            walls.remove((g.width - 1, i))
    except KeyError:
        pass

    baseline = g.shortest_path(
        start, end, get_weight, get_cardinal_neighbours, manhattan_heuristic
    )

    i = 0
    for w in walls:
        i += 1
        print(f"{i} / {len(walls)}")
        grid[w] = "."

        cheat_path = g.shortest_path(
            start, end, get_weight, get_cardinal_neighbours, manhattan_heuristic
        )

        saving = len(baseline[1]) - len(cheat_path[1])
        if saving > 0:
            count[saving] += 1

        grid[w] = "#"

    return count


def cheat_test(
    cheat: tuple[Point, Point],
    g: TextGrid,
    start: Point,
    end: Point,
) -> int:
    cheat_neighbours_fn = partial(
        get_neighbours_with_cheat, cheat_p1=cheat[0], cheat_p2=cheat[1]
    )

    cheat_path = g.shortest_path(start, end, get_weight, cheat_neighbours_fn)

    return cheat_path[0]


def find_cheats2(g: TextGrid) -> Counter:
    start = g.find("S")
    end = g.find("E")

    baseline = g.shortest_path(
        start,
        end,
        get_weight,
        partial(TextGrid.get_neighbours, directions=Direction.cardinal()),
    )

    cheat_combos = set()
    dots = g.find_all(".")
    dots.append(start)
    dots.append(end)
    i = 0
    for d in dots:
        i += 1
        print(f"{i} / {len(dots)}")
        cn = get_cheatable_neighbours(g, d, cheat_combos)
        for c in cn:
            cheat_combos.add((c, d))

    i = 0
    with ProcessPoolExecutor() as pool:
        results = pool.map(
            partial(cheat_test, g=g, start=start, end=end),
            cheat_combos,
            chunksize=500,
        )

        c = 0
        last_pct = 0
        for r in results:
            i += 1
            pct = int((i / len(cheat_combos)) * 1000)
            if pct > last_pct:
                print(f"[{pct/10}%] {i} / {len(cheat_combos)}")
                last_pct = pct
            saving = baseline[0] - r
            if saving > 0:
                c += 1

        return c


# part1 = find_cheats(grid)
# for k, v in sorted(part1.items()):
#     print(f"{k}: {v}")

# print(sum(c[1] for c in part1.items() if c[0] >= 100))

part2 = find_cheats2(grid)
print(part2)
