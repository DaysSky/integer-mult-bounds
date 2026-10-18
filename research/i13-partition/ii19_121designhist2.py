"""THE TAILS' DESIGN-GROUNDED MODEL (the (b)-model!!) — the decisive tail extraction (SS1547!!).

THE SS1547 BRACKET: the coarse tails {8: 121, 1: 121}: c = 0.001792776 (+2.77% — THE SAME
LOG-MOMENT AS THE C VARIANT!!!); the fine (target-like): c = 0.001635781 (-6.23%!!).

THE LOG-MOMENT INSIGHT (SS1547!!): at q ~ 0.0018 the root equation is effectively a
TWO-PARAMETER model: (the mass, LM = Σ mass_r·ln(m/r))!!!  The C variant (+2.77%) and the
coarse-tail design hist (+2.77%) AGREE because their LMs agree (15,254 vs 15,253!!!) —
the shape beyond the (mass, LM) pair DOES NOT MATTER (to the 1e-5 level!!).

THE (b)-MODEL (THE DESIGN-GROUNDED TAILS!!): the tail t's chain: 0 -> THE BUILD FRAME
(THE SPAN OF leftovers[t] — computable!!) -> THE READ SLOT (tgt_slot[(t, -1)] — IN THE
PKL!!) IF s > span (the tail at the span already SATISFIES the read (the src's frame ⊇
the gate's!!!)) -> FULL (9!!).  THE INTERPOLATION ESTIMATE: the LM lands between the
brackets -> ~-0.3%: RIGHT AT THE FRONTIER — THE DECISIVE MEASUREMENT!!

THE PRICE: at the design's OWN R=286 ONLY (the consistent pairing: the SS1547 R=299
column was the INCONSISTENT pairing (the R=286 hist 117 mass light for R=299: the +347%
GARBAGE!!!)).  THE HONEST CAVEATS: the arrival law (R >= 299: the design at 286 is
INFEASIBLE: 2,690 > 9x286 = 2,574!!), the nesting (121/121 FAIL!!), the bit-side-only
payoff!!
"""
import sys, pickle, itertools
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
V, H = 121, 9

# the system [the SS1419 code]
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = [list(al) + [0, 0] for al in AL]
L.append([0.0] * 8 + [1.0, 1.0])
L = np.array(L, dtype=float)

def span_dim(lines):
    return int(np.linalg.matrix_rank(L[list(lines)]))

d = pickle.load(open('/Users/dayssky/integer-mult-bounds/research/i13-partition/ii19_121_design.pkl', 'rb'))
pool, pranks, leftovers = d['pool'], d['pranks'], d['leftovers']
tgt_slot, src_assign = d['tgt_slot'], d['src_assign']

def jumps(chain):
    chain = sorted(set(chain))
    return [b - a for a, b in zip(chain, chain[1:])]

def LM_of(h):
    m = 73.0
    return sum(r * z * np.log(m / r) for r, z in h.items() if r < m)

hist = Counter()
# (1) THE PIECES (156): 0 -> the build frame (pranks!!) -> the read dims -> FULL
piece_reads = {}
for (t, p), s in tgt_slot.items():
    if p >= 0:
        piece_reads.setdefault(p, set()).add(s)
for p in range(len(pool)):
    for j in jumps([0, pranks[p]] + sorted(piece_reads.get(p, set())) + [H]):
        hist[j] += 1
# (2) THE SOURCES (121): 1 -> the src_assign slots -> FULL
src_slots = {}
for (s, p), slot in src_assign.items():
    src_slots.setdefault(s, set()).add(slot)
for s in range(V):
    for j in jumps([1] + sorted(src_slots.get(s, set())) + [H]):
        hist[j] += 1
# (3) THE TARGETS (121): 0 -> the tgt_slot dims (ALL incl. the p=-1 leftover slots!!) -> the t-perp (8)
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
core = Counter(hist)
core_mass = sum(r * z for r, z in core.items())
print('the core (the pieces + the sources + the targets + the gathers + the copies):')
print('  the hist: %s' % dict(sorted(core.items())))
print('  the mass: %d; the LM: %.0f' % (core_mass, LM_of(core)))

# (4) THE TAILS: THE (b)-MODEL (the design-grounded!!)
print()
print('(4) THE TAILS: the (b)-model (0 -> span(leftovers[t]) -> s(t) if s > span -> 9!!):')
sp_hist = Counter(span_dim(leftovers[t]) for t in range(V))
print('  the leftover spans: %s' % dict(sorted(sp_hist.items())))
s_hist = Counter(tgt_slot.get((t, -1)) for t in range(V) if (t, -1) in tgt_slot)
print('  the (t, -1) read slots: %s' % dict(sorted(s_hist.items())))
h_b = Counter(core)
for t in range(V):
    sp = span_dim(leftovers[t])
    s = tgt_slot.get((t, -1), None)
    chain = {0, sp, H}
    if s is not None and s > sp:
        chain.add(s)
    for j in jumps(sorted(chain)):
        h_b[j] += 1
mass_b = sum(r * z for r, z in h_b.items())
ident = 9 * 286 + 73 + 2 * V * (H - 1)
print('  THE (b)-MODEL HIST: %s' % dict(sorted(h_b.items())))
print('  the mass: %d (the identity %d: %s!!); the LM: %.0f (the coarse: 15,254; the fine: 17,098!!)' %
      (mass_b, ident, 'OK' if mass_b == ident else 'OFF!!', LM_of(h_b)))

# THE PRICE at the design's OWN R=286 (the consistent pairing ONLY!!)
print()
print('THE PRICE at the design\'s R=286 (the consistent pairing!!):')
for tag, h in (('THE (b)-MODEL (the design-grounded!!)', h_b),):
    c, prof, det = pprice(dict(h), V, H, 286)
    if c is None:
        print('  %s: NO-ROOT %s' % (tag, det))
    else:
        print('  %s: c = %.9f (%+.2f%% vs frontier)' % (tag, float(c), (float(c) / FRONTIER - 1) * 100))
# the bracket for the comparison (the SS1547 numbers!!)
print('  [the bracket: the coarse tails: c = 0.001792776 (+2.77%!!); the fine: c = 0.001635781 (-6.23%!!)]')
print()
print('THE HONEST CAVEATS: (1) the arrival law: 2,690 > 9x286 = 2,574 (105%!!): the design')
print('  at R=286 is INFEASIBLE — the honest R >= 299 (the pkl\'s own R_honest!!); (2) the')
print('  nesting: 121/121 target chains FAIL (SS1515!!): unrealizable as-is; (3) the payoff')
print('  is BIT-side only (the selected κ is complex-bound!!).')
print('DONE')
