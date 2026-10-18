"""THE MULTI-SRC EMISSION (ii19_nat78.py) — the 2-gate piece grammar -> GCHECK!!

THE GRAMMAR: the piece q: [SINGLE[a], q, [a]] (0->1, the a-role FREE!!!) +
[F, q, [b, c]] (1->dim(F): ONE multi-src gate (the b, c climb SINGLE -> F (the
singleton ⊆ F ✓✓ ALWAYS (their lines ∈ the span!!!)))). THE SOURCE-MATCHING: each
source at most ONE b/c-duty (its single F-climb!!) + unlimited a-roles (FREE!!!) ->
EVERY chain nests by construction!!! THE DROPS -> the carriers. THE GCHECK RUN!!!
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
PERP = [set(p) for p in SPEC['PERP']]
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

# ============ THE SOURCE-MATCHING (each source <= 1 b/c-duty (its ONE F-climb!!)) ============
bc_used = set()
kept = []
dropped = []
order = sorted(range(len(pool)), key=lambda i: -len(pool[i][1]))
for i in order:
    ps, users = pool[i]
    x, y, z = ps
    # the roles: 1 a (free!!) + the pair (b, c) (the ≤1-duty sources (the unused ones!!))
    found = None
    for a in ps:
        bc = [s for s in ps if s != a]
        if bc[0] in bc_used or bc[1] in bc_used:
            continue
        found = (a, bc)
        break
    if found is None:
        dropped.append(i)
        continue
    a, bc = found
    bc_used |= set(bc)
    kept.append((i, a, bc))
log('THE MATCHING: kept %d | dropped %d (-> the carriers!!) | the b/c-sources used %d' % (
    len(kept), len(dropped), len(bc_used)))
covered = [set() for _ in range(V)]
for i, a, bc in kept:
    for t in pool[i][1]:
        covered[t] |= set(pool[i][0])
left = [PERP[t] - covered[t] for t in range(V)]
nleft = sum(1 for lo in left if lo)
R = len(kept) + nleft + 9
log('THE ECONOMY: %d pieces + %d carriers + 9 = R %d' % (len(kept), nleft, R))

# ============ THE FRAMES ============
frames = [[]]
frames.append([[str(1 if i == j else 0) for j in range(h)] for i in range(h)])    # FULL
F_FULL = 1
def add_frame(basis, tag):
    assert gram_det(basis) != 0, ('degenerate', tag)
    frames.append([[str(x) for x in row] for row in basis])
    return len(frames) - 1
SINGLE = []
for s in range(V):
    SINGLE.append(add_frame([list(lines[s])], 'single%d' % s))
TPERP = []
for t in range(V):
    al = list(lines[t])
    piv = next(c2 for c2 in range(8) if al[c2] != 0)
    basis = []
    for f2 in range(8):
        if f2 == piv: continue
        vec = [Fraction(0)] * 8
        vec[f2] = Fraction(1)
        vec[piv] = Fraction(-al[f2], al[piv])
        basis.append(vec)
    TPERP.append(add_frame(basis, 'perp%d' % t))
# the pieces' F-frames: span{a, b, c} extended to dim >= 2 (the strict climbs: 1 -> F!!!)
PF = []
G8 = [[sum(a2[i] * b2[i] for i in range(8)) for b2 in lines] for a2 in lines]
for k, (i, a, bc) in enumerate(kept):
    ps = sorted([a] + bc)
    basis = rref([list(lines[x]) for x in ps], 8)
    d = len(basis)
    if d < 2:
        log('  !! the piece %d span dim %d (the skip!!)' % (k, d))
        PF.append(None)
        continue
    # the dim-2 span: the strict climb 1 -> 2 ✓ fine!! (the degenerate-check (the 2-dim
    # span of 3 collinear-ish lines: the Gram (the norm-4 lines: the 2-dim Gram ✓)))
    if gram_det(basis) == 0:
        log('  !! the degenerate piece-span %d (the skip!!)' % k)
        PF.append(None)
        continue
    PF.append(add_frame(basis, 'pf%d' % k))
npf = sum(1 for x in PF if x is not None)
log('THE FRAMES: %d (FULL + %d singles + %d perps + %d piece-frames!!)' % (
    len(frames) - 1, V, V, npf))

# ============ THE REGISTERS + THE GATES ============
NP = len(kept)
nreg = 2 * V + NP + 9
pieces_base = 2 * V
start = [0] * nreg
final = [0] * nreg
for s in range(V):
    start[s] = SINGLE[s]
    final[s] = F_FULL
for t in range(V):
    final[V + t] = TPERP[t]
for q in range(pieces_base, nreg):
    final[q] = F_FULL
A = []
ok_pieces = []
for k, (i, a, bc) in enumerate(kept):
    if PF[k] is None:
        continue
    q = pieces_base + k
    A.append([SINGLE[a], q, [a]])
    ok_pieces.append(k)
# THE TWO-BLOCK A-ORDER: all the gate-1s (the singleton-reads (the srcs at home!!)) FIRST,
# then all the gate-2s (the PF-climbs (the srcs' ONE b/c-climb!!!)) — EVERY chain nests!!!
A_gate2 = [[PF[k], pieces_base + k, kept[k][2]] for k in ok_pieces]
A = A + A_gate2
log('THE A-GATES: %d (the %d gate-1s + %d gate-2s!!)' % (len(A), len(ok_pieces), len(A_gate2)))
ret = [pieces_base + k for k in ok_pieces]
ret_frames = [PF[k] for k in ok_pieces]
scatter = []
for t in range(V):
    myp = [ki for ki, k in enumerate(ok_pieces) if t in pool[kept[k][0]][1]]
    scatter.append(myp[:1] if myp else [])
B = []
C = [[F_FULL, d, srcs] for (_, d, srcs) in reversed(A)]
D = []
for t in range(V):
    if scatter[t]:
        D.append([0, V + t, [ret[scatter[t][0]]]])
w = dict(
    h=h, v=V, R=NP + 9,
    form=dict(num=[[1 if i == j else 0 for j in range(h)] for i in range(h)], den=2),
    lines=[[float(x) for x in lines[s]] for s in range(V)],
    frames=frames, start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=ret, ret_frames=ret_frames, scatter=scatter,
)
path = 'ii19_ext120_multisrc.json'
with open(path, 'wt') as f:
    json.dump(w, f)
log('THE WORD WRITTEN: %s' % path)
from gcheck import main
try:
    out = main(path, do_price=True)
    log('THE GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)
