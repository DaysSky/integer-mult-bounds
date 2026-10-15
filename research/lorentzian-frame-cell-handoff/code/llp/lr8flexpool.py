"""Flex cover pool for all 220 lines.  Full 4-cover lists of t = P(0,1) / T(0,1,2) are rebuilt from the per-orbit-
representative lists (covers containing F = g . covers containing F1 with g from exact canonical forms, g fixing t),
filtered to FLEX covers (no frame with a rank-8 node and an exclusive part of rank >= 7, see lr8flexcov.py), mapped to
the 20 Z11 orbit representatives by a coordinate permutation, sampled (<= NMAX per rep, seeded) and rotated by Z11.
Output r8flex.pkl {t: [4-frame tuples]} (same format as r8covers.pkl).  usage: lr8flexpool.py NMAX"""
import sys, pickle, itertools, random, collections, time
from lgeo import *
NMAX = int(sys.argv[1]); random.seed(7); t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def inv(p):
    q = [0] * n
    for i, x in enumerate(p): q[x] = i
    return q
full = {}
PRK = {}
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    canon_of = {}
    for F in fr: canon_of[F] = canon((1 << t, F))
    rep_of = {}
    for F1 in D['covers']: rep_of[canon_of[F1][0]] = F1
    allc = set()
    for F in fr:
        cf, pF = canon_of[F]
        F1 = rep_of.get(cf)
        if F1 is None: continue
        p1 = canon_of[F1][1]
        g = [None] * n
        ipF = inv(pF)
        for x in range(n): g[x] = ipF[p1[x]]       # g = pF^-1 o p1 : maps (t, F1) -> (t, F)
        assert act(1 << t, g) == 1 << t and act(F1, g) == F
        for c in D['covers'][F1]:
            allc.add(tuple(sorted(act(X, g) for X in c)))
    log(kind, 'full covers', len(allc))
    flex = []
    for c in allc:
        P = [pm(F) & R for F in c]; bad = False
        for i, F in enumerate(c):
            if F not in PRK: PRK[F] = rank(pm(F))
            if PRK[F] != 8: continue
            ex = P[i] & ~(P[(i + 1) % 4] | P[(i + 2) % 4] | P[(i + 3) % 4])
            if ex and rank(ex) >= 7: bad = True; break
        if not bad: flex.append(c)
    log(kind, 'flex covers', len(flex))
    full[kind] = (t, flex)
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
out = {}
for r in reps:
    t, flex = full[KIND[r]]
    # coordinate permutation sending SUPP[t] -> SUPP[r]
    src = list(SUPP[t]); dst = list(SUPP[r])
    rest_s = [x for x in range(n) if x not in src]; rest_d = [x for x in range(n) if x not in dst]
    perm = [None] * n
    for a, b in zip(src + rest_s, dst + rest_d): perm[a] = b
    assert img_line(t, perm) == r
    smp = random.sample(flex, min(NMAX, len(flex)))
    out[r] = sorted(tuple(sorted(act(X, perm) for X in c)) for c in smp)
allc = {}
def rotm(m, k):
    for _ in range(k):
        m2 = 0
        for s in bits(m): m2 |= 1 << rot[s]
        m = m2
    return m
for t in range(V):
    o, k = orb[t]
    allc[t] = [tuple(sorted(rotm(F, k) for F in c)) for c in out[reps[o]]]
pickle.dump(allc, open('r8flex.pkl', 'wb')); log('saved r8flex.pkl', {r: len(out[r]) for r in reps[:2]})
