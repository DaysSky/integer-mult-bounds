"""For every cell {l,x} of a D4-type 4-frame {l,x,y,z}: the exclusive targets U (perp to l and x, not to y, z);
the dim of their common perp; the minimum number of hyperplanes of c-perp whose line sets cover U."""
import json, itertools
import numpy as np
from collections import Counter
S = json.load(open('ii19_nat69_spec.json')); L = np.array(S['lines'], float); V = len(L); G = L @ L.T
def nullspace(A):
    u, s, vt = np.linalg.svd(A); r = int((s > 1e-9).sum()); return vt[r:]
res = Counter(); sides = Counter()
frames = set()
for l in range(V):
    o = [j for j in range(V) if j != l and G[l, j] == 0]
    for a, b, c in itertools.combinations(o, 3):
        if G[a, b] or G[a, c] or G[b, c]: continue
        q = (l, a, b, c)
        A = L[list(q)]; Q = np.linalg.svd(A)[2][:4]
        if int((np.abs(L - (L @ Q.T) @ Q).max(axis=1) < 1e-9).sum()) == 12: frames.add(tuple(sorted(q)))
frames = sorted(frames)[:200]
for f in frames:
    for l, x in itertools.combinations(f, 2):
        y, z = [w for w in f if w not in (l, x)]
        U = [t for t in range(V) if G[t, l] == 0 and G[t, x] == 0 and G[t, y] != 0 and G[t, z] != 0 and t not in f]
        N = nullspace(L[U])            # the common perp of U
        res[(len(U), N.shape[0])] += 1
        # the cell's complement c-perp (6-dim); hyperplanes of it = (c + <v>)-perp; candidate v: lines in c-perp
        # and the min cover of U by sets {t in U : t perp v}: v ranges over vectors of c-perp spanned by U-subsets
        Cp = nullspace(L[[l, x]])      # basis of c-perp (6 x 8)
        best = None
        # one side covers U iff some v in c-perp is perp to all of U: v in N (and N is c itself -> no)
        one = N.shape[0] > 2
        if one: best = 1
        else:
            # two sides: U = U1 u U2 with U1, U2 each of rank <= 5 within c-perp (each inside a hyperplane of c-perp)
            # test all splits by hyperplanes spanned by U-lines
            cand = set()
            for comb in itertools.combinations(range(len(U)), 5):
                A = L[[U[k] for k in comb]]
                if np.linalg.matrix_rank(np.vstack([A, L[[l, x]]])) < 7: continue
                n = nullspace(np.vstack([A, L[[l, x]]]))
                if n.shape[0] != 1: continue
                cand.add(frozenset(k for k in range(len(U)) if abs(L[U[k]] @ n[0]) < 1e-9))
            cand = list(cand)
            full = frozenset(range(len(U)))
            best = 3
            for s1, s2 in itertools.combinations(cand, 2):
                if s1 | s2 == full: best = 2; break
        sides[best] += 1
print('(|U|, dim common perp of U):', dict(res))
print('min sides (hyperplane sections of c-perp) covering U:', dict(sides))
