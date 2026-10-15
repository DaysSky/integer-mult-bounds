"""Marginal value of each stop in the A3 shape (two-level Q, mid m, Q-node q) at fixed R: remove one stop class at a
time (chains re-joined), report c change.  Diagnostic only (mass kept consistent)."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def build(m, q, R, drop=()):
    v = 220; B = v / 6
    n_car = 440
    car_piece = round(8 * B); car_q = n_car - car_piece
    emp_q = round(2 * B); emp_copy = round(5 * B); dead = round(7 * B)
    extra = R - n_car - emp_q - emp_copy
    groups = [('src', [1, 2, m, 9, 11], 220), ('deadcar', [0, 1, 2, m, 9, 11], dead - 220),
              ('car', [0, 1, 2, m, 9, 10, 11], car_piece - (dead - 220)), ('carQ', [0, 1, 2, m, q, 9, 10, 11], car_q),
              ('empQ', [0, m, q, 9, 10, 11], emp_q), ('copy', [0, 9, 10, 11], emp_copy), ('extra', [0, 9, 11], extra),
              ('tgt', [0, 1, 10], v)]
    h = {}
    for name, ch, k in groups:
        ch = [x for x in ch if not any(name == g and x == st for g, st in drop) or x in (ch[0], ch[-1])]
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(h, R):
    c = price(h, 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
m, q, R = 3, 8, 696
print('base %+.2f%%' % pct(build(m, q, R), R))
for name, st in [('src', 2), ('src', m), ('src', 9), ('deadcar', 1), ('deadcar', 2), ('deadcar', m), ('deadcar', 9),
                 ('car', 1), ('car', 2), ('car', m), ('car', 9), ('car', 10), ('carQ', 1), ('carQ', 2), ('carQ', m),
                 ('carQ', q), ('carQ', 9), ('carQ', 10), ('empQ', m), ('empQ', q), ('empQ', 9), ('empQ', 10),
                 ('copy', 9), ('copy', 10), ('tgt', 1)]:
    print('drop', name, st, '%+.2f%%' % pct(build(m, q, R, [(name, st)]), R), flush=True)
