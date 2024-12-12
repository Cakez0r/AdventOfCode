from collections import defaultdict, deque
from enum import Enum
import heapq
from typing import Callable, Iterable, Iterator, Optional, TypeVar
import os

T = TypeVar("T")

p_cache: dict[int, list[int]] = dict()

Point = tuple[int, int]
PathWeightFunc = Callable[["TextGrid", Point, Point], Optional[int]]
NeighbourFunc = Callable[["TextGrid", Point], list[Point]]


class Direction(Enum):
    NORTH = (0, -1)
    NORTH_EAST = (1, -1)
    EAST = (1, 0)
    SOUTH_EAST = (1, 1)
    SOUTH = (0, 1)
    SOUTH_WEST = (-1, 1)
    WEST = (-1, 0)
    NORTH_WEST = (-1, -1)

    @classmethod
    def all(cls) -> deque["Direction"]:
        return deque(
            [
                cls.NORTH,
                cls.NORTH_EAST,
                cls.EAST,
                cls.SOUTH_EAST,
                cls.SOUTH,
                cls.SOUTH_WEST,
                cls.WEST,
                cls.NORTH_WEST,
            ]
        )

    @classmethod
    def cardinal(cls) -> deque["Direction"]:
        return deque(
            [
                cls.NORTH,
                cls.EAST,
                cls.SOUTH,
                cls.WEST,
            ]
        )

    @classmethod
    def intercardinal(cls) -> deque["Direction"]:
        return deque(
            [
                cls.NORTH_EAST,
                cls.SOUTH_EAST,
                cls.SOUTH_WEST,
                cls.NORTH_WEST,
            ]
        )

    @classmethod
    def cw(cls, start: "Direction") -> Iterable["Direction"]:
        all = cls.all()
        all.rotate(-all.index(start))
        return all

    @classmethod
    def ccw(cls, start: "Direction") -> Iterable["Direction"]:
        all = cls.all()
        all.rotate(-all.index(start) - 1)
        return reversed(all)

    def apply(self, point: Point) -> Point:
        return (point[0] + self.value[0], point[1] + self.value[1])


class TextGrid:
    lines: list[str]
    width: int
    height: int

    def __init__(self, lines: list[str], strip: bool = True):
        self.lines = [l.strip() for l in lines] if strip else lines

        if not all(len(l) == len(self.lines[0]) for l in self.lines):
            raise Exception("Bad shape")

        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def find_all(self, char: str) -> list[Point]:
        results = []

        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] == char:
                    results.append((x, y))

        return results

    def get_neighbours(
        self,
        p: Point,
        directions: Iterable[Direction] = Direction.all(),
        include_none: bool = False,
    ):
        return [
            d.apply(p) for d in directions if include_none or self[d.apply(p)] != None
        ]

    def _search(
        self,
        start: Point,
        get_weight: PathWeightFunc,
        popper: Callable[[deque[Point]], Point],
        get_neighbours: NeighbourFunc = get_neighbours,
        acyclic: bool = False,
    ) -> Iterator[tuple[str, Point]]:
        visited = set()
        s = deque([start])

        while s:
            cur = popper(s)
            if cur in visited and not acyclic:
                continue

            visited.add(cur)
            yield self[cur], (cur[0], cur[1])
            neighbours = get_neighbours(self, cur)
            for n in neighbours:
                if (
                    self[n] != None
                    and (n not in visited or acyclic)
                    and get_weight(self, cur, n) is not None
                ):
                    s.append(n)

    def dfs(
        self,
        start: Point,
        get_weight: PathWeightFunc,
        acyclic: bool = False,
        get_neighbours: NeighbourFunc = get_neighbours,
    ) -> Iterator[tuple[str, Point]]:
        return self._search(start, get_weight, deque.pop, get_neighbours, acyclic)

    def bfs(
        self,
        start: Point,
        get_weight: PathWeightFunc,
        acyclic: bool = False,
        get_neighbours: NeighbourFunc = get_neighbours,
    ) -> Iterator[tuple[str, Point]]:
        return self._search(start, get_weight, deque.popleft, get_neighbours, acyclic)

    def shortest_path(
        self,
        p1: Point,
        p2: Point,
        get_weight: PathWeightFunc,
        get_neighbours: NeighbourFunc = get_neighbours,
        heuristic: PathWeightFunc = None,
    ) -> Optional[tuple[int, deque[Point]]]:
        distance = defaultdict(lambda: float("inf"))
        distance[p1] = 0
        parents = dict()

        q = [(0, p1)]
        while q:
            cur_weight, cur = heapq.heappop(q)
            if cur == p2:
                break

            if cur_weight > distance[cur]:
                continue

            neighbours = get_neighbours(self, cur)
            for n in neighbours:
                weight = get_weight(self, cur, n)
                if weight is None:
                    continue

                weight += distance[cur]
                if heuristic:
                    weight += heuristic(self, cur, p2)

                if weight < distance[n]:
                    distance[n] = weight
                    parents[n] = cur
                    heapq.heappush(q, (weight, n))

        if p2 not in parents:
            return None

        path = deque()
        path.appendleft(p2)
        back = p2
        while (back := parents[back]) != p1:
            path.appendleft(back)

        return distance[p2], path

    def find(self, char: str) -> Optional[Point]:
        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] == char:
                    return (x, y)

    @classmethod
    def from_file(cls, path: str, strip: bool = True) -> "TextGrid":
        with open(path) as f:
            lines = f.readlines()

            return cls(lines, strip)

    def __getitem__(self, index: Point) -> Optional[str]:
        try:
            if index[0] >= 0 and index[1] >= 0:
                return self.lines[index[1]][index[0]]
        except:
            pass

    def __setitem__(self, index: Point, val: str) -> Optional[str]:
        ret = None
        try:
            if (
                index[0] >= 0
                and index[1] >= 0
                and index[0] < self.width
                and index[1] < self.height
            ):
                l = self.lines[index[1]]
                self.lines[index[1]] = l[: index[0]] + val + l[index[0] + 1 :]
        except:
            pass

    def __str__(self):
        s = ""

        for l in self.lines:
            s += l + os.linesep

        return s


def try_or_default(fn: Callable[[], T], default: T) -> T:
    try:
        return fn()
    except:
        return default


def permute(choose: int, base: int) -> list[list[int]]:
    if choose in p_cache:
        return p_cache[choose]

    result = []
    for counter in range(pow(base, choose)):
        p = [0] * choose

        i = 0
        current = counter
        p[i] = current % base
        while current >= base:
            current = int(current / base)
            i += 1
            p[i] = current % base

        result.append(p)

    p_cache[choose] = result

    return result
