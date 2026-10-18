"""THE ITERATED POOL-SOLVE (ii19_nat97b.py) — the shared-triple pool to the fixpoint!!

THE nat97's STATE: the pool 369 (the pass-1!!) but the reads 26-41 (the red>=1 bloat!!)
+ THE LOCAL-SEARCH DESYNC (the -1/0 counts!!) -> the pool 400 | R 539 > the 480 CEILING.
THE FIXES (this script!!):
(1) THE GREEDY: red >= 2 ONLY (the 3-in-1-out fits (the reads ~21-25 (the partition-
    leaning!!)));
(2) THE ROLLBACK: the eliminated-triple double-count FIXED;
(3) THE GLOBAL ITERATE: the FULL re-solve passes (the whole pool re-solved per pass
    (the fixpoint!!)) — the later passes reuse the pool hard!!
(4) THE CENSUS + THE R + THE PRICE -> THE EMISSION-GO!!!
"""
import os, sys, json
from collections import Counter
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
PERP = [set(p) for p in SPEC['PERP']]
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
pc = lambda x: x.bit_count()

def fresh_wire(res):
    """the max-reader new wire fitting the residual (3/2/1-line as needed!!)."""
    rl = sorted(res)
    if len(rl) <= 3:
        tri = 0
        for x in rl: tri |= (1 << x)
        return tri
    best_tri, best_sc = None, -1
    for i in range(len(rl)):
        a = rl[i]; pa = PM[a]
        for j in range(i + 1, min(len(rl), i + 25)):
            b = rl[j]
            ab = pa & PM[b]
            for c in rl:
                if c in (a, b): continue
                sc = pc(ab & PM[c])
                if sc > best_sc: best_sc = sc; best_tri = (1 << a) | (1 << b) | (1 << c)
            if best_sc >= 20: break
        if best_tri is not None and best_sc >= 20: break
    if best_tri is None:
        a, b, c = rl[0], rl[1], rl[2]
        best_tri = (1 << a) | (1 << b) | (1 << c)
    return best_tri

def solve_target(t, pool):
    """the basis over the pool (red >= 2!!) + the fresh finish; returns the wire list."""
    res = set(PERP[t])
    base = []
    while res:
        resm = sum(1 << s for s in res)
        best_tri, best_score = None, 1
        for tri in pool:
            m = pc(tri & resm)
            red = m - (pc(tri) - m)
            if red > best_score: best_score = red; best_tri = tri
        if best_tri is not None:
            base.append(best_tri)
            res ^= {s for s in range(V) if (best_tri >> s) & 1}
            continue
        tri = fresh_wire(res)
        base.append(tri)
        res ^= {s for s in range(V) if (tri >> s) & 1}
    return base

# (1) THE TARGET-ORDER (the perp-adjacent chain!!)
order = []
remaining = set(range(V)); cur = 0
order.append(cur); remaining.discard(cur)
while remaining:
    nxt = max(remaining, key=lambda t: pc(PM[cur] & PM[t]))
    order.append(nxt); remaining.discard(nxt); cur = nxt

# (2) THE GLOBAL ITERATE (the fixpoint!!)
pool = set()
for ps in range(6):
    new_pool = set()
    use = Counter()
    bases = [None] * V
    for t in order:
        # the pool-candidates: the current pool (the prior passes!!) + this pass's adds
        b = solve_target(t, list(pool | new_pool))
        bases[t] = b
        for x in b:
            use[x] += 1
            new_pool.add(x)
    log('  pass %d: the pool %d | the uses %d | the reads %s' % (
        ps, len(new_pool), sum(use.values()),
        dict(sorted(Counter(len(b) for b in bases).items()))))
    if new_pool == pool:
        break
    pool = new_pool

# (3) THE CENSUS + THE R + THE PRICE
log('\nTHE FINAL: the pool %d' % len(pool))
use = Counter()
for t in range(V):
    for x in bases[t]: use[x] += 1
log('  the use-census: %s' % dict(sorted(Counter(use.values()).items())))
log('  the per-target reads: %s' % dict(sorted(Counter(len(b) for b in bases).items())))
R_est = len(pool) + 9 + 130
log('\nTHE R: %d (the pool %d + 9 gathers + ~130 gather-side!!)' % (R_est, len(pool)))
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (R_est, R_est + 40, 480):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else str(dd.get('error', 'NO-ROOT'))))
json.dump({'pool': [list(s for s in range(V) if (tri >> s) & 1) for tri in pool],
           'bases': [[list(s for s in range(V) if (tri >> s) & 1) for tri in b] for b in bases]},
          open('ii19_nat97b_design.json', 'wt'))
log('SAVED ii19_nat97b_design.json')
