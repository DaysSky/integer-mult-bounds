"""Block-closed partitions of I_{13,1}: the 13 PG(2,3) D4(p_L, L) blocks (forced for full PPTT blocks) plus Pasch-pair
blocks (two TTTT frames with the same D4 closure = 4 complementary triple pairs on a 6-set) tiling the other 208 T
lines.  Every frame of a block shares the block's Q.  Enumerate apex offsets (Z13-invariant) and solve the tiling."""
import sys, itertools, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
sys.path.insert(0, '.')
import sympart as SP
g = Geom(13); V = g.V
D = [0, 1, 3, 9]
def T(*a): return g.idx[('T', tuple(sorted(x % 13 for x in a)))]
# Pasch pairs: 6-set S, Pasch frame {abc, ade, bdf, cef} and complements
pp = set()
for S in itertools.combinations(range(13), 6):
    for a, b, c, d, e, f in itertools.permutations(S):
        if a != S[0]: break
        P1 = frozenset([T(a, b, c), T(a, d, e), T(b, d, f), T(c, e, f)])
        comp = lambda t: T(*[x for x in S if x not in g.supp[t]])
        P2 = frozenset(comp(t) for t in P1)
        pp.add(frozenset([P1, P2]))
pp = [tuple(sorted(tuple(sorted(q)) for q in p)) for p in pp]
print('Pasch-pair blocks', len(pp), flush=True)
res = []
for c in range(13):
    if c in D: continue
    Ts = [T(k + d1, k + d2, k + c) for k in range(13) for d1, d2 in itertools.combinations(D, 2)]
    if len(set(Ts)) != 78: print('offset', c, 'apex collision'); continue
    pptt = []
    for k in range(13):
        W = [(k + d) % 13 for d in D]; p = (k + c) % 13
        for (a, b), (cc, d) in [((W[0], W[1]), (W[2], W[3])), ((W[0], W[2]), (W[1], W[3])), ((W[0], W[3]), (W[1], W[2]))]:
            pptt.append((g.P(a, b), g.P(cc, d), T(a, b, p), T(cc, d, p)))
    used = set(l for f in pptt for l in f); rest = set(range(V)) - used
    cand = [p for p in pp if set(p[0]) | set(p[1]) <= rest]
    m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in cand]
    byl = collections.defaultdict(list)
    for i, p in enumerate(cand):
        for l in p[0] + p[1]: byl[l].append(i)
    for l in rest: m.AddExactlyOne([x[i] for i in byl[l]])
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 2
    st = s.Solve(m)
    print('offset %d: candidates %d, tiling %s' % (c, len(cand), s.StatusName(st)), flush=True)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        part = pptt + [q for i, p in enumerate(cand) if s.Value(x[i]) for q in p]
        assert sorted(l for f in part for l in f) == list(range(V))
        ev = SP.evaluate(part)
        print('   compat %d  matefrac %.3f  greedy mean %.2f max %d' % ev, flush=True)
        res.append((c, ev, part))
pickle.dump(res, open('blockpart.pkl', 'wb'))
