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
- How the in-chain reads are counted decides the floor:
  * pool count (220 reads spread freely over cells): best systems 548-552.  NOT a valid exact floor.
  * EXACT read assignment (lcell/lexact.py: each target reads ONE cell; each bottleneck cell picks one minimal
    unserved set over all stream patterns and closure-node pairs, or takes a 3rd register; CP-SAT set packing).
    j=0 is infeasible for every read-saturated system tested (548 x2, 550 x2 -- one with 16 spare reads -- and 572),
    cross-checked by an independent backtracker (lcell/lxc.py) with a 4-cell hand-checkable certificate for 548;
    a read-light control system is feasible under both.  Full minimisation: 548 system sum j in [16, 20] -> exact
    floor in [564, 568]; a second 548 system (15 spare reads) [559, 567]; 550 systems [568, 573] and (16 spare
    reads) [560, 568]; a 136-defect system [577, 585].  (A global parity-level route model was too large: inconclusive.)
  * no in-chain cell reads at all: best 596.
- Best EXACT-read floor found: 567 (explicit read assignment: lcell/lsa6_q548_snapshot.json, 108 defects + 19 extra
  cell registers; three more low-defect systems at 568-569); proven per-system lower ends 559-564.
  A read-light system reaches 584 with j = 0.
So the cell-level floor of this class (heuristic minimum over systems, rigorous per system) is ~559-567 with exact
reads (596 without reads); the earlier "552 optimistic" figure was an artefact of pool counting.  The absolute floor
for any word is 426.

## Pricing (exact nine-stage pricer, v=220, h=11, vs P111-tuned 0.0017334; chain-shape models, not words)
| design shape | R=564 | R=568 | R=584 | R=596 |
|---|---|---|---|---|
| one middle level | +5.18% | +4.84% | +3.53% | +2.57% |
| one level + target node reads | +2.87% | +2.55% | +1.29% | +0.37% |
| two middle levels | +0.51% | +0.18% | -1.11% | -2.05% |
| two levels + target node reads | -1.60% | -1.92% | -3.15% | -4.06% |
(R=550, the old pool-count floor: +6.37 / +4.00 / +1.67 / -0.49%.)

## Middle depth
Every cell's sum stream first lands on its own private rank-3 node, so all sharing happens above rank 3 (cells rank 2,
sections rank 9).  Multi-cell nodes covering 40-60% of a cell's forced targets exist, so a one-level middle is not
excluded; nothing decides one vs two levels yet.

## Verdict
NOT proven worse (no all-word bound reaches break-even) and NOT shown better (no word).  In the natural frame-cell
class, a word built exactly at the best explicit exact-read cell floor (567-568) would land between about -1.9% and +4.8%
against P111-tuned depending on middle depth (at 564: -1.6% .. +5.2%; proven per-system lower ends reach 559) (no-read floor 596: between -4.1% and +2.6%).  The exact read assignment removed
~16-20 registers of the earlier optimism (pool-count floor 548-552, window -0.5%..+6.4%).  R420 shows E8 can sit
exactly on its class floor; whether a non-partition Lorentzian middle can is open.  Real words above the floor do worse.
Open: construct the middle (the R420 analogue) for a non-partition Lorentzian system; decide one vs two middle levels.

## Method (shared with the E8 result)
Cell bottleneck lemma: if a cell C={s,a} carries only its two branch registers, x_s and x_a leave C only in two
streams (at most one carries s+a); every register later carrying them sits at frames containing the stream's next
frame N ⊋ C.  A target whose every route for a line passes through C must meet such a stream inside its reading
frames or read C in-chain (one rank-2 read per target).  E8, R420 D4 partition: every cell needs a 3rd register
under any top with 2 deliveries (R >= 405; 420 under Z15) and R >= 390 under any top -- R420 is optimal in its class.
Files: scratchpad/cellb (E8), scratchpad/lcell (I_{11,1}), scratchpad/price (pricing), hf/NOTES.md (log).
