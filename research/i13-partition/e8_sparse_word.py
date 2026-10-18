"""E8 SPARSE WORD, PHASE 3 — the exact economics + the calibrated price projection.
Phase 1 (e8_rowspace.py): the rank-9 space PROVEN rigid (all 512 codewords: weights
{0,56,64,120}; every target's ONLY legal codeword is its full perp).
Phase 2 (e8_enrich.py): THE SPARSE DECODERS EXIST — the cancellation construction
(r'_t = r_t XOR ind(perp(t) & perp(x_t)), greedy partner choice) gives rows legal BY
CONSTRUCTION:  k=1: rows 34, rank 113 (dead) | k=2: rows 30, rank 33 (THE CANDIDATE)
| k=3+: rows 4, rank 57 (the identity class — likely outside the price regime).
THE k=2 CANDIDATE: demands 29 lines/target (vs B0's 63), the retained 33.
This script: (1) rebuild + verify the k=2 decoder; (2) the word structure: the carriers
240 + the middle grid (the E8-style shared covers, halved demands) + the retained 33;
(3) the cst grid; (4) the mass-exact frozen-shape price + the MEASURED calibration
(the frozen-shape family under-prices by 7.3%, pinned at the R434 control); (5) THE
VERDICT vs the frontier 0.001744386.  RAM-SAFE: no exponential enumerations."""
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
log('E8 system: %d lines; perp sizes mean %.1f' % (V, sum(bin(m).count('1') for m in PERP) / V))

def rank_packed(rows):
    piv = {}
    for row in rows:
        red = row
        while red:
            p = (red & -red).bit_length() - 1
            if p in piv: red ^= piv[p]
            else: piv[p] = red; break
    return len(piv)

# the k=2 greedy cancellation rows (phase 2's candidate)
def greedy_rows(npairs):
    out = []
    for t in range(V):
        cur = rows0[t]; used = set()
        for _ in range(npairs):
            bw = bin(cur).count('1'); best = None
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

rows2 = greedy_rows(2)
ws = [bin(r).count('1') for r in rows2]
rk = rank_packed(rows2)
# full verification
ok = all(((rows2[t] & ~(PERP[t] | (1 << t)) & ((1 << V) - 1)) == 0) and ((rows2[t] >> t) & 1) for t in range(V))
log('THE k=2 DECODER: rows min %d mean %.1f max %d | rank %d | diag+support legal: %s' % (min(ws), sum(ws) / V, max(ws), rk, ok))
# distinct junk sets (the sharing structure: how many distinct 29-line demands?)
junks = [r & ~(1 << t) for t, r in enumerate(rows2)] if False else [rows2[t] ^ (1 << t) for t in range(V)]
distinct = len(set(junks))
log('distinct junk sets: %d of %d targets (sharing %s)' % (distinct, V, 'WEAK' if distinct > 100 else ('moderate' if distinct > 40 else 'STRONG')))
# pairwise junk overlaps (the sharing economy input)
ovl = []
for a in range(0, V, 7):
    for b in range(a + 1, V, 7):
        ovl.append(bin(junks[a] & junks[b]).count('1'))
log('junk pairwise overlaps (sampled): mean %.1f min %d max %d' % (sum(ovl) / len(ovl), min(ovl), max(ovl)))

# the price machinery (mix.price model replaced by the frozen-shape family + calibration)
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
FRONTIER = 0.001744386
E8SHAPE = [(1, 1320), (2, 1440), (4, 60), (5, 120)]
CLIMB420 = 1320 + 2880 + 240 + 600  # 5040

def price_proj(label, R, cst, v=120, h=8):
    ident = h * R + cst + 2 * v * (h - 1)
    climb = ident - cst
    hist = {}
    for rank, cnt in E8SHAPE:
        mmass = climb * (rank * cnt) / CLIMB420
        hist[rank] = max(1, int(round(mmass / rank)))
    hist[8] = hist.get(8, 0) + max(1, cst // 8)  # the copy children
    climb_now = sum(k * n for k, n in hist.items()) - hist[8] * 8
    hist[1] = hist.get(1, 0) + (climb - climb_now)
    cc, _, det = pprice(hist, v, h, R)
    mass = sum(k * n for k, n in hist.items())
    return cc, mass, ident

# CONTROLS
c434, m434, i434 = price_proj('ctrl', 434, 72)
log('CONTROL R434 (frozen-shape): c = %s (true 0.0017444; ratio %.4f)' % (c434, 0.0017444 / c434 if c434 else 0))
c420, _, _ = price_proj('ctrl', 420, 72)
log('CONTROL R420 (frozen-shape): c = %s (true 0.0016538; ratio %.4f)' % (c420, 0.0016538 / c420 if c420 else 0))
CAL = 0.0017444 / c434 if c434 else 1.073
log('calibration factor (R434): %.4f' % CAL)

print()
log('=== THE k=2 SPARSE WORD: THE PRICE GRID (calibrated) ===')
log('structure: carriers 240 + middle MID + retained %d; demands ~%d lines/target' % (rk, int(sum(ws) / V) - 1))
best = None
for mid in (50, 70, 90, 110, 130):
    for cst in (150, 200, 250, 300):
        R = 240 + mid + rk
        cc, mass, ident = price_proj('cand', R, cst)
        if cc is None:
            log('  mid %3d cst %3d: R %3d mass/v %5.1f: NO ROOT' % (mid, cst, R, (ident) / 120))
            continue
        cal_c = cc * CAL
        pct = (cal_c / FRONTIER - 1) * 100
        log('  mid %3d cst %3d: R %3d mass/v %5.1f: frozen c %.7f -> calibrated %.7f (%+.2f%% vs frontier)'
            % (mid, cst, R, ident / 120, cc, cal_c, pct))
        if best is None or cal_c > best[0]:
            best = (cal_c, mid, cst, R, pct)
print()
if best:
    log('BEST: calibrated c %.7f (%+.2f%% vs frontier) @ mid %d cst %d R %d' % (best[0], best[4], best[1], best[2], best[3]))
    if best[0] > FRONTIER:
        log('THE k=2 SPARSE WORD PROJECTS ABOVE THE FRONTIER — next: the exact middle design (the shared covers')
        log('for the 29-line demands), the exact cst (the factorization), the word build, gcheck, the true price.')
    else:
        log('The projection lands below the frontier — the middle/cst estimates decide; refine before verdict.')
else:
    log('No priceable point — the regime question (the k=3 identity class) applies.')
log('DONE')