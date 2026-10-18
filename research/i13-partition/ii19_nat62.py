"""THE 2-CLASS BUILD STAGE 8 (ii19_nat62.py) — the global-flag frame library!!

THE WORD4'S PROVEN ARCHITECTURE (the nat27 duties!!): the sources read at the rung-levels
1 (the singletons!!) / 2 (the cells!!) / 4 (the 12-frames!!) — THE GLOBAL FLAG.  HERE: the
2-class's own flag-frames: (1) THE CELLS (per source: ONE dim-2 pair-plane (the partner
choice (the freedom!!)) (the class-blocked (the same-class pairs!!))); (2) THE DIM-4 FRAMES
(the E8-blocks' 12-frames (the 70 per class!!)); (3) THE NESTING CHECKS (the cell ⊆ the
dim-4 (the coordination!!)) — the frame library for the emission!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

roots240 = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots240.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots240.add(tuple(Fraction(x, 2) for x in s))

def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

d8 = {canon(r): r for r in roots240}
roots = sorted(d8.values())
V = 240
H = 10
L = []
for c in (0, 1):
    for a in roots:
        L.append([Fraction(x) for x in a] + [Fraction(c), Fraction(0)])
FORM = [[Fraction(0)] * H for _ in range(H)]
for i in range(8): FORM[i][i] = Fraction(1)
FORM[8][9] = FORM[9][8] = Fraction(1)
def ip(x, y):
    return sum(x[i] * y[j] * FORM[i][j] for i in range(H) for j in range(H) if FORM[i][j])
G = [[ip(L[s], L[t]) for t in range(V)] for s in range(V)]
CLS = [s // 120 for s in range(V)]

def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]

def gram_det(basis):
    n = len(basis)
    A = [[ip(basis[i], basis[j]) for j in range(n)] for i in range(n)]
    A = [[Fraction(x) for x in row] for row in A]
    det = Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return Fraction(0)
        if p != c:
            A[c], A[p] = A[p], A[c]; det = -det
        det *= A[c][c]
        for i in range(c + 1, n):
            if A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return det

# (1) THE CELLS: per source: the partner candidates (the same-class C= lines!!)
# the freedom: the partner chosen for the flag's coordination (the nesting!!)!!
CELLCAND = {}
for s in range(V):
    CELLCAND[s] = [m for m in range(V) if CLS[m] == CLS[s] and m != s and G[s][m] == 0]
log('(1) THE CELL CANDIDATES per source: %s' % dict(sorted(Counter(len(v) for v in CELLCAND.values()).items())))
# (2) THE DIM-4 FRAMES (the 12-frames: the maximal same-class sets with a dim-4 span!!)
# the honest construction: the E8-block's 12-frames — from the roots' structure: the
# dim-4 subspaces containing 12+ same-class lines!!
dim4 = defaultdict(set)
# the candidate frames: the spans of the 4-line subsets... the honest approach: from the
# word4's own 70 dim-4 frames (the 121-word's!!) — the same E8 geometry!! (the roots are
# the same (the canonical 120!!)!!) — the word4's frames: the dim-4 with 12 sources!!
w4 = json.load(open('ii19_own_word4.json', 'rt'))
fr4 = [rref([[Fraction(x) for x in row] for row in F], w4['h']) for F in w4['frames']]
dims4 = [len(F) for F in fr4]
# the word4's dim-4 frames' line-memberships (the 120 roots + the special (121!!))
L4 = [[Fraction(x) for x in l] for l in w4['lines']]
n4 = 0
for F in range(len(w4['frames'])):
    if dims4[F] != 4: continue
    # the members: the word4's lines whose span-mem...
    b = fr4[F]
    mem = []
    for s in range(w4['v']):
        if len(rref(list(b) + [L4[s]], w4['h'])) == 4:
            mem.append(s)
    if len(mem) >= 2 and w4['v'] == 121 and all(s < 120 for s in mem):
        # the 120-root frames (the E8-geometry (the same for both classes!!))
        dim4[n4] = set(mem)
        n4 += 1
log('(2) THE WORD4-SHARED DIM-4 FRAMES: %d (the E8-geometry (the same roots!!))' % n4)
sizes = Counter(len(v) for v in dim4.values())
log('    the source-counts: %s' % dict(sorted(sizes.items())))
# the per-class versions (the 2-class's lines: the SAME roots (the class-pairs!!))
# (the dim-4 frames serve BOTH classes' copies (the same x-geometry!!))
json.dump({'CELLCAND': {str(k): v for k, v in CELLCAND.items()},
           'dim4': {str(k): sorted(v) for k, v in dim4.items()}},
          open('ii19_nat62_flag.json', 'w'))
log('saved ii19_nat62_flag.json')
