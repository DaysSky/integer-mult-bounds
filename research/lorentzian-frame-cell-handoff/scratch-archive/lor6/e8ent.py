"""Value of entrance ranks on E8 (v = 111, h = 8, cst 63; P111-tuned local histogram).  Convert n helpers to entrance
rank e: remove e units of their climb (taken from their smallest children) and shrink their residual width to 8 - e.
Price with best-fit mixed-width hosting (calibrated: n = 0 reproduces P111-tuned)."""
import sys, bisect
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
v, h, R, K, T = 111, 8, 439, 4, 32
L = 2*K + 1; a = h - 1; m = 1 + L*a; W = 2*K*v*T
base = {1: 1321, 2: 1342, 3: 80, 4: 47, 5: 102, 6: 10, 7: 18}   # P111-tuned
def price_mixed(loc, widths):
    free = sorted(c for c in idle_slots(K, a) for _ in range(2*v))
    res = sorted((w for w, cnt in widths for _ in range(cnt*L)), reverse=True)
    for w in res:
        i = bisect.bisect_left(free, w)
        if i == len(free): return None
        c = free.pop(i)
        if c > w: bisect.insort(free, c - w)
    rem = {}
    for c in free: rem[c] = rem.get(c, 0) + 1
    prof = {}
    for r, z in loc.items(): prof[r] = prof.get(r, 0) + z*T*L
    for r, z in rem.items(): prof[r] = prof.get(r, 0) + z*T
    return root(prof, m, W)
c0 = price_mixed(base, [(8, R)])
print('control P111-tuned (best-fit hosting):', mp.nstr(c0, 12), 'vs', P111)
for e in (1, 2, 3, 4, 5):
    row = []
    for n in (50, 100, 200, 300, 439):
        loc = dict(base)
        # remove e units per converted helper: assume each converted helper loses one rank-e child (its entrance climb)
        if loc.get(e, 0) >= n: loc[e] -= n
        else:
            row.append('n%d:-' % n); continue
        c = price_mixed(loc, [(8, R - n), (8 - e, n)])
        row.append('n%d:%+.2f%%' % (n, float((c / P111 - 1) * 100)) if c else 'n%d:wall' % n)
    print('entrance rank %d:' % e, ' '.join(row), flush=True)
