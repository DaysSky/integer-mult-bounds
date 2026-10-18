"""THE E8-240 CENSUS (ii19_nat47.py) — the full root system at h=8 (the untouched direction!!).

THE V-SWEEP'S VERDICT (nat46!!): the c grows with v at the wall R = 4v - 10: the E8-240
(THE FULL ROOT SYSTEM: 112 roots +-e_i+-e_j + 128 half-roots, span dim 8, the perps 126!!)
prices **+93.75%** in the model!!!  THE GATES (the structure reality!!):
(1) THE DECODER: the 240x240 perp-pattern's GF(2) rank (the CST!!!) — the k=-1 lesson!!
(2) THE JUNK/PIECE ECONOMY: the perps (126!!): the shared-pieces greedy (the R420's own!!).
(3) THE HONEST PRICE at the measured economy.
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

# (0) THE 240 ROOTS (the standard E8 model: the even-coordinate system!!)
roots = []
for i, j in itertools.permutations(range(8), 2):
    v = [0] * 8
    v[i] = 1; v[j] = 1
    roots.append(tuple(v))
    v2 = list(v); v2[i] = -1
    roots.append(tuple(v2))
for bits in itertools.product([0, 1], repeat=8):
    if sum(bits) % 2 == 0:
        roots.append(tuple(Fraction(b, 2) for b in bits))
roots = sorted(set(roots))
V = len(roots)
log('THE E8-240: %d roots | the norm check: %s' % (V, sorted(set(sum(x * x for x in r) for r in roots))))
H = 8
G = [[sum(a[i] * b[i] for i in range(8)) for b in roots] for a in roots]
# (1) THE PERP-PATTERN RANK (the decoder!!)
PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
ps = Counter(len(p) for p in PERP)
log('THE PERPS: %s' % dict(sorted(ps.items())))
B0 = np.array([[1 if (s == t or s in PERP[t]) else 0 for s in range(V)] for t in range(V)], dtype=np.uint8)
def gf2_rank(M):
    M = M.copy(); rr = 0; rows, cols = M.shape
    for c in range(cols):
        p = next((i for i in range(rr, rows) if M[i][c]), None)
        if p is None: continue
        M[[rr, p]] = M[[p, rr]]
        for i in range(rows):
            if i != rr and M[i][c]:
                M[i] ^= M[rr]
        rr += 1
    return rr
rank_B = gf2_rank(B0)
log('THE DECODER RANK (the perp-pattern + self!!): %d' % rank_B)
# the within-E8-block structure: the class-split (the 112-roots vs the 128-half!!)
# (2) THE JUNK/PIECE ECONOMY (the R420's greedy!!!)
def greedy(kmin, umin, perps, VV):
    pair_count = Counter(); pair_users = defaultdict(list)
    for ti, pl in enumerate(perps):
        for a, b in itertools.combinations(sorted(pl), 2):
            pair_count[(a, b)] += 1; pair_users[(a, b)].append(ti)
    covered = [set() for _ in range(VV)]
    pool = []
    while True:
        cands = []
        for (a, b), c in pair_count.items():
            if c < 2: continue
            users = [ti for ti in pair_users[(a, b)] if a not in covered[ti] and b not in covered[ti]]
            if len(users) < umin: continue
            common = None
            for ti in users:
                unc = perps[ti] - covered[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < kmin: continue
            piece = frozenset(sorted(common)[:kmin])
            real = [ti for ti in users if piece <= perps[ti] - covered[ti]]
            if len(real) < umin: continue
            saving = len(piece) * len(real) - (len(piece) + len(real))
            if saving <= 0: continue
            cands.append((saving, piece, real))
        if not cands: break
        cands.sort(key=lambda c: c[0], reverse=True)
        for saving, piece, real in cands[:50]:
            if any(piece <= perps[ti] - covered[ti] for ti in real):
                pool.append((piece, real))
                for ti in real: covered[ti] |= set(piece)
                break
        else: break
    return pool, covered

pool, covered = greedy(3, 4, PERP, V)
left = [PERP[t] - covered[t] for t in range(V)]
R = len(pool) + sum(1 for lo in left if lo) + rank_B
log('THE PIECE ECONOMY: %d pieces (mean %.1f lines, %.1f users) + %d carriers + %d gathers = R %d' % (
    len(pool), sum(len(p) for p, u in pool) / max(1, len(pool)),
    sum(len(u) for p, u in pool) / max(1, len(pool)),
    sum(1 for lo in left if lo), rank_B, R))
log('  R/v = %.2f (the wall 4!!)' % (R / V))
# (3) THE HONEST PRICE at the measured economy (the frontier's shape scaled!!)
hist0 = {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18}
base = dict(hist0); base[7] -= 9
bm = sum(r * c for r, c in base.items())
cst = 7 * rank_B if rank_B <= 12 else None
if cst:
    climb = 8 * R + 2 * V * 7
    acc = Counter()
    for r in sorted(base, key=lambda r: -base[r] * r):
        n = int(Fraction(climb * (base[r] * r), bm) / r)
        acc[r] = n
    rem = climb - sum(r * c for r, c in acc.items())
    while rem > 0:
        for r in sorted(base, key=lambda r: -base[r]):
            if r <= rem: acc[r] += 1; rem -= r; break
        else:
            acc[max(1, rem)] += 1; rem = 0
    acc[7] += rank_B
    c = price(dict(acc), V, 8, R)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        log('THE HONEST MODEL PRICE at (240, 8, %d): %.20g (%+.2f%% vs the frontier!!)' % (
            R, float(c[0]), 100 * (float(c[0]) / float(FC) - 1)))
    else:
        log('THE HONEST MODEL PRICE at (240, 8, %d): NO-ROOT/spurious' % R)
else:
    log('the cst too big (rank %d!!): the honest price pending the decoder work' % rank_B)
json.dump({'roots': [list(map(str, r)) for r in roots], 'rank_B': int(rank_B)},
          open('ii19_nat47_e8240.json', 'w'))
log('saved ii19_nat47_e8240.json')
