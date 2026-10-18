"""THE II19 BREAKTHROUGH STEP 1 — THE c(R) REGIME-BREAK VERIFICATION (ii19_own1.py).

THE USER'S DIRECTIVE: 'make a breakthrough to make II19 the frontier'!!

THE TODAY's DISCOVERY (THE PRICER'S MECHANICS, DERIVED EXACTLY!!):
  c ~ (1 - fill)/(fill * wln)   where  fill = [(mass/v)*288 + (rems/v)*32] / (m*256)
  THE HYPERSENSITIVITY: the word3's -44.85% in c = the +0.16 in mass/v (the fill 0.9969
  vs the frontier's ~0.9943-0.9949!!!).
  THE FILL-CONSERVATION LAW: in the 48-slot regime, d(rems*32) = -d(local*288) EXACTLY
  (the empties' 48x45/5 x 32 = the 9x288!!!) -> THE R-LEVER IS NULL (the grid's flatness!!).
  THE REGIME BREAK: at nres = 9R < ~1450 (R < ~160), the 48/32-slot empties saturate
  (23,232/replica unhosted!!) -> THE FILL COLLAPSES (~0.92!!) -> THE c EXPLODES.
  THE E8's TRUE DEMAND INCIDENCE: 9/line (the SS19-28!!) -> the arrival floor R >= ~135;
  the §1398's own-structure estimate: R ~ 158 — EXACTLY AT THE REGIME EDGE!!!

THE QUESTION (THE GO/NO-GO FOR THE OWN-STRUCTURE BUILD!!!): does the pricer CONFIRM the
c-explosion at the R ~ 135-215?! THE c(R)-BANDS over several mass-exact hist shapes:
  (A) THE TRANSPLANT-STYLE (the word3's proportions!!)
  (B) THE E8-STYLE (the R420's proportions!!)
  (C) THE PIECES-STYLE (the SS1695's: the pieces' [0, 4, the read-dims, 9] chains!!)
AT THE R-GRID 135..460 -> THE c(R)-CURVES -> THE VERDICT!!!
"""
import sys, time
from collections import Counter
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

sys.path.insert(0, 'research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp, mpf
mp.dps = 40
P111 = mp.mpf('0.001733052823330162099157')
FRONTIER = mp.mpf('0.001744386')              # the R434 (the frontier!!)
V, H, CST = 121, 9, 83

# ============ (0) THE REMS' MODEL (the pricer's host_greedy, extracted exactly!!) ============
# the idle_slots(4, 8) x 2v = the slots; the nres = 9R of the width w = 9; the greedy fill!!
def idle_slots(K, a):
    sl = []
    if K >= 1 and 2 * K - 2 > 0:
        sl.append(a * (2 * K - 2))
    for p in range(1, K):
        sl += [2 * p * a, a]
        if 2 * K - 2 * p - 2 > 0:
            sl.append(a * (2 * K - 2 * p - 2))
    return sl

def rems_mass(R):
    """the hosting remainders' total rank-mass per replica (the pricer's own model!!)."""
    a = H - 1
    slots = Counter()
    for c in idle_slots(4, a):
        slots[c] += 2 * V
    nres = R * 9                              # L = 9 (the fixed!!)
    w = H
    # THE GREEDY ORDER (the per-residual saving: the smaller slots first (verified!!)):
    # the 16-slots (J=1) > the 32-slots (J=3) > the 48-slots (J=5)!!
    order = [c for c in (16, 32, 48) if slots.get(c, 0) > 0]
    rem = 0
    left = nres
    for c in order:
        n = slots[c]
        J = c // w
        full = min(n, left // J)
        left -= full * J
        partial = 1 if (left and full < n and left < J) else 0
        if partial:
            rem += c - left * w
            left = 0
            full += 1
        rem += full * (c - J * w) + (n - full) * c
    rem += slots.get(8, 0) * 8                # the unhostable 8-slots (the cap 8 < w 9!!)
    return rem

# ============ (1) THE SHAPES (the mass-exact!!) ============
def _fix_mass(out, mass):
    """the exact-mass correction (the +1/-1 adjustments!!)."""
    d = mass - sum(k * z for k, z in out.items())
    while d:
        if d > 0:
            out[1] = out.get(1, 0) + 1
            d -= 1
        else:
            k = max(out)
            if out.get(k, 0) > 0:
                out[k] -= 1
                d += k
            else:
                out[1] = out.get(1, 0) + 1
                d -= 1
    return {k: z for k, z in out.items() if z}

def shape_transplant(mass):
    """the word3's proportions: {1: 1091, 2: 1710, 3: 331, 4: 144, 8: 8, 9: 4}/6186."""
    prop = {1: 1091, 2: 1710, 3: 331, 4: 144, 8: 8, 9: 4}
    tot = sum(k * z for k, z in prop.items())
    out = {k: max(0, round(mass * prop[k] / tot)) for k in prop}
    return _fix_mass(out, mass)

def shape_e8(mass):
    """the R420's proportions: {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}/5112."""
    prop = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
    tot = sum(k * z for k, z in prop.items())
    out = {k: max(0, round(mass * prop[k] / tot)) for k in prop}
    return _fix_mass(out, mass)

def shape_pieces(mass, R):
    """the SS1695-style: the pieces' [0, 4, the read-dims, 9] chains: the +4s (the pieces!),
    the +1/+2s (the read-dims!), the +1s (the 8->9 finals!) — the mass-exact split."""
    np4 = max(1, int(R * 0.55))               # the pieces' 0->4 climbs!!
    rest = mass - 4 * np4
    n1 = max(1, int(rest * 0.45))
    n2 = (rest - n1) // 2
    out = {1: n1, 2: n2, 4: np4}
    return _fix_mass(out, mass)

# ============ (2) THE c(R)-BANDS!!! ============
log('(2) THE c(R)-BANDS: the shapes x the R-grid (the mass-exact models + the pricer!!)')
log('    the mass identity: M = 9R + %d + %d (the h=9, v=121!!)' % (CST, 2 * V * (H - 1)))
log('    R     mass   rems    fill      c(shape-A)          c(shape-B)          c(shape-C)')
for R in [135, 140, 145, 150, 155, 158, 160, 165, 170, 175, 180, 190, 200, 210, 215,
          230, 250, 280, 300, 339, 380, 420, 440, 451, 463, 484]:
    mass = 9 * R + CST + 2 * V * (H - 1)
    rm = rems_mass(R)
    m = 1 + 9 * (H - 1)
    W = 2 * 4 * V * 32
    fill = (mass * 288 + rm * 32) / (m * W)
    cs = []
    for (nm, sh) in [('A', shape_transplant), ('B', shape_e8), ('C', lambda M: shape_pieces(M, R))]:
        h = sh(mass)
        assert sum(k * z for k, z in h.items()) == mass, 'MASS BROKEN at R=%d: %d != %d' % (
            R, sum(k * z for k, z in h.items()), mass)
        c, prof, d = price(h, V, H, R)
        cs.append('%s' % (mp.nstr(c, 8) if c is not None else 'NONE(%s)' % d.get('error')))
    log('    %d  %d  %d  %.5f  %-18s %-18s %-18s' % (R, mass, rm, fill, cs[0], cs[1], cs[2]))
log('    THE FRONTIER: 0.001744386 (the R434!!) | THE REGIME EDGE: the R ~ 160 (the nres ~ 1440!!)')
log('DONE — THE c(R) REGIME-BREAK VERIFICATION!!')
