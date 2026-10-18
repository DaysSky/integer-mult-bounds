# Lorentzian I_{11,1} bit words: status (session 2026-10-15)

**Update 2026-10-18, session 8 (HANDOFF.md section 3j): lever A on E8 moves the bit frontier itself.**  P111's helper
bill 429 + 10 extra carriers is block-local.  An exhaustive keeper-plan census (freeline x thirds x receivers per
block, exact, calibrated against full builds) gives 8 extra carriers for P111's puncture set.  Over all 17,478
affinely independent puncture sets the minimum is 8, attained only by P111's set.  Cell-sum helpers (one helper holding
x_a + x_b of a cell, read from the cell's empty) bring it to 5, which is the exact per-block minimum: R = 434 (package
research/e8-bit-p111-r434).  After the tuner, the official nine-stage chain gives c = 0.001744385950814795279853,
+0.5715% over E1.  The Lorentzian target therefore moves up.  The gain is in the punctured unit, not in the
middle, and gives no Lorentzian word.

**Update 2026-10-17, session 7c (HANDOFF.md section 3i): I_{13,1}.**  (1) With lean stops the I_{13,1} frontier
allows 3.8-4.6v helpers at cst 156, not 3.2v.  (2) Register identity R + v = consumed + dead: frame tops need >= 2
consumed per target (no target perp has a 2-cover by sections).  So R = v + dead, and dead must stay <= ~3v.
(3) PG(2,3) frame top: load 79 per line, demand rank 0.60, half sharing 1.4, misalignment 21,930.  Large hubs serve
only 2-5 demands; the per-line pool cover is 4 (line partners) or 2-3 (arbitrary vectors).  (4) Width-12 exit would
add ~+1v of allowance, but cleanup inverse rows cannot be target-local when pools are shared.  (5) Proven: no
I_{13,1} partition into complete star-D4 blocks and complete Pasch pairs exists (parity lemma plus CP-SAT), so
E8-style half sharing is impossible; I_{16,1} fails the same count.  No word built; frontier not reached.

**Update 2026-10-17, session 7 (HANDOFF.md section 3h).**  The z-group lever is closed.  (1) Totals-feeder lemma
(proven): every word contaminates >= v distinct registers before the scatter; frame-0 middles absorb this, but a
pure z-group word pays about v extra frame-0 registers, so I_{11,1} with 3 groups carries 3v frame-0 registers and
at most ~1.0v group helpers at the frontier, no more than a frame-0 word.  (2) E8 has no cover by 3 hyperplanes
(exhaustive over all 77,488 line-spanned hyperplanes), so z-grouped E8 needs 4 groups and >= 345 entries; an
R420-quality middle then prices at -12%.  (3) Exact frontier budget: 1.95 per line for I_{11,1} helpers and stops
against 1.80 for P111, for twice the demand.  Best word unchanged (blkA4, -71.6%); only a middle strictly better
than R420 per incidence remains, and it would first be an E8 result.

**Update 2026-10-16, session 6f.**  The bit frontier is beaten on E8 itself, not by a new line system: research/e8-bit-p111-e1
(one entrance-rank-2 helper on P111-tuned) gives c = 0.001734473240795253742474 (+0.0604%) on the official nine-stage chain.  No
new line system result changed this session.

**Update 2026-10-16, session 6d (new line systems; HANDOFF.md "Session 6d").**  Root-like lines in R^{8,1}: at most 127
(exact: Lagrangian count + orthogonal-frame classes), below the 130+ that h = 9 needs, so h = 9 is closed for root-like units.
Decoder value is the deficit term 8v - 9 cst (+2.8% per cst unit on P111).  Every full-E8 decoder found costs exactly 72
(conjecture: cost >= 72 - #punctures).  Double-star decoders realise x = 54/102 (deficit value 330 > 321), but in the bitE8
format the saving needs per-total cuts at punctured-line frames.  On P111 a single such piece nets at most ~+0.26% after
block splits, with 49 phase-B frame conflicts.  No new line system gives a drastic gain under the current format.

**Update 2026-10-16 (sessions 6-6c; details in HANDOFF.md sections 3f and "Session 6c").**  Best verified word
R = 3,656 (gcheck PASS, `code/lbuild/word_blkA4.json.gz`).  The pricer's hosting wall for v = 220, h = 11 is R = 880, and break-even against
P111-tuned is ~650-840 depending on stops per register.  Other Lorentzian units (I_{n,1}, whole-lattice I_{10,1}
and I_{11,1} searches, h = 9 near the LP bound) do not reach the decoder cost per line that a word with an
R420-quality middle would need (estimate, #620 helper model).  On the block partition, a cell-hub middle does not
shrink the demand content, and an idealised varying-part hub middle already needs ~970 registers (greedy, no
content building).  Hub-sharing builders measured R = 4,129-4,717.  Aligned good-frame partitions need exactly 52
punctures (CP-SAT optimal), so an R420 port only exists at v <= 168, where the decoder cost kills the price.  Verdict unchanged: not proven worse, no
competitive construction, and every measured route points away from break-even.  The sections below are the
2026-10-15 snapshot.

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

## Session 6g update
Proven: root-like Lorentzian systems have at most C(h+1,3)+1 lines (h >= 11; 165 at h = 10, attained by I_{10,1}).  Every break-even line count in the model is above this ceiling, so a Lorentzian frontier would need a decoder cheaper than h(h-1), a system that is not root-like (none found; the best mixed-norm searches return the root-like I_{n,1}), or a middle better than R420 at about 2x E8's load.  Exact decoder costs: I_{11,1} x = 0.500 (optimal B0), I_{12,1} 0.500, the 298 system 0.520.
