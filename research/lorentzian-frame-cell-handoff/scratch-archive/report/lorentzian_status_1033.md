# Lorentzian I_{11,1} bit words: status (session 2026-10-15)

Scope: bit supplier, bitE8-style format with closed or general nondegenerate frames, monotone frame chains.
"Frame-cell sources": every source has 3 branch registers first-mixing at the cells {s,f} of a chosen good
4-frame (the only 3-covers of R(s) by plane sections are good frames and PPP triples), plus extra branches.

## Proven (exact / exhaustive computations)
1. Good 4-frames are only TTTT (13,860) and PPTT (6,930); each holds an even number of P lines.  With 55 P lines,
   no partition of the lines into good frames exists.
2. No symmetric good-frame source system exists: P lines need a perfect P-P matching (55 odd), and the T-T degree
   sum 55*1 + 110*3 = 385 is odd.  => every system has >= 2 asymmetric cells (each +1 register); >= 22 under Z11.
3. PPP covers are unusable (their mates are pairwise non-orthogonal: the mates can never receive the source, and as
   a top the mates lie in no section).
4. For the systems examined, no good-frame top routes any target (13-24 lines of R(t) missing under every frame
   triple through t), so targets need >= 3 delivered registers (4-section-type tops).

## Lower bounds (per system; valid relaxation incl. general frames)
Refined per-cell screen (free top): a 2-register cell emits at most one s+a stream; doubly/singly forced targets
must be served by stream nodes inside t-perp or by the target's single rank-2 in-chain read.
R >= 2v + asymmetric cells + extra cell registers.
- Best system found (non-symmetric local search, independently rescored): 440 + 112 + 0 = 552.  It uses 218 of the
  220 single cell reads; without in-chain cell reads the same system needs 624.
- Best system optimised for the no-read version: 599-601 (reader demand only 50).
- Best Z11-symmetric system: 572.
So the cell-level floor of this class sits between ~552 (optimistic) and ~600 (robust) -- heuristic minima over
systems, rigorous per system.  The absolute floor for any word is 426.

## Pricing (exact nine-stage pricer, v=220, h=11, vs P111-tuned 0.0017334; chain-shape models, not words)
| design shape | R=553 | R=600 | R=608 |
|---|---|---|---|
| one middle level | +6.1% | +2.3% | +1.6% |
| one level + target node reads | +3.8% | ~0% | -0.5% |
| two middle levels | +1.4% | -2.4% | -3.0% |
| two levels + target node reads | -0.7% | | -5.0% |

## Middle depth
Every cell's sum stream first lands on its own private rank-3 node, so all sharing happens above rank 3 (cells rank 2,
sections rank 9).  Multi-cell nodes covering 40-60% of a cell's forced targets exist, so a one-level middle is not
excluded; nothing decides one vs two levels yet.

## Verdict
NOT proven worse (no all-word bound reaches break-even) and NOT shown better (no word).  In the natural frame-cell
class, a word built exactly at the cell floor would land between about -0.7% and +6% against P111-tuned depending on
middle depth (robust floor ~600: between -5% and +2.3%).  R420 shows E8 can sit exactly on its class floor; whether a
non-partition Lorentzian middle can is open.  Real words above the floor do worse.
Open: construct the middle (the R420 analogue) for a non-partition Lorentzian system.

## Method (shared with the E8 result)
Cell bottleneck lemma: if a cell C={s,a} carries only its two branch registers, x_s and x_a leave C only in two
streams (at most one carries s+a); every register later carrying them sits at frames containing the stream's next
frame N ⊋ C.  A target whose every route for a line passes through C must meet such a stream inside its reading
frames or read C in-chain (one rank-2 read per target).  E8, R420 D4 partition: every cell needs a 3rd register
under any top with 2 deliveries (R >= 405; 420 under Z15) and R >= 390 under any top -- R420 is optimal in its class.
Files: scratchpad/cellb (E8), scratchpad/lcell (I_{11,1}), scratchpad/price (pricing), hf/NOTES.md (log).
