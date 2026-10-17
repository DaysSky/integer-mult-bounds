"""Exact marginal price effects on P111-tuned's local profile: merge two jumps (a,b)->(a+b) and split, at fixed v, R."""
import sys, collections
sys.path.insert(0, '../price')
from pricer import price
from mpmath import mp
v, R = 111, 439
h0 = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
c0 = price(dict(h0), v, 8, R)[0]
print('base', mp.nstr(c0, 12))
K = 20
def d(ch):
    h = collections.Counter(h0)
    for j, n in ch.items(): h[j] += n * K
    if min(h.values()) < 0: return None
    p = price({k: x for k, x in h.items() if x}, v, 8, R)[0]
    return float((p / c0 - 1) * 100) / K
print('per-event %% change (x%d events averaged):' % K)
for a in range(1, 7):
    for b in range(a, 8 - a):
        r = d({a: -1, b: -1, a + b: 1}) if a != b else d({a: -2, a + b: 1})
        print('  merge (%d,%d)->%d : %+.4f%%' % (a, b, a + b, r))
for a, b, cc, dd in ((1, 5, 2, 4), (1, 5, 3, 3), (2, 4, 3, 3), (1, 6, 3, 4), (1, 4, 2, 3), (1, 3, 2, 2), (1, 6, 2, 5)):
    print('  swap {%d,%d}->{%d,%d}: %+.4f%%' % (a, b, cc, dd, d({a: -1, b: -1, cc: 1, dd: 1}) if cc != dd else d({a: -1, b: -1, cc: 2})))
