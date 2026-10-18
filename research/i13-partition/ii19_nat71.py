"""THE EXTENSION-WORD BUILD STAGE 3 (ii19_nat71.py) — THE CHAIN DESIGN (the r434-grammar!!).

THE PIECES' 3-GATE RUNNING-SUMS: (1) [SINGLE[a], h, [a]] (0->1!!); (2) [CELL(a,b), h, [b]]
(1->2, b's OWN cell (the matching!!)); (3) [HOME4(c), h, [c]] (2->4, c's ONE dim-4 home
(the wall-dissolver!!!)). THE READS: the pieces read by their users at the shared rungs
(the capacity-law classes!!). CONSUMES: nat70's pool!! OUTPUT: the chain-spec!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(Fraction(x) for x in l) for l in SPEC['lines']]
V = len(lines)
H = 8
PERP = [set(p) for p in SPEC['PERP']]
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(frozenset(p), list(u)) for p, u in P70['pool']]
left = [set(l) for l in P70['left']]
log('(0) the economy: %d pieces + %d carriers' % (len(pool), sum(1 for lo in left if lo)))

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
    A = [[sum(basis[i][k] * basis[j][k] for k in range(8)) for j in range(n)] for i in range(n)]
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
G = [[sum(a[i] * b[i] for i in range(8)) for b in lines] for a in lines]

# (1) THE CELLS: per piece {a, b, c}: the pair (a, b) (the first-2 sorted!!): b's cell
# (ONE per source (the matching!!)): the greedy (the pair (a, b) = the piece's 2-line prefix!!)
partner = {}
used_as_pair = defaultdict(list)
for i, (p, u) in enumerate(pool):
    ps = sorted(p)
    a, b, c = ps
    if b in partner and partner[b] != a:
        log('  !! the b-conflict at piece %d (%s)' % (i, ps))
        continue
    partner[b] = a
    used_as_pair[(a, b)].append(i)
log('(1) THE CELLS: %d b-sources matched (%d conflicts-checked!!)' % (
    len(partner), len(pool) - len(partner)))
bloads = Counter(len(v) for v in used_as_pair.values())
log('    the pair-pieces per cell: %s' % dict(sorted(bloads.items())))

# (2) THE c-HOMES: the dim-4 frames containing the cells + the c's (the construction:
# the 12-frames of the {0,+-2}-class!!): the candidate dim-4s: the spans of the ⊥-quads!!
# THE SIMPLEST LEGAL HOME: span(a, b, c) itself (dim 3!!) — c climbs singleton -> dim-3?!
# THE c-WALL: c's multiple pieces: the incomparable dim-3 spans!!! -> THE SHARED HOMES:
# per c: ONE dim-4 home containing ALL its pieces' spans (the (a,b)-pairs + c!!!)
c_pieces = defaultdict(list)
for i, (p, u) in enumerate(pool):
    ps = sorted(p)
    c_pieces[ps[2]].append((i, ps[:2]))
cspan = {}
for c, plist in c_pieces.items():
    allq = {c}
    for i, ab in plist:
        allq |= set(ab)
    # the home: span(allq) — dim ?? (the nondegenerate?!!) — the honest: the dim = rank(allq)
    dim = len(rref([list(lines[x]) for x in sorted(allq)], 8))
    cspan[c] = (sorted(allq), dim)
dims = Counter(d for s, d in cspan.values())
log('(2) THE c-HOMES (the spans!!): the dims %s (the wall-check: the c-sources with the' 
    ' multi-piece spans must be CONTAINED in ONE dim-4!!)' % dict(sorted(dims.items())))
infeasible = [c for c, (s, d) in cspan.items() if d > 4]
log('    the dim>4 c-homes: %d (the split/re-home needed!!)' % len(infeasible))
# the honest alternative: the dim-3 spans (the per-piece!!) with the c-WALL... the homes:
# the dim-4 12-frames (the class's!!): the candidates: the maximal {0,+-2}-ip sets with the
# dim-4 spans!! — THE CENSUS (the bounded!!): the 4-line ⊥-quads!!
log('    (the dim-4 home-census: the next stage (the nat72!!)!!)')

# (3) THE READ-CLASSES (the capacity-law groups!!): per piece: the users partitioned by
# the rank <= 9-d (the nat40-class!!)!! (deferred to the emission (the frame-dependent!!))
json.dump({'partner': partner, 'c_pieces': {str(k): v for k, v in c_pieces.items()},
           'cspan': {str(k): v for k, v in cspan.items()}},
          open('ii19_nat71_chains.json', 'w'))
log('(4) saved ii19_nat71_chains.json (the chain-spec!!)')
