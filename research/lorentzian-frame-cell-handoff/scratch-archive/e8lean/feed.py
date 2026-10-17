"""E8, R420 partition: all flats W inside a design D6 H (closures of line subsets of H), the number of design D6s
containing W, and every unordered pair (W1, W2) of proper sub-flats of H whose union covers E(H).  Reports the
cover types by (rank, #lines, #D6 sharing)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V
cells = G.cells; cm = G.cmask
D6 = {c2: G.D6[c2] for c2 in cells}
pc = lambda m: bin(m).count('1')
c2 = cells[0]
H = D6[c2]; Hl = e8.bits(H)
E = G.esum(c2)
print('D6', c2, 'lines', len(Hl), 'E', pc(E), 'dcell', G.dcell[c2])
# enumerate all flats of H by BFS closure
flats = {0: 0}
frontier = [0]
while frontier:
    nf = []
    for F in frontier:
        for s in Hl:
            if F >> s & 1: continue
            Fc, d = e8.closure(F | (1 << s))
            if Fc not in flats:
                flats[Fc] = d; nf.append(Fc)
    frontier = nf
print('flats inside H:', len(flats), collections.Counter(flats.values()))
share = {F: sum(1 for c in cells if F & ~D6[c] == 0) for F in flats}
prop = [F for F in flats if 0 < flats[F] < 6]
covers = collections.Counter(); best = []
for W1, W2 in itertools.combinations(prop, 2):
    if (W1 | W2) & E == E:
        k = tuple(sorted(((flats[W1], pc(W1), share[W1]), (flats[W2], pc(W2), share[W2]))))
        covers[k] += 1
for F in prop:
    if F & E == E: covers[((flats[F], pc(F), share[F]),)] += 1
print('E-covers by two proper sub-flats (rank, lines, D6-sharing):')
for k, n in sorted(covers.items(), key=lambda kv: (-min(x[2] for x in kv[0]), kv[0])):
    print('  ', n, k)
