"""A3 shape with two-level Q-deliveries, exact counts at v = 220 (blocks scaled: per 6 targets: sources 6 pieces;
carriers 12 = 8 pieces + 4 Q; empties 7 = 2 Q + 5 copies; 7 dead pieces).  Q chains: carriers 0-1-2-m-q-9-10-11,
empties 0-m-q-9-10-11 (q = rank of the A3-perp node, 7 or 8).  Overhead = extra dead empties 0-9-11."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m, q, R):
    h = {}
    def add(ch, k):
        assert k >= 0, (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    v = 220; B = v / 6
    n_src = 220; n_car = 440
    car_piece = round(8 * B); car_q = n_car - car_piece          # 293, 147
    emp_q = round(2 * B); emp_copy = round(5 * B)                 # 73, 183
    dead = round(7 * B)                                           # 257
    E_base = emp_q + emp_copy
    extra = R - n_car - E_base; assert extra >= 0, (R, extra)
    # dead pieces: all 220 sources + 37 carriers
    add([1, 2, m, 9, 11], 220); add([0, 1, 2, m, 9, 11], dead - 220)
    add([0, 1, 2, m, 9, 10, 11], car_piece - (dead - 220))
    add([0, 1, 2, m, q, 9, 10, 11], car_q)
    add([0, m, q, 9, 10, 11], emp_q)
    add([0, 9, 10, 11], emp_copy)
    add([0, 9, 11], extra)
    add([0, 1, 10], v)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
base = 440 + round(2 * 220 / 6) + round(5 * 220 / 6)
print('ideal R', base)
for m, q in ((3, 7), (3, 8), (5, 8), (4, 7)):
    out = []
    for R in (base, base + 30, base + 60, base + 90, base + 120):
        c = price(hist(m, q, R), 220, 11, R)[0]
        out.append('R=%d %s' % (R, '%+.2f%%' % float((c / P111t - 1) * 100) if c else 'n/a'))
    print('mid', m, 'Qnode', q, ' | '.join(out), flush=True)
