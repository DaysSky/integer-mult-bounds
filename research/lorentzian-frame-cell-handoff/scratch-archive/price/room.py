"""Exact room (break-even R vs P111 minus the frame-independent line-mixing floor) for the I_{n,1} family."""
import sys, json, re, subprocess, os
from math import comb
from mpmath import mp
from pricer import price
from scen import local, P111
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def breakeven(v, h, cp, k):
    lo, hi = 0, 4 * v
    if price(local(v, h, 0, cp, k), v, h, 0)[0] < P111: return 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        c = price(local(v, h, mid, cp, k), v, h, mid)[0]
        if c is not None and c >= P111: lo = mid
        else: hi = mid
    return lo
floors = {}
for line in open(SP + '/floor/left.log'):
    m = re.search(r'== (\S+) v (\d+) min leftover (\d+) floor .* = (\d+)', line)
    if m: floors[int(m.group(2))] = (int(m.group(3)), int(m.group(4)))
for n in range(10, 18):
    p = SP + '/lor5/fam_n%d.json' % n
    c = subprocess.run([sys.executable, SP + '/lor3/costs.py', p], capture_output=True, text=True).stdout
    mb = re.search(r'BIT: rank P = (\d+) totals (\d+) cst = (\d+) x = ([\d.]+) window (\d+)', c)
    cst, h = int(mb.group(3)), int(mb.group(5)); v = comb(n, 2) + comb(n, 3)
    # copies: label-decoder totals; approximate their ranks as cst split evenly over the totals (rank <= h)
    nt = int(mb.group(2)); base, extra = divmod(cst, nt); cp = [base + 1] * extra + [base] * (nt - extra)
    if v in floors: left, fl = floors[v]
    else: left, fl = None, 2 * v - v // 15
    b3, b4 = breakeven(v, h, cp, 3), breakeven(v, h, cp, 4)
    print('I_{%d,1} v=%4d h=%2d x=%.3f floor %s%4d (%.2fv) | break-even k3 %4d (%.2fv) k4 %4d (%.2fv) | room k3 %+.2fv k4 %+.2fv'
          % (n, v, h, cst / v, '' if left else '~', fl, fl / v, b3, b3 / v, b4, b4 / v, (b3 - fl) / v, (b4 - fl) / v), flush=True)
