import sys
sys.path.insert(0, '.')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
# rank-7 sections Q-perp: s sections per target (1 in-chain + s-1 delivered); pieces climb pre + mid + [7, 10, 11]
def pct(s, X, pre_s, pre_c, mid, tgt=(0, 7, 10)):
    h = {}; npieces = 220 * (s - 1) + X; R = npieces - 220
    def add(ch, k):
        assert all(b > a for a, b in zip(ch, ch[1:]))
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    add(pre_s + mid + [7, 10, 11], 220); add(pre_c + mid + [7, 10, 11], npieces - 220)
    add(list(tgt), 220); h[10] = h.get(10, 0) + 11
    c = price(h, 220, 11, R)[0]
    return R, float((c / P111t - 1) * 100) if c else None
for s in (4, 5):
    for nm, ps, pc_, mid in (('cells,3', [1, 2], [0, 1, 2], [3]), ('cells,3,5', [1, 2], [0, 1, 2], [3, 5]), ('cells,5', [1, 2], [0, 1, 2], [5]), ('nocell,3', [1], [0, 1], [3]), ('nocell,3,5', [1], [0, 1], [3, 5])):
        print('s=%d %-11s' % (s, nm), ' | '.join('X=%d R=%d %+.2f%%' % ((X,) + pct(s, X, ps, pc_, mid)) for X in (0, 50, 100)), flush=True)
