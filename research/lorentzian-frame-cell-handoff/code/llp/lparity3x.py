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
def nm(s): return ('P' if KIND[s] == 'P' else 'T') + ''.join('abcdefghijk'[i] for i in SUPP[s])
def show(p): return '{' + ','.join(nm(s) for s in bits(p)) + '}'
def ptype(p):
    k = ''.join(sorted(KIND[s] for s in bits(p)))
    if len(k) == 2 and G[bits(p)[0]][bits(p)[1]] != 0: k += '*'
    return k
for t in (0, 100):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = [pm(p) for p in pl]
    seen = collections.defaultdict(list)
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        D = S[i] ^ S[j] ^ S[k] ^ R
        if pc(D) == 1:
            sig = tuple(sorted((ptype(pl[i]), ptype(pl[j]), ptype(pl[k]))))
            if len(seen[sig]) < 3: seen[sig].append((pl[i], pl[j], pl[k], D))
    print('TARGET', nm(t))
    for sig, lst in seen.items():
        for a, b, c, D in lst:
            print('  ', sig, show(a), show(b), show(c), ' defect', nm(bits(D)[0]))
