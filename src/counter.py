f = file('nn4-b1.txt')

lines = []

for l in f:
    lines.append(l)

step = 28
last_step = 0
cursor = 0

w = 0
d = 0
l = 0

while cursor < len(lines):
    line = lines[cursor]
    try:
        r = int(line[:2])
        if r == 1:
            w += 1
        elif r == 0:
            d += 1
        elif r == -1:
            l += 1
        cursor += 1
    except ValueError, e:
        print cursor, "\t", 
        print w, "\t", d, "\t", l
        w = 0
        d = 0
        l = 0
        last_step += step
        cursor = last_step
        continue
