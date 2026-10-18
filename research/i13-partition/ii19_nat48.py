"""THE TRUE E8-240 CENSUS (ii19_nat48.py) — the mod-4 fix + the decoder-rank gate!!

THE nat47 BUGS FIXED: the half-roots need sum(b) = 0 (mod 4!!), NOT mod 2 (which gave the
norm-1/2 vectors + the ZERO vector!!); the +-e_i+-e_j roots: all four sign combos!!
THE GATES: (1) the true 240 (norms all 2!!); (2) THE DECODER RANK (the make-or-break!!);
(3) the piece economy; (4) the honest price at the measured economy.
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

# (0) THE TRUE 240 ROOTS (the even-coordinate E8!!)
roots = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots.add(tuple(Fraction(x, 2) for x in s))
roots = sorted(roots)
V = len(roots)
norms = sorted(set(sum(x * x for x in r) for r in roots))
log('THE TRUE E8-240: %d roots | the norms: %s' % (V, norms))
assert V == 240 and norms == [Fraction(2)], 'THE CONSTRUCTION!!'
H = 8
G = [[sum(a[i] * b[i] for i in range(8)) for b in roots] for a in roots]
ips = Counter()
for s in range(V):
    for t in range(s + 1, V):
        ips[G[s][t]] += 1
log('the ip-structure: %s' % {str(k): v for k, v in sorted(ips.items(), key=lambda kv: str(kv[0]))})
PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
ps = Counter(len(p) for p in PERP)
log('THE PERPS: %s' % dict(sorted(ps.items())))

# (1) THE DECODER RANK (the perp-pattern + self!!)
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
log('  the cst if all-dim-7: %d | if all-dim-8: %d' % (7 * rank_B, 8 * rank_B))

# (2) THE PIECE ECONOMY (the R420's greedy!!)
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

# (3) THE HONEST PRICE (the frontier's shape scaled!!)
hist0 = {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18}
base = dict(hist0); base[7] -= 9
bm = sum(r * c for r, c in base.items())
cst = 7 * rank_B
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
    log('THE HONEST MODEL PRICE at (240, 8, %d): NO-ROOT/spurious (c = %s)' % (R, c[0] if c else None))
json.dump({'roots': [list(map(str, r)) for r in roots], 'rank_B': int(rank_B), 'R': int(R)},
          open('ii19_nat48_e8240.json', 'w'))
log('saved ii19_nat48_e8240.json')
