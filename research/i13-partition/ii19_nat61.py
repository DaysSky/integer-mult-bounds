"""THE LEAN-ECONOMY GRID (ii19_nat61.py) — the deep-DAG R toward the MX-crossover!!

THE TARGET: the economy (the pieces + the carriers + the 18 retained!!) at R <= 460 —
where the MX-shape crosses the frontier (the nat52 map: +0.4% at 460 / +4.5% at 400 /
+7.8% at 350!!).  THE RECORD'S OWN DESIGN: 202 + 94 + 18 = 314!! (the §453!!) — my greedy
gave 292 + 240 (R 550!!) — THE GRID: the (kmin, umin) variants + the piece-selection
orders (the FIRST-k vs the max-saving subset!!) + the coverage-depth knob (the greedy's
iteration structure!!).  THE OUTPUT: the leanest economies + the MX/W4 prices at their R!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({int(k): int(val) for k, val in hist.items()}, v, h, R)
FC = Fraction(str('0.001744385950814795279853'))

roots240 = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots240.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots240.add(tuple(Fraction(x, 2) for x in s))

def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

d8 = {canon(r): r for r in roots240}
roots = sorted(d8.values())
V = 240
H = 10
L = []
for c in (0, 1):
    for a in roots:
        L.append([Fraction(x) for x in a] + [Fraction(c), Fraction(0)])
FORM = [[Fraction(0)] * H for _ in range(H)]
for i in range(8): FORM[i][i] = Fraction(1)
FORM[8][9] = FORM[9][8] = Fraction(1)
def ip(x, y):
    return sum(x[i] * y[j] * FORM[i][j] for i in range(H) for j in range(H) if FORM[i][j])
G = [[ip(L[s], L[t]) for t in range(V)] for s in range(V)]
CLS = [s // 120 for s in range(V)]
CPERP = [set(s for s in range(V) if CLS[s] == CLS[t] and s != t and G[s][t] == 0) for t in range(V)]

def greedy(kmin, umin, best_subset=False):
    pair_count = Counter(); pair_users = defaultdict(list)
    for ti, pl in enumerate(CPERP):
        for a, b in itertools.combinations(sorted(pl), 2):
            pair_count[(a, b)] += 1; pair_users[(a, b)].append(ti)
    covered = [set() for _ in range(V)]
    pool = []
    while True:
        cands = []
        for (a, b), c in pair_count.items():
            if c < 2: continue
            users = [ti for ti in pair_users[(a, b)] if a not in covered[ti] and b not in covered[ti]]
            if len(users) < umin: continue
            common = None
            for ti in users:
                unc = CPERP[ti] - covered[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < kmin: continue
            if best_subset:
                # THE MAX-SAVING SUBSET (the biggest saving = k*u - (k+u)!!):
                best = None
                for k in range(kmin, min(len(common), 8) + 1):
                    piece = frozenset(sorted(common)[:k])
                    real = [ti for ti in users if piece <= CPERP[ti] - covered[ti]]
                    if len(real) < umin: continue
                    saving = k * len(real) - (k + len(real))
                    if saving > 0 and (best is None or saving > best[0]):
                        best = (saving, piece, real)
                if best is None: continue
                cands.append(best)
            else:
                piece = frozenset(sorted(common)[:kmin])
                real = [ti for ti in users if piece <= CPERP[ti] - covered[ti]]
                if len(real) < umin: continue
                saving = len(piece) * len(real) - (len(piece) + len(real))
                if saving <= 0: continue
                cands.append((saving, piece, real))
        if not cands: break
        cands.sort(key=lambda c: c[0], reverse=True)
        for saving, piece, real in cands[:50]:
            if any(piece <= CPERP[ti] - covered[ti] for ti in real):
                pool.append((piece, real))
                for ti in real: covered[ti] |= set(piece)
                break
        else: break
    return pool, covered

def economy_price(R):
    CST = 162
    out = {}
    climb = 10.0 * R + 2.0 * V * 9
    for nm, sh in [('D', {1: 0.262, 2: 0.571 / 2, 4: 0.048 / 4, 5: 0.119 / 5}),
                   ('W4', {1: 1100, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 18, 9: 2}),
                   ('MX', {9: 1.0})]:
        if nm == 'W4':
            bm = sum(r * c for r, c in sh.items())
            acc = Counter()
            for r in sorted(sh, key=lambda r: -sh[r] * r):
                acc[r] = int(Fraction(int(climb) * (sh[r] * r), bm) / r)
            rem = int(climb) - sum(r * c for r, c in acc.items())
            while rem > 0:
                for r in sorted(sh, key=lambda r: -sh[r]):
                    if r <= rem: acc[r] += 1; rem -= r; break
                else:
                    acc[max(1, rem)] += 1; rem = 0
            h = dict(acc)
            h[9] = h.get(9, 0) + 18
        else:
            h = {k: int(v * climb) for k, v in sh.items()}
            h[9] = h.get(9, 0) + 18
        c = price(h, V, H, R)
        if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
            out[nm] = 100 * (float(c[0]) / float(FC) - 1)
    return out

log('THE LEAN-ECONOMY GRID (the 63-perps!!) — the hunt: R <= 460 (the MX-crossover!!)')
results = []
for kmin, umin in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4), (5, 2), (5, 3), (6, 2)]:
    for best in (False, True):
        pool, covered = greedy(kmin, umin, best)
        left = [CPERP[t] - covered[t] for t in range(V)]
        ncar = sum(1 for lo in left if lo)
        R = len(pool) + ncar + 18
        pl = sum(len(p) for p, u in pool) / max(1, len(pool))
        pu = sum(len(u) for p, u in pool) / max(1, len(pool))
        results.append((R, kmin, umin, best, len(pool), ncar, pl, pu))
        log('  (%d,%d)%s: %d pieces (%.1f lines, %.1f users!!) + %d carriers -> R %d' % (
            kmin, umin, '*' if best else ' ', len(pool), pl, pu, ncar, R))
results.sort()
log('')
log('THE LEANEST ECONOMIES + THE PRICES!!')
for R, kmin, umin, best, np_, ncar, pl, pu in results[:6]:
    log('  R %d (%d,%d)%s: the prices %s' % (R, kmin, umin, '*' if best else ' ', economy_price(R)))
json.dump({'grid': results}, open('ii19_nat61_grid.json', 'w'))
log('saved ii19_nat61_grid.json')
