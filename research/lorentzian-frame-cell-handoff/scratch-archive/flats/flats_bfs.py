# Exact enumeration of all flats (closed line sets) of R_live(t) by rank, up to rank 9, by BFS closure(F + u).
# Membership via exact integer elimination is replaced by float projection on small-integer vectors (rank tol 1e-9,
# entries 0/+-1, dims <= 12); nondegeneracy of rank-9 flats via lw.nondegenerate (exact).
import sys, time, pickle, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, nondegenerate
t = int(sys.argv[1]); punct = set(pickle.load(open('../blk/partA.pkl', 'rb'))[1]); MAXR = int(sys.argv[2]) if len(sys.argv) > 2 else 9
R = [u for u in bits(g.HYP[t]) if u not in punct]; n = len(R)
L = g.L[R].astype(float)
def clo(idx):
    A = L[idx]; U, s, Vt = np.linalg.svd(A, full_matrices=False); r = int((s > 1e-9).sum()); Q = Vt[:r]
    res = L - (L @ Q.T) @ Q
    return frozenset(np.nonzero((res * res).sum(1) < 1e-12)[0].tolist()), r
t0 = time.time()
levels = {1: {frozenset([i]) for i in range(n)}}
for r in range(1, MAXR):
    nxt = set()
    for F in levels[r]:
        Fl = sorted(F); seen = set(F)
        for u in range(n):
            if u in seen: continue
            C, rr = clo(Fl + [u]); assert rr == r + 1
            seen |= C; nxt.add(C)
    levels[r + 1] = nxt
    print('t', t, g.kind[t], 'rank', r + 1, 'flats', len(nxt), '%.0fs' % (time.time() - t0), flush=True)
out = {r: [sorted(R[i] for i in F) for F in fl] for r, fl in levels.items() if r >= 5}
if MAXR >= 9:
    nd = [F for F in out[9] if nondegenerate(sum(1 << u for u in F))]
    print('rank-9 flats nondegenerate', len(nd), 'of', len(out[9]), flush=True)
pickle.dump(out, open('flats_%d.pkl' % t, 'wb'))
