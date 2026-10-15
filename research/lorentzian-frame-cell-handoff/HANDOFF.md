# Lorentzian I_{11,1} bit supplier: handoff (sessions of 2026-10-15)

Prepared by DaysSky with assistance from Claude.  Scratch research, not reviewed; claims are labelled
**proven** (exact/exhaustive computation, scope stated), **heuristic** (search result, no optimality claim) or
**estimate**.

## 0. The question

Can a bit word on the Lorentzian line system I_{11,1} (v = 220 lines, h = 11) beat the current bit supplier
P111-tuned (c = 0.001733427039589844, E8-based)?  A kappa gain is not required: a bit-supplier gain or an
architectural potential improvement suffices.

**Status: open.**
- Not proven worse: no all-word bound reaches break-even.
- Not shown better: no competitive word exists.
- A complete, independently verified Lorentzian frame-cell word exists (R = 11,494), but it is about 20x the cell
  floor.
- The realistic outlook from all constructions so far is negative (heuristic, not proven).

## 1. Setup and conventions

- **Lines:**
  - 55 P(ij) = e_i - e_j and 165 T(ijk) = e_i + e_j + e_k + f, in R^{11,1} with eta = diag(1,...,1,-1).
  - Rank 11, all in w-perp with w = (1^11; 3); w-perp is nondegenerate, signature (10,1).
  - Distinct lines have |<u,e>| <= 1.
- **Reader sets:**
  - R(t) = lines orthogonal to t.
  - |R(P)| = 129, |R(T)| = 115, so sum_t |R(t)| = 26,070.
- **Word format and checker:**
  - Format bitGen/1+mut; independent exact checker `code/tword/gcheck.py`.
  - Frames must be NONDEGENERATE subspaces.
  - The checker verifies:
    - nested climbs and content-in-frame;
    - exact F2 semantics on all columns (target final = y_t + x_t);
    - H1-H5 of the interleaved scalar-interface lemma;
    - the rank-mass identity.
- **Decoder:** binary labels give U U^T = J + G (mod 2).  Hence x_t + sum_{R(t)} x_u = sum_{i in label(t)} tot_i,
  where tot_i is the total of D10(i).
- **D10 frames:**
  - D10(i) = {P(ab), T(abi) : a,b != i}: 90 lines, rank 10, NONDEGENERATE (positive-definite D10).
  - So the 11 decoder totals can be retained at rank 10 (cst 110), or at FULL (cst 121).
- **Pricer:** `code/price/pricer.py`, price(hist, v, h, R); the hosting wall is about R = 7,920 for v = 220.
- **Register accounting:** "R" counts helpers; total registers = v + R.

### Break-even targets (exact pricer, chain-shape models, v = 220, h = 11, vs P111-tuned)

| R | one middle level | one level + target node read | two levels | two levels + node read |
|---|---|---|---|---|
| 550 | +6.37% | +4.00% | +1.67% | -0.49% |
| 553 | +6.11% | +3.76% | +1.42% | -0.73% |
| 564 | +5.18% | +2.87% | +0.51% | -1.60% |
| 568 | +4.84% | +2.55% | +0.18% | -1.92% |
| 575 | +4.27% | +2.00% | -0.38% | -2.46% |
| 584 | +3.53% | +1.29% | -1.11% | -3.15% |
| 596 | +2.57% | +0.37% | -2.05% | -4.06% |
| 608 | +1.62% | -0.54% | -2.98% | -4.95% |

**Break-even R:**
- about 630 for one level;
- about 600 for one level + node read;
- about 570 for two levels;
- about 545 for two levels + node read.

These are shape models (sources 1-2-mid-9-10/11, carriers 0-1-2-mid-9-.., targets 0-2-9-10, 660 deliveries,
11 totals at rank 10), not words.  For those stop-heavy shapes a word must reach roughly **R <= 600**.

**Superseded by session 2:** shapes with cheap chains price much better.  Those shapes have dead pieces skipping
t-perp, copies as empties, in-chain targets 0 -> S0 -> t-perp, and 440 deliveries.  Their break-even is ~690-740 for
frame union tops and ~720-757 for A3 tops; see 3b.  The reach lemma (3b) decides which of these shapes are
feasible.

