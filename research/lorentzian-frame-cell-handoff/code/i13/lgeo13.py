"""I_{13,1} lines (78 P + 286 T) -- copy of llp/lgeo.py with n = 13 with S11 canonical forms for tuples of line sets.
canon(masks) -> (canonical tuple of masks, a permutation of points realising it).
Canonical form = lexicographically minimal image over the individualisation-refinement tree (twin pruning: points
interchangeable by a transposition fixing every mask are branched on once).  Exact: no invariant shortcuts."""
import sys, os, itertools, functools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
import numpy as np
g = Geom(13); V = g.V; G = g.G; n = 13
HYP = g.HYP
FULL = (1 << V) - 1
bits = g.bits
pc = lambda m: bin(m).count('1')
KIND = g.kind; SUPP = g.supp; IDX = g.idx
PTS = [frozenset(s) for s in SUPP]
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
def pp(m): return pm(pm(m))
def rank(m):
    b = bits(m)
    return int(np.linalg.matrix_rank(g.LA[b])) if b else 0
def img_line(s, perm):
    return IDX[(KIND[s], tuple(sorted(perm[i] for i in SUPP[s])))]
def act(m, perm):
    r = 0
    for s in bits(m): r |= 1 << img_line(s, perm)
    return r
# transposition images of lines
TRL = {}
for x, y in itertools.combinations(range(n), 2):
    perm = list(range(n)); perm[x], perm[y] = y, x
    TRL[(x, y)] = [img_line(s, perm) for s in range(V)]
def act_tr(m, x, y):
    tl = TRL[(min(x, y), max(x, y))]
    r = 0
    for s in bits(m): r |= 1 << tl[s]
    return r
def _refine(col, masks_lines):
    """col: list of ints (point colours).  masks_lines: list over masks of list of point-tuples.  Equitable refinement."""
    while True:
        sig = []
        for x in range(n):
            parts = [col[x]]
            for mi, ml in enumerate(masks_lines):
                lst = []
                for pts in ml:
                    if x in pts:
                        lst.append((len(pts), tuple(sorted(col[y] for y in pts if y != x))))
                lst.sort(); parts.append(tuple(lst))
            sig.append(tuple(parts))
        keys = sorted(set(sig))
        new = [keys.index(sig[x]) for x in range(n)]
        if len(set(new)) == len(set(col)):
            return new
        col = new
def canon(masks):
    masks = tuple(masks)
    ml = [[SUPP[s] for s in bits(m)] for m in masks]
    best = [None, None]
    def leaf(col):
        # col discrete: point x -> rank col[x]
        perm = col[:]
        img = tuple(act(m, perm) for m in masks)
        if best[0] is None or img < best[0]: best[0] = img; best[1] = perm
    def rec(col):
        col = _refine(col, ml)
        if len(set(col)) == n: leaf(col); return
        # first smallest non-singleton class
        cls = {}
        for x in range(n): cls.setdefault(col[x], []).append(x)
        cands = [c for c in cls.values() if len(c) > 1]
        cmin = min(cands, key=lambda c: (len(c), col[c[0]]))
        # twin pruning
        reps = []
        for x in cmin:
            tw = False
            for y in reps:
                if all(act_tr(m, x, y) == m for m in masks): tw = True; break
            if not tw: reps.append(x)
        for x in reps:
            c2 = [2 * c for c in col]
            c2[x] = 2 * col[x] - 1 if col[x] > 0 else -1
            # renormalise
            keys = sorted(set(c2)); c2 = [keys.index(c) for c in c2]
            rec(c2)
    rec([0] * n)
    return best[0], best[1]
