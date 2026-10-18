"""II19 2-CLASS TRUE HIST — the refined shallow-word price band (the go/no-go for the build).
The SS1301 crossing (+0.58% at R=560 / -0.53% at R=572, the counting bound) used the
transplant-family hist which DISTORTS at shallow mid (the negative closure: the rank-1
collapse from 3,382 to 1,296).  THE TRUE WORD'S HISTOGRAM DECIDES.
THIS SCRIPT: the honest shallow-word structure — MASS-EXACT BY CONSTRUCTION (no closure
distortion possible):
  the sources+targets 3,840 (240x8 + 240x8, the fixed 2v(h-1));
  the helpers 9R (the mids 9(R-18) at the piece frames + the retained 18x9 at the gather
  frames); the copies 144 (the retained's 18 copy children at rank 8).
THE VARIANTS (the children's delta distribution — the +-30%-in-c shape sensitivity):
  A FINE: all delta-1 children;  B E8-STYLE: the R420-mix for the sources/targets, the
  piece-frame climbs for the mids;  C COARSE: the heavier mixes.
THE VERDICT: the band at the legal floor (R >= 573, the counting bound demands >= 13):
  entirely below -> the build would confirm death; straddling/clearing -> THE BUILD DECIDES.
PLUS: the demand side — the class perps, the greedy cancellation junks at the counting
bound, and the sharing structure (distinct junks: the E8 arc's lesson: the uncoordinated
greedy destroys the sharing; the canonical-partner coordination preserves it).
RAM-SAFE (no exponential enumerations)."""
import sys, time, resource, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

FRONTIER = 0.001744386
V2, H2 = 240, 9
CST = 144

# ============ PART 1: the 2-class system, the decoder, the demands ============
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
AL = list(d8.values())
A = len(AL)
# the 2-class lines: (alpha,0,0) and (alpha,1,0); the form: alpha.beta + a*d + b*c
L = []
CLS = []
for al in AL:
    L.append(list(al) + [0, 0]); CLS.append(0)
for al in AL:
    L.append(list(al) + [1, 0]); CLS.append(1)
L = np.array(L, dtype=float)
V = len(L)
FORM = np.zeros((10, 10))
FORM[:8, :8] = np.eye(8)
FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
log('2-class system: %d lines (%d level-0 + %d level-1a); h = 9' % (V, A, A))
assert V == 240

# the class perps (the within-class orthogonality)
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and CLS[s] == CLS[t] and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
sizes = [bin(m).count('1') for m in PERP]
log('class-perp sizes: min %d mean %.1f max %d' % (min(sizes), sum(sizes) / V, max(sizes)))

# the class-blocked decoder B: diag 1, support inside {t} u class-perp(t)
B = np.zeros((V, V), dtype=int)
np.fill_diagonal(B, 1)
for t in range(V):
    for s in range(V):
        if (PERP[t] >> s) & 1:
            B[t][s] = 1
def pack(M):
    return [int(''.join(str(int(x)) for x in row[::-1]), 2) for row in M]
def rank_packed(rows):
    piv = {}
    for row in rows:
        red = row
        while red:
            p = (red & -red).bit_length() - 1
            if p in piv: red ^= piv[p]
            else: piv[p] = red; break
    return len(piv)
Brows = pack(B)
log('class-blocked decoder rank: %d (expected 18)' % rank_packed(Brows))

# the cancellation demands: greedy k=1/2 within the class; + the canonical first-partner
def junks_greedy(npairs):
    out = []
    for t in range(V):
        cur = PERP[t]; used = set()
        partners = [s for s in range(V) if (PERP[t] >> s) & 1]
        for _ in range(npairs):
            bw = bin(cur).count('1'); best = None
            for x in partners:
                if x in used: continue
                cand = cur ^ (PERP[t] & PERP[x])
                w = bin(cand).count('1')
                if w < bw and (best is None or w < best[0]):
                    best = (w, x, cand)
            if best is None: break
            cur = best[2]; used.add(best[1])
        out.append(cur)
    return out
def junks_canonical(npairs):
    """the coordinated choice: the min-index partners (the shared prefix structure)."""
    out = []
    for t in range(V):
        cur = PERP[t]
        partners = sorted(s for s in range(V) if (PERP[t] >> s) & 1)
        for x in partners[:npairs]:
            cur = cur ^ (PERP[t] & PERP[x])
        out.append(cur)
    return out

