"""Plane orbit reps (lines in span of 2 lines) and the number of concrete closed sets inside each section pm(plane)."""
import pickle, time, collections, itertools
from lgeo import *
def plane_of(u, v):
    if G[u][v] == 0: return (1 << u) | (1 << w) if False else (1 << u) | (1 << v)
    m = (1 << u) | (1 << v)
    for w in range(V):
        if w in (u, v): continue
        # w in span(u,v)?  check rank
        if rank(m | (1 << w)) == 2: m |= 1 << w
    return m
reps = {}
for u in (0, 100):
    for v in range(V):
        if v == u: continue
        pi = plane_of(u, v)
        c = canon((pi,))[0][0]
        if c not in reps: reps[c] = (pc(c), pc(pm(c)))
print('plane orbits', len(reps), sorted(reps.values()))
pickle.dump(sorted(reps), open('planes.pkl', 'wb'))
t0 = time.time()
for pi in sorted(reps):
    S = pm(pi)
    seen = set(); fr = []
    for u in bits(S):
        N = pp(1 << u)
        if N not in seen: seen.add(N); fr.append(N)
    while fr:
        nf = []
        for N in fr:
            P = pm(N)
            done = set()
            for y in bits(S & ~N):
                P2 = P & HYP[y]
                if P2 in done: continue
                done.add(P2)
                N2 = pm(P2)
                if N2 not in seen: seen.add(N2); nf.append(N2)
        fr = nf
    print('plane', reps[pi], 'closed sets inside section:', len(seen), 'sum sizes', sum(pc(N) for N in seen), '%.0fs' % (time.time() - t0), flush=True)
