"""THE NORM-4-LINES CHECK (ii19_n4check.py) — the OTHER lines-convention (never measured!!).

THE QUESTION (the §151-class!!): the R420's halved-form ('<x,y>/2') makes the E8 ROOTS
(the norm-2-halved = the norm-4-in-x.y!!) the LINES — the 120-root-class. THE OTHER
CONVENTION: the NORM-4 vectors as the LINES (the 1080-line system: the (a,0,0)-class
with a^2 = 4!!) — the perps: the alpha.beta = 0 (the halving preserves the ⊥!!).

THE MASTER-LAW SCREEN: v=1080, h=8 (the norm-4-span = the full E8-8!!):
    the deficit = 256*1080 - 288*CST, the CST ~ rho*(h-1..h) = rho*(7..8!!)
    the frontier-class needs rho <= ~81 (rho/v <= 0.075!!).
THE E-TERMS: the [G = +-2]-off-diagonal pairs (the (2e_1).(11110000) = 2!! the
2-overlap-same-signs = 2!!) — the DENSE-ish E-matrix: the 2-class's E (the matching)
had the rank 120 (the full!!) -> the rho-explosion-expected!!
THE SURPRISE-CHECK: the Johnson-scheme-ish E's GF(2)-rank COULD collapse (the §151!!):
    IF rho <= 81: the deficit ~ 113k -> the c ~ +27% at the honest structure (3.5v!!!).
"""
import itertools
import numpy as np
from fractions import Fraction
from collections import Counter


def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)


def norm4_vectors():
    out = []
    for i in range(8):
        for s in (2, -2):
            v = [Fraction(0)] * 8
            v[i] = Fraction(s)
            out.append(v)
    for combo in itertools.combinations(range(8), 4):
        for signs in itertools.product([1, -1], repeat=4):
            v = [Fraction(0)] * 8
            for k, ix in enumerate(combo):
                v[ix] = Fraction(signs[k], 1)
            out.append(v)
    d = {}
    for v in out:
        d[canon(v)] = v
    return d


def gf2_rank(masks):
    piv = []
    for m in masks:
        x = m
        for p in piv:
            x = min(x, x ^ p)
        if x:
            piv.append(x)
            piv.sort(reverse=True)
    return len(piv)


n4 = norm4_vectors()
lines = [(np.array([float(x) for x in v]), 0, 0) for v in n4.values()]
n = len(lines)
co = np.array([list(al) + [a, b] for al, a, b in lines])
G = co[:, :8] @ co[:, :8].T
Z = np.abs(G) < 1e-9
perp_sizes = Z.sum(axis=1) - 1  # exclude self? no — Z diag is 0 (G=4), so -1 removes nothing
print('the norm-4 classes: %d' % n)
print('the perp-sizes: %s' % dict(sorted(Counter(int(s) for s in perp_sizes).items())))

# THE B0-rows: {t} U perp(t)!!
masks = []
for t in range(n):
    m = 1 << t
    for j in range(n):
        if j != t and Z[t, j]:
            m |= 1 << j
    masks.append(m)
rho = gf2_rank(masks)
print('THE NORM-4-ONLY: v=%d rho=%d (kern %d/%.3f)' % (n, rho, n - rho, (n - rho) / n))
d7 = 256 * n - 288 * rho * 7
d8 = 256 * n - 288 * rho * 8
print('the deficit@CST=rho*7: %d | @CST=rho*8: %d' % (d7, d8))
print('the verdict: %s' % ('DEAD (deficit negative!!)' if max(d7, d8) < 0 else
                           ('the rho/v = %.3f (the frontier-class needs <= 0.075!!)' % (rho / n))))

# THE E-MATRIX's OWN RANK (the [G = +-2]-adjacency!!) — the rho-anatomy!!
E = (np.abs(G - 2) < 1e-9) | (np.abs(G + 2) < 1e-9)
np.fill_diagonal(E, False)
emasks = []
for t in range(n):
    m = 0
    for j in range(n):
        if E[t, j]:
            m |= 1 << j
    emasks.append(m)
erho = gf2_rank(emasks)
print('THE E-RANK (the [G=+-2]-adjacency!!): %d' % erho)
print('DONE')
