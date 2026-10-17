"""Two middle levels (ranks m1 < m2) version of lor_framecell_price.py."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, R, m1, m2, ndel):
    h = {}
    def add(ch):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + 1
    regs = [[1, 2, m1, m2, 9] for _ in range(v)] + [[0, 1, 2, m1, m2, 9] for _ in range(2 * v)] + [[0, m2, 9] for _ in range(R - 2 * v)]
    for i, ch in enumerate(regs): add(ch + ([10, 11] if i < ndel else [11]))
    for _ in range(v): add([0, 2, 9, 10])
    h[10] = h.get(10, 0) + 11
    return h
for m1, m2 in ((4, 7), (3, 6), (5, 7)):
    row = []
    for R in (520, 550, 583, 620, 660):
        c = price(hist(220, R, m1, m2, 660), 220, 11, R)[0]
        row.append('R=%d %+.1f%%' % (R, float((c / P111t - 1) * 100)))
    print('levels', m1, m2, ' '.join(row), flush=True)
