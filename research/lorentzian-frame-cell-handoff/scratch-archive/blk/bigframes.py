# Largest closed nondegenerate frames by rank: perps of sets of 1..3 lines (all triples), plus closures.
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, dim
HYP = g.HYP
best = collections.defaultdict(lambda: (0, None))
def consider(F, tag):
    if F == 0: return
    d = dim(F); n = bin(F).count('1')
    if n > best[d][0] and nondegenerate(F): best[d] = (n, tag)
reps = [0, 55]   # S11 orbit reps for the first line: P(01), T(012)
seen = set()
for a in reps:
    consider(HYP[a], ('perp', a))
    for b in range(V):
        if b == a: continue
        F2 = HYP[a] & HYP[b]
        consider(F2, ('perp', a, b))
        for c in range(b + 1, V):
            if c == a: continue
            F3 = F2 & HYP[c]
            if F3 in seen: continue
            seen.add(F3)
            consider(F3, ('perp', a, b, c))
for d in sorted(best):
    n, tag = best[d]
    print('rank', d, 'max lines in a perp-frame', n, tag and [(g.kind[u], g.supp[u]) for u in tag[1:]])
