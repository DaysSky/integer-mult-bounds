"""E8: 4-covers of R(t) by rank-5 flats.  Which flat types occur in 4-covers; for D5 flats W, W-perp is an A3 (6
lines) containing t.  Enumerate A3 subsystems containing t and 4-subsets whose perps cover R(t)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
perp = e8.HYP
# all A3 subsystems: closures of two non-orthogonal... A3 = rank-3 flat with 6 lines
A3 = set()
for a in range(V):
    for b in range(a + 1, V):
        for c in range(b + 1, V):
            pass
# faster: rank-3 flats containing a given line via closures of triples incl. t
def a3s_through(t):
    out = set()
    for a in range(V):
        if a == t: continue
        for b in range(a + 1, V):
            if b == t: continue
            F, d = e8.closure((1 << t) | (1 << a) | (1 << b))
            if d == 3 and pc(F) == 6: out.add(F)
    return out
t = 0
X = sorted(a3s_through(t))
print('A3s through line 0:', len(X))
R = perp[t]
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= perp[s]
    return m
cov = {F: perpmask(F) & R for F in X}
print('X-perp cap R(t) sizes:', collections.Counter(pc(c) for c in cov.values()))
n4 = 0; ex = None
Xl = list(X)
for comb in itertools.combinations(range(len(Xl)), 4):
    m = 0
    for i in comb: m |= cov[Xl[i]]
    if m == R:
        n4 += 1
        if ex is None: ex = comb
print('4-subsets of A3s through t whose perps cover R(t):', n4)
if ex:
    for i in ex:
        F = Xl[i]; print('  A3 lines', e8.bits(F), 'perp lines in R(t):', pc(cov[F]))
    # pairwise intersections of the A3s (other than t)
    for i, j in itertools.combinations(ex, 2):
        print('   A3 intersection lines', e8.bits(Xl[i] & Xl[j]))
    # overlaps of the covers
    tot = sum(pc(cov[Xl[i]]) for i in ex)
    print('   sum of section sizes', tot, 'vs 63')
