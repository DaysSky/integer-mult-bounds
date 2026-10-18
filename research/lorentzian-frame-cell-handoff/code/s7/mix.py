"""Exact nine-stage price for a register mix with best-fit mixed-width hosting (bankprice model; banks if needed).
groups: list of (count, start_rank, [pieces]) for helpers; sources/targets given as piece lists."""
import sys, bisect, math
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp, mpf
E1 = mpf('0.001734473240795253742474'); P111 = mpf('0.001733427039589844')
K, T = 4, 32; L = 2*K + 1
def price(h, v, cst_pieces, src, tgt, helpers, nsrc=None, ntgt=None):
    a = h - 1; m = 1 + L*a
    nsrc = v if nsrc is None else nsrc; ntgt = v if ntgt is None else ntgt
    loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    for p in src: add(p, nsrc)
    for p in tgt: add(p, ntgt)
    for p in cst_pieces: add(p, 1)
    widths = []
    for cnt, e, pieces in helpers:
        assert sum(pieces) == h - e, (pieces, h, e)
        for p in pieces: add(p, cnt)
        widths += [h - e] * cnt
    assert sum(src) == h - 1 and sum(tgt) == h - 1
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
    W = 2*K*v*T + nb*T
    return root(prof, m, W, env=False)
pct = lambda c: '%+.2f%%' % float((c/E1 - 1)*100) if c is not None else 'none'
if __name__ == '__main__':
    # R420 control: sources 1,2,2,1,1 ; targets 2,5 ; carriers 240: 1,1,2,2,1,1 ; empties 180 ; totals 9 x 8
    # use the actual R420 histogram instead
    from pricer import price as p0
    c, _, _ = p0({1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}, 120, 8, 420)
    print('R420 actual', mp.nstr(c, 12), pct(c))
