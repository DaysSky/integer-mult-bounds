"""One-level reach bound (heuristic family first).  In a strict one-level middle every register visits ONE frame N
between its cell and the rank-9/10 frames; content entering N reaches only targets that read sections visited by N's
registers (<= 3 users each) and lie in perp(N).  So incidences through N <= min(a_N, 2k) * min(b_N, 3k) <= k*min(3a_N, 2b_N)
(a_N = lines covered by system cells inside N, b_N = |perp(N)|, k = registers at N).  Need
   sum_registers min(3a, 2b)(node of register) >= sum_t |R(t)| - 2V (cell reads).
Here: per-cell best value over a candidate family (pair closures, apex hubs, and their double-perp closures).
usage: lreach1.py SYSTEM.json"""
import sys, os, json, collections, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, closure, perp, g
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
def a_of(N):
    m = 0
    for C in cells:
        if C & ~N == 0: m |= C
    return pc(m)
fam = set()
for i, C in enumerate(cells):
    for D in cells[i + 1:]: fam.add(closure(C | D))
for p in range(11):
    others = [i for i in range(11) if i != p]
    for sz in (3, 4, 5, 6):
        for A in itertools.combinations(others, sz):
            m = 0
            for i, j in itertools.combinations(A, 2): m |= (1 << g.P(i, j)) | (1 << g.T(i, j, p))
            fam.add(closure(m))
fam2 = set()
for N in fam: fam2.add(perp(perp(N)))   # double-perp closure: same b, more lines
fam |= fam2
print('family size', len(fam), flush=True)
val = {}
for N in fam:
    b = pc(perp(N))
    if 2 * b <= 6: continue
    val[N] = min(3 * a_of(N), 2 * b)
best = {}
for C in cells:
    best[C] = max([v for N, v in val.items() if C & ~N == 0] + [min(6, 2 * pc(perp(C)))])
X = sum(2 * best[C] for C in cells)
Gmax = max(val.values())
req = sum(pc(HYP[t]) for t in range(V)) - 2 * V
print('cells', len(cells), 'best-value distribution', sorted(collections.Counter(best.values()).items()))
print('sum over cell registers (2/cell) of best value X =', X, '| required', req, '| Gmax', Gmax)
need_extra = max(0, req - X)
print('=> extra registers needed beyond 2/cell (each worth <= Gmax):', -(-need_extra // Gmax),
      '-> R >= 2*cells - v + that =', 2 * len(cells) - V + -(-need_extra // Gmax))
