"""I_{13,1} port of price/price_a3exact2.py (A3-parity shape, two-level Q-deliveries), generic h.  Per 6 targets
(one A3 block): sources 6 pieces; carriers 12 = 8 pieces + 4 Q; empties 7 = 2 Q + 5 copies; 7 dead pieces.  Chains
(h = 13, sections rank h-2 = 11, A3-perp node rank q): dead [.. m, h-2, h]; carriers 0-1-2-m-(h-2)-(h-1)-h; Q carriers
0-1-2-m-q-(h-2)-(h-1)-h; Q empties 0-m-q-(h-2)-(h-1)-h; copies 0-(h-2)-(h-1)-h; extra dead empties 0-(h-2)-h;
targets 0-1-(h-1); totals h at h-1.  I11 control (v 220, h 11) must reproduce price_a3exact2.
usage: python3 price_i13_a3shape.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'price'))
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, h, m, q, R):
    hh = {}
    def add(ch, k):
        assert k >= 0, (ch, k)
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + k
    B = v / 6; n_car = 2 * v
    car_piece = round(8 * B); car_q = n_car - car_piece
    emp_q = round(2 * B); emp_copy = round(5 * B); dead = round(7 * B)
    extra = R - n_car - emp_q - emp_copy; assert extra >= 0, (R, extra)
    add([1, 2, m, h - 2, h], v); add([0, 1, 2, m, h - 2, h], dead - v)
    add([0, 1, 2, m, h - 2, h - 1, h], car_piece - (dead - v))
    add([0, 1, 2, m, q, h - 2, h - 1, h], car_q)
    add([0, m, q, h - 2, h - 1, h], emp_q)
    add([0, h - 2, h - 1, h], emp_copy)
    add([0, h - 2, h], extra)
    add([0, 1, h - 1], v)
    hh[h - 1] = hh.get(h - 1, 0) + h
    assert sum(k * c for k, c in hh.items()) == (h - 1) * v + h * R + (h - 1) * v + (h - 1) * h
    return hh
def pct(v, h, m, q, R):
    c = price(hist(v, h, m, q, R), v, h, R)[0]
    return float((c / P111t - 1) * 100) if c else None
def be(v, h, m, q):
    base = 2 * v + round(2 * v / 6) + round(5 * v / 6)
    lo, hi = base, 5 * v
    if (pct(v, h, m, q, lo) or -1) < 0: return base, None
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if (pct(v, h, m, q, mid) or -1) > 0: lo = mid
        else: hi = mid
    return base, lo
for (name, v, h, cases) in (('I11', 220, 11, ((3, 7), (3, 8), (5, 8))), ('I13', 364, 13, ((3, 9), (3, 10), (5, 9), (5, 10), (7, 10), (5, 8)))):
    for m, q in cases:
        base, b = be(v, h, m, q)
        print('%s mid %d Qnode %d | ideal R %d (%.2f v) %+.2f%% | break-even R %s (%.2f v, room %s = %.2f per target)' % (
            name, m, q, base, base / v, pct(v, h, m, q, base), b, (b or 0) / v, (b - base) if b else None, ((b - base) / v) if b else float('nan')), flush=True)
