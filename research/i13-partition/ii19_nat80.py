"""THE INTERIM-WORD EMISSION (ii19_nat80.py) — the economy-mass trivial-delivery word!!

THE ALGEBRA (§648-9!!): the own-helpers q_t (the SINGLETON-builds (the trivial's e_t
delivery ✓✓✓)) + THE PIECES (the real registers (the 3-line values!!)) + THE PAIRED-READS
(each piece read TWICE at the same frame by its users (the value-XOR CANCELS ✓✓ (the
climbs legal (the first: the climb; the second: the no-climb!!!)))) — THE DELIVERED
UNCHANGED (e_t ✓✓✓) + THE ECONOMY'S REAL MASS (the verified-c's root-regime!!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
h = 8
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]

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

# the matching (nat78's!!)
bc_used = set()
kept = []
order = sorted(range(len(pool)), key=lambda i: -len(pool[i][1]))
for i in order:
    ps, users = pool[i]
    found = None
    for a in ps:
        bc = [s for s in ps if s != a]
        if bc[0] in bc_used or bc[1] in bc_used:
            continue
        found = (a, bc)
        break
    if found is None:
        continue
    a, bc = found
    bc_used |= set(bc)
    kept.append((i, a, bc))
NP = len(kept)
log('the pieces: %d' % NP)

# ============ THE FRAMES ============
frames = [[]]
frames.append([[str(1 if i == j else 0) for j in range(h)] for i in range(h)])
F_FULL = 1
def add_frame(basis, tag):
    assert gram_det(basis) != 0, ('degenerate', tag)
    frames.append([[str(x) for x in row] for row in basis])
    return len(frames) - 1
SINGLE = [add_frame([list(lines[s])], 's%d' % s) for s in range(V)]
TPERP = []
for t in range(V):
    al = list(lines[t])
    piv = next(c for c in range(8) if al[c] != 0)
    basis = []
    for f2 in range(8):
        if f2 == piv: continue
        vec = [Fraction(0)] * 8
        vec[f2] = Fraction(1)
        vec[piv] = Fraction(-al[f2], al[piv])
        basis.append(vec)
    TPERP.append(add_frame(basis, 'p%d' % t))
PF = []
for k, (i, a, bc) in enumerate(kept):
    basis = rref([list(lines[x]) for x in sorted([a] + bc)], 8)
    assert gram_det(basis) != 0, ('pf-degenerate', k)
    PF.append(add_frame(basis, 'pf%d' % k))
log('the frames: %d' % (len(frames) - 1))

# ============ THE REGISTERS ============
# sources [0, V) | targets [V, 2V) | pieces [2V, 2V+NP) | own-helpers [2V+NP, 2V+NP+V)
pieces_base = 2 * V
own_base = 2 * V + NP
nreg = own_base + V
R = NP + V                    # the actual helper count!!
start = [0] * nreg
final = [0] * nreg
for s in range(V):
    start[s] = SINGLE[s]
    final[s] = F_FULL
for t in range(V):
    final[V + t] = TPERP[t]
for q in range(pieces_base, nreg):
    final[q] = F_FULL
log('the registers: %d (R = %d!!)' % (nreg, R))

# ============ THE GATES ============
A = []
for k, (i, a, bc) in enumerate(kept):
    q = pieces_base + k
    A.append([SINGLE[a], q, [a]])
for t in range(V):
    q = own_base + t
    A.append([SINGLE[t], q, [t]])
A_gate2 = [[PF[k], pieces_base + k, kept[k][2]] for k in range(NP)]
A = A + A_gate2
log('the A-gates: %d (the block-1 singleton-reads %d + the block-2 PF-climbs %d!!)' % (
    len(A), NP + V, NP))
# THE B: EMPTY (the pieces as the pure mass-carriers (the A + the C (the self-only
# finals ✓✓)) + the trivial's own-delivery (the scatter (the e_t ✓✓✓)))
B = []
log('the B-gates: %d (the pure-mass design!!)' % len(B))
# THE SCATTER: the own-helpers (the trivial's e_t delivery ✓✓✓)
ret = [own_base + t for t in range(V)]
ret_frames = [SINGLE[t] for t in range(V)]
scatter = [[t] for t in range(V)]
# THE C: the A-reversal at FULL
C = [[F_FULL, d, srcs] for (_, d, srcs) in reversed(A)]
# THE D: the scatter-rets' self-bit cancellation (the trivial's ✓✓✓)
D = [[0, V + t, [ret[t]]] for t in range(V)]
w = dict(
    h=h, v=V, R=R,
    form=dict(num=[[1 if i == j else 0 for j in range(h)] for i in range(h)], den=2),
    lines=[[float(x) for x in lines[s]] for s in range(V)],
    frames=frames, start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=ret, ret_frames=ret_frames, scatter=scatter,
)
path = 'ii19_ext120_interim.json'
with open(path, 'wt') as f:
    json.dump(w, f)
log('THE WORD WRITTEN: %s (R = %d!!)' % (path, R))
from gcheck import main
try:
    out = main(path, do_price=True)
    log('THE GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)
