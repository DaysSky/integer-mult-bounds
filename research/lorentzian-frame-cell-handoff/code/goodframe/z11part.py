import sys, itertools, pickle, numpy as np, random
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
def shift(i, s=1):
    k, sup = g.kind[i], g.supp[i]
    return g.idx[(k, tuple(sorted((x + s) % 11 for x in sup)))]
orb = [-1] * V; reps = []
for i in range(V):
    if orb[i] < 0:
        j = i
        for s in range(11):
            orb[j] = len(reps); j = shift(j)
        reps.append(i)
print('line orbits', len(reps))
quads = pickle.load(open('quads.pkl', 'rb'))
# 4-frames whose 4 lines lie in 4 distinct orbits; key = frozenset of orbits
byorbs = {}
for q in quads:
    o = frozenset(orb[x] for x in q)
    if len(o) == 4: byorbs.setdefault(o, q)
print('distinct orbit-4-sets', len(byorbs))
# exact cover of 20 orbits by 5 orbit-4-sets
keys = list(byorbs)
cover = {o: [k for k in keys if o in k] for o in range(20)}
sols = []
def rec(rem, chosen):
    if not rem: sols.append(list(chosen)); return len(sols) < 50
    o = min(rem, key=lambda o: sum(1 for k in cover[o] if k <= rem))
    for k in cover[o]:
        if k <= rem:
            chosen.append(k)
            if not rec(rem - k, chosen): return False
            chosen.pop()
    return True
rec(frozenset(range(20)), [])
print('Z11 orbit covers found', len(sols))
if sols:
    s = sols[0]
    frames = []
    for k in s:
        q = byorbs[k]
        for sh in range(11): frames.append(tuple(shift_ for shift_ in [q[0], q[1], q[2], q[3]]) if sh == 0 else tuple(x for x in frames[-1] and [shift(y) for y in frames[-1]]))
    cov = sorted(x for f in frames for x in f)
    print('frames', len(frames), 'cover ok', cov == list(range(V)))
    print([[ (g.kind[x], g.supp[x]) for x in byorbs[k]] for k in s])
    pickle.dump((frames, sols), open('z11part.pkl', 'wb'))
