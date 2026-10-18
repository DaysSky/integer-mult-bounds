"""THE 2-CLASS BUILD STAGE 5 (ii19_nat58.py) — the (2,2)-economy + the chain-aware pass!!

THE FOUNDATIONS (nat54-57 ✓!!): the frames (481 nondegenerate!!), the decoder (rank 18 ✓),
the W (✓), the perps (63 ✓). HERE: (a) the (2,2)-economy (the record's lean R ~ 317!!);
(b) THE CHAIN-AWARE PASS (the nat44-machinery on the 63-perps (the roles + the budgets +
the caps!!)) — the kept-count + the loads + the ceilings; (c) the R + the price band.
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
Linn = np.array([[float(x) for x in l] for l in L])
rank = lambda lines: int(np.linalg.matrix_rank(Linn[sorted(lines)])) if lines else 0

# (a) THE (2,2)-ECONOMY!!
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

pool, covered = greedy(2, 2)
left = [CPERP[t] - covered[t] for t in range(V)]
RET = 18
R22 = len(pool) + sum(1 for lo in left if lo) + RET
log('(a) THE (2,2)-ECONOMY: %d pieces (mean %.1f lines, %.1f users) + %d carriers (%d lines) + %d = R %d (R/v %.2f!!)' % (
    len(pool), sum(len(p) for p, u in pool) / max(1, len(pool)),
    sum(len(u) for p, u in pool) / max(1, len(pool)),
    sum(1 for lo in left if lo), sum(len(lo) for lo in left), RET, R22, R22 / V))

# (b) THE CHAIN-AWARE PASS (the nat44-machinery (the 3rd-role budgets!!))
partner = {}; third_users = defaultdict(set); pairs_of = defaultdict(list)
kept = []
CAP = 21
c2 = [set() for _ in range(V)]
while True:
    best = None
    for b in range(V):
        for a in sorted(CPERP[b]):
            if a >= b: continue
            if b in partner and partner[b] != a: continue
            users = [t for t in range(V) if a in CPERP[t] and b in CPERP[t]
                     and a not in c2[t] and b not in c2[t]]
            if len(users) < 4: continue
            if len(users) > CAP: users = sorted(users)[:CAP]
            common = None
            for t in users:
                unc = CPERP[t] - c2[t]
                common = set(unc) if common is None else (common & unc)
            common -= {a, b}
            for c3 in sorted(common):
                if c3 in partner and any(partner[c3] not in CPERP[t] for t in users): continue
                nu = third_users[c3] | set(users)
                if any(x not in CPERP[u] for u in (third_users[c3] - set(users)) for x in (a, b)): continue
                frung = {a, b, c3} | {x for p in pairs_of[c3] for x in p}
                if rank(nu) + rank(frung) > 9: continue
                saving = 3 * len(users) - (3 + len(users))
                if saving <= 0: continue
                if best is None or saving > best[0]:
                    best = (saving, a, b, c3, users)
    if best is None: break
    saving, a, b, c3, users = best
    kept.append((frozenset({a, b, c3}), users))
    partner[b] = a
    third_users[c3] |= set(users)
    pairs_of[c3].append((a, b))
    for t in users: c2[t] |= {a, b, c3}
kleft = [CPERP[t] - c2[t] for t in range(V)]
log('(b) THE CHAIN-AWARE KEPT: %d | the leftovers %d lines' % (
    len(kept), sum(len(lo) for lo in kleft)))
sload = Counter()
for t in range(V):
    for l in kleft[t]: sload[l] += 1
log('    the singleton loads: %s' % dict(sorted(Counter(sload.values()).items())))
ceil = Counter()
for l in range(V):
    us = [t for t in range(V) if l in kleft[t]]
    if us: ceil[9 - rank(us)] += 1
log('    the singleton ceilings: %s' % dict(sorted(ceil.items())))
Rk = len(kept) + sum(1 for lo in kleft if lo) + RET
log('(c) R = %d (R/v %.2f!!)' % (Rk, Rk / V))
# the price band at Rk!!
CST = 162
for nm, sh in [('D', {1: 0.262, 2: 0.571 / 2, 4: 0.048 / 4, 5: 0.119 / 5}),
               ('MX', {9: 1.0})]:
    climb = 10.0 * Rk + 2.0 * V * 9
    h = {k: int(v * climb) for k, v in sh.items()}
    h[9] = h.get(9, 0) + 18
    c = price(h, V, H, Rk)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        log('    %s at R %d: %+.2f%% vs the frontier' % (nm, Rk, 100 * (float(c[0]) / float(FC) - 1)))
json.dump({'kept22': [(sorted(p), sorted(u)) for p, u in pool], 'left22': [sorted(lo) for lo in left],
           'R22': R22, 'kept_chain': [(sorted(p), sorted(u)) for p, u in kept],
           'left_chain': [sorted(lo) for lo in kleft], 'Rk': Rk, 'partner': partner},
          open('ii19_nat58_assign.json', 'w'))
log('saved ii19_nat58_assign.json')
