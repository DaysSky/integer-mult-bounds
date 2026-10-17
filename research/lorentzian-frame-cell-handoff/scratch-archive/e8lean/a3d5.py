"""E8, R420 partition: the (A3, D5) E-covers of each design D6.  For each such A3: its lines' roles in H, and for
every design D6 H' containing the A3, how many of the A3's lines are E-lines of H' (and is the A3's complement
part of an (A3,D5) cover of H' as well)."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V
pc = lambda m: bin(m).count('1')
cells = G.cells
Emask = {c: G.esum(c) for c in cells}
def flats_in(H):
    Hl = e8.bits(H); fl = {0: 0}; fr = [0]
    while fr:
        nf = []
        for F in fr:
            for s in Hl:
                if F >> s & 1: continue
                Fc, d = e8.closure(F | (1 << s))
                if Fc not in fl: fl[Fc] = d; nf.append(Fc)
        fr = nf
    return fl
A3use = collections.defaultdict(list)   # A3 mask -> list of D6 owners for which it is the A3 of an (A3,D5) cover
for c2 in cells[:180]:
    H = G.D6[c2]; E = Emask[c2]
    fl = flats_in(H)
    a3s = [F for F, d in fl.items() if d == 3 and pc(F) == 6 and pc(F & E) == 4]
    d5s = [F for F, d in fl.items() if d == 5 and pc(F & E) == 12]
    for A in a3s:
        if any((A | D) & E == E for D in d5s):
            A3use[A].append(c2)
print('distinct cover-A3s', len(A3use), 'D6s per A3:', collections.Counter(len(v) for v in A3use.values()))
A = next(iter(A3use))
c2 = A3use[A][0]
H = G.D6[c2]; E = Emask[c2]
role = lambda s, c: 'E' if Emask[c] >> s & 1 else ('d' if s in G.dcell[c] else ('Q' if G.blk[s] == G.comp[G.cblk[c]] else '?'))
print('example A3 lines and roles in its D6s:')
for c in A3use[A]:
    print('  D6', c, 'block', G.cblk[c], [role(s, c) for s in e8.bits(A)])
print('A3 lines blocks:', [G.blk[s] for s in e8.bits(A)], 'frames:', [G.phi[s] for s in e8.bits(A)])
