"""Frame-seeded random 4-covers of R(t) by perps of rank-3 frames through t (I11), vectorised (numpy popcount).
For every Z11 orbit representative r and every frame F through r with perp size >= MINP: up to PF greedy completions
(3 more frames, each among those covering >= best-1 of the still-uncovered lines, random choice) that cover R(r).
Rotated to all lines.  Saves r8covers.pkl {t: [tuple of 4 frames]}.  usage: lr8covers.py PF MINP"""
import sys, itertools, random, pickle, time
import numpy as np
from lgeo import *
PF = int(sys.argv[1]); MINP = int(sys.argv[2]); random.seed(1); t0 = time.time()
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
def rotk(x, k):
    for _ in range(k % n): x = rot[x]
    return x
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotk(s, k)
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(4)]
out = {}
for r in reps:
    R = HYP[r]; fr = {}
    for a, b in itertools.combinations([x for x in range(V) if x != r], 2):
        m = (1 << r) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)
        if F not in fr: fr[F] = pm(F)
    FL = list(fr.keys()); PW = np.array([words(fr[F]) for F in FL], dtype=np.uint64)
    seeds = [i for i, F in enumerate(FL) if pc(fr[F]) >= MINP]
    covs = set()
    for i0 in seeds:
        got = 0
        for _ in range(4 * PF):
            chosen = [i0]; U = fr[FL[i0]]
            for _ in range(3):
                need = np.array(words(R & ~U), dtype=np.uint64)
                cnt = np.bitwise_count(PW & need).sum(axis=1)
                best = int(cnt.max())
                cands = [j for j in np.nonzero(cnt >= best - 1)[0] if j not in chosen]
                j = int(random.choice(cands)); chosen.append(j); U |= fr[FL[j]]
            if U & R == R:
                covs.add(tuple(sorted(FL[j] for j in chosen))); got += 1
                if got >= PF: break
    out[r] = sorted(covs)
    print('rep', r, KIND[r], 'frames', len(FL), 'seeds', len(seeds), 'covers', len(out[r]), round(time.time() - t0), flush=True)
allc = {}
for t in range(V):
    o, k = orb[t]
    allc[t] = [tuple(sorted(rotm(F, k) for F in c)) for c in out[reps[o]]]
pickle.dump(allc, open('r8covers.pkl', 'wb'))
print('saved', flush=True)
