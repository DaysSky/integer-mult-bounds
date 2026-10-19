"""nat162: THE DISJOINT CELL-PACKING DESIGN (the 121's assembly economy's true test).

The nat161 set-greedy wasted on overlap (16 cells/target). The disjoint question:
perp(t) = 64 lines; the cells are 12-line: the disjoint packing >= 5 cells + raw-leftover.
If the disjoint covers align across the 13-user sharing: the distinct family ~50-100.
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
cand = {t: [i for i, f in enumerate(cells) if set(f) <= perp[t]] for t in range(v)}

# THE DISJOINT PACKING: per target: the cells DISJOINT from the already-covered set (no overlap!)
perp_mask = {t: mask_of(perp[t]) for t in range(v)}
design = {}
for t in range(v):
    covered = 0
    chosen = []
    remaining = set(cand[t])
    # phase 1: the disjoint packing (the biggest disjoint cell first)
    while True:
        best, bestn = None, 0
        for i in remaining:
            cm = cell_masks[i]
            if cm & covered:
                continue
            nn = bin(cm).count('1')
            if nn > bestn:
                bestn, best = nn, i
        if best is None:
            break
        covered |= cell_masks[best]
        chosen.append(best)
        remaining.discard(best)
    # phase 2: the overlap-fills for the remaining lines (the minimal-overlap cells)
    need_left = perp_mask[t] ^ (covered & perp_mask[t])
    while need_left:
        best, bestg = None, 0
        for i in remaining:
            cm = cell_masks[i]
            g = bin(need_left & cm).count('1') - bin((cm ^ need_left) & perp_mask[t] & cm).count('1')
            if g > bestg:
                bestg, best = g, i
        if best is None or bestg <= 0:
            break
        cm = cell_masks[best]
        covered |= cm
        # the parity: track the XOR
        chosen.append(best)
        remaining.discard(best)
        need_left = perp_mask[t] ^ (covered & perp_mask[t])
        if len(chosen) > 30:
            break
    raw = bin(perp_mask[t] ^ (covered & perp_mask[t])).count('1')
    # the XOR-parity raw (the exact): cur = XOR of chosen masks; the raw = the symmetric difference
    cur = 0
    for i in chosen:
        cur ^= cell_masks[i]
    raw_x = cur ^ perp_mask[t]
    design[t] = (chosen, bin(raw_x & perp_mask[t]).count('1'), bin(raw_x).count('1') - bin(raw_x & perp_mask[t]).count('1'))
    if (t+1) % 40 == 0:
        print('  %d done' % (t+1), flush=True)

nc = Counter(len(ch) for ch, _, _ in design.values())
nraw = Counter(r for _, r, _ in design.values())
print('the per-target cell-counts:', dict(sorted(nc.items())))
print('the per-target raw-counts (in-perp part):', dict(sorted(nraw.items())))
print('the means: cells %.2f, raw %.2f' % (
    sum(len(ch) for ch, _, _ in design.values())/v,
    sum(r for _, r, _ in design.values())/v))
uses = Counter()
for ch, _, _ in design.values():
    for i in ch:
        uses[i] += 1
print('THE DISTINCT CELLS: %d' % len(uses))
print('the uses histogram:', dict(sorted(Counter(uses.values()).items())))
json.dump({'design': {t: [ch, r] for t, (ch, r, _) in design.items()},
           'cells': [list(f) for f in cells]},
          open('ii19_nat162_disjoint.json', 'wt'))
print('SAVED ii19_nat162_disjoint.json')
