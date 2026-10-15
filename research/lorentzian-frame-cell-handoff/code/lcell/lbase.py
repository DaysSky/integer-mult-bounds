"""I_{11,1} cell-bottleneck base: good 4-frames (pairwise orthogonal, sum in 2L), group actions, nondegenerate
closures.  Saves goodframes.pkl."""
import sys, os, pickle, itertools, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lsec'))
os.environ.setdefault('GRP', '55')
from lcommon import g, V, G, bits, HYP, PERMS, act, nondeg_span, pc
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
orth = [set(np.nonzero(G[t] == 0)[0].tolist()) - {t} for t in range(V)]
def goodframes():
    p = os.path.join(HERE, 'goodframes.pkl')
    if os.path.exists(p): return pickle.load(open(p, 'rb'))
    fr = []
    for a in range(V):
        for b in orth[a]:
            if b <= a: continue
            for c in orth[a] & orth[b]:
                if c <= b: continue
                for d in orth[a] & orth[b] & orth[c]:
                    if d <= c: continue
                    s = g.L[[a, b, c, d]].sum(axis=0)
                    if all(x % 2 == 0 for x in s): fr.append((1 << a) | (1 << b) | (1 << c) | (1 << d))
    fr = sorted(fr); pickle.dump(fr, open(p, 'wb')); return fr
CL = {}
def closure(m):
    if m not in CL: CL[m] = g.closure(m)[0]
    return CL[m]
def perp(m):
    r = (1 << V) - 1
    for s in bits(m): r &= HYP[s]
    return r
if __name__ == '__main__':
    fr = goodframes()
    print('good frames', len(fr), 'per line', collections.Counter(sum(1 for F in fr if F >> s & 1) for s in range(V)))
    print('all good frames nondegenerate:', all(nondeg_span(F) for F in fr))
    print('PERMS (group order)', len(PERMS))
