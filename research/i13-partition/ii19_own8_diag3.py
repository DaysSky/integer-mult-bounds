"""THE SPECIAL's CHANNEL SOLVE: the repB-span analysis (the u-complement!!) + the S-set."""
import json
from collections import Counter
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
V, H, R, SP = W3['v'], W3['h'], W3['R'], 120
lines = W3['lines']
ret_list, scatter0 = W3['ret'], W3['scatter']
D, A = W3['D'], W3['A']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in W3['frames']]
nreg0 = 2 * V + R
XMASK = (1 << V) - 1

val = [1 << i for i in range(nreg0)]
cur = list(W3['start'])
def climb(r, F):
    if cur[r] != F:
        assert dims[F] >= dims[cur[r]]
        cur[r] = F
for F, d, srcs in D:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in A:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
xp = [val[r] & XMASK for r in ret_list]

# the unique reps Wp (the xT fix!!)
rows = list(xp); aug = [[1 if i == j else 0 for j in range(10)] for i in range(10)]
rr = 0; pivots = []; T = []
for col in range(V):
    piv_i = next((i for i in range(rr, 10) if (rows[i] >> col) & 1), None)
    if piv_i is None: continue
    rows[rr], rows[piv_i] = rows[piv_i], rows[rr]
    aug[rr], aug[piv_i] = aug[piv_i], aug[rr]
    for i in range(10):
        if i != rr and (rows[i] >> col) & 1:
            rows[i] ^= rows[rr]; aug[i] = [a ^ b for a, b in zip(aug[i], aug[rr])]
    pivots.append((col, rows[rr])); T.append(list(aug[rr])); rr += 1
def solve10(row):
    coords = [0] * 10; x = row
    for k, (col, rw) in enumerate(pivots):
        if (x >> col) & 1:
            coords[k] = 1; x ^= rw
    assert x == 0
    return coords
def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]
Brows = []
for t in range(V):
    m = 1 << t
    for u in range(V):
        if u != t and ip121(lines[t], lines[u]) == 0:
            m |= 1 << u
    Brows.append(m)
Wp = []
for t in range(V):
    red = solve10(Brows[t])
    w = [0] * 10
    for k in range(10):
        if red[k]:
            for j in range(10):
                if T[k][j]: w[j] ^= 1
    Wp.append(w)

# (a) the w*-complement (the rho=9 direction!!): w . Wp[t] = 0 for all t
#     = the null space of the 121 x 10 matrix (the rank 9 -> 1-dim!!)
import itertools
M = [Wp[t] for t in range(V)]
# gaussian elimination over F2 on the transpose: find w with M w = 0
mt = [[M[t][q] for t in range(V)] for q in range(10)]   # 10 x 121
# rref of mt -> the null space of M^T ... simpler: brute-force the 10-dim null
# via elimination on the 121 rows:
piv2 = []
Mr = [list(r) for r in M]
r2 = 0
for c in range(10):
    p = next((i for i in range(r2, len(Mr)) if Mr[i][c]), None)
    if p is None: continue
    Mr[r2], Mr[p] = Mr[p], Mr[r2]
    for i in range(len(Mr)):
        if i != r2 and Mr[i][c]:
            Mr[i] = [a ^ b for a, b in zip(Mr[i], Mr[r2])]
    piv2.append(c); r2 += 1
free = [c for c in range(10) if c not in piv2]
print('the Wp-matrix rank: %d (the free coords: %s)' % (r2, free))
assert len(free) == 1
fc = free[0]
wstar = [0] * 10
wstar[fc] = 1
for i, c in enumerate(piv2):
    wstar[c] = Mr[i][fc]
print('w* (the rho=9 complement!!): %s' % wstar)
print('    -> u[0] = w*[0] = %d | u[1] = w*[1] = %d' % (wstar[0], wstar[1]))

# (b) the SS1492 basis + repB (the own8 machinery!!)
PHI = lambda row: (row >> SP) & 1
cands = [k for k in range(1, V) if PHI(Brows[k]) == 1]
sel = []; cu = [Brows[0]]
def gf2_rank(rows_in):
    rs = list(rows_in); rank = 0
    for col in range(V):
        piv = next((i for i in range(rank, len(rs)) if (rs[i] >> col) & 1), None)
        if piv is None: continue
        rs[rank], rs[piv] = rs[piv], rs[rank]
        for i in range(len(rs)):
            if i != rank and (rs[i] >> col) & 1: rs[i] ^= rs[rank]
        rank += 1
    return rank
for k in cands:
    if gf2_rank(cu + [Brows[k]]) == len(cu) + 1:
        sel.append(k); cu = cu + [Brows[k]]
        if len(sel) == 8: break
print('sel = %s' % sel)
repB = []
for j, k in enumerate(sel):
    repB.append([Wp[0][q] ^ Wp[k][q] for q in range(10)])
repB.append(list(Wp[0]))          # the odd (j=8)
for j in range(8):
    print('  repB[%d] (sel=%d): %s (size %d)' % (j, sel[j], repB[j], sum(repB[j])))

# (c) the S-solve: P_S[0] = 1, P_S[1] = 0 (the q=2..8 absorbed by the old-ret reads!!)
#     brute-force over the 2^8 subsets (cheap!!)
best = None
for mask in range(1 << 8):
    P = [0] * 10
    for j in range(8):
        if (mask >> j) & 1:
            for q in range(10):
                P[q] ^= repB[j][q]
    if P[0] == 1 and P[1] == 0:
        S_old = [q for q in range(2, 9) if P[q]]
        cost = bin(mask).count('1') + len(S_old)
        if best is None or cost < best[0]:
            best = (cost, mask, S_old, P)
print('THE S-SOLVE (the minimal!!): cost=%d | S=%s | S_old=%s' % (
    best[0], [j for j in range(8) if (best[1] >> j) & 1], best[2]))
print('    P = %s' % best[3])
# the verification: the delivered = O_0?!
S = [j for j in range(8) if (best[1] >> j) & 1]
acc = 0
for j in S:
    acc ^= (1 << 0)  # placeholder
# the true check: XOR of the O_q parities:
P = best[3]
print('    the O-parity check: P[0]=%d P[1]=%d -> the delivered x = xp[0] + S_old-parts!!' % (P[0], P[1]))
print('    S_old old-rets = %s (the readable-at-673!!)' % [ret_list[q] for q in best[2]])
print('    S new-rets (the builds!!) = the j-set %s' % S)
