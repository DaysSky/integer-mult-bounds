"""II19 2-CLASS CROSSING — the h=9 window's chance (the user: keep pushing the frontier ON II19).
THE SS1297 VERDICT: the full-II19 class ladder (h=10) is measured dead — the control exposed
the SS1215 '-11%' as the 51-mass-light artifact (the mass-exact truth: -44%); the
monotone curve floors at -25.5% (R=810, bound-violating) / -27.7% (R=860, the counting
bound).  NO CROSSING at h=10: the window (m=82, 2v(h-1)=6,498, width-10 hosting) is the wall.
THE LIVE LEVER: THE WINDOW ITSELF.  The II19 family contains an h=9 system never priced
with this machinery: THE 2-CLASS SUBSET (level-0 + level-1a):
  - 240 lines; the level-0 span 8 dims, the level-1a lines (a,1,0) add the a-coordinate: h=9;
  - the class-blocked decoder: 2 blocks x rank 9 = 18 (the cross-class free on orthogonal
    pairs: legal per the relaxed definition);
  - the within-class orthogonality is the E8 pattern (a.b): the demands = the 63-line
    E8-like perps; the word: 2 E8-transplant subwords + glue;
  - branches 480 (2v), the middle 2x MID, the retained 18, cst ~144 (18 gathers x rank 8);
  - the mass identity at h=9: 9R + cst + 2x240x8 = 9R + cst + 3,840 (the window mass
    16/line vs h=10's 18 and h=8's 14);
  - the counting bound: rows >= 240/18 - 1 = 12.3 -> demands >= 13 -> mid >= ~37 -> R >= ~572;
  - m = 1 + 9x8 = 73 (vs 82 at h=10).
THIS SCRIPT: the mass-exact crossing curve for the 2-class word (the SS1297 methodology
at v=240, h=9): the R-ladder from the counting bound to the full transplant; the roots;
THE CROSSING vs the frontier 0.001744386.
RAM-SAFE."""
import sys, time, resource
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

FRONTIER = 0.001744386
V, H = 240, 9          # the 2-class subset: level-0 + level-1a
BRANCHES = 2 * V       # 480
M = 1 + 9 * (H - 1)    # 73

def hist_2class(R, mid, cst):
    """the structurally-derived transplant hist, MASS-EXACT.
    the R420 climb family x2: {1: 2640, 2: 2880, 4: 120, 5: 240} = 10,080
    + the h=9 extensions (+1 dim per register: single delta-1 children)
    + the E8 copies x2 (18 at rank 8) + the retained's 18 copies at rank 8
    + the middle-scaling; closed mass-exact on rank 1."""
    ident = H * R + cst + 2 * V * (H - 1)
    hist = {1: 2640.0, 2: 2880.0, 4: 120.0, 5: 240.0}     # the R420 family x2 = 10,080
    hist[1] -= 2.0 * (180 - mid)                          # the mids' rank-1 share ~180/class
    hist[1] += 2.0 * V * 1.0 + R                          # the h=9 extension: 480 x 1 + R x 1
    hist[8] = 18.0 + 18.0                                 # the E8 copies x2 + the retained's 18
    mass = sum(k * n for k, n in hist.items())
    hist[1] += ident - mass                               # MASS-EXACT closure
    return {k: int(n) for k, n in hist.items()}, ident

def price_at(R, mid, cst):
    hist, ident = hist_2class(R, mid, cst)
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) <= 2, (mass, ident)
    cc, _, det = pprice(hist, V, H, R)
    return cc, ident

log('II19 2-CLASS CROSSING (level-0 + level-1a): v %d, h %d, m %d; frontier %.9f' % (V, H, M, FRONTIER))
log('structure: branches %d + middle 2x MID + retained 18 (cst ~144); the counting bound: R >= ~572' % BRANCHES)

# THE E8 CONTROL (the calibration anchor: the same machinery at v=120, h=8, the R420 point)
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
def hist_e8(R=420, cst=72):
    ident = 8 * R + cst + 2 * 120 * 7
    hist = {1: 1320.0, 2: 1440.0, 4: 60.0, 5: 120.0, 8: 9.0}
    mass = sum(k * n for k, n in hist.items())
    hist[1] += ident - mass
    return {k: int(n) for k, n in hist.items()}
cc, _, _ = pprice(hist_e8(), 120, 8, 420)
log('CONTROL the E8 R420 true-hist: c = %.15f (published 0.001653826988146798944268)' % cc)

print()
log('=== THE 2-CLASS CROSSING CURVE (mid = (R - 480 - 18)/2; cst 144) ===')
best = None
for R in (560, 572, 600, 640, 680, 720, 760, 800, 858, 900):
    mid = (R - BRANCHES - 18) / 2.0
    if mid < 15: continue
    cc, ident = price_at(R, mid, 144)
    if cc is None:
        log('  R %4d (R/v %.2f, mid %5.1f, mass/v %5.1f): NO ROOT' % (R, R / V, mid, ident / V))
        continue
    pct = (cc / FRONTIER - 1) * 100
    log('  R %4d (R/v %.2f, mid %5.1f, mass/v %5.1f): c = %.9f (%+.2f%% vs frontier)'
        % (R, R / V, mid, ident / V, cc, pct))
    if best is None or cc > best[0]:
        best = (cc, R, mid, ident / V, pct)
print()
if best:
    log('BEST: c = %.9f (%+.2f%% vs frontier) @ R %d (mid %.1f, mass/v %.1f)' % (best[0], best[4], best[1], best[2], best[3]))
    if best[0] > FRONTIER:
        log('THE 2-CLASS WORD BEATS THE FRONTIER at R ~ %d!!  Next: the real construction (the class' % best[1])
        log('demands at mid %.1f/class, the frame legality, the word build, gcheck, the true price).' % best[2])
    else:
        log('No crossing at h=9 either — the window ladder (h=8: frontier / h=9 / h=10) is measured.')
log('DONE')