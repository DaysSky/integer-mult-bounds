"""For a (partial) good-frame partition: are the E-sets of each cell's section unions of partition cells?
How many sections need each cell?  usage: cellunion.py PART.pkl   (frames list, punctured list)"""
import sys, pickle, collections, random
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
pc = lambda m: bin(m).count('1')
orthm = [sum(1 << j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
frames, pun = pickle.load(open(sys.argv[1], 'rb'))
phi = {x: f for f in frames for x in f}
cells = [(a, b) for f in frames for i, a in enumerate(f) for b in f[i + 1:]]
cmask = {c: (1 << c[0]) | (1 << c[1]) for c in cells}
E = {}
for (t, e) in cells:
    o = [x for x in phi[t] if x not in (t, e)]
    E[(t, e)] = orthm[t] & orthm[e] & ~orthm[o[0]] & ~orthm[o[1]]
# E-set as union of cells: count lines whose E-set membership is covered by a whole cell inside E
stat = collections.Counter(); need = collections.Counter(); whole = 0; tot = 0
for H, m in E.items():
    inside = [c for c in cells if cmask[c] & ~m == 0]
    cov = 0
    for c in inside: cov |= cmask[c]
    stat[(pc(m), pc(m & ~cov))] += 1
    for c in inside: need[c] += 1
print('E-set size, lines not in a whole inside cell -> count:', sorted(stat.items())[:30])
print('sections needing a cell (whole cell in E): min/mean/max', min(need.values()), sum(need.values()) / len(cells), max(need.values()))
