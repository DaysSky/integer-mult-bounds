"""E8 SPARSE-DECODER HUNT — the never-run frontier lever (user: "look for ANY breakthrough";
"dont consider something dead unless 100% proven to be dead").
The masked-demand freedom (HANDOFF: "target t reads c_t = row t — NOT NECESSARILY ALL of R(t)")
applied to the FRONTIER SYSTEM (E8, h=8, no window penalty).  The R434 word runs B0-style
full-perp demands (~58 lines/target) -> middle ~194 -> R = 434, mass/v = 43.5.
A sparse decoder (rows ~12-25, above the counting bound v/c - 1 ~ 12) shrinks the demands ->
the middle -> R ~ 320-375 -> mass/v ~ 36-40 -> c potentially +5-15%???
VALIDITY: ANY masked B0 is a valid decoder (diag 1, support inside perp, by construction).
THE QUESTION: the RANK-vs-SPARSITY trade-off — a measurable curve, not a verdict.
1. B0 = (J + G) mod 2: verify rank 9, row sizes.
2. Random masks at f in (0.6, 0.5, 0.4, 0.3, 0.25, 0.2): rank distributions (300 trials each).
3. Structured prefix masks (shared junk prefixes across targets -> shared pieces): 40 shuffles each.
4. Best candidates: rank, row stats, cst (congruence gathers), demand structure.
5. PRICE PROJECTION: frozen-E8-shape mass-exact hists at the mid grid; the R434 calibration
   control included (the frozen-shape family must reproduce ~0.00174 at the R434 mass)."""
import sys, time, random, itertools, resource
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
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
ok_diag = bool((np.diag(B0) == 1).all())
viol = int(((np.abs(G) > 1e-9) & (B0 == 1) & (~np.eye(V, dtype=bool))).sum())
log('B0: diag all 1: %s; support violations: %d' % (ok_diag, viol))

def pack(M):
    return [int(''.join(str(int(x)) for x in row[::-1]), 2) for row in M]
def rank_packed(rows):
    rows = list(rows); r = 0
    for col in range(V - 1, -1, -1):
        piv = None
        for i in range(r, len(rows)):
            if (rows[i] >> col) & 1: piv = i; break
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> col) & 1): rows[i] ^= rows[r]
        r += 1
    return r

rk0 = rank_packed(pack(B0))
rowsizes = [int(B0[t].sum()) - 1 for t in range(V)]
log('B0 rank: %d (expected 9); row sizes mean %.1f min %d max %d' %
    (rk0, sum(rowsizes) / V, min(rowsizes), max(rowsizes)))

perp = [[s for s in range(V) if s != t and B0[t][s]] for t in range(V)]

def masked_rows(mode, f, rng):
    rows = []
    for t in range(V):
        if mode == 'rand':
            keep = [s for s in perp[t] if rng.random() < f]
        else:  # prefix on a shuffled global order
            k = int(np.ceil(f * len(perp[t])))
            keep = sorted(perp[t], key=lambda s: order[s])[:k]
        rows.append(sum(1 << s for s in keep) | (1 << t))
    return rows

log('RANDOM-MASK RANK CURVE (300 trials per f):')
best_at = {}
for f in (0.6, 0.5, 0.4, 0.3, 0.25, 0.2):
    rng = random.Random(1234 + int(f * 100))
    best = None; ranks = []
    for trial in range(300):
        rows = masked_rows('rand', f, rng)
        r = rank_packed(rows)
        ranks.append(r)
        if best is None or r < best[0]: best = (r, trial)
    best_at[f] = best[0]
    log('  f=%.2f (rows ~%.0f): rank min %d mean %.1f max %d' %
        (f, f * sum(rowsizes) / V, min(ranks), sum(ranks) / len(ranks), max(ranks)))

log('PREFIX-MASK RANK CURVE (40 shuffles per f):')
for f in (0.5, 0.4, 0.3, 0.25, 0.2):
    rng = random.Random(777 + int(f * 100))
    best = None; ranks = []
    for trial in range(40):
        order = list(range(V)); rng.shuffle(order)
        order = {s: order[s] for s in range(V)}
        rows = masked_rows('pref', f, rng)
        r = rank_packed(rows)
        ranks.append(r)
        if best is None or r < best[0]: best = (r, trial)
    log('  f=%.2f: rank min %d mean %.1f max %d' % (f, min(ranks), sum(ranks) / len(ranks), max(ranks)))

# the congruence for cst of a masked B
def congruence_columns(M):
    R = M.copy() % 2
    N = R.shape[0]
    cols = []
    while True:
        s = None
        for i in range(N):
            if R[i, i]: s = i; break
        if s is not None:
            v = R[:, s].copy()
        else:
            s2 = None
            for i in range(N):
                if R[i].sum(): s2 = i; break
            if s2 is None: break
            v = R[:, s2].copy(); v[s2] ^= 1
        cols.append(v.copy())
        R = (R ^ np.outer(v, v)) % 2
    return cols

# PRICE PROJECTION for candidate (rank c, row sizes, masked B matrix)
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from pricer import price as pprice
import mpmath as mp
NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
E8SHAPE = [(1, 1320), (2, 1440), (4, 60), (5, 120)]  # the R420 climb proportions (mass fractions)
CLIMB420 = 1320 + 2 * 1440 + 4 * 60 + 5 * 120

def price_proj(label, c, cst, demand_mean, R):
    h, v = 8, 120
    ident = h * R + cst + 2 * v * (h - 1)
    climb = ident - cst
    hist = {}
    for rank, cnt in E8SHAPE:
        mmass = climb * (rank * cnt) / CLIMB420
        hist[rank] = max(1, int(round(mmass / rank)))
    # the COPY children (the retained registers' copy ranks, E8-style at rank 8):
    hist[8] = hist.get(8, 0) + max(1, cst // 8)
    mnow = sum(k * n for k, n in hist.items())
    hist[1] = hist.get(1, 0) + (climb - (mnow - sum(k * n for k, n in hist.items() if k != 1) - (hist[8] * 8 - max(1, cst // 8) * 8)))
    # simpler: recompute — climb mass must be distributed, copies fixed
    climb_now = sum(k * n for k, n in hist.items()) - hist[8] * 8
    hist[1] += climb - climb_now
    cc, _, d = pprice(hist, v, h, R)
    if cc:
        log('  %s: R=%d cst=%d mass=%d (identity %d) mass/v=%.1f: c = %s (%+.2f%%)' %
            (label, R, cst, sum(k * n for k, n in hist.items()) + cst, ident, ident / v,
             mp.nstr(cc, 8), float(cc / NEWF - 1) * 100))
    else:
        log('  %s: R=%d: NO ROOT' % (label, R))

log('CALIBRATION CONTROL: the frozen-shape family at the R434 parameters (expect ~0.00174):')
price_proj('R434-model', 9, 72, 58, 434)
log('PRICE PROJECTION GRID (the sparse word: carriers 240 + mids + retained c):')
for f in (0.4, 0.3, 0.25, 0.2):
    c = best_at.get(f, 20)
    # cst estimate: c gathers at rank ~6 (measured range for E8-ish gathers); demand ~ f x 58
    for cst_est in (72, 90, 120):
        for mids in (60, 80, 100, 120):
            R = 240 + mids + c
            price_proj('f=%.2f c=%d cst=%d mids=%d' % (f, c, cst_est, mids), c, cst_est, f * 58, R)
log('DONE')