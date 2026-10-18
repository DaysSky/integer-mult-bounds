"""II19 DECODER CONSTRUCTION (Gate 3) — resolves the ledger's one soft estimate (cst 72-120 assumed).
Decoder = GF(2) labels u_s with u_s . u_t = 1  iff  (s = t or G[s,t] = 0), else 0 (geom.py convention).
Method: incremental GF(2) solve — each new label solves linear constraints against all previous
labels plus the odd-weight condition (greedy, canonical solution).  Then the centre totals:
for each label bit, gather its lines, closure, rank -> cst = sum of ranks (geom.py __main__ pattern).
Also verifies the full decoder property and the total-frame closedness."""
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
log('lines %d' % V)
E = np.eye(10); E[8, 8] = 0; E[9, 9] = 0; E[8, 9] = 1; E[9, 8] = 1
G = L @ E @ L.T
norms = np.diag(G)
log('norm check: %s (all 2)' % dict(zip(*np.unique(np.round(norms, 6), return_counts=True))))
M = np.zeros((V, V), dtype=int)
for s in range(V):
    for t in range(V):
        M[s, t] = 1 if (s == t or abs(G[s, t]) < 1e-9) else 0

def solve_gf2(A, b):
    """solve A x = b over GF(2); returns a solution array or None"""
    A = A.copy() % 2; b = b.copy() % 2
    m, k = A.shape
    aug = np.concatenate([A.astype(np.int64), b.reshape(-1, 1).astype(np.int64)], axis=1)
    r = 0
    piv = []
    for c in range(k):
        pr = None
        for i in range(r, m):
            if aug[i, c]: pr = i; break
        if pr is None: continue
        if pr != r: aug[[r, pr]] = aug[[pr, r]]
        for i in range(m):
            if i != r and aug[i, c]:
                aug[i] ^= aug[r]
        piv.append(c); r += 1
        if r == m: break
    for i in range(r, m):
        if aug[i, :k].sum() == 0 and aug[i, k]: return None
    x = np.zeros(k, dtype=np.int64)
    for i, c in enumerate(piv):
        x[c] = aug[i, k]
    return x

def build_labels(k):
    labels = []
    for t in range(V):
        rows = [labels[s] for s in range(t)]
        rhs = [M[s, t] for s in range(t)]
        rows.append(np.ones(k, dtype=np.int64)); rhs.append(1)  # odd weight
        sol = solve_gf2(np.array(rows), np.array(rhs))
        if sol is None:
            return None, t
        labels.append(sol)
        if (t + 1) % 100 == 0:
            log('k=%d: %d/%d labels built' % (k, t + 1, V))
    return labels, None

for k in (10, 12, 14, 16, 18):
    labels, fail_t = build_labels(k)
    if labels is None:
        log('k=%d: FAILED at t=%d (class of line: level %s)' %
            (k, fail_t, L[fail_t][8:].astype(int).tolist()))
        continue
    U = np.array(labels)
    chk = (U @ U.T) % 2
    ok = bool((chk == M).all())
    log('k=%d: ALL %d LABELS BUILT; decoder property U U^T == M: %s' % (k, V, ok))
    if not ok: continue
    # centre totals: per label bit, gather lines, closure, rank
    LA = L
    cst = 0
    ranks = []
    closed_all = True
    for bit in range(k):
        A_i = [s for s in range(V) if U[s, bit]]
        if not A_i:
            ranks.append(0); continue
        m_mask = sum(1 << s for s in A_i)
        A_mat = LA[A_i]
        u_, sv, vt = np.linalg.svd(A_mat, full_matrices=False)
        kk = int((sv_ > 1e-9).sum() if False else (sv > 1e-9).sum())
        Q = vt[:kk]
        res = LA - (LA @ Q.T) @ Q
        cm = 0
        for i in np.nonzero(np.abs(res).max(axis=1) < 1e-9)[0]:
            cm |= 1 << int(i)
        closed = (cm == m_mask)
        if not closed: closed_all = False
        ranks.append(kk)
        cst += kk
        log('  bit %d: %d lines, rank %d, frame closed: %s' % (bit, len(A_i), kk, closed))
    log('DECODER EXISTS at width k=%d: cst = %d (per-bit ranks %s), all totals closed: %s' %
        (k, cst, ranks, closed_all))
    np.save('ii19_labels_k%d.npy' % k, U)
    log('saved ii19_labels_k%d.npy' % k)
    break
log('DONE')