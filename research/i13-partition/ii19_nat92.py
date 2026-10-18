"""THE AGGREGATE-WORD'S DESIGN-SOLVE (ii19_nat92.py) — the XOR-basis + the chains + the R!!

THE nat91's BREAKTHROUGH: 9,661 dim-4 rich frames (7-12 lines (the spans dim 4!!) with
6-12 perpendicular targets (T(G)!!!)); the 9 patterns = 8-11 aggregates each (zero
singles!!); ALL 120 perps fully covered; a 16-aggregate global cover (zero residual!!).
THE REMAINING DESIGN-UNKNOWN (this script!!):
(1) THE PER-TARGET XOR-SOLVE: the B-reads must XOR to EXACTLY perp(t) (the union-cover
    ≠ the XOR-cover!!!): the wires: the aggregates (the big chunks (7-12 lines!!)) +
    the pool pieces (3-line!!) + the single-line carriers (the parity-fixes!!) — the
    greedy solve + the census (the read-counts!!);
(2) THE CHAIN-CAPACITY: per wire: the home-reads (free (no climb!!)) vs the chain-reads
    (ONE nested path (the suffix-structure!!)) — the dup-estimate (the R!!);
(3) THE LOW-R PRICE MAP (the sanity range (the artifacts!!)): the R-target's landing.
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
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]

# rebuild the rich-4 pool (nat91's exact!!)
def rank_span(vecs):
    return len(rref([list(v) for v in vecs], 8))
rich4 = {}
seen = set()
for ps, users in pool:
    for s4 in range(V):
        if s4 in ps: continue
        key = tuple(sorted(ps + [s4]))
        if key in seen: continue
        seen.add(key)
        if rank_span([lines[x] for x in key]) != 4: continue
        basis = rref([list(lines[x]) for x in key], 8)
        inF = [x for x in range(V) if len(rref(list(basis) + [list(lines[x])], 8)) == 4]
        if len(inF) >= 5:
            rich4[key] = (tuple(inF), tuple(t for t in range(V) if all(G8[k][t] == 0 for k in key)))
log('the rich-4 pool: %d' % len(rich4))

# THE GLOBAL GREEDY (nat91's exact!!) -> the 16 aggregates
BASIS_IDX = SPEC['BASIS_IDX']
pats = []
for c, o in BASIS_IDX:
    v = 0
    for t in o: v ^= B0[t]
    pats.append(set(bits(v)))
demands = [set(p) for p in pats] + [set(PERP[t]) for t in range(V)]
chosen = []
remaining = [set(d) for d in demands]
total_left = sum(len(r) for r in remaining)
while total_left > 0:
    best_key, best_gain = None, 0
    for key, (inF, T) in rich4.items():
        gain = sum(len(set(inF) & r) for r in remaining)
        if gain > best_gain: best_key, best_gain = key, gain
    if best_key is None or best_gain == 0: break
    chosen.append(best_key)
    for r in remaining: r ^= (set(rich4[best_key][0]) & r)
    total_left = sum(len(r) for r in remaining)
log('the chosen aggregates: %d' % len(chosen))

# (1) THE PER-TARGET XOR-SOLVE: wires = aggregates (chosen) + pieces + single-carriers
log('\n(1) THE PER-TARGET XOR-SOLVE (the exact-parity B-basis!!):')
AGG = []
for key in chosen:
    inF, T = rich4[key]
    AGG.append((set(inF), set(T)))
PIE = [(set(p), set(u)) for p, u in pool]
def solve_target(t):
    """greedy XOR-solve: pick wires reducing the |residual| most (GF(2) XOR!!)."""
    res = set(PERP[t])
    wires = []
    cand = [('A', i) for i, (inF, T) in enumerate(AGG) if t in T] + \
           [('P', i) for i, (ps, users) in enumerate(PIE) if t in users] + \
           [('C', s) for s in PERP[t]]
    used = set()
    while res:
        best, best_red = None, 0
        for kind, i in cand:
            if (kind, i) in used: continue
            if kind == 'A': w = AGG[i][0]
            elif kind == 'P': w = PIE[i][0]
            else: w = {i}
            red = len(w & res) - len(w - res)
            if red > best_red: best, best_red = (kind, i), red
        if best is None: return None
        kind, i = best
        w = AGG[i][0] if kind == 'A' else (PIE[i][0] if kind == 'P' else {i})
        res ^= w
        used.add(best); wires.append(best)
    return wires
sols = [solve_target(t) for t in range(V)]
assert all(s is not None for s in sols), 'the XOR-solve failed!!'
census = Counter()
for t, sol in enumerate(sols):
    c = Counter(kind for kind, _ in sol)
    census[(c['A'], c['P'], c['C'])] += 1
log('    the (A, P, C)-census: %s' % dict(sorted(census.items())))
tot = Counter()
for sol in sols:
    for kind, _ in sol: tot[kind] += 1
log('    the totals: aggregates %d | pieces %d | carriers %d'
    % (tot['A'], tot['P'], tot['C']))
read_c = Counter(len(s) for s in sols)
log('    the per-target read-counts: %s' % dict(sorted(read_c.items())))

# (2) THE CHAIN-CAPACITY CENSUS: per wire: the readers vs the home/chain split
log('\n(2) THE CHAIN-CAPACITY (the home-reads vs the chain-reads!!):')
wire_readers = defaultdict(list)
for t, sol in enumerate(sols):
    for kind, i in sol: wire_readers[(kind, i)].append(t)
# the home-frame reads: the FIRST read of each target (at the wire's home!!);
# the chain-reads: the target's later reads at ITS rungs (the wire's nested chain!!)
home_c = Counter()
chain_demand = Counter()
for (kind, i), readers in wire_readers.items():
    home_c[len(readers)] += 1
    chain_demand[len(readers) - 1] += 1   # ~the first-reader free + the rest on the chain
log('    the wire-reader counts: %s' % dict(sorted(home_c.items())))
log('    the chain-demand (the readers-1): %s (the chain-capacity ~4-5!!!)' %
    dict(sorted(chain_demand.items())))
overflow = sum(max(0, n - 1 - 4) for n in wire_readers.values())
log('    the naive overflow (the readers-1 > 4): ~%d dup-fills' % overflow)

# (3) THE LOW-R PRICE MAP (the sanity range!!)
log('\n(3) THE LOW-R PRICE MAP (cst=72!!):')
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (25, 40, 60, 80, 100, 120, 140, 160, 200):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else 'NO-ROOT'))

json.dump({'chosen': [list(k) for k in chosen],
           'sols': [[list(w) for w in s] for s in sols]},
          open('ii19_nat92_design.json', 'wt'))
log('SAVED ii19_nat92_design.json (the aggregate-word\'s design!!)')
