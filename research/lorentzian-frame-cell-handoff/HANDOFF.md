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
- Session 3 (rank-8 frame sections, section 3c):
  - **Top counting:** R = 572-583.
  - **Proven node and middle walls for the examined families:**
    - per-design R >= 1,001-1,133;
    - >= 260 nodes in any design.
    - (A triangle-top bound R >= 660 was retracted.)
  - **New structure:** the M11 / S(4,5,11) triangle design gives perfect T sharing.
  - **Remaining shape:** varying-part piece designs aligned at every level.

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
- The U = 0 system (`code/llp/lroute_best_11.json`, 98 non-reciprocal mates) does no better:
  - top-level model-A R ~ 870 (107 parts need 3 nodes; 135 sections have differing parts);
  - 544 pieces on 481 nodes, so ~1,449 cell-stage registers needed against 660;
  - the first-frame layer covers >= 97% of incidences.
- **Middle depth versus price** (model-A R = 550):

  | piece-chain middle stops | price at R = 550 | break-even R | feasibility |
  |---|---|---|---|
  | (3, 8) | +11.3% | 740 | rank-8 nodes would need inputs of >= ~17 lines; rank-3 frames carry <= 6 |
  | (5, 8) | +8.9% | 704 | reach is tight |
  | (3, 5, 8) | +5.9% | 656 | consistent with register conservation + content caps + reach |
  | (4, 6, 8) | +5.2% | 640 | |

  So the realistic potential of this line is break-even ~656, against the floor 550 + 0.5 x (non-reciprocal mates) +
  overheads.

**Rank-8 frame sections: the largest remaining loophole** (`code/llp/lr8design.py`, `lr8parts.py`,
`lr3cover.py`; `code/price/price_r8sec.py`).
- **Construction:**
  - Sections are F-perp for rank-3 frames F through t.  F-perp is a rank-8 node, and its users are the 3-6 lines
    of F.
  - R(t) is union-covered by 4 such perps (min 4 found).
  - Each target reads 1 section in-chain (0 -> F0-perp -> t-perp) and 3 delivered.  Delivered users get DISTINCT
    parts; in-chain users read GF(2) combinations of their section's delivered outputs.
  - So every cell-stage register is a delivery and no copies are needed: **R = 440 in counting.**
  - Delivered pieces go rank 8 -> t-perp with no section stop.
- **Prices at R = 440:**

  | chain | price | break-even R |
  |---|---|---|
  | cells, middle stops 3, 5 (content needs rank-5 inputs) | +13.5% | 662 |
  | cells, middle stop 5 | +16.9% | 710 |
  | cell-free, middle stops 3, 5 | +16.0% | 698 |

  This matches the earlier inch2v estimate (+20% at R = 2v).
- No pairing parity obstruction, since parts are per target.
- **Open layers:**
  1. A consistent design: every line in exactly 4 used frames, every orthogonal pair covered.  A Z11 CP-SAT is
     running.  An all-A3 version is impossible by counting.
  2. Parts with the in-chain span condition and independent delivered parts (`lr8parts.py`).
  3. Middle: parts must be generated by k inputs of <= 20 lines each, and reach needs >= ~32 registers carrying
     each line at the mid level.
- **proven, exhaustive (`code/llp/lr3cover_exact.py`):** no line has R(t) covered by 3 perps of rank-3 frames through
  t, i.e. by 3 rank-8 nodes.
  - Reduction: each such perp lies in a pair section, so a 3-cover refines an exact 3-section pair cover with each
    exclusive part inside one node.
  - P: no exact cover has any exclusive part inside a node.
  - T: only the 420 (PT-disj)^3 covers have all three exclusive parts inside nodes, but none of their 11,340 node
    triples covers R(t).
  - Consequences: rank-8-section tops need >= 4 sections; sources without cells need >= 4 branches.

**E8 analogue: 4-covers by rank-5 flats** (`code/e8r5/`).
- All E8 4-covers of R(t) by rank-5 flats are (D5, D5, D5, A5): three A3-perps plus a single-user A5.  There are
  5,040 per target.  All exclusive parts span their flats, so the A5 costs one assembly leftover per target.
- Locally any two users of an A3 can get identical parts.  But the **exact** hosting layer (consistent assignment of
  multiply-covered lines) hosts only **53-58 of 120** targets.  Annealing on the exact objective did not improve
  this, which suggests a structural cap near v/2.
