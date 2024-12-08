from collections import deque
from typing import Callable
from textgrid import TextGrid

class Node:
    x: int
    y: int
    connections: set

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

def find_dfs(node: Node, predicate: Callable[[Node], bool]):
    results: list[Node] = []
    stack = [node]

    while stack:
        n = stack.pop()

        if predicate(n):
            results.append(n)

        stack.extend(n.connections) 

    return results

connection_cache = dict()
def get_connections(grid: TextGrid, x: int, y: int) -> list[tuple[int,int]]:
    x = x % grid.width
    y = y % grid.height

    if (x,y) in connection_cache:
        return connection_cache[(x,y)]
    
    connections = []

    # for xo in range(-1, 2):
    #     for yo in range(-1, 2):
    #         if xo == 0 and yo == 0:
    #             continue
    #         if grid[x+xo, y+yo] == '.':
    #             connections.append(x+xo, y+yo)

    if grid[x+1,y] == '.':
        connections.append((x+1, y))

    if grid[x,y+1] == '.':
        connections.append((x,y+1))

    if grid[x-1,y] == '.':
        connections.append((x-1, y))

    if grid[x,y-1] == '.':
        connections.append((x, y-1))

    connection_cache[(x,y)] = connections
    return connections

def walk(grid: TextGrid, node: Node, max_steps: int):
    tree = { c: 1 for c in get_connections(grid, node.x, node.y) }
    for i in range(1, max_steps):
        print(i, ": ", sum(tree.values()))
        new_tree = dict()
        for x, y in tree:
            # new_tree = new_tree.union(get_connections(grid, n[0], n[1]))
            conns = get_connections(grid, x, y)
            for c in conns:
                if c not in new_tree:
                    new_tree[c] = 1
                else:
                    new_tree[c] = new_tree[c] + 1
        tree = new_tree

    return tree


grid = TextGrid.from_file("input2.txt")

start = grid.find('S')
grid[start[0], start[1]] = '.'

start_node = Node(start[0], start[1])
s = 1000
tree = walk(grid, start_node, s)

# In exactly 6 steps, he can still reach 16 garden plots.
# In exactly 10 steps, he can reach any of 50 garden plots.
# In exactly 50 steps, he can reach 1594 garden plots.
# In exactly 100 steps, he can reach 6536 garden plots.
# In exactly 500 steps, he can reach 167004 garden plots.
# In exactly 1000 steps, he can reach 668697 garden plots.
# In exactly 5000 steps, he can reach 16733044 garden plots.
print(len(tree))