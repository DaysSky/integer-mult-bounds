"""Ballpark: P111-tuned chains with Delta helpers removed (average helper chain mix) and targets on 0->4->6->7."""
import gzip, json, sys, collections
sys.path.insert(0, '../price')
from pricer import price
from mpmath import mp
import numpy as np
c = json.load(gzip.open(sys.argv[1], 'rt'))
v, R = c['v'], c['R']; nreg = 2 * v + R
lines = c['lines']; fr = c['frames']
fdim = [int(np.linalg.matrix_rank(np.array([lines[i] for i in f], dtype=float))) if f else 0 for f in fr]
cur = list(c['start']); chain = [[fdim[cur[r]]] for r in range(nreg)]
def step(r, f):
    if cur[r] != f: cur[r] = f; chain[r].append(fdim[f])
for ph in ('D', 'A', 'B', 'C'):
    for f, d, srcs in c[ph]:
        for x in [d] + srcs: step(x, f)
for r in range(nreg): step(r, c['final'][r])
def hist(chs):
    h = collections.Counter()
    for ch in chs:
        for a, b in zip(ch, ch[1:]): h[b - a] += 1
    return h
src = [chain[r] for r in range(v)]; tgt = [chain[r] for r in range(v, 2 * v)]; hl = [chain[r] for r in range(2 * v, nreg)]
hh = hist(hl)
P = mp.mpf('0.001733427039589844234749')
for newtgt in (False, True):
    for D in (0, 30, 60, 90, 120):
        keep = [hl[i] for i in range(len(hl)) if not (D and (i * D) // len(hl) != ((i + 1) * D) // len(hl))]
        assert len(keep) == R - D, (len(keep), R - D)
        h = hist(src) + hist([[0, 4, 6, 7]] * v if newtgt else tgt) + hist(keep)
        h[7] += 9
        mass = sum(k * n for k, n in h.items())
        assert mass == 8 * (R - D) + 63 + 14 * v, (mass, 8 * (R - D) + 63 + 14 * v)
        cc = price(dict(h), v, 8, R - D)[0]
        print('targets %-12s R=%d (drop %3d whole helpers): c=%s (%+.2f%% vs P111t)' % ('0-4-6-7' if newtgt else 'as P111', R - D, D, mp.nstr(cc, 8), float((cc / P - 1) * 100)), flush=True)
