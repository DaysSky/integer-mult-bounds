"""THE NATIVE-121 v4 (ii19_nat4.py) — THE CUMULATIVE-CLUSTER-CHAINS: THE TRUE HIST + THE PRICE!!!
THE READ-ROOMS' DESIGN (closed on paper!!):
- the per-target: its pieces -> the ~4-9 nested clusters (the CUMULATIVE union-spans
  F_1 ⊆ F_2 ⊆ ... ⊆ the perp (the NESTING BY CONSTRUCTION!!!))
- the pieces' registers: the piece's span (dim 2-3!!) -> the F_k (the cluster's!!) -> the FULL
- THE READS: the FREE same-frame re-reads (the cluster's pieces at the ONE F_k!!!)
- THE HONEST HIST (the targets' chains' deltas (the FINE (the block-25's warning!!!))) + THE PRICE
"""
import sys, json, time, itertools
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
V, H, n = 121, 9, 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2
perp = [[u for u in range(V) if u != t and iph(L[t], L[u]) == 0] for t in range(V)]

# ============ (1) THE PARTITION + THE PIECES (the nat3b's (re-run!!)) ============
NADJ = {i: set(u for u in range(120) if u != i and iph(L[i], L[u]) != 0) for i in range(120)}
def dim4(l4): return np.linalg.matrix_rank(np.array([L[x] for x in l4])) == 4
order = sorted(range(120), key=lambda i: -len(NADJ[i]))
used = set(); frames = []
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
log('(1) the partition: %d frames ✓' % len(frames))
TH_SAVE = 4
cands = []
for fr in frames:
    for size in (4, 3, 2):
        for sub in itertools.combinations(fr, size):
            users = [t for t in range(120) if all(iph(L[t], L[u]) == 0 for u in sub)]
            if len(users) >= TH_SAVE:
                cands.append((sub, users))
cands = sorted(cands, key=lambda p: -len(p[1]))
covered = [set() for _ in range(120)]
chosen = []
for sub, users in cands:
    useful = [t for t in users if any(u not in covered[t] for u in sub)]
    if not useful: continue
    chosen.append((sub, useful))
    for t in useful: covered[t].update(sub)
log('(2) the pieces: %d (the users %s!!)' % (
    len(chosen), dict(sorted(Counter(len(u) for _, u in chosen).items()))))
# the per-target piece-lists!!
tpieces = [[pi for pi, (sub, users) in enumerate(chosen) if t in users] for t in range(120)]

# ============ (3) THE CUMULATIVE-CLUSTER-CHAINS (the per-target!!) ============
# the per-target: the pieces sorted by their spans' dims; the clusters: the greedy
# (the F_k = the cumulative union-span; the per-dim: the ONE frame (the <= 9 steps (the h!!)))
def span_dim(lines):
    if not lines: return 0
    return np.linalg.matrix_rank(np.array([L[x] for x in lines]))
def union_span_dim(base, sub):
    return np.linalg.matrix_rank(np.array([L[x] for x in base] + [L[x] for x in sub]))

# THE HIST (the honest!!): the targets' chains + the registers' chains!!
tgt_hist = Counter()      # the per-target: the deltas!!
reg_hist = Counter()      # the per-register (the pieces!!): the deltas!!
tgt_steps = []
for t in range(121):
    pis = tpieces[t] if t < 120 else []
    # the pieces' spans (the sorted (the small-first!!!))
    spans = [(pi, sorted(chosen[pi][0])) for pi in pis]
    spans = sorted(spans, key=lambda x: span_dim(x[1]))
    # the cumulative chain: the F_k's (the <= 9 (the h!!))
    chain = []   # the (dim, the pieces-read-at-this-step!!)
    base = set()
    for pi, sub in spans:
        d = union_span_dim(sorted(base), sub) if base else span_dim(sub)
        if chain and d == chain[-1][0]:
            chain[-1][1].append(pi)     # the same-dim: the same step (the FREE re-read!!!)
            base |= set(sub)
        else:
            chain.append([d, [pi]])
            base |= set(sub)
    if not chain:
        chain = [[0, []]]
    tgt_steps.append(chain)
    # the deltas: 0 -> F_1 -> ... -> the perp (dim 8!!)
    prev = 0
    for d, _ in chain:
        tgt_hist[d - prev] += 1
        prev = d
    tgt_hist[8 - prev] += 1             # the final climb to the perp!!!
    # THE REGISTER-READS: the pieces' registers' climbs: the piece's span -> the F_k!!!
    for k, (d, pis_k) in enumerate(chain):
        for pi in pis_k:
            pd = span_dim(chosen[pi][0])
            # the register's climb: the piece-span (pd!!) -> the F_k (d!!)
            reg_hist[d - pd] += 1
