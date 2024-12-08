from typing import Final

from textgrid import TextGrid


dirs = [
    ( 1, 0),
    ( 1, 1),
    ( 0, 1),
    (-1, 1),
    (-1, 0),
    (-1,-1),
    ( 0,-1),
    ( 1,-1),
]

test = TextGrid.from_file("input.txt")
print(test[2,0])

with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    tg = TextGrid(lines)
    print(tg[2, 0])
    # lines = f.readlines()
    xmax = len(lines[0])
    ymax = len(lines)
    word = 'XMAS'

    count = 0
    for x in range(xmax):
        for y in range(ymax):
            if lines[y][x] != word[0]:
                continue

            for d in dirs:
                match = True
                for i in range(len(word)):
                    try:
                        _x = x+i*d[1]
                        _y = y+i*d[0]
                        if lines[_y][_x] != word[i] or _x < 0 or _y < 0:
                            match = False
                            break
                    except:
                        match = False
                        break
                if match:
                    count += 1
    print(count) 