import sys
sys.path.insert(0, '.')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist2(X, pre_s, pre_c, mid, extra='piece', tgt=(0, 8, 10)):
    h = {}; R = 440 + X
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    add(pre_s + mid + [8, 10, 11], 220); add(pre_c + mid + [8, 10, 11], 440)
    if extra == 'piece': add(pre_c + mid + [8, 10, 11], X)
    else: add([0, 9, 11], X)
    add(list(tgt), 220); h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h, R
def pct(X, *a, **k):
    h, R = hist2(X, *a, **k)
    c = price(h, 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
for X in (0, 50, 105, 150, 200):
    print('U+L=%d R=%d' % (X, 440 + X), ' | '.join('%s %s %+.2f%%' % (nm, ex, pct(X, ps, pc_, mid, extra=ex)) for nm, ps, pc_, mid in (('cells,3,5', [1, 2], [0, 1, 2], [3, 5]), ('nocell,3,5', [1], [0, 1], [3, 5])) for ex in ('piece', 'dead')), flush=True)
