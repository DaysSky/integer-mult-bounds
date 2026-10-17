"""EXACT search for 4-section PARITY covers (XOR = R(t), defect 0) of t in I_{13,1} that use at least one rank-2
section (perp of a nondegenerate rank-2 frame through t: pair or A2 triangle; rank-11 section).  Cases by number j of
rank-2 sections: j=4 (pair table), j=3 (r2 x r3 lookups in the r2-pair table), j=2 (sorted 64-bit hashes of r2^r3
combos vs r3^r2 queries), j=1 (r2 orbit reps x r3 x hashed r3^r3, as i13_parity4.py).  Hash hits are verified exactly.
usage: python3 i13_parity4_r2.py KIND"""
import sys, pickle, collections, itertools, time
import numpy as np
from lgeo13 import *
kind = sys.argv[1]; t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]; NW = (V + 63) // 64
eta = np.diag([1.0] * n + [-1.0])
def nondeg(m):
    M = np.zeros((0, n + 1))
    for s in bits(m):
        M2 = np.vstack([M, g.LA[s]])
        if np.linalg.matrix_rank(M2) > M.shape[0]: M = M2
    return abs(np.linalg.det(M @ eta @ M.T)) > 1e-6
r2 = {}
for u in range(V):
    if u == t: continue
    F = pp((1 << t) | (1 << u))
    if F not in r2 and nondeg(F): r2[F] = pm(F)
R2F = list(r2); R2P = [r2[F] for F in R2F]; n2 = len(R2F); n3 = len(FL)
log(kind, 'rank-2 sections', n2, 'rank-3 sections', n3)
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(NW)]
mult = np.array([0x9E3779B97F4A7C15 + 2 * w + 1 for w in range(NW)], dtype=np.uint64)
def fold(arr):
    with np.errstate(over='ignore'): return np.bitwise_xor.reduce(arr * mult, axis=-1)
W2 = np.array([words(P) for P in R2P], dtype=np.uint64); W3 = np.array([words(P) for P in PL], dtype=np.uint64)
p3 = {P: i for i, P in enumerate(PL)}
found = collections.Counter()
# j = 4 and j = 3 via r2-pair table
pair2 = collections.defaultdict(list)
for a in range(n2):
    for b in range(a + 1, n2): pair2[R2P[a] ^ R2P[b]].append((a, b))
for X, lst in pair2.items():
    for (c, d) in pair2.get(R ^ X, []):
        for (a, b) in lst:
            if len({a, b, c, d}) == 4: found['r2^4'] += 1
log('j=4 done', found['r2^4'])
for a in range(n2):
    Ra = R ^ R2P[a]
    for c in range(n3):
        for (b, d) in pair2.get(Ra ^ PL[c], []):
            if a not in (b, d): found['r2^3 r3'] += 1
log('j=3 done', found['r2^3 r3'])
# j = 2: combos r2 x r3 hashed (n2*n3 rows); query (R ^ r2 ^ r3)
H = fold((W2[:, None, :] ^ W3[None, :, :]).reshape(-1, NW))          # index = a*n3 + c
order = np.argsort(H); Hs = H[order]
Rw = np.array(words(R), dtype=np.uint64)
hits = 0
for a in range(n2):
    Q = fold(W2[a][None, :] ^ W3 ^ Rw[None, :])                          # R ^ r2_a ^ r3_c for all c
    pos = np.searchsorted(Hs, Q); pos[pos >= len(Hs)] = len(Hs) - 1
    for c in np.nonzero(Hs[pos] == Q)[0]:
        lo = pos[c]
        while lo < len(Hs) and Hs[lo] == Q[c]:
            idx = order[lo]; b, d = divmod(int(idx), n3)
            if b != a and d != c and R2P[a] ^ PL[c] ^ R2P[b] ^ PL[d] == R: found['r2^2 r3^2'] += 1
            lo += 1
log('j=2 done', found['r2^2 r3^2'])
# j = 1: r2 orbit reps x r3 x (r3 ^ r3) via coverer lookup
reps = {}
for a, F in enumerate(R2F): reps.setdefault(canon((1 << t, F))[0], a)
cov = collections.defaultdict(list)
for i, P in enumerate(PL):
    for s in bits(P): cov[s].append(i)
covarr = {s: np.array(v, dtype=np.int64) for s, v in cov.items()}
H3 = fold(W3); o3 = np.argsort(H3); H3s = H3[o3]
for key, a in reps.items():
    for i2 in range(n3):
        Y = R ^ R2P[a] ^ PL[i2]
        if not Y: continue
        u = min(bits(Y), key=lambda s: len(cov[s]))
        c3 = covarr[u]
        Z = W3[c3] ^ np.array(words(Y), dtype=np.uint64)
        hz = fold(Z); pos = np.searchsorted(H3s, hz); pos[pos >= n3] = n3 - 1
        for h in np.nonzero(H3s[pos] == hz)[0]:
            zint = 0
            for w in range(NW): zint |= int(Z[h][w]) << (64 * w)
            i4 = p3.get(zint)
            if i4 is not None and len({i2, int(c3[h]), i4}) == 3: found['r2 r3^3'] += 1
log('j=1 done', found['r2 r3^3'], '(r2 orbit reps %d)' % len(reps))
log(kind, 'defect-0 4-section parity covers with >= 1 rank-2 section:', dict(found))
