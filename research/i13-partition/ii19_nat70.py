"""THE EXTENSION-WORD BUILD STAGE 2 (ii19_nat70.py) — THE CHAINS + THE FIRST EMISSION!!

THE ECONOMY (nat67!!): 147 pieces (3-line, 13.5-user!!) + 120 carriers + 9 gathers =
R 276!! THE TARGET PRICE: +45.94% (the frontier's shape!!). THE JUDGE: gcheck.py!!
HERE: (1) THE PIECE-CHAIN DESIGN (the 3-gate running-sums (the sources at their
singletons + the shared cells (the r434-grammar!!)) + the read-classes (the capacity-law
groups!!)); (2) THE CARRIERS (the per-target leftover-assembly!!); (3) THE GATHERS'
BUILDS; (4) THE EMISSION (D/A/scatter/B/C!!) + THE MASS + GCHECK!!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
E67 = json.load(open('ii19_nat67_ext120.json', 'rt'))
lines = [tuple(x) for x in SPEC['lines']]
V = len(lines)
H = 8
PERP = [set(p) for p in SPEC['PERP']]
W = np.array(SPEC['W'], dtype=np.uint8)
BASIS_IDX = SPEC['BASIS_IDX']
frames = SPEC['frames']
SINGLE, TPERP = SPEC['SINGLE'], SPEC['TPERP']

# the economy (nat67's greedy on the 120!!): re-run (the (3,4)!!) for the assignments!!
def greedy(kmin, umin):
    pair_count = Counter(); pair_users = defaultdict(list)
    for ti, pl in enumerate(PERP):
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
                unc = PERP[ti] - covered[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < kmin: continue
            piece = frozenset(sorted(common)[:kmin])
            real = [ti for ti in users if piece <= PERP[ti] - covered[ti]]
            if len(real) < umin: continue
            saving = len(piece) * len(real) - (len(piece) + len(real))
            if saving <= 0: continue
            cands.append((saving, piece, real))
        if not cands: break
        cands.sort(key=lambda c: c[0], reverse=True)
        for saving, piece, real in cands[:50]:
            if any(piece <= PERP[ti] - covered[ti] for ti in real):
                pool.append((piece, real))
                for ti in real: covered[ti] |= set(piece)
                break
        else: break
    return pool, covered

pool, covered = greedy(3, 4)
left = [PERP[t] - covered[t] for t in range(V)]
RET = 9
R = len(pool) + sum(1 for lo in left if lo) + RET
log('(0) THE ECONOMY: %d pieces + %d carriers + %d = R %d' % (
    len(pool), sum(1 for lo in left if lo), RET, R))
json.dump({'pool': [(sorted(p), sorted(u)) for p, u in pool], 'left': [sorted(lo) for lo in left]},
          open('ii19_nat70_pool.json', 'w'))
log('saved the pool!! (the chains/emission next!!)')
