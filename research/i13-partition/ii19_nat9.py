"""THE NATIVE-121 v9 (ii19_nat9.py) — THE REGISTER-LOCAL SUPER-CHAINS + THE HONEST BUDGETS
THE DESIGN: per-register: its OWN users (the ~6-36) as the NESTED partition (G_1 > G_2 > ...):
the M(G) = the perp(span(G)) — NESTED ALWAYS (the perp-reversal: G_a supset G_b -> M(G_a) subset M(G_b)!!)
THE CONSTRUCTION: the DIVISIVE (the users'-splits (the co-read-pairs-within (the shared-pieces!!!)))
THE BUDGETS: the registers-chains (the <= ~7-slots (the mass-9!!)) + the targets-steps
(the DISTINCT-M's (the <= 8?!?! (the honest-MEASURE (the merges'-cost (the NEXT!!!))))
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

# ============ (0) THE SHARED-MACHINERY (the nat5/6/7/8's!!) ============
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
log('(0) the partition %d + the pieces %d OK' % (len(frames), len(chosen)))
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

# ============ (1) THE REGISTER-LOCAL SUPER-CHAINS (the DIVISIVE (the co-read-within!!)) ============
# the per-register: the users (~6-36): the NESTED partition (the ~4-5 levels):
# G_1 = the ALL (the M = the F (dim-3!!)); the splits (the co-read-pairs (the within-U!!!)):
# the SPLIT-CRITERION: the users'-subsets (the OWN-co-structure (the shared-pieces-within!!))
# THE SIMPLEST: the RANDOM-BALANCED (the ~5-6-users-per-level (the nested-prefix?!?! — hmm:
# the NESTED-CHAIN (the G_1 > G_2 > ... (the LINEAR (the nested-prefix (the sorted-users?!?!)))
# — hmm: the LINEAR-chain (the G_k (the LAST (the ~5-users (the M (the dim ~7-8?!?! (the ⊥(span(5))
# (the ~dim-4-5?!?! — hmm: the 5-users (the span (the ~5-dim (the M (the dim ~4?!?! — hmm: the
# ⊥(span(5-targets)): the span (the ~5 (the M (the ~4?!?! — hmm: the 9 − 5 = 4 (the ✓ (the dim-4!!)))
# — the chain: the G_1 (the ~24 (the M (the dim-3 (the F!!))) -> G_2 (the ~18?! (the M (dim ~3-4)))
# -> ... -> G_k (the ~5 (the M (the dim-4?!?! — hmm: the SLOW-ASCENT (the ~+0-1-per-level (the ~5-6
# levels (the ~+3-4-total?! (the ✗ (the M's-dims (the ~3-4?!?! (the reads (the dim-3-4?!?! — the
# targets'-perp-finals (the dim-8 (the chains (the ✓ (the fine!!!))) — hmm: the reads at the dim-3-4-M's
# (the targets'-steps (the dim-3-4?!?! — hmm — the ≥ 15-20-M's?!?! — the honest-measure (the below!!!)
rng = np.random.RandomState(77)
reg_chains = []
reg_slots = []
for pi, (sub, users) in enumerate(chosen):
    U = list(users)
    # the nested-chain: the prefix-removal (the ~5-6-per-level (the co-read-sorted (the
    # shared-pieces (the pairs-within (the greediest-first!!!)))
    # the sort: the users (the shared-pieces-within-U (the degree!!!))
    deg = {}
    for t in U:
        deg[t] = sum(1 for u2 in U if u2 != t and
                     sum(1 for pi2, (s2, us2) in enumerate(chosen) if t in us2 and u2 in us2) >= 3)
    U.sort(key=lambda t: -deg[t])
    # the nested-prefixes (the ~5-6-per-level!!)
    k = max(2, min(6, len(U) // 5 + 1))
    bounds = sorted(set(int(round(len(U) * f)) for f in np.linspace(1.0, 0.2, k)))
    bounds = [b for b in bounds if b >= 2]
    sets_chain = []
    prev = len(U)
    for b in bounds:
        if b < prev:
            sets_chain.append(sorted(U[:b]))
            prev = b
    if not sets_chain:
        sets_chain = [sorted(U)]
    # the M's (the perp-bases (the ASCENDING-dims (the perp-reversal ✓✓✓!!!)))
    Ms = [perp_basis(sc) for sc in sets_chain]
    # the NESTED-CHECK (the ALWAYS?! (the honest-verify!!!))
    ok = all(sub_leq(Ms[i], Ms[i + 1]) for i in range(len(Ms) - 1))
    # the reads: the per-user (the DEEPEST-level (the t's-membership-prefix?!?!))
    # the user t (the position p (the U-sorted (the deepest-set (the U[:b] (the t's-index < b
    # (the DEEPEST (the smallest-b (the t ∈ the set!!!))))) — the read-M (the M (the level!!!
    read_level = {}
    for t in U:
        p = U.index(t)
        best = len(sets_chain) - 1
        for li in range(len(sets_chain)):
            if p < bounds[li]:
                best = li
                break
        read_level[t] = best
    reg_chains.append((ok, sets_chain, Ms, read_level))
    reg_slots.append(len(sets_chain) + 2)
okc = sum(1 for ok, _, _, _ in reg_chains if ok)
log('(1) the chains: the NESTED-OK %d/%d | the slots (the chain-lengths %s (the mean %.1f!!))' % (
    okc, len(chosen), dict(sorted(Counter(reg_slots).items())), float(np.mean(reg_slots))))

# ============ (2) THE TARGETS'-STEPS (the HONEST-MEASURE (the DISTINCT-M's!!!)) ============
# the t's registers'-read-M's (the DISTINCT?!?! (the <= 8?!?! — the honest!!!
t_steps = []
t_dimcoll = 0
for t in range(120):
    ms = set()
    dims = set()
    for pi, (sub, users) in enumerate(chosen):
        if t in users:
            ok, sets_chain, Ms, read_level = reg_chains[pi]
            lev = read_level[t]
            ms.add((pi, lev))
            dims.add(len(Ms[lev]))
    t_steps.append(len(ms))
    if len(dims) < len(ms):
        t_dimcoll += 1
log('(2) THE TARGETS-STEPS (the DISTINCT reg-level Ms!!): %s (the mean %.1f!!) | the OVER-8: %d/120 | the DIM-COLLISIONS: %d/120' % (
    dict(sorted(Counter(t_steps).items())), float(np.mean(t_steps)),
    sum(1 for s in t_steps if s > 8), t_dimcoll))
log('DONE — THE NAT9 (the budgets-honest!!!)')
