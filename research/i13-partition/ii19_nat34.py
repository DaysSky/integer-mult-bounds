"""STAGE A (ii19_nat34.py) — THE DELIVERY ALGEBRA, EXTRACTED FROM THE PROVEN WORD4 AND TRANSPLANTED.

THE WORD4 EXTRACTION (the exact, proven template):
  per target t: the line-content algebra of its delivery:
     scatter(t)  = XOR of the W-selected rets' A-final line-sets
     B-reads(t)  = XOR of the line-sets read by t's B target-gates (at read time)
  THE IDENTITY (measured here): scatter(t) ^ B-reads(t) ^ (the D line-part (expected 0: pre-A
  helpers carry self-bits only!!)) == ??? (perp(t)? {t}? the junk?) — MEASURED, not assumed.

THE NATIVE TRANSPLANT: the §1398 economy (101 pieces + 47 carriers + 9 gathers (the rank-9
perp-pattern decoder (nat30!!)) = R 157) with the nat33 map's verdict: ANY legal hist crosses
(A-shape +4.31%!!).  Here: construct + verify the native per-target balance (pure GF(2)):
     perp(t) (or the measured identity) == XOR(assigned pieces) ^ carrier_t ^ (the k=1-shared...)
  + the arrival law (the demand-reads vs 9R).
"""
import os, sys, json
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from mpmath import mp

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H, nreg = V, H, nreg
LM = (1 << V) - 1
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# the perps of the word4's 121-line system
G4 = [[sum(w['lines'][s][i] * w['form']['num'][i][j] * w['lines'][t][j]
            for i in range(H) for j in range(H) if w['form']['num'][i][j]) for t in range(V)] for s in range(V)]
PERP4 = [sum(1 << s for s in range(V) if s != t and G4[s][t] == 0) for t in range(V)]

# simulate: the A-final values, then the scatter + the B target-gates with read-time values
val = [1 << r for r in range(nreg)]
for F, d, srcs in w['D']:
    for s in srcs: val[d] ^= val[s]
Dline = [0] * V
for F, d, srcs in w['D']:
    if V <= d < 2 * V:
        for s in srcs: Dline[d - V] ^= (val[s] & LM)   # the D line-part (expected 0!!)
for F, d, srcs in w['A']:
    for s in srcs: val[d] ^= val[s]
Afinal = list(val)
scat = [0] * V
for t in range(V):
    for k in w['scatter'][t]:
        scat[t] ^= (Afinal[w['ret'][k]] & LM)
bread = [0] * V
nreads = Counter()
for F, d, srcs in w['B']:
    if V <= d < 2 * V:
        for s in srcs:
            bread[d - V] ^= (val[s] & LM)
            nreads[d - V] += 1
    for s in srcs: val[d] ^= val[s]
for t in range(V):
    tot = scat[t] ^ bread[t] ^ Dline[t]
log('THE WORD4 IDENTITY: tot == perp(t): %d/121 | tot == {t}: %d | tot == 0: %d' % (
    sum(tot == PERP4[t] for tot, t in zip([(scat[t] ^ bread[t] ^ Dline[t]) for t in range(V)], range(V))),
    sum((scat[t] ^ bread[t] ^ Dline[t]) == (1 << t) for t in range(V)),
    sum((scat[t] ^ bread[t] ^ Dline[t]) == 0 for t in range(V))))
tots = [scat[t] ^ bread[t] ^ Dline[t] for t in range(V)]
log('  the tot==perp count: %d/121 | the D line-part: %s' % (
    sum(tots[t] == PERP4[t] for t in range(V)), Counter(Dline).most_common(3)))
log('  the B-reads per target: %s | the scatter rows: %s' % (
    sorted(set(nreads.values())), sorted(set(len(w['scatter'][t]) for t in range(V)))))
log('  the per-target read line-set sizes: mean %.1f' % (
    sum(bin(bread[t]).count('1') for t in range(V)) / V))

# ============ THE NATIVE TRANSPLANT: THE PERP-DIRECT GREEDY (the self-contained balance!!) ============
# the reads must XOR to perp(t) (the word4 identity + the rank-9 perp-pattern decoder (nat30!!));
# the greedy runs on the PERP-SETS directly (the pieces = the subsets shared by >=2 targets).
import itertools
perps = [[s for s in range(V) if (PERP4[t] >> s) & 1] for t in range(V)]
pair_count = Counter()
pair_users = defaultdict(list)
for ti, pl in enumerate(perps):
    for a, b in itertools.combinations(sorted(pl), 2):
        pair_count[(a, b)] += 1
        pair_users[(a, b)].append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 2]
covered = [set() for _ in range(V)]
pool = []
pool_users = []
while True:
    best = None
    for (c, (a, b)) in top:
        users = [ti for ti in pair_users[(a, b)] if a not in covered[ti] and b not in covered[ti]]
        if len(users) < 2: continue
        common = None
        for ti in users:
            unc = set(perps[ti]) - covered[ti]
            common = unc if common is None else (common & unc)
        if common is None or len(common) < 2: continue
        piece = frozenset(common)
        real = [ti for ti in users if piece <= set(perps[ti]) - covered[ti]]
        if len(real) < 2: continue
        saving = len(piece) * len(real) - (len(piece) + len(real))
        if saving <= 0: continue
        if best is None or saving > best[0]:
            best = (saving, piece, real)
    if best is None or best[0] < 2: break
    _, piece, real = best
    pool.append(piece)
    pool_users.append(real)
    for ti in real:
        covered[ti] |= set(piece)
leftovers = [set(perps[ti]) - covered[ti] for ti in range(V)]
carriers = sum(1 for lo in leftovers if lo)
log('THE PERP-DIRECT GREEDY: pool %d (mean %.1f lines, mean %.1f users) | carriers %d | leftover lines %d'
    % (len(pool), sum(len(p) for p in pool) / max(1, len(pool)),
       sum(len(us) for us in pool_users) / max(1, len(pool)), carriers,
       sum(len(lo) for lo in leftovers)))
R_nat = len(pool) + carriers + 9
log('THE NATIVE R: %d + %d + 9 gathers = %d (R/v %.2f)' % (len(pool), carriers, R_nat, R_nat / V))

# the balance verification (exact GF(2) per target!!) + the arrival law
demand = 0
ok = 0
for t in range(V):
    x = 0
    for pi, us in enumerate(pool_users):
        if t in us:
            m = 0
            for s in pool[pi]: m |= (1 << s)
            x ^= m
            demand += 1
    if leftovers[t]:
        m = 0
        for s in leftovers[t]: m |= (1 << s)
        x ^= m
        demand += 1
    ok += (x == PERP4[t])
log('THE BALANCE: %d/121 targets exact | the demand-reads (pieces+carriers) %d vs 9R = %d: %s' % (
    ok, demand, 9 * R_nat, 'FITS' if demand <= 9 * R_nat else 'OVER'))

