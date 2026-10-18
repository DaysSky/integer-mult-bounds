# I_{13,1} partition probe (session 2026-10-15, research/i13-partition)

Question: does the I_{13,1} Lorentzian line system (v = 78 P + 286 T = 364 lines, h = 13) admit a partition
of its lines into good 4-frames — the structure that E8's D4 partition gives R420 and that I_{11,1} provably
lacks (55 P lines odd, T-T degree sum 385 odd)?

**Answer: YES (exact cover found by CP-SAT; no symmetry assumed).**

## Facts (exact / exhaustive computations; `~/.venv/bin/python3`, code in this directory)

1. **Good 4-frames** (`base13.py`, goodframes13.pkl): 70,785 frames, census TTTT 51,480 + PPTT 19,305
   (same type law as I_{11,1}: every good frame holds an even number of P lines).  All nondegenerate.
   Frames per line: P 495, T 855.
2. **Parity obstructions vanish** (exact counts):
   - P lines: 78 = even -> P-P perfect matching possible (I_{11,1}: 55, odd).
   - If all P lines sit in PPTT frames: 39 PPTT frames force 78 T lines into PPTT (1 T-mate each) and the
     remaining 208 into TTTT (3 mates each); T-T degree sum = 78 + 624 = 702, even (I_{11,1}: 385, odd).
3. **Z13-invariant partition does NOT exist** (`part13.py`; 20,092 translation orbits of frames, 28 line
   orbits; CP-SAT INFEASIBLE).  As in I_{11,1}, symmetry must be broken.
4. **No-symmetry partition EXISTS** (`part13free.py`, CP-SAT OPTIMAL): 91 frames = 39 PPTT + 52 TTTT,
   cover counts {1: 364} (every line in exactly one frame).  Saved to `partition13.pkl`.
   This is the I_{13,1} analogue of E8's D4-quad partition.
5. **Reach table** (`reach13.py`, good-frame (pairwise-orthogonal) chains from P(01) and T(012) starts;
   max perp size by frame rank): 2: 138, 3: 77, 4: 56, 5: 31, 6: 30, 7: 15, 8: 12, 9: 3.
   I_{11,1} reference: 2: 85, 3: 56, 4: 36, 5: 25, 6: 17, 7: 11, 8: 6.  Rank-8 reach 12 vs 6 -> rank-8
   section designs need half as many rank-<=8-carrying registers per line as I_{11,1}.

## Why this matters (context from the I_{11,1} handoff)

- The I_{11,1} verdict rests on: no partition -> no symmetric source system -> >= 2 asymmetric cells ->
  defects (exact-read cell floor 559-567 vs break-even ~570-630, i.e. at best break-even) -> and, deeper,
  no zero-waste "hub alignment" anywhere (the R420 mechanism needs a balanced self-dual block partition).
- With a partition, I_{13,1} can run the R420 template verbatim: cells = 91 x 6 = 546 orthogonal-pair
  cells, cell-bottleneck floor R >= 3 x 546 - 364 = 1,274 = 3.5v.  Exact scenario break-evens for I_{13,1}
  (price/price_i13.py, full log): R <= 1,179 (k=3) / 1,020 (k=4).  So the plain R420 analogue still loses
  (~ +8% at k3, +25% at k4) -- the partition alone is not a word.
- But the highest-counting-potential Lorentzian class, the rank-8/10 4-section in-chain architecture
  (ideal R = 2v = 728; +14.9% at (cells,3,5) with break-even X ~ 270, the largest room of any family,
  vs ~145-190 for I_{11,1}), was blocked in I_{11,1} by exactly the missing partition (hub alignment).
  I_{13,1} has one, plus double the rank-8 reach.  **The decisive open question becomes: does the
  partition support a zero-waste middle (R420's quad/D6 mechanism) on I_{13,1}?**
- Caveat (scope): the notes' parity arguments for I_{11,1} frame-cell floors used odd-P counting; the
  I_{13,1} cell floor is 3.5v by plain counting, and the win must come from the in-chain / 4-section /
  rank-10 mechanisms, whose per-layer costs are unmeasured for I_{13,1}.

## Next steps (proposed)

1. Verify the partition independently (recompute cover from partition13.pkl, check frame legality,
   nondegeneracy, and the cell-bottleneck screens per cell: doubly-forced counts, k_C).
2. Quad structure of the partition: the 91 frame spans are rank-4 nondegenerate flats with 6 cells each;
   compute their perps (hub sizes), check the E8 zero-waste pattern (arriving span = needed span) at the
   cell -> quad -> section levels.
3. Price the I_{13,1} shapes that the partition unlocks (R = 2v in-chain 4-section with rank-10 nodes;
   R420-type with in-chain D-analogues) with the exact pricer.
4. Symmetry of the found partition: is it related to M13/M11-type designs, or essentially arbitrary?
   (Affects whether the middle can be built symmetrically.)

## Files

- `base13.py`: I_{n,1} geometry (parametric Geom), good 4-frames, Z13/affine group, nondegeneracy;
  writes `goodframes13.pkl`.
- `part13.py`: Z13-invariant partition test (INFEASIBLE).
- `part13free.py`: no-symmetry partition (OPTIMAL; writes `partition13.pkl`).
- `reach13.py`: max perp size by frame rank (writes `reach13.pkl`).
