"""I_{11,1}: 4-covers of R(t) by line-perp sections R(t) cap u-perp (u any line != t).  For each cover type: number
of users of each section (lines in span(t,u)), and whether each section's private set (lines in no other section
of the cover) spans the section's line flat.  t = T(0,1,2) and P(0,1)."""
import sys, itertools, collections
sys.path.insert(0, '../lword')
from geom import Geom
import numpy as np
g = Geom(11); V = g.V; G = g.G
perp = [0] * V
for a in range(V):
    for b in range(V):
        if a != b and G[a, b] == 0: perp[a] |= 1 << b
pc = lambda m: bin(m).count('1')
def users(t, u):
    A = np.vstack([g.LA[t], g.LA[u]])
    r = np.linalg.matrix_rank(A)
    return sum(1 for z in range(V) if np.linalg.matrix_rank(np.vstack([A, g.LA[z]])) == r)
for t in (g.T(0, 1, 2), g.P(0, 1)):
    R = perp[t]
    sec = {u: R & perp[u] for u in range(V) if u != t}
    by_line = collections.defaultdict(list)
    for u, m in sec.items():
        for s in g.bits(m): by_line[s].append(u)
    mx = max(pc(m) for m in sec.values())
    covers = set()
    def rec(unc, k, chosen):
        if unc == 0: covers.add(tuple(sorted(chosen))); return
        if k == 0 or pc(unc) > mx * k: return
        s = (unc & -unc).bit_length() - 1
        for u in by_line[s]:
            if u in chosen: continue
            rec(unc & ~sec[u], k - 1, chosen + [u])
    rec(R, 4, [])
    print(g.kind[t], g.supp[t], 'readers', pc(R), '4-covers by sections:', len(covers), flush=True)
    stat = collections.Counter(); uc = {}
    for cv in covers:
        key = []
        for u in cv:
            if u not in uc: uc[u] = users(t, u)
            others = 0
            for w in cv:
                if w != u: others |= sec[w]
            P = sec[u] & ~others
            key.append((uc[u], pc(sec[u]), pc(P), 'span' if (P and g.dim(P) == g.dim(sec[u])) else ('empty' if not P else 'proper')))
        stat[tuple(sorted(key))] += 1
    for k, n in stat.most_common(12): print('   ', n, k)
