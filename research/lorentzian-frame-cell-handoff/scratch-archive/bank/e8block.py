"""E8 R420 role model vs a rank-4 block-group variant (exact nine-stage pricer, mixed widths)."""
import sys; sys.path.insert(0, '.')
import bankprice as B
from mpmath import mp
def run(name, roles, cst_pieces, v=120, h=8):
    loc = {}; widths = []
    for cnt, pieces, width in roles:
        for p in pieces: loc[p] = loc.get(p, 0) + cnt
        widths += [width] * cnt if width else []
    for p in cst_pieces: loc[p] = loc.get(p, 0) + 1
    c, d = B.price(loc, v, h, widths)
    print('%-58s R=%4d c=%s %+.2f%%' % (name, len(widths), mp.nstr(c, 10), float(c / B.P111 - 1) * 100), dict(sorted(loc.items())))
dec = [8] * 9
# R420 reconstruction: sources 1,2,2,1,1; targets 2,5; helpers: 240 carriers [1,1,2,2,1,1]? fit histogram exactly
run('R420 (published histogram)', [], [], ) if False else None
loc420 = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
c, d = B.price(loc420, 120, 8, [8] * 420); print('R420 published hist', mp.nstr(c, 12), '%+.2f%%' % float((c / B.P111 - 1) * 100))
# role model matching the histogram: sources [1,2,2,1,1]; targets [2,5]; helpers: 360 x [1,2,2,1,1,1] (=8) wait sum 8
# helpers total pieces: 1:960, 2:1080, 4:60 over 420 helpers: 60 helpers [4,2,1,1], 360 helpers [1,2,2,1,1,1]? -> 1:4x360=1440 too many
# use: 60 x [4,2,1,1] ; 360 x [2,2,2,1,1] (1:720, 2:1080) ; then 1 remaining: 960-60*2-720=120 -> adjust 60 of them [2,2,1,1,1,1]
roles420 = [(120, [1, 2, 2, 1, 1], 0), (120, [2, 5], 0), (60, [4, 2, 1, 1], 8), (300, [2, 2, 2, 1, 1], 8), (60, [2, 2, 1, 1, 1, 1], 8)]
run('R420 role model', roles420, dec)
# block-group variant: targets [4,3]; 360 needer roles become group helpers [2,1,1] (width 4); originals drop their
# top climb (merge last two rank-1 pieces into one rank-2 piece) for 240 helpers and 120 sources
rolesG = [(120, [1, 2, 2, 2], 0), (120, [4, 3], 0), (60, [4, 2, 2], 8), (180, [2, 2, 2, 2], 8), (120, [2, 2, 2, 1, 1], 8),
          (60, [2, 2, 1, 1, 2], 8), (360, [2, 1, 1], 4)]
run('R420 + rank-4 block groups (360 width-4 needers added)', rolesG, dec)
rolesG2 = [(120, [1, 2, 2, 2], 0), (120, [4, 3], 0), (60, [4, 2, 2], 8), (120, [2, 2, 2, 2], 8), (360, [2, 1, 1], 4)]
run('same, 240 original needer-carriers dropped entirely', rolesG2, dec)
