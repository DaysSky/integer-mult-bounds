"""THE 2-CLASS BUILD STAGE 1 (ii19_nat53.py) — the economy + the chain-aware feasibility!!

THE TARGET: the Lorentzian frontier word — the 240-line 2-class at h=10 (the full II19
ambient!!), the economy R ~ 317 (the record's measured design (202 pieces / 12.6 users /
94 carriers / 18 retained!!)), the hist between the D (-14.2%) and the MX (+10.1%!!).
HERE: (1) the system (the 240 lines, the form, the perps!!); (2) the greedy economy
(the pair-intersection pieces (the record's (3,4)-class!!)); (3) THE CHAIN-AWARE
FEASIBILITY (the nat44-machinery adapted: the pair-orientation matching, the third-budgets,
the user-caps (the capacity law!!)); (4) the R + the honest price band.
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

# (1) THE SYSTEM: the 240 lines (the 120 E8 roots (the 2x-scaled (norm 4!!)) + the level!)
roots240 = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots240.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots240.add(tuple(Fraction(x, 2) for x in s))
assert len(roots240) == 240

def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

d8 = {}
for r in roots240:
    d8[canon(r)] = r          # one per +-pair -> 120!!
roots = sorted(d8.values())
assert len(roots) == 120
V = 240
# the lines: (alpha, 0, 0) and (alpha, 1, 0) (the 10-dim ambient; the form: a.b' + b.a'!!)
L = []
for c in (0, 1):
    for a in roots:
        L.append([Fraction(x) for x in a] + [Fraction(c), Fraction(0)])
H = 10
# the form matrix: I8 + the hyperbolic pair!!
FORM = [[Fraction(0)] * H for _ in range(H)]
for i in range(8): FORM[i][i] = Fraction(1)
FORM[8][9] = FORM[9][8] = Fraction(1)
def ip(x, y):
    return sum(x[i] * y[j] * FORM[i][j] for i in range(H) for j in range(H) if FORM[i][j])
G = [[ip(L[s], L[t]) for t in range(V)] for s in range(V)]
log('(1) THE SYSTEM: %d lines | the norms: %s' % (V, sorted(set(G[s][s] for s in range(V)))))
PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
log('    the perps: %s' % dict(sorted(Counter(len(p) for p in PERP).items())))
Linn = np.array([[float(x) for x in l] for l in L])
rank = lambda lines: int(np.linalg.matrix_rank(Linn[sorted(lines)])) if lines else 0

# (2) THE GREEDY ECONOMY (the record's (3,4)-class!!)
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
log('(2) THE ECONOMY (3,4): %d pieces (mean %.1f lines, %.1f users) | the leftovers %d lines' % (
    len(pool), sum(len(p) for p, u in pool) / max(1, len(pool)),
    sum(len(u) for p, u in pool) / max(1, len(pool)),
    sum(len(lo) for lo in left)))

# (3) THE CHAIN-AWARE FEASIBILITY (the nat44-machinery: the roles + the budgets!!)
partner = {}; third_users = defaultdict(set); pairs_of = defaultdict(list)
kept = []; kusers = []
CAP = 21
while True:
    best = None
    for b in range(V):
        for a in sorted(PERP[b]):
            if a >= b: continue
            if b in partner and partner[b] != a: continue
            users = [t for t in range(V) if a in PERP[t] and b in PERP[t]
                     and a not in covered[t] and b not in covered[t]]
            if len(users) < 4: continue
            if len(users) > CAP: users = sorted(users)[:CAP]
            common = None
            for t in users:
                unc = PERP[t] - covered[t]
                common = set(unc) if common is None else (common & unc)
            common -= {a, b}
            for c in sorted(common):
                if c in partner and any(partner[c] not in PERP[t] for t in users): continue
                nu = third_users[c] | set(users)
                if any(x not in PERP[u] for u in (third_users[c] - set(users)) for x in (a, b)): continue
                frung = {a, b, c} | {x for p in pairs_of[c] for x in p}
                if rank(nu) + rank(frung) > 9: continue
                saving = 3 * len(users) - (3 + len(users))
                if saving <= 0: continue
                if best is None or saving > best[0]:
                    best = (saving, a, b, c, users)
    if best is None: break
    saving, a, b, c, users = best
    kept.append((frozenset({a, b, c}), users))
    kusers.append(users)
    partner[b] = a
    third_users[c] |= set(users)
    pairs_of[c].append((a, b))
    for t in users: covered[t] |= {a, b, c}
log('(3) THE CHAIN-AWARE KEPT: %d pieces' % len(kept))
kleft = [PERP[t] - covered[t] for t in range(V)]
sload = Counter()
for t in range(V):
    for l in kleft[t]: sload[l] += 1
log('    the leftover loads: %s' % dict(sorted(Counter(sload.values()).items())))
ceil = Counter()
for l, us in [(l, [t for t in range(V) if l in kleft[t]]) for l in range(V)]:
    if us: ceil[9 - rank(us)] += 1
log('    the singleton ceilings: %s' % dict(sorted(ceil.items())))
nleft = sum(1 for lo in kleft if lo)
RET = 18
R = len(kept) + nleft + RET
log('(4) THE ECONOMY: %d pieces + %d carriers + %d retained = R %d (R/v %.2f!!)' % (
    len(kept), nleft, RET, R, R / V))
# the price band (the D..MX between!!)
CST = 162
climb = 10.0 * R + 2.0 * V * 9
for nm, sh in [('D', {1: 0.262, 2: 0.571 / 2, 4: 0.048 / 4, 5: 0.119 / 5}),
               ('OG', {9: 1.0 / 9 * 9}), ('MX', {9: 1.0})]:
    h = {k: int(v * climb) for k, v in sh.items()}
    h[9] = h.get(9, 0) + 18
    c = price(h, V, H, R)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        log('    %s at R %d: %+.2f%% vs the frontier' % (nm, R, 100 * (float(c[0]) / float(FC) - 1)))
json.dump({'kept': [(sorted(p), sorted(u)) for p, u in kept], 'partner': partner,
           'left': [sorted(lo) for lo in kleft], 'R': R},
          open('ii19_nat53_assign.json', 'w'))
log('saved ii19_nat53_assign.json')
