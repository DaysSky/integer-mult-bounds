"""A3 shape made REACH-compliant: every cell-stage register's first frame above the cell has rank m1 <= 6
(reach lemma: sum over the <= 8 cell-stage registers carrying x_u of maxreach(rank) >= |R(u)| = 115..129, maxreach =
56/36/25/17/11/6 for ranks 3..8).  Pieces then merge into rank-8 section nodes: carriers [0,1,2,m1,8,9,10,11],
dead [..,2,m1,8,9,11], sources [1,2,m1,8,9,11]; Q chains [0,1,2,m1,8(A3-perp),9,10,11]; empties as price_a3exact2.
Prints c vs P111-tuned at R = 696 (ideal) and the break-even R, for m1 = 3..6."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m1, R):
    h = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    v = 220; B = v / 6
    n_car = 440; car_piece = round(8 * B); car_q = n_car - car_piece
    emp_q = round(2 * B); emp_copy = round(5 * B); dead = round(7 * B)
    extra = R - n_car - emp_q - emp_copy; assert extra >= 0
    add([1, 2, m1, 8, 9, 11], 220); add([0, 1, 2, m1, 8, 9, 11], dead - 220)
    add([0, 1, 2, m1, 8, 9, 10, 11], car_piece - (dead - 220))
    add([0, 1, 2, m1, 8, 9, 10, 11], car_q)
    add([0, m1, 8, 9, 10, 11], emp_q)
    add([0, 9, 10, 11], emp_copy)
    add([0, 9, 11], extra)
    add([0, 1, 10], v)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(m1, R):
    c = price(hist(m1, R), 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
if __name__ == "__main__":
  for m1 in (3, 4, 5, 6):
      be = next((R - 1 for R in range(696, 900, 2) if pct(m1, R) < 0), None)
      print('first mid rank', m1, 'R=696 %+.2f%%' % pct(m1, 696), 'break-even ~', be, flush=True)
