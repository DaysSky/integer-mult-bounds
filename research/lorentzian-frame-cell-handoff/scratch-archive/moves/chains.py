"""Per-register frame chains of the P111-tuned word: dims visited, move counts by register class."""
import gzip, json, sys, collections
from fractions import Fraction as Fr
c = json.load(gzip.open(sys.argv[1], 'rt'))
v, R = c['v'], c['R']; nreg = 2 * v + R
lines = c['lines']; fr = c['frames']
import numpy as np
def rank(idx):
    if not idx: return 0
    M = np.array([lines[i] for i in idx], dtype=float)
    return int(np.linalg.matrix_rank(M))
fdim = [rank(f) for f in fr]
cur = list(c['start']); chain = [[fdim[cur[r]]] for r in range(nreg)]
def step(r, f):
    if cur[r] != f:
        cur[r] = f; chain[r].append(fdim[f])
for ph in ('D', 'A'):
    for f, d, srcs in c[ph]:
        for x in [d] + srcs: step(x, f)
for ph in ('B', 'C'):
    for f, d, srcs in c[ph]:
        for x in [d] + srcs: step(x, f)
for r in range(nreg): step(r, c['final'][r])
cls = lambda r: 'src' if r < v else ('tgt' if r < 2 * v else 'hlp')
st = collections.defaultdict(collections.Counter)
for r in range(nreg):
    st[cls(r)][tuple(chain[r])] += 1
for k in st:
    tot = sum(st[k].values()); mv = sum((len(ch) - 1) * n for ch, n in st[k].items())
    print(k, 'registers', tot, 'avg moves', round(mv / tot, 2))
    for ch, n in st[k].most_common(8): print('   ', ch, n)
