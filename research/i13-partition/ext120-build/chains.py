"""Per-register frame chains of a gcheck-format word: the dims sequence of each register, grouped by role."""
import json, sys
from collections import Counter, defaultdict
from fractions import Fraction as Fr
w = json.load(open(sys.argv[1]))
h, v, R = w['h'], w['v'], w['R']
import numpy as np
def rank(F): return int(np.linalg.matrix_rank(np.array(F, dtype=float))) if F else 0
dims = [rank(F) for F in w['frames']]
nreg = 2 * v + R
chain = [[w['start'][r]] for r in range(nreg)]
reads = defaultdict(list)   # register -> list of (phase, frame)
def go(gates, ph):
    for F, d, srcs in gates:
        for r in [d] + srcs:
            if chain[r][-1] != F: chain[r].append(F)
        for s in srcs: reads[s].append((ph, F, d))
for ph in ('D', 'A'): go(w[ph], ph)
for ph in ('B', 'C'): go(w[ph], ph)
for r in range(nreg):
    if chain[r][-1] != w['final'][r]: chain[r].append(w['final'][r])
role = lambda r: 'src' if r < v else ('tgt' if r < 2 * v else 'hlp')
pat = defaultdict(Counter)
for r in range(nreg):
    ds = [dims[f] for f in chain[r]]
    steps = tuple(b - a for a, b in zip(ds, ds[1:]))
    pat[role(r)][steps] += 1
for k in pat:
    print(k, sum(pat[k].values()), pat[k].most_common(12))
