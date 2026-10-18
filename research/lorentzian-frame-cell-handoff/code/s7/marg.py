"""Marginal cost (in units of the exact linear budget at q* = E1) of helpers of given entrance/pieces, I11 and E8."""
import sys, bisect
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots
from qbudget import cost, QSTAR
K, T = 4, 32; L = 9
def total_cost(h, v, cst_pieces, src, tgt, helpers):
    a = h - 1; m = 1 + L*a
    loc = 0.0
    loc += v*sum(cost(p, m) for p in src) + v*sum(cost(p, m) for p in tgt) + sum(cost(p, m) for p in cst_pieces)
    widths = []
    for cnt, e, pieces in helpers:
        loc += cnt*sum(cost(p, m) for p in pieces); widths += [h-e]*cnt
    res = sorted([w for w in widths for _ in range(L)], reverse=True)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2*v))
    over = 0
    for w in res:
        i = bisect.bisect_left(free, w)
        if i == len(free): over += w; continue
        c = free.pop(i)
        if c > w: bisect.insort(free, c - w)
    idle = sum(cost(c, m) for c in free)
    return 9*loc + idle, over
def budget(v, cst): return 8*v - 9*cst
if __name__ == '__main__':
    for name, h, v, cstp in (('I11', 11, 220, [10]*11), ('E8', 8, 120, [8]*9), ('P111', 8, 111, [7]*9)):
        cst = sum(cstp); B = budget(v, cst)
        a = h - 1
        base, _ = total_cost(h, v, cstp, [a], [a], [])
        print(name, 'budget', B, 'base(one-stop src/tgt, no helpers)', round(base, 2), 'free', round(B - base, 2), 'per line', round((B-base)/v, 3))
        for e, pieces in ((0, [h]), (1, [h-1]), (0, [1, 2, h-3]), (1, [2, h-3]), (0, [1,1,2,2,1,1] if h == 8 else [1,1,2,3,2,1,1])):
            out = []
            for k in (0.5, 1, 2, 3, 4, 5, 6):
                n = int(k*v)
                c, over = total_cost(h, v, cstp, [a], [a], [(n, e, pieces)])
                out.append('%.1fv:%.3f%s' % (k, (c - base)/n, '*' if over else ''))
            print('   e=%d pieces=%s avg cost/helper:' % (e, pieces), ' '.join(out))
