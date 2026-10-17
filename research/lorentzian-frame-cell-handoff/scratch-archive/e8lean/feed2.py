"""Intrinsic E-covers of a D6 (good frame) in E8, with each flat's potential sharing = number of orthogonal line pairs
{p,q} inside W-perp whose D6 {p,q}-perp contains W (all of them), i.e. how many D6s of ANY partition could share W."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V
pc = lambda m: bin(m).count('1')
c2 = G.cells[0]; H = G.D6[c2]; Hl = e8.bits(H); E = G.esum(c2)
flats = {0: 0}; frontier = [0]
while frontier:
    nf = []
    for F in frontier:
        for s in Hl:
            if F >> s & 1: continue
            Fc, d = e8.closure(F | (1 << s))
            if Fc not in flats: flats[Fc] = d; nf.append(Fc)
    frontier = nf
def perp_lines(F):
    return [s for s in range(V) if all(e8.GI[s, x] == 0 for x in e8.bits(F))]
def pot(F):
    P = perp_lines(F)
    return sum(1 for a, b in itertools.combinations(P, 2) if e8.GI[a, b] == 0)
prop = [F for F in flats if 0 < flats[F] < 6]
cov = collections.Counter(); seen = {}
for W1, W2 in itertools.combinations(prop, 2):
    if (W1 | W2) & E == E:
        for W in (W1, W2):
            if W not in seen: seen[W] = (flats[W], pc(W), pc(W & E), len(perp_lines(W)), pot(W))
        cov[tuple(sorted((seen[W1], seen[W2])))] += 1
print('cover types: ((rank, lines, E-lines, perp lines, orthogonal pairs in perp) x2): count')
for k, n in sorted(cov.items(), key=lambda kv: -min(x[4] for x in kv[0])):
    print('  ', n, k)
