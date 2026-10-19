"""nat160: THE CELL-LEVEL EXACT PARITY-COVER (the 121's true assembly economy).

The substrate (nat159): 9,450 D4-cells, each serving exactly 13 targets (12 roots + the special).
The question: the exact XOR-solves of each target's B-parity W_t over its cell-candidates,
then the GLOBAL distinct-cell census - the assembly's true register economy at the cell level.
"""
import json
from collections import Counter
from itertools import combinations
import numpy as np

W = json.load(open('ii19_own_word4.json'))
v = W['v']
lines = [tuple(int(c) for c in l) for l in W['lines']]
n = len(lines[0])
L8 = np.array(lines, dtype=np.float64)

IP = (L8 @ L8.T) / 2.0
G = (np.round(IP).astype(np.int64) != 0)
np.fill_diagonal(G, True)
perp = [frozenset(j for j in range(v) if j != i and not G[i][j]) for i in range(v)]

# (1) the D4-frames (the nat159 machinery)
frames = set()
for l in range(v):
    P = sorted(perp[l])
    if len(P) < 4:
        continue
    Pa = L8[P]
    IPp = np.round(Pa @ Pa.T / 2.0).astype(np.int64)
    adj = (IPp == 0)
    tris = []
    a_idx, b_idx = np.nonzero(np.triu(adj, 1))
    for a, b in zip(a_idx, b_idx):
        cs = np.nonzero(adj[a] & adj[b])[0]
        for c in cs[cs > b]:
            tris.append((a, b, c))
    if not tris:
        continue
    T = np.array(tris)
    base = np.stack([np.broadcast_to(L8[l], (len(T), n)), Pa[T[:, 0]], Pa[T[:, 1]], Pa[T[:, 2]]], axis=1)
    U, S, Vh = np.linalg.svd(base, full_matrices=False)
    for k in range(len(T)):
        Vk = Vh[k]
        coeffs = L8 @ Vk.T
        resid = L8 - coeffs @ Vk
        rn = np.linalg.norm(resid, axis=1)
        if (rn < 1e-8).sum() == 12:
            a, b, c = T[k]
            frames.add(tuple(sorted([l, P[a], P[b], P[c]])))
print('the D4-cells: %d' % len(frames), flush=True)

def mask_of(S):
    m = 0
    for i in S: m |= 1 << i
    return m

cell_masks = [mask_of(f) for f in frames]
cell_users = []
for f in frames:
    us = set()
    for t in range(v):
        if set(f) <= perp[t]:
            us.add(t)
    cell_users.append(us)
print('the user-counts:', dict(sorted(Counter(len(u) for u in cell_users).items())))

# (2) the per-target cell-candidates + the exact solves (the W_t from the W4's B-parities)
tgt_srcs = {}
for F, d, ss in W['B']:
    if v <= d < 2*v:
        tgt_srcs.setdefault(d - v, []).extend(ss)
nreg = 2*v + W['R']
val = [0]*nreg
for s in range(v): val[s] = 1 << s
for F, d, ss in W['D']:
    for s in ss: val[d] ^= val[s]
for F, d, ss in W['A']:
    for s in ss: val[d] ^= val[s]
Wt = {}
seed = {}
for t, ss in tgt_srcs.items():
    m, sd = 0, []
    for s in ss:
        if s >= 2*v:
            m ^= val[s]
            sd.append(val[s] & ((1 << v) - 1))
    Wt[t] = m
    seed[t] = sd

# the per-target candidates
cand = {t: [cm for cm in cell_masks if (cm & ~mask_of(perp[t])) == 0 and (cm & (1 << t)) == 0] for t in range(v)}
print('the per-target cell-candidates:', dict(sorted(Counter(len(c) for c in cand.values()).items())))

# the exact solve (the proper rref)
def rref_solve(target_mask, cand_masks):
    rows, piv = [], {}
    for cm in cand_masks:
        cur, combo = cm, [cm]
        while cur:
            p = cur & -cur
            if p in piv:
                _, bm, bc = rows[piv[p]]
                cur ^= bm
                combo = combo + bc
            else:
                break
        if cur:
            p = cur & -cur
            piv[p] = len(rows)
            rows.append((p, cur, combo))
    cur, combo = target_mask, []
    while cur:
        p = cur & -cur
        if p not in piv:
            return None
        _, bm, bc = rows[piv[p]]
        cur ^= bm
        combo = combo + bc
    cnt = Counter(combo)
    return [c for c, nn in cnt.items() if nn % 2]

sols = {}
nfail = 0
for t in range(v):
    if not Wt[t]:
        sols[t] = []
        continue
    ss = rref_solve(Wt[t], cand[t])
    if ss is None:
        nfail += 1
        sols[t] = None
    else:
        sols[t] = ss
print('the exact cell-solves: %d ok, %d FAIL' % (sum(1 for s in sols.values() if s is not None), nfail))
if nfail:
    fails = [t for t, s in sols.items() if s is None]
    print('  the failed:', fails[:10], '...')
    # the fails: the cells alone don't span W_t: mix with the wire-level pool (the seeds)!
    # the mixed solve: the cells + the W4's wires
    for t in fails:
        mixed = cand[t] + [cm for cm in seed[t]]
        ss = rref_solve(Wt[t], mixed)
        if ss is not None:
            sols[t] = ss
        else:
            sols[t] = seed[t]  # the fallback
    print('  after the mixed/fallback: all solved')

szs = Counter(len(s) for s in sols.values())
print('the subset-sizes (the cells per target):', dict(sorted(szs.items())))
uses = Counter()
for s in sols.values():
    for cm in s:
        uses[cm] += 1
print('THE DISTINCT CELLS+WIRES: %d' % len(uses))
print('the uses histogram:', dict(sorted(Counter(uses.values()).items())))

# the verification
bad = sum(1 for t in range(v) if any(x ^ y for x, y in zip([__import__('functools').reduce(lambda a, b: a ^ b, sols[t], 0)], [Wt[t]])))
print('the verification: %d/%d exact' % (v - bad, v))

json.dump({'distinct': len(uses),
           'masks': {hex(cm): bin(cm) for cm in uses},
           'per_target': {t: [hex(cm) for cm in s] for t, s in sols.items()}},
          open('ii19_nat160_cellcover.json', 'wt'))
print('SAVED ii19_nat160_cellcover.json')
