"""THE NATIVE-121 v10 (ii19_nat10.py) — THE BIG-PIECES (the ext6's carrier-scale!!) + THE BUDGETS
THE DESIGN-CHANGE (the measured-lesson (the ext6's-own!!)): the pieces at the ~8-12-LINE scale
(the unions of 2-3 partition-frames!!) -> the users (the ~1-6!!) -> THE ONE-SHARED-M-PER-PIECE
(the perp(span(users)) (the >= the piece-span (the perp-reversal (the ALWAYS!!)))) -> the ONE-CLIMB
(the reads (the FREE (the same-M!!!))); the targets: the ~6-8-pieces-per-target (the <= 8-STEPS
(the FITS!!!)) — THE BUDGETS (the measured (the honest!!!))
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

# ============ (0) THE SHARED-MACHINERY (the partition!!) ============
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
def perp_basis(tset):
    U = np.array([L[t] for t in tset])
    _, s, Vt = np.linalg.svd(U)
    fdim = 9 - int(np.sum(s > 1e-9))
    return Vt[9 - fdim:].copy() if fdim > 0 else np.zeros((0, 9))
def span_contains(B, v):
    if len(B) == 0: return False
    A = np.array(B)
    sol, _, _, _ = np.linalg.lstsq(A.T, v, rcond=None)
    return np.allclose(A.T @ sol, v, atol=1e-8)
def sub_leq(B1, B2):
    return all(span_contains(B2, v) for v in B1)

# ============ (1) THE BIG-PIECES (the unions-of-2-3-partition-frames!!!) ============
# THE CANDIDATES: the unions of 2-3 partition-frames (the 8-12-lines (the users (the
# perpendicular-to-ALL (the ~1-6?!?! (the BIG-pieces (the FEW-users!!!))))) — the greedy:
# the per-target-coverage (the ~6-8-pieces (the <= 8-STEPS!!!)))
TH_USERS = 6    # the ext6's carrier-scale (the <= 6 users!!!)
cands = []
for k in (3, 2):
    for combo in itertools.combinations(range(30), k):
        sub = tuple(sorted(set().union(*[set(frames[i]) for i in combo])))
        if len(sub) < 8 or len(sub) > 12: continue
        if rank_of([L[x] for x in sub]) > 9: continue
        users = [t for t in range(120) if all(iph(L[t], L[u]) == 0 for u in sub)]
        if 2 <= len(users) <= TH_USERS:
            cands.append((sub, users))
cands = sorted(cands, key=lambda p: (-len(p[0]), -len(p[1])))
log('(1) the big-piece-candidates: %d (the sizes %s)' % (
    len(cands), dict(sorted(Counter(len(s) for s, _ in cands).items()))))
# THE GREEDY-COVERAGE (the per-target (the ~6-8-pieces (the <= 8!!!)))
covered = [set() for _ in range(120)]
chosen = []
for sub, users in cands:
    useful = [t for t in users if any(u not in covered[t] for u in sub)]
    if not useful: continue
    chosen.append((sub, useful))
    for t in useful: covered[t].update(sub)
# the leftover-lines (the tails?!)
tails = [set(u for u in range(120) if iph(L[t], L[u]) == 0) - covered[t] for t in range(120)]
tail_sizes = sorted(len(tl) for tl in tails)
# remove the target-itself from its tail (the e_t-self-delivery (the scatter!!!)
for t in range(120):
    tails[t].discard(t)
log('    the big-pieces: %d (the users %s (the mean %.1f!!))' % (
    len(chosen), dict(sorted(Counter(len(u) for _, u in chosen).items())),
    float(np.mean([len(u) for _, u in chosen]))))
log('    the per-target-pieces: %s (the mean %.1f!!) | the OVER-8: %d/120' % (
    dict(sorted(Counter(sum(1 for s, us in chosen if t in us) for t in range(120)).items())),
    float(np.mean([sum(1 for s, us in chosen if t in us) for t in range(120)])),
    sum(1 for t in range(120) if sum(1 for s, us in chosen if t in us) > 8)))
log('    the tails: %s (the mean %.1f!!)' % (
    dict(sorted(Counter(len(tl) for tl in tails).items())), float(np.mean([len(tl) for tl in tails]))))

# ============ (2) THE USERS-SHARED-M's (the ONE-per-piece (the perp-reversal!!!)) ============
Ms = []
for pi, (sub, users) in enumerate(chosen):
    B = perp_basis(users)
    piece_B = [L[u] for u in sub]
    ok = sub_leq(piece_B, B)   # the piece-span ⊆ M (the perp-reversal: users ⊥ piece-lines!!)
    Ms.append((B, ok))
okc = sum(1 for _, ok in Ms if ok)
log('(2) THE PIECE-SPANS ⊆ THE USERS-M: %d/%d (the M-dims %s!!)' % (
    okc, len(chosen), dict(sorted(Counter(len(B) for B, _ in Ms).items()))))

# ============ (3) THE TARGETS-CHAINS (the per-dim-collisions (the honest-measure!!!)) ============
# the t's pieces'-M's (the DISTINCT (the dims (the per-dim (the ONE?!?! — the honest!!!))))
t_coll = 0
t_dims = []
for t in range(120):
    dims = {}
    for pi, (sub, users) in enumerate(chosen):
        if t in users:
            B, ok = Ms[pi]
            d = len(B)
            dims.setdefault(d, 0)
            dims[d] += 1
    t_dims.append(len(dims))
    if any(c > 1 for c in dims.values()):
        t_coll += 1
log('(3) THE TARGETS-DIM-LEVELS: %s (the mean %.1f!!) | the PER-DIM-COLLISIONS: %d/120' % (
    dict(sorted(Counter(t_dims).items())), float(np.mean(t_dims)), t_coll))
log('DONE — THE NAT10 (the big-pieces-budgets!!!)')
