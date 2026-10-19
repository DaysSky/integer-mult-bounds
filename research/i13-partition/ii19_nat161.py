"""nat161: THE FRESH CELL+RAW ASSEMBLY DESIGN (the 121's E8-style quad-total economy).

The nat160 obstruction: the cells' GF(2)-span is proper in each perp (a parity invariant).
The fresh design: per target, cover perp(t) with cells (the 13-shared family!) via SET-cover,
then read the XOR-leftover (the symmetric difference) RAW from the sources (legal direct reads).
Census: per-target cell-counts, raw-counts, the global distinct cells, the arrival fit.
"""
import json
from collections import Counter
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

# the D4-cells (the nat159/160 machinery)
frames = set()
for l in range(v):
    P = sorted(perp[l])
    if len(P) < 4:
        continue
    Pa = L8[P]
    IPp = np.round(Pa @ Pa.T / 2.0).astype(np.int64)
    adj = (IPp == 0)
    a_idx, b_idx = np.nonzero(np.triu(adj, 1))
    tris = []
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

cells = list(frames)
cell_masks = [mask_of(f) for f in cells]
# the per-target candidates: the cells ⊆ perp(t)
cand = {t: [i for i, f in enumerate(cells) if set(f) <= perp[t]] for t in range(v)}
print('the per-target cell-candidates:', dict(sorted(Counter(len(c) for c in cand.values()).items())), flush=True)

# THE FRESH ASSEMBLY: per target t: cover perp(t):
# (1) the SET-greedy over the cells (the new-line gain);
# (2) the XOR-parity: cur = XOR(chosen cell-masks); the target needs perp(t) delivered;
#     the symmetric-difference leftover = perp_mask ^ cur -> the RAW source-reads.
perp_mask = {t: mask_of(perp[t]) for t in range(v)}
design = {}
for t in range(v):
    need = perp_mask[t]
    cur = 0
    chosen = []
    remaining = set(range(len(cand[t])))
    while cur ^ need:  # the symmetric difference nonzero
        # the best cell: max (cur^need) & cell_mask - (cur & cell_mask) ... the gain:
        best, bestg = None, 0
        for i in remaining:
            cm = cell_masks[cand[t][i]]
            g = bin((cur ^ need) & cm).count('1') - bin(cur & cm).count('1')
            if g > bestg:
                bestg, best = g, i
        if best is None or bestg <= 0:
            break
        i = best
        cur ^= cell_masks[cand[t][i]]
        chosen.append(cand[t][i])
        remaining.discard(i)
        if len(chosen) > 40:
            break
    left = cur ^ need
    design[t] = (chosen, bin(left).count('1'))
    if len(design) % 30 == 0:
        print('  %d targets designed' % len(design), flush=True)

nc = Counter(len(ch) for ch, _ in design.values())
nr = Counter(r for _, r in design.values())
print('the per-target cell-counts:', dict(sorted(nc.items())))
print('the per-target RAW-leftover counts:', dict(sorted(nr.items())))
print('the mean cells/target: %.2f | the mean raw/target: %.2f' % (
    sum(len(ch) for ch, _ in design.values())/v, sum(r for _, r in design.values())/v))

uses = Counter()
for ch, _ in design.values():
    for i in ch:
        uses[i] += 1
print('THE DISTINCT CELLS: %d' % len(uses))
print('the uses histogram:', dict(sorted(Counter(uses.values()).items())))

# the total arrival accounting
tot_reads = sum(len(ch) + r for ch, r in design.values())
print('the total reads (cells + raw): %d | the per-target %.2f' % (tot_reads, tot_reads/v))
print('the arrival law: h*R >= the demand-reads: at R = 150: 9*150 = %d vs %d' % (1350, tot_reads))

json.dump({'design': {t: [ch, r] for t, (ch, r) in design.items()},
           'cells': [list(f) for f in cells]},
          open('ii19_nat161_freshdesign.json', 'wt'))
print('SAVED ii19_nat161_freshdesign.json')