- Realistic E8 price (rank-3 middle stop, reach-compliant):
  - all hosted: R = 360, +1.5%;
  - 30 unhosted: -2.1%;
  - 60 unhosted: -5.4%.
- So the E8 version is <= ~1.5% even in the ideal case.  This corrects the earlier +7.4% figure, which used a
  different chain model and no A5 leftovers.

**Assessment (end of session 2).**
- **heuristic:** no Lorentzian frame-cell architecture found beats P111-tuned.  Both top classes have positive
  *ideal* potential:

  | top class | ideal (zero-waste) potential | break-even R |
  |---|---|---|
  | A3 parity | <= ~2% | ~720-725 |
  | frame union, in-chain | +6..8% at model-A R = 550 | ~656-688 (three-level reach-compliant middle) |

  Every attempt to realise zero waste fails at a lower layer:
  - consistency (no consistent A3 design found);
  - routability: reachable (U = 0), but only for unstructured systems;
  - middle capacity: node sharing needs partition-like structure, and structured systems have U ~ 1,700-2,150.
- **Structural reasons** (the proven ones carry their label):
  1. **proven:** the reach lemma.  h = 11 makes rank-8 nodes reach <= 6 targets, forcing extra middle levels (each
     costs ~0.5-1.5%).
  2. **proven, exhaustive:** 4-section parity tops are impossible.
  3. The odd number of P lines (55) blocks every balanced block partition (frames, D4, D5, A4-type, A3); in E8 the
     D4 partition gives R420 its zero-waste quads.
- **proven gap:** no rigorous all-word bound reaches break-even.
  - The union-coverage LP gives only R >= 440.
  - The class floors are model-based: A3 715 / 705.8; frame union 550 + 0.5 x (non-reciprocal mates).

## 3c. Session 3 (continuation, 2026-10-15 17:40-22:10) — rank-8 sections: top counting fine, node/middle wall, M11 triangle design

**Cover enumeration (proven, exhaustive up to Stab(t), `code/llp/lr8allcovers.py`).**
- Frames through t: P 11,515 in 24 Stab(t)-orbits; T 14,945 in 29 orbits.
- 4-covers of R(t) by rank-8 nodes F-perp: **65,170 per P line, 258,020 per T line**.  The greedy pool
  (`r8covers.pkl`) had ~1,640 / ~630 of them.
- 13 of the 24 P frame orbits occur in no 4-cover.  Lists per orbit representative: `lr8allcovers_P.pkl`, `_T.pkl`.

**Top layer (heuristic searches, exact evaluation).**
- Z11 pool CP-SAT relaxations (`lr8poolmip.py`, `lr8poolmip2.py`, `lr8poolmip3.py`) reach cost 0 quickly, because
  they ignore part identity.
- Exact equivariant parts layer plus annealing over covers (`lr8z11.py`; env `XOR=1` allows GF(2)-combination
  hosting, `FAITH=1` uses the faithful-style objective).
- **Faithful node cost** (`lr8nodecost.py`):
  - At node F-perp the registers arrive from the last middle stop (rank RHO), so their contents are supported in
    rank-<=RHO sets.
  - Node registers = k + (m - d).  Here m = min #such vectors spanning all delivered and in-chain parts, and
    d = dim span(delivered parts).  This equals max(k, m) when the delivered parts are independent; see "Register
    accounting with copies" below.
  - R = 440 + sum of extras.
  - **Correction:** my earlier "only rank-8 single parts cost a leftover" rule holds only for RHO = 7.
- Best tops:

  | design | RHO = 7 | RHO = 5 |
  |---|---|---|
  | MIP2 covers, FAITH layer (`lr8det_f0.json`) | R = 583 | R ~ 1,180-1,280 |
  | annealed (`lr8det_f21.json`) | R = 572 | — |

- Prices with extras as full pieces (`code/price/price_mid7.py`):

  | chain | price at X = 0 | break-even X |
  |---|---|---|
  | (cells, 3, 7) | +15.06% | ~160 |
  | (cells, 3, 5, 7) | +10.3% | ~110 |
  | (cells, 3, 5) | +13.5% | ~145 |
  | (no cell, 3, 7) | +17.6% | ~190 |

  So the top alone would be ~+1.4% to +2% under (3, 7), *if the middle had zero waste*.

**Middle: the wall (proven for the given tops, `code/llp/lr8midlb.py`).**
- **Mechanism:**
  - A register reaching the node with a rank-7 content c must stop at the rank-7 set M = span-closure(c).
  - At M the contents come from rank-<=5 stops, so M needs >= kappa5(W_M) >= 2 registers.
  - A rider for M can only come from another used node F' with F' inside pm(M).
