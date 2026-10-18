"""THE SHARED-PARTITION SOLVE (ii19_nat96.py) — the B-basis with the maximal sharing!!

THE nat95's LESSON: the per-target fresh triples don't share (529/540 singletons!!) —
the pool 681 >> the 480 ceiling. THE PROTOCOL (this script!!): THE GLOBAL TRIPLE POOL:
per target: perp(t) = the DISJOINT 21-triple partition, the greedy preferring the
ALREADY-USED triples (the sharing automatic!!), the new triples chosen for the FUTURE
READERS (the triple's perp-count (|perp(a) ∩ perp(b) ∩ perp(c)| (the ~15-target
sharing!!))). THE MEASUREMENTS:
(1) THE POOL GROWTH (the distinct triples (the R!!!));
(2) THE PER-TARGET READS (the 21-partitions ✓ exact!!);
(3) THE READER-LOADS (the chain-capacity-fit (the dup-budget!!));
(4) THE R + THE PRICE -> THE EMISSION-GO!!!
"""
import os, sys, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
PERP = [set(p) for p in SPEC['PERP']]
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]        # the perp bitmasks (the reader-pools!!)
pc = lambda x: x.bit_count()

# the shared pool: {triple: use_count}
pool_use = Counter()
bases = []
log('(1) THE SHARED-PARTITION SOLVE:')
for t in range(V):
    res = set(PERP[t])
    base = []
    while res:
        resm = sum(1 << s for s in res)
        # (a) the USED triples fitting the residual (score 3!!) — the most-used first!!
        best_used = None; best_cnt = -1
        for tri, cnt in pool_use.items():
            if (tri & ~resm) == 0:          # tri ⊆ res
                if cnt > best_cnt: best_cnt = cnt; best_used = tri
        if best_used is not None:
            base.append(best_used); pool_use[best_used] += 1
            res ^= {s for s in range(V) if (best_used >> s) & 1}
            continue
        # (b) the NEW triple ⊆ res with the max future-readers (the sharing-score!!)
        rl = sorted(res)
        best_tri, best_sc = None, -1
        # the pair pre-filter: the top-CoP pairs first (the speed cap!!)
        pairs = []
        for i in range(len(rl)):
            a = rl[i]; pa = PM[a]
            for j in range(i + 1, len(rl)):
                b = rl[j]
                ab = pa & PM[b]
                p2 = pc(ab)
                if p2 >= 8: pairs.append((p2, a, b, ab))
        pairs.sort(reverse=True)
        for p2, a, b, ab in pairs[:400]:
            for c in rl:
                if c in (a, b): continue
                sc = pc(ab & PM[c])
                if sc > best_sc: best_sc = sc; best_tri = (1 << a) | (1 << b) | (1 << c)
            if best_sc >= p2 - 1: break     # the near-optimal found (the speed!!)
        if best_tri is None:
            a, b, c = rl[0], rl[1], rl[2]
            best_tri = (1 << a) | (1 << b) | (1 << c)
        base.append(best_tri); pool_use[best_tri] += 1
        res ^= {s for s in range(V) if (best_tri >> s) & 1}
    bases.append(base)
    if t % 20 == 0:
        log('  t=%3d: the pool %d' % (t, len(pool_use)))
log('  THE POOL: %d distinct triples | the uses %d' % (len(pool_use), sum(pool_use.values())))

# (2) the per-target reads
log('\n(2) THE PER-TARGET READS: %s' % dict(sorted(Counter(len(b) for b in bases).items())))
# (3) the reader-loads (the chain-fit!!)
log('\n(3) THE READER-LOADS (the chain-capacity ~ home(1..) + 4-5 clusters + 1 dying!!):')
log('  the triple-use census: %s' % dict(sorted(Counter(pool_use.values()).items())))
# the reader-loads EXACT: the triple's reader-set = the targets using it in their bases
readers = defaultdict(list)
for t, b in enumerate(bases):
    for tri in b: readers[tri].append(t)
log('  the exact reader-loads: %s' % dict(sorted(Counter(len(r) for r in readers.values()).items())))
# the home-read census: the first-triple of each target
firsts = Counter(bases[t][0] for t in range(V))
log('  the firsts: %d distinct (the home-reads)' % len(firsts))

# (4) THE R + THE PRICE
R_est = len(pool_use) + 9 + 80
log('\n(4) THE R: %d (the pool %d + 9 gathers + ~80 dups!!)' % (R_est, len(pool_use)))
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (R_est, R_est + 60, R_est + 120, 480):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else str(dd.get('error', 'NO-ROOT'))))
json.dump({'pool': [list((s for s in range(V) if (tri >> s) & 1)) for tri in pool_use],
           'bases': [[list(s for s in range(V) if (tri >> s) & 1) for tri in b] for b in bases]},
          open('ii19_nat96_design.json', 'wt'))
log('SAVED ii19_nat96_design.json (THE EMISSION-READY BASIS!!!)')
