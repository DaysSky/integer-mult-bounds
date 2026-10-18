# I_{13,1} dead-minimizer: architecture result and honest verdict (session 2026-10-18)

Scratch research by DaysSky with assistance from Claude.  Not reviewed, not a word; claims labelled.
**Sign convention (verified against README): kappa = c is the exponent saving in T(n) = O(n (log n)^{1-kappa});
HIGHER c IS BETTER.  P111-tuned c = 0.001733427039589844; E1 (frontier) c = 0.001734473240795253742474.**

## Architecture

PG(2,3) frame top of I_{13,1} (91 good frames, 610 distinct demands; sessions 6h/7c) with a shared-piece
middle assembled by CP-SAT:

- **proven (CP-SAT OPTIMAL, deadmin_primal.py):** all 610 demands assemble from **573 non-leaf pieces**
  (content-piece model: GF(2) content + closed nondegenerate frame rank <= 10 inside the demand frame;
  covers = disjoint partitions into <= 4 pieces + free leaf fills; pieces shared across demands at one
  register each).  907 pieces used; 66 pieces serve >= 2 demands (max 5); 334 leaf fills are branch
  registers.  Register identity (7c, c_t = 2 proven): R = 2v + dead = 728 + 573 = 1,301 = 3.57v.
- LP relaxation floor 150.05 (w_merge = 0); the integer optimum 573 is the honest model minimum.

## Exact-pricer verdict (chain-shape model, correct signs)

| dead | branches | kappa | vs P111-tuned |
|---|---|---|---|
| 573 (proven min) | (1,1,2,3,6) | 0.0017529 | **+1.06%** (above E1 too) |
| 573 | (1,2,2,3,5) | 0.0017355 | +0.06% |
| 573 | (1,1,3,3,5) | 0.0017469 | +0.46% |
| 573 | (1,1,2,9) | 0.0018331 | +5.69% |
| 600 | (1,1,2,3,6) | 0.0017337 | -0.05% (break-even dead ~598) |
| 705 | (1,1,2,9) | 0.0016239 | -6.37% |

- kappa DECREASES with more dead at fixed shape (fragmentation outweighs hosting value): the architecture's
  max kappa is at the proven-minimum dead = 573.  The "break-even dead" numbers of the intermediate scans
  are where kappa crosses P111-tuned from above as dead grows.
- Shape sensitivity is large (+5.7% to +0.06% across branch shapes at dead 573): joint shape optimisation
  has room, but the binding uncertainty is not shapes.

## The one remaining structural risk (RESOLVED: the feeding layer does NOT close)

The chain-shape pricer prices HISTOGRAMS, not functionality.  Feeding-layer arithmetic on the actual
optimal design (deadmin_primal.pkl):

- 824 DISTINCT piece frames for 827 used pieces (822 singletons: almost no frame sharing).
- Every line's content must reach 22-267 piece frames (median 92) - branch copies (2/line, ~5 nested
  stops) cover <= ~10 frames per line: 3,640 frame visits against 18,781 required merge-ins
  (content sizes: min 1, median 30, max 56, sum 19,605).
- Mid-layer lower bound: (18,781 - 3,640) / ~6 frames fed per mid = **>= ~2,500 extra registers**.

With the mid layer counted: R ~ 728 + 573 + 2,500 ~ 3,800 = 10.4v, and kappa falls with every middle
register (the scans): far below break-even.  **Same verdict as all prior Lorentzian architectures.**

## Root cause and the precise fix (new)

The top-layer set-cover model allowed sharing BETWEEN demands (pieces shared at one register each) but
the optimum picked DISTINCT FRAMES per demand (824 frames / 827 pieces): sharing pieces is not sharing
frames.  The middle repeats at full width.  A future attempt must make the ILP objective charge for
DISTINCT FRAMES (frame-aligned designs), which is the algebraic content of "R420 alignment" -- E8's
partition shares 70 quads + 180 D6 frames for its 180 cells, I13's PG top shares none.  The parity
lemma (6h, proven) already showed no fully frame-aligned partition exists for I13; the open question is
whether a PARTIALLY aligned one exists whose frame count is low enough (need ~ <= 200 frames for the
+1% regime: 824 -> 200 saves ~600 x 3 merge-ins x 1/6 ~ 300 registers... the required frame sharing is
~4x).

## Status (final for this session)

- NOT a word; the architecture as modelled (feeding free) is above the frontier (+1.06%) but the
  feeding layer costs >= 2,500 registers by incidence counting -> **far below break-even as built**.
- Real artifacts: proven-optimal 573-piece top assembly; exhaustive I13 cover/reach censuses; full
  kappa-vs-shape landscape (correct signs); the frame-sharing diagnosis above.
- Next (if resumed): frame-aligned ILP (charge distinct frames), or a different top with intrinsic
  frame sharing (the 17-Pasch-pair partition: half sharing 1.90 vs PG's 1.40 is the known best).

## Status (final for this session)

- NOT a word; the architecture as modelled (feeding free) is above the frontier (+1.06%) but the
  feeding layer costs >= 2,500 registers by incidence counting -> **far below break-even as built**.
- Real artifacts: proven-optimal 573-piece top assembly; exhaustive I13 cover/reach censuses; full
  kappa-vs-shape landscape (correct signs); the frame-sharing diagnosis above.
- Next (if resumed): frame-aligned ILP (charge distinct frames), or a different top with intrinsic
  frame sharing (the 17-Pasch-pair partition: half sharing 1.90 vs PG's 1.40 is the known best).

## Files (research/i13-partition/)

base13.py, lgeo13.py (geometry); part13free.py (partition); reach13.py (reach table);
deadmin_instance.py/.pkl (223,755 candidate flats); deadmin_menus2.py/.pkl (122k covers);
deadmin_lp.py (LP floor 150.05); deadmin_primal.py/.pkl (CP-SAT OPTIMAL 573);
deadmin_primal2.py (rank-weighted variants: 577-589 pieces, shallower profiles);
n13allcovers.py P/T (suspended): exhaustive rank-3-frame 4-cover census.
