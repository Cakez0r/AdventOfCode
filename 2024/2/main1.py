safe_count = 0
with open('input2.txt') as f:
    for l in f.readlines():
        nums = [int(s) for s in l.split(' ')]
        diffs = []
        for i in range(len(nums) - 1):
            d = nums[i+1] - nums[i]
            diffs.append(d)

        safe_dir = all(n > 0 for n in diffs) or all(n <= 0 for n in diffs)
        safe_incr = all(abs(n) <= 3 for n in diffs)

        if safe_dir and safe_incr:
            safe_count += 1

print(safe_count)
