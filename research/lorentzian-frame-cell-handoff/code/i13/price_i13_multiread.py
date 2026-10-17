"""I_{13,1}: price of targets that read TWO nodes in-chain (target chain 0 -> node(10) -> node(11) -> t-perp(12))
versus one (0 -> 10 -> 12).  Deliveries Del (v sources among them) climb cells -> mids -> 10 -> 12 -> 13; D waste
registers die at a given stop; R = Del - v + D.  Cases: T 3 sections/P 4 sections with 1 or 2 in-chain reads.
usage: python3 price_i13_multiread.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'price'))
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
v, h = 364, 13
def pct(Del, D, mid, deadch, tchains):
    hh = {}
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + k
    add([1, 2] + list(mid) + [10, 12, 13], v); add([0, 1, 2] + list(mid) + [10, 12, 13], Del - v)
    add(deadch, D)
    for ch, k in tchains: add(ch, k)
    hh[12] = hh.get(12, 0) + 13
    R = Del - v + D
    c = price(hh, v, h, R)[0]
    return R, (float((c / P111t - 1) * 100) if c else None)
def be(Del, mid, deadch, tchains):
    lo, hi = 0, 6 * v
    if (pct(Del, 0, mid, deadch, tchains)[1] or -1) < 0: return None
    while hi - lo > 1:
        m = (lo + hi) // 2
        if (pct(Del, m, mid, deadch, tchains)[1] or -1) > 0: lo = m
        else: hi = m
    return lo
cases = {
  'T3(1 read)+P4(1 read)': (2 * 286 + 3 * 78, [([0, 10, 12], 364)]),
  'T3(1 read)+P4(2 reads)': (2 * 286 + 2 * 78, [([0, 10, 12], 286), ([0, 10, 11, 12], 78)]),
  'T4(2 reads)+P4(2 reads)': (2 * 364, [([0, 10, 11, 12], 364)]),
  'T3(2 reads)+P4(2 reads)': (286 + 2 * 78, [([0, 10, 11, 12], 364)]),
}
for mid in ((3, 5), (3, 5, 7, 9), (5, 7, 9)):
    for name, (Del, tch) in cases.items():
        dn = [0, 1, 2] + list(mid) + [10, 13]; d3 = [0, 1, 2, 3, 13]
        R0, p0 = pct(Del, 0, mid, dn, tch)
        print('mid %-11s %-24s Del %4d | D=0 R=%d %+.2f%% | break-even D: dies at node %s, at 3 %s' % (
            mid, name, Del, R0, p0, be(Del, mid, dn, tch), be(Del, mid, d3, tch)), flush=True)
