"""THE TUNED POOL-SOLVE (ii19_nat98.py) — the use-priority + the seeds + the search!!

THE BUDGET (the verified law!!): R <= 480 (the cap 36v!!); the honest split: the pool
<= ~300 + 9 gathers + ~130 gather-side + ~60 chain-dups. THE nat97's pool 369 -> THE
MISSING LEVERS (this script!!):
(1) THE USE-PRIORITY TIE-BREAK (the pool-triples preferred at equal red (the sharing!!));
(2) THE SEEDS AT red>=1 (the 36/20-reader triples pre-seeded (the fits the partition
    rigidity blocked (the nat96b's lesson FIXED!!));
(3) THE LOCAL SEARCH (the singleton-elimination (THE ROLLBACK FIXED!!));
(4) THE ITERATE-TO-FIXPOINT + THE CENSUS + THE PRICE -> THE EMISSION-GO!!!
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

# THE SEEDS: the max-reader triples (the global scan!!)
log('(0) THE SEED SCAN:')
pairs = []
for a in range(V):
    for b in range(a + 1, V):
        p2 = pc(PM[a] & PM[b])
        if p2 >= 24: pairs.append((p2, a, b))
pairs.sort(reverse=True)
seed_sc = {}
for p2, a, b in pairs[:600]:
    ab = PM[a] & PM[b]
    for c in range(V):
        if c in (a, b): continue
        s3 = pc(ab & PM[c])
        if s3 >= 20:
            seed_sc[(1 << a) | (1 << b) | (1 << c)] = s3
log('  the seeds: %d (the scores %s)' % (len(seed_sc), dict(sorted(Counter(seed_sc.values()).items()))))
SEEDS = list(seed_sc.keys())

def fresh_wire(res):
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

use = Counter()
def solve_target(t, poolset):
    global use
    res = set(PERP[t])
    base = []
    while res:
        resm = sum(1 << s for s in res)
        best_tri, best_key = None, None
        for tri in poolset:
            m = pc(tri & resm)
            red = m - (pc(tri) - m)
            if red <= 0: continue
            key = (red, use.get(tri, 0))          # THE USE-PRIORITY TIE-BREAK!!!
            if best_key is None or key > best_key: best_key = key; best_tri = tri
        if best_tri is None:
            best_tri = fresh_wire(res)
        base.append(best_tri)
        use[best_tri] += 1
        poolset.add(best_tri)
        res ^= {s for s in range(V) if (best_tri >> s) & 1}
    return base

# the order (the perp-adjacent chain!!)
order = []
remaining = set(range(V)); cur = 0
order.append(cur); remaining.discard(cur)
while remaining:
    nxt = max(remaining, key=lambda t: pc(PM[cur] & PM[t]))
    order.append(nxt); remaining.discard(nxt); cur = nxt

poolset = set(SEEDS)
bases = [None] * V
log('\n(1) THE SOLVE (the seeds + the use-priority!!):')
for t in order:
    bases[t] = solve_target(t, poolset)
log('  the pool: %d | the uses: %d' % (len(poolset), sum(use.values())))
log('  the reads: %s' % dict(sorted(Counter(len(b) for b in bases).items())))
log('  the use-census: %s' % dict(sorted(Counter(use.values()).items())))

# (2) THE LOCAL SEARCH (the singletons; the rollback FIXED!!)
log('\n(2) THE LOCAL SEARCH:')
for it in range(8):
    singles = [tri for tri, cnt in use.items() if cnt == 1]
    elim = 0
    for tri in singles:
        t_use = next((t for t in range(V) if bases[t] and tri in bases[t]), None)
        if t_use is None: continue
        old = bases[t_use]
        # snapshot
        snap = dict(use)
        for x in old: use[x] -= 1
        use.pop(tri, None)
        b2 = solve_target(t_use, set(poolset))
        if tri not in b2 and len(b2) <= len(old) + 1:
            bases[t_use] = b2; elim += 1
        else:
            for k2, v2 in snap.items(): use[k2] = v2     # THE FULL RESTORE!!
    log('  iter %d: elim %d | the pool %d' % (it, elim, len([x for x in use if use[x] > 0])))
    if elim == 0: break
live = [x for x in use if use[x] > 0]
log('  THE FINAL POOL: %d' % len(live))
log('  the reads: %s' % dict(sorted(Counter(len(b) for b in bases).items())))
log('  the use-census: %s' % dict(sorted(Counter(use[x] for x in live).items())))

R_est = len(live) + 9 + 130
log('\n(3) THE R: %d (the pool %d + 9 + ~130!!)' % (R_est, len(live)))
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
json.dump({'pool': [list(s for s in range(V) if (tri >> s) & 1) for tri in live],
           'bases': [[list(s for s in range(V) if (tri >> s) & 1) for tri in b] for b in bases]},
          open('ii19_nat98_design.json', 'wt'))
log('SAVED ii19_nat98_design.json')
