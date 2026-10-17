"""Scenario break-even vs P111 (exact pricer, k even moves per register) for punctured line systems:
v live ports = v0 - p, totals as in the unpunctured scenario (copies of rank h-1).  E8 control: v0=120 -> 111."""
import sys
from mpmath import mp
from pricer import price
from scen import local, P111
def be(v, h, cp, k):
    lo, hi = 0, 4 * v
    while hi - lo > 1:
        mid = (lo + hi) // 2
        c = price(local(v, h, mid, cp, k), v, h, mid)[0]
        if c is not None and c >= P111: lo = mid
        else: hi = mid
    return lo
for k in (3, 4, 5):
    for v in (120, 111):
        print('E8 v=%d k=%d: beats P111 iff R <= %d' % (v, k, be(v, 8, [7] * 9, k)), flush=True)
for k in (3, 4, 5):
    for v in (220, 215, 209, 200):
        b = be(v, 11, [10] * 11, k)
        print('I11,1 v=%d k=%d: beats P111 iff R <= %d (%.3f/port)' % (v, k, b, b / v), flush=True)