print()
log('=== THE DEMANDS AT THE COUNTING BOUND (rows >= %d at c=18) ===' % (V // 18 - 1 + 1))
for label, fn, k in (('greedy k=1', junks_greedy, 1), ('greedy k=2', junks_greedy, 2),
                     ('canonical k=1', junks_canonical, 1), ('canonical k=2', junks_canonical, 2)):
    js = fn(k)
    ws = [bin(m).count('1') for m in js]
    dist = len(set(js))
    legal = min(ws) >= 13
    ovl = []
    for a in range(0, V, 13):
        for b in range(a + 1, V, 13):
            ovl.append(bin(js[a] & js[b]).count('1'))
    log('%s: junk sizes min %d mean %.1f max %d | distinct %d/%d (sharing %s) | overlaps mean %.1f | counting-bound-legal %s'
        % (label, min(ws), sum(ws) / V, max(ws), dist, V,
           'WEAK' if dist > 200 else ('moderate' if dist > 80 else 'STRONG'),
           sum(ovl) / len(ovl), 'YES' if legal else 'NO'))

# ============ PART 2: the refined-hist price band ============
def hist_true(R, variant):
    """MASS-EXACT BY CONSTRUCTION (the honest shallow structure)."""
    ident = H2 * R + CST + 2 * V * (H2 - 1)
    mids = R - 18
    if variant == 'A':      # FINE: all delta-1
        hist = {1: 3840.0 + 9.0 * R, 8: 18.0}
    elif variant == 'B':    # E8-STYLE
        hist = {1: 2400.0 + 3.0 * mids + 18.0, 2: 720.0 + 3.0 * mids, 8: 36.0}
    elif variant == 'D':    # THE E8'S OWN PROPORTIONS (the R420's measured climb shape)
        climb = 9.0 * R + 3840.0
        hist = {1: 0.262 * climb, 2: 0.571 * climb / 2.0, 4: 0.048 * climb / 4.0,
                5: 0.119 * climb / 5.0, 8: 18.0}
    else:                   # COARSE
        hist = {1: 1200.0 + 18.0, 2: 960.0 + 2.0 * mids, 4: 180.0, 5: 1.0 * mids, 8: 36.0}
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) < 2, (variant, mass, ident)
    return {k: int(n) for k, n in hist.items()}

print()
log('=== THE REFINED-HIST PRICE BAND (mass-exact by construction; cst %d) ===' % CST)
# the control: the E8 R420 true-hist (the perfect calibration anchor)
def hist_e8():
    ident = 8 * 420 + 72 + 2 * 120 * 7
    hist = {1: 1320.0, 2: 1440.0, 4: 60.0, 5: 120.0, 8: 9.0}
    mass = sum(k * n for k, n in hist.items())
    hist[1] += ident - mass
    return {k: int(n) for k, n in hist.items()}
cc, _, _ = pprice(hist_e8(), 120, 8, 420)
log('CONTROL the E8 R420 true-hist: c = %.15f (published 0.001653826988146798944268)' % cc)

band = {}
for R in (560, 573, 590, 620, 660, 700, 760):
    for var in ('A', 'B', 'C', 'D'):
        hist = hist_true(R, var)
        cc, _, det = pprice(hist, V, H2, R)
        if cc is None:
            log('  R %3d %s: NO ROOT' % (R, var))
            continue
        pct = (cc / FRONTIER - 1) * 100
        log('  R %3d (mid/class %5.1f) %s: c = %.9f (%+.2f%% vs frontier)' % (R, (R - 480 - 18) / 2.0, var, cc, pct))
        band.setdefault(R, []).append((var, cc, pct))
print()
live = [(R, vs) for R, vs in band.items() if any(c > FRONTIER for _, c, _ in vs)]
if live:
    log('THE BAND IS LIVE — the frontier is reachable at: %s' % ', '.join(str(r) for r, _ in live))
    log('THE BUILD DECIDES: the true word at R ~ %d (the legal floor 573+) -> gcheck -> the exact hist -> the true price.' % live[-1][0])
else:
    best = max((c for vs in band.values() for _, c, _ in vs), default=None)
    if best:
        log('The band is entirely below the frontier (best %.4f = %+.2f%%) — the refined shapes close the 2-class hope.' % (best, (best / FRONTIER - 1) * 100))
    else:
        log('No priceable point — the regime question applies.')
log('DONE')