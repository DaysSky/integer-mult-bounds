"""THE DIAL'S EXACT ARITHMETIC (ii19_nat86.py) — the (R, k, dup)-grid COMPUTED!!

THE §752's FIRST COMPUTATION: F(0) = (local×288 + rem×32)/(64×30720) − 1 < 0.
THE EXACT LAWS (verified numerically here with the PRICER'S OWN host_greedy):
(1) rem_mass(R) = 45,360 − 72·R (every hosted residual cuts its slot's rank by w=8
    — exactly 9R hosted — ORDER-FREE: the greedy's choices don't matter for MASS!!);
(2) the gcheck mass-identity (line 131!!): local = 8R + cst + 1,680 (v=120, h=8!!);
(3) => profile mass = 288·cst + 1,935,360 — THE R EXACTLY CANCELS (§685's compensation
    is EXACT, at every R (the dup's +8 local vs the rem's −8!!)) — THE R IS NOT A LEVER;
(4) => F(0) < 0 ⟺ cst ≤ 106 (R-INVARIANT!!!) — the current grammar's cst = 120 (the 14-over!!);
(5) THE PURE-SCATTER RANK BOUND: bit t can ONLY enter target t via the scatter (D reads
    pure-y srcs (content_ok at frame 0!!); B srcs' content ⊆ the gate frame ⊆ perp(t) ∌ t;
    A/C never touch targets!!) => the ret vals must GF(2)-span the e_t's => N ≥ 120
    => cst ≥ 120 — THE (R, k, dup) DIAL IS DEAD; the ONLY route under 106: THE B-PHASE
    (the gathers (the r434's OWN cst = 63!! (its mass 5,129 − 8·439 − 2·111·7 = 63!!!)));
(6) THE (R, shape) PRICE-MAP at cst ∈ {63, 72, 80, 106}: the target-class + the shape-scan.
"""
import os, sys, json
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
from pricer import price, idle_slots, host_greedy
from mpmath import mp, mpf
from collections import Counter
log = lambda *a: print(*a, file=sys.stderr, flush=True)

