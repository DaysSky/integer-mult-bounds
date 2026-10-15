"""Frame (exact union cover) tops with in-chain reads, model-A counts, reach-compliant pieces.
Per v = 220: 330 pair sections: 220 (in-chain user + delivered user): 2 pieces, the delivered user's register is the
merged piece; 110 (two delivered users): 2 pieces + 1 copy.  Pieces 660 = all cell-stage registers (220 sources dead,
110 carriers dead, 330 carriers alive/delivered); copies 110 [0,9,10,11]; targets 0 -> S0 (in-chain) -> t-perp.
Pieces: fraction phi takes a low first stop m1 before the rank-8 node (reach lemma), the rest cell -> 8 directly.
R = 550 ideal; extra dead empties [0,9,11] for R > 550.  Prints c vs P111-tuned and break-even."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m1, phi, R, node=8):
    h = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    def add2(pre, post, k):
        kl = round(phi * k); add(pre + [m1] + post, kl); add(pre + post, k - kl)
    v = 220
    add2([1, 2], [node, 9, 11], 220)
    add2([0, 1, 2], [node, 9, 11], 110)
    add2([0, 1, 2], [node, 9, 10, 11], 330)
    add([0, 9, 10, 11], 110)
    extra = R - 550; assert extra >= 0
    add([0, 9, 11], extra)
    add([0, 9, 10], v)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(m1, phi, R, node=8):
    c = price(hist(m1, phi, R, node), 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
for node in (8, 7):
    for m1, phi in ((3, 0.0), (3, 0.5), (3, 0.75), (3, 1.0), (4, 1.0), (5, 1.0)):
        if m1 >= node: continue
        be = next((R - 1 for R in range(550, 900, 2) if (pct(m1, phi, R, node) or -1) < 0), None)
        print('node', node, 'low stop', m1, 'phi', phi, 'R=550 %+.2f%%' % pct(m1, phi, 550, node), 'R=600 %+.2f%%' % pct(m1, phi, 600, node), 'break-even ~', be, flush=True)
