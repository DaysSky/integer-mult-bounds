"""RIGOROUS per-cell one-level value: best(C) = max over ALL flats N containing C of min(3 a_N, 2 b_N), where
a_N = #lines covered by system cells inside N and b_N = |perp(N)|.
WLOG N = pp(K) := perp(perp(lines of a set K of system cells)) (replacing N by pp(cells inside N) keeps a, can only
raise b).  Exhaustive DFS from pp(C) adding one system cell at a time, pruning when 2*b_N <= best (b is non-increasing
along the search).  Then the one-level bound: sum_t |R(t)| - 2V <= sum_registers best(cell of register) + extras*Gmax.
usage: lreach2.py SYSTEM.json [first_cell last_cell]"""
import sys, os, json, collections, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, perp
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0; hi = int(sys.argv[3]) if len(sys.argv) > 3 else len(cells)
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = (1 << V) - 1
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
def pp(m): return pm(pm(m))
VAL = {}
def val(N):
    r = VAL.get(N)
    if r is None:
        cov_ = 0
        for C in cells:
            if C & ~N == 0: cov_ |= C
        r = (pc(cov_), pc(pm(N))); VAL[N] = r
    return r
out = {}
t0 = time.time()
for ci in range(lo, hi):
    C = cells[ci]
    N0 = pp(C); a, b = val(N0); best = min(2 * a, 2 * b); arg = N0
    stack = [N0]; seen = {N0}; nvis = 0
    while stack:
        N = stack.pop(); nvis += 1
        a, b = val(N)
        if 2 * b <= best: continue
        v = min(2 * a, 2 * b)
        if v > best: best, arg = v, N
        P = pm(N)
        for D in cells:
            if D & ~N == 0: continue
            P2 = P
            for s in bits(D): P2 &= HYP[s]
            if 2 * pc(P2) <= best: continue
            N2 = pm(P2)
            if N2 not in seen: seen.add(N2); stack.append(N2)
    out[ci] = (best, val(arg)[0], val(arg)[1], nvis)
    print(ci, 'best', best, 'a,b', val(arg), 'visited', nvis, 'elapsed %.0fs' % (time.time() - t0), flush=True)
json.dump(out, open('lreach2v2_%s_%d_%d.json' % (os.path.basename(sys.argv[1]).split('.')[0], lo, hi), 'w'))
