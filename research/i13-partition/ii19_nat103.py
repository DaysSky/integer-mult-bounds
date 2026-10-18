"""THE EMITTER V1 (ii19_nat103.py) — THE 54-PIECE + SOURCES-AS-FILLS ARCHITECTURE!!!

THE ARCHITECTURE (the build-duty-honest!!!):
- THE 54 MATCHED PIECES (the nat78/84's own (the duty-legal builds!!!)) — the B-basis;
- THE FILL-SOURCES: the per-target residuals delivered by THE SOURCES THEMSELVES
  (the legal B-srcs (the r434's own 210!!!)) via THEIR LADDERS (the shared co-group
  rungs (the 63-reader forest!!!));
- THE 9 GATHERS (the W-scatter (cst=72!!!)) built from the dup-copies (V1: the
  dup-per-wire-gather (the budget ~347!!!));
- THE FOREST V1: the per-target rung-ladders + THE DUP-FILLS at the violations;
- THE D (the y-parity!!) + THE C (the reversal!!) + THE AUDIT + THE EMIT!!!
"""
import os, sys, json
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
LINES = [tuple(int(x) for x in l) for l in SPEC['lines']]
W_SC = [list(map(int, w)) for w in SPEC['W']]
PERP = [set(p) for p in SPEC['PERP']]
B0 = [sum(1 << s for s in ({t} | PERP[t])) for t in range(V)]

# ---------------- the 54 pieces (the nat70 pool + the bc-matching (the nat78!!)) ----------------
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool3 = [(sorted(p), sorted(u)) for p, u in P70['pool']]
# the perp[a] bitmask helpers
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
pc = lambda x: x.bit_count()
# the bc-matching (the nat78 grammar: each source <= 1 bc-duty!!)
def rref(rows, n=8):
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
def spans(vs): return len(rref([list(x) for x in vs]))

bc_used = set(); kept = []
for ps, users in pool3:
    a, b, c = ps
    if a in bc_used or b in bc_used or c in bc_used: continue
    # the 2-gate build: [SINGLE_a, q, [a]] + [PF, q, [b, c]]: the bc-duties: b, c!!
    if b in bc_used or c in bc_used: continue
    kept.append(ps); bc_used.update([a, b, c])
    if len(kept) >= 54: break
log('the matched pieces: %d (the bc-duties %d)' % (len(kept), len(bc_used)))

# the per-target piece-bases (the red-greedy over the kept pieces!!)
PIECE_MASK = {tuple(p): sum(1 << s for s in p) for p in kept}
def solve_pieces(t):
    res = set(PERP[t]); base = []
    while True:
        resm = sum(1 << s for s in res)
        best_p, best_red = None, 0
        for p in kept:
            m = pc(PIECE_MASK[tuple(p)] & resm)
            red = m - (3 - m)
            if red > best_red: best_red = red; best_p = p
        if best_p is None: break
        base.append(tuple(best_p)); res ^= set(best_p)
    return base, res          # the residual: THE FILL-SOURCES!!!
T_BASE = [None] * V; T_FILL = [None] * V
for t in range(V):
    T_BASE[t], T_FILL[t] = solve_pieces(t)
log('the piece-bases: the reads %s | the fills %s' % (
    dict(sorted(Counter(len(b) for b in T_BASE).items())),
    dict(sorted(Counter(len(f) for f in T_FILL).items()))))

# ---------------- the frames ----------------
fmap = {}; flist = []
def fidx(basis):
    key = tuple(tuple(r) for r in basis)
    if key not in fmap:
        fmap[key] = len(flist); flist.append(key)
    return fmap[key]
def spf(idx): return rref([list(LINES[i]) for i in idx])
EMPTY = fidx([]); FULL = fidx(rref([list(x) for x in LINES]))
SINGLE = [fidx(spf([s])) for s in range(V)]
TPERP = [fidx(spf(sorted(PERP[t]))) for t in range(V)]
_fmask = {}
def fmask(bi):
    if bi in _fmask: return _fmask[bi]
    B = flist[bi]; m = 0
    for s in range(V):
        if spans(list(B) + [list(LINES[s])]) == len(B): m |= (1 << s)
    _fmask[bi] = m
    return m

# ---------------- the registers ----------------
REG = 2 * V
piece_q = {}; piece_PF = {}
for p in kept:
    piece_q[tuple(p)] = REG; REG += 1
    piece_PF[tuple(p)] = fidx(spf(sorted(p)))
gather_q = [REG + g for g in range(9)]; REG += 9
# the gather-side dup pool (V1: the dup-per-wire (the pieces + the sources!!))
dupn = Counter()
gdup = {}      # (wire, wire-reg-or-src, gather) -> the dup register
def newdup():
    global REG
    q = REG; REG += 1
    return q

# ---------------- THE A-PHASE ----------------
A = []
# (1) the pieces' builds (the nat84 grammar!!)
for p in kept:
    q = piece_q[tuple(p)]
    a, b, c = p
    A.append([SINGLE[a], q, [a]])                      # the a-duty (a stays!!!)
    A.append([piece_PF[tuple(p)], q, [b, c]])          # the bc-duties (b,c climb ONCE!!)
log('the piece builds: %d gates' % len(A))

# (2) the gathers' bases (the pieces-first + the sources!!!) + the dup-builds!!
def solve_pattern(pat):
    res = pat; base = []
    while res:
        best_p, best_red = None, 0
        for p in kept:
            m = pc(PIECE_MASK[tuple(p)] & res)
            red = m - (3 - m)
            if red > best_red: best_red = red; best_p = p
        if best_p is not None and best_red > 0:
            base.append(('P', tuple(best_p))); res ^= PIECE_MASK[tuple(best_p)]
            continue
        # the source-fills!!
        rl = [s for s in range(V) if (res >> s) & 1]
        for s in rl: base.append(('S', s))
        break
    return base
GBASE = []
for g in range(9):
    c, o = SPEC['BASIS_IDX'][g]
    pat = 0
    for t in o: pat ^= B0[t]
    gb = solve_pattern(pat)
    x = 0
    for w in gb:
        x ^= PIECE_MASK[w[1]] if w[0] == 'P' else (1 << w[1])
    assert x == pat, 'the gather %d solve FAILED!!' % g
    GBASE.append(gb)
log('the gather bases: %s' % [len(gb) for gb in GBASE])
# the dup-registers per (wire, gather)!!
gdup = {}
for g in range(9):
    for w in GBASE[g]:
        key = (w, g)
        q = newdup()
        gdup[key] = q
        if w[0] == 'P':
            A.append([piece_PF[w[1]], q, [piece_q[w[1]]]])
        else:
            A.append([SINGLE[w[1]], q, [w[1]]])
log('the gather-side dups: %d (V1: per-wire-gather!!)' % len(gdup))
log('THE R SO FAR: %d' % REG)
json.dump({'pieces': [list(p) for p in kept],
           'bases': [[list(x) for x in b] for b in T_BASE],
           'fills': [sorted(f) for f in T_FILL],
           'gbases': [[([ 'P', list(w[1])] if w[0] == 'P' else ['S', w[1]]) for w in gb] for gb in GBASE]},
          open('ii19_nat103_design.json', 'wt'))
log('SAVED ii19_nat103_design.json (THE PHASE-1!!!)')
