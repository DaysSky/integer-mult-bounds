"""E8 PAIR-INTERSECTION ENRICHMENT — the low-rank sparse-decoder search, phase 2.
Phase 1 (e8_rowspace.py) PROVED the rank-9 space rigid by exhaustive enumeration: the
512 codewords have weights {0: 1, 56: 255, 64: 255, 120: 1}; every target's ONLY legal
codeword is its own full perp (weight 64).  No sparse decoder at rank 9 — proven.

PHASE 2 (this script): THE CANCELLATION CONSTRUCTION — rows legal BY CONSTRUCTION:
    r'_t = r_t XOR ind(perp(t) & perp(x_t))   for partners x_t in perp(t).
The intersection mask lies inside perp(t), so the XOR only REMOVES bits from the full
perp: supp(r'_t) stays inside {t} u perp(t) (legal), r'_t[t] = 1 (bit t never in the
intersection).  Row weight = 64 - |perp(t) & perp(x_t)|.
THE ONLY QUESTION: THE RANK of the enriched decoder B' (the retained registers).
  - the pair-intersection size distribution (the partner quality);
  - greedy 1/2/3/4-partner cancellations per target: the (weight, rank) trade-off curve;
  - THE WIN ZONE: rank <= ~30 with rows <= ~35 (mass/v <= 40 vs R434's 43.5);
  - the economics at each point + the calibrated price projection (the frozen-shape
    family under-prices by 7.3%, measured at the R434 control in e8_sparse_decoder.py).
RAM-SAFE: no exponential enumerations anywhere (the phase-1 lesson)."""
import sys, time, resource
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in __import__('itertools').product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
L = np.array(list(d8.values()))
V = len(L)
G = L @ L.T
log('E8 system: %d lines' % V)

B0 = (np.rint(1 + G).astype(int)) % 2
def pack(M):
    return [int(''.join(str(int(x)) for x in row[::-1]), 2) for row in M]
rows0 = pack(B0)

PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) <= 1e-9:
            m |= (1 << s)
    PERP.append(m)
partners = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]
log('perp sizes: mean %.1f; partners per target: mean %.1f' % (
    sum(bin(m).count('1') for m in PERP) / V, sum(len(p) for p in partners) / V))

# the pair-intersection size distribution
from collections import Counter
sizes = Counter()
for t in range(V):
    for x in partners[t]:
        sizes[bin(PERP[t] & PERP[x]).count('1')] += 1
log('pair-intersection sizes (size: count): %s' % dict(sorted(sizes.items())))
mx = max(sizes)
log('MAX pair-intersection size: %d -> the best single-partner row weight: %d' % (mx, 64 - mx))

def rank_packed(rows):
    piv = {}
    for row in rows:
        red = row
        while red:
            p = (red & -red).bit_length() - 1
            if p in piv:
                red ^= piv[p]
            else:
                piv[p] = red
                break
    return len(piv)

log('baseline: rank of B0 = %d (control)' % rank_packed(rows0))

def greedy_rows(npairs):
    """per target: greedily add partners whose intersection cancels the most row bits"""
    out = []
    for t in range(V):
        cur = rows0[t]
        used = set()
        for _ in range(npairs):
            bw = bin(cur).count('1')
            best = None
            for x in partners[t]:
                if x in used: continue
                cand = cur ^ (PERP[t] & PERP[x])
                w = bin(cand).count('1')
                if w < bw and (best is None or w < best[0]):
                    best = (w, x, cand)
            if best is None: break
            cur = best[2]; used.add(best[1])
        out.append(cur)
    return out

def economics(rows, label):
    ws = [bin(r).count('1') for r in rows]
    rk = rank_packed(rows)
    mean_w = sum(ws) / len(ws)
    mid = 194 * mean_w / 63.0
    R = 240 + mid + rk
    cst = 6 * rk
    mass = 8 * R + cst + 2 * V * 7
    mv = mass / V
    # legality check: every row's support inside {t} u perp(t), bit t set
    ok = True
    for t in range(V):
        npmask = ~ (PERP[t] | (1 << t)) & ((1 << V) - 1)
        if (rows[t] & npmask) or not ((rows[t] >> t) & 1):
            ok = False; break
    log('%s: row weights min %d mean %.1f max %d | rank %d | mid %.0f R %.0f cst %d mass/v %.1f (frontier 43.5) | legal %s'
        % (label, min(ws), mean_w, max(ws), rk, mid, R, cst, mv, 'OK' if ok else 'VIOLATION'))
    return rk, mean_w, R, cst, mv

print()
log('=== THE CANCELLATION CURVE (greedy partner additions) ===')
best = None
for k in (1, 2, 3, 4, 6, 8):
    rows = greedy_rows(k)
    rk, mw, R, cst, mv = economics(rows, 'k=%d partners' % k)
    if mv < 43.5 and (best is None or mv < best[4]):
        best = (k, rk, mw, R, cst, mv)
print()
if best:
    log('WIN-ZONE CANDIDATE: k=%d partners: rank %d, mean row %.1f, R %.0f, mass/v %.1f' % (best[0], best[1], best[2], best[3], best[4]))
    log('THE SPARSE DECODER EXISTS at rank %d — next: the exact cst (congruence), the middle design, the word build' % best[1])
else:
    log('No point on the greedy curve beats mass/v 43.5 — the rank grows too fast (the trade-off measured).')
log('DONE')