"""Good 4-frames of I_{n,1}: 4 mutually orthogonal lines {t,e1,e2,e3} such that for each member t, every line of
R(t) minus the other three is orthogonal to an odd number of them.  Counts by type (P/T composition), up to S_n."""
import sys, itertools, collections, numpy as np, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
n = int(sys.argv[1])
g = Geom(n); V = g.V; G = g.G
orth = (G == 0); np.fill_diagonal(orth, False)
om = [int(''.join('1' if orth[i, j] else '0' for j in reversed(range(V))), 2) for i in range(V)]
def good_for(t, es):
    R = om[t] & ~sum(1 << e for e in es)
    a, b, c = (om[e] for e in es)
    return (R & ~(a ^ b ^ c)) == 0
# canonical representatives under S_n: enumerate quads containing a fixed first line per kind, then canonicalise
def canon(q):
    # canonical form under S_n: sort supports after relabelling by first appearance (cheap invariant) -> use brute
    sup = [g.supp[x] for x in q]
    pts = sorted(set(p for s in sup for p in s))
    best = None
    for perm in itertools.permutations(range(len(pts))) if len(pts) <= 8 else [None]:
        if perm is None: return tuple(sorted(sup))
        mp = {p: perm[i] for i, p in enumerate(pts)}
        key = tuple(sorted(tuple(sorted(mp[p] for p in s)) for s in sup))
        if best is None or key < best: best = key
    return best
reps = {}
cnt = collections.Counter()
for first in (0, len([k for k in g.kind if k == 'P'])):     # P line 0, T line (first T)
    t = first
    nb = [j for j in range(V) if orth[t, j]]
    for e1, e2, e3 in itertools.combinations(nb, 3):
        if not (orth[e1, e2] and orth[e1, e3] and orth[e2, e3]): continue
        q = (t, e1, e2, e3)
        if all(good_for(x, [y for y in q if y != x]) for x in q):
            typ = ''.join(sorted(g.kind[x] for x in q))
            c = canon(q)
            if c not in reps: reps[c] = (typ, q)
            cnt[typ] += 1
print('n', n, 'lines', V, 'good frames through a P line / T line by type:', dict(cnt))
print('orbit reps:', len(reps), collections.Counter(v[0] for v in reps.values()))
for c, (typ, q) in list(reps.items())[:12]: print(typ, [g.supp[x] for x in q])
pickle.dump(reps, open('good_reps_n%d.pkl' % n, 'wb'))
