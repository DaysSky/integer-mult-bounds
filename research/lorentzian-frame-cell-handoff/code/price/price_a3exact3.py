"""A3 shape, two-level Q-deliveries, with SEPARATE ranks: pieces live in rank-mp nodes (exclusive-part pieces are
S & x-perp nodes, rank 8), Q chains go cell -> mq -> q (A3-perp, rank 8) -> section.  Exact counts at v = 220 as in
price_a3exact2.py.  Prints break-even R per (mp, mq, q)."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(mp_, mq, q, R):
    h = {}
    def add(ch, k):
        assert k >= 0, (ch, k)
        assert all(b > a for a, b in zip(ch, ch[1:])), ch
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    v = 220; B = v / 6
    n_car = 440
    car_piece = round(8 * B); car_q = n_car - car_piece
    emp_q = round(2 * B); emp_copy = round(5 * B); dead = round(7 * B)
    extra = R - n_car - emp_q - emp_copy; assert extra >= 0
    add([1, 2, mp_, 9, 11], 220); add([0, 1, 2, mp_, 9, 11], dead - 220)
    add([0, 1, 2, mp_, 9, 10, 11], car_piece - (dead - 220))
    add([0, 1, 2, mq, q, 9, 10, 11], car_q)
    add([0, mq, q, 9, 10, 11], emp_q)
    add([0, 9, 10, 11], emp_copy)
    add([0, 9, 11], extra)
    add([0, 1, 10], v)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(mp_, mq, q, R):
    c = price(hist(mp_, mq, q, R), 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
if __name__ == '__main__':
    for mp_, mq, q in ((8, 3, 8), (8, 4, 8), (8, 5, 8), (8, 6, 8), (8, 3, 7), (7, 3, 8), (6, 3, 8), (3, 4, 8)):
        prev = None
        for R in range(696, 820, 2):
            p = pct(mp_, mq, q, R)
            if p is not None and p < 0:
                print('pieces', mp_, 'Qmid', mq, 'Qnode', q, 'R696 %+.2f%%' % pct(mp_, mq, q, 696), 'break-even ~', R - 1, flush=True); break
