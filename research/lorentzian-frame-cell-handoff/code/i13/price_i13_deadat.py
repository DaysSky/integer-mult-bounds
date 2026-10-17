"""I_{13,1} 3-section top (R = v + D): price as a function of WHERE the D waste registers die.
Variants: dead at node [pre,mids,node,h]; dead at the top mid stop [pre,mids,h]; dead at rank 3 [0,1,2,3,h]; dead
empty [0,h-2,h].  Break-even D for each, chain (cells, mids) -> node.  usage: python3 price_i13_deadat.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'price'))
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
v, h = 364, 13
def pct(D, node, mid, deadch):
    hh = {}
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + k
    add([1, 2] + list(mid) + [node, h - 1, h], v); add([0, 1, 2] + list(mid) + [node, h - 1, h], v)
    add(deadch, D); add([0, node, h - 1], v); hh[h - 1] = hh.get(h - 1, 0) + h
    R = v + D
    c = price(hh, v, h, R)[0]
    return float((c / P111t - 1) * 100) if c else None
def be(node, mid, deadch):
    lo, hi = 0, 6 * v
    while hi - lo > 1:
        m = (lo + hi) // 2
        if (pct(m, node, mid, deadch) or -1) > 0: lo = m
        else: hi = m
    return lo
for node in (9, 10):
    for mid in ((3, 5), (3, 5, 7), (3, 5, 8), (4, 6, 8)):
        if max(mid) >= node: continue
        variants = {'at node': [0, 1, 2] + list(mid) + [node, h], 'at top mid': [0, 1, 2] + list(mid) + [h],
                    'at 3': [0, 1, 2, 3, h], 'empty': [0, h - 2, h], 'at 5': [0, 1, 2] + [x for x in mid if x <= 5] + [h]}
        print('node %d mid %s :' % (node, mid), ' | '.join('%s D_be=%d' % (k, be(node, mid, ch)) for k, ch in variants.items()), flush=True)
