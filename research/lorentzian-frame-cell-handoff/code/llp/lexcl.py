"""For every 3-section top (frame triples, defect-1 triples) of the representative targets: per section, the exclusive
lines (lines of R(t) in exactly that one section), the closure of that set, and whether it is a PROPER node (closure !=
whole section line set).  If proper: its line count and number of sink planes (shareability)."""
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
def nplanes(N):
    P = bits(pm(N)); return len(set(plane_of(a, b) for i, a in enumerate(P) for b in P[i + 1:]))
for t in (0, 100):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = {p: pm(p) for p in pl}
    stat = collections.Counter(); proper_ex = collections.Counter()
    for i, j, k in itertools.combinations(pl, 3):
        D = S[i] ^ S[j] ^ S[k] ^ R; d = pc(D)
        if not (d == 1 or (d == 3 and all(G[x][y] == 0 for x, y in itertools.combinations(bits(D) + [t], 2)))): continue
        for a, b, c in ((i, j, k), (j, i, k), (k, i, j)):
            ex = S[a] & ~S[b] & ~S[c]
            N = pp(ex)
            key = (d, pc(a), pc(S[a]), pc(ex), N == S[a])
            stat[key] += 1
            if N != S[a]: proper_ex[(d, pc(a), pc(S[a]), pc(ex), pc(N), rank(N), nplanes(N))] += 1
    print('target', KIND[t])
    for k, v in sorted(stat.items()): print('   (defect, plane, section, |excl|, closure==section):', k, 'x', v)
    for k, v in sorted(proper_ex.items()): print('   PROPER exclusive closure (defect, plane, section, |excl|, |closure|, rank, sink planes):', k, 'x', v)
