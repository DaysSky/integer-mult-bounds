"""THE LADDER-STAGE-1-FIXED (ii19_nat83.py) — the I2-partners = the piece co-lines!!

THE §716's DIAGNOSTIC: the I2 = span{l, the-⊥-partner} ⊄ the src's piece-PF (the
partner OUTSIDE!!) — THE FIX: the b/c-sources' I2-partner = THE PIECE'S CO-LINE (the
src's b/c-piece's other src (the I2 ⊆ the PF ✓✓✓!!)); the a-only-sources: ANY-⊥
(theirs chains: SINGLE -> I2 -> FULL ✓✓). THE GCHECK RUN!!!
"""
import os, sys, itertools, json
from collections import Counter
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

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

# the matching (the nat78's exact!!)
SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]
bc_used = set(); kept = []
order = sorted(range(len(pool)), key=lambda i: -len(pool[i][1]))
for i in order:
    ps, users = pool[i]
    found = None
    for a in ps:
        bc = [s for s in ps if s != a]
        if bc[0] in bc_used or bc[1] in bc_used:
            continue
        found = (a, bc); break
    if found is None: continue
    a, bc = found
    bc_used |= set(bc)
    kept.append((i, a, bc))
NP = len(kept)
log('the kept: %d' % NP)
# the b/c-sources' co-lines (the piece's other-src!!
co_line = {}
for k, (i, a, bc) in enumerate(kept):
    co_line[bc[0]] = bc[1]
    co_line[bc[1]] = bc[0]
G8 = [[sum(a2[i] * b2[i] for i in range(8)) for b2 in lines] for a2 in lines]
w = json.load(open('ii19_ext120_interim.json', 'rt'))
frames = w['frames']
start, final = list(w['start']), list(w['final'])
nreg = len(start)
F_FULL = 1
# THE I2-FRAMES (the partner: the co-line (the b/c-srcs!!) or the first-⊥ (the rest!!))
I2 = []
for l in range(V):
    x = co_line.get(l)
    if x is None or G8[l][x] != 0:
        x = next((s for s in range(V) if s != l and G8[l][s] == 0), None)
    basis = rref([list(lines[l]), list(lines[x])], 8)
    assert gram_det(basis) != 0, ('degenerate pair', l, x)
    frames.append([[str(v) for v in row] for row in basis])
    I2.append(len(frames) - 1)
log('the I2-rungs: %d' % V)
own_base = 2 * V + NP
A = list(w['A'])
changed = 0
for gi, (F, d, srcs) in enumerate(A):
    if d >= own_base and len(srcs) == 1 and srcs[0] == d - own_base:
        l = srcs[0]
        A[gi] = [I2[l], d, [l]]
        changed += 1
log('the own-builds raised: %d' % changed)
C = [[F_FULL, d, srcs] for (_, d, srcs) in reversed(A)]
w2 = dict(w)
w2['frames'] = frames
w2['A'] = A
w2['C'] = C
path = 'ii19_ext120_ladder1.json'
with open(path, 'wt') as f:
    json.dump(w2, f)
log('THE WORD WRITTEN: %s' % path)
from gcheck import main
try:
    out = main(path, do_price=True)
    log('THE GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)
