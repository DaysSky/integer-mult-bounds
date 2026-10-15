"""All exact 3-section union covers of R(t) by pair-plane sections {t,e}-perp, for every line t (mates triples).
Representatives enumerated exhaustively, mapped to all lines by S11 point permutations.  Saves covers3.pkl:
{t: [(e1,e2,e3), ...]} plus a 'good' flag per triple (good 4-frame: pairwise orthogonal, sum in 2L)."""
import itertools, pickle
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
rep = {}
for kind in ('P', 'T'):
    t = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[t]
    mates = [e for e in range(V) if e != t and pc(plane_of(t, e)) == 2]
    S = {e: HYP[t] & HYP[e] for e in mates}
    out = []
    for a, b, c in itertools.combinations(mates, 3):
        if (S[a] | S[b] | S[c]) == R: out.append((a, b, c))
    rep[kind] = (t, out)
    print(kind, 'exact pair-section covers', len(out), flush=True)
cov = {}
for s in range(V):
    r, TR = rep[KIND[s]]
    a_ = list(SUPP[r]); b_ = list(SUPP[s]); perm = [0] * n
    for x, y in zip(a_ + [i for i in range(n) if i not in a_], b_ + [i for i in range(n) if i not in b_]): perm[x] = y
    lst = []
    for tr in TR:
        ms = tuple(sorted(img_line(e, perm) for e in tr))
        good = all(G[x][y] == 0 for x, y in itertools.combinations((s,) + ms, 2)) and all(int(z) % 2 == 0 for z in g.L[[s] + list(ms)].sum(axis=0))
        lst.append((ms, good))
    cov[s] = lst
    # sanity: exact cover
    for ms, gd in lst[:3]:
        assert (HYP[s] & HYP[ms[0]]) | (HYP[s] & HYP[ms[1]]) | (HYP[s] & HYP[ms[2]]) == HYP[s]
pickle.dump(cov, open('covers3.pkl', 'wb'))
print('saved; options per line', sorted(set(len(v) for v in cov.values())), 'good per line', sorted(set(sum(gd for _, gd in v) for v in cov.values())))
