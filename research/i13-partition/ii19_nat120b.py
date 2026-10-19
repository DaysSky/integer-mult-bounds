"""nat120b: THE v=111 CELL-FLOOR CENSUS - vectorized (the D4-frames via triangle filter + batched SVD).

Stages: (1) live-111; (2) D4-type 4-frames (batched); (3) the cells' sides-law;
(4) the section-cover floor (greedy); (5) the verdict.
"""
import json, itertools, sys
import numpy as np
from collections import Counter

S = json.load(open('ii19_nat69_spec.json'))
LALL = [tuple(int(c) for c in l) for l in S['lines']]
V = len(LALL)

import gzip
W = json.load(gzip.open('../e8-bit-p111-r434/data/bitE8mut-p111-r434.json.gz', 'rt'))
hub = []
for l in W['lines']:
    x = list(l)
    if isinstance(x[0], list):
        x = x[0]
    hub.append(tuple(int(c[0]) if isinstance(c, list) else int(c) for c in x))


def canon(v):
    v = list(v)
    for i, c in enumerate(v):
        if c:
            if c < 0:
                v = [-u for u in v]
            break
    return tuple(v)


hubset = {canon(tuple(reversed(x))) for x in hub}
live_idx = [i for i, l in enumerate(LALL) if canon(l) in hubset]
live_set = set(live_idx)
print('the live-111: %d (removed-9: %s)' % (len(live_idx), sorted(set(range(V)) - live_set)), flush=True)

L = np.array([LALL[i] for i in live_idx], float)
n = len(L)
G = L @ L.T
print('the ⊥-counts:', dict(sorted(Counter((G == 0).sum(axis=1) - 1).items())), flush=True)

# (2) THE D4-TYPE 4-FRAMES: (l, a, b, c): l⊥a,b,c; a,b,c pairwise ⊥; the span holds exactly 12 live lines
frames = set()
for l in range(n):
    P = [j for j in range(n) if j != l and G[l, j] == 0]
    # the triangles within P (pairwise-⊥ triples)
    cands = []
    Pl = np.array(P)
    sub = G[np.ix_(P, P)] == 0
    for i in range(len(P)):
        ai = P[i]
        for j in range(i+1, len(P)):
            if not sub[i, j]:
                continue
            bj = P[j]
            for k in range(j+1, len(P)):
                if sub[i, k] and sub[j, k]:
                    cands.append((l, ai, bj, P[k]))
    if not cands:
        continue
    A = np.array([L[list(c)] for c in cands])            # (m, 4, 8)
    # batched orthonormal bases: via QR on the transpose-stack
    m = len(cands)
    # project all live lines onto each candidate's span: count == 12
    # basis via SVD per candidate (batched):
    Usv, _, _ = np.linalg.svd(A, full_matrices=False)    # (m, 4, 8): the left vectors? A is (m,4,8): svd gives U (m,4,4), s (m,4), Vh (m,4,8)
    # the orthonormal span basis: Vh[:, :4, :] rows
    B = _ = None
    Vh = np.linalg.svd(A)[2]                              # (m, 4, 8) - the row space bases
    # projection test: for each candidate, count live lines t with |proj(t onto span)| == |t|
    Lt = L                                                # (111, 8)
    # coords: X = Lt @ Vh[m].T  (111, 4); residual = Lt - X @ Vh[m]
    prods = np.einsum('mki,tk->mtk', Vh, Lt)              # (m, 111, 4)
    reco = prods @ Vh                                     # (m, 111, 8)
    resid = np.abs(Lt[None, :, :] - reco).max(axis=2)     # (m, 111)
    counts = (resid < 1e-9).sum(axis=1)                   # (m,)
    for c, cnt in zip(cands, counts):
        if cnt == 12:
            frames.add(tuple(sorted(c)))
    if l % 10 == 0:
        print('  line %d: the candidates %d | the frames so far %d' % (l, len(cands), len(frames)), flush=True)
frames = sorted(frames)
print('the D4-type 4-frames (live): %d' % len(frames), flush=True)

# (3) THE CELLS {l,x}: the exclusive targets U + the sides-law
def nullspace(A):
    u, s, vt = np.linalg.svd(A)
    r = int((s > 1e-9).sum())
    return vt[r:]


sides = Counter()
usz = Counter()
for f in frames:
    for l, x in itertools.combinations(f, 2):
        y, z = [w for w in f if w not in (l, x)]
        U = [t for t in range(n) if G[t, l] == 0 and G[t, x] == 0 and G[t, y] != 0 and G[t, z] != 0 and t not in f]
        usz[len(U)] += 1
        N = nullspace(L[U])
        if N.shape[0] > 2:
            sides[1] += 1
        else:
            cand = set()
            for comb in itertools.combinations(range(len(U)), 5):
                A = L[[U[k] for k in comb]]
                if np.linalg.matrix_rank(np.vstack([A, L[[l, x]]])) < 7:
                    continue
                nv = nullspace(np.vstack([A, L[[l, x]]]))
                if nv.shape[0] != 1:
                    continue
                cand.add(frozenset(k for k in range(len(U)) if abs(L[U[k]] @ nv[0]) < 1e-9))
            cand = list(cand)
            full = frozenset(range(len(U)))
            best = 3
            for s1, s2 in itertools.combinations(cand, 2):
                if s1 | s2 == full:
                    best = 2
                    break
            sides[best] += 1
print('the cells: |U| census:', dict(sorted(usz.items())), flush=True)
print('the cells: min-sides census:', dict(sorted(sides.items())), flush=True)

# (4) THE COVER-SECTIONS + the greedy floor
demand = {}
sec_pool = set()
for l in range(n):
    P = [j for j in range(n) if j != l and G[l, j] == 0]
    for x in P:
        m = frozenset(t for t in P if t != x and G[t, x] == 0)
        sec_pool.add(m)
    demand[l] = frozenset(P)
print('the distinct sections: %d' % len(sec_pool), flush=True)

chosen = []
remaining = {l: set(demand[l]) for l in range(n)}
sec_list = [set(s) for s in sec_pool]
while any(remaining[l] for l in range(n)):
    best, gain = None, 0
    for s in sec_list:
        g = sum(len(s & remaining[l]) for l in range(n))
        if g > gain:
            best, gain = s, g
    if best is None:
        break
    chosen.append(best)
    for l in range(n):
        remaining[l] -= best
print('the greedy register-cover: %d wires cover all %d live-perps' % (len(chosen), n), flush=True)

print()
print('THE v=111 FLOOR CENSUS:')
print('  the cells: %d frames x 6 = %d cells' % (len(frames), 6*len(frames)))
print('  the sides-law: %s' % dict(sorted(sides.items())))
print('  the cover-floor (greedy): R_delivery >= %d' % len(chosen))
print('  vs the r434 skeleton: 429; vs the shipped: 434')
