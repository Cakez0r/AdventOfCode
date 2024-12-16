from collections import defaultdict, deque
from functools import partial
import heapq
from typing import Optional
from aoc import Direction, TextGrid, Point, Vector, PathWeightFunc, NeighbourFunc


grid = TextGrid.from_file("input.txt")

start = grid.find("S")
end = grid.find("E")


def shortest_path(
    g: TextGrid,
    p1: Point,
    p2: Point,
) -> Optional[tuple[int, deque[Point]]]:
    distance = defaultdict(lambda: float("inf"))
    distance[p1] = 0
    parents = dict()
    facing = Direction.EAST.value

    q = [(0, p1, facing)]
    while q:
        cur_weight, cur, cur_facing = heapq.heappop(q)
        if cur == p2:
            break

        if cur_weight > distance[cur]:
            continue

        neighbours = g.get_neighbours(cur, Direction.cardinal())
        for n in neighbours:
            if g[n] == "#":
                continue

            diff = Vector(n) - cur
            weight = 1 if diff == cur_facing else 1001
            weight += distance[cur]

            if weight < distance[n]:
                distance[n] = weight
                parents[n] = cur
                heapq.heappush(q, (weight, n, diff))

    if p2 not in parents:
        return None

    path = deque()
    path.appendleft(p2)
    back = p2
    while (back := parents[back]) != p1:
        path.appendleft(back)

    return distance[p2], path


def find_all_tiles_on_path(
    g: TextGrid, p1: Point, p2: Point, best_weight: int
) -> Optional[tuple[int, deque[Point]]]:
    distance = defaultdict(lambda: float("inf"))
    distance[p1] = 0
    parents = dict()
    facing = Direction.EAST.value
    all_tiles_on_path = set()
    all_tiles_on_path.add(p2)

    q = deque([(0, p1, facing)])
    while q:
        cur_weight, cur, cur_facing = q.pop()
        if cur == p2 and distance[p2] == best_weight:
            back = p2
            while back in parents:
                back = parents[back]
                all_tiles_on_path.add(back)

            distance = defaultdict(lambda: float("inf"))
            for n in q:
                distance[n[1]] = n[0]
            parents = dict()
            continue

        if cur_weight > distance[cur]:
            continue

        neighbours = g.get_neighbours(cur, Direction.cardinal())
        for n in neighbours:
            if g[n] == "#":
                continue

            diff = Vector(n) - cur
            weight = 1 if diff == cur_facing else 1001
            weight += distance[cur]

            if weight <= distance[n] and weight <= best_weight:
                distance[n] = weight
                parents[n] = cur
                q.append((weight, n, diff))

    return all_tiles_on_path


path = shortest_path(grid, start, end)
all_tiles = find_all_tiles_on_path(grid, start, end, path[0])

print(path[0])  # Part 1
print(len(all_tiles))  # 538 - Part 2
