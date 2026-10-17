"""Run histograms per register class in P111-tuned (per local word): data x (sources), data y (targets), helpers,
copies.  A run = one maximal climb between consecutive distinct frames (a paid child)."""
import gzip, json
import numpy as np
from collections import Counter
w = json.load(gzip.open('bitE8mut-p111-e1.json.gz', 'rt'))
v = w['v']; R = w['R']; n = 2 * v + R
L = np.array(w['lines'], dtype=float)
fd = [int(np.linalg.matrix_rank(L[f])) if f else 0 for f in w['frames']]
cur = list(w['start']); hist = {'x': Counter(), 'y': Counter(), 'h': Counter()}
kind = lambda r: 'x' if r < v else ('y' if r < 2 * v else 'h')
def climb(r, f):
    if cur[r] != f:
        d = fd[f] - fd[cur[r]]; assert d > 0
        hist[kind(r)][d] += 1; cur[r] = f
for sec in ('D', 'A'):
    for f, d, srcs in w[sec]:
        for r in [d] + srcs: climb(r, f)
for f, d, srcs in w['B']:
    for r in [d] + srcs: climb(r, f)
for f, d, srcs in w['C']:
    for r in [d] + srcs: climb(r, f)
for r in range(n): climb(r, w['final'][r])
tot = Counter()
for k in hist:
    print(k, dict(sorted(hist[k].items())), 'runs', sum(hist[k].values()), 'mass', sum(a * b for a, b in hist[k].items()))
    tot.update(hist[k])
tot[7] += 9   # copies (rank 7 each)
print('total incl copies', dict(sorted(tot.items())), 'mass', sum(a * b for a, b in tot.items()))
