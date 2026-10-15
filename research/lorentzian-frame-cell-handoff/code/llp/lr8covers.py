"""Random 4-covers of R(t) by perps of rank-3 frames through t (I11), for every line: randomised greedy (start from
a random large-perp frame, add the frame covering most uncovered lines with random tie-breaks, keep exact 4-covers).
Generated for the 20 Z11 orbit representatives and rotated to all lines.  Saves r8covers.pkl {t: [tuple of 4 frames]}.
usage: lr8covers.py per_frame minperp
Covers are seeded from every frame through the line with perp size >= minperp (per_frame covers each), so co-users of
a frame have covers containing it."""
import sys, itertools, random, pickle, time, collections
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
out = {}
for r in reps:
    R = HYP[r]; fr = {}
    for a, b in itertools.combinations([x for x in range(V) if x != r], 2):
        m = (1 << r) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)
        if F not in fr: fr[F] = pm(F)
    FL = list(fr.items())
    seeds = [F for F, P in FL if pc(P) >= MINP]
    covs = set(); tries = 0
    for F0 in seeds:
        got = 0
        for _ in range(4 * PF):
            tries += 1
            chosen = [F0]; U = fr[F0]
            for _ in range(3):
                need = R & ~U
                best = max(pc(P & need) for F, P in FL)
                cands = [F for F, P in FL if pc(P & need) + 1 >= best and F not in chosen]
                F = random.choice(cands); chosen.append(F); U |= fr[F]
            if U & R == R:
                covs.add(tuple(sorted(chosen))); got += 1
                if got >= PF: break
    out[r] = sorted(covs)
    print('rep', r, KIND[r], 'seed frames', len(seeds), 'covers', len(out[r]), 'tries', tries, round(time.time() - t0), flush=True)
allc = {}
for t in range(V):
    o, k = orb[t]
    allc[t] = [tuple(sorted(rotm(F, k) for F in c)) for c in out[reps[o]]]
pickle.dump(allc, open('r8covers.pkl', 'wb'))
