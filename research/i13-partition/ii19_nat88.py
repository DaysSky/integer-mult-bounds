"""THE CST=63 DESIGN CENSUS (ii19_nat88.py) — the gather-word's ground measurements!!

THE nat86/87's verdicts: F(0) < 0 ⟺ cst ≤ 106 (R-exactly-neutral!!); the route = the r434's
own grammar (the 9 gathers at dim-7 frames (cst = 63!!) + the W-scatter + the B-phase
perp-delivery + the free D-phase (the y-cancellation (the readers' self-bits — D-reads
at frame 0 (NO HIST!!)))). THE DESIGN'S GATES (this census):
(1) THE W-BASIS SPANS: the 9 gathers' patterns (BASM) must span ≤ dim 7 each (the dim-7
    ret-frames (cst = 63!!)) — the basis-RECHOICE search (the row-space's 512 elements!!);
(2) THE POOL COVERAGE: per target t: the pieces with t ∈ users (their lines ⊆ perp(t)!!),
    the covered-vs-perp(t), the leftovers (the carriers' loads!!);
(3) THE GATHER-BUILD WIRES: the patterns' lines ← the pieces (the 3-line content) — the
    gather-wire census + the dup-question (the frame-conflict (the pieces serve the
    targets at the perp-frames (B!!) and the gathers at the gather-frames (A!!)));
(4) THE R-ESTIMATE: pieces + gathers + carriers + dups.
"""
import os, sys, json, itertools
from collections import Counter, defaultdict
from fractions import Fraction
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

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
PERP = [set(p) for p in SPEC['PERP']]
B0 = [sum(1 << s for s in ({t} | PERP[t])) for t in range(V)]
def bits(x): return [s for s in range(V) if (x >> s) & 1]

# ---- (1) THE W-BASIS SPANS (the nat69 basis — and the rechoice search!!)
BASIS_IDX = SPEC['BASIS_IDX']
def span_dim(x):
    bs = [list(lines[s]) for s in bits(x)]
    return len(rref(bs, 8)) if bs else 0
log('(1) THE NAT69 BASIS (the gathers patterns (x-parts!!)):')
bad = 0
for k, (c, o) in enumerate(BASIS_IDX):
    val = 0
    for t in o: val ^= B0[t]
    d = span_dim(val); n = len(bits(val))
    log('  gather %d (pivot %3d, %2d rows): %3d lines | span dim %d %s'
        % (k, c, len(o), n, d, '' if d <= 7 else '(>7!! the FULL-frame case!!)'))
    if d > 7: bad += 1
log('  the dim>7 gathers: %d (the cst = %d if all-dim-7!!)' % (bad, sum(
    min(span_dim(0 if len(o) == 1 and False else (0 if False else 0)), 8) for _, _ in [(0, 0)] * 0) if bad else 63))

# the rechoice: the row-space (rank 9!!) — search for 9 independent patterns with span ≤ 7
# (and small-ish line-counts + the 512-element space's structure)
log('\n(1b) THE ROW-SPACE SEARCH (the dim<=7 basis-rechoice!!):')
# the row space: span of the B0 patterns (GF(2), rank 9 per the decoder!!)
import random
rng = random.Random(12345)
spans_cache = {}
def spdim(x):
    if x not in spans_cache: spans_cache[x] = span_dim(x)
    return spans_cache[x]
# generate the 512 elements via the basis (9 rows -> all XORs)
base_rows = []
for c, o in BASIS_IDX:
    acc = 0
    for t in o: acc ^= B0[t]
    base_rows.append(acc)
elems = set()
for mask in range(1 << 9):
    acc = 0
    for j in range(9):
        if (mask >> j) & 1: acc ^= base_rows[j]
    elems.add(acc)
log('  the row-space: %d elements (2^9 = 512?!)' % len(elems))
dims_c = Counter(spdim(e) for e in elems)
sizes_c = Counter(len(bits(e)) for e in elems)
log('  the spans: %s | the line-counts: %s' % (dict(sorted(dims_c.items())), dict(sorted(sizes_c.items()))))
ok7 = [e for e in elems if spdim(e) <= 7]
log('  the dim<=7 elements: %d' % len(ok7))
# the independent 9-subsets of the dim<=7 elements (small line-counts preferred!!)
cand = sorted(ok7, key=lambda e: (len(bits(e)), spdim(e)))
log('  the smallest dim<=7 elements: %s' % [(len(bits(e)), spdim(e)) for e in cand[:20]])
def indep(vs):
    rr = 0; M = list(vs)
    for c in range(V):
        p = next((i for i in range(rr, len(M)) if (M[i] >> c) & 1), None)
        if p is None: continue
        M[rr], M[p] = M[p], M[rr]
        for i in range(len(M)):
            if i != rr and ((M[i] >> c) & 1): M[i] ^= M[rr]
        rr += 1
    return rr
