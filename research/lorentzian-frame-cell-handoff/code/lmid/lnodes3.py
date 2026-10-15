"""Big-node census for a one-level middle: apex hubs D(A,p) = {P(ij), T(ijp): i,j in A} (|A| = 3..8) and their
closures, plus greedy multi-cell closures.  Per node: c = system cells inside, a = lines covered by them, b = lines in
perp(N).  One-level per-register incidence bound with k input registers (k <= 2c): min(a, 2k) * min(b, 3k) / k,
maximised over k.  usage: lnodes3.py SYSTEM.json"""
import sys, os, json, collections, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, closure, perp, g
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
def stats(N):
    ins = [C for C in cells if C & ~N == 0]
    a = 0
    for C in ins: a |= C
    c, a, b = len(ins), pc(a), pc(perp(N))
    best = 0
    for k in range(1, 2 * c + 1):
        best = max(best, min(a, 2 * k) * min(b, 3 * k) / k)
    return c, a, b, g.dim(N), pc(N), best
n = 11
res = collections.defaultdict(list)
for p in range(n):
    others = [i for i in range(n) if i != p]
    for sz in (3, 4, 5, 6, 7, 8):
        for A in itertools.combinations(others, sz):
            if A[0] != others[0] and sz >= 6: continue   # subsample big sizes
            m = 0
            for i, j in itertools.combinations(A, 2):
                m |= (1 << g.P(i, j)) | (1 << g.T(i, j, p))
            N = closure(m)
            res[sz].append(stats(N))
for sz in sorted(res):
    rows = res[sz]
    bmax = max(r[5] for r in rows)
    avg = sum(r[5] for r in rows) / len(rows)
    print('|A|=%d nodes %d: rank %s lines %s | cells inside %s..%s, covered lines %s..%s, perp %s, per-reg bound max %.1f avg %.1f'
          % (sz, len(rows), rows[0][3], rows[0][4], min(r[0] for r in rows), max(r[0] for r in rows),
             min(r[1] for r in rows), max(r[1] for r in rows), sorted(set(r[2] for r in rows)), bmax, avg), flush=True)
