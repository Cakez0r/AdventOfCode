from typing import Counter


with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]

    sum = 0
    sum2 = 0
    for l in lines:
        id, sets = l[5:].split(": ")
        ok = True

        min_r = 0
        min_g = 0
        min_b = 0
        for s in sets.split("; "):
            counter = Counter()
            counter.update(
                {
                    k: int(v)
                    for v, k in map(lambda split: split.split(" "), s.split(", "))
                }
            )

            if counter["red"] > min_r:
                min_r = counter["red"]
            if counter["green"] > min_g:
                min_g = counter["green"]
            if counter["blue"] > min_b:
                min_b = counter["blue"]

            # if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.
            if counter["red"] > 12 or counter["green"] > 13 or counter["blue"] > 14:
                ok = False

        if ok:
            sum += int(id)

        sum2 += min_r * min_g * min_b

print(sum)
print(sum2)
