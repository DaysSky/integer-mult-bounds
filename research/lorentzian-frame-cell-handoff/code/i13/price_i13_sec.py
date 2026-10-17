"""Generic-h port of price/price_r8sec.py (4 frame sections per target: 1 in-chain, 3 delivered; every cell-stage
register is a delivered piece, 3v deliveries, no copies).  Pieces: cell -> mids -> node -> t-perp (h-1) -> h; v of
them are sources (pre [1,2]), 2v start empty (pre [0,1,2]).  Extra registers = dead empties [0, h-2, h] (R - 2v of
them).  Targets 0 -> node -> h-1; h decoder totals at rank h-1.  Mass identity asserted as in the original.
I11 control (h=11, v=220, node 8) must reproduce price_r8sec.py.  usage: python3 price_i13_sec.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'price'))
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(R, v, h, node, mid, cells=True):
    hh = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + k
    pre_s = [1, 2] if cells else [1]; pre_c = [0, 1, 2] if cells else [0, 1]
    add(pre_s + list(mid) + [node, h - 1, h], v); add(pre_c + list(mid) + [node, h - 1, h], 2 * v)
    add([0, h - 2, h], R - 2 * v); add([0, node, h - 1], v)
    hh[h - 1] = hh.get(h - 1, 0) + h
    assert sum(k * c for k, c in hh.items()) == (h - 1) * v + h * R + (h - 1) * v + (h - 1) * h
    return hh
def pct(R, v, h, node, mid, cells=True):
    c = price(hist(R, v, h, node, mid, cells), v, h, R)[0]
    return float((c / P111t - 1) * 100) if c else None
def breakeven(v, h, node, mid, cells=True):
    lo, hi = 2 * v, 5 * v
    if (pct(lo, v, h, node, mid, cells) or -1) < 0: return None
    while hi - lo > 1:
        m = (lo + hi) // 2
        if (pct(m, v, h, node, mid, cells) or -1) > 0: lo = m
        else: hi = m
    return lo
if __name__ == '__main__':
    print('I11 control (cells,3,5) node 8: R=440 %+.2f%%  break-even R %s' % (pct(440, 220, 11, 8, (3, 5)), breakeven(220, 11, 8, (3, 5))), flush=True)
    v, h = 364, 13
    for node in (8, 9, 10):
        for mid in ((3, 5), (3, 5, 7), (3, 6), (4, 7), (3, 5, 8), (3, 6, 8), (5,), (3,), (4, 6, 8), (3, 5, 7, 9)):
            if max(mid) >= node: continue
            for cells in (True, False):
                be = breakeven(v, h, node, mid, cells)
                print('I13 node %d mid %-12s %-6s | R=728 %+.2f%% | break-even R %s (extra %s, %.2f per target)' % (
                    node, mid, 'cells' if cells else 'nocell', pct(2 * v, v, h, node, mid, cells), be,
                    be - 2 * v if be else None, (be - 2 * v) / v if be else float('nan')), flush=True)
