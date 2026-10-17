"""I_{13,1} mixed top: T targets 3 sections (2 delivered), P targets 4 sections (3 delivered): 806 deliveries
(364 sources + 442 empties), D waste registers, R = 442 + D.  Break-even D by waste location, several chains.
usage: python3 price_i13_mix.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'price'))
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
v, h = 364, 13; DEL = 2 * 286 + 3 * 78
def pct(D, node, mid, deadch):
    hh = {}
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + k
    add([1, 2] + list(mid) + [node, h - 1, h], v); add([0, 1, 2] + list(mid) + [node, h - 1, h], DEL - v)
    add(deadch, D); add([0, node, h - 1], v); hh[h - 1] = hh.get(h - 1, 0) + h
    R = DEL - v + D
    c = price(hh, v, h, R)[0]
    return float((c / P111t - 1) * 100) if c else None
def be(node, mid, deadch):
    lo, hi = 0, 6 * v
    if (pct(0, node, mid, deadch) or -1) < 0: return None
    while hi - lo > 1:
        m = (lo + hi) // 2
        if (pct(m, node, mid, deadch) or -1) > 0: lo = m
        else: hi = m
    return lo
for node in (9, 10):
    for mid in ((3, 5), (3, 5, 7), (3, 5, 8), (3, 6, 8), (4, 6, 8)):
        if max(mid) >= node: continue
        vs = {'node': [0, 1, 2] + list(mid) + [node, h], 'top': [0, 1, 2] + list(mid) + [h], '5': [0, 1, 2] + [x for x in mid if x <= 5] + [h], '3': [0, 1, 2, 3, h]}
        print('node %d mid %-10s | D=0 (R=%d) %+.2f%% | break-even D:' % (node, mid, DEL - v, pct(0, node, mid, vs['node'])),
              ' '.join('%s=%s' % (k, be(node, mid, ch)) for k, ch in vs.items()), flush=True)
