"""Exact price of the A3-parity architecture shape (per 6-target block): 6 sources + 12 carriers + E empties;
P = 14 piece arrivals (via one middle node of rank m) of which (P - 7) delivered and 7 dead (die at 11 without the
rank-10 stop); copies = carriers not used as pieces (0-1-2-9-10-11) + empties (0-9-10-11), all delivered;
targets 0 -> 1 -> 10; 11 decoder totals at rank 10.  'extra' = additional empty registers beyond the ideal 7 per
block (they are dead: 0-9-11), modelling realistic overheads.  Scaled to v = 220."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m, extra, v=220):
    h = {}
    def add(ch, k):
        if k <= 0: return
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    B = v / 6.0
    src, car, emp = 6 * B, 12 * B, 7 * B
    pieces = 14 * B; dead_p = 7 * B
    # sources: all pieces; 3 delivered-pieces from carriers etc.  distribute dead pieces among sources first
    s_dead = min(src, dead_p); s_del = src - s_dead
    c_piece = pieces - src; c_dead = dead_p - s_dead; c_pdel = c_piece - c_dead; c_copy = car - c_piece
    add([1, 2, m, 9, 11], round(s_dead)); add([1, 2, m, 9, 10, 11], round(s_del))
    add([0, 1, 2, m, 9, 11], round(c_dead)); add([0, 1, 2, m, 9, 10, 11], round(c_pdel))
    add([0, 1, 2, 9, 10, 11], round(c_copy)); add([0, 9, 10, 11], round(emp))
    add([0, 9, 11], round(extra * B))              # overhead registers (dead)
    add([0, 1, 10], v)
    h[10] = h.get(10, 0) + 11
    R = round((18 + 7 + extra) * B) - v
    return h, R
for m in (3, 5, 8):
    out = []
    for extra in (0, 3, 6, 9, 12, 15, 18):
        hh, R = hist(m, extra)
        c = price(hh, 220, 11, R)[0]
        out.append('R=%d %s' % (R, '%+.2f%%' % float((c / P111t - 1) * 100) if c else 'n/a'))
    print('mid rank', m, ' | '.join(out), flush=True)