best = None
# greedy: take smallest, extend
sel = []
for e in cand:
    if len(sel) == 9: break
    if indep(sel + [e]) == len(sel) + 1: sel.append(e)
log('  the greedy dim<=7 basis: %d elements %s' % (len(sel), [(len(bits(e)), spdim(e)) for e in sel]))
if len(sel) == 9:
    log('  => CST=63 FEASIBLE (all 9 at dim<=7!!) — the rechoice basis exists!!')
    json.dump([e for e in sel], open('ii19_nat88_basis7.json', 'wt'))

# ---- (2) THE POOL COVERAGE
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]
log('\n(2) THE POOL COVERAGE (the B-delivery!!):')
cov = [set() for _ in range(V)]
for k, (ps, users) in enumerate(pool):
    for t in users: cov[t] |= set(ps)
left = [PERP[t] - cov[t] for t in range(V)]
log('  per-target covered: %s' % dict(sorted(Counter(len(cov[t]) for t in range(V)).items())))
log('  per-target LEFT: %s' % dict(sorted(Counter(len(left[t]) for t in range(V)).items())))
log('  the LEFTOVER lines (the carriers!!): total %d' % sum(len(l) for l in left))
log('  the pool pieces\' users: %s' % dict(sorted(Counter(len(u) for _, u in pool).items())))

# ---- (3) THE GATHER-WIRE CENSUS (the pattern-lines via the pool pieces)
log('\n(3) THE GATHER-WIRE CENSUS (the rechoice basis (the smallest!!)):')
if len(sel) == 9:
    line2pieces = defaultdict(list)
    for k, (ps, users) in enumerate(pool):
        for s in ps: line2pieces[s].append(k)
    tot_wires = 0
    for g, e in enumerate(sel):
        pat = set(bits(e))
        wires = []
        # greedy: cover the pattern with pool-pieces (a set-cover per gather!!)
        uncovered = set(pat)
        wc = Counter()
        while uncovered:
            best_k, best_n = None, 0
            for k, (ps, users) in enumerate(pool):
                n = len(set(ps) & uncovered)
                if n > best_n: best_k, best_n = k, n
            if best_k is None or best_n == 0: break
            wires.append(best_k); uncovered ^= (set(pool[best_k][0]) & uncovered)
        singles = len(uncovered)
        tot_wires += len(wires) + singles
        log('  gather %d: %3d lines | %2d pool-pieces + %2d singles (the dup-carriers!!)'
            % (g, len(pat), len(wires), singles))
    log('  the total gather-wires: %d (the R-estimate below!!)' % tot_wires)

# ---- (4) THE R-ESTIMATE
log('\n(4) THE R-ESTIMATE: pieces %d + gathers 9 + the dup-wires + the carriers/leftovers...'
    % len(pool))

# ---- (5) THE HONEST cst=72 PRICE-MAP (the ext120's gathers at FULL (the R420's own!!))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R, cst, tmpl):
    mass = 8 * R + cst + 2 * V * (h - 1)
    d = Counter(tmpl); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
h = 8
v = V
log('\n(5) THE cst=72 R-MAP (the ext120-honest class (the R420-grammar!!)):')
for R in (140, 160, 174, 190, 200, 230, 250, 274, 300):
    c, prof, d = price(synth(R, 72, TARGET), v, h, R)
    log('  R=%3d  root=%s' % (R, mp.nstr(c, 10) if c is not None else 'NO-ROOT'))
log('  (the cst=63 R-map (the punctured-class) for reference:)')
for R in (174, 200, 274):
    c, prof, d = price(synth(R, 63, TARGET), v, h, R)
    log('  R=%3d  root=%s' % (R, mp.nstr(c, 10) if c is not None else 'NO-ROOT'))

print(json.dumps({'basis7': [e for e in sel] if len(sel) == 9 else None,
                  'pool_pieces': len(pool),
                  'leftover_total': sum(len(l) for l in left)}, indent=1))
