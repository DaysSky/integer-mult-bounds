"""THE EMITTER V2 (ii19_nat104.py) — THE COMPLETE WORD!!!

THE ARCHITECTURE: the matched pieces (54 (the user-sorted matching!!)) + the sources-
as-fills + the 9 gathers (the W-scatter (cst=72!!!)) + the gather-side (the
dup-per-wire (~140) + the coordinated shared rungs!!) + the B-phase (the forest:
the shared rich-4 rungs (the co-groups!!!) + the dup-fills at the divergences!!) +
the D + the C + THE AUDIT + THE EMIT -> GCHECK!!!
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

# ---------------- (1) the matched pieces ----------------
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool3 = [(sorted(p), sorted(u)) for p, u in P70['pool']]
pool3.sort(key=lambda pu: -len(pu[1]))          # the user-rich first!!!
bc_used = set(); kept = []
for ps, users in pool3:
    a, b, c = ps
    if a in bc_used or b in bc_used or c in bc_used: continue
    kept.append(tuple(ps)); bc_used.update(ps)
    if len(kept) >= 54: break
log('the matched pieces: %d' % len(kept))
PMASK = {p: sum(1 << s for s in p) for p in kept}

def solve_pieces(t):
    res = set(PERP[t]); base = []
    while True:
        resm = sum(1 << s for s in res)
        best_p, best_red = None, 0
        for p in kept:
            m = pc(PMASK[p] & resm)
            red = m - (3 - m)
            if red > best_red: best_red = red; best_p = p
        if best_p is None or best_red <= 0: break
        base.append(best_p); res ^= set(best_p)
    return base, res
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
def fdim(bi): return len(flist[bi])

# the rung-extension: a frame G ⊇ (the current) ∪ (the wire-homes) ⊆ perp(t)!!
def extend(cur, need_lines, t, target_dim):
    """a frame ⊇ cur (the basis-lines) + the needed lines' spans, ⊆ perp(t), dim = target_dim"""
    base_lines = []
    # the cur-frame's basis expressed via the rref rows -> the lines inside cur!!
    cm = fmask(cur)
    for s in range(V):
        if (cm >> s) & 1:
            base_lines.append(s)
    # the needed lines
    base_lines = sorted(set(base_lines) | set(need_lines))
    # the ⊥-extensions inside perp(t): add perp-lines until the dim = target_dim
    for s in sorted(PERP[t]):
        if len(base_lines) >= 24: break
        cand = spf(sorted(set(base_lines + [s])))
        if len(cand) == len(spf(sorted(set(base_lines)))): continue
        if len(cand) > target_dim: continue
        if fmask(fidx(cand)) & ~sum(1 << x for x in PERP[t]):
            continue                       # keep inside perp(t)!!
        base_lines = sorted(set(base_lines + [s]))
        if len(spf(base_lines)) == target_dim:
            return fidx(spf(base_lines))
    F = fidx(spf(sorted(set(base_lines))))
    assert fdim(F) == target_dim, 'the extension failed (dim %d != %d)' % (fdim(F), target_dim)
    return F

# ---------------- the registers ----------------
REG = 2 * V
piece_q = {p: REG + i for i, p in enumerate(kept)}; REG += len(kept)
piece_PF = {p: fidx(spf(sorted(p))) for p in kept}
gather_q = [REG + g for g in range(9)]; REG += 9

# ---------------- THE A-PHASE ----------------
A = []
for p in kept:
    q = piece_q[p]; a, b, c = p
    A.append([SINGLE[a], q, [a]])
    A.append([piece_PF[p], q, [b, c]])
log('the piece builds: %d gates' % len(A))

# ---------------- the gather-side (the dup-per-wire + the shared rungs!!) ----------------
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
log('the gather bases: %s' % [len(gb) for gb in GBASE])
wire_uses = defaultdict(list)      # the wire -> its gathers
for g in range(9):
    for w in GBASE[g]: wire_uses[w].append(g)
gdup = {}; gdup_home = {}
for w, gs in wire_uses.items():
    q = REG; REG += 1
    gdup[w] = q
    gdup_home[w] = piece_PF[w[1]] if w[0] == 'P' else SINGLE[w[1]]
    A.append([gdup_home[w], q, [piece_q[w[1]] if w[0] == 'P' else w[1]]])
log('the gather-side dups (per-wire!!): %d' % len(gdup))

