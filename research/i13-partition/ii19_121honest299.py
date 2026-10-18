"""THE HONEST-R BRACKET: the (b)-model hist + the +13 registers at R=299 (the consistent pairing!!).

THE SS1551 RESULT: THE (b)-MODEL (the design-grounded tails: 0 -> span(leftovers[t]) ->
the read slot if s > span -> 9!!) PRICES c = 0.001770409 (+1.49%!!) AT THE DESIGN'S R=286
(the mass 4,583 EXACT!!).  BUT R=286 VIOLATES THE DESIGN'S OWN ARRIVAL HEURISTIC (2,690
reads > 9x286 = 2,574: R >= 299: the pkl's R_honest!!).

THE DECISIVE QUESTION: DOES THE (b)-SHAPE AT THE HONEST R=299 STILL CROSS?!  THE
CONSISTENT PAIRING: the (b)-hist + THE +13 REGISTERS' CHAINS (the arrival-slack
registers!!): THE BRACKET — (a) the coarse-13 ({8, 1} each: the optimistic!!), (b) the
fine-13 (the piece-like {2, 1x6, 1}: the pessimistic!!): the mass identity at R=299:
9x299 + 73 + 1,936 = 4,700 EXACTLY (the SS1547 lesson: the consistent pairing ONLY —
the R=299-with-the-286-hist was the +347% GARBAGE!!).

THE ESTIMATE (the SS1536 R-sensitivity: ~-1.7 to -1.8 points per +13 R!!): the (b) at
299 ~ -0.3%: RIGHT AT THE FRONTIER — THE MEASUREMENT DECIDES!!
"""
import sys
from collections import Counter
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
V, H = 121, 9
# THE (b)-MODEL HIST (SS1551!!): the mass 4,583 = 9x286 + 73 + 1,936 EXACT!!
hb = Counter({1: 1548, 2: 425, 3: 113, 4: 116, 5: 76, 6: 35, 7: 82, 8: 25, 9: 2})
assert sum(r * z for r, z in hb.items()) == 9 * 286 + 73 + 2 * V * 8
ident299 = 9 * 299 + 73 + 2 * V * 8
print('THE HONEST-R BRACKET: the (b)-hist (SS1551!!) + the +13 registers at R=299!!')
print('the mass identity at R=299: %d' % ident299)
for tag, js13 in (('COARSE-13 ({8, 1}: the optimistic!!)', [8, 1]),
                  ('FINE-13 (the piece-like: the pessimistic!!)', [2, 1, 1, 1, 1, 1, 1, 1])):
    h = Counter(hb)
    for _ in range(13):
        for j in js13:
            h[j] += 1
    mass = sum(r * z for r, z in h.items())
    print()
    print('=== THE %s: the mass %d (the identity %d: %s!!) ===' %
          (tag, mass, ident299, 'OK' if mass == ident299 else 'OFF!!'))
    print('  the hist: %s' % dict(sorted(h.items())))
    c, prof, d = pprice(dict(h), V, H, 299)
    if c is None:
        print('  R=299: NO-ROOT %s' % d)
    else:
        print('  R=299: c = %.9f (%+.2f%% vs frontier)' % (float(c), (float(c) / FRONTIER - 1) * 100))
print()
print('DONE')
