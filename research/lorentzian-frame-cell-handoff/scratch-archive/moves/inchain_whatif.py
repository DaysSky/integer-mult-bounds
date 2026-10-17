"""What-if (histogram level, exact pricer): k targets read one t-perp register in-chain at its D6 instead of at t-perp.
Per such target: needer ...6->7->8 becomes 6->8; target 0->2->7 becomes 0->2->6->7.  Net: -{1,5} +{2,4}."""
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
h0 = collections.Counter()
for ch in chain:
    for a, b in zip(ch, ch[1:]): h0[b - a] += 1
h0[7] += 9
c0 = price(dict(h0), v, 8, R)[0]
print('base', mp.nstr(c0, 12), dict(sorted(h0.items())))
tg = collections.Counter(tuple(chain[r]) for r in range(v, 2 * v)); print('target chains', tg.most_common(5))
# registers ending ...,6,7,8
n678 = sum(1 for r in range(nreg) if len(chain[r]) >= 3 and chain[r][-3:] == [6, 7, 8]); print('registers ending 6-7-8:', n678)
for k in (28, 56, 111):
    h = collections.Counter(h0); h[1] -= k; h[5] -= k; h[2] += k; h[4] += k
    p = price(dict(h), v, 8, R)[0]; print('k=%3d  c=%s  %+.3f%%' % (k, mp.nstr(p, 12), float((p / c0 - 1) * 100)))
# variant: target reads at D6 and does NOT go to t-perp at all is impossible (needs t-perp reads of other needers)
