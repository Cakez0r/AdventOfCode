from aoc import permute


ops = [
    lambda x, y: x + y,
    lambda x, y: x * y,
    lambda x, y: int(str(x) + str(y)),
]

BASE = 3

def apply_ops(nums, p):
    accum = split[0]

    for p_index in range(len(p)):
        accum = ops[p[p_index]](accum, nums[p_index+1])
    
    return accum

with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]

    sum = 0
    c = 0
    for l in lines:
        split = l.split(': ')
        target = int(split[0])
        split = [int(x) for x in split[1].split(' ')]
        print(c, " / ", len(lines), ": ", len(split))
        permutations = permute(len(split)-1, BASE)
        for p in permutations:
            res = apply_ops(split, p)
            if res == target:
                sum += target
                print(sum)
                break
        c += 1
    
    print(sum)
        
# 4998784546369