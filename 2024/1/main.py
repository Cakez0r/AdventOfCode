import math

l = []
r = []
# 16435   48069
rdict = dict()
with open("input.txt") as f:
    for line in f.readlines():
        split = line.split('   ')
        l.append(int(split[0]))
        rnum = int(split[1])
        r.append(rnum)
        if rnum in rdict:
            rdict[rnum] += 1
        else:
            rdict[rnum] = 1

l.sort()
r.sort()

sum = 0
simscore = 0
for i in range(len(l)):
    a = l[i]
    b = r[i]
    d = 0
    if a > b:
        d = a - b
    else:
        d = b - a
    sum += d

    if a in rdict:
        simscore += a * rdict[a]

print(sum)
print(simscore)
