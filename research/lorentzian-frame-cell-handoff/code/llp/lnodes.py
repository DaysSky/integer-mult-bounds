"""Enumerate S11-orbits of closed line sets N = pp(N) (nodes) with rank <= 8 and |pm(N)| >= 2.  BFS: N -> pp(N + y).
Saves nodes.pkl: list of (canonical mask, rank, |N|, |pm N|, orbit size)."""
import pickle, time, collections, math
from lgeo import *
t0 = time.time()
seen = {}
frontier = []
for s in (0, 100):     # P line, T line representatives
    N = pp(1 << s); c = canon((N,))[0][0]
    if c not in seen: seen[c] = rank(c); frontier.append(c)
while frontier:
    nf = []
    for N in frontier:
        P = pm(N)
        cand_y = {}
        for y in bits(FULL & ~N):
            P2 = P & HYP[y]
            if pc(P2) < 2: continue
            if P2 in cand_y: continue
            cand_y[P2] = y
        for P2, y in cand_y.items():
            N2 = pm(P2)
            if N2 == N: continue
            r = rank(N2)
            if r > 8: continue
            c = canon((N2,))[0][0]
            if c not in seen:
                seen[c] = r; nf.append(c)
    frontier = nf
    print('level done: total', len(seen), 'new', len(nf), '%.0fs' % (time.time() - t0), flush=True)
out = []
for c, r in seen.items():
    out.append((c, r, pc(c), pc(pm(c))))
out.sort(key=lambda x: (x[1], x[2]))
pickle.dump(out, open('nodes.pkl', 'wb'))
cnt = collections.Counter((r) for c, r, a, b in out)
print('orbits by rank', sorted(cnt.items()))
for r in range(1, 9):
    best = sorted([x for x in out if x[1] == r], key=lambda x: -min(3 * x[2], 2 * x[3]))[:3]
    print('rank', r, 'top (lines, perp):', [(a, b) for c, r_, a, b in best])
