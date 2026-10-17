import sys; sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
def hist(R, extra1=0, hchain=(1,1,6,3)):
    h = {}
    def add(r, n): h[r] = h.get(r, 0) + n
    v = 220
    add(1, v); add(9, v); add(1, v); add(9, v)
    for j in hchain: add(j, R)
    add(10, 11); add(1, extra1)
    return h
def pc(c): return '%+.3f%%' % float((c/P111-1)*100) if c is not None else 'none'
for R in (600, 700, 760):
    for ch in ((1,1,6,3), (8,3), (11,)):
        r0 = price(hist(R, hchain=ch), 220, 11, R)
        r1 = price(hist(R, extra1=220, hchain=ch), 220, 11, R)
        r3 = price(hist(R + 20, hchain=ch), 220, 11, R + 20)
        print('R', R, 'helper chain', ch, 'base', pc(r0[0]), r0[2].get('error', ''), '| +220 rank-1 retained', pc(r1[0]), '| +20 helpers', pc(r3[0]), flush=True)
