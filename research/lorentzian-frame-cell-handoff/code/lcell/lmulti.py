"""One-level plausibility probe: for each cell C of a system, nodes N = closure(C u C') (C' another system cell):
#system cells inside N and fraction of C's forced targets (D u S u A) lying in perp(N).  Reports, per cell, the best
coverage achievable by a node holding >= 3 cells, and by any node."""
import sys, os, json, collections
os.environ['GRP'] = '11'
from lbase import *
pc_ = lambda m: bin(m).count('1')
P = {}
def pm(m):
    if m not in P: P[m] = perp(m)
    return P[m]
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
hist3 = collections.Counter(); histany = collections.Counter(); ncells = collections.Counter()
for C in cells[::3]:
    s, a = list(bits(C)); os_ = 0; oa_ = 0
    for c in co[s]:
        if c != C: os_ |= pm(c)
    for c in co[a]:
        if c != C: oa_ |= pm(c)
    PC = pm(C); F = (PC & ~os_) | (PC & ~oa_)
    nF = pc_(F)
    if not nF: continue
    best3 = 0; bestany = 0
    for C2 in cells:
        if C2 == C or C2 & ~PC == 0 and False: pass
        if C2 == C: continue
        N = closure(C | C2)
        k = sum(1 for c in cells if c & ~N == 0)
        cov_ = pc_(F & pm(N)) / nF
        bestany = max(bestany, cov_)
        if k >= 3: best3 = max(best3, cov_)
        ncells[k] += 1
    hist3[round(best3, 1)] += 1; histany[round(bestany, 1)] += 1
print('best forced-target coverage by a node with >= 3 cells (fraction):', sorted(hist3.items()))
print('best coverage by any closure(C u C\'):', sorted(histany.items()))
print('cells per closure(C u C\') node:', sorted(ncells.items())[:12])
