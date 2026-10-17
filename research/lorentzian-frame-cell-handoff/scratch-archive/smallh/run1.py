from screen import *
import itertools
def box(n, vals):
    return list(itertools.product(vals, repeat=n))
I = lambda n: np.eye(n, dtype=int)
# 1. {0,+-1}^n standard form
for n in (3, 4):
    L = dedupe_lines(box(n, (0, 1, -1)), I(n))
    screen('01^%d std' % n, L, I(n))
# {0,+-1,+-2}^3
L = dedupe_lines(box(3, (0, 1, -1, 2, -2)), I(3)); screen('012^3 std', L, I(3))
# indefinite forms
for n, sig in ((3, (1, 1, -1)), (4, (1, 1, 1, -1)), (4, (1, 1, -1, -1))):
    F = np.diag(sig)
    L = dedupe_lines(box(n, (0, 1, -1)), F); screen('01^%d %s' % (n, sig), L, F)
# F4: D4 roots + (+-1,0,0,0) + (+-1/2)^4 scaled by 2: long roots 2(+-e_i+-e_j)... use integer: D4 roots (+-1,+-1,0,0) scaled x1; short e_i scaled; (1/2)^4 -> multiply all by 2
F4 = [tuple(2*a for a in v) for v in box(4, (0, 1, -1)) if sum(abs(a) for a in v) == 2] + \
     [tuple(2 if i == j else 0 for i in range(4)) for j in range(4)] + list(box(4, (1, -1)))
L = dedupe_lines(F4, I(4)); screen('F4', L, I(4))
# B4 / C4 (16 lines), B3 (9 lines)
B4 = [v for v in box(4, (0, 1, -1)) if sum(abs(a) for a in v) in (1, 2)]
screen('B4', dedupe_lines(B4, I(4)), I(4))
B3 = [v for v in box(3, (0, 1, -1)) if sum(abs(a) for a in v) in (1, 2)]
screen('B3', dedupe_lines(B3, I(3)), I(3))
