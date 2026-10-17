"""Price of the lever blueprint for I_{11,1} (exact nine-stage pricer, bank overflow, best-fit mixed hosting):
220 sources, M frame-0 movers (width 11), H lever hubs entering at f-perp (rank 7, width 4), targets 0 -> f-perp ->
t-perp, cst 110.  Pieces per role given as explicit lists."""
import sys; sys.path.insert(0, '.')
import bankprice as B
from mpmath import mp
def prof(roles):
    loc = {}; widths = []
    for cnt, pieces, width in roles:
        for p in pieces: loc[p] = loc.get(p, 0) + cnt
        if width: widths += [width] * cnt
    for p in [10] * 11: loc[p] = loc.get(p, 0) + 1          # decoder: 11 copies of rank 10
    return loc, widths
v = 220
src_opts = {'s6': [1, 2, 4, 1, 1, 1], 's4': [1, 6, 2, 1], 's3': [1, 7, 2]}
mov_opts = {'m5': [2, 2, 2, 2, 3], 'm4': [2, 3, 3, 3], 'm3': [4, 4, 3]}
hub_opts = {'h3': [1, 2, 1], 'h2': [3, 1], 'h4': [1, 1, 1, 1]}
tgt_opts = {'t2': [7, 3], 't3': [7, 1, 2]}
for M in (300, 450, 600):
    for H in (660, 1100, 1500, 2000):
        row = []
        for sk, mk, hk, tk in (('s6', 'm5', 'h4', 't3'), ('s4', 'm4', 'h3', 't2'), ('s3', 'm3', 'h2', 't2')):
            loc, w = prof([(v, src_opts[sk], 0), (M, mov_opts[mk], 11), (H, hub_opts[hk], 4), (v, tgt_opts[tk], 0)])
            c, d = B.price(loc, v, 11, w)
            row.append('%s/%s/%s/%s %+.1f%%%s' % (sk, mk, hk, tk, float(c / B.P111 - 1) * 100, ' (banks %d)' % d['banks'] if d['banks'] else ''))
        print('movers %d hubs %d (R %d):' % (M, H, M + H), ' | '.join(row), flush=True)
