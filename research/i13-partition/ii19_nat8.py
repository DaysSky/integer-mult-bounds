"""THE NATIVE-121 v8 (ii19_nat8.py) — THE GLOBAL POOL-TREE + THE BUDGETS + (if-fit) THE GATES!!
THE SUPER-CHAIN-DESIGN (the final-core!!): the GLOBAL read-frame-pool organized as a TREE
(the levels (the dims 4-8!!): the co-read-clusters' perp-subspaces; the levels nest by the
PERP-REVERSAL (the cluster-tree (the SUPERSET-relations!!!))) — the registers climb the
tree (the F (dim-3!!) -> the level-4 -> ... -> the level-8 (the FULL!!!)): the ~2-4 levels
per register (the ARRIVAL-FIT (the ~360-720 (the <= 9R = 1,971!!!))); the targets read
their registers at the tree-nodes (the <= 8 steps (the per-dim-ONE (the FREE-multi!!!)))
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

# ============ (0) THE SHARED-MACHINERY (the nat5/6's!!) ============
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
log('(0) the partition %d + the pieces %d + the Fs OK' % (len(frames), len(chosen)))
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

# ============ (1) THE GLOBAL POOL-TREE (the greedy co-read (the hierarchical levels!!)) ============
# THE LEVELS: the cluster-sizes (the co-read): the level-8 (the pairs/triples (the M-dims 7-8!!)),
# the level-6 (the 4-6-clusters (the M-dims 5-6!!)), the level-4 (the 8-16-clusters (the M-dims 3-4!!))
# THE CONSTRUCTION (the bottom-up (the pairs-merged (the co-read (the >= 3-shared-pieces!!!))))
pairs = []
for i in range(120):
    for j in range(i + 1, 120):
        shared = sum(1 for pi, (sub, users) in enumerate(chosen) if i in users and j in users)
        if shared >= 3:
            pairs.append((shared, i, j))
pairs = sorted(pairs, key=lambda x: -x[0])
# THE HIERARCHICAL-CLUSTERING (the levels (the SIZE-CAPS (the ~4 (the level-8), the ~8 (the
# level-6), the ~16 (the level-4)!!!)))
def build_tree(cap_sizes):
    # the multi-level: the level-l (the cap (the cluster-sizes ≤ cap-l!!)): the greedy-merge
    levels = []
    cur = [{t} for t in range(120)]
    for cap in cap_sizes:
        merged = [set(c) for c in cur]
        # the greedy: the merge the co-read-clusters while the size <= cap!!
        changed = True
        while changed:
            changed = False
            # the best-merge (the max-shared-pieces (the inter-cluster-pairs!!!))
            best = None
            for ai in range(len(merged)):
                for bi in range(ai + 1, len(merged)):
                    if len(merged[ai]) + len(merged[bi]) > cap:
                        continue
                    sh = sum(1 for pi, (sub, users) in enumerate(chosen)
                             if any(t in merged[ai] for t in users) and any(t in merged[bi] for t in users))
                    if best is None or sh > best[0]:
                        best = (sh, ai, bi)
            if best is not None and best[0] >= 3:
                sh, ai, bi = best
                merged[ai] |= merged[bi]
                merged.pop(bi)
                changed = True
        levels.append(merged)
        cur = merged
    return levels
cap_sizes = [4, 8, 16]
levels = build_tree(cap_sizes)
for li, lev in enumerate(levels):
    sizes = sorted(len(c) for c in lev if len(c) > 1)
    log('(1) the level-%d: %d clusters (the sizes %s.. (the multi: %d!!))' % (
        li, len(lev), sizes[:6], sum(1 for c in lev if len(c) > 1)))
# THE POOL: the clusters' M's (the perp-subspaces!!)
pool = []
for li, lev in enumerate(levels):
    for c in lev:
        if len(c) > 1:
            B = perp_basis(sorted(c))
            if len(B) >= 3:
                pool.append((li, sorted(c), B))
log('    the pool: %d M-frames (the dims %s!!)' % (
    len(pool), dict(sorted(Counter(len(B) for _, _, B in pool).items()))))

# ============ (2) THE REGISTERS'-CHAIN-ASSIGNMENT (the SUPER-CHAINS!!) ============
# the per-register: its users -> the pool-nodes (the co-read (the users'-subsets!!)):
# the chain: the pool-nodes with the ⊆-nested M's (the tree-paths (the users'-nested!!!))
# THE ASSIGNMENT: the user t reads the register r at the DEEPEST pool-node (the ⊇ the r's-F
# + the ∋ t (the t ∈ the node's-cluster!!!)))
reg_chains = []
reg_chain_ok = 0
for pi, (sub, users) in enumerate(chosen):
    # the candidate-nodes: the ∩ with the users (the non-empty (the M ⊇ the F!!))
    nodes = []
    for ni, (li, c, B) in enumerate(pool):
        inter = [t for t in c if t in users]
        if len(inter) >= 2 and sub_leq(regF_basis[pi], B):
            nodes.append((ni, inter, B))
    # the chain: the nodes sorted (the ⊆-nested (the M-dims ascending (the LI (the tree-paths!!!))))
    nodes.sort(key=lambda x: (len(x[2]), -len(x[1])))
    chain = []
    prevB = regF_basis[pi]
    ok = True
    for ni, inter, B in nodes:
        if sub_leq(prevB, B):
            chain.append((ni, inter, B))
            prevB = B
        else:
            ok = False
            break
    if ok and chain:
        reg_chain_ok += 1
    reg_chains.append((ok, chain))
# THE COVERAGE: the chain's users'-union vs the register's-users!!!
cov_ok = 0
t_steps = Counter()
for pi, (sub, users) in enumerate(chosen):
    ok, chain = reg_chains[pi]
    if ok and set().union(*[set(i) for _, i, _ in chain]) == set(users):
        cov_ok += 1
log('(2) the chains: the nested-OK %d/%d | the users-covered %d/%d' % (
    reg_chain_ok, len(chosen), cov_ok, len(chosen)))
log('DONE — THE NAT8-FIRST-CUT (the tree-fit!!)')
