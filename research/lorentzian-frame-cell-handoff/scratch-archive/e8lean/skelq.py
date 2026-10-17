"""E8, R420 quad skeleton (60 quads): for every plane Q (orthogonal pair or A2) the skeleton quads inside Q-perp;
then for target t: 4-plane covers {Q_i ∋ t} such that the lines of the quads feeding Q_i (with #quads >= |Q_i|)
cover R(t).  Also the R420 frame covers for comparison."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
quads = G.quads
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
t = 0; R = e8.HYP[t]
planes = {}
for u in range(V):
    if u == t: continue
    F, d = e8.closure((1 << t) | (1 << u))
    planes[F] = None
info = {}
for Q in planes:
    P = perpmask(Q)
    qs = [i for i, U in enumerate(quads) if U & ~P == 0]
    cov = 0
    for i in qs: cov |= quads[i]
    info[Q] = (pc(Q), qs, cov & R)
print('planes through t:', len(planes), ' by (size, #skeleton quads inside perp):',
      collections.Counter((v[0], len(v[1])) for v in info.values()))
good = [Q for Q, v in info.items() if len(v[1]) >= v[0]]
print('planes with enough feeding quads:', len(good))
best = 0; nc = 0
for comb in itertools.combinations(good, 4):
    m = 0
    for Q in comb: m |= info[Q][2]
    c = pc(m)
    best = max(best, c)
    if m == R: nc += 1
print('4-plane covers via skeleton-quad lines:', nc, ' best coverage', best, 'of', pc(R))
for k in (3,):
    nc3 = sum(1 for comb in itertools.combinations(good, 3) if (info[comb[0]][2] | info[comb[1]][2] | info[comb[2]][2]) == R)
    print('3-plane covers via quad lines:', nc3)
