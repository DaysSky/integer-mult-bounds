"""E8 on the R420 partition: A3 flats made of 3 design cells, and how D6 E-sets decompose into them."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V
cells = G.cells; cm = G.cmask
cellset = set(cells)
cell_of_mask = {cm[c]: c for c in cells}
# A3 flats spanned by design cells: closure of two cells with rank 3 containing exactly 3 cells / 6 lines
a3 = {}
for c1, c2 in itertools.combinations(cells, 2):
    m = cm[c1] | cm[c2]
    F, d = e8.closure(m)
    if d == 3:
        a3.setdefault(F, set())
for F in a3:
    a3[F] = [c for c in cells if cm[c] & ~F == 0]
print('rank-3 flats spanned by two design cells:', len(a3))
print('  by (#lines, #design cells):', collections.Counter((bin(F).count('1'), len(cs)) for F, cs in a3.items()))
good = {F: cs for F, cs in a3.items() if bin(F).count('1') == 6 and len(cs) == 3}
print('A3 flats = 3 design cells:', len(good))
# blocks of the three cells
print('  block patterns:', collections.Counter(tuple(sorted(collections.Counter(G.cblk[c] for c in cs).values())) for cs in good.values()))
# D6 containment
D6s = {c2: G.D6[c2] for c2 in cells}
cont = {F: [c2 for c2 in cells if F & ~D6s[c2] == 0] for F in good}
print('  #design D6 containing an A3:', collections.Counter(len(v) for v in cont.values()))
# for each D6: E-cells, and which A3s inside the D6 contain 2 E-cells + the dcell
ecell = {}
for c2 in cells:
    em = G.esum(c2)
    ecell[c2] = [c for c in cells if cm[c] & ~em == 0]
    assert len(ecell[c2]) == 8
stats = collections.Counter()
for c2 in cells:
    inside = [F for F in good if F & ~D6s[c2] == 0]
    roles = collections.Counter()
    for F in inside:
        cs = good[F]
        ne = sum(1 for c in cs if c in ecell[c2]); nd = sum(1 for c in cs if c == G.dcell[c2])
        roles[(ne, nd)] += 1
    stats[tuple(sorted(roles.items()))] += 1
print('per D6: A3s inside by (#E-cells, has dcell):')
for k, n in stats.items(): print('   ', n, 'D6s:', k)
