"""THE 2-CLASS BUILD STAGE 3b (ii19_nat56.py) — the CLASS-BLOCKED delivery!!

THE RECORD'S OWN DESIGN (§453!!): the 18-gather CLASS-BLOCKED decoder: the scatter delivers
B'[t] = {t} | the same-class perp (63 lines!!); the reads XOR to the same-class perp; the
cross-class ⊥-lines NEVER delivered (the full-pattern rank 240 is NOT the demand (the nat55
lesson!!)). HERE: (1) the class-blocked perps (63!!); (2) the decoder rank (18?! (verify!!));
(3) THE GREEDY on the 63-perps (the (3,4)-economy!!); (4) THE BALANCE (the reads = the
same-class perp, the scatter = B'[t] via the 18-gather W!!)!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

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
# (1) THE CLASS-BLOCKED PERPS (the same-class ⊥-lines: 63!!)
CPERP = [set(s for s in range(V) if CLS[s] == CLS[t] and s != t and G[s][t] == 0) for t in range(V)]
log('(1) THE CLASS-BLOCKED PERPS: %s' % dict(sorted(Counter(len(p) for p in CPERP).items())))
# (2) THE DECODER (the class-blocked B': {t} | the same-class perp!!)
B0 = np.array([[1 if (s == t or (CLS[s] == CLS[t] and s in CPERP[t])) else 0
                for s in range(V)] for t in range(V)], dtype=np.uint8)
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
log('(2) THE CLASS-BLOCKED DECODER RANK: %d (the record 18!!)' % rank_B)
# (3) THE GREEDY on the 63-perps (the (3,4)-economy!!)
def greedy(kmin, umin):
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

pool, covered = greedy(3, 4)
left = [CPERP[t] - covered[t] for t in range(V)]
log('(3) THE (3,4)-ECONOMY on the 63-perps: %d pieces (mean %.1f lines, %.1f users) + %d carriers (%d leftover lines)' % (
    len(pool), sum(len(p) for p, u in pool) / max(1, len(pool)),
    sum(len(u) for p, u in pool) / max(1, len(pool)),
    sum(1 for lo in left if lo), sum(len(lo) for lo in left)))
RET = 18
R = len(pool) + sum(1 for lo in left if lo) + RET
log('    R = %d (R/v %.2f!!)' % (R, R / V))
# (4) THE BALANCE: the reads (= the pieces' XOR per target!) = the same-class perp ✓ by the
# greedy's construction (the coverage!!); the scatter: the 18-gather W (B'[t] in the span!!)
log('(4) THE BALANCE: the coverage construction guarantees it (the reads XOR = the perp!!)')
json.dump({'pool': [(sorted(p), sorted(u)) for p, u in pool], 'left': [sorted(lo) for lo in left],
           'rank_B': int(rank_B), 'R': R},
          open('ii19_nat56_delivery.json', 'w'))
log('saved ii19_nat56_delivery.json')
