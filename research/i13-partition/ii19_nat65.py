"""THE FAMILY FRONTIER LADDER (ii19_nat65.py) — the sparse-decoder subsets at v > 111!!

THE PROGRAM-DEFINITION (nat64!!): the frontier (the P111-R434!!) = the II19-family word at
the 2x-E8-subset (the positive-definite (the family's OWN class!!)) — THE V-SWEEP's BIGGER
SUBSETS (the E8-120: +13.07%!! the 125: +19.59%!! the 130: +25.55%!!!) ARE FAMILY-LEGAL!!
THE DECIDING GATE: THE SPARSE-DECODER SUBSETS at v = 120-130 (the perp-pattern rank (the
record's era-1 hunt (the 111/120 exist!!)): the RANK + the junk-economy + the price!!
HERE: (1) the subset families (the 2x-E8 (the P111's class!!): the coordinate-roots + the
half-roots (the canon!!)); (2) THE RANK at v = 111 (the control!!), 120, 125, 130, 140;
(3) the junk/piece economy; (4) THE HONEST PRICES!!
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

# the 2x-E8 roots (the P111's class!!): the canonical 120 (the +-pairs!!)
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
roots120 = sorted(d8.values())          # the canonical 120 (the 2x-scale candidates!!)
# the P111's own 111: read from the frontier word (the reference subset!!)
w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
P111 = set()
for l in w['lines']:
    t = tuple(Fraction(x, 2) for x in l)      # the /2: the 1x-scale!!
    P111.add(canon(t))
log('THE P111 subset: %d canonical lines (of the 120!!)' % len(P111))
missing = [r for r in roots120 if canon(tuple(r)) not in P111]
log('    the missing (the 120 - the 111): %d' % len(missing))

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

def subset_census(lines, name):
    V = len(lines)
    Lx = [[Fraction(x) * 2 for x in l] for l in lines]        # the 2x-scale (the P111-form den 2!!)
    G = [[sum(a[i] * b[i] for i in range(8)) for b in Lx] for a in Lx]
    PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
    B0 = np.array([[1 if (s == t or s in PERP[t]) else 0 for s in range(V)] for t in range(V)], dtype=np.uint8)
    rank_B = gf2_rank(B0)
    log('  %s: v %d | the perps %s | THE DECODER RANK: %d' % (
        name, V, dict(sorted(Counter(len(p) for p in PERP).items())), rank_B))
    return V, PERP, rank_B

# (2) the ladder: the P111 (the control!!) + the 120 + the 125/130 (the subsets?! — the
# 125/130: BIGGER than the canonical 120?! — the 240-roots (the +-pairs both!!): the
# 125 = the 120 + 5 opposites?! the 130 = +10!! — the family's subsets (the mixed-sign!!)!!
log('(2) THE FAMILY LADDER:')
V111, PERP111, R111 = subset_census([d8[c] for c in sorted(P111)], 'THE P111 (the control!!)')
V120, PERP120, R120 = subset_census(roots120, 'THE E8-120')
# the 125: the 120 + the 5 -pairs (the opposites (the norm-4 (the 2x!!))!!)
opp = {canon(tuple(-x for x in r)): r for r in roots120}
extra5 = sorted(opp.keys())[:5]
lines125 = list(roots120) + [opp[c] for c in extra5]
V125, PERP125, R125 = subset_census(lines125, 'THE E8-125 (the +5 opposites!!)')
extra10 = sorted(opp.keys())[:10]
lines130 = list(roots120) + [opp[c] for c in extra10]
V130, PERP130, R130 = subset_census(lines130, 'THE E8-130 (the +10!!)')
# (3) the junk-economy (the (3,4)-greedy!!) at the 120/125/130!!
def greedy(PERP, V, kmin, umin):
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
    left = [PERP[t] - covered[t] for t in range(V)]
    return pool, left

for nm, (Vv, PERPv, RANKv) in [('the 120', (V120, PERP120, R120)),
                               ('the 125', (V125, PERP125, R125)),
                               ('the 130', (V130, PERP130, R130))]:
    pool, left = greedy(PERPv, Vv, 3, 4)
    R = len(pool) + sum(1 for lo in left if lo) + max(9, RANKv)
    log('(3) %s: %d pieces + %d carriers + %d gathers = R %d (R/v %.2f!!)' % (
        nm, len(pool), sum(1 for lo in left if lo), max(9, RANKv), R, R / Vv))
    # (4) THE PRICE (the frontier's shape scaled!! (the nat49-style!!))
    hist0 = {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18}
    base = dict(hist0); base[7] -= 9
    bm = sum(r * c for r, c in base.items())
    cst = 7 * max(9, RANKv)
    climb = 8 * R + 2 * Vv * 7
    acc = Counter()
    for r in sorted(base, key=lambda r: -base[r] * r):
        acc[r] = int(Fraction(climb * (base[r] * r), bm) / r)
    rem = climb - sum(r * c for r, c in acc.items())
    while rem > 0:
        for r in sorted(base, key=lambda r: -base[r]):
            if r <= rem: acc[r] += 1; rem -= r; break
        else:
            acc[max(1, rem)] += 1; rem = 0
    acc[7] += max(9, RANKv)
    c = price(dict(acc), Vv, 8, R)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        log('(4) %s: THE FRONTIER-SHAPE PRICE at (v %d, 8, R %d): %+.2f%% vs the frontier!!!' % (
            nm, Vv, R, 100 * (float(c[0]) / float(FC) - 1)))
    else:
        log('(4) %s: NO-ROOT/spurious' % nm)
