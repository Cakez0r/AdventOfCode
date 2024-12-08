from collections import defaultdict
from textgrid import TextGrid


grid = TextGrid.from_file("input.txt")

antenna_locations = defaultdict(set)
antinode_locations = set()

for x in range(grid.width):
    for y in range(grid.height):
        char = grid[x,y]
        if char != '.':
            antenna_locations[char].add((x,y))

# part 1
# for freq,locs in antenna_locations.items():
#     for a in locs:
#         for b in locs:
#             if a != b:
#                 distance = (b[0] - a[0], b[1] - a[1])
#                 antinode_pos = (a[0] + distance[0]*2, a[1] + distance[1]*2)
#                 grid[antinode_pos[0], antinode_pos[1]] = '#'

# part 2
for freq,locs in antenna_locations.items():
    for a in locs:
        for b in locs:
            if a != b:
                distance = (b[0] - a[0], b[1] - a[1])
                distance_multiplier = 1
                while True:
                    antinode_pos = (a[0] + distance[0]*distance_multiplier, a[1] + distance[1]*distance_multiplier)
                    if (antinode_pos[0] < 0 or antinode_pos[1] < 0 or antinode_pos[0] >= grid.width or antinode_pos[1] >= grid.height):
                        break

                    grid[antinode_pos[0], antinode_pos[1]] = '#'
                    distance_multiplier += 1
print(grid)

antinode_count = 0
for x in range(grid.width):
    for y in range(grid.height):
        if grid[x,y] == '#':
            antinode_count += 1

print(antinode_count)