"""THE NATIVE-121 v7 (ii19_nat7.py) — THE GLOBAL-M-POOL: THE GREEDY CO-READ CLUSTERS +
THE BUDGETS (the registers-chains (the <= ~7!!) + the targets-steps (the <= 8!!))
THE DESIGN: the shared read-frames (the M-pool): the co-read clusters (the maximal target-groups
with the common-perp-subspaces (the M (⊆ every member's perp!!) ⊇ the cluster's registers'-F's!!)
+ the NESTED (the ⊃-clusters (the perp-reversal!!!)) — THE REGISTERS'-chains: the F -> the pool's
M's (the ascending!!) — THE TARGETS'-steps: the pool-members (the per-dim-merged (the ONE!!!))
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

# ============ (1) THE PARTITION + THE PIECES + THE REGISTERS'-F (the nat5/6's!!) ============
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
regF_basis = []
for sub, users in chosen:
    U = np.array([L[t] for t in users])
    _, s, Vt = np.linalg.svd(U)
    fdim = 9 - int(np.sum(s > 1e-9))
    regF_basis.append(Vt[9 - fdim:].copy() if fdim > 0 else np.zeros((0, 9)))
log('(1) the partition %d + the pieces %d + the Fs OK' % (len(frames), len(chosen)))

# ============ (2) THE GLOBAL-M-POOL (the greedy co-read clusters (the ⊥-nested!!)) ============
# THE CANDIDATE-M's: the targets'-clusters' common-perp-subspaces (the intersections!!)
# THE FIRST-CUT: the R420-STYLE LADDER: the perps (dim-8!!) + the pair-intersections (dim ~7!!)
# + the quad-clusters (dim ~6!!) — the greedy (the maximal co-read (the piece-sharing!!!))
# THE CONCRETE-POOL: per PAIR {t, u}: the M = the common-perp-SUBSPACE (the ⊥(span(t, u))!!)
# — the pair-intersections' M's (the dim-7 (the {31, 37}-common-perps (the 7,140-pairs!!!)))
# THE GREEDY: the pairs sorted by the shared-pieces-count (the co-read!!): the maximal!!
# THE BUDGETS: the registers'-chains (the pair-M's (the users'-pairs?!?! (the ~12-18-pairs
# per register?!?! ✗ — the PAIRS-too-fine (the ~12-18!!) — hmm: the QUADS (the ~3-6!!!)))
# -> THE QUAD-CLUSTERS (the {8-target-groups (the block-20's!!)): the M (the dim ~5-6!!)
def perp_subspace_basis(target_set):
    # the ⊥(span(target_set)) (the ambient 9!!
    U = np.array([L[t] for t in target_set])
    _, s, Vt = np.linalg.svd(U)
    fdim = 9 - int(np.sum(s > 1e-9))
    return Vt[9 - fdim:].copy() if fdim > 0 else np.zeros((0, 9))

# THE QUAD-CLUSTERS (the greedy (the co-read (the pieces-shared!!!)))
# the pool: the maximal target-clusters (the ~2-8 targets (the shared-pieces ≥ 2!!!))
log('(2) THE GLOBAL-M-POOL (the greedy quad-clusters (the co-read!!)):')
# the pieces-shared-matrix (the targets'-pairs?!): the co-read-pairs (the ≥ 3-shared-pieces!!)
pairs = []
for i in range(120):
    for j in range(i + 1, 120):
        shared = sum(1 for pi, (sub, users) in enumerate(chosen) if i in users and j in users)
        if shared >= 3:
            pairs.append((shared, i, j))
pairs = sorted(pairs, key=lambda x: -x[0])
log('    the co-read-pairs (the >= 3-shared): %d (the top: %s)' % (
    len(pairs), pairs[:5]))
# THE GREEDY-CLUSTERS (the maximal (the pairs-merged (the shared-pieces-preserved!!!)))
clusters = []
in_cluster = [False] * 120
for shared, i, j in pairs:
    if in_cluster[i] and in_cluster[j]:
        continue
    # the merge-candidates: the existing-cluster (the i-or-j (the MERGE (the +the-other!!!)))
    ci = next((c for c in clusters if i in c), None)
    cj = next((c for c in clusters if j in c), None)
    if ci is not None and cj is not None:
        continue   # the different-clusters (the no-merge (the FIRST-CUT!!!))
    if ci is None and cj is None:
        clusters.append({i, j})
        in_cluster[i] = in_cluster[j] = True
    elif ci is not None:
        ci.add(j); in_cluster[j] = True
    else:
        cj.add(i); in_cluster[i] = True
sizes = Counter(len(c) for c in clusters)
log('    the clusters: %d (the sizes %s (the mean %.1f!!))' % (
    len(clusters), dict(sorted(sizes.items())), float(np.mean([len(c) for c in clusters]))))
# THE M's (the clusters'-perp-subspaces!!)
Mpool = []
for c in clusters:
    B = perp_subspace_basis(sorted(c))
    Mpool.append((sorted(c), B))
Mdims = [len(B) for _, B in Mpool]
log('    the M-dims: %s' % dict(sorted(Counter(Mdims).items())))

# ============ (3) THE BUDGETS (the registers'-chains + the targets'-steps!!!) ============
# THE REGISTERS'-READS: the register's users: the cluster-memberships?!?! — the user t: its
# cluster (the M (the ⊆ perp(t) OKOKOK!!!)): the register's read at the M?!?! (the register's-F
# (the dim-3!!) ⊆ the M?!?! — the M (the ⊥(span(cluster))): the register's-F (the ⊥-ALL-its-users
# (the ⊆ ⊥-the-cluster?!?! — the cluster ⊆ the users?!?! (the register's-users ∩ the cluster?!)))
# — the register's-F (the ⊥-its-USERS (the dim-3!!!)): ⊆ the M (the ⊥-the-cluster (the cluster ⊆
# the users?!?! — NO (the cluster (the CO-READ (the targets (the ANY!!!)) — hmm: the cluster
# (the pair-merged (the shared-pieces (the register ∈ the shared?!?! — the register's-users ⊇
# the cluster?!?! (the register-shared-by-the-cluster (the cluster's-TARGETS ∈ the register's-
# users OKOKOK (the co-read (the ≥3-shared!!!)))) — the span(cluster) ⊆ span(users) ⟹ the M (the
# ⊥-span(cluster)) ⊇ the F (the ⊥-span(users)) OKOKOKOKOKOK THE NESTED (the register's-F ⊆ the M!!!)))
# THE READS: the register r's users'-clusters: the user t's-cluster-M's (the reads (the per-user?!))
# hmm — the register read by the users (the t's (the cluster-members (the M_t?!?! (the user's
# OWN-cluster (the DIFFERENT-M's (the ~24-users (the ~2-8-clusters?!?! (the ✗✗✗ (the incomparable!!!)
# — hmm: the register's users: the ~24: the CLUSTER-MEMBERSHIPS (the per-user (the ~2-8-M's?!?!
# — the register's reads: AT THE USERS'-CLUSTERS'-M's (the ~2-8 (the DISTINCT-clusters (the per-
# register (the users'-cluster-partition?!?! — hmm: the clusters (the DISJOINT?! (the greedy (the
# SOME-overlap (the merged?!))) — the FIRST-CUT: the DISJOINT-ish (the pairs-merged (the trees?!)
# — the register's users (the ~24): the ~2-8-clusters (the per-user (the M's (the ~2-8 (the
# INCOMPARABLE?!?! — the clusters'-M's (the dim ~4-7 (the ⊥-subspaces (the ✗✗✗ (the incomparable
# (the different-clusters!!!))))) — ARGH — THE SAME-WALL?!?! — hmm — THE ⊃-NESTING (the clusters:
# THE NESTED?!?! (the ⊃-chains (the cluster-trees?!?! (the greedy (the ✗ (the DISJOINT!!!))))
# — the honest-first-cut: the MEASUREMENT (the registers'-distinct-M-counts (the per-register
# (the users'-clusters'-M's (the ≤ ~7?!?! — the ~24-users (the ~2-8-clusters (the DISTINCT-M's
# (the ~2-8 (the OK-ish?!?! (the ≤ ~7 (the borderline!!!)))) — the MEASURE!!!
reg_Mcounts = []
reg_incomparables = 0
def span_contains(B, v):
    if len(B) == 0: return False
    A = np.array(B)
    sol, _, _, _ = np.linalg.lstsq(A.T, v, rcond=None)
    return np.allclose(A.T @ sol, v, atol=1e-8)
def sub_leq(B1, B2):
    return all(span_contains(B2, v) for v in B1)
for pi, (sub, users) in enumerate(chosen):
    # the users'-clusters (the M's (the DISTINCT-clusters'-M's (the per-user!!!)))
    tMs = {}
    for t in users:
        for ci, (c, B) in enumerate(Mpool):
            if t in c:
                tMs[t] = (ci, B)
                break
    distinct = {}
    for t, (ci, B) in tMs.items():
        distinct[ci] = B
    reg_Mcounts.append(len(distinct))
    # the nesting-check (the pairwise?!)
    Ms = list(distinct.values())
    for a in range(len(Ms)):
        for b in range(len(Ms)):
            if a != b and not (sub_leq(Ms[a], Ms[b]) or sub_leq(Ms[b], Ms[a])):
                reg_incomparables += 1
                break
        else:
            continue
        break
log('(3) THE REGISTERS-M-COUNTS: %s (the mean %.1f!!) | the INCOMPARABLE-REGISTERS: %d/%d' % (
    dict(sorted(Counter(reg_Mcounts).items())), float(np.mean(reg_Mcounts)),
    reg_incomparables, len(chosen)))
# THE TARGETS'-STEPS: the t's-registers'-reads at the M's (the DISTINCT-M's (the ≤ 8?!?!))
tgt_steps = []
for t in range(120):
    ms = set()
    for pi, (sub, users) in enumerate(chosen):
        if t in users:
            for ci, (c, B) in enumerate(Mpool):
                if t in c:
                    ms.add(ci)
                    break
    tgt_steps.append(len(ms))
log('    THE TARGETS-M-STEPS: %s (the mean %.1f!!) | the OVER-8: %d/120' % (
    dict(sorted(Counter(tgt_steps).items())), float(np.mean(tgt_steps)),
    sum(1 for s in tgt_steps if s > 8)))
log('DONE — THE NAT7-FIRST-CUT!!')
