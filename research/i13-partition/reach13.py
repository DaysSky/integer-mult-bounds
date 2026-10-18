"""I_{13,1} reach table: max |lines(F-perp)| over representative frames F of each rank, and the rank-5/6
Pareto frontier (rank, perp size).  Reach lemma: R(u) must be covered by perps of the first frames >= k
of the registers carrying x_u; E8 control: D4 (rank 4) reaches 12.  I11,1: rank 8 reaches 6."""
import os, pickle, collections
import base13 as B

g, V = B.g, B.V
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'reach13.pkl')
if os.path.exists(p):
    rows = pickle.load(open(p, 'rb'))
else:
    # enumerate perps of all frames of rank <= 8 through a representative line of each orbit kind.
    # Cheaper: enumerate ALL closed line sets (flats) is huge; instead enumerate frames (orthogonal
    # tuples with sum in 2L is the "good" restriction, but reach should consider ALL frames = any
    # orthogonal set with nondegenerate span?  The reach lemma counts any frame on a chain, which can be
    # any nondegenerate frame containing content.  We enumerate maximal perps among flats spanned by <= 8 lines.
    # To keep it tractable: enumerate perps as intersections of HYP over line subsets, canonicalised.
    # Approach: for each rank r, sample frames as orthogonal r-tuples (t, f2, ..., fr) greedily extended
    # from every start line; take max perp size and record the Pareto (lines covered, perp size) by rank.
    HYP = g.HYP
    best = {}  # rank -> max perp size
    pareto = collections.defaultdict(set)  # rank -> set of (perp_size) seen with their line count
    def perpmask(lines):
        m = (1 << V) - 1
        for s in lines: m &= HYP[s]
        return m
    def nl(mask): return bin(mask).count('1')
    import itertools
    # iterate: start from each line, extend orthogonally (frames need pairwise orthogonal lines)
    def rec(cur, pool, rank_target):
        r = len(cur)
        pm = perpmask(cur)
        # record best at this rank
        if r >= 2:
            key = r
            sz = nl(pm)
            if key not in best or sz > best[key]: best[key] = sz
        if r == rank_target: return
        # candidates orthogonal to all of cur, within pm (any line in pm is orthogonal to cur by def)
        cand = [s for s in g.bits(pm)]
        for i, s in enumerate(cand):
            if s <= (cur[-1] if cur else -1): continue
            npm = pm & HYP[s]
            if nl(npm) == 0: continue
            rec(cur + [s], None, rank_target)
    for start in range(V):
        rec([start], None, 9)
        break  # all lines equivalent? P and T differ; do one per kind
    # do one start per (kind, orbit under affine group) - use group to bound: just do all starts of 2 reps
    reps = [g.P(0, 1), g.T(0, 1, 2)]
    best = {}
    for start in reps:
        rec([start], None, 9)
    rows = dict(sorted(best.items()))
    pickle.dump(rows, open(p, 'wb'))
print('I13,1 max perp size by frame rank (from P(01) and T(012) starts):')
for r, sz in rows.items(): print(' rank', r, 'max perp', sz)
print()
print('I11,1 reference: 1:129 2:85 3:56 4:36 5:25 6:17 7:11 8:6')
