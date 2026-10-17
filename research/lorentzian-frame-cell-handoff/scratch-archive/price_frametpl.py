"""Exact-shape price of the frame-top in-chain template (per frame: 4 keepers line->cell->section->t-perp,
8 carriers + 4 empties through cell->hub->section; 4 delivered merged E, 4 dead p2, 4 in-chain-only),
targets 0 -> section -> t-perp.  F frames (default 55), extra helpers as dead empties."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def shape(F=55, hub=5, cell=2, sec=9, extra=0):
    h = {}
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    v = 4 * F
    add([1, cell, sec, 10, 11], 4 * F)                 # keepers = sources -> third needer
    # 8 carriers + 4 empties per frame through the hub: 4 delivered (to t-perp), 8 dead at the section
    add([0, 1, cell, hub, sec, 10, 11], 4 * F)         # carriers delivered
    add([0, 1, cell, hub, sec, 11], 4 * F)             # carriers dead
    add([0, cell, hub, sec, 11], 4 * F)                # empties dead
    add([0, 9, 11], extra)
    add([0, sec, 10], v)                               # targets
    h[10] = h.get(10, 0) + 11
    R = 12 * F + extra
    return h, v, R
for hub in (4, 5, 6):
    for extra in (0, 20):
        hh, v, R = shape(hub=hub, extra=extra)
        c = price(hh, v, 11, R)[0]
        print('hub rank', hub, 'R', R, 'v', v, 'vs P111-tuned %+.2f%%' % float((c / P111t - 1) * 100))
