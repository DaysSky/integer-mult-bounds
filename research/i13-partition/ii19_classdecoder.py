"""II19 CLASS-BLOCKED DECODER — the II19-native decode under the TRUE (relaxed asymmetric)
definition from gcheck.py/HANDOFF:  B = U W^T with B_tt = 1 and B_ts = 0 ONLY on
non-orthogonal pairs (FREE on orthogonal pairs).  NOT the symmetric full-pattern
convention (that was only the naive B0 = J + G, rank 241 — the wrong convention).
DESIGN: B = the class-blocked matrix (within-class symmetric M-blocks, one per level
class, + the special line's singleton).  VALID: diagonal 1; cross-class 0 (always legal);
rank 3x9 + 1 = 28.  junk(t) = the within-class perp only.
WORD: 3 disjoint root-lattice-class subwords + glue: branches 2v, middle 3x180, retained 28.
THIS SCRIPT: verify B; the junk sizes; the cst (the retained gathers' ranks); THE PRICE
at R ~ 1,290 helpers vs the frontier 0.0017444.  E8-parameter control included."""
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
log('system: %d lines' % V)

# classes
cls = []
for s in range(V):
    a, b = int(L[s][8]), int(L[s][9])
    cls.append((a, b))
classes = {}
for s in range(V): classes.setdefault(cls[s], []).append(s)
log('classes: %s' % {k: len(v) for k, v in sorted(classes.items())})

# 1. THE CLASS-BLOCKED B
B = np.zeros((V, V), dtype=np.int64)
for k, idx in classes.items():
    for s in idx:
        B[s, s] = 1
        for t in idx:
            if s != t and abs(G[s, t]) < 1e-9:
                B[s, t] = 1
# verify: diagonal; support ONLY on orthogonal pairs
ok_diag = bool((np.diag(B) == 1).all())
viol = 0
for s in range(V):
    for t in range(V):
        if s != t and B[s, t] and abs(G[s, t]) > 1e-9:
            viol += 1
log('B check: diagonal all 1: %s; support violations on non-orthogonal pairs: %d' % (ok_diag, viol))

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
rk = gf2_rank(B)
log('CLASS-BLOCKED DECODER RANK: %d (expected 28 = 3x9 + 1)' % rk)

# 2. junk sizes: the within-class perp counts
junk = {}
for s in range(V):
    k = cls[s]
    junk[s] = [t for t in classes[k] if t != s and abs(G[s, t]) < 1e-9]
sizes = [len(junk[s]) for s in range(V)]
log('junk(t) sizes: mean %.1f min %d max %d; total load %d' %
    (sum(sizes) / V, min(sizes), max(sizes), sum(sizes)))
xsp = [s for s in range(V) if cls[s] == (1, 1)]
log('special line junk: %s' % ([len(junk[s]) for s in xsp]))

# 3. the retained registers + cst: per class, the symmetric decoder labels via congruence
def congruence_columns(M):
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

def rank_of_lines(idx):
    if not idx: return 0
    return int(np.linalg.matrix_rank(L[idx]))

cst_pieces = []
gather_info = []
for k in sorted(classes):
    idx = classes[k]
    if len(idx) == 1:
        cst_pieces.append(1)
        gather_info.append((k, 1, 1))
        continue
    Mk = B[np.ix_(idx, idx)]
    cols = congruence_columns(Mk)
    for c_, v in enumerate(cols):
        supp = [idx[s] for s in range(len(idx)) if v[s]]
        r_ = rank_of_lines(supp)
        cst_pieces.append(r_)
        gather_info.append((k, len(supp), r_))
    log('class %s: %d decoder columns (gathers), ranks %s' %
        (k, len(cols), [g[2] for g in gather_info if g[0] == k]))
cst = sum(cst_pieces)
log('RETAINED: %d registers, cst (sum of gather ranks) = %d' % (len(cst_pieces), cst))
log('gather (class, size, rank) sample: %s' % gather_info[:12])

# 4. THE WORD: branches 2v + middle 3x180 + retained; R = helpers
MID_PER_CLASS = 180
nret = len(cst_pieces)
H_mid = 3 * MID_PER_CLASS + nret
R_helpers = 2 * V + H_mid
log('WORD STRUCTURE: branches %d + middle %d (3x%d + %d retained) = R %d helpers = %.2fv' %
    (2 * V, H_mid, MID_PER_CLASS, nret, R_helpers, R_helpers / V))

# 5. THE PRICE
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from mix import price
import mpmath as mp
NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
h, v = 10, 361
log('PRICE GRID (frontier %s)' % mp.nstr(NEWF, 8))
best = None
for midpc in (120, 150, 180, 240):
    H_mid = 3 * midpc + nret
    for src in ([9], [1, 8]):
        for tgt in ([9], [1, 8]):
            for midshape in ([9], [4, 5]):
                c = price(h, v, cst_pieces, src, tgt, [(2 * v, 0, [1, 9]), (H_mid, 1, midshape)])
                if c and (best is None or c > best[0]):
                    best = (c, midpc, src, tgt, midshape, 2 * v + H_mid)
if best:
    c, midpc, src, tgt, midshape, Rtot = best
    log('BEST c = %s (%+.2f%% vs frontier) @ mid/class %d, src %s tgt %s mid %s, R = %d helpers (%.2fv)' %
        (mp.nstr(c, 8), float(c / NEWF - 1) * 100, midpc, src, tgt, midshape, Rtot, Rtot / v))
else:
    log('NO ROOT in the grid')
# the scan across mid costs: report the c at each midpc
for midpc in (120, 150, 180, 240, 300):
    H_mid = 3 * midpc + nret
    bb = None
    for src in ([9], [1, 8]):
        for tgt in ([9], [1, 8]):
            c = price(h, v, cst_pieces, src, tgt, [(2 * v, 0, [1, 9]), (H_mid, 1, [9])])
            if c and (bb is None or c > bb): bb = c
    if bb:
        log('  mid/class %d -> R %d (%.2fv): c = %s (%+.2f%%)' %
            (midpc, 2 * v + H_mid, (2 * v + H_mid) / v, mp.nstr(bb, 8), float(bb / NEWF - 1) * 100))
    else:
        log('  mid/class %d -> R %d (%.2fv): NO ROOT' % (midpc, 2 * v + H_mid, (2 * v + H_mid) / v))
log('DONE')