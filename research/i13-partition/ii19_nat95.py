"""THE FULL-POOL MIXED SOLVE (ii19_nat95.py) — the B-basis design (the emission-go!!)

THE VERDICTS SO FAR: the 147-pool pieces span perp(t) for 0/120 (too few candidates!!);
the rich-4 greedy stuck (17 wires); THE FIX: THE FULL POOL — every 3-line subset of
perp(t) is a legal piece (~40,000 candidates/target; the disjoint 21-triple partitions
trivially span!!!) + the rich-4 chunks (nat94's cache (the span verdict pending!!)).
THE PIPELINE:
(1) THE PER-TARGET EXACT BASES: the greedy + the exact finish over the candidates
    (the rich-4s (the big chunks (the shared wires!!)) + the ⊥-triples (the fixes!!));
(2) THE POOL-MERGE: the local search (re-solve each target PREFERRING the current pool
    (the sharing-maximization (the R!!)));
(3) THE CENSUS: the pool (the R!!), the per-target reads, the piece-reader loads (the
    chain-capacity!!), the R-budget vs the 480 hosting ceiling -> THE PRICE -> GO!!
"""
import os, sys, json
import numpy as np
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
PERP = [set(p) for p in SPEC['PERP']]
B0 = [sum(1 << s for s in ({t} | PERP[t])) for t in range(V)]
G8 = [[sum(a[i] * b[i] for i in range(8)) for b in lines] for a in lines]

# the rich-4 cache (nat94's!!) — the span verdict rides on it!!
RICH_OK = os.path.exists('ii19_nat94_richpool.npz')
rich_masks = rich_T = None
rich_keys = []
if RICH_OK:
    z = np.load('ii19_nat94_richpool.npz')
    rich_masks = z['masks']; rich_T = z['Tmat']
    rich_keys = [tuple(int(x) for x in k) for k in z['keys']]
    log('the rich-4 cache: %d frames' % len(rich_keys))
else:
    log('!! the rich-4 cache absent — the piece-only route!!')

# the triples: per target: the ⊥-triples = all 3-subsets of PERP[t] (the span ⊇ perp(t)!!) —
# TOO MANY to enumerate raw (C(63,3) ~ 40k x 120!!) — THE DESIGN: the per-target basis via
# the STRUCTURED candidates: the perp(t)-partition triples (21 disjoint!!) + the pool-pieces
# (nat70) + the rich-4s. THE PARTITION-PIECES: the fresh triples chosen for the SHARING!!
log('\n(1) THE PER-TARGET BASES (the structured candidates!!):')
pool = json.load(open('ii19_nat70_pool.json', 'rt'))['pool']
pool = [(sorted(p), sorted(u)) for p, u in pool]
# the candidate generator per target: (a) the nat70 pieces with t in users; (b) the rich-4s
# with t in T(G); (c) the FRESH TRIPLES: built greedily ON DEMAND (the biggest-reduction
# triples over the residual!!) — the triple {a,b,c} ⊆ residual with the maximal coverage
def fresh_triples(t, residual):
    """the best disjoint triples covering the residual (the partition-style!!)."""
    out = []
    rem = set(residual)
    while rem:
        # the best triple: the ⊥-structure — try the pairs first: {a,b} with many common
        # ⊥-targets (the sharing!!) then the third line completing ⊥-ness is automatic
        # (all in perp(t)!!) — ANY 3 lines of perp(t) form a legal piece for t!!!
        best, best_score = None, -1
        rem_l = sorted(rem)
        # sample-based search for speed: the pairs with the high co-perp counts
        for i in range(len(rem_l)):
            a = rem_l[i]
            for j in range(i + 1, len(rem_l)):
                b = rem_l[j]
                # the sharing score: |{u : u ⊥ a and u ⊥ b}| (the piece's future readers!!)
                sc = CoP[a][b]
                if sc > best_score:
                    best_score = sc
                    best = (a, b)
                if j > 40: break     # the speed cap
            if i > 40: break
        a, b = best
        c = next(x for x in rem_l if x not in (a, b))
        out.append((a, b, c))
        rem -= {a, b, c}
    return out

# the co-perp counts (the sharing score!!): CoP[a][b] = |{u : u ⊥ a, u ⊥ b}|
CoP = [[0] * V for _ in range(V)]
for a in range(V):
    for b in range(a + 1, V):
        c = len(PERP[a] & PERP[b])
        CoP[a][b] = CoP[b][a] = c

bases = []
used_pool = set()
fresh_census = Counter()
for t in range(V):
    res = set(PERP[t])
    base = []
    # (a) the pool-pieces (the free shared registers!!)
    for i, (ps, u) in enumerate(pool):
        if t in u:
            base.append(('P', i)); res ^= set(ps)
    # (b) the rich-4s (the big chunks!!)
    if RICH_OK:
        res_arr = np.array([1 if s in res else 0 for s in range(V)], dtype=np.uint8)
        sel = np.where(rich_T[:, t] > 0)[0]
        for k in sel:
            m = rich_masks[k]
            if (m & (1 - res_arr)).any():
                continue
            S = {s for s in range(V) if m[s]}
            if S & res and len(S & res) >= len(S - res):
                base.append(('R', int(k))); res ^= S
    # (c) the fresh triples (the partition of the residual!!)
    for tri in fresh_triples(t, res):
        base.append(('T', tri))
        fresh_census['triples'] += 1
    bases.append(base)
log('  the per-target bases: %s' % dict(sorted(Counter(
    (sum(1 for k, _ in b if k == 'P'), sum(1 for k, _ in b if k == 'T')) for b in bases).items())))
log('  the fresh-triple total: %d' % fresh_census['triples'])

# (2) THE POOL-MERGE: the fresh-triple sharing across targets (the SAME triple used by
# many targets (the ⊥-structure!!)) — the dedup census!!
log('\n(2) THE POOL-MERGE (the triple-sharing!!):')
triple_use = Counter()
for b in bases:
    for k, x in b:
        if k == 'T': triple_use[tuple(sorted(x))] += 1
log('  the distinct fresh triples: %d (the uses %d)' % (len(triple_use), sum(triple_use.values())))
log('  the triple-use census: %s' % dict(sorted(Counter(triple_use.values()).items())))
R_pool = len(pool) + (len(rich_keys) if RICH_OK else 0) + len(triple_use)
log('  THE POOL: %d (the pieces %d + the rich %d + the triples %d)'
    % (R_pool, len(pool), len(rich_keys) if RICH_OK else 0, len(triple_use)))

# (3) THE R-BUDGET + THE PRICE
log('\n(3) THE R-BUDGET (the ceiling 480!!!) + THE PRICE:')
R_est = R_pool + 9 + 80   # + the gathers + the gather-side dup estimate
log('  R ~ %d (the pool + 9 gathers + ~80 dups!!)' % R_est)
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (R_est, R_est + 50, R_est + 100, 480):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else str(dd.get('error', 'NO-ROOT'))))
json.dump({'bases': [[(k, list(x) if k == 'T' else x) for k, x in b] for b in bases]},
          open('ii19_nat95_design.json', 'wt'))
log('SAVED ii19_nat95_design.json')
