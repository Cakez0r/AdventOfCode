from aoc import Direction, TextGrid, Point


dirs = {
    "^": Direction.NORTH,
    ">": Direction.EAST,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
}


def read_moves(path: str) -> str:
    with open(path) as f:
        return "".join([l.strip() for l in f.readlines()])


def widen(grid: TextGrid) -> TextGrid:
    ng = TextGrid([" " * grid.width * 2] * grid.height, False)

    for x in range(grid.width):
        for y in range(grid.height):
            val = grid[x, y]
            if val == "#":
                ng[x * 2, y] = "#"
                ng[x * 2 + 1, y] = "#"
            elif val == ".":
                ng[x * 2, y] = "."
                ng[x * 2 + 1, y] = "."
            elif val == "O":
                ng[x * 2, y] = "["
                ng[x * 2 + 1, y] = "]"
            elif val == "@":
                ng[x * 2, y] = "@"
                ng[x * 2 + 1, y] = "."

    return ng


def find_free_space(grid: TextGrid, pos: Point, dir: Direction):
    while val := grid[pos]:
        if val == ".":
            return pos
        elif val == "#":
            return None

        pos = dir.apply(pos)

    raise Exception("Shouldn't happen")


def push_h(grid: TextGrid, pos: Point, dir: Direction):
    initial = grid[pos]
    while val := grid[pos]:
        if val == ".":
            grid[pos] = "]" if initial == "[" else "["
            break
        elif val == "[":
            grid[pos] = "]"
        elif val == "]":
            grid[pos] = "["

        pos = dir.apply(pos)


def check_v(grid: TextGrid, pos: Point, dir: Direction) -> bool:
    p1 = grid[pos]
    p1_next_pos = dir.apply(pos)
    p1_next = grid[p1_next_pos]

    pos2 = Direction.EAST.apply(pos) if p1 == "[" else Direction.WEST.apply(pos)
    p2_next_pos = dir.apply(pos2)
    p2_next = grid[p2_next_pos]

    if p1_next == "." and p2_next == ".":
        return True
    elif p1_next == "#" or p2_next == "#":
        return False
    elif p1_next == "[" and p2_next == "]":
        return check_v(grid, p1_next_pos, dir)
    elif p1_next == "]" and p2_next == "[":
        return check_v(grid, Direction.WEST.apply(p1_next_pos), dir) and check_v(
            grid, p2_next_pos, dir
        )
    elif p1_next == "]" and p2_next == ".":
        return check_v(grid, Direction.WEST.apply(p1_next_pos), dir)
    elif p1_next == "." and p2_next == "[":
        return check_v(grid, p2_next_pos, dir)


def push_v(grid: TextGrid, pos: Point, dir: Direction):
    p1 = grid[pos]
    p1_next_pos = dir.apply(pos)
    p1_next = grid[p1_next_pos]

    pos2 = Direction.EAST.apply(pos) if p1 == "[" else Direction.WEST.apply(pos)
    p2 = grid[pos2]
    p2_next_pos = dir.apply(pos2)
    p2_next = grid[p2_next_pos]

    if p1_next == "[" and p2_next == "]":
        push_v(grid, p1_next_pos, dir)
    elif p1_next == "]" and p2_next == "[":
        push_v(grid, Direction.WEST.apply(p1_next_pos), dir)
        push_v(grid, p2_next_pos, dir)
    elif p1_next == "]" and p2_next == ".":
        push_v(grid, Direction.WEST.apply(p1_next_pos), dir)
    elif p1_next == "." and p2_next == "[":
        push_v(grid, p2_next_pos, dir)

    grid[p1_next_pos] = p1
    grid[p2_next_pos] = p2
    grid[pos] = "."
    grid[pos2] = "."


def part1():
    grid = TextGrid.from_file("sample2_map.txt")
    moves = read_moves("sample2_moves.txt")

    pos = grid.find("@")

    for i in range(len(moves)):
        m = moves[i]
        md = dirs[m]
        nextpos = md.apply(pos)
        val = grid[nextpos]

        if val == ".":
            grid[nextpos] = "@"
            grid[pos] = "."
            pos = nextpos
        elif val == "O":
            free = find_free_space(grid, nextpos, md)
            if free:
                grid[free] = "O"
                grid[nextpos] = "@"
                grid[pos] = "."
                pos = nextpos

        # print(i, ": ", m)
        # print(grid)
        # input()

    total = 0
    boxes = grid.find_all("O")
    for b in boxes:
        total += 100 * b[1] + b[0]

    print(total)


def part2():
    grid = TextGrid.from_file("input_map.txt")
    moves = read_moves("input_moves.txt")

    grid = widen(grid)
    pos = grid.find("@")
    print(grid)

    for i in range(len(moves)):
        m = moves[i]
        md = dirs[m]
        nextpos = md.apply(pos)
        val = grid[nextpos]

        if val == ".":
            grid[nextpos] = "@"
            grid[pos] = "."
            pos = nextpos
        elif val == "[" or val == "]":
            if m == "<" or m == ">":
                free = find_free_space(grid, nextpos, md)
                if free:
                    push_h(grid, nextpos, md)
                    grid[nextpos] = "@"
                    grid[pos] = "."
                    pos = nextpos
            else:
                can_move = check_v(
                    grid, nextpos if val == "[" else Direction.WEST.apply(nextpos), md
                )
                if can_move:
                    push_v(
                        grid,
                        nextpos if val == "[" else Direction.WEST.apply(nextpos),
                        md,
                    )
                    grid[nextpos] = "@"
                    grid[pos] = "."

                    pos = nextpos

        # print(i, ": ", m)
        # print(grid)

    total = 0
    boxes = grid.find_all("[")
    for b in boxes:
        total += 100 * b[1] + b[0]

    print(total)


part2()
