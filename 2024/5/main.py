ordering = []
updates = []

with open("ordering.txt") as f:
    lines = f.readlines()
    ordering = [(int(t.split('|')[0]), int(t.split('|')[1])) for t in  lines]

with open("updates.txt") as f:
    lines = f.readlines()
    updates = [[int(i) for i in t.split(',')] for t in lines]
    

order_dict = dict()
for o in ordering:
    if o[0] not in order_dict:
        order_dict[o[0]] = set()

    order_dict[o[0]].add(o[1])

def is_in_order(u: list[int]) -> bool:
    for i in range(len(u)):
        p = u[i]
        if p in order_dict:
            after = set(u[i+1:])
            violations = order_dict[p].intersection(u).difference(after)
            if violations:
                return False

    return True

def fix_order(u: list[int]) -> list[int]:
    while not is_in_order(u):
        for i in range(len(u)):
            p = u[i]
            if p in order_dict:
                after = set(u[i+1:])
                violations = order_dict[p].intersection(u).difference(after)
                if violations:
                    min = 999999999999
                    for v in violations:
                        idx = u.index(v)
                        if idx < min:
                            min = idx
                    
                    u = u[:i] + u[i+1:]
                    u = u[:idx] + [p] + u[idx:]

    return u


sum = 0
bad_sum = 0
for u in updates:
    if is_in_order(u):
        mid = u[int(len(u) / 2)]
        sum += mid
    else:
        # 75,97,47,61,53 becomes 97,75,47,61,53.
        # 61,13,29 becomes 61,29,13.
        # 97,13,75,29,47 becomes 97,75,47,29,13.
        fixed =fix_order(u)
        mid = fixed[int(len(fixed) / 2)]
        bad_sum += mid

print(bad_sum)