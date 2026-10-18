"""THE PIECES-EMISSION (ii19_nat74.py) — the first REAL delivery -> GCHECK!!

THE CLEAN CHAINS (nat73!!): 118 pieces (the 3-gate grammar: SINGLE[a] -> CELL(a,b) ->
HOME(c)!!) + the 9 gathers (the W-scatter ✓!!) + the targets. THE DELIVERY: the scatter
delivers B'[t] (the W-rows!!); the pieces' reads XOR toward e_t (the partial coverage
(the leftovers pending the carriers!!)) -> THE EXPECTED REJECT (the balance!!) — THE
GCHECK'S HONEST FEEDBACK (the content/climb rules at the real delivery!!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
CH = json.load(open('ii19_nat73_chains.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
h = 8
W = SPEC['W']
BASIS_IDX = SPEC['BASIS_IDX']
PERP = [set(p) for p in SPEC['PERP']]
kept = [(i, a, b, c) for i, a, b, c in CH['kept']]
partner = {int(k): v for k, v in CH['partner'].items()}
c_home = {int(k): v for k, v in CH['c_home'].items()}
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]
log('the pieces kept: %d | the pool: %d' % (len(kept), len(pool)))

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

# ============ THE FRAME LIST ============
frames = [[]]
frames.append([[1 if i == j else 0 for j in range(h)] for i in range(h)])      # 1 = FULL
F = {}
F['full'] = 1
def add_frame(basis, tag):
    assert gram_det(basis) != 0, ('degenerate', tag)
    frames.append([[str(x) for x in row] for row in basis])
    return len(frames) - 1
SINGLE = []
for s in range(V):
    SINGLE.append(add_frame([list(lines[s])], 'single%d' % s))
TPERP = []
for t in range(V):
    # the 7-dim perp-space basis (nat69's construction!!)
    al = list(lines[t])
    piv = next(c for c in range(8) if al[c] != 0)
    basis = []
    for f2 in range(8):
        if f2 == piv: continue
        v = [Fraction(0)] * 8
        v[f2] = Fraction(1)
        v[piv] = Fraction(-al[f2], al[piv])
        basis.append(v)
    TPERP.append(add_frame(basis, 'perp%d' % t))
# the cells: span(a, b) (the pairs (the partner-structure!!)
CELL = {}
for b, a in partner.items():
    key = (a, b)
    if key not in CELL:
        basis = rref([list(lines[a]), list(lines[b])], 8)
        CELL[key] = add_frame(basis, 'cell%s' % (key,))
# the homes: the c-homes' spans EXTENDED to dim >= 3 (the STRICT climb rule (gcheck:
# dims[F] > dims[cur]!!!) — the cell (dim 2) -> the home MUST be dim >= 3!!)
HOME = {}
G8 = [[sum(a[i] * b[i] for i in range(8)) for b in lines] for a in lines]
for c, v in c_home.items():
    span_idx = sorted(set(v['span']))
    basis = rref([list(lines[x]) for x in span_idx], 8)
    d = len(basis)
    if d > 4:
        log('  !! the home dim %d at c=%d (the skip!!)' % (d, c))
        continue
    # the extension: the lines ⊥ the whole basis (the Gram-check per addition!!)
    for ext in range(V):
        if d >= max(3, len(rref([list(lines[x]) for x in span_idx], 8))):
            if d >= 3:
                break
        if ext in span_idx: continue
        cand = [list(lines[ext])]
        if all(sum(basis[i][k] * lines[ext][k] for k in range(8)) == 0 for i in range(d)):
            nb = rref(list(basis) + cand, 8)
            if gram_det(nb) != 0 and len(nb) == d + 1 and len(nb) <= 4:
                basis = nb; d += 1
                span_idx = sorted(set(span_idx) | {ext})
        if d >= 3:
            break
    if d < 3:
        log('  !! the home stuck at dim %d at c=%d (the skip!!)' % (d, c))
        continue
    if gram_det(basis) == 0:
        log('  !! the degenerate home at c=%d (the skip!!)' % c)
        continue
    HOME[c] = add_frame(basis, 'home%d' % c)
log('the frames: %d (FULL + %d singles + %d perps + %d cells + %d homes!!)' % (
    len(frames) - 1, V, V, len(CELL), len(HOME)))

# ============ THE REGISTERS ============
# sources [0, V) | targets [V, 2V) | pieces [2V, 2V+118) | gathers [2V+118, 2V+127)
NP = len(kept)
nreg = 2 * V + NP + 9
pieces_base = 2 * V
gathers_base = 2 * V + NP
R = NP + 9                      # (the carriers pending!!)
log('the registers: R %d (the pieces %d + the 9 gathers (the carriers pending!!))' % (R, NP))
start = [0] * nreg
final = [0] * nreg
for s in range(V):
    start[s] = SINGLE[s]
    final[s] = F['full']
for t in range(V):
    final[V + t] = TPERP[t]
for q in range(pieces_base, nreg):
    final[q] = F['full']

# ============ THE GATES ============
# THE A-PHASE: the pieces' 3-gate builds (the running-sums!!) + the gathers' builds!!
A = []
skipc = 0
for k, (i, a, b, c) in enumerate(kept):
    q = pieces_base + k
    A.append([SINGLE[a], q, [a]])                      # 0 -> 1: read a (free!!)
    if (a, b) not in CELL:
        skipc += 1
        continue
    A.append([CELL[(a, b)], q, [b]])                   # 1 -> 2: read b (its cell!!)
    if c in HOME:
        A.append([HOME[c], q, [c]])                    # 2 -> dim: read c (its home!!)
log('the A-gates: %d (the skips: %d)' % (len(A), skipc))
# THE GATHERS: the 9 values (the BASIS rows (the line-XORs!!)) — the builds: the sources
# read at their singletons?! — THE WALL... THE HONEST FIRST VERSION: the gathers built
# from the PIECES?! — the simplest: the gathers' values assembled from the SOURCES at
# their SINGLETONS with the one-per-gate rule... (the same wall!!) — THE STAGED HONESTY:
# THE GATHERS VIA THE TRIVIAL-STYLE (the per-gather ONE helper-chain... deferred!!
# THE FIRST EMISSION: the scatter via the TRIVIAL rets (the own-lines (the e8-template!!))
# THE FIRST EMISSION: the scatter via the PIECES as rets (their values: the 3-line sets!!),
# the ret-frames = THE PIECES' A-END POSITIONS (the last A-gate's frame (the pub2-extraction!!))
ret = []
ret_frames = []
for k, (i, a, b, c) in enumerate(kept):
    q = pieces_base + k
    # the piece's last A-frame (the home if gated, else the cell, else the singleton!!)
    last = SINGLE[a]
    if (a, b) in CELL:
        last = CELL[(a, b)]
    if c in HOME:
        last = HOME[c]
    ret.append(q)
    ret_frames.append(last)
# the scatter rows: THE FIRST HONEST DELIVERY-STAGE (the diagnostic minimal: the target
# scatters ITS FIRST piece (the balance pending the B-reads!!))
scatter = []
for t in range(V):
    myp = [k for k, (i, a, b, c) in enumerate(kept) if t in pool[i][1]]
    scatter.append(myp[:1] if myp else [])
B = []
C = [[F['full'], d, [s]] for (_, d, [s]) in reversed(A)]
# THE D: the doubling (the targets' B-srcs (none yet!!) + the scatter-rets!!)
D = []
for t in range(V):
    if scatter[t]:
        D.append([0, V + t, [ret[scatter[t][0]]]])
w = dict(
    h=h, v=V, R=R,
    form=dict(num=[[1 if i == j else 0 for j in range(h)] for i in range(h)], den=2),
    lines=[[float(x) for x in lines[s]] for s in range(V)],
    frames=frames, start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=ret, ret_frames=ret_frames, scatter=scatter,
)
path = 'ii19_ext120_pieces.json'
with open(path, 'wt') as f:
    json.dump(w, f)
log('THE WORD WRITTEN: %s (the pieces %d + the trivial scatter!!)' % (path, NP))

from gcheck import main
try:
    out = main(path, do_price=True)
    log('THE GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)