## 2. Proven structural facts

### 2a. Source side (frame-cell class)

- **Covers:**
  - Every source needs >= 3 branches.
  - The 3-covers of R(s) by plane sections are good 4-frames and PPP triples.
  - The frame-independent line-mixing cut justifies the frame-cell class.
- **Good 4-frames:**
  - Types: TTTT (13,860) and PPTT (6,930), each with an even number of P lines.
  - Frames per line: 252 for P lines, 420 for T lines.
- **No partition:** with 55 P lines (odd), no partition of the lines into good frames exists.
- **No symmetric system** (two parity obstructions):
  - the P lines need a perfect P-P matching;
  - the T-T degree sum is 55 + 330 = 385, which is odd.
  - So every system has >= 2 asymmetric cells (>= 22 under Z11).
- **PPP covers are unusable** (source side and top side).
- **Cell bottleneck lemma** (free top, any middle):
  - A 2-register cell emits at most one s+a stream.
  - Forced targets must be served by stream nodes inside t-perp, or by the target's single rank-2 in-chain read.
  - R >= 2v + defects + extra cell registers.

### 2b. Cell floors (rigorous per system; minimum over systems is heuristic)

**Pool counting is invalid.**  Spreading 220 reads freely over cells gave floors of 548-552.  That is NOT valid:
each target reads ONE cell.

**Exact read assignment** (`lexact.py`, CP-SAT set packing, j = 0 cross-checked by the independent backtracker
`lxc.py`):

| system | defects | exact floor |
|---|---|---|
| lsa6_n548 | 108 | [564, 568] |
| lsa6_q548 (15 spare reads) | 108 | **[559, 567]**, explicit assignment at 567 = best found |
| lsa6_n550 | 110 | [568, 573] |
| lsa6_q550 (16 spare reads) | 110 | [560, 568] |
| lsa6_s185_a | 114 | [562, 569] |
| lsa6_r140_a | 136 | [577, 585] |
| lsa6_nr596 (read-light) | 144 | **584 exact** (j = 0 feasible) |
| lsa3_best_f (Z11) | 132 | >= 573 |

- Certificate for lsa6_n548: with slack 0, cells {4,53}, {35,60}, {59,71} and {10,84} have unique minimum unserved
  sets that collide.
- The obstruction is global: no pairwise or mandatory conflicts exist.
- **No in-chain cell reads:** best floor 596.
- **Absolute floor (any word):** 426.

### 2c. Top (system lsa6_q548; scripts in `code/lmid`)

- **Plane-section covers** (`ltop4.py`):
  - Every target needs >= 4 plane sections covering R(t) by routable lines (some system cell inside the section),
    plus one in-chain cell read.
  - 213 targets need exactly 4 and 7 need 5.
  - So there are >= 667 delivered registers.
- **A2-only sections** (3-user planes, `ltop4a.py`): every target needs 5.  Hence any 4-section top uses >= 1
  two-user section; >= 1,801 incidences are forced through 2-user sections (`lmt.py`).
- **Frame-top parity identity** (`lftop.py`): for ANY good frame {t, e1, e2, e3},
  R(t) = sum_i tot({t,e_i}-perp) + x_e1 + x_e2 + x_e3.  Verified exactly for all 220 targets.
  - This is the R420 mechanism: section totals are shared by both users, so in-chain reads are free.
  - On lsa6_q548 the unroutable part forces a private correction.
    - Own frames: 23-58 lines.
    - Best over all good frames through t: 16-28 lines (`lftop2.py`).
  - For NO target and NO frame does it fit routably in one extra section.
  - So a shared-total frame top costs >= 4 deliveries per target (R >= 660) on this system.
- **Parity covers by routable section totals exist** for every target (`lparspan.py`): 1[R(t)] is in the F2 span of
  {rt(S)}, span dimension 86-120.
  - The minimum weight is unknown; the CP-SAT lower bound is 5.
  - Note: with >= 5 sections per target this gives >= 4 deliveries.

