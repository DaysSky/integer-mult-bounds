from mix import price, pct, mp
h, v = 8, 120
tot = [8]*9
base = dict(src=[1,2,2,1,1], tgt=[2,5])
c = price(h, v, tot, [1,2,2,1,1], [2,5], [(240,0,[1,1,2,2,1,1]), (120,0,[2,2,2,2]), (60,0,[2,2,4])])
print('R420 model', mp.nstr(c,10), pct(c))
for tg in ([1,2,4],[1,6],[2,5]):
    c = price(h, v, tot, [1,2,2,1,1], tg, [(240,0,[1,1,2,2,1,1]), (120,1,[2,2,2,1]), (60,1,[2,4,1])])
    print('R420 z-empties, targets', tg, mp.nstr(c,10), pct(c))
# all helpers entrance-1 (upper bound)
c = price(h, v, tot, [1,2,2,1,1], [1,2,4], [(240,1,[1,2,2,1,1]), (120,1,[2,2,2,1]), (60,1,[2,4,1])])
print('all entrance-1', pct(c))
# P111-like: v=111 cst 63 (9 x 7)
c = price(8, 111, [7]*9, [1,2,2,1,1], [2,5], [(222,0,[1,1,2,2,1,1]), (217,0,[2,2,2,2])])
print('P111-ish frame0 R439', pct(c))
c = price(8, 111, [7]*9, [1,2,2,1,1], [1,2,4], [(222,0,[1,1,2,2,1,1]), (217,1,[2,2,2,1])])
print('P111-ish z-empties R439', pct(c))
