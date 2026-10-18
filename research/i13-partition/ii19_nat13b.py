"""THE NATIVE-121 v13b (ii19_nat13b.py) — THE PER-TARGET D6-COVERAGE (THE SET-COVER-SCOPE!!)
THE MEASURE: the per-target: the DISTINCT-pair-commons (the D6s ⊆ perp(t)!!) -> the coverage
(the ~2-3-D6s-per-perp?! (the <= 8-pieces-per-target?!)) + the u-memberships (the <= ~7?!)
"""
import sys, json, time
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

perps = [set(x for x in range(120) if x != t and iph(L[t], L[x]) == 0) for t in range(120)]

# ============ (1) THE PER-TARGET D6-COVERAGE ============
# the t's-D6s: the pair-commons (t, u) for the ~119-u?! -> the DISTINCT?! -> the unions?!
res = {}
for t in range(120):
    d6s = {}
    for u in range(120):
        if u == t: continue
        c = tuple(sorted(perps[t] & perps[u]))
        if len(c) >= 15:
            d6s[c] = d6s.get(c, 0) + 1
    res[t] = d6s
sizes = [len(d) for d in res.values()]
log('(1) THE PER-TARGET DISTINCT-D6s: %s (the mean %.1f!!)' % (
    dict(sorted(Counter(sizes).items())), float(np.mean(sizes))))
# the COVERAGE (the 2-3-D6-unions?! — the per-target (the best-2 (the best-3?! — the MEASURE!!!
cov2 = []
cov3 = []
for t in range(120):
    d6s = sorted(res[t].keys(), key=lambda c: -len(c))
    u2 = set().union(*d6s[:2]) if len(d6s) >= 2 else set()
    u3 = set().union(*d6s[:3]) if len(d6s) >= 3 else set()
    cov2.append(len(u2 & perps[t]) / max(1, len(perps[t])))
    cov3.append(len(u3 & perps[t]) / max(1, len(perps[t])))
log('    the top-2-D6-coverage: %.3f (the min %.3f!!)' % (float(np.mean(cov2)), float(np.min(cov2))))
log('    the top-3-D6-coverage: %.3f (the min %.3f!!)' % (float(np.mean(cov3)), float(np.min(cov3))))
# the FULL-SET-COVER?! — the greedy (the per-target (the <= 8 (the D6s?! — the GLOBAL (the SHARED!!!
# the GLOBAL-GREEDY (the max-coverage (the <= 8-per-target!!!))
chosen = []
covered = [set() for _ in range(120)]
cnt = [0] * 120
all_d6s = {}
for t in range(120):
    for c in res[t]:
        all_d6s.setdefault(c, set()).add(t)
log('(2) THE GLOBAL-D6s: %d (the users %s)' % (len(all_d6s),
    dict(sorted(Counter(len(v) for v in all_d6s.values()).items()))))
while True:
    # the most-uncovered
    prio = sorted(range(120), key=lambda x: -len(perps[x] - covered[x]))
    t = prio[0]
    need = perps[t] - covered[t]
    if not need or cnt[t] >= 8: break
    best = None
    for c, users in all_d6s.items():
        if t not in users: continue
        gain = len(set(c) & need)
        # the constraints: the t's-count + the users'-counts!!!
        if gain > 0 and (best is None or gain > best[0]):
            best = (gain, c, users)
    if best is None: break
    _, c, users = best
    chosen.append((c, users))
    for u2 in users:
        covered[u2].update(c)
        cnt[u2] += 1
    if len(chosen) % 100 == 0:
        rem = sorted(len(perps[x] - covered[x]) for x in range(120))
        log('    %d chosen: the worst-remaining %d..' % (len(chosen), rem[-1]))
tails = [len(perps[t] - covered[t]) for t in range(120)]
log('(3) THE CHOSEN: %d | the per-target %s (the OVER-8: %d!!) | the tails %s (the mean %.1f!!)' % (
    len(chosen), dict(sorted(Counter(cnt).items())), sum(1 for x in cnt if x > 8),
    dict(sorted(Counter(tails).items())), float(np.mean(tails))))
src_mem = Counter()
for c, users in chosen:
    for x in c:
        src_mem[x] += 1
log('    the u-memberships: %s (the mean %.1f!!) | the OVER-8: %d/120' % (
    dict(sorted(Counter(src_mem.values()).items())), float(np.mean(list(src_mem.values()))),
    sum(1 for x in src_mem.values() if x > 8)))
log('DONE — THE NAT13B (the D6-set-cover!!!)')
