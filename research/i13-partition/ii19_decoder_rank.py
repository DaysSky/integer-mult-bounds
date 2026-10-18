"""II19 decoder rank analysis: rank of M = (1 iff s=t or orthogonal) over GF(2).
Any symmetric M with nonzero diagonal factors as W W^T at width = rank(M) (congruence
argument), so the decoder EXISTS at width rank(M) — the question is the WIDTH, which
drives cst (k centre totals x rank <= 10 each => cst ~ 10k; k <= 14 fits the budget,
k >> 14 blows it).  Also: sub-block ranks (level-0, level-1 classes) for structure."""
import sys, time, itertools, resource
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
R8 = list(d8.values())
L = []
for al in R8:
    L.append(list(al) + [0, 0])
    L.append(list(al) + [1, 0])
    L.append(list(al) + [0, 1])
L.append([0.0] * 8 + [1, 1])
L = np.array(L, dtype=float)
V = len(L)
E = np.eye(10); E[8, 8] = 0; E[9, 9] = 0; E[8, 9] = 1; E[9, 8] = 1
G = L @ E @ L.T
M = np.zeros((V, V), dtype=np.int64)
for s in range(V):
    for t in range(V):
        M[s, t] = 1 if (s == t or abs(G[s, t]) < 1e-9) else 0
log('system: %d lines' % V)

def gf2_rank(A):
    A = (A.copy()) % 2
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        pr = None
        for i in range(r, rows):
            if A[i, c]: pr = i; break
        if pr is None: continue
        if pr != r: A[[r, pr]] = A[[pr, r]]
        for i in range(rows):
            if i != r and A[i, c]: A[i] ^= A[r]
        r += 1
        if r == rows: break
    return r

r_full = gf2_rank(M)
log('rank(M) FULL SYSTEM over GF(2): %d  -> decoder exists at width %d (congruence)' % (r_full, r_full))
# sub-blocks: level-0 (the 120 E8 roots at (0,0)), level (1,0) 120, level (0,1) 120
idx00 = [s for s in range(V - 1) if L[s][8] == 0 and L[s][9] == 0]
idx10 = [s for s in range(V - 1) if L[s][8] == 1 and L[s][9] == 0]
idx01 = [s for s in range(V - 1) if L[s][8] == 0 and L[s][9] == 1]
for name, idx in (('level-(0,0)', idx00), ('level-(1,0)', idx10), ('level-(0,1)', idx01),
                  ('level-(0,0)+(1,1)', idx00 + [V - 1])):
    S = M[np.ix_(idx, idx)]
    log('rank(M[%s]): %d of %d lines' % (name, gf2_rank(S), len(idx)))
# the natural hope: rank ~ 10-14 (fits cst budget); wide rank blows cst
if r_full <= 14:
    log('DECODER AT NATURAL WIDTH: cst projection ~ %d x <=10 = <=%d — FITS the budget band' % (r_full, 10 * r_full))
else:
    log('DECODER WIDE: cst projection ~ up to %d — check against the budget (robust through ~120-140)' % (10 * r_full))
log('DONE')