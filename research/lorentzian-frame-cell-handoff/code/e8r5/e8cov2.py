"""E8 4-covers (3 A3-perps + 1 Z-perp, Z = t x A2 with t the A1 factor) of R(t): enumerate for t = 0 by branching on
the lowest uncovered line, then map to every line t by a word of root reflections (W(E8) is transitive on lines).
Saves covers.pkl {t: [(X1,X2,X3,Z)]} with frames as line masks."""
import sys, itertools, collections, pickle, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
V = e8.V; HYP = e8.HYP; bits = e8.bits; GI = e8.GI
pc = lambda m: bin(m).count('1')
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
t0 = time.time()
# reflections as line permutations
L = [np.array(x) for x in e8.LINES]
idx = {}
for i, x in enumerate(e8.LINES):
    idx[tuple(x)] = i; idx[tuple(-a for a in x)] = i
refl = []
for r in range(V):
    perm = [idx[tuple(L[x] - GI[x][r] * L[r])] for x in range(V)]
    refl.append(perm)
def actm(m, perm):
    o = 0
    for s in bits(m): o |= 1 << perm[s]
    return o
# BFS: permutation mapping line 0 to each line
maps = {0: list(range(V))}; fr = [0]
while fr:
    nf = []
    for a in fr:
        for r in range(V):
            b = refl[r][a]
            if b not in maps:
                maps[b] = [refl[r][maps[a][x]] for x in range(V)]; nf.append(b)
    fr = nf
assert len(maps) == V
# covers of t = 0
t = 0; R = HYP[t] & ~(1 << t)
X3s = set(); Zs = set()
for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
    F, d = e8.closure((1 << t) | (1 << a) | (1 << b))
    if d != 3: continue
    if pc(F) == 6: X3s.add(F)
    elif pc(F) == 4 and all(GI[t][x] == 0 for x in bits(F) if x != t): Zs.add(F)
X3s = sorted(X3s); Zs = sorted(Zs)
PX = {X: pm(X) & R for X in X3s}; PZ = {Z: pm(Z) & R for Z in Zs}
cov0 = set()
def rec(U, chosenX, chosenZ):
    if U == 0:
        if len(chosenX) == 3 and chosenZ is not None: cov0.add((tuple(sorted(chosenX)), chosenZ))
        return
    if len(chosenX) == 3 and chosenZ is not None: return
    u = (U & -U).bit_length() - 1
    if len(chosenX) < 3:
        for X in X3s:
            if PX[X] >> u & 1 and X not in chosenX: rec(U & ~PX[X], chosenX + [X], chosenZ)
    if chosenZ is None:
        for Z in Zs:
            if PZ[Z] >> u & 1: rec(U & ~PZ[Z], chosenX, Z)
rec(R, [], None)
# canonical: X triple sorted, require exactly 3 X and 1 Z
cov0 = sorted(cov0)
print('t=0 covers', len(cov0), 'time', round(time.time() - t0, 1), flush=True)
covers = {}
for tt in range(V):
    p = maps[tt]
    covers[tt] = [(tuple(sorted(actm(X, p) for X in Xs)), actm(Z, p)) for Xs, Z in cov0]
# sanity on a few lines
for tt in (1, 57, 119):
    Rt = HYP[tt] & ~(1 << tt)
    for Xs, Z in covers[tt][:20]:
        U = 0
        for X in Xs: U |= pm(X)
        U |= pm(Z)
        assert U & Rt == Rt and all(X >> tt & 1 for X in Xs) and Z >> tt & 1
print('mapped and checked', time.time() - t0, flush=True)
pickle.dump(dict(covers=covers), open('covers.pkl', 'wb'))
