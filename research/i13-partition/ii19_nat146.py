"""nat146: THE DIMENSIONAL SCAN - the (lattice, h) family price map.

The h-lever: m = 1+L(h-1) enters every (m/r)^q term: smaller h -> slower F -> bigger root.
Candidates: E7 (63 lines, h=7), E6 (36, h=6), D6/A6..., vs the E8-family's h=8.
Per lattice: (1) the B0 GF(2)-rank; (2) the rowspace support-dims + the cst-floor;
(3) the price map at (v, h, rho, cst, the realizable hist).
"""
import numpy as np, itertools, json
from collections import Counter
import mpmath as mp
import os, sys

mp.mp.dps = 40
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import idle_slots, host_greedy

P111 = mp.mpf('0.001733052823330162099157')


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


def lattice_census(name, lines, h):
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
    bas_masks = []
    bas_rows = []
    for m in B0:
        cand = bas_rows + [[(m >> i) & 1 for i in range(n)]]
        if gf2_rank(cand) > len(bas_rows):
            bas_rows = cand; bas_masks.append(m)
    elems = {0}
    for b in bas_masks:
        elems |= {x ^ b for x in elems}
    sd = Counter()
    for e in elems:
        if e:
            sd[sup_dim(e, L, n)] += 1
    # the cst-floor: the min sum of support-dims over spanning families (greedy on span growth)
    edims = {e: sup_dim(e, L, n) for e in elems if e}
    span = {0}
    remaining = set(B0)
    total = 0
    k = 0
    while remaining and k < 40:
        best, bg = None, -1
        for e, d in edims.items():
            ns = span | {x ^ e for x in span}
            cov = sum(1 for nm in remaining if nm in ns)
            g = cov / d if d else 0
            if g > bg:
                best, bg = e, g
        if best is None or bg <= 0:
            break
        span |= {x ^ best for x in span}
        remaining = {nm for nm in remaining if nm not in span}
        total += edims[best]
        k += 1
    cf = (total, k) if not remaining else None
    perps = int((G == 0).sum(axis=1).mean()) - 1
    print('%-6s h=%d v=%-3d perps~%-3d rank=%-3d supdims=%-26s cst-floor=%s' % (
        name, h, n, perps, rank, dict(sorted(sd.items())), cf), flush=True)
    return dict(v=n, h=h, rank=rank, perps=perps, sd=dict(sd), cst=cf)


# ===== the lattices =====
# E7: the 63 lines (126 roots): construct via the E8 root system's orthogonal complement trick:
# take E8's 120 lines; pick a root r; E7-ish = the perp-sublattice's lines... simpler: the standard E7 roots
# standard E7: in R^8: (±1±1,0,0,0,0,0,0) all even sign combos? Use the known construction:
# E7 roots = E8 roots orthogonal to a fixed root.
S = json.load(open('ii19_nat69_spec.json'))
LALL = [tuple(int(c) for c in l) for l in S['lines']]
L8 = np.array(LALL, float)
G8 = L8 @ L8.T
r0 = L8[0]
e7 = [LALL[i] for i in range(len(LALL)) if abs(np.dot(L8[i], r0)) < 1e-9 and i != 0]
e7 = [l for l in e7]
# dedupe antipodes
seen = set()
e7u = []
for l in e7:
    if l not in seen and tuple(-x for x in l) not in seen:
        seen.add(l)
        e7u.append(l)
print('E7 constructed: %d lines (expect 63: the roots ⊥ r0, minus antipodes)' % len(e7u), flush=True)
# the E7 spans 7 dims? verify
print('  the E7 span dim: %d' % int(np.linalg.matrix_rank(np.array(e7u, float))), flush=True)

# E6: the E7 roots ⊥ another root
r1 = np.array(e7u[0])
e6 = [l for l in e7u if abs(np.dot(np.array(l, float), r1)) < 1e-9 and l != e7u[0]]
seen = set()
e6u = []
for l in e6:
    if l not in seen and tuple(-x for x in l) not in seen:
        seen.add(l)
        e6u.append(l)
print('E6 constructed: %d lines | the span dim: %d' % (len(e6u), int(np.linalg.matrix_rank(np.array(e6u, float)))), flush=True)

censuses = {}
censuses['E7'] = lattice_census('E7', e7u, 7)
censuses['E6'] = lattice_census('E6', e6u, 6)

# ===== the price map per lattice =====
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
    """the realizable-shape hist: the r434-proportional mass fractions, rank-7 capped at h-1"""
    mass = h*R + cst + 2*v*(h-1)
    # shape: 26% mass at rank1, 53% at rank2, ~19% at mids 3-6, the targets at h-1
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


print()
print('THE DIMENSIONAL PRICE MAP:')
for name, c in censuses.items():
    if not c['cst']:
        print('%s: no cst-floor (skip)' % name)
        continue
    v, h = c['v'], c['h']
    cst = c['cst'][0]
    for rho in (3.3, 3.5, 3.7, 3.9):
        R = int(round(rho*v))
        H = hist_real(v, h, R, cst)
        q = price(v, h, R, cst, H)
        if q is None:
            print('%s h=%d v=%-3d rho=%.1f R=%-4d cst=%-3d NO-ROOT' % (name, h, v, rho, R, cst))
        elif q == 'beyond':
            print('%s h=%d v=%-3d rho=%.1f R=%-4d cst=%-3d BEYOND 0.2 (!!)' % (name, h, v, rho, R, cst))
        else:
            print('%s h=%d v=%-3d rho=%.1f R=%-4d cst=%-3d %s (%+.1f%%)' % (name, h, v, rho, R, cst,
                  mp.nstr(q, 8), float((q-P111)/P111)*100))