- **Results:**
  - `lr8det_f0` (R = 583 top): 429 forced rank-7 closures hold a single register, and NONE has a possible rider.
    Middle waste >= 429, so R >= 1,012.
  - The `FAITH=2` variant of the same covers (R = 616): waste >= 385, so R >= 1,001.
  - `lr8det_f21` (R = 572 top): waste >= 561, so R >= 1,133.
  - Both are far beyond break-even.
- **Observed for f0 (heuristic):** delivered parts average 28.3 lines (rank 5/6/7/8 = 99/44/451/66).  kappa3 of the
  parts is 3-13, and the 594 rank-<=7 parts have 539 distinct closures.
- **Consequence:** cover-driven tops cannot work.  A viable rank-8 design must be *hub-aligned*: delivered parts
  must share rank-7 closures in groups of >= kappa5(W_M), and likewise at every lower level.  This is the same
  node-sharing requirement that blocks the frame-union line, now with a clean necessary condition.

**Rank-7 sections.**
- **proven, exhaustive (`code/llp/lr7refine.py`):** no P or T line has R(t) covered by 4 perp-closed rank-7 sets
  Q-perp (Q a rank-4 closed set through t).
- So rank-7 perp-section tops need >= 5 sections, hence R >= 660 even at zero waste: (no cell, 3) +0.39%,
  (cells, 3) -2.06% (`price_r7.py`).
- Span-closed rank-7 hyperplane subsets of rank-8 nodes do refine most 4-covers (P 3,642 / 3,642; T 12,376 /
  13,101 representative covers; `lr7refine2.py`).  Nondegeneracy of those subspaces is not checked.  They lower the
  node to rank 7 but leave the middle problem unchanged.

**More exhaustive facts (session 3).**
- **No disjoint 4-covers** (`lr8exactcov.py`): every 4-cover of R(t) by rank-3-frame perps overlaps.  The minimum
  total overlap is 33 lines for both P and T.  So unlike E8's exact frame triples, users of a node cannot all take
  the whole perp.
- **P covers contain at most 2 rank-7 nodes** (`lr8autoshare.py`).  A rank-7 node is one whose perp has rank 7, so
  all rank-7 parts there share the node as their closure.  T has 931 all-rank-7 representative covers.
- **Usable users** (`lr8usable.py`): which lines of a frame can use it in some 4-cover.
  - Fully usable:
    - P-A3: 6/6;
    - A2(B) + P(de): 4/4, perp 42;
    - A2(B) + T(abc): 4/4, perp 43, rank 7;
    - mixed A3 {A2(K), T(12k) : k in K}: 6/6, perp 47;
    - {P(ab), T(B1), T(B2), T(B3)}: 4/4, perp 36, rank 7.
  - Poor: L(abc), whose perp is A7, is usable only by its T line (1 of 4).
  - Covers whose four nodes all have >= 4 usable users: P 44,380 of 65,170; T 31,080 of 258,020
    (`lr8sharepool.py` -> `r8share.pkl`).
- **Flex covers** have no rank-8 node with an exclusive part of rank >= 7: P 4,060, T 64,120 per line
  (`lr8flexcov.py`, `lr8flexpool.py`).  Their designs still fail the middle (R ~ 990-1,089 with rank-7 nodes fed at
  rank 5).

**Register accounting with copies (corrects the node model).**
- At any frame, gates are invertible, so the final contents span exactly the arriving non-empty span (m dims).
- Delivered registers cover d = dim span(delivered contents); dead registers carry the rest.
- Empty registers can take copies for free.  So registers at a frame = k + (m - d).
- `lr8nodecost.py` uses this formula; it gives the same result as max(k, m) when the delivered parts are independent.
- **Identical parts + copies:** all users of a node take the same W_F.  One register is assembled from m_F pieces;
  the other delivered users get copies (empties 0 -> 8 -> 10 -> 11, a cheap chain).  Cost m_F - 1 per node.
- Prices with m_F = 2 (`code/price/price_copies.py`):

  | chain | N = 147 | N = 220 | N = 260 |
  |---|---|---|---|
  | (cells, 3, 5) | +14.4% | +5.2% | +0.8% |
  | (3, 5, 7) | — | +3.4% | — |

  Break-even is ~270 nodes, *provided the pieces themselves cost nothing*.  The lower levels repeat the same
  assembly problem: every distinct rank-5 piece needs kappa3 - 1 ~ 3 leftovers unless pieces are shared or aligned.
