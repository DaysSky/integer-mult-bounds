"""Exact price of the idealised I_{11,1} A3-parity architecture histogram (per 6-target A3 block: 25 registers =
6 sources + 12 carriers + 7 empties; 14 piece arrivals via one middle node of rank m, 11 copies without middle node;
3 deliveries per target; targets 0 -> <d> (rank 1) -> t-perp), scaled to v = 220, vs P111-tuned.  Also a sweep of
the number of extra registers per block to locate break-even."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(blocks, m, extra_per_block, piece_frac=14 / 25):
    h = {}
    def add(ch, k=1):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    nreg = blocks * (18 + extra_per_block)
    npiece = round(nreg * piece_frac)
    v = blocks * 6
    # sources: 1-2-[m]-9-10-11 (piece) ; carriers 0-1-2-[m]-9-10-11 (piece) or 0-1-2-9-10-11 (copy); empties 0-9-10-11
    src = v; car = 2 * v; emp = nreg - src - car
    # assign piece arrivals first to sources then carriers
    p_src = min(src, npiece); p_car = min(car, npiece - p_src)
    add([1, 2, m, 9, 10, 11], p_src); add([1, 2, 9, 10, 11], src - p_src)
    add([0, 1, 2, m, 9, 10, 11], p_car); add([0, 1, 2, 9, 10, 11], car - p_car)
    add([0, 9, 10, 11], emp)
    add([0, 1, 10], v)                       # targets: keeper read at <d>, then t-perp
    h[10] = h.get(10, 0) + 11                # 11 decoder totals at rank 10
    return h, nreg - v
for m in (3, 5, 8):
    row = []
    for extra in (4, 7, 10, 13, 16):
        hh, R = hist(220 // 6 + 0, m, extra)
        hh2 = {k: v * 220 / (6 * (220 // 6)) for k, v in hh.items()}   # scale to v=220
        hh2 = {k: round(v) for k, v in hh2.items()}
        R2 = round(R * 220 / (6 * (220 // 6)))
        c = price(hh2, 220, 11, R2)[0]
        row.append('extra/block %d (R=%d): %+.2f%%' % (extra, R2, float((c / P111t - 1) * 100)))
    print('mid rank', m, ' | '.join(row), flush=True)
