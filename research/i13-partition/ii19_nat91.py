"""THE AGGREGATE-POOL CENSUS (ii19_nat91.py) — the deep-DAG's ground measurement!!

THE nat90's law: the target's read-chain = ~4-5 rung-slots (dims 3->7!!!) with the
multi-src gates; the wires read above their home-frames have ONE nested user-chain —
the off-chain users cost DUP-COPIES (THE R-DRIVER!!). THE R-LEVER = THE DEEP-DAG (the
r434's own: its 9 gathers read ~4 wires each (the shared aggregates!!!)). THE CENSUS:
(1) THE LINE-RICH FRAMES: the dim-4..6 subspaces containing MANY of the 120 lines
    (the aggregate-candidates: contents = the line-sets (the spans small (the frames
    cheap!!) + the T(G) = the perpendicular targets LARGE (the user-groups!!)));
(2) THE GATHER-COVERAGE: the 9 patterns (the nat69 basis!!) covered by the dim-4-5
    aggregates (the wires-per-gather (the r434's 4?!?));
(3) THE B-SIDE COVERAGE: perp(t) via the aggregates + the pieces (the per-target
    read-counts (the ~4-5 slots!!!));
(4) THE R-ESTIMATE (the honest register count) + the price it lands at.
"""
import os, sys, json, itertools
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
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
G8 = [[sum(a[i] * b[i] for i in range(8)) for b in lines] for a in lines]
def ip_lines(i, j): return G8[i][j]

# (1) THE LINE-RICH FRAMES: the dim-d subspaces spanned by d lines, containing > d lines
log('(1) THE LINE-RICH FRAMES (the aggregate-candidates!!):')
# a frame F (a subspace): its line-set L(F) = {s : lines[s] ∈ F}. Build from spans of
# line-sets: start from the pieces' PFs (dim 3) and EXTEND: the dim-4 candidates:
# span(PF + 1 line) etc. THE CENSUS: the dim-4 subspaces = spans of 4-line subsets with
# >= 5 lines inside (the "rich" ones!!) — enumerate via the pieces + their co-lines.
# cheap enumeration: for each 3-line piece (the pool!!) + each 4th line ⊥-compatible:
rich4 = {}
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]
seen = set()
for ps, users in pool:
    for s4 in range(V):
        if s4 in ps: continue
        key = tuple(sorted(ps + [s4]))
        if key in seen: continue
        seen.add(key)
        # the span of the 4 lines: dim?
        d = len(rref([list(lines[x]) for x in key], 8))
        if d != 4: continue
        # the lines inside span(key): L(F)
        basis = rref([list(lines[x]) for x in key], 8)
        inF = [x for x in range(V) if len(rref(list(basis) + [list(lines[x])], 8)) == 4]
        if len(inF) >= 5:
            rich4[key] = inF
log('    the dim-4 rich frames: %d (from %d probes)' % (len(rich4), len(seen)))
sz = Counter(len(v) for v in rich4.values())
log('    the line-counts inside: %s' % dict(sorted(sz.items())))
# the T(G) census (the perpendicular targets!!): for each rich frame: T = {t : G ⊆ perp(t)}
tsize = Counter()
richT = {}
for key, inF in rich4.items():
    # G = span(key): T(G) = {t : all of G's basis ⊥ t} = {t : the 4 key-lines ⊥ t}
    T = [t for t in range(V) if all(ip_lines(k, t) == 0 for k in key)]
    richT[key] = (inF, T)
    tsize[len(T)] += 1
log('    the T(G) sizes (the perpendicular targets): %s' % dict(sorted(tsize.items())))

# (2) THE GATHER-COVERAGE: the 9 patterns vs the dim-4 aggregates
log('\n(2) THE GATHER-COVERAGE (the nat69 basis patterns via the aggregates!!):')
BASIS_IDX = SPEC['BASIS_IDX']
pats = []
for c, o in BASIS_IDX:
    v = 0
    for t in o: v ^= B0[t]
    pats.append(set(bits(v)))
# the greedy set-cover per pattern with the rich-4 frames (their line-sets!!)
wire_hist = Counter()
for g, pat in enumerate(pats):
    unc = set(pat)
    wires = []
    while unc:
        best_key, best_n = None, 0
        for key, (inF, T) in richT.items():
            n = len(set(inF) & unc)
            if n > best_n: best_key, best_n = key, n
        if best_key is None or best_n == 0: break
        wires.append(best_key); unc ^= (set(richT[best_key][0]) & unc)
    wire_hist[len(wires)] += 1
    if g < 4:
        log('    gather %d (%d lines): %d dim-4 wires + %d singles'
            % (g, len(pat), len(wires), len(unc)))
log('    the wire-counts per gather (dim-4 aggregates): %s' % dict(sorted(wire_hist.items())))

# (3) THE B-SIDE: perp(t) via the aggregates (the shared big reads!!)
log('\n(3) THE B-SIDE COVERAGE (perp(t) via the rich frames!!):')
cov = defaultdict(set)
for key, (inF, T) in richT.items():
    for t in T: cov[t] |= set(inF)
log('    the per-target aggregate-coverage: %s' %
    dict(sorted(Counter(len(cov[t] & PERP[t]) for t in range(V)).items())))
# the T(G)-side: how many rich frames serve each target
serv = Counter()
for key, (inF, T) in richT.items():
    for t in T: serv[t] += 1
log('    the per-target serving-frames: %s' % dict(sorted(serv.values().__class__ and Counter(serv.values()).items())))

# (4) THE R-ESTIMATE
log('\n(4) THE R-ESTIMATE + THE PRICE:')
# registers: the aggregates actually used (a covering subfamily!!) + pieces + gathers + carriers
# the greedy cover over ALL demands (the 9 gathers + the 120 targets' perps!!):
def greedy_cover(demands):
    """demands: list of sets; return the chosen rich-frames (keys) covering most mass."""
    chosen = []
    remaining = [set(d) for d in demands]
    total_left = sum(len(r) for r in remaining)
    while total_left > 0:
        best_key, best_gain = None, 0
        for key, (inF, T) in richT.items():
            gain = sum(len(set(inF) & r) for r in remaining)
            if gain > best_gain: best_key, best_gain = key, gain
        if best_key is None or best_gain == 0: break
        chosen.append(best_key)
        for r in remaining: r ^= (set(richT[best_key][0]) & r)
        total_left = sum(len(r) for r in remaining)
    return chosen, total_left
demands = [set(p) for p in pats] + [set(PERP[t]) for t in range(V)]
chosen, left = greedy_cover(demands)
log('    the global greedy: %d aggregates chosen | the uncovered mass %d' % (len(chosen), left))
R_est = len(chosen) + 9  # aggregates + gathers (+ the pieces/carriers for the leftovers!)
for R in (160, 180, 200, 230, 260):
    pass
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (170, 190, 210, 240):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else 'NO-ROOT'))
print(json.dumps({'rich4': len(rich4), 'chosen': len(chosen), 'uncovered': left}, indent=1))
