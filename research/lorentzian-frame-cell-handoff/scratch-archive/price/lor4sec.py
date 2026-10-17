"""Exact price of the I_{11,1} 4-section architecture's forced chain structure at R = 3v = 660 (v=220, h=11,
11 totals of rank 10), vs P111-tuned.  Registers: 4v = 880 (220 sources + 660 helpers); per target 3 deliveries read at
t-perp (rank 10) + 1 section read in-chain (register ends section -> FULL).  Targets 0 -> section(9) -> t-perp(10)."""
from mpmath import mp
from pricer import price
P = mp.mpf('0.001733427039589844234749')
v, h, R = 220, 11, 660
def prof(src_chain, dlv_chain, inch_chain, n_src_inch):
    loc = {}
    def add(ch, n):
        for a, b in zip(ch, ch[1:]): loc[b - a] = loc.get(b - a, 0) + n
    add(src_chain[0], n_src_inch); add(src_chain[1], v - n_src_inch)       # sources: in-chain-ended or delivered
    n_inch_h = v - n_src_inch                                               # in-chain-ended registers total = v
    add(inch_chain, n_inch_h); add(dlv_chain, R - n_inch_h)
    add([0, 9, 10], v)                                                      # targets
    loc[10] = loc.get(10, 0) + 11                                           # totals (COPY ranks)
    return loc
cases = {
  'no middle (cell->section direct; coverage-infeasible upper bound)':
     (([1, 2, 9, 11], [1, 2, 9, 10, 11]), [0, 2, 9, 10, 11], [0, 2, 9, 11]),
  'one middle node at rank 5':
     (([1, 2, 5, 9, 11], [1, 2, 5, 9, 10, 11]), [0, 2, 5, 9, 10, 11], [0, 2, 5, 9, 11]),
  'one middle node at rank 7':
     (([1, 2, 7, 9, 11], [1, 2, 7, 9, 10, 11]), [0, 2, 7, 9, 10, 11], [0, 2, 7, 9, 11]),
  'copies at line + node rank 5 (E8-like forced copy stop)':
     (([1, 2, 5, 9, 11], [1, 2, 5, 9, 10, 11]), [0, 1, 2, 5, 9, 10, 11], [0, 1, 2, 5, 9, 11]),
}
for name, (sc, dc, ic) in cases.items():
    for nsi in (220, 0):
        c = price(prof(sc, dc, ic, nsi), v, h, R)[0]
        print('%-62s sources in-chain-ended=%3d: c = %s (%+.2f%% vs P111t)' % (name, nsi, mp.nstr(c, 8), float((c / P - 1) * 100)), flush=True)
print('--- sweep (copy stop at <s> forced for the 3 copies per line):')
best = None
for cs in (0, 1):
    pre = [0, 1, 2] if cs else [0, 2]
    for nodes in ([], [3], [4], [5], [6], [7], [8], [3, 5], [4, 7], [5, 7], [3, 7]):
        sc = ([1, 2] + nodes + [9, 11], [1, 2] + nodes + [9, 10, 11]); dc = pre + nodes + [9, 10, 11]; ic = pre + nodes + [9, 11]
        c = price(prof(sc, dc, ic, 220), v, h, R)[0]
        tag = 'copystop' if cs else 'no-copystop'
        print('%-12s middle ranks %-8s c = %s (%+.2f%%)' % (tag, nodes, mp.nstr(c, 8), float((c / P - 1) * 100)), flush=True)
