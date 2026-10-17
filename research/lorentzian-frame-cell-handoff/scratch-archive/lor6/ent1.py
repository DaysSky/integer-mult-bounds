import mixcore as M
def ok(C, kc, eC, H, e, kh, ks=2, kt=3):
    Hs = {}
    def add(r, z):
        if z: Hs[r] = Hs.get(r, 0) + z
    for p in M.split(10, ks): add(p, M.v)
    for p in M.split(10, kt): add(p, M.v)
    for p in M.split(11 - eC, kc): add(p, C)
    for p in M.split(11 - e, kh): add(p, H)
    add(10, 11)
    c = M.price_mixed(Hs, [(11 - eC, C), (11 - e, H)])
    return c is not None and c >= M.P111
for eC in (0, 1, 2):
    row = []
    for kc in (3, 4, 5):
        lo, hi = 0, 4000
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ok(mid, kc, eC, 0, 0, 1): lo = mid
            else: hi = mid
        row.append('kc%d: R<=%d' % (kc, lo))
    print('all helpers entrance rank %d:' % eC, ' | '.join(row), flush=True)
