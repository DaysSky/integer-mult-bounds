"""Slice-cover geometry for target perps in E8.  For a root t, perp(t) = the 63 E7 lines.  A target's reads are
confined to hyperplane slices of t-perp (its own top proper frame, each private register's, each source's).
Q1: minimum number of slices covering all 63 lines (kappa).  Q2: with one slice fixed to an E6 slice (36 lines,
shareable by the 3 lines of an A2), the minimum number of further slices covering the remaining 27.
Candidate slices: t-perp intersected with w-perp for w over all E8 roots and norm-4 vectors (exhaustive over
these normals; any slice with more lines is spanned by roots and is among them)."""
import itertools
import numpy as np
from screen_reach import e8_roots2, e8_norm4_2, lines_of
R = np.array(lines_of(e8_roots2())); W = np.array(e8_roots2() + e8_norm4_2())
t = R[0]
perp = [i for i in range(len(R)) if R[i] @ t == 0]; P = R[perp]; assert len(perp) == 63
slices = {}
for w in W:
    if abs(w @ t) == abs(t @ t) and np.linalg.matrix_rank(np.array([w, t])) == 1: continue   # w = +-t
    m = frozenset(i for i in range(63) if P[i] @ w == 0)
    if len(m) < 63: slices[m] = slices.get(m, w)
sizes = sorted({len(m) for m in slices}, reverse=True)
print('distinct slices of t-perp: %d; line counts available: %s' % (len(slices), sizes[:8]))
S = sorted(slices, key=len, reverse=True)
def min_cover(universe, cand, kmax=4):
    cand = [c & universe for c in cand if c & universe]
    cand = sorted(set(cand), key=len, reverse=True)
    for k in range(1, kmax + 1):
        # prune: only the largest few hundred candidates matter for small k
        pool = cand[:400] if k >= 3 else cand
        for combo in itertools.combinations(pool, k):
            if frozenset().union(*combo) >= universe: return k, combo
    return None, None
U63 = frozenset(range(63))
k, combo = min_cover(U63, S, 3)
print('Q1 kappa(E7) =', k, 'slice sizes', [len(c) for c in combo] if combo else None)
e6 = [m for m in S if len(m) == 36]
print('E6 slices through this target:', len(e6))
best = None
for G in e6:
    rest = U63 - G
    k2, c2 = min_cover(rest, [m for m in S if m != G], 3)
    if best is None or (k2 or 99) < best[0]: best = (k2 or 99, [len(x & rest) for x in c2] if c2 else None)
    if k2 == 2: break
print('Q2: after an E6 slice, the remaining 27 lines need %s more slices %s' % best)
