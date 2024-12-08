from typing import List


safe_count = 0

def is_safe(nums: List[int]) -> bool:
    asc = nums[1] > nums[0]
    for i in range(len(nums) - 1):
        a = nums[i]
        b = nums[i+1]
        d = b - a
        if d == 0 or abs(d) > 3 or (asc and d < 0) or (not asc and d > 0):
            return False
        
    return True


with open('input.txt') as f:
    safe_count = 0 
    removed = False

    for l in f.readlines():
        perms = []
        nums = [int(s) for s in l.split(' ')]
        perms.append(nums)
        for i in range(len(nums)):
            perms.append(nums[:i] + nums[i+1:])
        if any(is_safe(p) for p in perms):
            safe_count += 1

    print(safe_count)
