"""4-part kappa=1 shape with a REACH-respecting two-level middle: every piece goes cell (2) -> mid (m1) -> node (8)
-> target (10) -> 11; copies are empties reading the piece at its node: [0, 8, 10, 11].  All 4 parts delivered
(no in-chain section); targets 0 -> <d> -> t-perp.  Pieces 660 (= all 3 branch registers per line: 220 sources
[1,2,m1,8,10,11] + 440 carriers [0,1,2,m1,8,10,11]), copies 220 -> R = 660 ideal.  Also a variant where half the
pieces die at the node (merged into a sibling output) [..,8,11] with extra copies."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m1, R, dd=1):
    h = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    v = 220
    add([1, 2, m1, 8, 10, 11], 220)
    add([0, 1, 2, m1, 8, 10, 11], 440)
    extra = R - 440 - 220; assert extra >= 0
    add([0, 8, 10, 11], 220)
    add([0, 9, 11], extra)
    add([0, dd, 10] if dd else [0, 10], v)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
for m1 in (3, 4, 5, 6):
    row = []
    for R in (660, 700, 750, 800, 850):
        c = price(hist(m1, R), 220, 11, R)[0]
        row.append('R=%d %s' % (R, '%+.2f%%' % float((c / P111t - 1) * 100) if c else 'n/a'))
    print('mid rank', m1, ' | '.join(row), flush=True)
