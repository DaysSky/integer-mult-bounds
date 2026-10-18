"""nat120: THE v=111 CELL-FLOOR CENSUS (the true floor of R for the r434's own live system).

The live-111 (the r434's lines), the per-line l-perp covers (the 3-section law),
the cells' exclusive-target sides-law, and the register set-cover floor.
"""
import json, itertools
import numpy as np
from collections import Counter

S = json.load(open('ii19_nat69_spec.json'))
LALL = [tuple(int(c) for c in l) for l in S['lines']]
V = len(LALL)

# (1) THE LIVE-111: the SPEC's 120 minus the r434's removed-9 (the [6,58,81,88,97,109,112,115,116] from nat113)
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
print('the live-111: %d lines (the removed-9: %s)' % (len(live_idx), sorted(set(range(V)) - live_set)))

L = np.array([LALL[i] for i in live_idx], float)
n = len(L)
G = L @ L.T
print('the ⊥-counts:', dict(sorted(Counter((G == 0).sum(axis=1) - 1).items())))


def nullspace(A):
    u, s, vt = np.linalg.svd(A)
    r = int((s > 1e-9).sum())
    return vt[r:]


# (2) THE D4-TYPE 4-FRAMES among live lines (the 12-line spans)
frames = set()
for l in range(n):
    o = [j for j in range(n) if j != l and G[l, j] == 0]
    for a, b, c in itertools.combinations(o, 3):
        if G[a, b] or G[a, c] or G[b, c]:
            continue
        q = (l, a, b, c)
        A = L[list(q)]
        Q = np.linalg.svd(A)[2][:4]
        if int((np.abs(L - (L @ Q.T) @ Q).max(axis=1) < 1e-9).sum()) == 12:
            frames.add(tuple(sorted(q)))
frames = sorted(frames)
print('the D4-type 4-frames (live): %d' % len(frames))

# (3) THE CELLS {l,x}: the exclusive targets U (⊥ l,x, not ⊥ y,z), the sides-law
sides = Counter()
usz = Counter()
cell_wires = set()
for f in frames:
    for l, x in itertools.combinations(f, 2):
        y, z = [w for w in f if w not in (l, x)]
        U = [t for t in range(n) if G[t, l] == 0 and G[t, x] == 0 and G[t, y] != 0 and G[t, z] != 0 and t not in f]
        usz[len(U)] += 1
        N = nullspace(L[U])
        if N.shape[0] > 2:
            sides[1] += 1
        else:
            # the two-side test: hyperplanes of the c-perp spanned by U-subsets
            Cp = nullspace(L[[l, x]])
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
print('the cells: |U| census:', dict(sorted(usz.items())))
print('the cells: min-sides census:', dict(sorted(sides.items())))

# (4) THE COVER-SECTIONS: per live-line l, the sections (root-perps within l-perp) covering l's live-perp
#     a wire's content = a section; the registers = the distinct sections covering ALL the perps
def root_sections(l):
    P = [j for j in range(n) if j != l and G[l, j] == 0]
    sections = {}
    for x in P:
        m = frozenset(t for t in P if t != x and G[t, x] == 0)
        sections[(l, x)] = m
    return P, sections


demand = {}   # per l: the live-perp set
sec_pool = set()
for l in range(n):
    P, sections = root_sections(l)
    demand[l] = frozenset(P)
    sec_pool.update(sections.values())
print('the distinct sections (the wire-content candidates): %d' % len(sec_pool))

# greedy set-cover over the demands: each l's perp covered by the chosen sections
chosen = []
covered = {}
remaining = {l: set(demand[l]) for l in range(n)}
while any(remaining[l] for l in range(n)):
    best, gain = None, 0
    pool = set()
    for l in range(n):
        if remaining[l]:
            pool.update(remaining[l])
    # candidate sections touching any uncovered demand-line
    cands = [s for s in sec_pool if s & set().union(*[set(demand[l]) for l in range(n) if remaining[l]])]
    for s in cands:
        g = sum(len(s & remaining[l]) for l in range(n))
        if g > gain:
            best, gain = s, g
    if best is None:
        break
    chosen.append(best)
    for l in range(n):
        remaining[l] -= set(best)
print('the greedy register-cover: %d wires cover all %d live-perps' % (len(chosen), n))

# (5) the floor verdict
floor = len(chosen)
print()
print('THE v=111 FLOOR CENSUS:')
print('  the cells: %d frames x 6 cells = %d cells (|U| mean %.1f)' % (len(frames), 6 * len(frames), (sum(k * v for k, v in usz.items()) / sum(usz.values())) if usz else 0))
print('  the sides-law: %s' % dict(sorted(sides.items())))
print('  the cover-floor (greedy): R_delivery >= %d' % floor)
print('  vs the r434 skeleton: 429; vs the shipped: 434')
