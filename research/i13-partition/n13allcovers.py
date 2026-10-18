"""EXHAUSTIVE 4-covers of R(t) = HYP[t] by perps of rank-3 frames through t (I_{13,1}), up to the stabiliser of t
in S13.  Port of llp/lr8allcovers.py.  Reports, per orbit: |perp|, covers containing the rep, and the overlap
histogram (sum |perp & R| - |R|), i.e. whether DISJOINT (zero-overlap) covers exist — I11's minimum was 33.
usage: n13allcovers.py P|T"""
import sys, itertools, collections, pickle, time
import numpy as np
from lgeo13 import *
kind = sys.argv[1]; t0 = time.time()
def log(*a, **kw): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
t = g.P(0, 1) if kind == 'P' else g.T(0, 1, 2)
R = HYP[t]
fr = {}
for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
    m = (1 << t) | (1 << a) | (1 << b)
    if rank(m) != 3: continue
    F = pp(m)
    if F not in fr: fr[F] = pm(F) & R
FL = list(fr.keys())
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(5)]
PW = np.array([words(fr[F]) for F in FL], dtype=np.uint64)
log(kind, SUPP[t], '|R|', pc(R), 'rank-3 frames through t', len(FL))
orbs = collections.defaultdict(list)
for i, F in enumerate(FL):
    cf, perm = canon((1 << t, F)); orbs[cf].append((i, perm))
log('Stab(t)-orbits of frames', len(orbs), 'sizes', sorted(len(v) for v in orbs.values()), flush=True)
cover_by = {u: np.array([i for i, F in enumerate(FL) if fr[F] >> u & 1]) for u in bits(R)}
def cnt_of(U): return np.bitwise_count(PW & np.array(words(U), dtype=np.uint64)).sum(axis=1)
out = {'t': t, 'orbits': [], 'covers': {}, 'overlap_hist': {}}
total = 0
all_ov = collections.Counter()
three_found = False
for cf, members in sorted(orbs.items(), key=lambda kv: len(kv[1])):
    i1 = members[0][0]; F1 = FL[i1]
    U1 = R & ~fr[F1]
    covs = set()
    c1 = cnt_of(U1)
    u2 = min(bits(U1), key=lambda u: len(cover_by[u]))
    for i2 in cover_by[u2]:
        if i2 == i1: continue
        U2 = U1 & ~fr[FL[i2]]
        if U2 == 0:
            three_found = True
            log('3-COVER FOUND with', F1, FL[i2]); continue
        c2 = cnt_of(U2); n2 = pc(U2); mx = int(c2.max())
        if 2 * mx < n2: continue
        u3 = min(bits(U2), key=lambda u: len(cover_by[u]))
        cand3 = [i for i in cover_by[u3] if c2[i] >= n2 - mx and i != i1 and i != i2]
        for i3 in cand3:
            U3 = U2 & ~fr[FL[i3]]
            if U3 == 0:
                three_found = True
                log('3-COVER FOUND with', F1, FL[i2], FL[i3]); continue
            need = np.array(words(U3), dtype=np.uint64)
            ok = np.nonzero(((PW & need) == need).all(axis=1))[0]
            for i4 in ok:
                if i4 in (i1, i2, i3): continue
                c = tuple(sorted((F1, FL[i2], FL[i3], FL[i4])))
                covs.add(c)
                P4 = [pm(F) & R for F in c]
                o = sum(pc(p) for p in P4) - pc(R)
                all_ov[o] += 1
    out['orbits'].append((F1, len(members)))
    out['covers'][F1] = covs
    total += len(members) * len(covs)
    log('orbit size', len(members), 'perp', pc(fr[F1]), 'lines', pc(F1), 'covers w/ rep', len(covs), flush=True)
log('total covers (sum |orbit| * N / 4) =', total / 4)
log('overlap histogram (smallest 12):', sorted(all_ov.items())[:12])
log('3-covers exist:', three_found)
out['overlap_hist'] = dict(all_ov)
pickle.dump(out, open('n13allcovers_%s.pkl' % kind, 'wb'))
log('saved')
