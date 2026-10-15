"""E8 check (lines P(ij), T(ijk) on 9 points of I_{9,1}): parity triples of plane sections through t with small defect."""
import sys, os, itertools, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
import numpy as np
g = Geom(9); V = g.V; G = g.G; HYP = g.HYP; bits = g.bits
pc = lambda m: bin(m).count('1')
FULL = (1 << V) - 1
print('E8 lines', V, 'rank', g.h, '|R(t)|', pc(HYP[0]), pc(HYP[50]))
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
w = np.array([1] * 9 + [3])
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            v = g.L[a] - sg * g.L[b]
            for k in range(-3, 4):                       # modulo the null vector w
                c = VEC.get(tuple(int(x) for x in (v + k * w)))
                if c is not None and c not in (a, b): m |= 1 << c
    return m
def ptype(p):
    k = len(bits(p)); o = all(G[x][y] == 0 for x, y in itertools.combinations(bits(p), 2))
    return ('A2' if k == 3 else ('cell' if o else '2nonorth%d' % k))
for t in (0, 50):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = [pm(p) for p in pl]
    print('target', t, 'planes', len(pl), collections.Counter(ptype(p) for p in pl), 'section sizes', sorted(set(pc(s) for s in S)))
    best = collections.defaultdict(lambda: 999); cnt = collections.Counter()
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        d = pc(S[i] ^ S[j] ^ S[k] ^ R)
        sig = tuple(sorted((ptype(pl[i]), ptype(pl[j]), ptype(pl[k]))))
        best[sig] = min(best[sig], d)
        if d <= 3: cnt[(d, sig)] += 1
    for sig in sorted(best, key=lambda s: best[s]): print('   ', sig, 'min defect', best[sig])
    print('   ', sorted(cnt.items()))
