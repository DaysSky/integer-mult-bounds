"""THE PRICE MODEL AUDIT'S RE-RUN — the honest band with the artifacts separated (SS1488!!).

THE AUDIT'S FINDINGS (pricer.py read, SS1488!!):
1. THE MODEL IS FULLY PARAMETRIC IN h: m = 1 + L(h-1) with L = 2K+1 = 9 (the PIPELINE's
   replica structure: the #463/#510 template's nine-stage bit price!!), a = h-1 (the
   slots), w = h (the residual width!!) — THE WINDOW IS PIPELINE-DERIVED, NOT E8-FITTED!!
   (THE USER'S SS1469 CHALLENGE ANSWERED: the h=9 window is structurally legitimate!!)
2. THE 288x AMPLIFICATION: the root: sum z_r (r/(mW)) (m/r)^q + env = 1 with prof = the
   local hist x T x L (T=32, L=9: the x288!!): the local mass changes are amplified 288x
   in the root -> the ±9 local mass (the cst/basis!!) moves the c by ±26-29%!!!  (The
   observed CST 72->81 swing (-21 points!!) is quantitatively explained!!)
3. THE INT-TRUNCATION ARTIFACT: the SS1406/SS1468 band's hist_true int() truncation loses
   ~4.4 mass -> the c INFLATED ~+14%!!!  THE HONEST HISTS: THE MASS-EXACT (the largest
   remainder!!) — gcheck's own assert demands mass == the identity EXACTLY.
4. THE 'NO ROOT' AT R=520 = THE HOSTING WALL: nres = 9R > cap = 38v = 4598 (the wall at
   R = 511!!) — the hosting capacity 38v/9.
5. THE h=9 HOSTING PENALTY: the residual leftovers rank c-jh = {3,5,7} at h=9 vs {2,4,6}
   at h=8 — a genuine structural h=9 cost.

THIS SCRIPT: THE HONEST BAND: {int-truncated, mass-exact} x {cst 81 (the pivot basis:
all 9 gathers at FULL), cst 73 (the smart basis: 8 dim-8 rows + 1 dim-9: PLAUSIBLE,
unmeasured!!)} x {A,B,C,D} x the R grid + THE CONTROL (the R420's true hist: the exact
reproduction check!!) -> THE BAND WITH THE TRUE ERROR BARS.
"""
import sys
from mpmath import mp, mpf
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
V = 121
H = 9

def hist_model(R, variant, cst, exact):
    climb = 1.0 * H * R + 2.0 * V * (H - 1)
    ident = climb + cst
    if variant == 'A':
        fr = [(1, 1.0)]
    elif variant == 'B':
        fr = [(1, 0.50), (2, 0.25), (5, 0.25)]
    elif variant == 'C':
        fr = [(1, 0.30), (2, 0.20), (5, 0.50)]
    else:  # D: the R420's own climb proportions
        fr = [(1, 0.262), (2, 0.571), (4, 0.048), (5, 0.119)]
    fl = {r: f * climb / r for r, f in fr}
    hist = {r: int(n) for r, n in fl.items()}
    if exact:
        # THE MASS-EXACT: the largest-remainder distribution of the deficit
        mass = sum(r * n for r, n in hist.items())
        rem = ident - mass - cst   # the climb's remaining mass (the copies below!!)
        order = sorted(((fl[r] - int(fl[r]), r) for r in fl), reverse=True)
        i = 0
        while rem > 0:
            _, r = order[i % len(order)]
            hist[r] += 1
            rem -= r
            i += 1
        while rem < 0:
            _, r = order[i % len(order)]
            if hist[r] > 0:
                hist[r] -= 1
                rem += r
            i += 1
    # the copy children: the cst modeling: 81 = the pivot basis (9 gathers at FULL: 9 rank-9!!);
    # 73 = the smart basis (8 dim-8 rows + 1 dim-9: {8: 8, 9: 1}!!)
    if cst == 81:
        hist[9] = hist.get(9, 0) + 9
    else:
        hist[8] = hist.get(8, 0) + 8
        hist[9] = hist.get(9, 0) + 1
    mass = sum(r * n for r, n in hist.items())
    ident = climb + cst
    return hist, mass, ident

print('=== THE CONTROL: the R420 true hist (the model validation at h=8!!) ===')
r420 = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
c, prof, d = pprice(r420, 120, 8, 420)
pub = mpf('0.001653826988146798944268')
print('  R420: c = %s vs published 0.001653826988146798944268: the ratio %.9f' %
      (mp.nstr(c, 20), c / pub))

print()
print('=== THE HONEST BAND AT h=9 (v=121): the artifacts separated!! ===')
for exact in (False, True):
    tag = 'MASS-EXACT' if exact else 'int-truncated'
    print('--- the hists: %s ---' % tag)
    for cst in (81, 73):
        print('  cst = %d (%s):' % (cst, 'the pivot basis: 9 gathers at FULL' if cst == 81
              else 'the smart basis: 8 dim-8 + 1 dim-9 (plausible, unmeasured!!)'))
        for R in (286, 300, 325, 350):
            line = '    R %3d: ' % R
            for var in ('A', 'B', 'C', 'D'):
                hist, mass, ident = hist_model(R, var, cst, exact)
                ok = (mass == ident)
                c, prof, d = pprice(hist, V, H, R)
                if c is None:
                    line += '%s NO-ROOT  ' % var
                else:
                    pct = (float(c) / FRONTIER - 1) * 100
                    line += '%s %+.2f%% (m%s)  ' % (var, pct, 'ok' if ok else 'OFF!!')
            print(line)
print()
print('=== THE ARTIFACT SIZES (the same R/variant across the columns!!) ===')
print('  the truncation artifact: the int vs the exact at cst=81 (the ~+14%% expectation!!)')
print('  the basis sensitivity: the cst 81 vs 73 (the ~±26-point expectation!!)')
print('DONE')
