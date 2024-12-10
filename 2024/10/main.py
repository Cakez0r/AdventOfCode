from collections import deque
from aoc import TextGrid

def gather_eligible_neighbours(grid: TextGrid, pos: tuple[int, int]) -> list[tuple[int, int]]:
    neighbours = []
    eligible_score = int(grid[pos[0], pos[1]]) + 1
    try:
        if int(grid[pos[0]-1, pos[1]]) == eligible_score:
            neighbours.append((pos[0]-1, pos[1]))
    except:
        pass

    try:
        if int(grid[pos[0]+1, pos[1]]) == eligible_score:
            neighbours.append((pos[0]+1, pos[1]))
    except:
        pass

    try:
        if int(grid[pos[0], pos[1]-1]) == eligible_score:
            neighbours.append((pos[0], pos[1]-1))
    except:
        pass

    try:
        if int(grid[pos[0], pos[1]+1]) == eligible_score:
            neighbours.append((pos[0], pos[1]+1))
    except:
        pass

    return neighbours

def find_routes(grid: TextGrid, start: tuple[int, int]):
    reachable = list()
    q = deque([start])

    while q:
        cur = q.pop()

        cur_char = grid[cur[0], cur[1]]
        if cur_char == '9':
            reachable.append(cur)
        
        neighbours = gather_eligible_neighbours(grid, cur)

        for n in neighbours:
            q.append(n)

    return reachable

def find_reachable_nines(grid: TextGrid, start: tuple[int, int]):
    reachable = set()
    visited = set()
    q = deque([start])

    while q:
        cur = q.pop()

        visited.add(cur)

        cur_char = grid[cur[0], cur[1]]
        if cur_char == '9':
            reachable.add(cur)
        
        neighbours = gather_eligible_neighbours(grid, cur)

        for n in neighbours:
            if n not in visited:
                q.append(n)

    return reachable


grid = TextGrid.from_file("input.txt")
heads = grid.find_all('0')

score = 0
for h in heads:
    r = find_routes(grid, h)
    score += len(r)

print(score)