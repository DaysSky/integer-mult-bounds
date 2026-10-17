"""Rank-12 decoders containing C_11 for I_{11,1}: phi in F2^V (the new coset rep) and per-target I_t in F2^11 with
phi(u) = <I_t, label(u)> for u in N(t) and phi(t) + <I_t, label(t)> = 1  (target t uses the new coset).  Solve the
F2 linear system for a chosen set S of targets; report the solution-space dimension (C_11 itself is always a solution
family of dimension 11 when all targets use B0-like rows)."""
import sys, itertools, random
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
import numpy as np
g = Geom(11); V = g.V; n = 11
lab = [g.binlabel(u) for u in range(V)]
N = [[u for u in range(V) if u != t and g.G[t, u] != 0] for t in range(V)]
Rr = [[u for u in range(V) if u != t and g.G[t, u] == 0] for t in range(V)]
def solve_space(S):
    # unknown vector: phi (V bits) + I_t (11 bits) for t in S
    idx = {t: V + 11 * k for k, t in enumerate(S)}
    nv = V + 11 * len(S)
    rows = []; rhs = []
    for t in S:
        for u in N[t]:
            m = 1 << u
            for i in range(n):
                if lab[u] >> i & 1: m ^= 1 << (idx[t] + i)
            rows.append(m); rhs.append(0)
        m = 1 << t
        for i in range(n):
            if lab[t] >> i & 1: m ^= 1 << (idx[t] + i)
        rows.append(m); rhs.append(1)
    # gaussian elimination over F2 with augmented bit at position nv
    piv = {}
    for m, b in zip(rows, rhs):
        x = m | (b << nv)
        while x & ((1 << nv) - 1):
            hb = (x & ((1 << nv) - 1)).bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; break
        else:
            if x >> nv & 1: return None, None
    rank = len(piv)
    # projection of solution space onto phi coordinates: dimension = nullity restricted... compute phi-space dim
    # free variables count:
    return nv - rank, piv
S = list(range(V))
dim, piv = solve_space(S)
print('all targets in new coset: solution space dim (phi + I) =', dim)

def extra(S):
    d, _ = solve_space(S)
    return None if d is None else d - 11   # dims beyond C_11 (phi in C_11 gives exactly 11 incl. determined I's)
Pset = [u for u in range(V) if g.kind[u] == 'P']; Tset = [u for u in range(V) if g.kind[u] == 'T']
print('S = all P:', extra(Pset)); print('S = all T:', extra(Tset))
for k in (0, 1):
    star = [u for u in range(V) if k in g.supp[u]]
    print('S = lines through point %d (%d):' % (k, len(star)), extra(star))
    nstar = [u for u in range(V) if k not in g.supp[u]]
    print('S = lines avoiding point %d (%d):' % (k, len(nstar)), extra(nstar))
random.seed(0)
for size in (20, 40, 80, 120, 160):
    ex = [extra(random.sample(range(V), size)) for _ in range(3)]
    print('random S size', size, 'extra dims', ex, flush=True)
