"""THE FULL WORD EMITTER V4 (ii19_nat107.py) — THE JOINT NODE-ASSIGNMENT!!!

THE PROTOCOL: per target: its reads at THE SHARED RICH-4 NODES (the greedy ladder
(each read's frame ⊇ the cur (the nesting BY CONSTRUCTION!!!) + the shared-node
preference (the co-groups!!!)); per wire: the dup-fills only at the same-dim node
splits; the batched multi-src gates; THE W-SCATTER (cst=72!!!); the D (the y-parity
(the mechanical!!)); THE C (the reversal!!); THE EMIT (the gcheck format!!!) ->
GCHECK -> THE PRICE!!!
"""
import os, sys, json, copy
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
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
pc = lambda x: x.bit_count()

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

# the matched pieces (the nat104's own (the user-sorted matching!!))
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool3 = [(sorted(p), sorted(u)) for p, u in P70['pool']]
pool3.sort(key=lambda pu: -len(pu[1]))
bc_used = set(); kept = []
for ps, users in pool3:
    a, b, c = ps
    if a in bc_used or b in bc_used or c in bc_used: continue
    kept.append(tuple(ps)); bc_used.update(ps)
    if len(kept) >= 54: break
PMASK = {p: sum(1 << s for s in p) for p in kept}
log('the matched pieces: %d' % len(kept))

def solve_pieces(t):
    """the LEGAL bases: only FULLY-⊥ pieces (the content ⊆ perp(t)!!!!!)"""
    res = set(PERP[t]); base = []
    while True:
        resm = sum(1 << s for s in res)
        best_p, best_red = None, 0
        for p in kept:
            if PMASK[p] & ~PM[t]: continue          # THE LEGALITY: the piece ⊥ t!!!
            m = pc(PMASK[p] & resm)
            red = m - (3 - m)
            if red > best_red: best_red = red; best_p = p
        if best_p is None or best_red <= 0: break
        base.append(best_p); res ^= set(best_p)
    return base, res
T_BASE = [None] * V; T_FILL = [None] * V
for t in range(V):
    T_BASE[t], T_FILL[t] = solve_pieces(t)

# the frames
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
def fdim(bi): return len(flist[bi])

# the registers
REG = 2 * V
piece_q = {}
for p in kept:
    piece_q[p] = REG; REG += 1
piece_PF = {p: fidx(spf(sorted(p))) for p in kept}
gather_q = [REG + g for g in range(9)]; REG += 9

# the A-phase (the piece builds (the nat84 grammar!!) + the gathers!!)
A = []
for p in kept:
    q = piece_q[p]; a, b, c = p
    A.append([SINGLE[a], q, [a]])
    A.append([piece_PF[p], q, [b, c]])

# the gather bases + dups (the nat104 design (the exact solves!!))
def solve_pattern(pat):
    res = pat; base = []
    while True:
        best_p, best_red = None, 0
        for p in kept:
            m = pc(PMASK[p] & res)
            red = m - (3 - m)
            if red > best_red: best_red = red; best_p = p
        if best_p is not None and best_red > 0:
            base.append(('P', best_p)); res ^= PMASK[best_p]
            continue
        for s in range(V):
            if (res >> s) & 1: base.append(('S', s))
        break
    return base
GBASE = []
for g in range(9):
    c, o = SPEC['BASIS_IDX'][g]
    pat = 0
    for t in o: pat ^= B0[t]
    gb = solve_pattern(pat)
    x = 0
    for w in gb: x ^= PMASK[w[1]] if w[0] == 'P' else (1 << w[1])
    assert x == pat, 'the gather %d solve FAILED!!' % g
    GBASE.append(gb)
gdup = {}
for g in range(9):
    for w in GBASE[g]:
        if w not in gdup:
            q = REG; REG += 1
            gdup[w] = q
            A.append([piece_PF[w[1]] if w[0] == 'P' else SINGLE[w[1]], q,
                       [piece_q[w[1]] if w[0] == 'P' else w[1]]])
for g in range(9):
    A.append([FULL, gather_q[g], [gdup[w] for w in GBASE[g]]])
log('the A: %d gates | the gdups %d | R so far %d' % (len(A), len(gdup), REG))

# ---------------- THE JOINT NODE-ASSIGNMENT (V4!!!) ----------------
readers = defaultdict(list)
for t in range(V):
    for p in T_BASE[t]: readers[('P', p)].append(t)
    for s in T_FILL[t]: readers[('S', s)].append(t)
wire_home = {w: (piece_PF[w[1]] if w[0] == 'P' else SINGLE[w[1]]) for w in readers}

