from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, R, mids, ndel, tchain):
    h = {}
    def add(ch):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + 1
    regs = [[1, 2] + mids + [9] for _ in range(v)] + [[0, 1, 2] + mids + [9] for _ in range(R)]
    for i, ch in enumerate(regs): add(ch + ([10, 11] if i < ndel else [11]))
    for _ in range(v): add(tchain)
    h[10] = h.get(10, 0) + 11
    return h
for nm, mids in (('zero-level', []), ('one-level r3', [3]), ('one-level r8', [8])):
    row = []
    for R in (640, 680, 720, 760, 800):
        c = price(hist(220, R, mids, 660, [0, 2, 9, 10]), 220, 11, R)[0]
        row.append('%d:%+.2f' % (R, float((c / P111t - 1) * 100)))
    print(nm, ' '.join(row), flush=True)