- Varying parts (users take different unions of a node's pieces, with d_F = m_F) remove the top-level leftover
  entirely.
- Parts need not partition R(t).  Only the target's F2 sum matters, so overlap lines can cancel.  This is not yet
  exploited.
- Identical-parts CP-SAT (`lr8identical.py`, Z11; `PARITY=1` uses the F2 version):
  - Feasible at once, but with 880 single-user nodes.
  - Maximising sharing: the 60-cover overlap/random pool needs >= 638 nodes (CP-SAT bound).
  - The shareable pool (150 per rep) was still at ~825 nodes after a few minutes.
  - Sharing needs a globally consistent symmetric structure, not pool search.

**Node-count LP (proven, `lr8covtypes.py`).**
- Node type = (frame lines, perp size, usable P users, usable T users).  P has 11 node-type cover classes, T 60.
- Every node of a type serves at most its usable users of each kind.  Merging types by key is a relaxation.
- Result: **any rank-8-section design needs >= 260 distinct nodes.**
- Consequence for identical parts + copies (R = 440 + sum of (m_F - 1)):
  - **Estimate:** R ~ 700 if every node needs m_F >= 2 pieces (average part ~30 lines).  That is break-even at best,
    even with a free lower middle.
  - **Rigorous (incidence count):** only R >= ~511.  This uses rank-5 subsets of <= 20 lines, verified for the six
    largest T node types (`lclosed.py`).
- Only varying-part designs with an aligned middle keep the +13.5% counting potential.

**T-triangle design: perfect top sharing for all T lines (proven by construction).**
- Files: `code/llp/lttri_design.py`, `lttri_check.py`, `lttri_design_z11.json`.
- **Triangle node:** three pairwise disjoint triples {A, B, C}.  The frame {T(A), T(B), T(C)} has rank 3 and perp
  37 = A2(A) + A2(B) + A2(C) + P(E) + 27 transversal T lines, where E is the leftover pair.  All three T lines can
  use the node.
- **Cover condition:** four nodes (A, B_i, C_i, E_i) cover R(T(A)) iff every pair of the complement D lies inside a
  block of some node and across B_i x C_i of some node.  There are 840 such 4-sets per T line.
- **Construction:** a Z11-symmetric CP-SAT finds, in 5 s, 220 nodes with every triple in exactly 4 nodes, each
  triple's nodes forming a valid cover.
- **Geometric check:** all 165 T lines are covered, each with overlap exactly 33, the proven minimum.
- **Closed form (checked):** this is the Steiner system S(4,5,11).  For each pair E, the 12 triples T with E u T a
  block form the affine plane AG(2,3) on the other 9 points.  The 4 nodes over E are its 4 parallel classes:
  55 x 4 = 220 nodes, invariant under M11 (order 7,920).  The best P cover type uses the same derived planes, so
  M11 is the natural symmetry for further Lorentzian top designs.
- So all 660 T uses sit on 220 nodes used by all their users.  Pool searches needed ~780 or more.
- **Forced contents at a node:** T(A) receives f_A = A2(B) + A2(C) + P(E) there, a rank-5 set.
  - Own A2(A): received once (odd) over its 4 nodes.
  - Transversal-type T lines (84 per T line): received an odd number of times.
  - Because P(E) is needed by all three users, an in-chain user can be hosted only by an identical delivered part.
- **RETRACTED (session 3, same day):** the claim ">= 1 extra register per triangle node, R >= 660" was wrong.  It
  used f_A + f_B + f_C = A2(A) + A2(B) + A2(C) + P(E); the correct sum is P(E).
  - **Still true:**
    - A user takes a full fibre at every node.  Each node has >= 1 single-crossing pair, since at most 8 pairs cross more than
      once; in the M11 design, 24 pairs cross once and 4 cross three times.  So every part at a triangle node has rank 8.
    - Pairwise sums P_A + P_B always have rank <= 7.
    - An in-chain user can be hosted only by an IDENTICAL delivered part.
  - **Corrected node condition:**
    - With three delivered users, the node is zero-waste iff P_A + P_B + P_C (= P(E) + own-A2 terms + XOR of the
      transversal sets) has rank <= 7, e.g. when the transversal sets XOR to 0.
    - A node with an in-chain user costs >= 1.  So the T-part waste is >= ~83, from 165 in-chain uses with two per
      node.
  - So the triangle top is NOT ruled out.  `lttri_cost.py` gives 380 with random assignments; 5 nodes were already
    zero-waste.
  - **Local test (`lttri_local2.py`):** zero waste needs the XOR transversal set inside the zero set of a nonzero
    additive alpha_a + beta_b + gamma_c.  The 6 forced-odd transversals of every node always fit one, so a node
    is never ruled out locally.
  - **Optimiser (`lttri_opt.py`, exact node model):** fast cooling took 385 to 363 in 30 s.  The floor from
    in-chain hosting is 83.
  - **Combined M11 top (`lm11design.py`, all covers verified):** T lines on triangles; each P(E) on one parallel
    class (three A2(B_i) + P(E) nodes and {P(E), T(B1), T(B2), T(B3)}, which shares the triangle hub M_n).
    - Exact layer node waste is 297 (R = 737), with middle bound >= 110 (55 riders).
    - Total >= 407, well over the margin.  The P side has no sharing.
  - **Exact CP-SAT (`lttri_cpsat2.py` / `lttri_cpsat3.py`):**
    - The lower-cost model reaches the in-chain floor 83.
    - Faithful costs (waste = m - d) reach 121, against that model's floor of 110.
    - With the P lines' in-chain floor of 55 (single-user P nodes), the M11 family's top waste is >= 138
      optimistically and ~176 realistically, before any middle cost.
    - **Verdict (heuristic; the floors are rigorous):** break-even at best, unless the synergy below works.
    - **Synergy to test:** P(E)'s node {P(E), T(B1), T(B2), T(B3)} has perp equal to the triangle hub M_n.  So
      P(E) can read in-chain there from the triangle's pairwise-sum registers.  Choosing P(E)'s in-chain part as
      one of those combinations removes the P floor of 55, leaving the top at ~83-121.  The decisive layer is
      then the hub middle.
  - **Rank-5 feeding test (`lttri_rho5local2.py`, `lttri_hublocal.py`):**
    - The only possible rank-<=5 basis of a node span is {P_p + P_q, P_p + P_r, P_A + P_B + P_C}.
    - Exhaustively, over own-A2 patterns, pivots and the 14,361 maximal rank-5 subsets, it is impossible at
      node 0.  All 220 nodes are equivalent under M11, through a regular V4 action on the 4 parallel classes.
    - The hub condition alone (two pairwise sums of rank <= 5) is satisfiable.  So the obstruction is the triple
      sum, which contains P(E).
    - With rank-5 pieces below the node, every triangle node costs >= 1, so T-part >= 220 and R >= 660.
    - Exceptions: riders at the triple-sum stops (none found), or rank-6 stops (untested).
    - Re-checked at nodes 1, 57, 130 and 219: all infeasible.
    - **Rank-6 stops do not help.**  A register alone at its rank-6 stop must still be assembled there from
      rank-<=5 inputs, so it needs rank <= 5 itself.  Only riders can relax this.
    - **Riders at the hubs M_n:** they come from P(E)'s node {P(E), T(B1), T(B2), T(B3)}.  Each P line picks one
      class, so at most 55 of the 220 hubs get one.  None were found for the triple-sum stops.
    - Even a rider at the hub does not rescue a node (`lttri_riderlocal.py`, node 0 infeasible), because the
      triple sum must still have rank <= 5.  So T-part waste is >= 220 (R >= 660) with rank-5 feeding.
    - **Final for this family: no gain.**  The one remaining loophole would be riders at the triple-sum stops,
      and none are known.
  - **Middle of a triangle node:**
    - Its good vectors, the pairwise sums, all lie in the hub M_n = A2(A) + A2(B) + A2(C) + 27 transversals
      (36 lines, rank 7).
    - Rank-5 subsets of M_n hold <= 17 lines, so kappa5(M_n) >= 3.  pm(M_n) holds no other triangle.
    - So the two pairwise-sum registers stopping at M_n need their XOR span to have a rank-5 basis.  That requires
      transversal choices aligned to single slices (e.g. P_A + P_B = A2(A) + A2(B) + one C-slice, rank 5).  This
      can be encoded as a further constraint in `lttri_opt.py`.
- **P lines:** their best fully P-shareable cover type is A3({a, b, c, d}) + 2 lone A2(B) + P(ab) + a mixed A3.  Its
  lone A2 + P nodes are not used by their A2 members.  A role-aware P design is next.

**Rank capacity lemma (proven for T; P being checked, `lrankcap.py`).**
- A set of lines of rank <= 6 contains at most 20 of the 84 lines T(x, y, z) of R(T(abc)).  At rank <= 5 the
  maximum is 12, at rank <= 7 it is 30.
- Proof: projection onto the x- and f-coordinates, plus edge-vector ranks of graphs.
- So every T line has a part of rank >= 7.  That part is one of:
  - a rank-7 delivered part at a rank-8 node, whose closure must be shared;
  - a full-rank part, which needs a sum structure;
  - the line's in-chain part, hosted by co-users' delivered parts.
- The third case escapes, so this gives no waste bound on its own.

**Natural hub family (not yet used).**
- For a coordinate set S, L(S) = {P(ij), T(ijk) inside S} has rank |S| and C(|S|,2) + C(|S|,3) lines:
  - 4 lines at |S| = 3;
  - 10 at 4;
  - 20 at 5;
  - 35 at 6;
  - 56 at 7.
- L(S) is positive definite for |S| <= 8.
- P-type A3 nodes (A3 on 4 coordinates) have F-perp = L(complement), which is rank 7 with 56 lines and 6 users.
  Every rank-7 part on such a node has the same closure, so these nodes share automatically.
- Mixed A3 frames {T(abx), P(xy) : x,y in {c,d,e}} have 47-line perps.
- Rank-3 hubs inside L(5): kappa3(L(5)) ~ 4-5 using mixed A3s (the T triples through a K2 + K3 edge set).
- A hub-aligned design would mirror E8's quad partition on this coordinate hierarchy.

**Assessment (end of session 3).**
- **Not proven worse, not shown better.**  The rank-8 class keeps a counting potential of +13.5% (R = 440, every
  layer zero-waste).
- **Proven:**
  - exhaustive cover lists;
  - no 3-covers, and no disjoint 4-covers;
  - no rank-7 perp-section 4-covers;
  - >= 260 nodes in any design;
  - the T rank-capacity lemma;
  - the per-design middle bounds R >= 1,001-1,133.
- **Heuristic:** every concrete design family evaluated failed by >= ~200 registers, against a margin of ~145-190.
  That covers greedy, flex, shareable and identical-parts designs.
- **The M11 triangle design**, re-examined after the retraction:
  - node waste 114-121 under RHO = 7;
  - with rank-5 feeding, every node costs >= 1 because of the triple-sum obstruction, so R >= 660 (local
    exhaustive test, all nodes M11-equivalent).
- **Observed trade-off:**
  - A sharing-maximal design (`lr8tshare.py`, 528 nodes) has node waste 462, so R ~ 902.
  - The cover-driven f0 has node waste 143 but 429 isolated rank-7 closures.
  - Sharing forces full-rank parts; not sharing isolates closures.
- **The wall is hub alignment.**  At every frame the arriving span must equal the needed span, with copies free.  It
  first bites at the rank-7 stops: closure sharing of rank-7 parts, kappa5.
- **New structure:** the M11 / S(4,5,11) triangle design gives every T line a perfectly shared 4-cover.  Any further
  attempt should use M11 symmetry.  Next candidates: node types with 4 usable T users, (6,42,0,4) and (5,37,1,4).

**Session-3 reproduction commands** (run in `code/llp/`; times on 4 cores).
- `python3 lr8allcovers.py P` / `T`: exhaustive rank-8 4-covers per Stab(t) orbit representative (3 / 16 min).
- `python3 lr7refine.py P|T`: no perp-closed rank-7 4-covers (seconds).
- `python3 lr8exactcov.py`: no disjoint 4-covers (1 min).
- `python3 lr8usable.py`; `python3 lr8covtypes.py`: usable users, cover-type census, LP >= 259.7 nodes (2-5 min).
- `python3 lttri_design.py 600 z11`; `python3 lttri_check.py lttri_design_z11.json`: the M11 triangle design (5 s).
- `python3 lttri_cost.py lttri_design_z11.json 7 1`: triangle node cost.
- Exact layer and costs for a Z11 design:
  - `FAITH=1 python3 lr8mkdet.py sel.json det.json`;
  - then `python3 lr8nodecost.py det.json 7 [5]` and `python3 lr8midlb.py det.json`.
  - Pools are chosen by env `POOL`: `r8covers.pkl`, `r8flex.pkl` (`lr8flexpool.py`), `r8share.pkl`
    (`lr8sharepool.py`).
- `python3 lrankcap.py 6` (env `KINDS`): exhaustive rank-capacity check (long).

**Source side of the R = 440 count (`lsrccell.py` .. `lsrccell4.py`).**
- **proven:** R420-style cells (orthogonal pair, 3 registers each) at 660 registers put every line in exactly 2
  cells.  Its 4 first hubs must then form a 4-cover of R(u) splitting into two pairs through distinct orthogonal
  cell partners.
  - No such cover exists (P 0 / 3,642, T 0 / 13,101 representative covers).
  - The argument extends to hubs of any rank.
- Without target reads at rank <= 2, the best coverage found leaves 24 (P) and 16 (T) lines uncovered (top-60
  heuristic).  Targets can read only ~2 lines each at rank <= 2.  The exact computation (`lsrccell3.py`) is
  pending.
- General cells: the budget forces 220 sum registers plus 440 single ones.  The weak per-line conditions are
  satisfiable, so the general source side is a design problem mirroring the top.

**Punctured / sub-systems (session 3).**
- P111-tuned uses the R420 skeleton, punctured (`code/e8r420/align.py`).
- **T_11 (the 165 T lines, h = 11):**
  - It has a natural point-total decoder.
  - On it the M11 triangle design would avoid the P(E) obstruction.
  - It is **verifiably uncompetitive by price** (`price/price_t11.py`).  At R = 2v = 330, realistic shapes give
    -33% to -37%.  Even with no middle stops, R = 330 gives -11.6%, and it would need R < ~1.2v.

**Overarching insight (session 3).**
- All open classes (rank-8 sections, frame union, A3/TT*) hit the same wall: **hub alignment**.
- **Zero waste** needs, at every frame of the network, the span of arriving contents to equal the span of needed
  outgoing contents.  Copies are free, so identical needs cost nothing.
- E8's R420 achieves this through its D4-quad partition.  I_{11,1} has no comparable partition: the 55 P lines are
  odd, there are no disjoint 4-covers, and shared nodes force full-rank parts.
- The M11 geometry (S(4,5,11), derived AG(2,3) planes) is the only large symmetric structure found that organises
  the top.  The next session should:
  - (i) **DONE (`code/e8r420/align.py`):** E8 R420's alignment pattern.
    - Frames and registers per frame: lines (3 registers) -> cells (3, rank 2) -> D4 quads and blocks (~7,
      rank 4) -> D6 (3, rank 6) -> t-perp (3 needers, rank 7).
    - At every frame #registers = span dim, i.e. zero waste.
    - That costs 4.5 registers per line, while I_{11,1} must reach <= ~3.7 per line to beat P111.  So I_{11,1}
      needs a template MORE efficient than R420's own; the rank-8 ideal is 3 per line.
    - R420 delivers 360 registers (3 needers per target).  Another 180, 1.5 per target, are never read by a
      target.
    - I_{11,1} can afford only ~0.7-0.9 such registers per target, about half of R420's relative overhead.
  - (ii) look for the M11 analogue, or prove that no I_{11,1} frame hierarchy admits one, e.g. by a
    dimension-count LP over frame orbits with the per-frame condition arriving span = needed span.

## 4. Next goals (priority order)

Updated in session 3 (rank-8 item 0); the rest dates from session 2.  Every class examined is at or below
break-even once all layers are counted.  The items below are the remaining loopholes, in order of plausibility.

0. **Rank-8 frame sections: the NODE-RANK WALL** (session 3, see 3c).
   - **Established:**
     - The top counting reaches R = 572-583 (RHO = 7).
     - Every cover-driven top is dead in the middle: proven per design, R >= 1,001-1,133.
     - Any design needs >= 260 nodes (LP).
     - (A triangle-top impossibility claimed here was RETRACTED; see 3c.)
   - **Key mechanism (proven in the triangle case):** a node whose users' parts span the whole node rank needs an
     extra register, unless the part span has a basis of lower-rank vectors.  Coverage forces such full-rank parts.
   - **Next, in order:**
     - (a) **Checked:** the triangle argument does not generalise through exclusive parts (`lr8forced.py`).
       Exclusives are rarely full-rank, so node-level zero waste (RHO = 7) is locally possible.  The binding
       constraint is the rank-7 stop.  Every rank-7 part's closure M needs >= kappa5(W_M) >= 2 registers: shared
       by aligned co-users of the same node, or by riders from nodes F' inside pm(M).
       - Aim for an LP or exhaustive bound on the minimum number of isolated closures over all designs.
       - Alternatively, a design search with an exact closure-sharing objective.  `lr8z11.py MID=1` is a first
         version; runs on the share and flex pools were launched.
     - (b) Build the top from aligned node types (P-A3 L(7-set) nodes, A2 + X nodes), then the coordinate hub
       hierarchy L(3) < L(5) < L(7).
     - (c) The P-line analogue of the triangle design (role-aware: A2 + P nodes used by their members).
     - (c') **Mixed triangle covers.**
       - The triple-sum obstruction comes from P(E) being forced into all three users' parts.  In the pure M11
         design the within-block pairs are covered exactly once (4 x 7 = 28), which forces this.
       - Covers mixing 2-3 triangle nodes with other node types, e.g. A2(B) + T nodes, can cover some P lines of D
         twice and release the parity.
       - Test with `lttri_rho5local2.py` adapted to mixed nodes.
       - **Probe done (`code/llp/lttri_rho5_pe.py`):** making P(E) OPTIONAL per user (a Boolean per user, all
         other forced parts kept) is still infeasible at node 0: 14361 maximal rank-5 subsets, no feasible
         (delta, pivot) sub-problem.  So releasing P(E) alone does not help; the obstruction already comes from the
         forced transversal / A2 fibres.  A mixed cover must also change which A2/transversal lines each triangle
         user carries, i.e. it must break the triangle-node part structure itself, not just the parity of P(E).
         Scope: one node (all nodes are M11-equivalent in the pure design; in a mixed design they need not be).
       - **Relaxation probes (`code/llp/lttri_rho5_relax.py`, node 0):** freeing P(E) and the A2(other) lines
         (transversals still forced) is INFEASIBLE; freeing P(E) and the multiplicity-1 transversals (A2 still
         forced) is FEASIBLE for 7 of the 8 own-A2 patterns.  So the obstruction lives entirely in the
         coverage-forced transversal memberships.  A mixed design must cover some of those transversals at other
         (non-triangle) nodes; `code/llp/lttri_rho5_minrel.py` computes the minimum number to release.
     - (d) **Varying-part piece design (the only zero-waste shape left).**
       - At each node, the users' parts are XOR combinations of a few rank-5 pieces.  The DISTINCT parts must span
         exactly the arriving pieces (m = d).  Equal parts are served by copies.
       - Nested parts, e.g. user 1 takes a + b and user 2 takes a, make the rank-7 or rank-5 stop zero-waste,
         because every arriving dimension is needed by some user.
       - Each user's 4 parts must still XOR to R(t).
       - Formulate as a CP-SAT over a fixed candidate piece family per node orbit (rank-5 closed subsets of the
         perp), under Z11 or a subgroup of M11.  Start from the low-waste f0 covers, not from shared nodes.
   - Older notes below are kept for context.
   (Original item:) **Rank-8 frame sections** (the only class whose counting reaches the union-LP floor R = 440:
   +13.5% there, break-even 662 with a reach-compliant middle).  See 3b.
   - (a) Top design: 4 frames per line covering R(t), and each in-chain section has a delivered co-user.
     `code/llp/lr8design.py` (strict, Z11) and `lr8design2.py` (relaxed).
   - (b) Parts: the in-chain span condition plus independent delivered parts (`lr8parts.py`).
   - (c) Node check: delivered parts must be generated by k inputs supported on rank-5 sets (`lr8midcheck.py`).
   - (d) Exact GF(2) middle: cells -> rank-3 -> rank-5 -> section nodes.
   - Each failure can be priced with `price/price_r8sec.py`.  Every unspanned in-chain part costs ~0.09% (110 of them
     leave +3.2%).
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
- **Session 2 scripts:**
  - `llp/`:
    - LP / top analysis: lpsolve, lparity*, la3*, lexcl*, lkappa, lkex*, lpar4_*, lpar_inchain, lunion_min,
      lexcl_union, lr3cover_exact;
    - A3 designs: e11design*, e11eval, e11agglp*, e11lpdesign;
    - frame union routability: lroute_sa*, lroute_z11, lroute_a3, lcovers (covers3.pkl), lmatch*, lframe1,
      lmidcap, lfull_eval.sh;
    - rank-8 sections: lr8design*, lr8parts, lr8midcheck, lr8slots.
  - `price/`: price_a3exact*, price_a3reach, price_a3mix, price_frame*, price_general, price_4sec*, price_r8sec,
    price_ceiling, price_stops, budget.
  - Systems: `llp/lroute_best_11.json` (weak U = 0); `llp/a3part_11.json` (27-block A3 packing).
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
