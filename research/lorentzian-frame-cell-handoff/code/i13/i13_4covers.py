"""EXHAUSTIVE 4-section covers of R(t) in I_{13,1} (method of llp/lr8allcovers.py): F1 = a largest frame of the cover,
up to Stab(t) (lgeo13.canon); F2 over frames covering the uncovered line u2 with fewest coverers (sizes <= |F1|);
F3 over frames covering u3 (fewest coverers in U2) with |perp n U2| >= |U2| - |F1|; all F4 containing U3 (vectorised).
Every cover with largest frame F1 contains a frame through u2 and one through u3, so none is missed.  For each cover:
per-section (|perp|, line rank of perp, |exclusive|, rank of exclusive).  usage: python3 i13_4covers.py KIND"""
import sys, pickle, collections, time
import numpy as np
from lgeo13 import *
kind = sys.argv[1]; t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]; NF = len(FL); NW = (V + 63) // 64
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(NW)]
PW = np.array([words(P) for P in PL], dtype=np.uint64)
SZ = np.array([pc(P) for P in PL])
cov = collections.defaultdict(list)
for i, P in enumerate(PL):
    for s in bits(P): cov[s].append(i)
reps = {}
for i, F in enumerate(FL):
    key = canon((1 << t, F))[0]
    if key not in reps: reps[key] = i
covers = set()
for key, i1 in sorted(reps.items(), key=lambda kv: -SZ[kv[1]]):
    s1 = SZ[i1]
    if 4 * s1 < pc(R): continue
    U1 = R & ~PL[i1]
    u2 = min(bits(U1), key=lambda s: len(cov[s]))
    n0 = len(covers)
    for i2 in cov[u2]:
        if SZ[i2] > s1: continue
        U2 = U1 & ~PL[i2]
        if not U2: continue
        if pc(U2) > 2 * s1: continue
        u3 = min(bits(U2), key=lambda s: len(cov[s]))
        for i3 in cov[u3]:
            if SZ[i3] > s1 or pc(PL[i3] & U2) < pc(U2) - s1: continue
            U3 = U2 & ~PL[i3]
            if not U3: continue
            uw = np.array(words(U3), dtype=np.uint64)
            ok = np.nonzero(np.all((PW & uw) == uw, axis=1) & (SZ <= s1))[0]
            for i4 in ok: covers.add(tuple(sorted((i1, i2, i3, int(i4)))))
    log('F1 orbit rep |perp|', s1, '-> covers so far', len(covers), '(+%d)' % (len(covers) - n0))
log(kind, 'total 4-covers (largest frame up to Stab(t)):', len(covers))
RK = {}
def rk(m):
    if m not in RK: RK[m] = rank(m)
    return RK[m]
hist = collections.Counter(); allproper = 0
for c in covers:
    row = []
    for a in c:
        o = 0
        for b in c:
            if b != a: o |= PL[b]
        ex = PL[a] & ~o
        row.append((int(SZ[a]), rk(PL[a]), pc(ex), rk(ex) if ex else 0))
    if all(r[3] < r[1] for r in row): allproper += 1
    hist[tuple(sorted(row, reverse=True))] += 1
log('covers with EVERY exclusive part proper (rank < section line rank):', allproper, 'of', len(covers))
for k, v in sorted(hist.items(), key=lambda kv: -kv[1])[:25]:
    print('  %5d | %s' % (v, k), flush=True)
pickle.dump(covers, open('i13_4covers_%s.pkl' % kind, 'wb'))
