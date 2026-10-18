"""THE DESIGN-DERIVED HISTOGRAM (the SS1515 audit's missed item 2) — the TRUE shape from
the design's own chains (ii19_121_design.pkl!!) instead of the A/B/D priors.

THE EXTRACTION: (1) the pieces' chains (0 -> the build frame (pranks!!) -> the read dims
(the tgt_slot!!) -> FULL!!); (2) the sources' chains (1 -> the src_assign slots -> FULL);
(3) the targets' chains (0 -> the tgt_slot dims (incl. the p=-1 leftover slots!!) -> the
t-perp (8!!)); (4) THE TAILS (121: NOT in the pkl!!): THE BRACKET — (a) the coarse
(0->8->9: the optimistic!!), (b) the fine (the target-like!!); (5) the gathers (the 9:
0->8->9 x8 (the even!!), 0->9 x1 (the odd!!)); (6) the copies (the MEASURED cst=73: the
{8: 8, 9: 1}!!).
THE MASS CHECK: == 9x286 + 73 + 1,936 = 4,583 EXACTLY (the design's R=286 structure!!) —
the extraction's own verification!!
THE PRICE: at the design's own R=286 (the honest caveats: the arrival law sets R >= 299
(the demand 2,690 > 9x286 = 2,574: the design at 286 is INFEASIBLE!!); the nesting fails
(121/121!!); the payoff is BIT-side only (the selected κ is complex-bound!!)).
"""
import sys, pickle
from collections import Counter
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
V, H = 121, 9
d = pickle.load(open('/Users/dayssky/integer-mult-bounds/research/i13-partition/ii19_121_design.pkl', 'rb'))
pool, pranks = d['pool'], d['pranks']
tgt_slot, src_assign = d['tgt_slot'], d['src_assign']
print('the design pkl: %d pieces, %d tgt_slot entries, %d src_assign entries, R_honest=%s' %
      (len(pool), len(tgt_slot), len(src_assign), d.get('R_honest')))

def jumps(chain):
    chain = sorted(set(chain))
    return [b - a for a, b in zip(chain, chain[1:])]

hist = Counter()
# (1) THE PIECES (156): 0 -> the build frame (pranks!!) -> the read dims (tgt_slot!!) -> FULL
piece_reads = {}
for (t, p), s in tgt_slot.items():
    if p >= 0:
        piece_reads.setdefault(p, set()).add(s)
for p in range(len(pool)):
    for j in jumps([0, pranks[p]] + sorted(piece_reads.get(p, set())) + [H]):
        hist[j] += 1
print('(1) the pieces: the jumps hist so far: %s' % dict(sorted(hist.items())))
# (2) THE SOURCES (121): 1 -> the src_assign slots -> FULL
src_slots = {}
for (s, p), slot in src_assign.items():
    src_slots.setdefault(s, set()).add(slot)
for s in range(V):
    for j in jumps([1] + sorted(src_slots.get(s, set())) + [H]):
        hist[j] += 1
# (3) THE TARGETS (121): 0 -> the tgt_slot dims (ALL entries incl. the p=-1 leftovers!!) -> the t-perp (8)
tgt_dims = {}
for (t, p), s in tgt_slot.items():
    tgt_dims.setdefault(t, set()).add(s)
for t in range(V):
    for j in jumps([0] + sorted(tgt_dims.get(t, set())) + [8]):
        hist[j] += 1
# (5) THE GATHERS (9): the even 0->8->9 x8; the odd 0->9 x1
hist[8] += 8; hist[1] += 8; hist[9] += 1
# (6) THE COPIES: the MEASURED cst=73 ({8: 8, 9: 1}!!)
hist[8] += 8; hist[9] += 1
mass_core = sum(r * z for r, z in hist.items())
print('(2)-(6) the core (the pieces + the sources + the targets + the gathers + the copies):')
print('  the hist: %s' % dict(sorted(hist.items())))
print('  the mass: %d (the tails to add: 121 x 9 = 1,089!!)' % mass_core)

# (4) THE TAILS' BRACKET + THE PRICE
ident = 9 * 286 + 73 + 2 * V * (H - 1)
print("the mass identity (the design's R=286): %d" % ident)
for tag, tail_js in (('COARSE (0->8->9: the optimistic!!)', [8, 1]),
                     ('FINE (the target-like!!)', [2, 1, 1, 1, 1, 1, 1, 1])):
    h2 = Counter(hist)
    for _ in range(V):
        for j in tail_js:
            h2[j] += 1
    mass = sum(r * z for r, z in h2.items())
    print()
    print('=== THE TAILS %s: the mass %d (the identity %d: %s!!) ===' %
          (tag, mass, ident, 'OK' if mass == ident else 'OFF!!'))
    print('  THE TRUE DESIGN HIST: %s' % dict(sorted(h2.items())))
    for R in (286, 299):
        c, prof, det = pprice(dict(h2), V, H, R)
        if c is None:
            print('  R %d: NO-ROOT %s' % (R, det))
        else:
            print('  R %d: c = %.9f (%+.2f%% vs frontier)' % (R, float(c), (float(c) / FRONTIER - 1) * 100))
print()
print('THE HONEST CAVEATS: (1) the arrival law: the demand 2,690 > 9x286 = 2,574 (105%%!!):')
print('  the design at R=286 is INFEASIBLE — the honest R >= 299 (the pkl\'s own R_honest!!);')
print('(2) the nesting: 121/121 target chains FAIL (SS1515!!): the design is unrealizable as-is;')
print('(3) the payoff: BIT-side only (the selected κ is complex-bound!!).')
print('DONE')
