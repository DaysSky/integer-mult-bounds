"""Two-level chain-shape prices vs P111-tuned, all mid-rank pairs; same model as lor_fc_price3 (660 deliveries)."""
from pricer import price
from mpmath import mp
import itertools
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
for m1, m2 in itertools.combinations(range(3, 9), 2):
    for tname, tch in (('t0-2-9-10', [0, 2, 9, 10]),):
        row = []
        for R in (520, 550, 580, 610, 640):
            c = price(hist(220, R, [m1, m2], 660, tch), 220, 11, R)[0]
            row.append('%d:%+.2f' % (R, float((c / P111t - 1) * 100)))
        print('two-level', m1, m2, tname, ' '.join(row), flush=True)
# one level + target node read (target 0-2-m-9-10)
for m in range(3, 9):
    row = []
    for R in (520, 550, 580, 610, 640):
        c = price(hist(220, R, [m], 660, [0, 2, m, 9, 10]), 220, 11, R)[0]
        row.append('%d:%+.2f' % (R, float((c / P111t - 1) * 100)))
    print('one-level+node-read', m, ' '.join(row), flush=True)
