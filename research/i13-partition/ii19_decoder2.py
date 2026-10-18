"""II19 DECODER v2 (Gate 3 resolution): the congruence construction at the true width.
rank(M) = 241 (measured) forces decoder width >= 241 — the natural width-10 hope is dead,
but the REGISTER cost is one per centre total (~241), keeping R = 2,337 + 2,230 + 241
= 4,808 = 13.3v UNDER both budgets.  THE REAL GATE: the centre totals must CLOSE
(the I-family's assert 'total frame contains extra lines').
Construction: symmetric congruence over GF(2) — extract columns v = M[:,s] at diagonal
pivots (structured: perps first), alternating-fallback v = M[:,s] + e_s; M = sum v v^T.
Then per column: support, closure (SVD), closed?, rank -> the true cst list.
E8 control: the level-0 block (rank 9) must reproduce E8-grade closed totals.
Then the price at the TRUE cst and R."""
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
LA = L
M = np.zeros((V, V), dtype=np.int64)
for s in range(V):
    for t in range(V):
        M[s, t] = 1 if (s == t or abs(G[s, t]) < 1e-9) else 0
log('system: %d lines' % V)

def congruence_columns(M):
    """symmetric GF(2) congruence: extract columns v with M = sum v v^T.
    diagonal pivots first (v = M[:,s]); alternating fallback (v = M[:,s] + e_s)."""
    R = M.copy() % 2
    N = R.shape[0]
    cols = []
    while True:
        s = None
        for i in range(N):
            if R[i, i]: s = i; break
        if s is not None:
            v = R[:, s].copy()
        else:
            s2 = None
            for i in range(N):
                if R[i].sum(): s2 = i; break
            if s2 is None: break
            v = R[:, s2].copy(); v[s2] ^= 1
        cols.append(v.copy())
        R = (R ^ np.outer(v, v)) % 2
    return cols

def closure_of(idx):
    if not idx: return 0, 0
    A = LA[idx]
    u_, sv, vt = np.linalg.svd(A, full_matrices=False)
    k = int((sv > 1e-9).sum())
    Q = vt[:k]
    res = LA - (LA @ Q.T) @ Q
    cm = 0
    for i in np.nonzero(np.abs(res).max(axis=1) < 1e-9)[0]:
        cm |= 1 << int(i)
    return cm, k

log('extracting decoder columns (congruence)...')
cols = congruence_columns(M)
log('columns extracted: %d (rank(M) was 241)' % len(cols))
# verify W W^T == M
W = np.array(cols).T % 2
chk = (W @ W.T) % 2
log('decoder property W W^T == M: %s' % bool((chk == M % 2).all()))
np.save('ii19_labels_full.npy', W)

cst_pieces = []
closed_cnt = 0
open_cnt = 0
ranks_hist = {}
for c, v in enumerate(cols):
    idx = [s for s in range(V) if v[s]]
    m_mask = sum(1 << s for s in idx)
    cm, k = closure_of(idx)
    if cm == m_mask:
        closed_cnt += 1
    else:
        open_cnt += 1
    cst_pieces.append(k)
    ranks_hist[k] = ranks_hist.get(k, 0) + 1
    if c < 12:
        log('  col %d: %d lines, rank %d, closed %s' % (c, len(idx), k, cm == m_mask))
log('TOTALS: %d closed, %d open; rank histogram %s' % (closed_cnt, open_cnt, dict(sorted(ranks_hist.items()))))
log('TRUE cst: %d registers (one per total), sum of ranks %d' % (len(cst_pieces), sum(cst_pieces)))

# E8 control: the level-0 block
idx00 = [s for s in range(V - 1) if L[s][8] == 0 and L[s][9] == 0]
M0 = M[np.ix_(idx00, idx00)]
cols0 = congruence_columns(M0)
cl0 = 0
for v in cols0:
    idx = [idx00[s] for s in range(len(idx00)) if v[s]]
    m_mask = sum(1 << s for s in idx)
    cm, k = closure_of(idx)
    if cm == m_mask: cl0 += 1
log('E8 CONTROL (level-0, rank 9): %d columns, %d closed, ranks %s' %
    (len(cols0), cl0, sorted(closure_of([idx0 for idx0 in []])[1] for _ in [0]) if False else
     [closure_of([idx00[s] for s in range(len(idx00)) if v[s]])[1] for v in cols0]))

# price at the TRUE decoder
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from mix import price
import mpmath as mp
NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
h, v = 10, 361
R_id = 2337
tiles = 2230
ncols = len(cst_pieces)
R = R_id + tiles + ncols
H = R - 3 * v
log('R = %d (R_id) + %d (tiles) + %d (decoder) = %d (%.2fv); H = %d' %
    (R_id, tiles, ncols, R, R / v, H))
best = None
for src in ([9], [1, 8]):
    for tgt in ([9], [1, 8]):
        c = price(h, v, cst_pieces, src, tgt, [(2 * v, 0, [1, 9]), (H, 1, [9])])
        if c and (best is None or c > best[0]): best = (c, src, tgt)
if best:
    c, src, tgt = best
    log('PRICE at true decoder: c = %s (%+.2f%% vs frontier) @ src %s tgt %s' %
        (mp.nstr(c, 8), float(c / NEWF - 1) * 100, src, tgt))
else:
    log('PRICE at true decoder: no root (over wall)')
log('DONE')