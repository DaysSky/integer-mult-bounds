"""THE LADDER-EMISSION STAGE 1 (ii19_nat82.py) — the own-helpers' ladders!!

THE RESHAPE-TARGET (§708!!): the word's hist -> the {1: ~1010, 2: ~1038, 3: ~53, 4: ~34,
5: ~79, 6: ~9, 7: ~15}-class (the F(0) < 0 (THE ROOT (+47.36%!!!))).
THE LEVER 1 (THE OWN-HELPERS (the 220!!)): their chains (the 0 -> SINGLE (rank-1!!) +
the C-climbs (the SINGLE -> FULL (rank-7s!!!)) -> THE LADDERS (the q_l's builds at the
RAISED frames (the 0 -> I_1 -> I_2 -> ... -> FULL (the split-climbs (the src-l's
laddered reads!!!))). EACH STAGE GCHECK-HELD!!!
"""
import os, sys, json
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

w = json.load(open('ii19_ext120_interim.json', 'rt'))
V, h = w['v'], w['h']
frames = w['frames']
start, final = list(w['start']), list(w['final'])
nreg = len(start)
F_FULL = 1
# THE SHARED LADDER-RUNGS (the generic (the... — NO!! THE HONEST: THE PIECES' FRAMES
# AS THE RUNGS?! — hmm — the simplest: THE OWN-HELPERS' A-GATES AT RAISED FRAMES:
# the q_l's build: [I2_l, q_l, [l]] (the 0 -> dim-2 (the src-l's climb SINGLE -> I2!!)
# — the I2_l = span{l, x_l} (the extension-line (the ⊥-partner?! (the any-legal!!!
# THE PER-HELPER 2-STEP LADDER: 0 -> I2 (rank 2!!) -> FULL (the C (the rank-6!!)):
# the hist-shift: the {1: +220 (the 0->I2?! no — the RANK-2 (the {2: +220!!!)) + the
# C-climbs (the I2 -> FULL (the rank-6 (the {6: ...})))
L = [[Fraction(x) for x in l] for l in w['lines']]
G = [[sum(a[i] * b[i] for i in range(8)) for b in L] for a in L]
new_frames = 0
I2 = []
for l in range(V):
    # the partner: the first ⊥-line (the nondegenerate pair!!)
    x = next((s for s in range(V) if s != l and G[l][s] == 0), None)
    basis = rref([list(L[l]), list(L[x])], 8)
    assert gram_det(basis) != 0, ('degenerate pair', l)
    frames.append([[str(v) for v in row] for row in basis])
    I2.append(len(frames) - 1)
    new_frames += 1
log('the I2-rungs: %d (the new frames %d!!)' % (V, new_frames))
# THE A-EDIT: the own-helpers' gates [SINGLE[l], q_l, [l]] -> [I2_l, q_l, [l]]
# (the q_l: 0 -> dim-2 (rank 2!!) + the src-l: SINGLE -> I2 (rank-1!!!))
NP = 54
own_base = 2 * V + NP
A = list(w['A'])
changed = 0
for gi, (F, d, srcs) in enumerate(A):
    if d >= own_base and len(srcs) == 1 and srcs[0] == d - own_base and F <= len(w['frames']):
        # the own-helper's build-gate (the [SINGLE[l], q_l, [l]]!!)
        l = srcs[0]
        A[gi] = [I2[l], d, [l]]
        changed += 1
log('the own-build gates raised: %d' % changed)
# THE C: the A-reversal at FULL (the same (the srcs' laddered climbs (the I2 -> FULL!!
C = [[F_FULL, d, srcs] for (_, d, srcs) in reversed(A)]
w2 = dict(w)
w2['frames'] = frames
w2['A'] = A
w2['C'] = C
path = 'ii19_ext120_ladder1.json'
with open(path, 'wt') as f:
    json.dump(w2, f)
log('THE WORD WRITTEN: %s (the own-helpers laddered!!)' % path)
from gcheck import main
try:
    out = main(path, do_price=True)
    log('THE GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)
