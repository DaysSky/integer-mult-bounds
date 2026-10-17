"""For the R420 partition: for every design D6 H, its two D5 feeding flats of type (D5_j = B-perp + one d-cell axis)
and the E-lines each must carry; for each D5, list the design D6s containing it and whether they need the SAME
forced E-lines from it (forced coincidence) -- exact, all 180 D6s.  Also the (quad, D5) mixed covers: which D5s
(rank 5, 12 E-lines) and their D6 sharing + coincidence."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V
pc = lambda m: bin(m).count('1')
cells = G.cells
D6 = {c: G.D6[c] for c in cells}
Em = {c: G.esum(c) for c in cells}
Bperp = {c: G.blocks[G.comp[G.cblk[c]]] for c in cells}
# D5 candidates inside H: closure(B-perp + one E-line) has rank 5?  enumerate by adding each E-line
d5_of = collections.defaultdict(set)    # D5 mask -> set of D6 owners containing it
d5_type = {}
for c in cells:
    H = D6[c]; E = Em[c]
    for s in e8.bits(E):
        F, d = e8.closure(Bperp[c] | (1 << s))
        if d == 5:
            d5_type[F] = 'Bperp+axis'
            d5_of[F]
for F in list(d5_of):
    for c in cells:
        if F & ~D6[c] == 0: d5_of[F].add(c)
print('B-perp+axis D5s:', len(d5_of), 'E-lines carried per (D5, D6):',
      collections.Counter(pc(F & Em[c]) for F in d5_of for c in d5_of[F]))
print('D6s per D5:', collections.Counter(len(v) for v in d5_of.values()))
coin = collections.Counter()
for F, cs in d5_of.items():
    sets = {F & Em[c] for c in cs}
    coin[(len(cs), len(sets))] += 1
print('(#D6, #distinct forced E-sets):', dict(coin))
# mixed covers: D5 with 12 E-lines of H
mix = collections.defaultdict(set)
for c in cells[:180]:
    H = D6[c]; E = Em[c]
    Hl = e8.bits(H)
    # D5 = closure of a quad of H plus one more line; quads of H = d6quads
    for q in G.d6quads[c]:
        U = G.quads[q]
        for s in Hl:
            if U >> s & 1: continue
            F, d = e8.closure(U | (1 << s))
            if d == 5 and pc(F & E) == 12:
                mix[F]
for F in list(mix):
    for c in cells:
        if F & ~D6[c] == 0: mix[F].add(c)
print('quad+line D5s with 12 E-lines for some D6:', len(mix))
print('  D6s per such D5:', collections.Counter(len(v) for v in mix.values()))
print('  E-lines carried per (D5,D6):', collections.Counter(pc(F & Em[c]) for F in mix for c in mix[F]))
coin = collections.Counter()
for F, cs in mix.items():
    coin[(len(cs), len({F & Em[c] for c in cs}))] += 1
print('  (#D6, #distinct forced sets):', dict(coin))
