"""THE 2-CLASS BUILD STAGE 4 (ii19_nat57.py) — the class-blocked decoder + the W + the gathers!!

THE 18-GATHER MACHINERY (the record's own design!!): the class-blocked B' (rank 18!!):
(1) the basis (the 18 rows (the E8-block magic!!)); (2) THE W (the scatter rows: B'[t] =
XOR of the 18 gathers!!); (3) the weights (the scatter cost!!); (4) THE GATHER FRAMES (the
18 retained's final frames: the dim-9 (the CST 162!!)) + the emission's scatter skeleton.
"""
import os, sys, itertools, json
from collections import Counter
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

roots240 = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots240.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots240.add(tuple(Fraction(x, 2) for x in s))

def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

d8 = {canon(r): r for r in roots240}
roots = sorted(d8.values())
V = 240
H = 10
L = []
for c in (0, 1):
    for a in roots:
        L.append([Fraction(x) for x in a] + [Fraction(c), Fraction(0)])
FORM = [[Fraction(0)] * H for _ in range(H)]
for i in range(8): FORM[i][i] = Fraction(1)
FORM[8][9] = FORM[9][8] = Fraction(1)
def ip(x, y):
    return sum(x[i] * y[j] * FORM[i][j] for i in range(H) for j in range(H) if FORM[i][j])
G = [[ip(L[s], L[t]) for t in range(V)] for s in range(V)]
CLS = [s // 120 for s in range(V)]
CPERP = [set(s for s in range(V) if CLS[s] == CLS[t] and s != t and G[s][t] == 0) for t in range(V)]

# (1) THE CLASS-BLOCKED B' + THE RANK!!
B0 = np.array([[1 if (s == t or (CLS[s] == CLS[t] and s in CPERP[t])) else 0
                for s in range(V)] for t in range(V)], dtype=np.uint8)
M2 = np.concatenate([B0.copy(), np.eye(V, dtype=np.uint8)], axis=1)
rr = 0; piv_rows = {}
for c in range(V):
    p = next((i for i in range(rr, V) if M2[i][c]), None)
    if p is None: continue
    M2[[rr, p]] = M2[[p, rr]]
    piv_rows[c] = rr
    for i in range(V):
        if i != rr and M2[i][c]:
            M2[i] ^= M2[rr]
    rr += 1
log('(1) THE CLASS-BLOCKED DECODER RANK: %d (the record 18!!)' % rr)
BASIS_IDX = [(c, [i for i in range(V) if M2[r][V + i]]) for c, r in piv_rows.items()]
log('    the basis (the pivot, the original-row-sets): %d | the set-sizes: %s' % (
    len(BASIS_IDX), Counter(len(o) for c, o in BASIS_IDX)))
# (2) THE W (the scatter rows!!)
BASM = np.array([np.bitwise_xor.reduce(B0[list(o)], axis=0) if len(o) > 1 else B0[o[0]]
                 for c, o in BASIS_IDX])
W = np.zeros((V, len(BASIS_IDX)), dtype=np.uint8)
for t in range(V):
    for k, (c, o) in enumerate(BASIS_IDX):
        if B0[t][c]:
            W[t][k] = 1
chk = (W.astype(int) @ BASM.astype(int) % 2 == B0).all()
log('(2) THE W-SOLVE: %s' % bool(chk))
wpw = Counter(int(x) for x in W.sum(axis=1))
log('    the W-weights (the scatter rows!!): %s' % dict(sorted(wpw.items())))
# (3) the gathers' VALUES (the basis rows: the LINE-SETS!!)
for k, (c, o) in enumerate(BASIS_IDX):
    val = np.bitwise_xor.reduce(B0[list(o)], axis=0) if len(o) > 1 else B0[o[0]]
    bits = sorted(set(np.where(val)[0]) & set(range(V)))
    log('    the gather %d (pivot %d, %d rows): the value %d lines (the class-mix: %d/%d!!)' % (
        k, c, len(o), len(bits), sum(1 for b in bits if CLS[b] == 0), sum(1 for b in bits if CLS[b] == 1)))
json.dump({'BASIS_IDX': [(c, o) for c, o in BASIS_IDX], 'W': W.tolist(), 'rank': int(rr)},
          open('ii19_nat57_W.json', 'w'))
log('saved ii19_nat57_W.json')
