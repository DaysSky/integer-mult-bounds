"""Shape pricing of an R420-type cell word on I_{11,1}: lines -> cells(2) -> quads(qr) -> sections(9) -> t-perp(10) -> 11.
3 registers per cell; 6 cells per 4-frame; v lines (v/4 frames).  Needers (3 per target) climb to t-perp, the rest dead."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, R, qr=4, extra_stop=None, tgt=(0, 2, 10)):
    h = {}
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    mid = [qr] + ([extra_stop] if extra_stop else []) + [9]
    cells = 6 * v // 4; regs = 3 * cells          # = v + R0
    R0 = regs - v
    needers = 3 * v; dead = regs - needers
    # sources: keepers read by targets at cells, then block node (rank qr), host section, t-perp, full
    add([1, 2] + mid + [10, 11], v)
    ncar = 2 * v; nemp = cells
    # carriers and empties: (needers - v) of them climb to t-perp, the rest die at the section frame
    nd_left = needers - v
    car_n = min(ncar, nd_left); add([0, 1, 2] + mid + [10, 11], car_n); add([0, 1, 2] + mid + [11], ncar - car_n)
    nd_left -= car_n
    emp_n = min(nemp, nd_left); add([0, 2] + mid + [10, 11], emp_n); add([0, 2] + mid + [11], nemp - emp_n)
    add([0, 9, 11], R - R0)                      # any extra helpers: dead empties
    add(list(tgt), v)
    h[10] = h.get(10, 0) + 11
    return h, R0
def pct(v, R, **kw):
    hh, R0 = hist(v, R, **kw)
    c = price(hh, v, 11, R)[0]
    return (float((c / P111t - 1) * 100) if c else None), R0
for v in (220, 216):
    for qr in (4, 5, 6):
        for es in (None, 7):
            R0 = 3 * (6 * v // 4) - v
            p, _ = pct(v, R0, qr=qr, extra_stop=es)
            print('v', v, 'quad rank', qr, 'extra stop', es, 'R0', R0, 'vs P111-tuned %+.2f%%' % p)
