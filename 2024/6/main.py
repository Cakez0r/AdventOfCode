from collections import deque
from textgrid import TextGrid


dirmap = dict()

dirmap['^'] = 0
dirmap['>'] = 1
dirmap['v'] = 2
dirmap['<'] = 3

dirs = [
    (0,-1),
    (1,0),
    (0,1),
    (-1,0),
]

g = TextGrid.from_file("input.txt")

up = g.find('^')
right = g.find('>')
down = g.find('v')
left = g.find('<')


d = None
pos = None
if up:
    d = 0
    pos = up
elif right:
    d = 1
    pos = right
elif down:
    d = 2
    pos = down
elif left:
    d = 3
    pos = left

def step(pos, d):
    step_dir = dirs[d]
    return (pos[0]+step_dir[0],pos[1]+step_dir[1])
    
def find_missing_vert(verts):
    min_x = 999999999
    max_x = -1
    min_y = 999999999
    max_y = -1
    for v in verts:
        if v[0] < min_x:
            min_x = v[0]
        if v[1] < min_y:
            min_y = v[1]
        if v[0] > max_x:
            max_x = v[0]
        if v[1] > max_y:
            max_y = v[1]

    w = max_x - min_x
    h = max_y - min_y
    all_verts = [
        (min_x, max_y),
        (min_x, min_y),
        (max_x, min_y),
        (max_x, max_y),
    ]

    return set(all_verts).difference(verts).pop(), all_verts


def has_obstructions_all(verts):
    for i in range(4):
        f = verts[i]
        t = verts[(i+1)%4]
        if has_obstructions(f, t, i):
            return True

    return False

def has_obstructions(start, end, d):
    p = start
    while p != end:
        if g[p[0], p[1]] == '#':
            return True

        step_dir = dirs[d]
        p = (p[0]+step_dir[0],p[1]+step_dir[1])
    
    return False

def is_loop(grid, start_pos, start_dir):
    d = start_dir
    p = start_pos
    visited = set()

    while True:
        visited.add((p[0], p[1], d))
        next = step(p,d)        
        next_char = grid[next[0], next[1]]
        if next_char == '#':
            d = (d + 1) % 4
        elif next_char == None:
            break
        else:
            p = next
        
        if (p[0], p[1], d) in visited:
            return True

    return False

count = 0
possible_obstructions = 0
visited = set()
verts = deque()
sample_obs = set([
    (3,6),
    (6,7),
    (7,7),
    (1,8),
    (3,8),
    (7,9),
])
obs = []

print(is_loop(g,pos,d))

loop_count = 0
c  = 0
for x in range(g.width):
    for y in range(g.height):
        if g[x,y] == '.':
            g[x,y] = '#'
            if is_loop(g, pos, d):
                loop_count += 1
            g[x,y] = '.'
        
        c += 1
        print (c, " / ", g.width * g.height)

print(loop_count)
while True:
    next = step(pos, d)
    next_char = g[next[0], next[1]]
    if next_char == '#':
        d = (d + 1) % 4
        verts.append(pos)
        if len(verts) == 4:
            verts.popleft()
        if len(verts) == 3:
            test_pos, all_verts = find_missing_vert(verts)
            test_pos = (test_pos[0]+dirs[d][0], test_pos[1]+dirs[d][1])
            ordered_verts = []

            if g[test_pos[0],test_pos[1]] == '.' and not has_obstructions_all(all_verts):
                obs.append(test_pos)
                possible_obstructions += 1

    elif next_char == None:
        break
    else:
        visited.add(pos)
        count += 1
        pos = next

print(count)
print(len(visited)+1)
print(possible_obstructions)


