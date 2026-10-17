"""Reprice P111-tuned with stated chain compressions (exact pricer, same v, R, totals).  Local histogram = moves of all
registers + COPY ranks of totals (9 x 7).  Controls: uncompressed must reproduce the published local profile."""
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
base = hist(chain)
tot = collections.Counter(base); tot[7] += 9          # nine COPY ranks 7 (retained totals)
print('replayed local profile', dict(sorted(tot.items())))
cP = price(dict(tot), v, 8, R)[0]; print('price (replayed profile):', mp.nstr(cP, 12))
def variant(drop_hlp, drop_src):
    chs = []
    for r in range(nreg):
        ch = chain[r]
        if r >= 2 * v: ch = [x for i, x in enumerate(ch) if i in (0, len(ch) - 1) or x not in drop_hlp]
        elif r < v: ch = [x for i, x in enumerate(ch) if i in (0, len(ch) - 1) or x not in drop_src]
        chs.append(ch)
    h = hist(chs); h[7] += 9
    return price(dict(h), v, 8, R)[0], h
for dh, ds, name in (({1}, set(), 'helpers skip rank-1 copy stop'), ({7}, {7}, 'skip rank-7 stops (helpers+sources)'),
                     ({1, 7}, {7}, 'both'), ({1, 2, 7}, {2, 7}, 'also skip cells'), ({1, 2, 4, 7}, {2, 7}, 'helpers 0->6->8 style')):
    p, h = variant(dh, ds)
    print('%-40s c = %s (%+.2f%%)  profile %s' % (name, mp.nstr(p, 10), float((p / cP - 1) * 100), dict(sorted(h.items()))))
