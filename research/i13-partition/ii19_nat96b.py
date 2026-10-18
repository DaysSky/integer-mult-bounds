"""THE SEEDED SHARED-PARTITION SOLVE (ii19_nat96b.py) — the pool-minimization!!

THE nat96's LESSON: the greedy's pool 719 (the avg use 3.5 vs the triples' ~36-reader
potential!!!). THE PROTOCOL (this script!!):
(1) THE GLOBAL SEEDS: the top-reader triples (|perp(a) ∩ perp(b) ∩ perp(c)| (the max
    sharing!!)) — the pool PRE-POPULATED (~300-600 seeds!!);
(2) THE PER-TARGET SOLVE over the SEEDS+USED (the exact 21-partition, the seeds-first!!);
(3) THE LOCAL SEARCH: the singleton-triples eliminated (the re-solves over the pool!!));
(4) THE CENSUS (the pool (the R!!), the reads, the loads) + THE PRICE -> THE EMISSION-GO.
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
FULL = (1 << V) - 1

# (1) THE GLOBAL SEEDS: the top-reader triples!!
log('(1) THE GLOBAL SEED SCAN (the max-reader triples!!):')
pairs = []
for a in range(V):
    for b in range(a + 1, V):
        p2 = pc(PM[a] & PM[b])
        if p2 >= 24:
            pairs.append((p2, a, b))
pairs.sort(reverse=True)
log('  the pairs with |perp(a)∩perp(b)| >= 24: %d' % len(pairs))
cand = Counter()
for p2, a, b in pairs[:4000]:
    ab = PM[a] & PM[b]
    rest = ab
    while rest:
        c = (rest & -rest).bit_length() - 1
        rest ^= (1 << c)
        if c > b:
            tri = (1 << a) | (1 << b) | (1 << c)
            cand[tri] = pc(ab & PM[c])
    # the full c-scan for the top pairs
for p2, a, b in pairs[:800]:
    ab = PM[a] & PM[b]
    for c in range(V):
        if c in (a, b): continue
        s3 = pc(ab & PM[c])
        if s3 >= 20:
            cand[(1 << a) | (1 << b) | (1 << c)] = s3
log('  the seed candidates: %d (the reader-counts %s)'
    % (len(cand), dict(sorted(Counter(cand.values()).items()))))
seeds = set(cand)
log('  THE SEED POOL: %d' % len(seeds))

# (2) THE PER-TARGET SOLVE (the seeds/used-first, the 21-partition!!)
log('\n(2) THE PER-TARGET SOLVE:')
pool_use = Counter()
bases = []
def solve_target(t, res):
    base = []
    while res:
        resm = sum(1 << s for s in res)
        best_used, best_cnt = None, -1
        for tri, cnt in pool_use.items():
            if (tri & ~resm) == 0 and cnt > best_cnt:
                best_cnt = cnt; best_used = tri
        if best_used is not None:
            base.append(best_used); pool_use[best_used] += 1
            res ^= {s for s in range(V) if (best_used >> s) & 1}
            continue
        # the SEED fit!!
        best_seed, best_cnt = None, -1
        for tri in seeds:
            if (tri & ~resm) == 0 and pool_use[tri] == 0 and cand[tri] > best_cnt:
                best_cnt = cand[tri]; best_seed = tri
        if best_seed is not None:
            base.append(best_seed); pool_use[best_seed] += 1
            res ^= {s for s in range(V) if (best_seed >> s) & 1}
            continue
        # the fresh triple (the future-readers!!)
        rl = sorted(res)
        best_tri, best_sc = None, -1
        for i in range(len(rl)):
            a = rl[i]; pa = PM[a]
            for j in range(i + 1, min(len(rl), i + 30)):
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
        base.append(best_tri); pool_use[best_tri] += 1
        res ^= {s for s in range(V) if (best_tri >> s) & 1}
    return base
for t in range(V):
    bases.append(solve_target(t, set(PERP[t])))
log('  the pool: %d | the uses: %d' % (len(pool_use), sum(pool_use.values())))
log('  the per-target reads: %s' % dict(sorted(Counter(len(b) for b in bases).items())))

# (3) THE LOCAL SEARCH: eliminate the singleton triples!!
log('\n(3) THE LOCAL SEARCH (the singleton-elimination!!):')
for it in range(6):
    singles = [tri for tri, cnt in pool_use.items() if cnt == 1]
    if not singles: break
    elim = 0
    for tri in singles:
        # the using target re-solves WITHOUT the singleton (over the pool + the seeds!!)
        t_use = next(t for t in range(V) if tri in bases[t])
        save = pool_use[tri]
        del pool_use[tri]
        for x in bases[t_use]:
            if x != tri: pool_use[x] -= 1
        b2 = solve_target(t_use, set(PERP[t_use]))
        if len(b2) <= len(bases[t_use]) + 1 and tri not in b2:
            bases[t_use] = b2
            elim += 1
        else:
            pool_use[tri] = save
            for x in bases[t_use]:
                if x != tri: pool_use[x] += 1
    log('  iter %d: eliminated %d | the pool %d' % (it, elim, len(pool_use)))
    if elim == 0: break
log('  THE FINAL POOL: %d | the uses %d' % (len(pool_use), sum(pool_use.values())))
log('  the use-census: %s' % dict(sorted(Counter(pool_use.values()).items())))
log('  the per-target reads: %s' % dict(sorted(Counter(len(b) for b in bases).items())))

# (4) THE R + THE PRICE
R_est = len(pool_use) + 9 + 130
log('\n(4) THE R: %d (the pool %d + 9 + ~130 gather-side!!)' % (R_est, len(pool_use)))
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
          open('ii19_nat96b_design.json', 'wt'))
log('SAVED ii19_nat96b_design.json')
