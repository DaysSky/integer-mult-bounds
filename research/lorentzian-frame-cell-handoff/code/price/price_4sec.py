"""4-section kappa=1 shape (in-chain section + 3 delivered sections per target, every exclusive part inside ONE proper
node of rank m).  Per target (sections with 3 users): in-chain section = 3 pieces read in-chain at S (pieces climb to S
and die: [..,2,m,9,11]); delivered section = 1 piece delivered straight from its node ([..,2,m,10,11]) + 2 copies
(empties reading the piece at its node: [0,m,10,11]).  Targets 0 -> (defect frame dd) -> S -> t-perp.
Exact counts at v = 220: pieces 440 (220 sources + 220 carriers), copies 440 -> R = 660 + extra dead empties.
Prints c vs P111-tuned for node ranks m and defect frame ranks dd (0 = no defect read)."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m, dd, R, u=3):
    h = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    v = 220
    n_in = v            # in-chain pieces (3 per in-chain section, sections shared by 3 users -> 1 per target)
    n_del = v           # delivered pieces (3 delivered sections x 1/3)
    n_copy = 2 * v      # copies
    # sources are pieces: 220 sources take the in-chain role ([1,2,m,9,11]); carriers the delivered role
    add([1, 2, m, 9, 11], n_in)
    add([0, 1, 2, m, 10, 11], n_del)
    add([0, m, 10, 11], n_copy)
    extra = R - n_del - n_copy; assert extra >= 0
    add([0, 9, 11], extra)
    add([0, dd, 9, 10] if dd else [0, 9, 10], v)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(m, dd, R):
    c = price(hist(m, dd, R), 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
for m in (3, 5, 7, 8):
    for dd in (0, 1, 2):
        row = []
        for R in (660, 700, 750, 800, 850):
            p = pct(m, dd, R); row.append('R=%d %s' % (R, '%+.2f%%' % p if p is not None else 'n/a'))
        print('node rank', m, 'defect frame', dd, ' | '.join(row), flush=True)