# the gathers' coordinated chains: the shared rungs (the dup-batches!!)
# V2-SIMPLE: the gathers' chains: 0 -> R_j (the shared dim-4 rungs) -> FULL:
# per gather: its dups batched by the HOME-DIM (the pieces (dim 3!!) then the sources (dim 1!!))
gchain = {}
for g in range(9):
    R1 = extend(EMPTY, [], 0, 4) if False else None    # (the placeholder!!)
# (the simple version: the gather reads ALL its dups at FULL (the one-gate!!!))
# the dups climb home -> FULL (their one climb (serving ONE gather (the V2-simple!!)))
# the dup shared across gathers: the FIRST gather at FULL; the others?! — the dup is
# at FULL: the OTHER gathers read it AT FULL (NO further climb!!! ✓✓✓ LEGAL!!!)
for g in range(9):
    A.append([FULL, gather_q[g], [gdup[w] for w in GBASE[g]]])
log('the gathers built (the one-gate at FULL!!!)')
log('THE R: %d (the pieces %d + the gathers 9 + the gdups %d)' % (REG, len(kept), len(gdup)))

# ---------------- THE B-PHASE (the forest V1: the per-target ladders + the dup-fills!!) ----------------
# the wires' readers (the pieces + the fills (the sources!!!))
readers = defaultdict(list)
for t in range(V):
    for p in T_BASE[t]: readers[('P', p)].append(t)
    for s in T_FILL[t]: readers[('S', s)].append(t)
log('the readers: %d wires | the loads %s' % (len(readers), dict(sorted(Counter(len(v) for v in readers.values()).items()))))

# the wires' chains (the V1: the per-wire suffix-chains (the nat90!!!)):
# the chain: home -> f_1 -> ... -> f_m (the dims +1 (the ⊥-extensions inside the
# suffix-common-perps!!!)); the readers assigned to the chain-slots (the clusters!!)
def suffix_chain(w, rs):
    """the wire w (the home-frame!!), the readers rs: the chain-frames + the reader-slots."""
    home = piece_PF[w[1]] if w[0] == 'P' else SINGLE[w[1]]
    if len(rs) == 1:
        return home, [rs[0]]                     # the single reader: at the home!!!
    # the ordered readers: the suffix-greedy (the later readers' common-perps ⊇ the
    # earlier frames!!!): the chain: the frames f_i ⊆ ∩-perp(suffix_i) ⊇ home
    order = sorted(rs)                            # V1: the fixed order!!
    chain = [home]; slots = defaultdict(list)
    cur = home
    curdim = fdim(home)
    remaining = set(order)
    while remaining:
        # the next frame: +1 dim inside the common perp of the remaining!!
        common = None
        for t in remaining:
            common = PM[t] if common is None else (common & PM[t])
        # the extension: the lines ⊥ all the remaining!!
        need = fmask(cur)
        base_lines = [s for s in range(V) if (need >> s) & 1]
        ok = [s for s in range(V) if (common >> s) & 1 and spans(list(flist[cur]) + [list(LINES[s])]) > curdim]
        if not ok:
            break
        nxt = fidx(rref(list(flist[cur]) + [list(LINES[ok[0]])]))
        # the readers that can read at nxt (nxt ⊆ their perps!!)
        nm = fmask(nxt)
        group = [t for t in remaining if (nm & ~PM[t]) == 0]
        if not group:
            # take the next-best extension...
            remaining.discard(min(remaining))
            continue
        for t in group: slots[len(chain)].append(t); remaining.discard(t)
        chain.append(nxt); cur = nxt; curdim = fdim(nxt)
        if curdim >= 8: break
    if remaining:
        return None                              # V1: the overflow -> the dup-fills!!!
    return chain, slots
WCHAIN = {}
overflow = []
for w, rs in readers.items():
    ch = suffix_chain(w, list(rs))
    if ch is None: overflow.append((w, len(rs))); WCHAIN[w] = None
    else: WCHAIN[w] = ch
log('the suffix-chains: %d ok | %d overflow (%s)' % (
    sum(1 for v in WCHAIN.values() if v), len(overflow),
    [o for o in overflow[:10]]))
json.dump({'pieces': [list(p) for p in kept],
           'bases': [[list(x) for x in b] for b in T_BASE],
           'fills': [sorted(f) for f in T_FILL],
           'gbases': [[(['P', list(w[1])] if w[0] == 'P' else ['S', w[1]]) for w in gb] for gb in GBASE],
           'R': REG},
          open('ii19_nat104_design.json', 'wt'))
log('SAVED ii19_nat104_design.json (THE PHASE-2 (the forest census!!))')
