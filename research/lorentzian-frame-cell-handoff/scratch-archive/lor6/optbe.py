"""Most optimistic break-even R for I_{11,1} (v = 220, h = 11, cst = 110): minimal stop counts per register.
sources 1 stop (rank 10), targets 1 or 2 stops, helpers 1 or 2 stops (split r / 11 - r), 11 copies of rank 10."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
v, h, cst = 220, 11, 110
def hist(R, tsplit, hsplit):
    H = {}
    def add(r, z): H[r] = H.get(r, 0) + z
    add(10, v)                                  # sources: one climb 1 -> 11
    if tsplit: add(tsplit, v); add(10 - tsplit, v)
    else: add(10, v)                            # targets 0 -> t-perp
    if hsplit: add(hsplit, R); add(11 - hsplit, R)
    else: add(11, R)
    add(10, 11)                                 # copies
    assert sum(r*z for r, z in H.items()) == h*R + cst + 2*v*(h-1)
    return H
def c_of(R, ts, hs):
    c, _, d = pricer.price(hist(R, ts, hs), v, h, R)
    return c
for ts in (0, 2, 5):
    for hs in (0, 1, 3, 5):
        lo, hi = 300, 2000
        if c_of(lo, ts, hs) is None or c_of(lo, ts, hs) < P111:
            print('ts', ts, 'hs', hs, 'even R=300 loses:', c_of(lo, ts, hs)); continue
        for _ in range(25):
            mid = (lo + hi) // 2
            c = c_of(mid, ts, hs)
            if c is not None and c >= P111: lo = mid
            else: hi = mid
            if hi - lo <= 1: break
        print('targets split %s, helpers split %s: break-even R = %d (c at R=426: %s)' % (ts or '-', hs or '-', lo, mp.nstr(c_of(426, ts, hs) or 0, 8)), flush=True)
