"""THE LADDER-STAGE-1-FINAL (ii19_nat84.py) — the post-PF own-builds!!

THE §726's TRACE-FIX: the b/c-srcs' own-builds AT THE POST-PF I3-RUNGS (the piece's PF
+ a-⊥-extension (dim 3!!)) IN THE BLOCK-3 (AFTER the gate-2s!!) — the src's chain:
SINGLE -> PF (rank-1!!) -> I3 (rank-1!!) -> FULL (rank-5!!) — ALL STRICTLY-LEGAL!!!
THE a-only-srcs (12!!): the I2-rungs (any-⊥ (dim 2!!)) — THE GCHECK RUN!!!
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

# the matching + the pieces (the nat78's exact!!)
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
G8 = [[sum(a2[i] * b2[i] for i in range(8)) for b2 in lines] for a2 in lines]

# the pieces' PF-spans (the src's piece-PF map!!)
pf_of = {}
for k, (i, a, bc) in enumerate(kept):
    ps = sorted([a] + bc)
    pf_of[bc[0]] = ps
    pf_of[bc[1]] = ps

w = json.load(open('ii19_ext120_interim.json', 'rt'))
frames = w['frames']
F_FULL = 1
# THE POST-PF I3/I2 RUNGS!!
RUNG = {}
for l in range(V):
    if l in pf_of:
        # the b/c-src: the I3 = the piece's span + a-⊥-extension (dim 3 (the rank-3-span's case: dim 2!!))
        ps = pf_of[l]
        basis = rref([list(lines[x]) for x in ps], 8)
        d = len(basis)
        want = max(3, d + 1)         # the rung STRICTLY above the PF!!!
        while d < want:
            ext = next((s for s in range(V) if s not in ps and
                        all(sum(basis[i2][k] * lines[s][k] for k in range(8)) == 0 for i2 in range(d)) and
                        gram_det(rref(list(basis) + [list(lines[s])], 8)) != 0), None)
            if ext is None: break
            nb = rref(list(basis) + [list(lines[ext])], 8)
            if gram_det(nb) != 0 and len(nb) == d + 1:
                basis = nb; d += 1
                ps = ps + [ext]
            else:
                break
        frames.append([[str(v) for v in row] for row in basis])
        RUNG[l] = len(frames) - 1
    else:
        # the a-only-src: the I2 (any-⊥!!)
        x = next((s for s in range(V) if s != l and G8[l][s] == 0), None)
        basis = rref([list(lines[l]), list(lines[x])], 8)
        frames.append([[str(v) for v in row] for row in basis])
        RUNG[l] = len(frames) - 1
log('the rungs: %d (the b/c: %d | the a-only: %d!!)' % (
    len(RUNG), len(pf_of), V - len(pf_of)))

own_base = 2 * V + NP
# THE A (the 3-blocks!!): block-1 (the gate-1s (the srcs' homes!!)) + block-2 (the gate-2s
# (the b/c-climbs!!)) + block-3 (the own-builds (the post-PF (the raised!!)))
A = list(w['A'])
# the interim's A-order: the block-1 = the first (NP + V) (the §657's!!); the block-2 = the rest!!
b1 = A[:NP + V]
b2 = A[NP + V:]
# the own-builds extracted from the block-1 (the dests >= own_base!!)
b1_own = [g for g in b1 if g[1] >= own_base]
b1_gate1 = [g for g in b1 if g[1] < own_base]
b3 = []
for (F, d, srcs) in b1_own:
    l = srcs[0]
    b3.append([RUNG[l], d, [l]])
A2 = b1_gate1 + b2 + b3
log('the A: %d (the b1 %d + the b2 %d + the b3 %d!!)' % (len(A2), len(b1_gate1), len(b2), len(b3)))
C = [[F_FULL, d, srcs] for (_, d, srcs) in reversed(A2)]
# THE RET-FRAMES (the own-helpers' NEW A-ENDS (the RUNGs (the §428's extraction-rule!!!))
ret_frames = [RUNG[l] for l in range(V)]
w2 = dict(w)
w2['frames'] = frames
w2['A'] = A2
w2['C'] = C
w2['ret_frames'] = ret_frames
path = 'ii19_ext120_ladder2.json'
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
