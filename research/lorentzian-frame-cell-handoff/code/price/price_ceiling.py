"""Absolute pricing ceiling for I_{11,1} (v=220, h=11): every chain a single jump (sources 1->11, helpers 0->11,
targets 0->10, totals 10) -- no architecture can price better at a given R.  Prints c vs P111-tuned over R."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(R, tgt=((0, 10),)):
    h = {10: 220 + 11, 11: R}
    # targets: 0 -> 10 in one jump (mass 10 each)
    h[10] += 220
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
for R in range(700, 1001, 25):
    c = price(hist(R), 220, 11, R)[0]
    print('R', R, '%+.2f%%' % float((c / P111t - 1) * 100) if c else 'n/a', flush=True)