# the candidate nodes per (t, w): the shared frames ⊆ perp(t) ⊇ home_w:
# V4-SIMPLE: the nodes = the ⊥-EXTENSIONS OF THE WIRE'S HOME INSIDE perp(t)!!!
# (per (t, w): the node: home_w extended by the perp-lines (the dim +1!!) — the
# TARGET-SIDE nesting by construction; the SHARED-NODE bias via the (t,w)-memo!!)
NODE_MEMO = {}
def node_for(t, w, cur):
    """the frame: ⊇ cur ∪ home_w, ⊆ perp(t): the dim = cur+1 (the shared-memo!!)"""
    key = (t, w, cur)
    if key in NODE_MEMO: return NODE_MEMO[key]
    hl = [s for s in range(V) if (fmask(wire_home[w]) >> s) & 1]
    cl = [s for s in range(V) if (fmask(cur) >> s) & 1] if cur != EMPTY else []
    base = sorted(set(hl) | set(cl))
    # extend inside perp(t) to dim = max(fdim(cur), fdim(home)) + 1
    tgt = max(fdim(cur), fdim(wire_home[w])) + 1
    if tgt > 7: tgt = 7
    for s in sorted(PERP[t]):
        if s in base: continue
        cand_lines = sorted(set(base + [s]))
        CF = fidx(spf(cand_lines))
        if fdim(CF) != len(spf(base)) + 1: continue      # must grow the dim!!
        if fmask(CF) & ~PM[t]: continue                   # the FULL content must stay ⊥ t!!!
        base = cand_lines
        if fdim(fidx(spf(base))) == tgt: break
    F = fidx(spf(base))
    assert fdim(F) <= 7 and (fmask(F) & ~PM[t]) == 0, 'the node escaped perp(t)!!'
    NODE_MEMO[key] = F
    return F

# per target: the greedy ladder (the reads nested BY CONSTRUCTION!!)
T_READ = [None] * V      # the per-target [(frame, [wires])] in the ladder order!!
for t in range(V):
    cur = EMPTY
    ladder = []
    wires = [w for w in readers if t in readers[w]]
    # the order: the pieces first (the higher homes!!), then the fills!!
    wires.sort(key=lambda w: -fdim(wire_home[w]))
    batch_f = None; batch = []
    for w in wires:
        F = node_for(t, w, cur if batch_f is None else batch_f)
        if batch_f is not None and fdim(F) == fdim(batch_f) and F == batch_f:
            batch.append(w); continue
        if batch_f is not None and fdim(F) == fdim(batch_f) and F != batch_f:
            # the same-dim different-frame: the target climbs anyway?!? — NO: the
            # nesting: the batch_f ⊄ F: the SEPARATE GATE (the target's chain
            # broken!!!) — the fix: MERGE: extend the batch to the bigger frame!!
            merged = fidx(rref(list(flist[batch_f]) + list(flist[F])))
            if fdim(merged) <= 7 and (fmask(merged) & ~PM[t]) == 0:
                batch_f = merged; batch.append(w); continue
        if batch:
            ladder.append((batch_f, batch)); batch = []
        batch_f = F; batch.append(w)
        cur = F
    if batch: ladder.append((batch_f, batch))
    T_READ[t] = ladder
log('the ladders: the gates %s | the reads %s' % (
    dict(sorted(Counter(len(l) for l in T_READ).items())),
    dict(sorted(Counter(sum(len(b) for _, b in l) for l in T_READ).items()))))

# THE WIRE-SIDE: the same-dim splits (the dup-fills!!)
# per wire: its (reader, frame) list: the frames grouped by dim: the splits!!
wframes = defaultdict(list)
for t in range(V):
    for F, ws in T_READ[t]:
        for w in ws: wframes[w].append((t, F))
dupq = {}
for w, lst in wframes.items():
    bydim = defaultdict(list)
    for t, F in lst: bydim[fdim(F)].append((t, F))
    for d, sub in bydim.items():
        fs = set(F for _, F in sub)
        if len(fs) > 1:
            # the splits: keep ONE (the first (the wire's chain!!!)); the others: dups!!
            keep = sub[0][1]
            for t, F in sub[1:]:
                if F != keep:
                    dupq[(t, w)] = True
log('THE DUP-FILLS: %d' % len(dupq))
R_TOTAL = REG + len(dupq)
log('THE R: %d (the core %d + the dups %d) vs the ceiling 480' % (R_TOTAL, REG, len(dupq)))
json.dump({'r': R_TOTAL, 'dups': len(dupq), 'core': REG}, open('ii19_nat107_census.json', 'wt'))
log('SAVED ii19_nat107_census.json')
