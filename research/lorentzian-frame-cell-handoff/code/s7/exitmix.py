"""Exact price with per-helper widths = end rank - start rank (exit/entrance), bank-aware best-fit hosting."""
import sys, bisect, math
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mpf
E1 = mpf('0.001734473240795253742474')
K, T = 4, 32; L = 2*K + 1
def price(h, v, cst_pieces, src_groups, tgt_groups, helpers):
    """src_groups/tgt_groups: list of (count, pieces); helpers: list of (count, start, end, pieces)"""
    a = h - 1; m = 1 + L*a; loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    for cnt, pcs in src_groups + tgt_groups:
        for p in pcs: add(p, cnt)
    for p in cst_pieces: add(p, 1)
    widths = []
    for cnt, s, e, pcs in helpers:
        assert sum(pcs) == e - s, (s, e, pcs)
        for p in pcs: add(p, cnt)
        widths += [e - s]*cnt
    res = sorted([w for w in widths for _ in range(L)], reverse=True)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2*v))
    banked = []
    for w in res:
        i = bisect.bisect_left(free, w)
        if i == len(free): banked.append(w); continue
        c = free.pop(i)
        if c > w: bisect.insort(free, c - w)
    over = sum(banked); nb = math.ceil(over/m); pad = nb*m - over
    rem = {}
    for c in free: rem[c] = rem.get(c, 0) + 1
    prof = {}
    for r_, z in loc.items(): prof[r_] = prof.get(r_, 0) + z*T*L
    for r_, z in rem.items(): prof[r_] = prof.get(r_, 0) + z*T
    if pad: prof[pad] = prof.get(pad, 0) + T
    return root(prof, m, 2*K*v*T + nb*T, env=False)
pct = lambda c: '%+.2f%%' % float((c/E1 - 1)*100) if c is not None else 'none'
if __name__ == '__main__':
    # R420 control
    base_h = [(96,0,8,[1,1,2,2,1,1]), (96,0,8,[2,2,2,2]), (84,0,8,[1,1,2,2,2]), (84,0,8,[2,2,2,1,1]), (60,0,8,[1,1,4,1,1])]
    print('R420', pct(price(8, 120, [8]*9, [(120,[1,2,2,1,1])], [(120,[2,5])], base_h)))
    # all helpers exit at rank 7 (drop last piece 1 where present) -- upper-bound flavour
    ex = [(96,0,7,[1,1,2,2,1]), (96,0,7,[2,2,2,1]), (84,0,7,[1,1,2,2,1]), (84,0,7,[2,2,2,1]), (60,0,7,[1,1,4,1])]
    print('R420, every helper exits at rank 7 (hypothetical)', pct(price(8, 120, [8]*9, [(120,[1,2,2,1,1])], [(120,[2,5])], ex)))
    # E1-like (P111 shape): helpers 439 width 8
    p_h = [(95,0,8,[1,1,2,2,1,1]), (79,0,8,[2,2,2,2]), (75,0,8,[2,2,2,1,1]), (74,0,8,[1,1,2,2,2]), (36,0,8,[1,1,4,1,1]), (36,0,8,[1,3,2,1,1]), (27,0,8,[1,3,2,2]), (17,0,8,[1,5,1,1])]
    print('P111-shape control', pct(price(8, 111, [7]*9, [(111,[1,2,2,1,1])], [(111,[2,5])], p_h)))
    for frac in (0.25, 0.5, 1.0):
        hh = []
        for c, s, e, pc in p_h:
            k = int(round(c*frac))
            if pc[-1] == 1 and len(pc) > 2:
                hh.append((k, 0, 7, pc[:-1])); hh.append((c-k, s, e, pc))
            else: hh.append((c, s, e, pc))
        print('P111-shape, %.0f%% of needer-type helpers exit at 7' % (100*frac), pct(price(8, 111, [7]*9, [(111,[1,2,2,1,1])], [(111,[2,5])], hh)))
