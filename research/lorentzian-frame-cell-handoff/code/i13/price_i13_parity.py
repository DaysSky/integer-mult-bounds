"""I_{13,1} PARITY top pricing (identical full-section parts; copies), adapted from price/price_copies.py:
N nodes, each assembles its section sum from m pieces (cells -> mids -> node): one assembled register is delivered
(node -> 12 -> 13), m-1 pieces die at the node (-> 13); every other delivery is a COPY (0 -> node -> 12 -> 13).
v sources are among the pieces (delivered assembled first, then dead).  Targets 0 -> node -> 12, 13 totals at 12.
Del = 286 (kT - 1) + 78 (kP - 1).  R = Del + (m - 1) N - v.  usage: python3 price_i13_parity.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'price'))
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
v, h = 364, 13
def pct(Del, N, m, node, mid, cells=True):
    hh = {}
    def add(ch, k):
        assert k >= 0, (ch, k)
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + k
    pre_s = [1, 2] if cells else [1]; pre_c = [0, 1, 2] if cells else [0, 1]
    npieces = m * N; assert npieces >= v and Del >= N
    deliv = N; dead = npieces - N
    s_deliv = min(v, deliv); s_dead = v - s_deliv
    add(pre_s + list(mid) + [node, h - 1, h], s_deliv); add(pre_c + list(mid) + [node, h - 1, h], deliv - s_deliv)
    add(pre_s + list(mid) + [node, h], s_dead); add(pre_c + list(mid) + [node, h], dead - s_dead)
    add([0, node, h - 1, h], Del - N)
    add([0, node, h - 1], v); hh[h - 1] = hh.get(h - 1, 0) + h
    R = Del + (m - 1) * N - v
    c = price(hh, v, h, R)[0]
    return R, (float((c / P111t - 1) * 100) if c else None)
if __name__ == '__main__':
    for kT, kP in ((4, 4), (4, 5), (5, 5), (5, 6), (6, 6)):
        Del = 286 * (kT - 1) + 78 * (kP - 1)
        for node, mid in ((10, (3, 5)), (10, (3, 5, 7, 9)), (10, (5, 7, 9)), (9, (3, 5, 7))):
            row = []
            for N in (200, 300, 400, 500, 600):
                if 2 * N < v or N > Del: continue
                R, p = pct(Del, N, 2, node, mid)
                row.append('N=%d R=%d %+.2f%%' % (N, R, p))
            print('kT=%d kP=%d Del=%d node %d mid %-11s | %s' % (kT, kP, Del, node, mid, ' | '.join(row)), flush=True)
