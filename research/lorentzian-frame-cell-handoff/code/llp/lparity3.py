"""Parity triples: sets of 3 plane sections through t whose mod-2 sum differs from 1_{R(t)} in few lines.
Reports, per target type, the minimum defect weight and the plane-type signature of the best triples."""
import itertools, collections
from lgeo import *
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
def ptype(p):
    k = ''.join(sorted(KIND[s] for s in bits(p)))
    if len(k) == 2 and G[bits(p)[0]][bits(p)[1]] != 0: k += '*'     # non-orthogonal 2-line plane
    return k
for t in (0, 100):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = [pm(p) for p in pl]
    hist = collections.Counter(); best = collections.defaultdict(lambda: 999); ex = {}
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        d = pc(S[i] ^ S[j] ^ S[k] ^ R)
        sig = tuple(sorted((ptype(pl[i]), ptype(pl[j]), ptype(pl[k]))))
        if d < best[sig]: best[sig] = d; ex[sig] = (i, j, k)
        if d <= 6: hist[(d, sig)] += 1
    print('target', 'P' if t < 55 else 'T', '|R|', pc(R))
    for sig in sorted(best, key=lambda s: best[s])[:12]:
        i, j, k = ex[sig]; D = S[i] ^ S[j] ^ S[k] ^ R
        print('   ', sig, 'min defect', best[sig], 'defect lines', [(KIND[s], SUPP[s]) for s in bits(D)][:6], 'rank', rank(D))
    print('   counts (defect, signature) <= 6:', sorted(hist.items())[:12])
