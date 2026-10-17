from geo13 import *
from collections import Counter
def sections_of(t):
    out = []
    for X in A2:
        if t in X: out.append(('A2', X, pm(sum(1 << x for x in X))))
    for a, b in CELLS:
        if t in (a, b): out.append(('cell', (a, b), pm((1 << a) | (1 << b))))
    return out
for t in (g.T(0, 1, 2), g.P(0, 1)):
    tp = HYP[t]; S = sections_of(t)
    print(g.kind[t], g.supp[t], 'perp', pc(tp), 'sections', len(S), Counter((k, pc(m)) for k, _, m in S))
    best2 = max(pc(a[2] | b[2]) for a, b in itertools.combinations(S, 2))
    print('  max 2-union', best2)
    # 3-covers
    n3 = Counter()
    ms = [m for _, _, m in S]
    for i, j, k in itertools.combinations(range(len(S)), 3):
        if ms[i] | ms[j] | ms[k] == tp:
            n3[tuple(sorted((S[i][0], S[j][0], S[k][0])))] += 1
    print('  3-covers by section types', n3)
