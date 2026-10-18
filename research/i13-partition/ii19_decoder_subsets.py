"""II19 SUBSET DECODER SCREEN — completes the closure map with measurements.
rank(M) forces decoder width; the ceiling v/(h+4)^2 vs E8 (120/144 = 0.83) bounds the
architecture.  Every II19 subset gets both numbers: a subset is viable ONLY IF BOTH pass
(rank ~ h AND ceiling >> 0.83).  Also verifies the derived 2-class full-rank result."""
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
FULL = []
for al in R8:
    FULL.append(list(al) + [0, 0])
    FULL.append(list(al) + [1, 0])
    FULL.append(list(al) + [0, 1])
FULL.append([0.0] * 8 + [1, 1])
FULL = np.array(FULL, dtype=float)
E = np.eye(10); E[8, 8] = 0; E[9, 9] = 0; E[8, 9] = 1; E[9, 8] = 1

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

def screen(name, L):
    G = L @ E @ L.T
    V = len(L)
    M = np.zeros((V, V), dtype=np.int64)
    for s in range(V):
        for t in range(V):
            M[s, t] = 1 if (s == t or abs(G[s, t]) < 1e-9) else 0
    r = gf2_rank(M)
    h = int(np.linalg.matrix_rank(L))
    ceil = V / (h + 4) ** 2 / (120 / 144)
    verdict = 'VIABLE-ISH' if (r <= h + 4 and ceil > 1.0) else ('decoder-dead' if r > h + 4 else 'ceiling-dead')
    log('%-34s v=%4d h=%2d rank(M)=%4d ceiling=%.2fx E8 -> %s' % (name, V, h, r, ceil, verdict))
    return r, ceil

log('II19 SUBSET DECODER SCREEN (rank(M) vs h; ceiling vs E8 0.83)')
screen('E8 alone (level 0)', FULL[[s for s in range(360) if s % 3 == 0]])
screen('E8 + special line', FULL[[s for s in range(360) if s % 3 == 0] + [360]])
for pair, nm in ((((0, 0), (1, 0)), '2-class (0,0)+(1,0)'),
                 (((0, 0), (0, 1)), '2-class (0,0)+(0,1)'),
                 (((1, 0), (0, 1)), '2-class (1,0)+(0,1) [twisted]')):
    idx = [s for s in range(360) if tuple(FULL[s][8:].astype(int)) in pair]
    screen(nm, FULL[idx])
screen('3-class minus (0,1), +special', FULL[[s for s in range(360) if tuple(FULL[s][8:].astype(int)) != (0, 1)] + [360]])
screen('3-class minus (1,0), +special', FULL[[s for s in range(360) if tuple(FULL[s][8:].astype(int)) != (1, 0)] + [360]])
screen('FULL II19 (all 3 + special)', FULL)
log('DONE')