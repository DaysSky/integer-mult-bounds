"""Exact scenario prices vs arrivals per section a: R = (#sections) a - v; E8 (180 sections) and I11,1 (330)."""
from mpmath import mp
from pricer import price
from scen import local, P111
R420 = mp.mpf('0.001653826988146798944268')
print('calibration E8 R=420 scenarios (real R420 word: %s, 4.45 moves/register):' % mp.nstr(R420, 8))
for k in (3, 4, 5, 6):
    c = price(local(120, 8, 420, [8] * 9, k), 120, 8, 420)[0]
    print('   k=%d  %s' % (k, mp.nstr(c, 8)))
for name, v, h, cp, S in (('E8', 120, 8, [8] * 9, 180), ('I11,1', 220, 11, [10] * 11, 330)):
    for a in (2.0, 2.25, 2.5, 2.75, 3.0):
        R = int(round(S * a - v))
        row = []
        for k in (3, 4, 5):
            c = price(local(v, h, R, cp, k), v, h, R)[0]
            row.append('k%d %s (%+.1f%%)' % (k, mp.nstr(c, 6), float((c / P111 - 1) * 100)) if c is not None else 'k%d wall' % k)
        print('%-6s a=%.2f R=%4d (%.2f/port): %s' % (name, a, R, R / v, '  '.join(row)), flush=True)
