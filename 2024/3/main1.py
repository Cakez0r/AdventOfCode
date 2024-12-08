import re
with open('input.txt') as f:
    text = f.read()

    matches = re.findall('mul\\([0-9]{1,3},[0-9]{1,3}\\)|do\\(\\)|don\'t\\(\\)', text)
    sum = 0
    enabled = True
    for m in matches:
        if m == 'do()':
            enabled = True
        elif m == 'don\'t()':
            enabled = False
        else:
            if enabled:
                nums = m.replace('mul(','').replace(')', '').split(',')
                sum += int(nums[0]) * int(nums[1])
    print(sum)