### 2d. Middle (system lsa6_q548)

- **One-level reach bound** (`lreach2.py`, `lreach3.py`, `lgmax.py`; exhaustive over all flats;
  WLOG N = perp(perp(cells)) with DFS and b-pruning).
  - "Strict one level" means every register visits <= 1 frame strictly between rank 2 and rank 9.
  - Then incidences through node N are <= k * min(3 a_N, 2 b_N), where:
    - a_N = lines covered by system cells inside N;
    - b_N = |perp N|;
    - k = registers at N.
  - The global maximum per register is G* = 40 (D5 apex hub: 20 lines, perp 20).
  - First bound: **R >= 585**.
  - Refined with A2-packing reach limits: **one-level R >= 603** for this system (perfect-efficiency bound; real
    designs are far above).
  - One level + node reads is NOT constrained by this counting.
- **Node census** (`lnodes2.py`, `lnodes3.py`):
  - Pair-closure nodes have rank 3-4 and <= 8 covered lines.
  - Apex hubs D(A,p):

    | |A| | rank | lines | covered (max) | perp |
    |---|---|---|---|---|
    | 5 | 5 | 20 | 13 | 20 |
    | 6 | 6 | 30 | 22 | 12 |
    | 7 | 7 | 42 | 30 | 6 |
    | 8 | 8 | 56 | 46 | 2 |

### 2e. Apex structure (exact identities)

- D10(p) is a D10 root system (P(ij) <-> eps_i - eps_j, T(ijp) <-> eps_i + eps_j).  P lines lie in 9 apexes,
  T lines in 3.
- R(T(abc)) = sum_{p in abc} tot(D10(p) ∩ t-perp): 3 rank-9, single-user terms; equivalently
  sum_p tot(D(S,p)) + P(ab) + P(ac) + P(bc), with S = [11] \ abc.
- R(P(bc)) = sum_{p not in bc} tot(D10(p) ∩ P(bc)-perp): 9 terms.
- Each D8 total tot(D(S,p)) (|S| = 8) is needed by exactly 2 users: T(pbc) and P(bc).  There are 495 such totals.
- tot(D(S,p)) = tau_p + mu_p(b) + mu_p(c) + sigma_p(bc).  This is algebraically cheap but NOT frame-legal: D10(p) is
  not inside t-perp.
- P(bc)-perp contains E8(M) (the I_{9,1} lines on M = [11] \ bc, 120 lines; degenerate span) plus 9 lines T(bck).

## 3. Built artifacts

- **`code/lmid/lw.py`:** I_{11,1} word builder.
  - Closed-mask frames with nondegeneracy check, integer basis (P(01..9,10), T(012)), Gram form.
  - Emits bitGen/1+mut for gcheck.
  - `frame_alg` = exact F2 transform at a frame.
- **`code/lmid/build3.py`:**
  - Pipeline: per-target min plane-section top (887 private parts); one-level middle line -> cell -> node -> section ->
    t-perp; exact algebra; totals at FULL on dead registers.
  - Result `word3.json.gz` (regenerable in about 12 min): **gcheck PASS**, R = 11,494, beyond the hosting wall,
    unpriced.
  - **This is the first verified Lorentzian frame-cell word.**
- **Other middles** (all valid by construction; R includes totals):

  | builder | design | R |
  |---|---|---|
  | build5 | capacity-aware greedy | 11,819 |
  | build6 | every part from its section | 15,533 |
  | build7 | simulated annealing over node covers | 11,637 |
  | bc2 | demand-driven broadcaster/collector | 22,846 |

- **Diagnosis:**
  - With private parts (887 distinct sums of about 28 lines), node-based middles pay one register per node
    arrival.
  - Broadcaster/collector (R420's mechanism: single-line broadcasters read and never consumed, deliveries collect
    along ONE nested chain) fails because a broadcaster can only serve a NESTED family of read frames.
  - Section-local nodes never nest across sections, so every read spawns a broadcaster.
  - bc1.py: random broadcaster chains leave about 68 of 115 lines unread even with 12 chains per target.
