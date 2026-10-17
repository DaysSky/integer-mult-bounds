"""Exact prices of R420-shaped words with fewer helpers: remove k helpers with R420's average helper chain
(whole helpers, mass identity kept) -- estimate of where a frame-cell word on v=120 breaks even with P111-tuned."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
base = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
# R420 helper chains (generator anatomy): carriers 0->1->2->...; approximate removal of an 'empty' helper:
# empty chain in R420: 0 -> cell(2) -> quad(4) -> D6(6) -> full(8): jumps 2,2,2,2
for k in (0, 20, 40, 60, 80, 100, 120):
    h = dict(base); h[2] -= 4 * k
    c = price(h, 120, 8, 420 - k)[0]
    print('R = %d  c = %s  vs P111t %+.2f%%' % (420 - k, mp.nstr(c, 10), float((c / P111t - 1) * 100)))
