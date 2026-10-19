"""Replay a word (gcheck semantics, no checks) and report the climb sequences by register role."""
import json, gzip, sys
from fractions import Fraction as Fr
from collections import Counter
path = sys.argv[1]
w = json.load((gzip.open if path.endswith('.gz') else open)(path, 'rt'))
h, v, R = w['h'], w['v'], w['R']
def rank(vs):
    m = [[Fr(x) for x in r] for r in vs]; rk = 0
    for c in range(h):
        p = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[rk], m[p] = m[p], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]; m[i] = [a - f * b for a, b in zip(m[i], m[rk])]
        rk += 1
    return rk
dims = [rank(F) if F else 0 for F in w['frames']]
nreg = 2 * v + R
cur = list(w['start']); seq = [[] for _ in range(nreg)]; reads = Counter(); gates_at = [Counter() for _ in range(nreg)]
def climb(r, F):
    if cur[r] != F: seq[r].append(dims[F] - dims[cur[r]]); cur[r] = F
for ph in ('D', 'A'):
    for F, d, srcs in w[ph]:
        for r in [d] + srcs: climb(r, F)
for ph in ('B', 'C'):
    for F, d, srcs in w[ph]:
        for r in [d] + srcs: climb(r, F)
        if ph == 'B' and v <= d < 2 * v: reads[d] += len(srcs)
for r in range(nreg): climb(r, w['final'][r])
roles = {'source': range(v), 'target': range(v, 2 * v), 'helper': range(2 * v, nreg)}
print(path.split('/')[-1], 'v', v, 'h', h, 'R', R)
for nm, rg in roles.items():
    nc = Counter(len(seq[r]) for r in rg); pat = Counter(tuple(seq[r]) for r in rg)
    hist = Counter(x for r in rg for x in seq[r])
    print('  %-7s climbs/reg %s | hist %s' % (nm, dict(sorted(nc.items())), dict(sorted(hist.items()))))
    print('          top patterns', pat.most_common(6))
print('  B-reads per target', dict(sorted(Counter(reads[v + t] for t in range(v)).items())))
