"""Frame-top R420-style shape for I_{11,1}: 330 sections x (2 one-level pieces + 1 differentiator).
pieces = 660 branch registers (sources 1-2-m-9-[10]-11, carriers 0-1-2-m-9-[10]-11), 330 dead (one per section);
differentiators = 330 empties: 220 Q-deliveries (two-level 0-m-q-9-10-11) + 110 copies (0-9-10-11);
targets 0-2-10; 11 totals at rank 10.  R = 440 + 330 = 770 (+ overhead dead empties 0-9-11)."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(m, q, R, qtwo=True):
    h = {}
    def add(ch, k):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    add([1, 2, m, 9, 11], 220); add([0, 1, 2, m, 9, 11], 110); add([0, 1, 2, m, 9, 10, 11], 330)
    add([0, m, q, 9, 10, 11] if qtwo else [0, 9, 10, 11], 220); add([0, 9, 10, 11], 110)
    add([0, 9, 11], R - 770)
    add([0, 2, 10], 220); h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
for m, q in ((3, 7), (5, 7), (4, 7)):
    for qtwo in (True, False):
        c = price(hist(m, q, 770, qtwo), 220, 11, 770)[0]
        print('mid', m, 'Q', q, 'two-level Q' if qtwo else 'Q as plain empties', 'R=770: %+.2f%%' % float((c / P111t - 1) * 100), flush=True)
