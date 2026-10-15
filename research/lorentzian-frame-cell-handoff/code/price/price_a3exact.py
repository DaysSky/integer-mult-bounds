"""Exact-count price of the A3-parity architecture shape at v = 220, h = 11, R helpers:
sources 220 (pieces) 1-2-m-9-[10]-11; carriers 440: 293 pieces 0-1-2-m-9-[10]-11, 147 copies 0-1-2-9-10-11;
dead pieces 257 (no rank-10 stop), delivered pieces 256; empties E = R - 440: 257 delivered copies 0-9-10-11, rest dead
0-9-11 (overhead); targets 0-1-10; 11 totals at rank 10.  Mass consistency asserted:
mass = 10*220 (sources) + 11*R (helpers) + 10*220 (targets) + 10*11 (totals)."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m, R):
    h = {}
    def add(ch, k):
        assert k >= 0
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    E = R - 440; assert E >= 257
    # dead pieces: 257 -> take all from sources first (220) then 37 carriers
    add([1, 2, m, 9, 11], 220); add([0, 1, 2, m, 9, 11], 37)
    add([0, 1, 2, m, 9, 10, 11], 293 - 37)          # delivered carrier pieces (256)
    add([0, 1, 2, 9, 10, 11], 147)                  # carrier copies (zero-level)
    add([0, 9, 10, 11], 257)                        # delivered empties
    add([0, 9, 11], E - 257)                        # overhead (dead empties)
    add([0, 1, 10], 220)                            # targets
    h[10] = h.get(10, 0) + 11
    mass = sum(k * v for k, v in h.items())
    assert mass == 10 * 220 + 11 * R + 10 * 220 + 10 * 11, (mass, R)
    return h
for m in (3, 5, 8):
    out = []
    for R in (697, 720, 750, 780, 810, 840, 870):
        c = price(hist(m, R), 220, 11, R)[0]
        out.append('R=%d %s' % (R, '%+.2f%%' % float((c / P111t - 1) * 100) if c else 'n/a'))
    print('mid rank', m, ' | '.join(out), flush=True)
# control: the standard one-level model at R=697 rank 5 with exact counts (lor_fc_price3 style)
def std(m, R):
    h = {}
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    add([1, 2, m, 9, 10, 11], 220); add([0, 1, 2, m, 9, 10, 11], 440); add([0, 1, 2, m, 9, 11], R - 440)
    add([0, 2, 9, 10], 220); h[10] = h.get(10, 0) + 11
    return h
for R in (629, 697):
    c = price(std(5, R), 220, 11, R)[0]; print('standard one-level rank 5 R=%d %+.2f%%' % (R, float((c / P111t - 1) * 100)))
