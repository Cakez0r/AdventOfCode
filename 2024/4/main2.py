combos = set([
    ('M', 'M', 'S', 'S'),
    ('M', 'S', 'S', 'M'),
    ('S', 'S', 'M', 'M'),
    ('S', 'M', 'M', 'S'),
])

with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    xmax = len(lines[0])
    ymax = len(lines)

    count = 0
    for x in range(1, xmax):
        for y in range(1,ymax):
            if lines[y][x] != 'A':
                continue
            try:
                layout = (lines[y-1][x-1], lines[y-1][x+1], lines[y+1][x+1], lines[y+1][x-1])

                if layout in combos:
                    count += 1
            except:
                pass
    print(count) 