- **Paired top** (`ltopP.py`: in-chain read of a co-user's full delivery): CP-SAT found only 956 deliveries
  (bound 126); not usable as formulated.

## 3b. Session 2 (9-hour run, 2026-10-15 13:12-) — new results

All scripts are in `code/llp/` and `code/price/`; the full log is `NOTES-full-log.md`.

**Pricing (exact pricer, chain-shape model, vs P111-tuned).**  Uneven jumps price better.

| shape | break-even R |
|---|---|
| zero-level (cell -> section) | ~755 |
| one-level, middle rank 3 or 8 | ~677 |
| one-level, rank 4 or 7 / rank 5 or 6 | ~642 / ~632 |
| one-level + target node read, rank 3 or 8 | ~656 |
| two-level (3,4), (3,8), (7,8) | ~611 |
| two-level (4,6), (4,7), (5,7) | ~570 |

**proven: all-systems union-coverage LP** (`lpsolve.py`, `lp_model.md`; S11-symmetric, 319 node orbits = all closed line
sets with >= 2 perp lines, 7 plane-section orbits).  Optimum = 660 registers = the branch floor, so R >= 440 only.
Coverage counting cannot separate one-level words from the floor (with or without the >= 2 deliveries cut, which holds
because two plane sections always leave >= 15 lines of rank 9 uncovered: `l2cover.py`).  What decides the question is
exact mod-2 assembly, not coverage.

**proven: defect-1 parity tops** (`lparity3.py`, `la3.py`).  For an A3 subsystem (6 lines = edges of K4: 4 A2
triangles, 3 orthogonal opposite pairs) and t in it:
tot(Q1-perp) + tot(Q2-perp) + tot({t, opp t}-perp) = 1_{R(t)} + x_{opp t}, with Q1, Q2 the two triangles through t.
- These are exactly the defect-1 triples: E8 7,560 A3s (378 per line); I_{11,1} 13,200 A3s (612 per P line, 276 per T
  line), plus T-line triples through non-orthogonal TT pairs (61-line sections).
- A2 sections have 3 users, so sections are shared more than in the frame top (defect 3, 2-user sections).
- The defect line lies in none of t's sections, so it must come from a keeper read at <opp t>; then t cannot also read
  a section in-chain (nesting), so targets take 3 deliveries (R420-like).
- I_{11,1}: at most 27 disjoint A3s (every A3 holds >= 2 P lines; OPTIMAL), covering 162 of 220 lines.
- Compatible A3 packings (sections meeting other blocks only in whole cells): E8 none of full size (exhaustive), both
  lattices about 8 blocks.

**proven: fully routable A3 design on R420's D4 partition** (`e8a3.py`, `data/e8a3_sol_0.json`).
- Each line takes 2 triangle cells (in its block) + 1 R420 pair cell, forming an A3; the top is self-dual.
- 140 sections (80 E6 + 60 D6), versus R420's 180; 0 unroutable incidences.
- Anatomy: E6 = B' + 8 triangle pieces (one per other block); D6 = R420's D6.
- **heuristic, middle cost:** any 4 E6 pieces span the whole E6, so each E6 needs >= 3 node arrivals (best nodes are
  rank-4 D4s with 3 pieces serving 4 E6s).  With R420's mechanism (merge + Q-deliveries + copies) this gives about 580
  registers, R ~ 460 > 420.  Not excluded: cross-section corrections through the 8 non-B' lines that lie in all three
  of a target's sections.
- **heuristic, same accounting for I_{11,1}:** with kappa >= 3 pieces per section, the cost is >= 5.3 registers per
  target, versus ~3.9 at break-even.

**Exact U = 0 own-frame routability** (`code/lmid/fru0.py`): Z11 and no-symmetry both UNKNOWN after 1 h each, so it is
undecided.

**Parity-top landscape (proven for the representative targets, exhaustive).**  Sections may be plane sections or
A3-perp frames (rank 8, 6 users).  Combinations of <= 4 sections with defect <= 1 are ONLY:
- the A3 triples (E8 378, I11 P 612, I11 T 276);
- 1204 TT-non-orthogonal triples per I11 T line.

So every top is a frame triple (defect 3) or one of these.  Sections have <= 3 users.

**Section-assembly accounting.**
- **proven, independence lemma:** registers delivered from one section to different users are linearly independent.
  If k arrival groups each carry a line that every delivered user needs exclusively, then
  arrivals >= k + (#delivered users) - 1.
- **heuristic, cost model:** the remaining steps assume R420-type assembly (sections carry exclusive parts, the
  triple-overlap part is delivered once per target, nodes fed by cell registers).
- **heuristic, E8:** frame top: k = 2 per D6, giving R420's 540 registers exactly.  A3 top: k_E6 = 3 (any 4 E6
  pieces span the E6), giving >= 580 registers.  So frame tops are optimal in E8 and the A3 design does not beat R420.
- **I_{11,1}:**
  - The triple overlap per target is 25-56 lines (E8: B' 12 + 8).
  - **proven:** K4-type exclusive parts have closure = the whole section (no proper node contains them), so k >= 2 at
    any depth.
  - **heuristic:** partition-like systems share the triple part but meet the cell lemma (3 registers per cell, R >= 770).
    Non-partition systems avoid it, but must assemble 25-56-line triple parts per target: in one level that costs
    ~20 dead registers per block, and in two levels the break-even drops to 570-634.
  - **heuristic:** every accounting tried lands at R ~ 650-770, above the best break-evens (570-677).
- **proven, chain constraint:** the move lever "carriers copy at the cell (0 -> 2)" would raise break-evens by 20-33,
  but it is not available: >= 2 fresh helpers per source must stop at <s>.

**A3-parity architecture: the closest Lorentzian candidate** (`code/llp/lkex*.py`, `code/price/price_a3exact.py`).

*Pricing.*
- **proven:** the pricer is extremely sensitive to local rank mass at fixed R, so histograms must be mass-consistent.
  Sources climb 10, helpers 11, targets 10, totals 10.
- **proven, exact pricer on the shape:** the A3 shape is much cheaper than the standard shapes.
  - Targets go 0 -> <d> -> t-perp.
  - Differentiators skip the middle: empties 0-9-10-11, carrier copies 0-1-2-9-10-11.
  - Merged-away pieces die without the t-perp stop.
  - With one-level Q-deliveries the break-even would be R ~ 777 (rank-5 nodes) to ~811 (rank 3/8), versus 629-675
    for the standard one-level shapes.
  - **Corrected** (`price/price_a3exact2.py`): the Q-deliveries carry the 42-56-line A3-perp triple part, so they need
    two middle levels (cell -> mid -> A3-perp node of rank 7/8 -> section).  Break-even is then R ~ 712 (mid rank 5)
    to ~756 (mid rank 3, Q-node 8).  Use these numbers.
- **proven, frame-top shape** (`price/price_frame.py`, R = 770 = 330 sections x (2 pieces + 1)): -3.5..-5.6% with
  two-level Q-deliveries; +0.6% only if Q-deliveries were plain empties, which is impossible.  Frame tops lose.
- **proven, E8 control:** R420 is reproduced (-4.59%).  The E8 A3 shape at R = 460 gives -5..-6%, so there is no E8 gain.

*Section assembly.*
- **proven:** the exclusive part of every section of every 3-section top is covered by EXACTLY 2 proper nodes (optimal;
  pieces 12-35 lines).  Full sections need 3.
- **proven, shareability** (sinks >= ceil(|piece|/2)):
  - OK for PT-inc 56, PT-disj 66 (|E| 19), PP 70 (|E| 14), PTT 71 (|E| 24) and TT 56.
  - NOT OK for large A2 exclusive parts (ratio 0.54-0.78) or for TT* 61.

*Accounting.*
- **heuristic, idealized:** 25 registers per 6 targets, R ~ 696; against the corrected break-even 712-756 this is
  only +0.85..+3.4%.
- **heuristic, per-target best tops with measured shareability:** P ~4.5 and T ~4.17 registers per target, so
  R ~ 713, i.e. at the corrected break-even, IF realizable.
- **proven, counting:** no consistent all-A3 design exists in I_{11,1}.  T lines need 165 PTT triangles but P lines
  offer only 110 triangle slots, so >= ~55 T lines take TT* (or frame) tops at about +1 register each.

*Caveats, which push the estimate to break-even:*
- Q-deliveries need a second middle level to carry the 42-56-line A3-perp triple part.
- Users of a shared section have different exclusive parts unless they share an A3 block.
- At most 27 disjoint A3s exist, so 58 lines need TT* or frame tops; this gives R ~ 777.
- Defects, routability, keeper reads and decoder totals are not counted.

*Verdict.*  **heuristic:** an architectural potential at break-even +- a few %, not a realized gain.  This is the
next thing to build: a globally consistent design (tops + cells + shared nodes) with exact section-level GF(2)
content.

**Reach lemma (proven; `code/llp/nodes.pkl` for the reach table).**
- From the checker rules (every gate operand climbs to the gate frame; frames are nested), along any content path
  s_u -> r1 -> ... -> target t the gate frames are nested, so t lies in F-perp for every frame F on the path.
- Let A run over the registers that carry x_u at a frame of rank <= 2, and F_A = A's first frame of rank >= 3.  Then
  R(u) is covered by the sets lines(F_A-perp), plus targets that read x_u themselves at rank <= 2.
- Max reach |lines(F-perp)| by rank of F (exhaustive over node orbits):

  | rank of F | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|---|---|
  | max reach | 129 | 85 | 56 | 36 | 25 | 17 | 11 | 6 |

  E8 control: D4 quads reach 12, and R420 gives 9 x 12 = 108 >= 63.
- **Consequence:** with 3 branches per line and cells of <= 3 lines, <= 8-9 cell-stage registers carry x_u.  Direct
  cell -> rank-8-node chains then reach <= 54 < 115-129 targets, so that shape is impossible.
- The A3-shape break-even ~757 (pieces cell -> 8) was for an infeasible shape.
- In self-dual A3 designs, a cell's exclusive targets must be covered by its registers' first-frame perps.  This is
  exactly the kappa_ex = 2 cover, so >= 2 registers per cell take a low stop: phi >= 2/3..1.
- Prices (`price/price_a3mix.py`, `price/price_a3reach.py`):

  | low stop at rank 3, fraction phi | 1/4 | 1/3 | 1/2 | 1 |
  |---|---|---|---|---|
  | break-even R | 755 | 749 | 739 | 705 |

  At phi ~ 0.75 the break-even is ~720-725.
- I_{11,1} needs one more middle level than E8 (fan-out at rank <= 5-6, fan-in at rank 8), and every extra stop
  costs.

**Aggregated counting LP for A3/TT* designs (proven within its cost models; `code/llp/e11agglp.py`).**
- Plane-type balance over the exact option classes.
- With kappa = 2 for every section (the rigorous arrivals model): registers >= 935, so R >= 715, consistent or not.
- With measured shareability per option, consistent designs: R >= 828.
- The Z11 consistent CP-SAT (`e11design2.py`) found no design at all in 900 s.  Its bound was R >= 794 (shareability
  costs).
- **A3/TT* class, heuristic:** the floor is R >= 715 against a reach-compliant break-even of ~720-725.  At most ~1% of
  room, and only for a perfect zero-waste consistent design, which has not been found.

**Stop-entropy budget (`code/price/budget.py`).**
- At fixed R the word beats P111-tuned iff the sum over all local jumps of r (m/r)^q* stays under a budget B(R):
  q* = c(P111-tuned), m = 91.
- Budget above the all-single-jump baseline: 26.1 units at R = 660, 23.9 at R = 720, 22.5 at R = 760.
- Exchange rate: one extra register ~0.057 units; one extra stop 0.005-0.012 units.  So one register is worth ~5-10
  stops.
- Per-chain costs are listed by the script, e.g. carrier 0-1-2-8-9-10-11 0.027, target 0-1-10 0.006.

**4-part kappa = 1 shapes** (`price/price_4sec.py`, `price/price_4sec2.py`).
- Pieces cell -> 8 -> t-perp would give +9.8% at the ideal R = 660, but that violates the reach lemma.
- The reach-compliant version (cell -> m1 -> 8 -> t-perp) gives +2.2..+4.3% at R = 660, break-even ~700-735.

**Top landscape completed (proven, exhaustive per representative; `code/llp/lpar4_min.py`, `lpar_inchain.py`,
`lunion_min.py`, `e11agglp2.py`).**
- **Parity tops with 4 plane sections are impossible:** the minimum defect over 4 sections through t is 42 lines
  (P and T).  The method was validated by recounting the 3-section defect-1 tops (612 / 1480).
- 3-section parity tops with defect 2-3 never have all defect lines inside one section.  In-chain parity reads exist
  only through 280 TT* tops per T line, where d (a P line) lies in both TT* sections.
- With that option the optimistic aggregated floor drops to R >= 705.8.
- **Exact union covers by 3 sections exist:** P 252 (PP, PT-disj, PT-inc); T 1120.  These are the frame tops of the
  old main line.  4-section exact union covers are plentiful.
- The union-coverage LP (R >= 440) is compatible with the reach lemma, so its gap is mod-2 exactness plus
  independence.

**Frame union tops re-priced; routability and middle capacity (`code/llp/lroute_sa.py`, `lmatch3.py`,
`lframe1.py`, `lmidcap.py`; `code/price/price_frameinchain.py`, `price_general.py`).**
- **Cheap-chain pricing of in-chain union tops:** dead pieces skip t-perp, copies are 0-9-10-11, and targets read
  0 -> S0 -> t-perp.  This moves the break-even for the old main line from ~600 to **~690-740**.

  | case | break-even R |
  |---|---|
  | no extra cell registers | 740 |
  | 50 extra cell registers | 716 |
  | 108 extra cell registers | 692 |
  | targets with a rank-2 read | about 40 lower |

  - Model-A counts: R = 550 at +11.25% (two-level pieces, low stop at rank 3).  This matches the earlier inch2v
    estimate (break-even 682-743).
  - Section 1's "R <= ~600" target applies only to the old stop-heavy shapes.
- **Shared parts must be identical** (kappa = 2 with full-closure parts).  So the deliveries of each line u pair up
  the targets in R(u).  |R(u)| is odd, which forces >= 1 non-shared delivery per line.
- **Weak routability is the real union-top requirement.**  A target-line pair (t,u) is routable if some section of
  t contains some cell of u (some e in M(t), f in M(u) with e _|_ u, f _|_ t, e _|_ f).  This is much weaker than the
  fru0 condition.
  - Stored systems have 7,400-8,000 unroutable (t,u) pairs.
  - A good-frame anneal reaches **U = 0**, with 98 non-reciprocal mates.
  - Z11-symmetric systems stay at U ~ 1,750.
- **Binding obstacle: middle capacity.**
  1. Reach forces low first frames: rank 3 carries <= 6 lines, rank 5 <= 20.
  2. Pieces sharing a node through a common user are disjoint.
  3. A node with k inputs has only k outputs.
  4. Pieces of 15-30 lines therefore need node sharing with overlapping content (R420's D4 quads).  That needs
     partition-like frames, which bring the cell lemma (R ~ 770).
  5. Unstructured systems waste inputs.  For lsa6_q548: 702 pieces on 688 distinct nodes, about 1,880 cell-stage
     registers needed against 660.

**Assessment.**
- **heuristic:** no Lorentzian frame-cell architecture found beats P111-tuned.  The binding reason is structural:
  sections, exclusive parts and triple-overlap blocks are 2-5x larger than the largest shareable nodes (~20-30 lines),
  whereas in E8 the triple part B' (12 lines) is itself a node.
- **proven gap:** a rigorous all-word bound is still missing.  The union-coverage LP only gives 660, and exact-assembly
  bounds were derived only for the classes above.

## 4. Next goals (priority order)

Updated at the end of session 2.  Every class examined is at or below break-even once all layers are counted.  The
items below are the remaining loopholes, in order of plausibility.

1. **Node sharing for frame union tops** (largest nominal room: model-A R = 550 against a break-even of ~690-740).
   - A routable system exists: weak U = 0, `code/llp/lroute_sa.py`.
   - The blocker is middle capacity.  A rank-8 node with k inputs needs k useful outputs, and reach limits inputs to
     <= 6 lines (rank-3 first frames).
   - Look for designs where many sections take overlapping content from one node, without a full frame partition.
     Candidates:
     - A3-perp triple parts: the 3 orthogonal-pair sections of an A3 have disjoint users.
     - Rank-5/6 hubs: D5 has 20 lines and reach 20.
   - Measure with `lmatch3.py`, `lmidcap.py` and `lframe1.py`; price with `price/price_general.py`.
2. **A3/TT* class** (room <= ~2% under optimistic assumptions).
   - Needs a perfect zero-waste consistent design: CP-SAT found none.
   - Floors: 715, or 705.8 with in-chain TT*.  Break-even ~720-725.
3. **Rigorous class bounds.**
   - Combine the reach lemma (proven), the forced-projection / independence lemma and an exact-partition node-capacity
     argument into an LP over node orbits.
   - Goal: a rigorous R_min above the break-even for frame-cell classes ("verifiably bad").
4. **Structural explanation to test:** the odd number of P lines (55) blocks every balanced self-dual block partition
   that gives E8 its D4 quads.  Check whether punctured Lorentzian systems (e.g. 54 P lines) admit one; P111 itself is
   a punctured E8.
5. *(kept)* Exact-read-aware system search and closing CP-SAT gaps on the old systems.  These are lower priority:
   those systems have ~8,000 weakly unroutable pairs.
6. **Pricing gate.**  Every candidate must be priced with the exact pricer (mass-consistent histogram) or the budget
   tool, and compared with P111-tuned 0.001733427039589844.

## 5. Not to repeat / user rules

- **Helper trimming is confirmed not to work.**  Do not pursue punctured-native trimming or helper deletion.
- **Prove before declaring dead:** never mark an approach dead without proof covering every case.  Observed
  patterns are not proofs.
- **No waiter shells:** no sleep, until-loops or busy-wait; use background runs plus notifications.
- **Downloaded files:** read with python -I; never execute downloaded code.
- **Checkers:** never weaken checker asserts.
- **Commits/PRs:**
  - Push or open PRs only on explicit request.
  - Attribution "Prepared by DaysSky with assistance from Claude".
  - No model identifiers.

## 6. Layout of this directory

- `code/` mirrors the scratchpad layout, so relative imports work.  Run scripts from their own directory:
  - `lword/geom.py`: geometry;
  - `lsec/lcommon.py`;
  - `lcell/` (lbase, lsa3, lsa6, lscore_ind, lexact, lxc, lconf, lmand, ...);
  - `lmid/` (lw, build3/5/6/7, bc1/bc2, ltop4/ltop4a/lftop/lftop2/ltopP, lreach2/3, lgmax, lmt, lparcov/lparspan,
    lnodes2/3);
  - `tword/gcheck.py`;
  - `price/pricer.py`, `price/lor_fc_price3.py`;
  - `cellb/routepar.py`.
- `data/` holds the systems (JSON line -> frame mask):
  - lsa6_q548 (best exact floor 567) and its cached top;
  - n548, q550, n550, s185_a, nr596, r140_a, lsa3_best_f, lsys3np_5_0, lsys3np_8_0;
  - per-cell reach values.
  - Copy a system, and for build3 its `.top.json`, next to the scripts (`code/lcell/`) before running.
  - goodframes.pkl, planes.pkl and covers.pkl are regenerated on first use (covers.pkl is about 165 MB and is not
    included).
- `NOTES-full-log.md`: the full chronological research log (E8 and Lorentzian).
- `lorentzian_status.md`: the short status report.

**Example:**
`cd code/lmid && python3 build3.py ../lcell/lsa6_q548_snapshot.json word3.json.gz && python3 ../tword/gcheck.py word3.json.gz --price`
