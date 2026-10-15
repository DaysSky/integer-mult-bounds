"""Identical-parts rank-8 design with copies: N nodes, each assembling its shared part from m = 2 rank-5 pieces
(cells -> 3 -> 5 -> node 8): one assembled register is delivered (-> 10 -> 11), one piece dies at the node (-> 11);
the node's other delivered users get COPIES (empty registers 0 -> 8 -> 10 -> 11).  Sources are among the pieces.
Registers = 660 + N (R = 440 + N).  Optional mid list.  usage: run from code/price"""
import sys
sys.path.insert(0, '.')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def pct(N, mid=(3, 5), m=2, cells=True):
    h = {}
    def add(ch, k):
        assert all(b > a for a, b in zip(ch, ch[1:])), ch
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    pre_s = [1, 2] if cells else [1]; pre_c = [0, 1, 2] if cells else [0, 1]
    npieces = m * N; nsrc = 220
    assert npieces >= nsrc
    # assume sources are delivered assembled registers first, then dead pieces
    deliv = N; dead = npieces - N
    s_deliv = min(nsrc, deliv); s_dead = nsrc - s_deliv
    add(pre_s + list(mid) + [8, 10, 11], s_deliv); add(pre_c + list(mid) + [8, 10, 11], deliv - s_deliv)
    add(pre_s + list(mid) + [8, 11], s_dead); add(pre_c + list(mid) + [8, 11], dead - s_dead)
    add([0, 8, 10, 11], 660 - N)
    add([0, 8, 10], 220); h[10] = h.get(10, 0) + 11
    R = 440 + N + (m - 2) * N
    c = price(h, 220, 11, R)[0]
    return R, float((c / P111t - 1) * 100) if c else None
for mid in ((3, 5), (5,), (3,), (3, 5, 7)):
    for cells in (True, False):
        print('mid', mid, 'cells' if cells else 'nocell', ' | '.join('N=%d R=%d %+.2f%%' % ((N,) + pct(N, mid, 2, cells)) for N in (110, 147, 180, 220, 260)), flush=True)
