"""THE 2-CLASS BUILD STAGE 7 (ii19_nat60.py) — the carriers' feasibility census!!

THE CARRIERS (the leftover assemblers (the per-target!!)): their builds = the running-sums
over the leftover lines at the sources' rungs (the cells (the pair-partners!!)) — THE WALL
(the 121's lesson!!): the source's cell-partner must be C= the perps of ALL the carrier-
targets reading that source!!  HERE: (1) nat56's leftovers (the (3,4)-economy!!); (2) the
per-source carrier-target sets; (3) THE PARTNER-BUDGETS: the candidate partners C= the
targets (the C=perp counts!!); (4) THE VERDICT: does the partner-assignment exist (the
bipartite feasibility (the Hall-ish check!!))?!
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
CPERP = [set(s for s in range(V) if CLS[s] == CLS[t] and s != t and G[s][t] == 0) for t in range(V)]

D56 = json.load(open('ii19_nat56_delivery.json', 'rt'))
left = [set(lo) for lo in D56['left']]
log('(1) THE LEFTOVERS (the (3,4)-economy!!): %d lines over %d targets (mean %.1f!!)' % (
    sum(len(lo) for lo in left), sum(1 for lo in left if lo),
    sum(len(lo) for lo in left) / max(1, sum(1 for lo in left if lo))))
# (2) the per-source carrier-target sets!!
src_targets = defaultdict(set)
for t in range(V):
    for l in left[t]:
        src_targets[l].add(t)
log('(2) THE CARRIER-DUTY LOADS: %s' % dict(sorted(Counter(len(v) for v in src_targets.values()).items())))
# (3) THE PARTNER-BUDGETS: for each source l: the candidates m C= CPERP of ALL its targets!!
# (the honest check: the SAME-CLASS partners (the cell = the (l, m)-pair (the same class!!))!!)
cand_counts = []
infeasible = []
for l, ts in src_targets.items():
    cands = set(m for m in CPERP[l] if all(m in CPERP[t] for t in ts))
    cand_counts.append(len(cands))
    if not cands:
        infeasible.append((l, sorted(ts)))
log('(3) THE PARTNER CANDIDATES per source: %s' % dict(sorted(Counter(cand_counts).items())))
log('    THE INFEASIBLE SOURCES (no partner C= all the targets!!): %d' % len(infeasible))
if infeasible:
    log('    the first: %s' % infeasible[:5])
# (4) THE MATCHING-FEASIBILITY (the Hall-ish: the partners distinct per source?!)
# (the cells: the (l, m)-pairs: m shared across sources?! THE CELL = ONE PAIR PER SOURCE:
# the partner m serves as l's cell — m can be the partner of ONE source (the matching!!)!!)
# THE HONEST CHECK: the bipartite matching (source -> candidate partner!!)!!
match = {}
used = set()
def try_match(l, cands, depth=0):
    for m in sorted(cands):
        if m in used: continue
        used.add(m); match[l] = m
        return True
    return False
ok_all = True
for l in sorted(src_targets):
    cands = set(m for m in CPERP[l] if all(m in CPERP[t] for t in src_targets[l]))
    if not try_match(l, cands):
        ok_all = False
        log('    THE MATCHING FAILS at source %d!!' % l)
        break
log('(4) THE GREEDY MATCHING: %s (%d sources matched!!)' % ('OK' if ok_all else 'FAILED', len(match)))
json.dump({'src_targets': {str(k): sorted(v) for k, v in src_targets.items()},
           'match': {str(k): v for k, v in match.items()},
           'infeasible': infeasible},
          open('ii19_nat60_carriers.json', 'w'))
log('saved ii19_nat60_carriers.json')
