"""Evaluate a good-frame partition of I13: demands, sharing, load, F2 rank, misalignment (odd E-set/frame pairs),
pool cover on sample lines (line partners).  usage: eval13.py PART.pkl"""
import sys, pickle, itertools, collections
from geo13 import *
from ortools.sat.python import cp_model
part = pickle.load(open(sys.argv[1], 'rb'))
OM = HYP
DEM = []
for fi, f in enumerate(part):
    Q = OM[f[0]] & OM[f[1]] & OM[f[2]] & OM[f[3]]
    DEM.append(('Q', Q, Q, fi, f))
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        E = OM[f[a]] & OM[f[b]] & ~OM[f[o[0]]] & ~OM[f[o[1]]]
        DEM.append(('E', OM[f[a]] & OM[f[b]], E, fi, (f[a], f[b])))
halves = collections.Counter()
for fi, f in enumerate(part):
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        E = OM[f[a]] & OM[f[b]] & ~OM[f[o[0]]] & ~OM[f[o[1]]]
        k, l = f[o[0]], f[o[1]]
        Ep = sum(1 << u for u in bits(E) if G[u, k] == G[u, l]); Em = E & ~Ep
        for hh in (Ep, Em):
            if hh: halves[hh] += 1
def f2rank(vecs):
    basis = {}; r = 0
    for x in set(vecs):
        while x:
            hb = x.bit_length() - 1
            if hb in basis: x ^= basis[hb]
            else: basis[hb] = x; r += 1; break
    return r
dist = set(d[2] for d in DEM)
inc = sum(pc(d) for d in dist)
hinc = sum(pc(h) for h in halves) + sum(pc(q) for q in set(d[2] for d in DEM if d[0] == "Q"))
print('frames', len(part), collections.Counter(''.join(sorted(g.kind[x] for x in f)) for f in part))
print('demands', len(DEM), 'distinct E/Q contents', len(dist), 'incidences', inc, 'load/line %.1f' % (inc / V))
print('halves distinct', len(halves), 'slots', sum(halves.values()), 'sharing %.2f' % (sum(halves.values()) / len(halves)),
      'half+Q incidences', hinc, 'load/line %.1f' % (hinc / V))
print('F2 rank demands', f2rank(list(dist)), 'halves', f2rank(list(halves)))
fm = [sum(1 << x for x in f) for f in part]
odd = sum(1 for d in dist for m in fm if pc(d & m) & 1)
print('misalignment (odd (demand, frame) pairs)', odd)
