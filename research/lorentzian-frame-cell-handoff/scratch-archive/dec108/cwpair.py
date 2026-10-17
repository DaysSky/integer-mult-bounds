"""For each S11-orbit of nonzero C_11 codewords (sum of s coordinate totals, s = 1..11): weight, support rank, and the
cheapest pair of frames (pool: rank-9 sections {p,q}-perp, rank-10 frames t-perp / z_i-perp (D10) / I10(W) / z3-perp,
coordinate flats L(S) |S|<=8, apex D's K_h(S) |S|<=8) whose line sets cover the support.  In a 12-piece decoder
containing C_11 with cost < 110, the coset pieces v_k, v_l satisfy supp(c_k + c_l) inside L(F_k) u L(F_l)."""
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a, b))))]; T = lambda a, b, c: idx[('T', tuple(sorted((a, b, c))))]
label = [g.binlabel(u) for u in range(V)]
OM = np.array([[i != j and G[i, j] == 0 for j in range(V)] for i in range(V)])
LA = np.array(g.LA, dtype=float)
rk = lambda m: int(np.linalg.matrix_rank(LA[np.nonzero(m)[0]])) if m.any() else 0
pool = {}   # key bytes -> (mask, rank, kind)
def add(m, kind):
    m = np.asarray(m, dtype=bool); k = m.tobytes()
    if k not in pool: pool[k] = (m, rk(m), kind)
for p in range(V):
    add(OM[p], 'tperp')
    for q in range(p + 1, V):
        if not OM[p, q]: continue
        add(OM[p] & OM[q], 'sec')
for i in range(11):
    add(np.array([label[u] >> i & 1 for u in range(V)], dtype=bool), 'D10')
    add(np.array([i not in g.supp[u] for u in range(V)], dtype=bool), 'I10')
add(np.array([g.kind[u] == 'P' for u in range(V)], dtype=bool), 'A10')
for k in range(3, 9):
    for S in itertools.combinations(range(11), k):
        S = set(S); add(np.array([set(g.supp[u]) <= S for u in range(V)], dtype=bool), 'L%d' % k)
    for h in range(11):
        for S in itertools.combinations([i for i in range(11) if i != h], k):
            m = np.zeros(V, dtype=bool)
            for a, b in itertools.combinations(S, 2): m[P(a, b)] = True; m[T(a, b, h)] = True
            add(m, 'K%d' % k)
masks = np.array([v[0] for v in pool.values()]); ranks = np.array([v[1] for v in pool.values()]); kinds = [v[2] for v in pool.values()]
print('pool', len(masks), 'by kind', {k: kinds.count(k) for k in sorted(set(kinds))}, flush=True)
for s in range(1, 12):
    c = np.array([bin(label[u] & ((1 << s) - 1)).count('1') % 2 == 1 for u in range(V)])
    w = int(c.sum()); best = None
    for fi in range(len(masks)):
        Rm = c & ~masks[fi]
        if not Rm.any():
            cand = (ranks[fi], 0, kinds[fi], '-')
        else:
            cols = np.nonzero(Rm)[0]
            ok = masks[:, cols].all(axis=1)
            if not ok.any(): continue
            j = int(np.argmin(np.where(ok, ranks, 99)))
            cand = (ranks[fi] + ranks[j], 1, kinds[fi], kinds[j])
        if best is None or cand[0] < best[0]: best = cand
    print('codeword s=%d weight %d support rank %d: cheapest frame pair cover' % (s, w, rk(c)), best, flush=True)
