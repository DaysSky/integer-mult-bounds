"""Covers of I_{n,1} lines by perps of TIMELIKE ambient vectors z = (b; sum(b)/3) (every frame containing a timelike z is
nondegenerate).  Greedy set cover over labelled vectors generated from value patterns by random relabelling, then
exact small-cover search by DFS over the best candidates."""
import itertools, random, sys
from fractions import Fraction as Fr
n = int(sys.argv[1]) if len(sys.argv) > 1 else 11
vals = list(range(-3, 4))
P = list(itertools.combinations(range(n), 2)); T = list(itertools.combinations(range(n), 3))
NL = len(P) + len(T); FULLM = (1 << NL) - 1
def cov(b):
    c = Fr(sum(b), 3); nrm = sum(x*x for x in b) - c*c
    if nrm >= 0: return None, nrm
    m = 0
    for k, (i, j) in enumerate(P):
        if b[i] == b[j]: m |= 1 << k
    for k, (i, j, l) in enumerate(T):
        if b[i] + b[j] + b[l] == c: m |= 1 << (len(P) + k)
    return m, nrm
pats = []
for b in itertools.combinations_with_replacement(vals, n):
    m, nrm = cov(b)
    if m is None: continue
    pats.append((bin(m).count('1'), b))
pats.sort(reverse=True)
print('timelike patterns', len(pats), 'best coverage', pats[:8], flush=True)
random.seed(1)
pool = {}
for cnt, b in pats[:300]:
    for _ in range(60):
        bb = list(b); random.shuffle(bb); bb = tuple(bb)
        m, _n = cov(bb)
        pool[bb] = m
pool = list(pool.items())
print('pool', len(pool), flush=True)
best = None
for trial in range(200):
    U = FULLM; chosen = []
    while U:
        cand = max(pool, key=lambda kv: bin(kv[1] & U).count('1') + random.random() * 0.5)
        chosen.append(cand[0]); U &= ~cand[1]
        if best and len(chosen) >= len(best): break
    if not U and (best is None or len(chosen) < len(best)):
        best = chosen; print('cover size', len(best), best, flush=True)
