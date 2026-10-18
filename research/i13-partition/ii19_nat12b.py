"""THE NATIVE-121 v12b (ii19_nat12b.py) — THE FULL-WORD BUILD (THE ACTUAL FRONTIER WORD!!)
THE DESIGN: THE FULL CATALOG of the 8-12-line pieces (the partition-frame-unions (the users
(the <= 8 (THE CARRIER-SCALE (THE ONLY-MEASURED-LEGAL!!!)))) + THE SET-COVER (the perps
(the <= 8-pieces-per-target!!!)) + the budgets (the sources'-memberships + the dim-collisions)
+ (IF-FIT) THE GATES + THE REPLAY + THE GCHECK!!!
"""
import sys, json, time, itertools
from collections import Counter
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
V, H, n = 121, 9, 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

perps = [set(u for u in range(120) if u != t and iph(L[t], L[u]) == 0) for t in range(120)]

# ============ (0) THE PARTITION (the shared-machinery!!) ============
NADJ = {i: set(u for u in range(120) if u != i and iph(L[i], L[u]) != 0) for i in range(120)}
def rank_of(vecs):
    if not vecs: return 0
    return np.linalg.matrix_rank(np.array(vecs))
order = sorted(range(120), key=lambda i: -len(NADJ[i]))
used = set(); frames = []
def dim4(l4): return rank_of([L[x] for x in l4]) == 4
def rec():
    if len(frames) == 30: return len(used) == 120
    seed = next((o for o in order if o not in used), None)
    if seed is None: return len(used) == 120
    for trio in itertools.combinations(sorted(NADJ[seed]), 3):
        if any(u in used for u in trio): continue
        if any(b not in NADJ[a] for a, b in itertools.combinations(trio, 2)): continue
        l4 = (seed,) + trio
        if not dim4(l4): continue
        used.update(l4); frames.append(l4)
        if rec(): return True
        frames.pop(); used.difference_update(l4)
    return False
assert rec(), 'the partition!!'
log('(0) the partition %d OK' % len(frames))

# ============ (1) THE FULL CATALOG (the 8-12-line pieces (the <= 8 users!!!)) ============
catalog = []
for k in (2, 3):
    for combo in itertools.combinations(range(30), k):
        sub = tuple(sorted(set().union(*[set(frames[i]) for i in combo])))
        if len(sub) < 8 or len(sub) > 12: continue
        if rank_of([L[x] for x in sub]) > 9: continue
        users = [t for t in range(120) if all(iph(L[t], L[u]) == 0 for u in sub)]
        if 1 <= len(users) <= 8:
            catalog.append((sub, users))
log('(1) THE FULL CATALOG: %d pieces (the sizes %s (the users %s (the mean %.1f!!)))' % (
    len(catalog), dict(sorted(Counter(len(s) for s, _ in catalog).items())),
    dict(sorted(Counter(len(u) for _, u in catalog).items())),
    float(np.mean([len(u) for _, u in catalog]))))

# ============ (2) THE SET-COVER (the perps (the <= 8-pieces-per-target!!!)) ============
# the greedy (the max-new-coverage-first (the per-target-priority (the UNDER-COVERED-FIRST!!!)))
# the pre-pass: the per-target-the-CANDIDATE-pieces (the piece's-lines ∩ the t's-perp!!!
cand_by_t = [[] for _ in range(120)]
for pi, (sub, users) in enumerate(catalog):
    for t in users:
        cand_by_t[t].append(pi)
log('(2) THE SET-COVER: the candidate-pieces-per-target: %s (the mean %.1f!!)' % (
    dict(sorted(Counter(len(c) for c in cand_by_t).items())),
    float(np.mean([len(c) for c in cand_by_t]))))
chosen = []
covered = [set() for _ in range(120)]
t_pieces = [0] * 120
# THE GREEDY-ROUNDS (the until-the-full-coverage (the <= 8-per-target!!!))
while True:
    # the most-uncovered-target (the priority!!!)
    prio = sorted(range(120), key=lambda t: -len(perps[t] - covered[t]))
    t = prio[0]
    need = perps[t] - covered[t]
    if not need:
        break
    # the best-piece (the max-coverage-of-the-need!!!)
    best = None
    for pi in cand_by_t[t]:
        sub, users = catalog[pi]
        gain = len(set(sub) & need)
        if gain > 0 and (best is None or gain > best[0]):
            best = (gain, pi)
    if best is None:
        log('    THE STUCK: t=%d the need %d (NO piece!!)' % (t, len(need)))
        break
    pi = best[1]
    sub, users = catalog[pi]
    chosen.append((sub, users))
    for u2 in users:
        covered[u2].update(sub)
        t_pieces[u2] += 1
    if len(chosen) % 50 == 0:
        rem = sorted(len(perps[x] - covered[x]) for x in range(120))
        log('    %d pieces: the remaining %s..' % (len(chosen), rem[-5:]))
tail_sizes = [len(perps[t] - covered[t]) for t in range(120)]
log('    THE CHOSEN: %d pieces | the tails %s (the mean %.1f!!) | the per-target %s (the mean %.1f, the OVER-8: %d!!)' % (
    len(chosen), dict(sorted(Counter(tail_sizes).items())), float(np.mean(tail_sizes)),
    dict(sorted(Counter(t_pieces).items())), float(np.mean(t_pieces)),
    sum(1 for x in t_pieces if x > 8)))
# the sources'-memberships
src_mem = Counter()
for sub, users in chosen:
    for x in sub:
        src_mem[x] += 1
log('    the sources-memberships: %s (the mean %.1f!!) | the OVER-7: %d/120' % (
    dict(sorted(Counter(src_mem.values()).items())), float(np.mean(list(src_mem.values()))),
    sum(1 for x in src_mem.values() if x > 7)))
log('DONE — THE NAT12B (the set-cover!!!)')
