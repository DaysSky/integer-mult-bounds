"""All 3-element partner sets N of a line s (N in s-perp, every target t in s-perp has a partner != t in t-perp).
Classify by the orthogonality pattern inside N (a good frame {s} + N is the R420 case: N pairwise orthogonal)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
G = g.G
def run(lines, s, label):
    P = [x for x in lines if x != s and G[s, x] == 0]
    idx = {t: i for i, t in enumerate(P)}
    full = (1 << len(P)) - 1
    # hit[u] = set of targets t in P (t != u) with u in t-perp
    hit = {u: sum(1 << idx[t] for t in P if t != u and G[t, u] == 0) for u in P}
    sols = []
    for a, b, c in itertools.combinations(P, 3):
        if hit[a] | hit[b] | hit[c] == full: sols.append((a, b, c))
    pat = collections.Counter()
    for a, b, c in sols:
        o = sum(1 for x, y in ((a, b), (a, c), (b, c)) if G[x, y] == 0)
        pat[o] += 1
    print('%s s = %s %s: |s-perp| %d, partner triples %d, by number of orthogonal pairs inside N: %s' % (
        label, g.kind[s], tuple(g.supp[s]), len(P), len(sols), dict(sorted(pat.items()))), flush=True)
    return sols
allL = list(range(V))
run(allL, 0, 'I11'); run(allL, 55, 'I11')
M = [x for x in range(V) if 9 not in g.supp[x] and 10 not in g.supp[x]]
run(M, M[0], 'E8(M)'); run(M, M[-1], 'E8(M)')
