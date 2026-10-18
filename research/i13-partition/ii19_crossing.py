"""II19 CROSSING — the decisive price curve for the class-sparse words (the user: keep
pushing the frontier ON II19).
THE CORRECTION THAT REOPENS II19: the SS1221 mass-scaled hists (-30 to -45%) were the
WRONG shape family (lazy proportions).  The SS1215 STRUCTURALLY-DERIVED hists (the R420's
own climb family x3 + the h=10 extension children) priced the class word at -8 to -11%.
The E8 arc's calibration decides it: the frozen-shape family reproduces the R420's
published c EXACTLY (1.0000) — the E8SHAPE proportions ARE the R420's own histogram, and
the SS1215 hists are that family x3 + extensions.  THE HONEST CLASS-WORD PRICE: -8 to -11%.
THIS SCRIPT: the SS1215-style price curve over R (the class-sparse ladder: the middle
shrinks with the demands): THE CROSSING POINT where c = the frontier 0.001744386.
  - the hist: the R420 family x3 (sources/carriers/quads/targets climbs: {1: 3960,
    2: 4320, 4: 180, 5: 360} = 15,120) + the E8 copies x3 (27 at rank 8) + the retained's
    copies (the cst 235-style ranks) + the middle-scaling (the mids' rank-1 share) +
    the h=10 extensions (delta-1 and delta-2 variants);
  - MASS-EXACT closure at every point (the SS1215 lesson: +-0.3% mass = +-35% c);
  - the roots check (the regime question at R/v 2.2-3.6);
  - THE CROSSING: the R where the class-sparse word beats the frontier.
RAM-SAFE (the phase-1 lesson: no exponential enumerations)."""
import sys, time, resource
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

FRONTIER = 0.001744386
V, H = 361, 10
BRANCHES = 2 * V  # 722

def hist_cross(R, mid, cst, retained, ext_delta2=False):
    """the SS1215-style structurally-derived hist, MASS-EXACT."""
    ident = H * R + cst + 2 * V * (H - 1)
    hist = {1: 3960.0, 2: 4320.0, 4: 180.0, 5: 360.0}   # the R420 climb family x3 = 15,120
    # the middle-scaling: the mids' share of the rank-1 children ~ 180/class at mid 180
    hist[1] -= 3.0 * (180 - mid)
    # the h=10 extensions: the sources/targets 720 registers x 2 dims; the helpers R x 2
    if ext_delta2:
        hist[2] += 720.0 + R
    else:
        hist[1] += 1440.0 + 2.0 * R
    # the copies: the E8's x3 (27 at rank 8) + the retained's (the cst 235-style ranks:
    # [8]x9 + [9]x18 + [1]x1 = mass 235)
    hist[8] = hist.get(8, 0.0) + 27.0 + round(9.0 * cst / 235.0)
    hist[9] = hist.get(9, 0.0) + round(18.0 * cst / 235.0)
    hist[1] += round(1.0 * cst / 235.0)
    # MASS-EXACT closure on rank 1
    mass = sum(k * n for k, n in hist.items())
    hist[1] += ident - mass
    return {k: int(n) for k, n in hist.items()}, ident

def price_at(R, mid, cst, retained, ext_delta2=False):
    hist, ident = hist_cross(R, mid, cst, retained, ext_delta2)
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) <= 2, (mass, ident)
    cc, _, det = pprice(hist, V, H, R)
    return cc, ident

log('II19 CROSSING SCAN — the SS1215-style curve; frontier %.9f' % FRONTIER)
log('structure: branches %d + middle 3x MID + retained; v %d h %d; m = %d' % (BRANCHES, V, H, 1 + 9 * (H - 1)))

# THE SS1215 REPRODUCTION CONTROL (R=1290, mid=180, cst=235, delta-1: expect ~0.00155)
cc, ident = price_at(1290, 180, 235, 28, False)
log('CONTROL SS1215 point (R=1290, mid=180, cst=235, delta-1): c = %s (expect ~0.00155, -11%%)' % (cc if cc is None else '%.9f' % cc))
cc2, _ = price_at(1290, 180, 235, 28, True)
log('CONTROL SS1215 delta-2 variant: c = %s (expect ~0.00160, -8%%)' % (cc2 if cc2 is None else '%.9f' % cc2))

print()
log('=== THE CROSSING CURVE (mid = (R - 722 - retained)/3; cst 235; delta-1 | delta-2) ===')
best = None
for R in (810, 860, 900, 950, 1000, 1060, 1120, 1200, 1290, 1350):
    mid = (R - BRANCHES - 28) / 3.0
    if mid < 10: continue
    for ed2 in (False, True):
        cc, ident = price_at(R, mid, 235, 28, ed2)
        tag = 'd2' if ed2 else 'd1'
        if cc is None:
            log('  R %4d (R/v %.2f, mid %5.1f, mass/v %5.1f) %s: NO ROOT' % (R, R / V, mid, ident / V, tag))
            continue
        pct = (cc / FRONTIER - 1) * 100
        log('  R %4d (R/v %.2f, mid %5.1f, mass/v %5.1f) %s: c = %.9f (%+.2f%% vs frontier)'
            % (R, R / V, mid, ident / V, tag, cc, pct))
        if best is None or cc > best[0]:
            best = (cc, R, mid, ident / V, tag, pct)
print()
if best:
    log('BEST: c = %.9f (%+.2f%% vs frontier) @ R %d (mid %.1f, mass/v %.1f, %s)' % (best[0], best[5], best[1], best[2], best[3], best[4]))
    if best[0] > FRONTIER:
        log('THE CROSSING EXISTS INSIDE THE SCANNED BAND — the class-sparse word BEATS THE FRONTIER at R ~ %d!!' % best[1])
        log('FEASIBILITY: mid %.1f/class = the demands ~%.0f lines/target — the sparse-cancellation construction target!!' % (best[2], best[2] * 63.0 / 180.0))
    else:
        log('No crossing in the band — extend the ladder (deeper masks/cancellations) or refine the shape.')
log('DONE')