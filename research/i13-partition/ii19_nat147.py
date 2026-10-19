"""nat147: THE 121-LINE FAMILY'S CST-VERDICT (the nat112's unresolved question).

The 121-line (120 E8 roots + the special (0,1,1), h=9): the P111-analog systems =
the j-punctures of the 121-line. Per j: the B0 rank + the rowspace support-dims +
the cst-floor + THE PRICE at (v=121-j, h=9, m=73, rho, cst).
THE QUESTION: dim-(h-2)-supported gathers (cst = 9x7 = 63: the +30-39% class)
vs forced dim-8 gathers (cst = 9x8 = 72: the +5-9% class).
"""
import json, itertools
import numpy as np
from collections import Counter
import mpmath as mp
import os, sys

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import idle_slots, host_greedy

P111 = mp.mpf('0.001733052823330162099157')

# the 121-line: the E8's 120 + the special (0,1,1) (from CONFIG #94: span dim 9,
# form x.x' + 2aa' positive-definite; the special ⊥ all 120 roots)
S = json.load(open('ii19_nat69_spec.json'))
L120 = [tuple(int(c) for c in l) for l in S['lines']]
# the 121-line (the II19 dual construction, CONFIG #94): the 120 roots in R^9 (x, 0)
# + the special ((0,...,0), 1); the form x.x' + 2aa'
L121 = [l + (0,) for l in L120] + [(0, 0, 0, 0, 0, 0, 0, 0, 1)]
print('the 121-line: %d lines | the span dim: %d' % (len(L121), int(np.linalg.matrix_rank(np.array(L121, float)))), flush=True)


def gf2_rank(rows):
    m = [list(r) for r in rows]; rank = 0
    for c in range(len(m[0]) if m else 0):
        piv = None
        for i in range(rank, len(m)):
            if m[i][c]: piv = i; break
        if piv is None: continue
        m[rank], m[piv] = m[piv], m[rank]
        for i in range(len(m)):
            if i != rank and m[i][c]:
                m[i] = [(a ^ b) for a, b in zip(m[i], m[rank])]
        rank += 1
    return rank


def sup_dim(mask, L, n):
    idx = [i for i in range(n) if (mask >> i) & 1]
    return int(np.linalg.matrix_rank(L[idx])) if idx else 0


def system_census(lines, tag):
    L = np.array(lines, float)
    n = len(L)
    G = L @ L.T
    B0 = []
    for t in range(n):
        m = 1 << t
        for q in range(n):
            if q != t and G[t, q] == 0:
                m |= 1 << q
        B0.append(m)
    rows = [[(m >> i) & 1 for i in range(n)] for m in B0]
    rank = gf2_rank(rows)
    bas_masks, bas_rows = [], []
    for m in B0:
        cand = bas_rows + [[(m >> i) & 1 for i in range(n)]]
        if gf2_rank(cand) > len(bas_rows):
            bas_rows = cand; bas_masks.append(m)
    elems = {0}
    for b in bas_masks:
        elems |= {x ^ b for x in elems}
    sd = Counter()
    edims = {}
    for e in elems:
        if e:
            edims[e] = sup_dim(e, L, n)
            sd[edims[e]] += 1
    # the cst-floor: greedy on span-growth
    span = {0}
    remaining = set(B0)
    total = 0
    k = 0
    while remaining and k < 40:
        best, bg = None, -1
        for e, d in edims.items():
            if d == 0: continue
            ns = span | {x ^ e for x in span}
            cov = sum(1 for nm in remaining if nm in ns)
            g = cov / d
            if g > bg: best, bg = e, g
        if best is None or bg <= 0: break
        span |= {x ^ best for x in span}
        remaining = {nm for nm in remaining if nm not in span}
        total += edims[best]
        k += 1
    cf = (total, k) if not remaining else None
    print('%-18s v=%-3d rank=%-3d supdims=%-30s cst-floor=%s' % (tag, n, rank, dict(sorted(sd.items())), cf), flush=True)
    return n, rank, cf, dict(sd)


# (1) the full 121
system_census(L121, 'the 121-line')
# (2) the P111-analog: the 9-punctures (random + the special-removed variants)
import random
rng = random.Random(21)
rem9 = set(rng.sample(range(121), 9))
system_census([L121[i] for i in range(121) if i not in rem9], '121 minus 9 (rand)')
rem9b = {120} | set(rng.sample(range(120), 8))
system_census([L121[i] for i in range(121) if i not in rem9b], '121-9 (special kept)')
rem9c = set(rng.sample(range(120), 9))
system_census([L121[i] for i in range(121) if i not in rem9c], '121-9 (special in)')
# (3) the deeper punctures
for j in (12, 16):
    rem = set(rng.sample(range(121), j))
    system_census([L121[i] for i in range(121) if i not in rem], '121 minus %d' % j)

print()
print('THE PRICE MAP at the cst-verdicts (h=9, m=73, the realizable hist):')
K, T = 4, 32
L = 2*K+1


def price(v, h, R, cst, hist, hi='0.2'):
    a = h-1; m_ = 1+L*a; w = h
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2*v
    W = 2*K*v*T
    def F_of(q):
        nres = R*L
        rem = host_greedy(slots, nres, w, q, m_)
        prof = {}
        for r, z in hist.items(): prof[r] = prof.get(r, 0) + z*T*L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z*T
        tot = sum(prof.values())
        s = sum(mp.mpf(r)*z/(m_*W)*(mp.mpf(m_)/r)**q for r, z in prof.items() if r < m_)
        s += 32*m_*mp.mpf(tot)/(mp.mpf(10)**16 * W)*mp.mpf(m_)**q
        return s - 1
    lo, hq = mp.mpf(0), mp.mpf(hi)
    if F_of(lo) >= 0: return None
    if F_of(hq) < 0: return 'beyond'
    for _ in range(80):
        mid = (lo+hq)/2
        if F_of(mid) >= 0: hq = mid
        else: lo = mid
    return (lo+hq)/2


def hist_real(v, h, R, cst):
    mass = h*R + cst + 2*v*(h-1)
    hist = {h-1: v}
    lo = mass - (h-1)*v
    h3 = lo // 12
    h1 = int(lo * 0.26)
    h2m = lo - h1 - h3
    hist[1] = h1
    hist[2] = h2m // 2
    hist[3] = h3 // 3
    hist[1] += mass - sum(r*c for r, c in hist.items())
    assert sum(r*c for r, c in hist.items()) == mass
    return hist


for (v, cst) in ((121, 72), (112, 63), (112, 72), (109, 63), (109, 72), (105, 63)):
    for rho in (3.5, 3.91):
        R = int(round(rho*v))
        H = hist_real(v, 9, R, cst)
        q = price(v, 9, R, cst, H)
        if q is None:
            print('v=%-3d cst=%-3d rho=%.2f R=%-4d NO-ROOT' % (v, cst, rho, R))
        elif q == 'beyond':
            print('v=%-3d cst=%-3d rho=%.2f R=%-4d BEYOND 0.2 (!!)' % (v, cst, rho, R))
        else:
            print('v=%-3d cst=%-3d rho=%.2f R=%-4d %s (%+.1f%%)' % (v, cst, rho, R,
                  mp.nstr(q, 8), float((q-P111)/P111)*100))
