from functools import reduce
from PIL import Image
import operator
import os

from aoc import TextGrid


W = 101
H = 103
STEPS = 10_000

pos = []
vel = []


def step():
    for i in range(len(pos)):
        p = pos[i]
        v = vel[i]

        pos[i] = ((p[0] + v[0]) % W, (p[1] + v[1]) % H)


def safety_factor():
    quadrants = [0, 0, 0, 0]
    mid_x = int(W / 2)
    mid_y = int(H / 2)
    for p in pos:
        if p[0] < mid_x and p[1] < mid_y:
            quadrants[0] += 1
        if p[0] > mid_x and p[1] < mid_y:
            quadrants[1] += 1
        if p[0] < mid_x and p[1] > mid_y:
            quadrants[2] += 1
        if p[0] > mid_x and p[1] > mid_y:
            quadrants[3] += 1

    return reduce(operator.mul, quadrants)


def print_grid():
    grid = TextGrid([" " * W] * H, False)
    for p in pos:
        assert p[0] < W
        assert p[1] < H
        grid[p] = "*"
    print(grid)


def create_image(i):
    with Image.new("RGB", (W, H), "white") as img:
        pixels = img.load()
        for p in pos:
            pixels[p] = (0, 0, 0)
        img.save(f"imgs/{i}.png")


with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]

    for l in lines:
        pvs = l.split(" ")
        ps = pvs[0][2:].split(",")
        vs = pvs[1][2:].split(",")
        p = (int(ps[0]), int(ps[1]))
        v = (int(vs[0]), int(vs[1]))
        pos.append(p)
        vel.append(v)

    for i in range(1, STEPS):
        step()
        create_image(i)

        if i == 8087:
            os.system("clear")
            print(i + 1, ": ")
            print_grid()
            input()

    print(safety_factor())
