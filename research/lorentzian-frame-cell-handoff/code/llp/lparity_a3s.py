"""Parity tops mixing plane sections and A3-perp sections (rank-8 frames with 6 users).  For target t: sections =
pm(pi) for planes pi through t, and pm(X) for A3s X containing t.  Find combinations of <= 4 sections with
XOR = 1_{R(t)} + D, |D| <= 1 (defect lines must be readable), by meet in the middle on exact XOR (D = 0) and
single-flip lookups (|D| = 1).  Reports signatures (section kinds) and counts."""
import sys, itertools, collections, pickle
from lgeo import *
d = pickle.load(open('a3compat_11.pkl', 'rb')); A3 = [sum(1 << s for s in X) for X in d['A3']]
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
for t in (0, 100):
    R = HYP[t]
    secs = []
    for p in sorted(set(plane_of(t, e) for e in range(V) if e != t)): secs.append(('pl%d' % pc(p), pm(p)))
    for X in A3:
        if X >> t & 1: secs.append(('A3', pm(X)))
    print('target', KIND[t], 'sections', collections.Counter(k for k, S in secs), flush=True)
    N = len(secs)
    pairs = collections.defaultdict(list)
    for i in range(N):
        for j in range(i + 1, N): pairs[secs[i][1] ^ secs[j][1]].append((i, j))
    print('  pair XORs', len(pairs), flush=True)
    res = collections.Counter()
    # 4 sections, defect 0 or 1: X_ij ^ X_kl ^ R in {0, single line}
    for X, lst in pairs.items():
        Y = X ^ R
        for D in [0] + [1 << s for s in bits(R)]:
            for (k, l) in pairs.get(Y ^ D, []):
                for (i, j) in lst:
                    if len({i, j, k, l}) == 4 and i < k:
                        sig = tuple(sorted(secs[x][0] for x in (i, j, k, l)))
                        res[(pc(D), sig)] += 1
    # 3 sections, defect <= 1
    for k in range(len(secs)):
        Y = secs[k][1] ^ R
        for D in [0] + [1 << s for s in bits(R)]:
            for (i, j) in pairs.get(Y ^ D, []):
                if k > j:
                    res[(pc(D), tuple(sorted(secs[x][0] for x in (i, j, k))))] += 1
    for key, v in sorted(res.items()): print('   defect %d' % key[0], key[1], 'x', v)