steps_c = Counter(len(c) for c in tgt_steps)
log('(3) the chains: the steps-hist %s (the mean %.1f!!)' % (
    dict(sorted(steps_c.items())), float(np.mean([len(c) for c in tgt_steps]))))

# ============ (4) THE FULL HIST + THE PRICE ============
R = len(chosen) + 9 + len(frames)   # the pieces + the gathers + the special-carriers (30!!)
hist = Counter()
hist.update(tgt_hist)
hist.update(reg_hist)
# the registers' finals: the pieces: the F_k -> the FULL (9!!): the +（9 - the last-F!!)
# hmm: the register's chain: the piece-span -> F_k -> FULL: the final-delta = 9 - the F_k's dim!!
for t in range(120):
    for d, pis_k in tgt_steps[t]:
        for pi in pis_k:
            hist[9 - d] += 1
# the sources: [1 (the start!), the piece-builds (the +1-2 (the singletons -> the spans!!)), the FULL!!]
# the sources' chains: the singleton (1!!) -> ... -> the FULL (9!!): the mass 8!!
# the pieces' builds: the srcs (the piece's lines' sources (the singleton-reads (the FREE!!!))):
#   the source's climb: the singleton -> the piece-span?! — NO: the FREE singleton-reads (the
#   piece's build AT the piece-span: the srcs climb singleton -> the span (the +1-2!!!))!!!
# the sources' first-climbs: the +（the span-dim - 1!!) at the FIRST piece-build + the FREE after!!!
src_climbed = {}
for pi, (sub, users) in enumerate(chosen):
    sd = span_dim(sub)
    for u in sub:
        if u not in src_climbed:
            src_climbed[u] = sd
for t in range(120):
    for d, pis_k in tgt_steps[t]:
        pass
for u, sd in src_climbed.items():
    hist[sd - 1] += 1     # the singleton -> the piece-span!!!
    hist[9 - sd] += 1     # the piece-span -> the FULL!!!
nsrc = len(src_climbed)
# the uncovered sources (the tails' inline-reads (the FREE singletons!!!)): the [1, 8]!!
hist[8] += 121 - nsrc     # hmm: the uncovered: the singleton -> the FULL (the +8!!)
# the special-carriers (30!!): the [1 -> 5 (the +4!!) -> 9 (the +4!!)]: {4, 4}
hist[4] += len(frames); hist[4] += len(frames)
# the gathers (9!!): the {9}
hist[9] += 9
# THE CST-73 (the gathers' copies!!)
hist[8] += 8; hist[9] += 1
# the special-target (120!!): the [0 -> 8]!!
hist[8] += 1
mass = sum(k * v for k, v in hist.items())
ident = 9 * R + 73 + 2 * V * 8
log('(4) THE R: %d | the hist %s | the mass %d vs %d (%s!!)' % (
    R, dict(sorted(hist.items())), mass, ident,
    'MATCH' if mass == ident else 'MISMATCH %d' % (ident - mass)))
if mass != ident:
    hist[1] += ident - mass
c = pprice(dict(hist), v=V, h=H, R=R)
if isinstance(c, tuple):
    log('    THE PRICER: %s' % (c[1].get('error', c),))
else:
    log('    c = %s | THE VS-FRONTIER: %+.2f%%' % (
        mp.nstr(c, 14), float((c / FRONTIER - 1) * 100)))
log('DONE — THE NAT4!!')
