"""THE COORDINATED SPARSE XOR-SOLVE (ii19_nat93.py) — the aggregate-word's true basis!!

THE nat92's VERDICT: the myopic XOR-greedy over (16 aggregates + pieces + carriers)
strands the residuals (27-40 wires/target (the pieces 1,676!! the carriers 2,152!!!)) —
the dup-explosion kills it (the R-ceiling 480!!!). THE TRUE SOLVE: the rich-frame pool
ITSELF (9,661 candidates; each target has 400-1,200 of them ⊥!!): perp(t) = the XOR of
~6-9 BIG SHARED wires (the coordinated solve (the minimal POOL (the R!!) + the minimal
per-target reads (the chain-load!!))). THE PIPELINE:
(1) THE GLOBAL GREEDY (the XOR-reduction measure!!): the pool driving all 129 residuals
    (the 9 patterns + the 120 perps!!) down together;
(2) THE EXACT SPAN-FINISH: per demand: the residual's exact GF(2) combination from the
    candidates (NO carriers unless truly stuck!!);
(3) THE CENSUS: the pool-size (the R!!), the per-target reads, the wire-reader loads
    (the chain/overflow!!), the sub-piece build-budget (the R!!) -> THE PRICE at the
    landed R!!! -> THE EMISSION-GO.
"""
import os, sys, json
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
pool3 = [(sorted(p), sorted(u)) for p, u in P70['pool']]

# the rich-4 pool (nat91's exact!!)
def rspan(vecs): return len(rref([list(v) for v in vecs], 8))
rich = {}
seen = set()
for ps, users in pool3:
    for s4 in range(V):
        if s4 in ps: continue
        key = tuple(sorted(ps + [s4]))
        if key in seen: continue
        seen.add(key)
        if rspan([lines[x] for x in key]) != 4: continue
        basis = rref([list(lines[x]) for x in key], 8)
        inF = [x for x in range(V) if len(rref(list(basis) + [list(lines[x])], 8)) == 4]
        if len(inF) >= 5:
            rich[key] = (frozenset(inF), frozenset(t for t in range(V) if all(G8[k][t] == 0 for k in key)))
log('the rich-4 pool: %d' % len(rich))

# the demands: 9 patterns + 120 perps (as bitmasks!!)
BASIS_IDX = SPEC['BASIS_IDX']
pats = []
for c, o in BASIS_IDX:
    v = 0
    for t in o: v ^= B0[t]
    pats.append(v)
demands = list(pats) + [sum(1 << s for s in PERP[t]) for t in range(V)]
ND = len(demands)

# the candidates as bitmasks + the per-demand candidate lists
cand_keys = list(rich.keys())
cand_mask = {k: sum(1 << s for s in rich[k][0]) for k in cand_keys}
per_demand_cands = []
for d in demands:
    cs = [k for k in cand_keys if (cand_mask[k] & ~d) == 0]   # the wire ⊆ the demand!!!
    per_demand_cands.append(cs)
log('the per-demand candidate counts: %s' % dict(sorted(Counter(len(c) for c in per_demand_cands).items())))

# (1) THE GLOBAL GREEDY: drive all residuals down together (the XOR-reduction!!)
res = list(demands)
chosen = []
for rounds in range(200):
    total = sum(bin(r).count('1') for r in res)
    if total == 0: break
    best_k, best_red = None, 0
    for k in cand_keys:
        m = cand_mask[k]
        red = 0
        for i in range(ND):
            if res[i] == 0: continue
            r = res[i]
            red += bin(r).count('1') - bin(r ^ m).count('1')
        if red > best_red: best_k, best_red = k, red
    if best_k is None or best_red <= 0: break
    chosen.append(best_k)
    m = cand_mask[best_k]
    for i in range(ND): res[i] ^= m
    if rounds % 10 == 0:
        log('  round %d: chosen %d | the residual mass %d' % (rounds, len(chosen), sum(bin(r).count('1') for r in res)))
log('THE GLOBAL GREEDY: %d wires | the residual mass %d' % (len(chosen), sum(bin(r).count('1') for r in res)))
log('  the residual sizes: %s' % dict(sorted(Counter(bin(r).count('1') for r in res).items())))

# (2) THE EXACT SPAN-FINISH per demand (the residual via the candidates (the span-solve!!))
log('\n(2) THE EXACT SPAN-FINISH:')
extra = set()
solved = []
for i in range(ND):
    r = res[i]
    if r == 0:
        solved.append([]); continue
    cs = per_demand_cands[i]
    # the greedy exact-solve on the small residual: pick candidates reducing it, then
    # the exact finish via the single-LINE carriers only if the span fails
    combo = []
    cur = r
    # reduce greedily first
    while True:
        best_k, best_red = None, 0
        for k in cs:
            red = bin(cur).count('1') - bin(cur ^ cand_mask[k]).count('1')
            if red > best_red: best_k, best_red = k, red
        if best_k is None or best_red <= 0: break
        combo.append(best_k); cur ^= cand_mask[best_k]
    # the exact finish: the span-solve over the candidates (GF(2) on the residual space)
    if cur != 0:
        # try the linear span: solve cur = XOR of candidates (the rref over GF(2)!!))
        vecs = [(k, cand_mask[k]) for k in cs]
        piv = {}
        rows = []
        for k, m in vecs:
            w = m
            for p, pv in sorted(piv.items(), reverse=True):
                if (w >> p) & 1: w ^= pv[1]
            if w:
                pb = w.bit_length() - 1
                piv[pb] = (k, w)
                rows.append((k, w))
        # reduce cur
        target = cur
        used = []
        for p in sorted(piv, reverse=True):
            if (target >> p) & 1:
                k, w = piv[p]
                target ^= w
                used.append(k)
        if target == 0:
            combo += used
            extra.update(used)
        else:
            # the carriers as the last resort (the single lines!!)
            combo += [('C', s) for s in bits(cur)]
    solved.append(combo)
fin_c = Counter()
for combo in solved:
    for c in combo:
        fin_c['C' if isinstance(c, tuple) else 'W'] += 1
log('    the finish: the wire-uses %d | the carrier-uses %d' % (fin_c['W'], fin_c['C']))
# the wire-usage census
use = Counter()
per_t = []
for i, combo in enumerate(solved):
    ws = [c for c in combo if not isinstance(c, tuple)]
    per_t.append(ws)
    for k in ws: use[k] += 1
log('    the per-demand wire-counts: %s' % dict(sorted(Counter(len(w) for w in per_t).items())))
allw = set(k for w in per_t for k in w) | set(chosen)
log('    THE POOL: %d distinct wires (the greedy %d + the finish %d)'
    % (len(allw), len(chosen), len(allw) - len(set(chosen))))
log('    the wire-reader loads: %s' % dict(sorted(Counter(use.values()).items())))

# (3) THE R-CENSUS + THE PRICE
log('\n(3) THE R-CENSUS:')
sub_pieces = sum(len(rich[k][0]) // 5 + 1 for k in allw)   # ~5-line sub-pieces per wire!!
R_est = len(allw) + sub_pieces + 9
log('    the wires %d + the sub-pieces ~%d + the gathers 9 = R ~ %d' % (len(allw), sub_pieces, R_est))
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (R_est, R_est + 50, R_est + 100):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else 'NO-ROOT'))
json.dump({'wires': [list(k) for k in allw],
           'per_demand': [[list(k) if not isinstance(k, tuple) else list(k) for k in combo] for combo in solved]},
          open('ii19_nat93_design.json', 'wt'))
log('SAVED ii19_nat93_design.json')
