"""THE NATIVE-121 v6 (ii19_nat6.py) — THE JOINT-CLUSTERING FEASIBILITY: THE REGISTERS'-M-CHAIN
DECOMPOSITIONS (THE DILWORTH-MIN vs THE MASS-9 BUDGET!!!) + THE ⊥-REVERSAL-ORDER!!
THE DERIVATION (the breakthrough!!): the register's F (= the M(ALL-users)) ⊆ M(G) for
every subgroup G (the +-complement-of-more ⊆ +-complement-of-less!!!) -> the read-chain:
the F -> the BIGGEST-group's M (the lowest-dim!!) -> the SMALLER-groups' M's (the ASCENDING
dims!!) — THE NESTED BY THE +-DUALITY!!!
THE MEASUREMENT (the decisive!!): the register's users'-M(t)-frames (the per-target unions
(the dim 5-7!!)): the +-chain-decompositions (the minimal (the Dilworth!!)) vs the ≤ ~6
extra steps (the mass-9: the build 2-3 + the F 0-1 + the reads Σ ≤ ~5-6!!!)
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

# ============ (1) THE PARTITION + THE PIECES (the nat3b's!!) ============
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

# ============ (2) THE REGISTERS'-F (the users'-+-complements (dim-3!!)) ============
regF_basis = []   # the per-piece: the F's BASIS (the orthonormal (the SVD's Vt!!))
for pi, (sub, users) in enumerate(chosen):
    U = np.array([L[t] for t in users])
    # the +-complement: the null-space (the SVD!!): the vectors ⊥ all the users!!
    _, s, Vt = np.linalg.svd(U)
    fdim = 9 - int(np.sum(s > 1e-9))
    # the basis: the Vt's last fdim rows (the null-directions!!)
    regF_basis.append(Vt[9 - fdim:].copy() if fdim > 0 else np.zeros((0, 9)))
log('(2) the registers-F: %d (the dims %s!!)' % (
    len(regF_basis), dict(sorted(Counter(len(b) for b in regF_basis).items()))))

# ============ (3) THE TARGETS'-M(t) (the unions of their registers'-F's (⊆ perp(t)!!)) ============
# the M(t): the basis (the cumulative RREF of the t's-registers'-F-bases!!)
def subspace_contains(basis_big, vec):
    # is vec ∈ span(basis_big)?!
    if len(basis_big) == 0: return False
    A = np.array(basis_big)
    sol, res, rank, sv = np.linalg.lstsq(A.T, vec, rcond=None)
    recon = A.T @ sol
    return np.allclose(recon, vec, atol=1e-8)
tgtM = []
for t in range(120):
    basis = []
    for pi, (sub, users) in enumerate(chosen):
        if t in users:
            for v in regF_basis[pi]:
                if not subspace_contains(basis, v):
                    basis.append(v)
    tgtM.append(np.array(basis) if basis else np.zeros((0, 9)))
tgtM_dims = [len(b) for b in tgtM]
log('(3) the targets-M: the dims %s (the mean %.1f!!)' % (
    dict(sorted(Counter(tgtM_dims).items())), float(np.mean(tgtM_dims))))

# ============ (4) THE FEASIBILITY: THE REGISTERS'-USERS'-M(t)'s: THE ⊆-CHAIN DECOMPOSITIONS ============
# the per-register: its users'-M(t)'s (the frames (the subspaces!!)): the poset (the ⊆!!):
# the MINIMAL chain-decomposition (the Dilworth (the greedy (the longest-chains!!)))
def subset_leq(B1, B2):
    # span(B1) ⊆ span(B2)?!
    if len(B1) == 0: return True
    if len(B2) == 0: return False
    return all(subspace_contains(B2, v) for v in B1)
reg_chains = []
chain_counts = []
for pi, (sub, users) in enumerate(chosen):
    Ms = [(t, tgtM[t]) for t in users]
    # the greedy chain-decomposition (the patience-sorting (the ⊆-poset!!))
    chains = []
    for t, M in sorted(Ms, key=lambda x: -len(x[1])):
        placed = False
        for ch in chains:
            if subset_leq(M, ch[-1][1]):   # M ⊆ the chain's last (the descending-insert!!)
                ch.append((t, M))
                placed = True
                break
        if not placed:
            chains.append([(t, M)])
    reg_chains.append(chains)
    chain_counts.append(len(chains))
log('(4) THE CHAIN-COUNTS: %s (the mean %.1f!!) | the registers over the budget (the > 5): %d/%d' % (
    dict(sorted(Counter(chain_counts).items())), float(np.mean(chain_counts)),
    sum(1 for c in chain_counts if c > 5), len(chains)))
# THE MASS-CHECK (the per-register: the Σdeltas ≤ 9!!)
mass_over = 0
for pi, (sub, users) in enumerate(chosen):
    ps = rank_of([L[x] for x in sub])
    m = ps  # the build!!
    prev = ps
    for ch in reg_chains[pi]:
        # the chain's dims (the ascending (the chain-order (the descending-insert (the REVERSED!!!))))
        # the chain: the DESCENDING-dims (the insert-order!!): the reads (the ASCENDING (the ⊥-reversal!!!)))
        ch_dims = sorted(set(len(M) for _, M in ch))
        for d in ch_dims:
            m += max(0, d - prev)
            prev = max(prev, d)
    m += 9 - prev
    if m > 9:
        mass_over += 1
log('    THE MASS-OVER (the > 9!!): %d/%d registers!!' % (mass_over, len(chosen)))
log('DONE — THE NAT6-FEASIBILITY!!')
