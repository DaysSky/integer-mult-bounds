"""Exact prices of Lorentzian frame-cell word SHAPES (R420-like chains, h=11, v=220) vs P111-tuned.
Registers: sources 1->2->m->9->10->11; carriers 0->1->2->m->9->10->11; extras 0->m->9->10->11 (or ->11 if dead);
targets 0->2->9->10 (cell read, in-chain section, t-perp); 11 totals copied at rank 10.
Middle node rank m in 3..8.  Deliveries: 3 per target (660) end at t-perp; other registers die at full."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, R, m, ndel):
    h = {}
    def add(ch):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + 1
    regs = []
    for _ in range(v): regs.append([1, 2, m, 9])
    ncar = 2 * v
    for _ in range(ncar): regs.append([0, 1, 2, m, 9])
    for _ in range(R - ncar): regs.append([0, m, 9])
    # first ndel registers are deliveries (end 9 -> 10 -> 11), rest die (9 -> 11)
    for i, ch in enumerate(regs):
        add(ch + ([10, 11] if i < ndel else [11]))
    for _ in range(v): add([0, 2, 9, 10])
    h[10] = h.get(10, 0) + 11
    return h
for m in (4, 5, 6, 7):
    row = []
    for R in (550, 583, 620, 660, 700):
        c = price(hist(220, R, m, 660), 220, 11, R)[0]
        row.append('R=%d %+.1f%%' % (R, float((c / P111t - 1) * 100)) if c else 'R=%d wall' % R)
    print('node rank', m, ' '.join(row), flush=True)
