"""THE EMITTER (ii19_nat99.py) — THE SURGERY ON THE LADDER2 SKELETON!!!

THE WORD: the pool-wires (the B-basis (nat98!!)) + the 9-gather W-scatter (cst=72!!)
+ the perp-delivery B-phase (the forest (the wires' suffix-chains + the targets'
rung-ladders + the dup-fills)) + the D (the y-parity (mechanical!!)) + the C.
THE TARGET: gcheck PASS -> THE PRICED ROOT (the verified c!!!).
"""
import os, sys, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# ---------- the spec + the design ----------
SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
LINES = [tuple(int(x) for x in l) for l in SPEC['lines']]
W_SC = [list(map(int, w)) for w in SPEC['W']]                # the scatter (VERIFIED!!)
PERP = [set(p) for p in SPEC['PERP']]
DES = json.load(open('ii19_nat98_design.json', 'rt'))
POOL = [tuple(p) for p in DES['pool']]                        # the wire line-sets
BASES = [[tuple(w) for w in b] for b in DES['bases']]         # the per-target bases
log('the design: the pool %d | the bases %d' % (len(POOL), len(BASES)))

# ---------- the frames ----------
# frame: the rref basis (the list of 8-tuples (the exact Gram (the nondegenerate!!!)))
from fractions import Fraction
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
def rrank(M):
    return spans(M)
def span_of(idx):
    return rref([list(LINES[i]) for i in idx])

frames = {}          # the tuple-of-tuples -> the index
flist = []            # the index -> the basis
def fidx(basis):
    key = tuple(tuple(r) for r in basis)
    if key not in frames:
        frames[key] = len(flist); flist.append(key)
    return frames[key]
EMPTY = fidx([]); FULL = fidx(rref([list(x) for x in LINES]))
SINGLE = [fidx(span_of([s])) for s in range(V)]
TPERP = [fidx(span_of(sorted(PERP[t]))) for t in range(V)]
log('the base frames: %d (FULL=%d EMPTY=%d)' % (len(flist), FULL, EMPTY))

# the span-mask helper: which lines lie in the frame-span
_sp = {}
def span_mask(bi):
    if bi in _sp: return _sp[bi]
    B = flist[bi]
    m = 0
    for s in range(V):
        if spans(list(B) + [list(LINES[s])]) == len(B):
            m |= (1 << s)
    _sp[bi] = m
    return m

# ---------- the registers ----------
NS, NT = V, V                       # sources, targets
REG = 2 * V                          # the next free register index
wire_reg = {}                        # the wire-key -> the register
def newreg():
    global REG
    REG += 1
    return REG - 1

# the wires' homes (their content-spans!!)
wire_home = {}
for w in POOL:
    wire_home[w] = fidx(span_of(sorted(w)))
    wire_reg[w] = newreg()

# ---------- the A-phase: the wires' builds (the 1-src ladders!!!) ----------
A = []
def climb_frames(start_idx, target_idx):
    """the nested chain from start to target (the growing spans (the exact ⊆!!!))"""
    if start_idx == target_idx: return []
    # the line-sets: the target's span ⊇ the start's: the chain via the growing spans
    sm = span_mask(start_idx); tm = span_mask(target_idx)
    assert sm & ~tm == 0, 'the climb %d->%d not nested!' % (start_idx, target_idx)
    # the target basis lines: add them one at a time (the spans grow!!)
    chain = []
    cur = start_idx
    B = list(flist[target_idx])
    for row in B:
        cand = fidx(rref(list(flist[cur]) + [list(row)]))
        if cand != cur:
            chain.append(cand); cur = cand
    assert cur == target_idx, 'the chain failed %d -> %d (got %d)' % (start_idx, target_idx, cur)
    return chain

for w in POOL:
    q = wire_reg[w]
    acc = [w[0]]
    cur = SINGLE[w[0]]
    for x in w[1:]:
        nxt = fidx(span_of(sorted(acc + [x])))
        A.append([cur, q, [x]])
        cur = nxt
        acc = acc + [x]
    # cur == wire_home ✓ (the span of the full wire!!)
    assert cur == wire_home[w], 'the wire build frame mismatch!'
log('the wire builds: %d gates (1-src ladders!!)' % len(A))

# ---------- the gather-side: the patterns' bases + the dup-wires ----------
B0 = [sum(1 << s for s in ({t} | PERP[t])) for t in range(V)]
BASIS_IDX = [(int(c), [int(x) for x in o]) for c, o in SPEC['BASIS_IDX']]
gather_pat = []
for c, o in BASIS_IDX:
    v = 0
    for t in o: v ^= B0[t]
    gather_pat.append(v)
# the gathers' bases: the exact solve over the pool + the fresh (the greedy!!)
pm = lambda w: sum(1 << s for s in w)
def solve_pattern(pat):
    res = pat
    base = []
    poolm = {w: pm(w) for w in POOL}
    while res:
        best_w, best_red = None, 0
        for w in POOL:
            m = poolm[w] & res
            red = bin(m).count('1') - (bin(poolm[w] & ~res).count('1'))
            if red > best_red: best_red = red; best_w = w
        if best_w is not None:
            base.append(best_w); res ^= poolm[best_w]; continue
        # the fresh triple (the max-fit!!)
        rl = [s for s in range(V) if (res >> s) & 1]
        if len(rl) <= 3:
            base.append(tuple(rl)); break
        a, b, c = rl[0], rl[1], rl[2]
        base.append((a, b, c)); res ^= pm((a, b, c))
    return base
gather_bases = [solve_pattern(p) for p in gather_pat]
for g, p in enumerate(gather_pat):
    x = 0
    for w in gather_bases[g]: x ^= pm(w)
    assert x == p, 'the gather %d solve FAILED!!' % g
log('the gather bases: %s' % [len(b) for b in gather_bases])
# the dups: per (triple in a gather base) — shared across gathers (the coordinated chains!!)
gather_wires = sorted({w for b in gather_bases for w in b})
dup_reg = {}; dup_home = {}
for w in gather_wires:
    dup_reg[w] = newreg(); dup_home[w] = wire_home.get(w, fidx(span_of(sorted(w))))
    if w not in wire_home:
        # the fresh gather-wire: build it!!
        q = dup_reg[w]
        acc = [w[0]]; cur = SINGLE[w[0]]
        for x in w[1:]:
            nxt = fidx(span_of(sorted(acc + [x])))
            A.append([cur, q, [x]]); cur = nxt; acc = acc + [x]
        assert cur == dup_home[w]
# the dup builds: the copies at the wires' homes!!
for w in gather_wires:
    A.append([dup_home[w], dup_reg[w], [wire_reg.get(w, dup_reg[w])]] if w in wire_reg
             else [dup_home[w], dup_reg[w], [dup_reg[w]]])
log('the gather-side: %d dups (the shared wires!!)' % len(gather_wires))
json.dump({'todo': 1}, open('ii19_nat99_progress.json', 'wt'))
log('THE SKELETON SAVED (the frames %d | the A %d | the regs %d)' % (len(flist), len(A), REG))
