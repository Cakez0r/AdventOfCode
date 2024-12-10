from collections import deque
from enum import Enum
from typing import Callable, Iterable, Iterator, Optional
import os

p_cache: dict[int, list[int]] = dict()


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
    def cw(cls, start: "Direction") -> Iterable["Direction"]:
        all = cls.all()
        all.rotate(-all.index(start))
        return all

    @classmethod
    def ccw(cls, start: "Direction") -> Iterable["Direction"]:
        all = cls.all()
        all.rotate(-all.index(start) - 1)
        return reversed(all)

    def apply(self, point: tuple[int, int]) -> tuple[int, int]:
        return (point[0] + self.value[0], point[1] + self.value[1])


class TextGrid:
    lines: tuple[str]
    width: int
    height: int

    def __init__(self, lines: list[str], strip: bool = True):
        self.lines = [l.strip() for l in lines] if strip else lines

        if not all(len(l) == len(self.lines[0]) for l in self.lines):
            raise Exception("Bad shape")

        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def find_all(self, char: str) -> list[tuple[int, int]]:
        results = []

        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] == char:
                    results.append((x, y))

        return results

    def _search(
        self,
        start_x: int,
        start_y: int,
        is_connected: Callable[["TextGrid", tuple[int, int], tuple[int, int]], bool],
        popper: Callable[[deque[tuple[int, int]]], tuple[int, int]],
        get_neighbours: Callable[["TextGrid", tuple[int, int]], list[tuple[int, int]]],
        acyclic: bool = False,
    ) -> Iterator[tuple[int, int, str]]:
        visited = set()
        s = deque([(start_x, start_y)])

        while s:
            cur = popper(s)
            visited.add(cur)
            yield cur[0], cur[1], self[cur]
            neighbours = get_neighbours(self, cur)
            for n in neighbours:
                if (
                    self[n] != None
                    and (n not in visited or acyclic)
                    and is_connected(self, cur, n)
                ):
                    s.append(n)

    def adjacent_neighbours(self, p: tuple[int, int]):
        return [d.apply(p) for d in Direction.all() if self[p] != None]

    def dfs(
        self,
        start_x: int,
        start_y: int,
        is_connected: Callable[["TextGrid", tuple[int, int], tuple[int, int]], bool],
        acyclic: bool = False,
        get_neighbours: Callable[
            ["TextGrid", tuple[int, int]], list[tuple[int, int]]
        ] = adjacent_neighbours,
    ) -> Iterator[tuple[int, int, str]]:
        return self._search(
            start_x, start_y, is_connected, deque.pop, get_neighbours, acyclic
        )

    def bfs(
        self,
        start_x: int,
        start_y: int,
        is_connected: Callable[["TextGrid", tuple[int, int], tuple[int, int]], bool],
        acyclic: bool = False,
        get_neighbours: Callable[
            ["TextGrid", tuple[int, int]], list[tuple[int, int]]
        ] = adjacent_neighbours,
    ) -> Iterator[tuple[int, int, str]]:
        return self._search(
            start_x, start_y, is_connected, deque.popleft, get_neighbours, acyclic
        )

    def find(self, char: str) -> Optional[tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] == char:
                    return (x, y)

    @classmethod
    def from_file(cls, path: str, strip: bool = True) -> "TextGrid":
        with open(path) as f:
            lines = f.readlines()
            return cls(lines)

    def __getitem__(self, index: tuple[int, int]) -> Optional[str]:
        try:
            if index[0] >= 0 and index[1] >= 0:
                return self.lines[index[1]][index[0]]
        except:
            pass

    def __setitem__(self, index: tuple[int, int], val: str) -> Optional[str]:
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
