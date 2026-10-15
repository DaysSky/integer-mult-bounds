"""For a good-frame system: per target, min #unroutable lines (lines of the chosen sections with no system cell inside
the section) over good-frame triples (defect 3) and over defect-1 parity triples.  Triples of every target are images
of the two representatives' triples under a point permutation.   usage: lptopq.py SYSTEM.json [out.json]"""
import sys, json, itertools, collections
from lgeo import *
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a]) if b != a))
cells_of = collections.defaultdict(list)
for C in cells:
    for s in bits(C): cells_of[s].append(C)
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
def triples(t):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = [pm(p) for p in pl]; out = []
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        D = S[i] ^ S[j] ^ S[k] ^ R; d = pc(D)
        if d == 1 or (d == 3 and all(G[x][y] == 0 for x, y in itertools.combinations(bits(D) + [t], 2))):
            out.append((pl[i], pl[j], pl[k], D))
    return out
reps = {}
for t in range(V):
    if KIND[t] not in reps: reps[KIND[t]] = (t, triples(t))
UNR = {}
def unr(p):
    if p not in UNR:
        S = pm(p); UNR[p] = sum(1 for u in bits(S) if not any(C & ~S == 0 for C in cells_of[u]))
    return UNR[p]
best_all = {}
for t in range(V):
    r, TR = reps[KIND[t]]
    a = list(SUPP[r]); b = list(SUPP[t])
    perm = [0] * n
    for x, y in zip(a + [i for i in range(n) if i not in a], b + [i for i in range(n) if i not in b]): perm[x] = y
    bf = (999, None); b1 = (999, None)
    for p1, p2, p3, D in TR:
        q = (act(p1, perm), act(p2, perm), act(p3, perm), act(D, perm))
        u = unr(q[0]) + unr(q[1]) + unr(q[2])
        if pc(D) == 1:
            if u < b1[0]: b1 = (u, q)
        elif u < bf[0]: bf = (u, q)
    best_all[t] = (bf, b1)
print('frame-triple min unroutable per target:', sorted(collections.Counter(v[0][0] for v in best_all.values()).items()))
print('defect-1 triple min unroutable per target:', sorted(collections.Counter(v[1][0] for v in best_all.values()).items()))
print('targets fully routable: defect-1', sum(1 for v in best_all.values() if v[1][0] == 0), 'frame', sum(1 for v in best_all.values() if v[0][0] == 0))
if len(sys.argv) > 2:
    json.dump({str(t): [v[0][0], v[1][0], [hex(x) for x in v[1][1]]] for t, v in best_all.items()}, open(sys.argv[2], 'w'))
