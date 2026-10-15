"""A3 shape with a fraction phi of the cell-stage registers (sources, carriers) taking a low first stop m1 before the
rank-8 node (reach lemma needs >= 2-3 low-stop registers per line among its ~8 cell-stage registers, i.e.
phi >= 1/4..1/3); the rest go cell -> 8 directly.  Break-even R vs P111-tuned."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m1, phi, R):
    h = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    def add2(pre, post, k):          # split k registers: phi with the low stop
        kl = round(phi * k); add(pre + [m1] + post, kl); add(pre + post, k - kl)
    v = 220; B = v / 6
    n_car = 440; car_piece = round(8 * B); car_q = n_car - car_piece
    emp_q = round(2 * B); emp_copy = round(5 * B); dead = round(7 * B)
    extra = R - n_car - emp_q - emp_copy; assert extra >= 0
    add2([1, 2], [8, 9, 11], 220); add2([0, 1, 2], [8, 9, 11], dead - 220)
    add2([0, 1, 2], [8, 9, 10, 11], car_piece - (dead - 220))
    add2([0, 1, 2], [8, 9, 10, 11], car_q)
    add([0, m1, 8, 9, 10, 11], emp_q)
    add([0, 9, 10, 11], emp_copy)
    add([0, 9, 11], extra)
    add([0, 1, 10], v)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(m1, phi, R):
    c = price(hist(m1, phi, R), 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
for m1 in (3, 4):
    for phi in (0.25, 1 / 3, 0.5):
        be = next((R - 1 for R in range(696, 900, 2) if pct(m1, phi, R) < 0), None)
        print('low stop rank', m1, 'phi %.2f' % phi, 'R=696 %+.2f%%' % pct(m1, phi, 696), 'R=715 %+.2f%%' % pct(m1, phi, 715), 'break-even ~', be, flush=True)
