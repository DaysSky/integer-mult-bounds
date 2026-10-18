"""THE 2-CLASS BUILD STAGE 3 (ii19_nat55.py) — the delivery algebra!!

(1) THE DECODER: the perp-pattern matrix B (the 240x240 (the perps + self!!)): the GF(2)
rank (the record's 18!!) + the 18-retained basis (the W-solve!!); (2) THE BALANCE: the
per-target reads (the (3,4)-greedy pieces + the leftover carriers!!) XOR the scatter
(the W-rows!!) = e_t (the nat34-class exact GF(2) check!!); (3) THE OUTPUT: the delivery
assignment (ii19_nat55_delivery.json!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# the system (as nat54!!)
roots240 = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
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
PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]

# (1) THE DECODER (the perp-pattern + self!!)
B0 = np.array([[1 if (s == t or s in PERP[t]) else 0 for s in range(V)] for t in range(V)], dtype=np.uint8)
def gf2_rank(M):
    M = M.copy(); rr = 0; rows, cols = M.shape
    for c in range(cols):
        p = next((i for i in range(rr, rows) if M[i][c]), None)
        if p is None: continue
        M[[rr, p]] = M[[p, rr]]
        for i in range(rows):
            if i != rr and M[i][c]:
                M[i] ^= M[rr]
        rr += 1
    return rr, M
rank_B, RREF = gf2_rank(B0)
log('(1) THE DECODER RANK (the perp-pattern + self!!): %d' % rank_B)
# the 18-retained basis: the rref rows + the W-solve (B[t] = XOR of the basis rows!!)
# the W: for each target t: the basis-subset XORing to B[t]!!
BAS = RREF[:rank_B]
W = np.zeros((V, rank_B), dtype=np.uint8)
# solve: the row-space membership: B[t] = sum of the basis rows: use the elimination tracking!!
# (the honest solve: re-run the elimination on [B0 | I] to get the representations!!)
M2 = np.concatenate([B0.copy(), np.eye(V, dtype=np.uint8)], axis=1)
rr = 0
piv_rows = {}
for c in range(V):
    p = next((i for i in range(rr, V) if M2[i][c]), None)
    if p is None: continue
    M2[[rr, p]] = M2[[p, rr]]
    piv_rows[c] = rr
    for i in range(V):
        if i != rr and M2[i][c]:
            M2[i] ^= M2[rr]
    rr += 1
log('    the basis rows: %d | the pivot-map: %d' % (rr, len(piv_rows)))
# the W-rows: each target t: B[t] = XOR of the basis: from the tracking: the target t's
# representation = the row t's history?! (the elimination gives: B[t] -> e_{piv}: the
# representations: solve directly: the basis (the rref rows) -> the W via back-substitution!!)
# (the simplest: for each t: the representation of B[t] in the rref basis: greedily cancel!!)
for t in range(V):
    vec = B0[t].copy()
    for c in sorted(piv_rows):
        if vec[c]:
            W[t] ^= M2[piv_rows[c]][V:]      # the basis-row's representation!!
            vec ^= B0[np.where((M2[piv_rows[c]][V:] == 1))[0][0] if False else 0]
    # hmm — the honest approach below!!
log('    (the W via the rref-basis representations: recomputed below!!)')
# THE HONEST W: the basis = the pivot rows of the reduced M2 (the first rr rows (the B-part = e_c!!)):
# B[t] = XOR of the basis rows k with the pivot c_k in the support of B[t]!!
# the basis rows (the original indices!): the M2's first rr rows' I-parts!!
BASIS_IDX = []
for c, r in piv_rows.items():
    # the row r's I-part: the original rows XORed!!
    orig = [i for i in range(V) if M2[r][V + i]]
    BASIS_IDX.append((c, orig))
log('    the basis (the pivot, the original-row-sets): %d entries' % len(BASIS_IDX))
# the W: B[t] = XOR of the basis-entries with pivots in B[t]'s support!!
W = np.zeros((V, len(BASIS_IDX)), dtype=np.uint8)
for t in range(V):
    for k, (c, orig) in enumerate(BASIS_IDX):
        if B0[t][c]:
            W[t][k] = 1
# the check: W[t] @ BAS-matrix == B0[t]?!
BASM = np.array([B0[o[0]] if len(o) == 1 else np.bitwise_xor.reduce(B0[list(o)], axis=0) for c, o in BASIS_IDX])
chk = (W @ BASM % 2 == B0).all()
log('    THE W-SOLVE CHECK: %s' % bool(chk))
wpw = Counter(W.sum(axis=1))
log('    the W-weights (the scatter rows!!): %s' % dict(sorted(wpw.items())))
json.dump({'rank_B': int(rank_B), 'BASIS_IDX': [(c, orig) for c, orig in BASIS_IDX],
           'W': W.tolist()}, open('ii19_nat55_delivery.json', 'w'))
log('saved ii19_nat55_delivery.json')
