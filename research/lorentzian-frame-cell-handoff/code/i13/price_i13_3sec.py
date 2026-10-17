"""I_{13,1} 3-section tops (1 in-chain + 2 delivered sections per target): 2v delivered pieces (v sources), D dead
pieces that climb the full chain and die at the node level (-> h), targets 0 -> node -> h-1, h totals at h-1.
R = v + D.  D = 2v is the worst case 'every delivery needs 2 arrivals' (kappa = 2).  Also prices dead pieces as
cheap dead empties [0, h-2, h] for comparison.  usage: python3 price_i13_3sec.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'price'))
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(D, v, h, node, mid, cells=True, dead='piece'):
    hh = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + k
    pre_s = [1, 2] if cells else [1]; pre_c = [0, 1, 2] if cells else [0, 1]
    add(pre_s + list(mid) + [node, h - 1, h], v); add(pre_c + list(mid) + [node, h - 1, h], v)
    if dead == 'piece': add(pre_c + list(mid) + [node, h], D)
    else: add([0, h - 2, h], D)
    add([0, node, h - 1], v); hh[h - 1] = hh.get(h - 1, 0) + h
    R = v + D
    assert sum(k * c for k, c in hh.items()) == (h - 1) * v + h * R + (h - 1) * v + (h - 1) * h
    return hh, R
def pct(D, v, h, node, mid, cells=True, dead='piece'):
    hh, R = hist(D, v, h, node, mid, cells, dead)
    c = price(hh, v, h, R)[0]
    return R, (float((c / P111t - 1) * 100) if c else None)
def be(v, h, node, mid, cells=True, dead='piece'):
    lo, hi = 0, 6 * v
    if (pct(lo, v, h, node, mid, cells, dead)[1] or -1) < 0: return None
    while hi - lo > 1:
        m = (lo + hi) // 2
        if (pct(m, v, h, node, mid, cells, dead)[1] or -1) > 0: lo = m
        else: hi = m
    return lo
if __name__ == '__main__':
    v, h = 364, 13
    for node in (9, 10):
        for mid in ((3, 5), (3, 5, 7), (4, 6, 8), (3, 5, 7, 9), (3, 6), (5,)):
            if max(mid) >= node: continue
            for dead in ('piece', 'empty'):
                r0 = pct(0, v, h, node, mid, True, dead); r2 = pct(2 * v, v, h, node, mid, True, dead); b = be(v, h, node, mid, True, dead)
                print('I13 3-sec node %d mid %-12s dead=%-5s | D=0 (R=%d) %+.2f%% | D=2v (R=%d) %+.2f%% | break-even D=%s (%.2f per target)' % (
                    node, mid, dead, r0[0], r0[1], r2[0], r2[1], b, b / v if b else float('nan')), flush=True)
    print('I11 control 3-sec node 8 (3,5): D=0 %+.2f%%, D=2v %+.2f%%, break-even D %s' % (pct(0, 220, 11, 8, (3, 5))[1], pct(440, 220, 11, 8, (3, 5))[1], be(220, 11, 8, (3, 5))), flush=True)
