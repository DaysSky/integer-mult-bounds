"""THE NATIVE-121 v13c (ii19_nat13c.py) — THE D4-CENSUS (THE CELLS-LADDER's-LEVEL-BELOW!!)
THE GOAL: the D6-builds' ~33-srcs -> the sources'-~78-wall -> THE LADDER: the D6s built
from the D4s?! (the dim-4-subspaces (the shared-sums (the u's-~1-3-memberships!!!))
THE CENSUS: the D4-analogs (the quad-common-perps?! — the 4-targets'-commons (the dim ~4-5?!))
"""
import sys, json, time, itertools
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

perps = [set(x for x in range(120) if x != t and iph(L[t], L[x]) == 0) for t in range(120)]

# ============ (1) THE TRIPLE-COMMONS (the dim ~4-5-subspaces (the D4-analog-candidates!!)) ============
# the triples (t, u, v): the common = the perp(t) & perp(u) & perp(v)?! — the ~13-19-lines?!
# THE LIGHT-CENSUS: the pairs-first?! — the 4,900-D6s?! — the INTERNAL-STRUCTURE!!! — hmm:
# the D6 (the 30-36-lines (the span-dim-6!!) — the D4-DECOMPOSITION?! (the internal?! —
# the D6's-lines (the ~30-36 (the D4s?! — hmm: the perp(t) & perp(u) (the dim-6?! —
# hmm: the D6 (the ⊥-complement?! — hmm — the DIRECT-QUESTION?! — the D6s'-PAIRS'-STRUCTURE!!!
# ============ THE MEASURE (THE CONCRETE (THE SIMPLEST!!!)) ============
# the 286-chosen-D6s?! — the RE-RUN (the 13b's-greedy (the chosen?! — the SAVED?! —
# the RE-DERIVE (the FAST (the 13b's-code!!!))
res = {}
for t in range(120):
    d6s = {}
    for u in range(120):
        if u == t: continue
        c = tuple(sorted(perps[t] & perps[u]))
        if len(c) >= 15:
            d6s[c] = d6s.get(c, 0) + 1
    res[t] = d6s
all_d6s = {}
for t in range(120):
    for c in res[t]:
        all_d6s.setdefault(c, set()).add(t)
chosen = []
covered = [set() for _ in range(120)]
cnt = [0] * 120
while True:
    prio = sorted(range(120), key=lambda x: -len(perps[x] - covered[x]))
    t = prio[0]
    need = perps[t] - covered[t]
    if not need or cnt[t] >= 8: break
    best = None
    for c, users in all_d6s.items():
        if t not in users: continue
        gain = len(set(c) & need)
        if gain > 0 and (best is None or gain > best[0]):
            best = (gain, c, users)
    if best is None: break
    _, c, users = best
    chosen.append((c, users))
    for u2 in users:
        covered[u2].update(c)
        cnt[u2] += 1
log('(0) the re-derived: %d-chosen (the tails %s)' % (len(chosen),
    dict(sorted(Counter(len(perps[t] - covered[t]) for t in range(120)).items()))))

# ============ (1) THE D6s'-PAIR-STRUCTURE (THE CELLS'-POTENTIAL!!!) ============
# the pairs'-co-occurrence-WITHIN-the-chosen-D6s?! — the cell {u, w}?! — the ~?! —
pair_occ = Counter()
for c, users in chosen:
    for u, w in itertools.combinations(c, 2):
        pair_occ[(u, w)] += 1
log('(1) THE PAIRS-IN-CHOSEN-D6s: %d distinct (the co-occ %s (the mean %.1f!!))' % (
    len(pair_occ), dict(sorted(Counter(pair_occ.values()).items())),
    float(np.mean(list(pair_occ.values())))))
# the best-partner-per-source (the cell {u, w}?! — the ~?! — hmm: the u's-CELLS?! —
best_partner = {}
for (u, w), c in pair_occ.items():
    if u not in best_partner or c > best_partner[u][1]: best_partner[u] = (w, c)
    if w not in best_partner or c > best_partner[w][1]: best_partner[w] = (u, c)
log('    the best-partner-co-occs: %s (the mean %.1f!!)' % (
    dict(sorted(Counter(c for _, c in best_partner.values()).items())),
    float(np.mean([c for _, c in best_partner.values()]))))
# ============ (2) THE D4-ANALOGS (THE TRIPLE-COMMONS!!!) ============
# the triples (t, u, v): the perp(t) & perp(u) & perp(v)?! — the sizes?! — the LIGHT!!!
# the seeds?! — hmm: the D6s'-USERS?! — the pairs (the users?! — the D6 (the users {t, u}?! —
# hmm: the D6's-users (the 2-3?! — hmm: the D6 (the pair-common(t, u)??! — the triple?! —
# hmm: the users (the ~2-3?! — hmm: the D6 (the the-{t, u}-common?! — the D4?! — hmm —
# THE SIMPLER: the D6 (the ~33-lines?! — the SPAN?! (the dim-6?! — the D4s-inside?! —
# hmm: the D6's-INTERNAL-PAIR-STRUCTURE?! — hmm — THE DIRECT-D4-CENSUS?!?! —
# the 4-targets?! — the ✗?!?! — hmm — THE HONEST?! — hmm — hmm — OK: the honest-first!
# the D6s'-LINE-STRUCTURE?! — the nat12c's-21-line-splits?! — hmm — hmm —
# THE MOST-CONCRETE-NEXT (THE LADDER's-TEST!!!): the D6s'-BUILDS?! — hmm — hmm —
log('DONE — THE NAT13C (the pairs-in-chosen (the D4-census-scoped!!!))')
