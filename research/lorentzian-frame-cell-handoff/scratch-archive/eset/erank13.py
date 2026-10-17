"""E-set rank structure of I_{13,1}'s PG(2,3) good-frame partition (compare erank.py: E8 R420 rank 6/8 halves 4/8;
I11 rank 8-9/11).  E(t,e) = lines perp t,e and not perp the other two; Q = perp all four.  Also: best 2-hub split
(greedy, rank r hubs) and max lines in rank-r subspaces containing many E-lines."""
import sys, pickle, collections, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; G = g.G; LA = np.array(g.LA, dtype=float)
part = pickle.load(open('../i13a/pg23_partition.pkl', 'rb'))
orth = lambda a, b: a != b and G[a, b] == 0
rk = lambda S: int(np.linalg.matrix_rank(LA[sorted(S)])) if S else 0
E = {}; Qs = []
for f in part:
    Qs.append([u for u in range(V) if all(orth(u, x) for x in f)])
    for i, t in enumerate(f):
        for e in f[i + 1:]:
            o = [x for x in f if x not in (t, e)]
            E[(t, e, g.kind[f[0]] + g.kind[f[1]] + g.kind[f[2]] + g.kind[f[3]])] = [u for u in range(V) if orth(u, t) and orth(u, e) and not orth(u, o[0]) and not orth(u, o[1])]
# pattern classes: for each frame, line patterns (number of frame members it is perp to)
pat = collections.Counter()
for f in part:
    for u in range(V):
        if u in f: continue
        pat[sum(orth(u, x) for x in f)] += 1
print('frames', len(part), 'perp-count distribution over (frame, line):', sorted(pat.items()))
print('Q sizes/ranks', sorted(collections.Counter((len(q), rk(q)) for q in Qs).items()))
stat = collections.Counter()
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 60
items = list(E.items()); items = items[:lim] if lim > 0 else items[lim:]
for k, S in items:
    r = rk(S); res = []
    for hr in (5, 6, 7, 8):
        basis = []; cov = set()
        for _ in range(hr):
            best = None
            for u in S:
                if u in cov: continue
                B = basis + [u]
                if rk(B) <= len(basis): continue
                c = [x for x in S if rk(B + [x]) == len(B)]
                if best is None or len(c) > len(best[1]): best = (u, c)
            if best is None: break
            basis.append(best[0]); cov = set(best[1])
        rest = [x for x in S if x not in cov]
        res.append((hr, len(cov), rk(rest)))
    stat[(k[2], len(S), r)] += 1
    print(k, 'E size', len(S), 'rank', r, 'greedy hub (r, covered, rank rest):', res, flush=True)
print(sorted(stat.items()))
