"""Global G* = max over all flats N of min(3|N|, 2|perp(N)|) (value bound for a register whose content is unrestricted
by the cell system, e.g. empties or extra branches).  WLOG N = pp(X); DFS from one P line and one T line (S11 makes every
line equivalent to one of them, and any flat contains a line), adding one line at a time, pruning 2*b <= best."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, g
pc = lambda m: bin(m).count('1')
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = (1 << V) - 1
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
best = 0; arg = None
for s0 in (g.P(0, 1), g.T(0, 1, 2)):
    N0 = pm(pm(1 << s0)); stack = [N0]; seen = {N0}
    while stack:
        N = stack.pop(); P = pm(N); b = pc(P)
        if 2 * b <= best: continue
        v = min(3 * pc(N), 2 * b)
        if v > best: best, arg = v, (pc(N), b, g.dim(N))
        for x in range(V):
            if N >> x & 1: continue
            P2 = P & HYP[x]
            if 2 * pc(P2) <= best: continue
            N2 = pm(P2)
            if N2 not in seen: seen.add(N2); stack.append(N2)
    print('start', g.kind[s0], 'best so far', best, arg, 'visited', len(seen), flush=True)
print('G* =', best, '(|N|, |perp N|, rank) =', arg)
