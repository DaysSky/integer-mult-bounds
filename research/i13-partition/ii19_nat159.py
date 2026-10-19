"""nat159: THE 121's CELL-ASSEMBLY MECHANISM CENSUS (the E8 quad-total comparison).

The E8's assembly: the D4-cells (12-line closures) read by ~12 targets each;
incidence 9/line (vs the naive 63). THE QUESTION at the 121: the D4-cell family
and its TRUE sharing depths - the construction fact that decides whether the
121's assembly mechanism is better than the E8's own.
(1) the D4-frames at v=121 (the vectorized nat120b machinery);
(2) the per-frame user-counts (the targets whose perps contain the frame);
(3) the per-line incidence (the assembly's true read economy);
(4) the comparison with the E8's 9/line.
"""
import json
from collections import Counter
from itertools import combinations
import numpy as np

W = json.load(open('ii19_own_word4.json'))
v = W['v']
lines = [tuple(int(c) for c in l) for l in W['lines']]
n = len(lines[0])
print('the 121: %d lines, dim %d' % (v, n))

L8 = np.array(lines, dtype=np.float64)

# the ⊥-structure: the form (x,y)/2: the integer inner product x.y must be 0 mod... 
# the lines: norm 2 (the form (x,y)/2: x.x = 4 => norm 4/2 = 2): the ⊥ iff x.y = 0
IP = (L8 @ L8.T) / 2.0
print('the norms census:', dict(sorted(Counter(np.round(np.diag(IP), 3)).items())))
G = (np.round(IP).astype(np.int64) != 0)
np.fill_diagonal(G, True)
print('the perp sizes:', dict(sorted(Counter((~G[j] & [i != j for i in range(v)]).sum()).items() for j in range(0))))
perp = [frozenset(j for j in range(v) if j != i and not G[i][j]) for i in range(v)]
print('the perp-size census:', dict(sorted(Counter(len(p) for p in perp).items())))

# (1) THE D4-FRAMES: the 4-sets of pairwise-⊥ lines whose span holds exactly 12 lattice lines
# the vectorized approach (nat120b-style): per line l, the triangles in perp(l), batched 12-line test
frames = {}
for l in range(v):
    P = sorted(perp[l])
    if len(P) < 4:
        continue
    Pa = L8[P]
    # the ⊥-graph within P
    IPp = np.round(Pa @ Pa.T / 2.0).astype(np.int64)
    adj = (IPp == 0)
    tris = []
    a_idx, b_idx = np.nonzero(np.triu(adj, 1))
    for a, b in zip(a_idx, b_idx):
        cs = np.nonzero(adj[a] & adj[b])[0]
        for c in cs[cs > b]:
            tris.append((a, b, c))
    if not tris:
        continue
    T = np.array(tris)
    # batched: for each (a,b,c) + l: the 4 rows; count the lattice lines in the span
    # the span test: the line t in span(l,a,b,c) iff rank([l,a,b,c,t]) == 4
    base = np.stack([np.broadcast_to(L8[l], (len(T), n)), Pa[T[:, 0]], Pa[T[:, 1]], Pa[T[:, 2]]], axis=1)  # (nT, 4, n)
    # the projection test: t in span iff the residual after projecting on the 4-space is ~0
    # via the batched SVD (small: nT x 4 x 8)
    U, S, Vh = np.linalg.svd(base, full_matrices=False)  # (nT,4,4),(nT,4),(nT,4,n)
    counts = np.zeros(len(T), dtype=np.int64)
    for k in range(len(T)):
        Vk = Vh[k]  # (4, n)
        coeffs = L8 @ Vk.T  # (v, 4)
        resid = L8 - coeffs @ Vk
        rn = np.linalg.norm(resid, axis=1)
        inside = (rn < 1e-8).sum()
        counts[k] = inside
    good = np.nonzero(counts == 12)[0]
    for k in good:
        a, b, c = T[k]
        fr = frozenset([l, P[a], P[b], P[c]])
        key = tuple(sorted(fr))
        frames[key] = True
    if l % 20 == 0:
        print('  line %d: %d triples, %d good, %d frames so far' % (l, len(T), len(good), len(frames)), flush=True)

print()
print('(1) THE D4-FRAMES AT THE 121: %d (vs the E8-at-111: 20 live-12; the E8-120: ~200)' % len(frames))

# (2) the per-frame user-counts: the targets t with frame ⊆ perp(t)
frame_list = [frozenset(f) for f in frames]
users = []
for f in frame_list:
    us = set()
    for t in range(v):
        if f <= perp[t]:
            us.add(t)
    users.append(us)
uc = Counter(len(u) for u in users)
print('(2) the per-frame user-counts:', dict(sorted(uc.items())))

# (3) the per-line incidence: the assembly economy
# the coverage: pick the maximal-sharing frames greedily to cover the perp-demands
# the honest per-line incidence: for each line l: the frames containing l, weighted by their users
inc = {}
for l in range(v):
    tot = 0
    for f, u in zip(frame_list, users):
        if l in f:
            tot += len(u)
    inc[l] = tot
print('(3) the per-line incidence (the raw Σ users over the frames containing l):')
inc_mean = sum(inc.values())/v
inc_census = dict(sorted(Counter(inc.values()).items()))
print('(3) the per-line incidence: the mean %.1f | the census: %s' % (inc_mean, inc_census))

# (4) THE GREEDY CELL-ASSEMBLY: cover all the targets' perp-demands with the cells
# the demand: each target t needs perp(t)'s lines delivered: the cells ⊆ perp(t) + the leftovers
demands = {t: set(perp[t]) for t in range(v)}
chosen = []
cov = {t: set() for t in range(v)}
remaining = {t: set(perp[t]) for t in range(v)}
progress = True
while progress and any(remaining.values()):
    progress = False
    # the best frame: (the targets it serves, the new lines covered)
    best = None
    for f, u in zip(frame_list, users):
        gain = sum(len(f & remaining[t]) for t in u if t in remaining and remaining[t])
        if gain and (best is None or gain > best[0]):
            best = (gain, f, u)
    if best:
        _, f, u = best
        chosen.append((f, u))
        for t in u:
            remaining[t] -= f
        progress = True
uncovered = sum(len(r) for r in remaining.values())
print('(4) THE GREEDY CELL-ASSEMBLY: %d cells chosen | the uncovered lines: %d' % (len(chosen), uncovered))
print('    vs the E8: the 315-cover structure; the incidence economy below')
# the incidence: the Σ over the chosen cells of (the users) / the Σ over the targets
tot_reads = sum(len(u) for f, u in chosen)
print('    the total cell-reads: %d | the per-target: %.2f | the per-line: %.2f' %
      (tot_reads, tot_reads/v, tot_reads/v))
print('    THE E8 BENCHMARK: 9/line')
json.dump({'frames': len(frames), 'user_census': dict(uc),
           'chosen': [(sorted(f), sorted(u)) for f, u in chosen[:50]],
           'uncovered': uncovered}, open('ii19_nat159_cells121.json', 'wt'))
print('SAVED ii19_nat159_cells121.json')
