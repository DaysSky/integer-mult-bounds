"""Rectangle tops for I_{11,1}: a demand d (line set) with user set U (every user perp every line of d).  Families:
 K5: apex D5 K_h(S5) (20 lines), users K_h(S5') (S5' = rest of [11]-h), 2772 demands;
 L5: coordinate D5 L(S5) (20 lines: P and T inside S5), users = lines perp all of it;
 K4: star block K_h(S4) (12 lines), users = lines perp all of it (star D6 etc.);
 generic: any rank-r closed set from a pool, users = its perp lines.
Question 1: is the all-ones vector over ordered orthogonal pairs (t, u) in the F2 span of the rectangle indicators?
usage: rectcover.py FAMILIES (comma list of K5,L5,K4,K3,L4)"""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a, b))))]; T = lambda a, b, c: idx[('T', tuple(sorted((a, b, c))))]
OM = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: OM[i] |= 1 << j
pairs = [(t, u) for t in range(V) for u in range(V) if OM[t] >> u & 1]
pid = {p: i for i, p in enumerate(pairs)}
print('ordered orthogonal pairs', len(pairs), flush=True)
def users(dmask):
    out = 0
    for t in range(V):
        if dmask & ~OM[t] == 0: out |= 1 << t
    return out
def Kset(h, S): return [P(a, b) for a, b in itertools.combinations(S, 2)] + [T(a, b, h) for a, b in itertools.combinations(S, 2)]
def Lset(S): return [P(a, b) for a, b in itertools.combinations(S, 2)] + [T(*c) for c in itertools.combinations(S, 3)]
fams = sys.argv[1].split(',')
dem = set()
for h in range(11):
    rest = [i for i in range(11) if i != h]
    for k in (3, 4, 5, 6):
        if 'K%d' % k not in fams: continue
        for S in itertools.combinations(rest, k): dem.add(frozenset(Kset(h, S)))
for k in (3, 4, 5, 6):
    if 'L%d' % k not in fams: continue
    for S in itertools.combinations(range(11), k): dem.add(frozenset(Lset(S)))
cols = []; info = []
for d in dem:
    dm = sum(1 << u for u in d); U = users(dm)
    if not U: continue
    col = 0; tt = U
    while tt:
        b = tt & -tt; t = b.bit_length() - 1; tt ^= b
        for u in d: col |= 1 << pid[(t, u)]
    cols.append(col); info.append((len(d), bin(U).count('1')))
print('rectangles', len(cols), 'size x users distribution', sorted(collections.Counter(info).items())[:12], flush=True)
# F2 rank and membership of all-ones
target = (1 << len(pairs)) - 1
basis = {}   # pivot bit -> vector
for c in cols:
    x = c
    while x:
        p = x.bit_length() - 1
        if p in basis: x ^= basis[p]
        else: basis[p] = x; break
print('rank of rectangle span', len(basis), 'of', len(pairs), flush=True)
x = target
while x:
    p = x.bit_length() - 1
    if p in basis: x ^= basis[p]
    else: break
print('all-ones in span:', x == 0, '| residual weight', bin(x).count('1'))