v, h, K, T = 120, 8, 4, 32
L = 2 * K + 1; a = h - 1; m = 1 + L * a; W = 2 * K * v * T
BUDGET = m * W
slots = {}
for c in idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
slot_mass = sum(c * n for c, n in slots.items())
cap = sum(n * (c // h) for c, n in slots.items())
log('slots %s | slot_mass %d | cap %d | R-ceiling %d | m %d W %d budget %d'
    % (slots, slot_mass, cap, cap // L, m, W, BUDGET))

# ---- (1) the rem law: rem_mass(R) = slot_mass − 8·(9R) — the order-free exact law
log('\n(1) THE REM LAW (the pricer\'s own host_greedy):')
for R in (120, 174, 200, 274, 314, 420, 480):
    rem = host_greedy(slots, R * L, h, mpf('0.0017'), m)
    assert rem is not None, R
    rm = sum(r * z for r, z in rem.items())
    law = slot_mass - 8 * R * L
    log('  R=%3d  rem_mass=%7d  law=%7d  %s  (rem-shape %s)'
        % (R, rm, law, 'OK' if rm == law else 'FAIL', dict(sorted(rem.items()))))

# ---- (3)+(4) the collapse: profile mass = 288·cst + 1,935,360 at EVERY R; root ⟺ cst ≤ 106
log('\n(2) THE COLLAPSE (price() itself — the profile mass at (R, cst)):')
def synth(R, cst, tmpl):
    """the template hist rescaled-by-rank-1 to the identity mass 8R + cst + 1680."""
    mass = h * R + cst + 2 * v * (h - 1)
    d = Counter(tmpl); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
for cst in (63, 106, 107, 120):
    for R in (174, 274, 420):
        c, prof, d = price(synth(R, cst, TARGET), v, h, R)
        pm = sum(r * z for r, z in prof.items())
        law = 288 * cst + (2 * v * (h - 1)) * 288 // (2 * v * (h - 1)) * 0  # placeholder
        pred = 288 * cst + 1_935_360
        log('  cst=%3d R=%3d  profile-mass=%7d  predicted=%7d  %s  F(0)=%+.6f  root=%s'
            % (cst, R, pm, pred, 'OK' if pm == pred else 'FAIL',
               pm / BUDGET - 1, mp.nstr(c, 8) if c is not None else 'NO-ROOT'))

# ---- (5) the boundary bisection at one R: the exact cst-line
log('\n(3) THE cst-LINE at R=274 (root exists ⟺):')
for cst in range(104, 109):
    c, prof, d = price(synth(274, cst, TARGET), v, h, 274)
    log('  cst=%3d  F(0)=%+.7f  root=%s' % (cst, sum(r * z for r, z in prof.items()) / BUDGET - 1,
        mp.nstr(c, 8) if c is not None else 'NO-ROOT'))

# ---- (6) THE (R, shape) PRICE-MAP at cst=63 (the target-class) + the shape-scan
log('\n(4) THE (R) PRICE-MAP at cst=63 (the target-shape, the mass identity-matched):')
best = None
for R in (174, 200, 230, 250, 274, 300, 314, 350, 400, 420, 460, 480):
    c, prof, d = price(synth(R, 63, TARGET), v, h, R)
    if c is not None and (best is None or c > best[1]): best = (R, c)
    log('  R=%3d  root=%s' % (R, mp.nstr(c, 10) if c is not None else 'NO-ROOT'))
log('  THE BEST R at cst=63: %s (c=%s)' % (best[0], mp.nstr(best[1], 10)))

log('\n(5) THE SHAPE-SCAN at (R=274, cst=63) — the mass fixed (3,935), the spread moving:')
base_mass = h * 274 + 63 + 2 * v * (h - 1)
assert base_mass == sum(r * z for r, z in TARGET.items())
shapes = {
    'target': dict(TARGET),
    'interim-like(7-heavy)': {1: 429, 2: 27, 3: 0, 4: 0, 5: 27, 6: 135, 7: 252 + (3935 - 2760 - 252)},
}
# the 7->(1,2) transfer family: k rank-7s become 7 rank-1s (the deep-DAG direction)
for k in (0, 40, 80, 120, 160, 200, 240, 280, 320, 337):
    s = dict(TARGET); take = min(k, s.get(7, 0)); s[7] = s.get(7, 0) - take; s[1] = s.get(1, 0) + 7 * take
    shapes['7to1 x%d' % k] = s
# the 1->2 transfer: rank-1 pairs merged to rank-2 (the r434's own {1:1014, 2:1044} mix)
for k in (0, 100, 200, 300, 400, 500):
    s = dict(TARGET); mv = min(k, s.get(1, 0) // 2); s[1] -= 2 * mv; s[2] = s.get(2, 0) + mv
    shapes['1to2 x%d' % k] = s
for name, s in shapes.items():
    mt = sum(r * z for r, z in s.items())
    if mt != base_mass:
        log('  %-22s MASS %d != %d (skipped)' % (name, mt, base_mass)); continue
    c, prof, d = price(s, v, h, 274)
    log('  %-22s root=%s' % (name, mp.nstr(c, 10) if c is not None else 'NO-ROOT'))

log('\n(6) THE cst-SCAN at R=274 (the target-shape base): which cst classes price?')
for cst in (63, 72, 80, 90, 100, 106):
    c, prof, d = price(synth(274, cst, TARGET), v, h, 274)
    log('  cst=%3d  root=%s' % (cst, mp.nstr(c, 10) if c is not None else 'NO-ROOT'))

# ---- the r434's own cst check (the precedent's cst!!)
log('\n(7) THE PRECEDENT (the r434\'s own cst): mass 5,129 - 8*439 - 2*111*7 = %d'
    % (5129 - 8 * 439 - 2 * 111 * 7))
P111 = mpf('0.001733052823330162099157')
c, prof, d = price(TARGET, v, h, 274)
if c is not None:
    log('  THE TARGET-CLASS REPLAY: c = %s  vs frontier %+.4f%%'
        % (mp.nstr(c, 22), float((c / P111 - 1) * 100)))
print(json.dumps({'slot_mass': slot_mass, 'cap': cap, 'R_ceiling': cap // L,
                  'profile_law': '288*cst + 1935360', 'cst_line': 106}, indent=1))
