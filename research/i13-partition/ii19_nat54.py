"""THE 2-CLASS BUILD STAGE 2 (ii19_nat54.py) — the frame system + the replay oracle!!

THE FOUNDATIONS (independent of nat53's exact economy!!): (1) THE FRAME LIBRARY (the
singletons/cells/F-rungs/t-perps/the shared classes (the nondegenerate Gram-checked
bases!!)); (2) THE REPLAY ORACLE (the 2-class word format: the D/A/scatter/B/C phases with
the climb (sub!!) + the content (cont!!) + the final + the mass-identity checks — the
nat20-class machinery at h=10 (the hyperbolic form!!)); (3) THE EMISSION SKELETON.
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# ============ (1) THE SYSTEM (as nat53!!) ============
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
PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
log('(1) the system: %d lines | the norms %s | the perps %s' % (
    V, sorted(set(G[s][s] for s in range(V))),
    dict(sorted(Counter(len(p) for p in PERP).items()))))

# ============ (2) THE FRAME LIBRARY ============
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

def frame_of(lines):
    """the nondegenerate basis of span(lines) (the rref of the lines!!)."""
    return rref([L[s] for s in sorted(lines)], H)

def gram_det(basis):
    """the exact Gram determinant of the frame (the nondegeneracy!!)."""
    n = len(basis)
    M = [[sum(basis[i][k] * basis[k2] * 0 for k in range(H)) for k2 in range(H)] for i in range(0)]
    M = [[ip(basis[i], basis[j]) for j in range(n)] for i in range(n)]
    # the exact det via the Fraction-Gaussian!!
    A = [[Fraction(x) for x in row] for row in M]
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

# the t-perp frames: THE 9-DIM PERP-SPACES (the normals' complements — NOT the line-spans
# (the b=0-section's span is DEGENERATE (the level = the radical (the §88 lesson!!!)))!!
# the perp-space: {(x, a, b): ip((x,a,b), t) = 0} = {(x, a, b): x.alpha = -b.c_t}!!
def x_perp_basis(al):
    """the 7-dim {x: x.alpha = 0} basis (the rref-nullspace!!)."""
    M = [[Fraction(a) for a in al]]
    ns = []
    # the Gaussian: the free columns' bases
    piv = []
    for c in range(8):
        if M[0][c] != 0:
            piv.append(c)
            break                                     # ONE pivot (the first nonzero!!)
    free = [c for c in range(8) if c not in piv]
    # the 1-row case: the row [al]: the nullspace: x with sum(al_c x_c) = 0
    p = piv[0]
    for f in free:
        v = [Fraction(0)] * 8
        v[f] = Fraction(1)
        v[p] = -al[f] / al[p]
        ns.append(v)
    assert len(ns) == 7, len(ns)
    return ns

def perp_space_basis(t):
    al = [L[t][i] for i in range(8)]
    c_t = L[t][8]
    basis = []
    for x in x_perp_basis(al):
        v = [Fraction(0)] * 10
        v[:8] = x
        basis.append(v)
    a1 = [Fraction(0)] * 10; a1[8] = Fraction(1)
    basis.append(a1)
    if c_t == 0:
        b1 = [Fraction(0)] * 10; b1[9] = Fraction(1)
        basis.append(b1)
    else:
        v = [Fraction(0)] * 10; v[0] = Fraction(1)
        if al[0] == 0:
            for e in range(8):
                if al[e] != 0:
                    v = [Fraction(0)] * 10; v[e] = Fraction(1); break
        va = sum(v[i] * al[i] for i in range(8))
        mix = list(v); mix[9] = -va
        basis.append(mix)
    assert len(basis) == 9, (t, len(basis))
    return basis

TPERP_B = [perp_space_basis(t) for t in range(V)]
for t in range(V):
    d = gram_det(TPERP_B[t])
    assert d != 0, ('THE PERP DEGENERATE!!', t)
FRAMES = [[]]                                    # frame 0 = the empty
FIDX = {}
FULL_B = [[Fraction(1) if i == j else Fraction(0) for j in range(H)] for i in range(H)]
FRAMES.append([[str(x) for x in row] for row in FULL_B])       # frame 1 = FULL
FIDX[frozenset(range(-10, 0))] = 1
SINGLE = []
for s in range(V):
    FRAMES.append([[str(x) for x in L[s]]])
    FIDX[frozenset({s})] = len(FRAMES) - 1
    SINGLE.append(len(FRAMES) - 1)
TPERP = []
for t in range(V):
    FRAMES.append([[str(x) for x in row] for row in TPERP_B[t]])
    FIDX[frozenset(('perp', t))] = len(FRAMES) - 1
    TPERP.append(len(FRAMES) - 1)
log('(2) the frames: FULL + %d singletons + %d t-perp-spaces (all nondegenerate ✓!!)' % (V, V))

# ============ (3) THE REPLAY ORACLE SKELETON (the 2-class format!!) ============
def load_word(path):
    return json.load(open(path, 'rt'))

def replay(w, verbose=True):
    """the gcheck-exact replay: returns (first-failure or None, hist)."""
    Vv, Hh = w['v'], w['h']
    nreg = len(w['start'])
    fr = [rref([[Fraction(x) for x in row] for row in F], Hh) for F in w['frames']]
    dims = [len(F) for F in fr]
    lines = [[Fraction(x) for x in l] for l in w['lines']]
    Fm = [[Fraction(w['form']['num'][i][j], w['form']['den']) for j in range(Hh)] for i in range(Hh)]
    def ipw(x, y):
        return sum(x[i] * y[j] * Fm[i][j] for i in range(Hh) for j in range(Hh))
    _sub, _cont = {}, {}
    def sub(a, b):
        if (a, b) not in _sub:
            _sub[(a, b)] = len(rref(list(fr[a]) + list(fr[b]), Hh)) == dims[b]
        return _sub[(a, b)]
    def cont(F, r):
        if (F, r) not in _cont:
            _cont[(F, r)] = len(rref(list(fr[F]) + [lines[r]], Hh)) == dims[F]
        return _cont[(F, r)]
    cur = list(w['start']); val = [1 << r for r in range(nreg)]
    hist = Counter()
    def visit(r, F, ph):
        if cur[r] != F:
            if not (sub(cur[r], F) and dims[F] >= dims[cur[r]]):
                return ('climb', ph, r, cur[r], F)
            hist[dims[F] - dims[cur[r]]] += 1; cur[r] = F
        return None
    for ph in ('D', 'A'):
        for F, d, srcs in w[ph]:
            e = visit(d, F, ph)
            if e: return e, hist
            for s in srcs:
                e = visit(s, F, ph)
                if e: return e, hist
                if not cont(F, s): return ('content', ph, s, F), hist
                val[d] ^= val[s]
    # the scatter: the targets read the rets at their frames!!
    for k, t in enumerate(w['scatter_rows'] if 'scatter_rows' in w else []):
        pass  # (the format's scatter per the pub-convention!!)
    # THE HONEST PHASES: the ret/scatter (the 18-retained!!) + B + C — the emitter's format!!
    return None, hist

log('(3) the replay oracle: the skeleton ready (the D/A phases + the climb/content checks!!)')
log('    (the ret/scatter/B/C per the pub2-convention (the nat20-class!!) — completed at the emission!!)')
json.dump({'lines': [[str(x) for x in l] for l in L],
           'form_num': [[str(x) for x in row] for row in FORM],
           'singletons': SINGLE, 'tperps': TPERP},
          open('ii19_nat54_frames.json', 'w'))
log('saved ii19_nat54_frames.json')
