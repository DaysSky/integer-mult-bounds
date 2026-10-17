import sys, collections, itertools, json
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V; GI = e8.GI
cls = {tuple(map(int, k.split('_'))): frozenset(v) for k, v in json.load(open('classes.json')).items()}
cellset = set(G.cells)
pieces = collections.Counter()
piece_in = collections.defaultdict(set)
for (a, x), S in cls.items():
    if a > x: continue
    byb = collections.defaultdict(list)
    for s in S: byb[G.blk[s]].append(s)
    for b, ls in byb.items():
        p = tuple(sorted(ls))
        kind = 'cell' if p in cellset else ('orth' if GI[p[0], p[1]] == 0 else 'A2')
        pieces[kind] += 1
        piece_in[p].add((a, x))
print('pieces by kind', dict(pieces))
print('distinct pieces', len(piece_in), 'each used by', collections.Counter(len(v) for v in piece_in.values()))
# per piece: which top contents use it; are they all in one block pair / share structure?
p0 = next(iter(piece_in))
print('example piece', p0, 'used by', sorted(piece_in[p0])[:8])
# quads: G.quads (4-dim D4 frames of 6 cells from 6 blocks). For each class, decompose into quad-supported chunks?
print('n quads', len(G.quads))
qcells = [set(G.qcells[q]) for q in range(len(G.quads))]
# which quads contain >= 2 of a class's cells
cnt = collections.Counter()
for (a, x), S in cls.items():
    if a > x: continue
    cs = set()
    byb = collections.defaultdict(list)
    for s in S: byb[G.blk[s]].append(s)
    for b, ls in byb.items(): cs.add(tuple(sorted(ls)))
    hits = sorted((len(cs & qc), q) for q, qc in enumerate(qcells) if len(cs & qc) >= 2)
    cnt[tuple(h for h, q in hits)] += 1
print('per class: multiset of #cells shared with quads (>=2):', dict(cnt))
