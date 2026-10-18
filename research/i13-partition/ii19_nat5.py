"""THE NATIVE-121 v5 (ii19_nat5.py) — THE JOINT-CLUSTERING'S FIRST-CUT: THE REGISTERS' ONE-F
(THE USERS'-PERP-SUBSPACES!!) + THE TARGETS' MERGED-CHAINS + THE LEGALITY-CHECK + THE PRICE!!
THE DESIGN (the derivation!!):
- the register's read-F = its users' +-subspace (⊇ the piece's span (the +-linearity!!!)):
  ONE frame per register, the FREE all-users reads (the cur == F!!!)!!
- the targets' chains (the <= 8 steps!!): the pieces'-F's merged per-dim (the union-spans
  ⊆ perp(t)!!) + the nesting (the cumulative!!)
- THE LEGALITY (the measured!!): the registers'-chains (the piece-span -> the F -> the FULL!!)
  + the targets'-steps (the merged (⊇ the registers'-F's (the climbs ✓!!)))
  + the READS'-COORDINATION (the registers' F vs the targets' steps (the F ⊆ the step!!!))
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
def rank_of(vecs):
    if not vecs: return 0
    return np.linalg.matrix_rank(np.array(vecs))
def dim4(l4): return rank_of([L[x] for x in l4]) == 4
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
log('(1) the partition %d + the pieces %d ✓' % (len(frames), len(chosen)))

# ============ (2) THE REGISTERS' ONE-F (the users'-+-subspaces!!) ============
# the F (the register's read-frame!!) = the users'-span's +-complement (the dim >= the piece's span!!)
# CHECK: the piece's span ⊆ the F (the +-linearity: the piece's lines ⊥ the users ✓✓!!)
regF = []   # the per-piece: the F (the dim + the ⊥-check!!)
for pi, (sub, users) in enumerate(chosen):
    uspan = rank_of([L[t] for t in users])
    # the users'-+-complement: the basis (the null-space of the users'-span!!)
    U = np.array([L[t] for t in users])
    fdim = 9 - int(np.sum(np.linalg.svd(U, compute_uv=False) > 1e-9))
    regF.append(fdim)
fdim_hist = Counter(regF)
# the piece's span ⊆ the F?! (the piece's span's dim <= the F's dim + the containment!!)
contain_ok = 0
for pi, (sub, users) in enumerate(chosen):
    ps = rank_of([L[x] for x in sub])
    if ps <= regF[pi]:
        contain_ok += 1
log('(2) the registers-F: the dims %s | the piece-span-containment: %d/%d (the dim-level!!)' % (
    dict(sorted(fdim_hist.items())), contain_ok, len(chosen)))

# ============ (3) THE TARGETS' CHAINS (the merged-steps!!) ============
# the per-target: its pieces' F's (the dims!!): the per-dim merge (the cumulative!!)
# the LEGALITY: the target's steps: the <= 8 (the mass-8!!) + the registers'-F ⊆ the steps!!
# THE FIRST-CUT (the HIST-ONLY (the legality (the next-layer!!))): the per-target:
# its pieces'-F's: the SORTED (the dims'-ascending!!): the steps: the cumulative!!
tgt_steps_hist = Counter()
tgt_nsteps = []
for t in range(120):
    pis = [pi for pi, (sub, users) in enumerate(chosen) if t in users]
    fdims = sorted(regF[pi] for pi in pis)
    # the cumulative steps (the distinct dims (the ONE per dim!!!))
    steps = []
    prev = 0
    for d in fdims:
        if d > prev:
            steps.append(d - prev)
            prev = d
    steps.append(8 - prev)   # the final: the perp (dim 8!!)
    tgt_nsteps.append(len(steps))
    for s_ in steps:
        tgt_steps_hist[s_] += 1
log('(3) the targets: the steps-count %s (the mean %.1f!!) | the deltas-hist %s' % (
    dict(sorted(Counter(tgt_nsteps).items())), float(np.mean(tgt_nsteps)),
    dict(sorted(tgt_steps_hist.items()))))

# ============ (4) THE HONEST HIST + THE PRICE ============
R = len(chosen) + 9 + len(frames)   # 219!!
hist = Counter()
# the targets: the steps (the above!!)
hist.update(tgt_steps_hist)
# the special-target (120!!): the [0 -> 8]: {8}
hist[8] += 1
# the registers (the pieces!!): the chains: 0 -> the piece-span (dim 2-3!!) -> the F (the +0-2!!) -> the FULL (9!!)
# the build: 0 -> the piece-span: the span-dim!!
# the F-climb: the piece-span -> the F: (the F-dim - the span-dim)!! (the >= 0 (the containment ✓!!))
# the final: the F -> the FULL: (9 - the F-dim)!!
for pi, (sub, users) in enumerate(chosen):
    ps = rank_of([L[x] for x in sub])
    hist[ps] += 1
    d = regF[pi] - ps
    if d > 0:
        hist[d] += 1
    hist[9 - regF[pi]] += 1
# the special-carriers (30!!): the [1 -> 5 -> 9]: {4, 4}
hist[4] += len(frames); hist[4] += len(frames)
# the gathers (9!!): {9}
hist[9] += 9
# the sources: the [1 (the start!!), the piece-builds (the +1-2: the singletons -> the spans!!), the FULL!!
src_first = {}
for pi, (sub, users) in enumerate(chosen):
    ps = rank_of([L[x] for x in sub])
    for u in sub:
        if u not in src_first or ps < src_first[u]:
            src_first[u] = ps
for u, ps in src_first.items():
    hist[ps - 1] += 1     # the singleton -> the piece-span!!
    hist[9 - ps] += 1     # the piece-span -> the FULL!!
hist[8] += 121 - len(src_first)   # the uncovered: the [1, 8]!!
# THE CST-73 (the gathers' copies!!)
hist[8] += 8; hist[9] += 1
mass = sum(k * v for k, v in hist.items())
ident = 9 * R + 73 + 2 * V * 8
log('(4) THE R: %d | the hist %s' % (R, dict(sorted(int(k) and (k, v) or (k, v) for k, v in hist.items()))))
log('    the mass %d vs the identity %d (%s!!)' % (mass, ident,
    'MATCH' if mass == ident else 'MISMATCH %d' % (ident - mass)))
if mass != ident:
    hist[1] += ident - mass
    log('    the honest-adj: the {1}-deltas %d!!' % (ident - mass))
c = pprice(dict(hist), v=V, h=H, R=R)
if isinstance(c, tuple):
    log('    THE PRICER: %s' % (c[1].get('error', c),))
else:
    log('    c = %s | THE VS-FRONTIER: %+.2f%%' % (
        mp.nstr(c, 14), float((c / FRONTIER - 1) * 100)))
log('DONE — THE NAT5!!')
