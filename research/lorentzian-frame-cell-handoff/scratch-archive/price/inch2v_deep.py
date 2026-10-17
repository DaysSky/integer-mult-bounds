from mpmath import mp
from pricer import price
P = mp.mpf('0.001733427039589844234749')
def run(name, v, h, sec, tot_rank, ntot, tot_fresh, nodes, copystop=True, tnode=None):
    def loc(waste):
        L = {}
        def add(ch, n):
            for a, b in zip(ch, ch[1:]): L[b - a] = L.get(b - a, 0) + n
        pre = [0, 1] if copystop else [0]
        add([1] + nodes + [sec, sec + 1, h], v)
        add(pre + nodes + [sec, sec + 1, h], 2 * v)
        add(pre + nodes[:1] + [h], waste)
        add([0, h], tot_fresh)
        add([0] + ([tnode] if tnode else []) + [sec, sec + 1], v)
        L[tot_rank] = L.get(tot_rank, 0) + ntot
        return L
    R0 = 2 * v + tot_fresh
    f = lambda w: price(loc(w), v, h, R0 + w)[0]
    c0 = f(0); lo, hi = 0, 4 * v - R0
    if f(hi) >= P: be = 'beats at wall R=%d' % (R0 + hi)
    else:
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if f(mid) >= P: lo = mid
            else: hi = mid
        be = 'beats P111t iff R <= %d' % (R0 + lo)
    print('%-22s levels %-10s zero-waste R=%d c=%s (%+.2f%%); %s' % (name, nodes, R0, mp.nstr(c0, 7), float((c0 / P - 1) * 100), be), flush=True)
for nodes in ([2, 4], [2, 5], [3, 5], [2, 4, 5]):
    run('E8 punctured v=111', 111, 8, 6, 7, 9, 9, nodes, tnode=nodes[-1])
for nodes in ([2, 7], [4, 7], [2, 5, 8], [3, 6, 8]):
    run('I_{11,1} v=220', 220, 11, 9, 10, 11, 11, nodes, tnode=nodes[-1])
