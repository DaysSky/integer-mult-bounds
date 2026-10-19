"""(1) The pricer's closed form; (2) stage count; (3) the x-threshold per window h; (4) transplant calibration."""
from _common import price, mp, FRONTIER, R434, COPY_R434, W4T, COPY_W4T, R420, COPY_R420, transplant, pct
from pricer import idle_slots

print('(1) closed form: profile mass = T L (cst + 2 K a v), deficit = T (2 K v - L cst); R- and h-independent')
K, T, L = 4, 32, 9
for nm, hist, v, h, R in (('P111', {1: 1321, 2: 1342, 3: 80, 4: 47, 5: 102, 6: 10, 7: 18}, 111, 8, 439),
                          ('R420', R420, 120, 8, 420), ('r434', R434, 111, 8, 434), ('W4 tuned', W4T, 121, 9, 472)):
    a = h - 1; cst = sum(r * z for r, z in hist.items()) - h * R - 2 * v * a
    c, _, d = price(hist, v, h, R)
    ok = d['mass'] == T * L * (cst + 2 * K * a * v) and d['deficit'] == T * (2 * K * v - L * cst)
    print('  %-9s v=%d h=%d R=%d cst=%d  c=%s  mass %d  deficit %d  closed form %s'
          % (nm, v, h, R, cst, mp.nstr(c, 16), d['mass'], d['deficit'], 'EXACT' if ok else 'MISMATCH'))
print('  (HANDOFF line 1679 writes T(h v - (h+1) cst); that equals the pricer only at h = 8.)')

print('\n(2) stage count s = 2K+1: hosting wall R/v and prices of the record words')
for h in (8, 9):
    print('  h=%d  Rmax/v:' % h, {2 * k + 1: round(sum(2 * (c // h) for c in idle_slots(k, h - 1)) / (2 * k + 1), 3)
                                for k in (2, 3, 4, 5)})
for nm, hist, v, h, R in (('r434', R434, 111, 8, 434), ('W4 tuned', W4T, 121, 9, 472)):
    print('  %-9s' % nm, {2 * k + 1: (('%+.2f%%' % p) if p is not None else e) for k in (3, 4, 5)
                         for p, e in [pct(hist, v, h, R, K=k)]})
print('  low-R W4 shape at v=121: s=9 vs s=7')
for R in (150, 200, 240, 276):
    hs = transplant(W4T, COPY_W4T, 121, 9, R, COPY_W4T)
    print('    R=%d  s=9 %+.2f%%  s=7 %+.2f%%' % (R, pct(hs, 121, 9, R, K=4)[0], pct(hs, 121, 9, R, K=3)[0]))

print('\n(3) x needed to tie the frontier with a frontier-quality middle (r434 shape, v=111, R/v=3.91)')
for h in (8, 9, 10):
    row = []
    for cst in (63, 57, 50, 44):
        cop = {7: cst // 7}; cop.update({cst % 7: 1} if cst % 7 else {})
        row.append('x=%.3f %+6.1f%%' % (cst / 111, pct(transplant(R434, COPY_R434, 111, h, 434, cop), 111, h, 434)[0]))
    print('  h=%d  ' % h + '   '.join(row))

print('\n(4) transplant calibration on the one published puncture (R420 -> P111)')
c420 = price(R420, 120, 8, 420)[0]
for R in (389, 439):
    c = price(transplant(R420, COPY_R420, 111, 8, R, {7: 9}), 111, 8, R)[0]
    print('  R420 shape at (111, 8, cst 63, R=%d): %+.2f%% vs R420' % (R, float((c / c420 - 1) * 100)))
print('  published P111 (R=439): %+.2f%% vs R420' % float((mp.mpf('0.001733052823330162099157') / c420 - 1) * 100))
