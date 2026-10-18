"""THE INCREMENTAL EXACT-BASIS POOL (ii19_nat97.py) — the shared-triple route's core!!

THE nat96/96b's LESSON: the DISJOINT-partition rigidity blocks the sharing (the pool
719/783!!). THE PROTOCOL (this script!!): THE EXACT XOR-BASIS (the overlaps allowed
(the parity cancels!!)) over the INCREMENTALLY-GROWN SHARED POOL:
(1) THE TARGET-ORDER: the perp-adjacent chain (the next target = the max pool-line
    overlap (the early-reuse!!!));
(2) THE PER-TARGET BASIS: the pool-triples-first (the greedy XOR-reduction!!) + the
    exact-span over the pool + the fresh-triple finish (the max-reader new triples!!);
(3) THE LOCAL SEARCH: the singleton-elimination (the desync FIXED (the rollback on the
    failed re-solves!!!));
(4) THE CENSUS (the pool (the R!!!)) + THE PRICE -> THE EMISSION-GO!!!
"""
import os, sys, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
PERP = [set(p) for p in SPEC['PERP']]
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
pc = lambda x: x.bit_count()

pool_use = Counter()          # the shared pool (triple -> uses)
bases = [None] * V

def fresh_triple(res):
    """the max-reader triple fitting the residual (the capped scan!!)."""
    rl = sorted(res)
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
    if len(rl) <= 3:
        tri = 0
        for x in rl: tri |= (1 << x)
        return tri
    if best_tri is None:
        a, b, c = rl[0], rl[1], rl[2]
        best_tri = (1 << a) | (1 << b) | (1 << c)
    return best_tri

def solve_target(t, allow=()):
    """the basis: the pool-first greedy + the fresh finish; returns the triple list."""
    res = set(PERP[t])
    base = []
    pl = list(pool_use.keys())
    while res:
        resm = sum(1 << s for s in res)
        best_tri, best_score = None, 0
        for tri in pl:
            m = tri & resm
            out = pc(tri) - pc(m)
            red = pc(m) - out            # the XOR-reduction score
            if red > best_score: best_score = red; best_tri = tri
        if best_tri is not None:
            base.append(best_tri); pool_use[best_tri] += 1
            res ^= {s for s in range(V) if (best_tri >> s) & 1}
            continue
        tri = fresh_triple(res)
        base.append(tri); pool_use[tri] += 1
        res ^= {s for s in range(V) if (tri >> s) & 1}
    return base

# (1) THE TARGET-ORDER: the perp-adjacent chain!!
log('(1) THE ORDER + THE SOLVE:')
order = []
remaining = set(range(V))
cur = 0
order.append(cur); remaining.discard(cur)
while remaining:
    pm_mask = PM[cur]
    nxt = max(remaining, key=lambda t: pc(pm_mask & PM[t]))
    order.append(nxt); remaining.discard(nxt); cur = nxt
for t in order:
    bases[t] = solve_target(t)
log('  the pool after the pass: %d | the uses %d' % (len(pool_use), sum(pool_use.values())))
log('  the per-target reads: %s' % dict(sorted(Counter(len(b) for b in bases).items())))
log('  the use-census: %s' % dict(sorted(Counter(pool_use.values()).items())))

# (3) THE LOCAL SEARCH (the singleton-elimination, THE ROLLBACK FIXED!!)
log('\n(2) THE LOCAL SEARCH:')
for it in range(8):
    singles = [tri for tri, cnt in pool_use.items() if cnt == 1]
    elim = 0
    for tri in singles:
        t_use = next((t for t in range(V) if bases[t] and tri in bases[t]), None)
        if t_use is None: continue
        old = bases[t_use]
        for x in old: pool_use[x] -= 1
        del pool_use[tri]
        b2 = solve_target(t_use)
        if tri not in b2 and len(b2) <= len(old) + 1:
            bases[t_use] = b2
            elim += 1
        else:
            # THE FULL ROLLBACK (the phantom-uses FIXED!!)
            for x in b2: pool_use[x] -= 1
            pool_use[tri] = 1
            for x in old: pool_use[x] += 1
    log('  iter %d: eliminated %d | the pool %d' % (it, elim, len(pool_use)))
    if elim == 0: break
log('  THE FINAL POOL: %d | the uses %d' % (len(pool_use), sum(pool_use.values())))
log('  the use-census: %s' % dict(sorted(Counter(pool_use.values()).items())))
log('  the per-target reads: %s' % dict(sorted(Counter(len(b) for b in bases).items())))

# (4) THE R + THE PRICE
R_est = len(pool_use) + 9 + 130
log('\n(3) THE R: %d (the pool %d + 9 + ~130 gather-side!!)' % (R_est, len(pool_use)))
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (R_est, R_est + 50, 480):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else str(dd.get('error', 'NO-ROOT'))))
json.dump({'pool': [list(s for s in range(V) if (tri >> s) & 1) for tri in pool_use],
           'bases': [[list(s for s in range(V) if (tri >> s) & 1) for tri in b] for b in bases]},
          open('ii19_nat97_design.json', 'wt'))
log('SAVED ii19_nat97_design.json')
