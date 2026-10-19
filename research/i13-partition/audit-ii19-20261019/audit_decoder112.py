"""Extract the r434 frontier word's decoder, verify it, then add the 121-family 'special' line as an
orthogonal singleton total in 9 dims.  Tests the record's claim 'the special kills the span-7 window'
(ii19_121sub.py: 121-family deficit capped at 9,952)."""
import json, itertools
from fractions import Fraction as Fr
from collections import Counter
import sys
import os
from _common import I13
P = I13 + os.sep
w = json.load(open(P + 'ii19_pub2_p111-r434.json'))
v, h, R = w['v'], w['h'], w['R']
den = w['form']['den']; Bf = [[Fr(x, den) for x in r] for r in w['form']['num']]
L = w['lines']
def ip(x, y, B): return sum(x[i] * B[i][j] * y[j] for i in range(len(x)) for j in range(len(x)) if B[i][j])
def rank(vecs):
    m = [[Fr(x) for x in r] for r in vecs]; rk = 0; n = len(m[0]) if m else 0
    for c in range(n):
        p = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[rk], m[p] = m[p], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]; m[i] = [a - f * b for a, b in zip(m[i], m[rk])]
        rk += 1
    return rk
def gram_det_nonzero(vecs, B):
    # basis of span, then Gram determinant
    bas = []
    for x in vecs:
        if rank(bas + [x]) > len(bas): bas.append(x)
    G = [[ip(a, b, B) for b in bas] for a in bas]
    M = [r[:] for r in G]; k = len(M); d = Fr(1)
    for c in range(k):
        p = next((i for i in range(c, k) if M[i][c] != 0), None)
        if p is None: return False, len(bas)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for i in range(c + 1, k):
            f = M[i][c] / M[c][c]; M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return d != 0, len(bas)
# --- replay D and A exactly (F2 values) ---
nreg = 2 * v + R
val = [1 << i for i in range(nreg)]
for F, d, srcs in w['D'] + w['A']:
    for s in srcs: val[d] ^= val[s]
ret = w['ret']; rf = w['ret_frames']
U = [val[q] & ((1 << v) - 1) for q in ret]
dims = [rank(w['frames'][f]) if w['frames'][f] else 0 for f in rf]
B = [0] * v
for t in range(v):
    for k in w['scatter'][t]: B[t] ^= U[k]
G = [[ip(L[s], L[t], Bf) for t in range(v)] for s in range(v)]
bad = [(t, s) for t in range(v) for s in range(v)
       if (s == t and not (B[t] >> s) & 1) or (s != t and G[s][t] != 0 and (B[t] >> s) & 1)]
print('r434 decoder: totals %d, frame dims %s, cst %d, validity violations %d' % (len(U), dims, sum(dims), len(bad)))
print('  free (orthogonal) entries used as 1: %d of %d' % (
    sum(1 for t in range(v) for s in range(v) if s != t and G[s][t] == 0 and (B[t] >> s) & 1),
    sum(1 for t in range(v) for s in range(v) if s != t and G[s][t] == 0)))
# --- the 112-line system in 9 dims: roots + special, special norm +2 and -2 ---
for sign in (+1, -1):
    B9 = [[Fr(0)] * 9 for _ in range(9)]
    for i in range(8): B9[i][i] = Bf[i][i]
    B9[8][8] = Fr(2 * sign)
    L9 = [l + [0] for l in L] + [[0] * 8 + [1]]
    V = v + 1; SP = v
    U9 = U + [1 << SP]                         # the special singleton total
    frames9 = [[x + [0] for x in w['frames'][f]] for f in rf] + [[[0] * 8 + [1]]]
    ok_frames = [gram_det_nonzero(F, B9) for F in frames9]
    cont_ok = all(rank(frames9[k] + [L9[s]]) == rank(frames9[k]) for k in range(len(U9))
                  for s in range(V) if (U9[k] >> s) & 1)
    B112 = [0] * V
    for t in range(v):
        for k in w['scatter'][t]: B112[t] ^= U9[k]
    B112[SP] = U9[-1]
    G9 = [[ip(L9[s], L9[t], B9) for t in range(V)] for s in range(V)]
    bad9 = [(t, s) for t in range(V) for s in range(V)
            if (s == t and not (B112[t] >> s) & 1) or (s != t and G9[s][t] != 0 and (B112[t] >> s) & 1)]
    cst = sum(d for _, d in ok_frames)
    print('112-line system (special norm %+d): frames nondegenerate %s, content-in-frame %s, violations %d, cst %d, '
          'deficit 256v-288cst = %d' % (2 * sign, all(o for o, _ in ok_frames), cont_ok, len(bad9), cst, 256 * V - 288 * cst))
# --- the record's method: min-cost basis of rowspace(B0) for the same 112 lines (special kept) ---
V = v + 1
L9 = [l + [0] for l in L] + [[0] * 8 + [1]]
B9 = [[Fr(0)] * 9 for _ in range(9)]
for i in range(8): B9[i][i] = Bf[i][i]
B9[8][8] = Fr(2)
rows = []
for t in range(V):
    m = 1 << t
    for u in range(V):
        if u != t and ip(L9[t], L9[u], B9) == 0: m |= 1 << u
    rows.append(m)
bx = {}
for r in rows:
    x = r
    while x:
        p = (x & -x).bit_length() - 1
        if p in bx: x ^= bx[p]
        else: bx[p] = x; break
piv = list(bx.values()); rk = len(piv)
cws = set()
for mask in range(1, 1 << rk):
    x = 0
    for k in range(rk):
        if (mask >> k) & 1: x ^= piv[k]
    cws.add(x)
spans = Counter(rank([L9[i] for i in range(V) if (x >> i) & 1]) for x in cws)
print('record method on the same 112 lines: rank(B0) %d, codeword span census %s' % (rk, dict(sorted(spans.items()))))
