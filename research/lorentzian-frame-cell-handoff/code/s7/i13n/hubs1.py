from part13 import *
import collections
frames = sorted(set(d[1] for d in DEM))
print('distinct demand frames', len(frames))
cand = collections.Counter()
for i in range(len(frames)):
    for j in range(i + 1, len(frames)):
        x = frames[i] & frames[j]
        if pc(x) >= 6: cand[x] += 1
print('distinct pairwise intersections (>=6 lines)', len(cand))
# users per candidate: demands whose frame contains the hub lines and meet E
res = []
for A in cand:
    us = [k for k, d in enumerate(DEM) if A & ~d[1] == 0 and A & d[2]]
    res.append((pc(A), len(us), sum(pc(A & DEM[k][2]) for k in us), A))
res.sort(key=lambda r: -r[1] / r[0])
print('top hubs by users/size (size, users, delivered incidences):')
for r in res[:30]: print('  ', r[:3], 'rank', rk(r[3]))
dist = collections.Counter((r[0], r[1]) for r in res)
print('size-users histogram (top):', dist.most_common(40))
pickle.dump(res, open('hubs1.pkl', 'wb'))
