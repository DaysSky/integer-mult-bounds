# Lorentzian I_{11,1} bit supplier: handoff (sessions of 2026-10-15)

Prepared by DaysSky with assistance from Claude.  Scratch research, not reviewed; claims are labelled
**proven** (exact/exhaustive computation, scope stated), **heuristic** (search result, no optimality claim) or
**estimate**.

## 0. The question

Can a bit word on the Lorentzian line system I_{11,1} (v = 220 lines, h = 11) beat the current bit supplier
P111-tuned (c = 0.001733427039589844, E8-based)?  A kappa gain is not required: a bit-supplier gain or an
architectural potential improvement suffices.

**Status: open.**
- Session 6g: **proven** that root-like Lorentzian systems have at most C(h+1,3) + 1 lines (h >= 11; 165 at h = 10),
  so the I_{n,1} family is optimal up to one line.  Every model break-even line count lies above this ceiling (see
  "Session 6g" in 3f).
- **Bottom line after session 6g** (what a Lorentzian frontier would still need):
  1. **Line system.**
     - Root-like: capped (theorem).
     - Lines compatible with all of I_{n,1}: enumerated exactly; each costs one decoder unit, so x never drops.
     - Mixed-norm, mixed-sign, h = 9 and twin searches: nothing better than I_{n,1} or E8.
  2. **Decoder.**
     - I_{11,1}'s B0 is the unique rank-11 decoder (110).
     - Cyclic structured families cheaper than 110 do not exist in every range searched.
     - A decoder costing >= 120 already puts the h = 11 tie density at or below the 426 floor.
  3. **Middle.**
     - Even a perfectly aligned R420 analogue (3.5 registers per line) misses at x = 0.5, where the tie needs
       2.66 (abs) / 3.34 (rel).
     - Aligned partitions need >= 16 punctures (proven).
     - Non-aligned designs need about 2x E8's cells per line (relaxation): R ~ 1,000+.
  - So every route needs an architecture more efficient than the best known E8 middle on a misaligned system with
    about twice the load.  Not excluded by an all-word bound (the all-word floor is 426 against a break-even of
    about 630-757), but no mechanism for it is known.
- **Session 6h additions** (details in 3f, "Alignment of I_{13,1} partitions" and the h = 9 block):
  - *With the entrance lever* (model): Lorentzian systems allow 3.6-4.4v at 25-50% hubs, still 0.3-0.6v less
    than E8 at the same lever use.
  - *I_{13,1} R420 analogue:*
    - partitions are misaligned (PG(2,3): per-line cover >= 6, E8 3) and rigid;
    - symmetric classes do no better (greedy cover >= 6.18);
    - the demand load is 3.2x E8's per line.
    - The +9-22% rows assumed R = 3.5v, which this does not support.
  - *h = 9:* systems that use the timelike direction and contain a frame have <= 111 lines (exact).
    - Frame-free systems have <= 119.
    - The 119-point O^-(8,2) quadric is proven non-realisable.
    - Twin configurations are still open; the lever model needs >= 117 lines.
  - *Decoder:* ten units are worth about 0.7v of middle; pseudo-punctures and sparse rows do not pay at about
    12.5 helpers per unit.
- **Session 6i additions** (details in 3g):
  - *Price identity:* whenever every residual is hosted, the deficit is T (8v - 9 cst), independent of R.
    Helpers cost only through D, the piece log-spread.
  - *z-groups (new mechanism, format-validated):*
    - Targets perp a non-null z take span(z) as their first phase-B frame and cancel group-helper dirt there.
      Group helpers start at span(z), width h - 1, with no in-chain or fan-in limits inside the group.
    - A toy I_{11,1} word with 26,070 such helpers passes gcheck_z, which is gcheck plus the E1 relaxation.
  - *Branch floor is frame-0:* in any word, the ~2v extra branches per source must be frame-0 helpers (426 for
    I_{11,1}, 706 for I_{13,1}).
  - *Best case with both facts:* I_{11,1} R <= 743-896, I_{13,1} R <= 1,205-1,449.  The non-branch middle may
    then use 1.4-2.1v helpers: R420-sized, at 2-3x R420's per-line load.  So there is still no route without a
    middle more efficient per incidence than E8's best.
  - *Decoders:* rank-12 codes containing C_11 cannot sparsify rows (exact linear algebra).  Z11-invariant
    rank-12 decoders with every row <= 116: none found in 600 s (the B0-weight control solves in 7 s).
  - *h = 9:* the 119-point quadric's zero pattern fails to realise in R^{8,1} (numerical, E8 control passes).
  - *Later in 6i (details at the end of 3g):*
    - First priced Lorentzian word: word_blkA4 (R = 3,656) at c = 0.000493, -71.6% (bank-overflow pricer whose
      P111 and R420 controls are exact).
    - E8 R420's partition is fully aligned (0 odd (E-set, frame) pairs).  I_{11,1} partitions carry about 7,700,
      and I_{13,1}'s PG(2,3) partition 23,348.  E-set halves can be shared (star-D4 blocks 3-fold, Pasch pairs
      2-fold), but sharing does not buy alignment.
    - Rank-7 block groups make delivery cheap (model -2% to +14% at 450 movers + 660 width-4 helpers), but the
      half assembly needs about 2.5x E8's registers per line.
    - 10-frame tops (per-line cell cover 11-12) and full-rectangle tops (no exact F2 cover) are dead.
    - A target cannot relay for another target (its own line is always in its content).
    - Lever calibration on E8: group helpers pay only when they remove frame-0 registers (+11.8% if 240 R420
      needer-carriers could be dropped, -17.8% if added).
  - *Bottom line after 6i.*
    - The best Lorentzian ideal price (I_{11,1}, one stop, R = 0) is about 15% below E8's.  So a Lorentzian word
      must beat R420's relative efficiency (eta 0.404) by about 10% (eta >= 0.444).
    - Even a perfectly aligned R420 analogue with z-groups only ties (-3.3% to +0.3%).  Real I_{11,1}/I_{13,1}
      structures are far from aligned, and their assembly costs about 2.5x E8's registers per line.
    - A Lorentzian frontier therefore needs an architecture strictly more efficient than R420, which would first
      of all be a large E8 improvement.  Every Lorentzian-specific lever examined (z-groups, rank-7 block groups,
      sharing partitions, rectangle tops, cheaper decoders) is closed or falls short.
- **Session 7 corrections** (details in 3h):
  - *Totals-feeder lemma (proven):* in any word >= v distinct registers are contaminated (frame holding their line
    plus another line) before the scatter.  Frame-0 middles absorb this for free; a pure z-group word must spend
    about v extra frame-0 registers on it.  With 3 groups that is 3v frame-0 registers for I_{11,1}, leaving
    <= 1.0v group helpers at the frontier: no more middle room than a frame-0 word.  The 6i "z-groups bring an
    R420-quality middle up to a tie" is withdrawn.
  - *E8 has no 3-hyperplane cover (exhaustive):* z-grouped E8 needs 4 groups and >= 345 frame-0 entries; an
    R420-quality middle then prices at -12% even with free totals.  The E8 stepping stone (6i item B) is closed in
    pure form.
  - *Exact budget:* I_{11,1} has 1.95 per line for helpers and stops at the frontier, P111 1.80, for half the
    demand.  So the middle must be about 2x more efficient per incidence than P111's, at 1.4x the cost per helper.
- Not proven worse: no all-word bound reaches break-even.
- Not shown better: no competitive word exists.
- A complete, independently verified Lorentzian frame-cell word exists (R = 11,494), but it is about 20x the cell
  floor.  The best verified word is now R = 3,656 (`code/lbuild/word_blkA4.json.gz`, session 6c: `build_blk_pairs.py` with
  per-frame pairings; frames 2 and 50 use pairing 2, all others 1; gcheck PASS).  Previous: 3,681 (`word_blkA3`).
- Session 6b (end of 3f): exact checks show that no section-type top (full plane sections, A3-perps, 2-cover
  "varying" parts, mixed rank-8/9 covers) beats the A3/TT* floor R ~ 715; only general "gossip" networks remain
  unexcluded, and they would need a middle more efficient than E8's R420 (<= 0.94-1.38 v above the sink floor
  426, against R420's 1.58 v).
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
      sum, which contains P(E).  **Refined later:** it persists with P(E) optional and with the A2(other) lines
      free, and disappears when the multiplicity-1 transversals are free; it lives in those coverage-forced
      transversals (see next step (c')).
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
    - **Loophole closed (later in session 3, `code/llp/lttri_tau_riders_all.py`, all 220 nodes):** every good basis
      contains tau = p_A + p_B + p_C (rank >= 5, so assembled at a stop).  A rider at a stop M containing supp(tau)
      comes from a frame F' inside pm(M), which lies inside pm(supp tau); co-user registers are excluded because P(E) is in
      tau but not in the hub.  At every node exactly 3 lines l qualify (transversal T lines; M_l has 16 lines, rank 7,
      kappa5 = 2), and pm(M_l) = {T(A), T(B), T(C), T(l)}.  So the only rider frames are the 9 frames {two of the
      node's T lines + T(l)}, and none is a design frame.  A target taking one must leave >= 3 of its 4 triangle
      nodes (see (c') below).  So every node pays >= 1 extra register at ANY RHO in the pure design and in every
      modification where targets leave <= 2 triangle nodes: R >= 660.
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
  heuristic).  Targets can read only ~2 lines each at rank <= 2.  The exact computation (`lsrccell3.py`) did NOT
  finish: it was stopped at its ~50-minute limit with no output (not even the P case).  So the 24/16 figures remain
  heuristic; an exact version needs a pruned or LP-bounded pair search.
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

## 3d. Session 4 (2026-10-15 22:10 - 2026-10-16) — correction, I_{13,1}, and verified words down to R = 4,239

**CORRECTION (proven, exact Gram determinants; found by `lw.nondegenerate` while building).**
- For pairwise disjoint triples A, B, C (9 points), T(A)+T(B)+T(C) is the null vector of the 9-point coordinate
  flat, so every M11 "triangle frame" span{T(A),T(B),T(C)} and its section are DEGENERATE.  All 220 triangle frames
  and sections of `lttri_design_z11.json` are degenerate; the combined M11 top (`lr8det_m11_*`, `r8m11_*`,
  `r8tshare3`) uses 660/660 degenerate T sections.  gcheck rejects degenerate frames.
- So every section-3c result about the triangle design (perfect T sharing, rank-5 obstruction, riders, mixed covers,
  min-release, leave-1/2/3, tau-rider closure) concerns frames NO WORD CAN USE.  The geometry is correct but
  irrelevant to realisable words.
- Legal designs (all sections nondegenerate): `lr8det_f0/f1/m1/mip2opt.json` (pool `r8covers.pkl`, 4,609 of ~104.6k
  T covers there contain a degenerate frame, P all legal), `lr8z11_1/_32_det.json`, `lr8det_flex0.json`.
- Coordinate flats L(S) are closed and legal for |S| <= 8 and |S| = 10, degenerate at |S| = 9 (L(S9) is a degenerate
  copy of E8: 120 lines with a null radical).  Star flats K_a(S) = {P(xy), T(axy) : x,y in S} are legal for |S| <= 9
  and satisfy K_a(S)-perp = K_a(([11]-a)-S); K_a(S8) = {P(bc),T(abc)}-perp.

**I_{13,1} (proven within the stated scopes; `code/i13/`).**
- The A3 parity identity holds in I_{13,1} too.
- T type-(a) 3-section frame tops need R >= 1,352: each exclusive part (rank 8) has a degenerate rank-8 closure, so it
  is assembled at the section's private rank-9 flat by >= 2 registers that leave only through that node; 858 distinct
  T nodes give >= 1,716 registers.
- No 3- or 4-section parity cover of a T target, and no 4-section parity cover of a P target (exhaustive, rank-3 frame
  sections).
- Open there: multi-T-node (star / A3-type) designs, defect-1 tops with rank-11 sections, >= 5-section parity.

**Verified words on legal tops (all gcheck PASS; scripts in `code/lbuild/`; nothing priced, all far above the hosting
wall R ~ 7,920 only for the first rows).**

| word | top / middle | R |
|---|---|---|
| `word_f0_v1` | lr8det_f0 rank-8 frame top, direct line carriers (`build_m11.py`) | 19,251 |
| `word_f0_v2` | same, shared atom pieces (`build_v2.py`) | 11,572 |
| `word_a3h_v1` | A3 parity top (Z11 selection), hierarchical flat pieces (`build_a3h.py`) | 11,130 |
| `word_pack_p` | 27 packed A3 blocks + 58 leftovers, pure opposite sources (`build_a3p.py`) | 8,026 |
| `word_pack_b3` | + line values broadcast along exact Dilworth chain covers (`build_a3b.py`) | 7,055 |
| `word_pack_t` | + telescoped block reads 0 -> B-perp -> Q1-perp -> t-perp (`build_a3t.py`) | 6,836 |
| `word_pack_g2` | + general residual pieces (`genpieces.py`, MINSIZE=2) (`build_a3g.py`) | 5,956 |
| `word_pack_paar` | Paar cancellation-free CSE pieces (`paarpieces.py`) | 5,517 |
| `word_r2_alla3` | + lazy copies with leftover reuse, random-weight packing seed 2, B-perp split for every A3-type target | 5,075 |
| `word_r2L` | + leftovers reselected by content of distinct demands (`a3_left2.py`) | **4,239** |

- Reproduce the best: `PIECES=paar HOP=0 MP=0 python3 build_a3g.py a3_choice_r2L.pkl OUT.json.gz` (~2 s), then
  `python3 tword/gcheck.py OUT.json.gz`.

**Accounting (exact for these builders).**  R = (#registers read by targets - 220) + junk, where junk counts the
registers never read.  A node that turns s independent inputs into copies of ONE content leaves s - 1 junk, so with
single-content nodes R tracks the XOR-gate count of the piece circuit (pieces + terms of the top demands).  Observed:
R ~ 0.46 x (total content of distinct top demands).  First-hop receptions do not help (a one-child hop just swaps a copy
for an assembler); nested child chains would save only 101 of 3,902 child uses.
- **heuristic, A3 content floor:** with complete blocks the distinct-demand content is about 45/6 + 29/3 + 29/3 + 14/2
  ~ 34 lines per target (~7,500 total, against 9,198 now), so this middle family bottoms out near R ~ 3,500.  Reaching
  the break-even (~700) needs multi-output (butterfly) nodes whose distinct outputs span exactly their inputs, i.e.
  the hub alignment of section 3c, not better piece selection.
- **Multi-output nodes (exact accounting, `momplan.py`).**  A node with arrivals A_X and distinct outputs O_X costs
  junk |A_X| - rank(O_X); it is junk-free iff span(O_X) has a basis of lower-rank vectors (closures properly inside
  X) and every arrival is used.  If all outputs of a node share a full-closure essential part E (identical needs, or
  E + compensable differences), junk >= 1 there, because E itself needs >= 2 lower-rank arrivals.  In the A3 top every
  triangle and pair node is of this kind (the essential parts sigma_d + T(abc) and pi_ab + pi_cd cannot be compensated
  by the users' other reads), so:
  - **heuristic, A3 template ideal (perfect lower middle):** per complete block B-perp 2-3 in-chain registers,
    triangle nodes 2-3 each, pair nodes 3 each, i.e. ~21 helpers + 6 opposite sources per 6 targets = 4.5 registers
    per line, R ~ 770: below break-even even ideally (this corrects the 25/6 idealisation of section 3b).
  - A top-down multi-output planner on the r2L top finds junk 5,982 on 5,966 nodes (one per node): the A3 contents
    have no shared multi-output structure; only 22 pairs of Paar pieces could share a node (frames of their parents
    disagree), and joint per-frame assembly saves 6 copies.
  - Consequence: a gain needs a top whose node users take VARYING parts (nested parts give junk-free 2-user nodes:
    S = A u B with A, B lower-rank, user 1 takes S, user 2 takes A and covers B elsewhere) AND lower nodes shared by
    many parents (R420's D4 quads lie in 6 D6 sections).  Neither the A3 nor the coordinate tops have this.
- Mixed PPTTTT blocks (hub h, pairs pq|rs, W = 6 other points) have B-perp = K_h(W) u T(pq|W) u T(rs|W) (42 lines);
  E_Q = P(h z) + star of the other point over W in family h + Y_z(W) + one T line (29); E_P contains the triangle
  lines of W (20).  A3s sharing the 5-set {h,p,q,r,s} share W-structures.

## 3e. Session 5 (2026-10-16) — builder down to R = 3,798; good-frame classification; stop pricing

**Verified words (all gcheck PASS; `code/lbuild/`, choice `a3_choice_lsB13.pkl` from `ls_tops.py` seed 13).**

| word | builder change | R |
|---|---|---|
| `word_lsB13` | local search over A3 tops (`ls_tops.py`, EVAL mode of `build_a3g.py`) | 4,183 |
| `word_lsB13q` | `QMERGE=1`: multi-output quad nodes on the top demands (`qmerge.py`) | 3,936 |
| `word_lsB13pq` | `PCHAIN=1`: pieces read-only along minimum chain covers of their parents' frames | 3,812 |
| `word_lsB13qa` | `QALL=1`: quad merges on every node (non-top users must strictly contain the quad frame) | **3,798** |

- Reproduce: `QALL=1 PCHAIN=1 QMERGE=1 PIECES=paar HOP=0 MP=0 python3 build_a3g.py a3_choice_lsB13.pkl OUT.json.gz`
  (~20 s), then `python3 ../tword/gcheck.py OUT.json.gz`.
- Roles at 3,798: copies 1,965, carriers 1,491, empties 321, keepers 10, totals 11.  The generic middle is an
  XOR-count circuit; PCHAIN saved only ~290 copies because parent frames are rarely nested.  **heuristic:** this family
  cannot get near break-even; the gap is ~5x.
- Accounting used throughout: reads are free and non-destructive, every register is one path of nested frames, and
  R counts the paths that are not line sources.  A register can be read at its own frame by every path passing that
  frame, then climb along one chain, then be continued by one parent.

**Good 4-frames (proven, exhaustive; `code/goodframe/`).**  Call an orthogonal 4-frame good for t if every line of
R(t) other than the 3 partners is orthogonal to an odd number of them (this is what makes R(t) = Phi-perp u E1 u E2 u
E3 u partners a partition, as in E8's skeleton).
- I_{11,1} has 1,926,540 orthogonal 4-frames; 20,790 are good, and goodness is all-or-nothing (good for all 4 members
  or for none).
- **PPTT (6,930):** P(pq), P(rs), T(hpq), T(hrs).  The span closure is the star D4 K_h({p,q,r,s}) (12 lines, three
  good frames = the three pairings).  The perp is the star D6 K_h(W), W = the other 6 points (30 lines, rank 6).
- **TTTT (13,860):** 4 of the 8 transversals of a perfect matching of a 6-set Y, one parity class.  The closure has 11
  lines (rank 4); the perp has 25 lines (rank 7).
- **Parity obstruction:** every good frame holds 0 or 2 P lines and there are 55 P lines, so no partition of all 220
  lines into good frames exists.  The minimum puncture is 4 lines (1 P + 3 T).  CP-SAT found such a partition: 27 PPTT
  + 27 TTTT frames (`goodpart.pkl`).  A partition into complete star-D4 blocks would need a K4-decomposition of K11 - e,
  which is impossible (vertex degree 10 is not divisible by 3).
- Z11-invariant partitions into (non-good) orthogonal 4-frames exist (`z11part.py`), so "no 4-frame partition" is
  not the obstruction; goodness is.
- For the found partitions the section E-sets are far from unions of partition cells (`cellunion.py`): a 29-line
  E-set typically has ~21 lines outside whole cells.  An R420-type cell-sum network needs an aligned partition, i.e.
  |E(H) n Phi'| even for every section H and frame Phi'.
- Hub geometry: star flats satisfy K_h(S5) _|_ K_h(S5') (D5 _|_ D5, |S5| = |S5'| = 5).  A D5 hub holding the d-cell of
  an owner gives that owner 12 E-lines (6 cells), so two D5 hubs give 24 = the smallest E-set size (E-sets have 24,
  29, 34 or 38 lines).

**Exact shape prices (`code/goodframe/price_ideal.py`, nine-stage pricer, v = 220, vs P111-tuned).**

| R | minimal chains | cell -> section | cell -> rank-5 hub -> section |
|---|---|---|---|
| 440 | +48.3% | +30.4% | +20.3% |
| 550 | +35.8% | +19.1% | +9.4% |
| 660 | +25.3% | +9.7% | +0.3% |
| 700 | +21.9% | +6.6% | -2.7% |
| 770 | +16.3% | +1.6% | -7.5% |

- One extra stop on every register costs about 9% at fixed R.  Break-even: ~790 without a hub level, ~662 with one.
- An R420-type cell word (3 registers per cell, R = 770) needs a hub level for reach, so it lands at about -7%
  (`price_cell.py`: -6.7% with quad rank 4).  The plain pricer at v = 216 (4 punctured lines) gives -8.9%, but it does
  not model P111's pseudo-target totals.
- **Consequence (heuristic):** a gain needs R <= ~660 with one hub level.  The 3-per-cell family cannot reach this.
  The candidate below 660 is a zero-waste cell network: 2 registers per cell, targets read their d-lines from cell
  registers before they climb (no keepers), and section users take varying parts and compensate in-chain at a hub on
  their chain.  In counting that is R ~ 440 (+20% in the hub shape).  Feasibility is open: aligned partition, a D5
  hub system covering every E-set with k = 2 hubs, invertible hub matrices, and compensation chains.

**Alignment is impossible with 4 punctures (proven; `compat.py`, `aligncp.py`).**
- Two disjoint good frames are compatible if every E-set of each meets the other in an even number of lines.  An
  aligned partition (every E-set a union of partition cells) is a partition into pairwise compatible frames.
- Each good frame is compatible with 2,149 (TTTT) or 3,229 (PPTT) of the 20,790.  All frames on point sets
  disjoint from a frame's support are compatible with it, and TTTT frames meeting in one point always are; otherwise
  compatibility is partial (`compat_anat.py`).
- No single frame leaves a line uncoverable (`kills.py`), and about half the compatible pairs leave <= 4
  (`kills2.py`).  Even so, CP-SAT proves that **no aligned partition with <= 4 punctured lines exists**.  Completeness:
  some P line is unpunctured, and S11 is transitive on (P line, good frame through it), so the frame (4;01|23) can be
  fixed; the remaining frames must lie in its compatible set.
- So E8's cell-sum quads (each hub input is the sum of a cell) cannot be copied exactly.  Unaligned E-sets need
  single-line inputs or corrections, and for the CP-SAT partition most E-lines are unpaired.

**Deeper hub shapes (`code/goodframe/price_deep.py`; targets 0 -> cell -> section -> t-perp).**  Break-even R is about
647 with one hub level (rank 5), 603 with two (3, 5), 600 with (3, 6), 590 with (4, 7) and 550 with three (3, 5, 7).
Reach forces a low first hub after the cells (each cell must branch to cover the ~43 sections whose E-sets contain
it).  A cell network then needs >= ~2.5-3 registers per cell, i.e. R ~ 605-770.  **heuristic:** this family sits
between break-even and about -15%.

**Structural facts (session 5, second half).**
- **What the targets must read (exact, from `tword/gcheck.py`).**
  - The checker only demands target final = y_t + x_t.  The scatter adds sum_{k in row(t)} r_k (r_k = retained
    register contents), and the phase-B reads, all inside t-perp, supply c_t = x_t + sum_{row(t)} r_k.
  - So a decoder is a pairing B = U W^T with B_tt = 1 and B_ts = 0 on non-orthogonal pairs; c_t is row t of B off
    the diagonal.  The D10 labels give B0 = J + G, i.e. c_t = R(t).
  - A sparser rank-11 pairing would shrink every target.  **Argued, not proven:** B0 is unique at window 11.  Every row
    of a rank-11 B lying in the affine span of B0's rows must be B0's row, as at E8 window 9 (format package C.6).
    A higher window costs ~16% per unit, so R(t) is effectively forced.
- **D5 subsystems (exhaustive over closures D4 + line, `code/goodframe/d5enum.py`).**  Exactly 3,234 D5s: the coordinate
  flats L(S5) and the stars K_h(S5), all with 10 P lines.  So there is no 11-block D5 partition, the analogue of E8's
  10-block D4 partition.
- **A3 blocks host at most 110 T lines (proven).**  An A3 holds 0 T (PPPPPP), 3 T (PPPTTT) or 4 T with 2 P (PPTTTT);
  there is no TTTTTT A3, since two T lines meeting in 2 points differ by a P line.  So 55 P lines carry at most 110
  of the 165 T lines.  The current best top (47 A3s, 23 complete) works around this with incomplete blocks.
- **Why E8's cells align and I_{11,1}'s cannot.**  A cell must be a set of lines with identical membership in all
  section E-sets.  For frame tops that means identical orthogonality to every partner pair.  E8's D4-pair partition
  has this; the CP-SAT result above shows no good-frame partition of I_{11,1} with <= 4 punctured lines has it.
- **Hub capacity (counting, heuristic bound).**  Hubs give sections their E-parts.  A hub with n input registers and n
  owners serves at most n * (part size) (line, section) incidences.  Reach caps n at about 15 (rank X + rank X-perp
  <= 11 with D5/D6 line counts).  The sections need sum |E(H)| ~ 9,700 incidences.  So one level of hubs needs ~1,300
  registers with single-line inputs, or ~650 with cell-sum inputs (which needs alignment).  E8: 2,880 incidences at 8
  per register give R420's 360 hub registers exactly.

**Open next questions.**
1. Minimum puncture count for an aligned partition (`aligncp_min.py`).  **Answered (session 6c): exactly 52.**
2. Cheapest corrections for an unaligned partition: minimise the number of odd (E-set, frame) intersections over
   good-frame partitions; each odd intersection costs a single-line hub input or a correction.
3. Given an (almost) aligned partition: a hub system giving every section its E-set from 2 hubs with invertible
   owner-by-input matrices, and the Q-parts (Phi-perp, 25-30 lines per frame) without per-target registers.
4. Can varying parts at the 2-user sections be compensated by in-chain reads on chains 0 -> d-cell -> hub -> t-perp?
   This decides whether R drops from ~770 toward ~600.
5. Pricing of puncturing with pseudo-target totals at h = 11 (adapt P111's `adapt9p.py`).

## 3f. Session 6 (2026-10-16) — frame-top word, arrival floor, blocks and layers, D10 decomposition

**Route status after session 6 (what is proven, what is only measured).**
- *Closed by proof:*
  - sparser decoders at window 11 (B0 unique);
  - 2-sub-frame covers of R(t) (every target needs >= 2 arrivals; R >= 231; the older line-mixing sink floor of
    section 2b, R >= 426, is the stronger all-word bound);
  - aligned good-frame partitions with <= 15 punctures (so E8 R420-type aligned cell words need v <= 204);
  - complete star blocks beyond 6 (K4 packing);
  - block partitions with B <= 24.
- *Bad on exact relaxations (not all-word proofs):*
  - cell-based line distribution needs ~6 partner cells per line for block or frame-top demands (E8: 3);
  - hubs serving layers of k blocks need rank X <= 4 for k >= 3;
  - best aligned hubs on the block partition serve 4 owners x 6 lines (E8 quads: 6 x 8).
- *Verified words:* `word_blkA3.json.gz` R = 3,681 (best; `PAIR=1 PCHAIN=1 QMERGE=1 QALL=1 PIECES=paar HOP=0 MP=1
  python3 build_blk.py blkpartA.pkl OUT`, gcheck PASS, session 6b option sweep), `word_blkA2.json.gz` 3,714,
  `word_blkA.json.gz` 3,723, frame-top 4,717.
- *Open:*
  - an architecture not built on shared good-frame sections or block layers;
  - window-12 decoders with much sparser rows (SAT run in progress, `scratchpad/dec/dec12w.py`);
  - better block partitions (fewer lone TTTT frames; lower bounds now computable from the two parity lemmas).

**Verified word.** `code/lbuild/build_f2hub.py` (good-frame top, partner sources accumulate their deliveries in
phase A): R = 4,717, gcheck PASS on the CP-SAT partition `goodpart.pkl`.  Top = 382 registers (Q, 2 IN, 4 X per
frame); the generic middle costs the rest (copies 2,645, carriers 1,906).  `build_blk.py` generalises it to blocks
(frames sharing a cell-sum plane share Q at pm(W) and layers at pm(V)); on singleton blocks it reproduces 4,717.
Neither beats `word_lsB13qa` (3,798).

**Arrival floor (proven).**
- For a T target, the 115 lines of R(t) impose 55 independent conditions on quadratic forms of t-perp (rank 55 =
  dim Sym^2), so no product of two linear forms vanishes on R(t): R(t) is not inside two hyperplanes.
- For a P target the conditions have rank 54; the unique null form has signature (1,1), i.e. R(P(ab)) lies in
  exactly one pair of hyperplanes: L(S9) (S9 = the other 9 points; 120 lines) and span{T(abk)}.  L(S9) is
  DEGENERATE: it is the affine E8 root set, with null vector (1^9; 3).  So it is not a legal frame.
- Hence every target needs, besides its own chain, at least two registers arriving at t-perp from proper
  sub-frames.  Such a register can only go on to the full frame, so R >= 2*220 - 220 sources + 11 totals = 231.
  (Weak, but it is an all-word bound; the frame-top word meets it at the top level: 216 X + 4.)

**E8 R420 alignment, re-checked.**  In #493/R420 every E-set equals the union of the 8 E-cells of its two feeding
quads (180/180), but 5,760 (cell, E-set) pairs are split.  So E8 has exact covers by chosen cells, not "every cell
aligned".  (The I_{11,1} alignment impossibility of 3e is about all partition cells and is unaffected.)

**Blocks and layers (exact).**
- Frames sharing a cell-sum plane pi span a 4-dim W.  For a section <x,y> of a frame U in W, the two other
  hyperplanes V, V' of W containing <x,y> give E_xy = L(V) + L(V'), with L(V) = N(V) - N(W).  Every layer lies
  inside its real frame pm(V), and all pm(V) are nondegenerate (rank 7-8).
- Complete star block (h; F4): Q = K_h(W6) (30 lines), 12 layers (178 lines), each shared by 3 sections:
  - 4 layers {P(zx), T(hzx) : x in W6} for z in F4, each made of 6 s_h-cells;
  - 4 layers {P(hz), T(F4 - z), T(z, W6, W6)} (17 lines each);
  - 3 layers {T(pqx), T(rsx)} for the matchings pq|rs (6 cells each, cell sum e_F4);
  - 1 layer {P(hx)} + T(W6^3) (26 lines).
- Octet (2 TTTT frames, one 3-matching): W holds the 8 transversals + the 3 matching P lines; Q = 25 lines; 12
  layers (174 lines), each shared by 2 sections; six of them are unions of 6 cells with a common 4-set sum.
- Line incidences of the tops drop from 53 per target (frame top) to 17.3 (star) / 24.9 (octet).

**Block partitions (proven).**
- Maximum edge-disjoint K4 packing of K11 = 6, unique up to isomorphism: {0123, 0456, 0789, 147X, 258X, 369X}
  (exhaustive search with the first block fixed: 10,080 packings, all isomorphic).  So <= 6 complete star blocks.
  The leftover P graph is the two "diagonal" parallel classes of AG(2,3) plus the edge 0X.
- Counting: with s3/s2/s1 star blocks of 3/2/1 frames, o octets, f lone TTTT frames, punctures pP + pT:
  6s3 + 4s2 + 2s1 = 55 - pP and 8o + 4f = 110 - pT + pP.  With 4 punctures, B = #blocks >= 24, and B = 24 forces
  (pP, pT) = (3, 1), s3 = 6, s2 = 4, s1 = 0, o = 14.
- On the unique packing, B = 24 is INFEASIBLE (exact CP-SAT, `scratchpad/blk/exact24.py`).  So B >= 25.
  Independent check: beside the 6-packing at most 3 edge-disjoint two-frame stars fit (9 candidate 4-sets,
  exhaustive), so (s3, s2) = (6, 4) is impossible.
- **Mod-4 point-degree lemma (proven).**  An octet puts 4 of its triples on each of its 6 points, a lone TTTT
  frame 2.  With H(p) = number of PPTT frames with hub p, pi(p) / tau(p) = punctured P / T lines at p, and
  lambda(p) = number of lone TTTT frames at p, the T lines left for TTTT blocks satisfy
  45 - (2H(p) + 10 - pi(p)) - tau(p) = 2 lambda(p)  (mod 4)  for every point p.
  Consequences with 4 punctures:
  - (pP, pT) = (3, 1) with no lone frame is impossible: it needs pi(p) + tau(p) odd at all 11 points, but the
    punctures supply only 9.
  - So B = 25 forces pP = 1, pT = 3, the four punctured supports partitioning the 11 points, (s3, s2, s1) = (5, 6, 0),
    o = 13, f = 1, and H(p) + lambda(p) even exactly at the two points of the punctured P line.

**Decoder (proven by SAT, CaDiCaL via pysat, no proof logs; `code/goodframe/dec11.py`, encoding of
`research/p111-minrank-proof-reconciliation/vendor/pr620/minrank_sat.py`).**
- The largest set of pairwise non-orthogonal lines has 10 lines (exhaustive maximal-clique enumeration).
- Pattern minrank = 11: words in F2^10 are UNSAT (1 s), B0 = (J + G) mod 2 has F2 rank 11.
- **B0 is the unique rank-11 decoder**, with asymmetric labels allowed: "c = 11 and B != B0 on some free pair" is
  UNSAT (8 s).  So R(t) is forced at window 11; session 5's "argued" is now proven (modulo the solver).
- Window 12 admits B0 + 1_A 1_S^T with A, S mutually orthogonal (rows in A drop S, e.g. a block's Q); the savings
  are a few hundred line incidences against 26,070 for one extra window unit.

**Verified block word.**  `build_blk.py` on partition `blkpartA.pkl` (6 complete stars, 3 two-frame stars,
6 octets, 3 lone PPTT, 15 lone TTTT; punctures P(0,10), T(157), T(269), T(348)):
`QALL=1 PCHAIN=1 QMERGE=1 PIECES=paar HOP=0 MP=0 python3 build_blk.py blkpartA.pkl OUT` -> **R = 3,723, gcheck
PASS** (`word_blkA.json.gz`), the new best (was 3,798).  Seeding Paar with the layers (SEEDL=1) gives 3,763; HOP
gives nothing (pieces are not nested).  The middle is still ~3,300 registers (copies 1,949, carriers 1,641).
- Partition facts used: every good-frame partition has pi(p) + tau(p) odd at every point (mod-4 lemma), so with 4
  punctures they are one P line plus three T lines partitioning the other 9 points.  For partA's P side, lambda(5),
  lambda(6) must be odd and all others even, so >= 3 lone TTTT frames (CP-SAT bound 5, found 15).

**Hub and alignment measurements (exact counts on the given partitions; scripts copied to `code/goodframe/`).**
- `quads.py` (hubs = closures of two partition cells, owners = sections containing the hub, aligned = E-part is a
  union of the hub's cells): CP-SAT partition `goodpart.pkl`: best hubs have 3 aligned owners with 2-4 lines each.
  Block partition `blkpartA.pkl`: best hubs are D4s with 6 cells and 4 aligned owners x 6 lines (2 such), most hubs
  serve one owner.  E8's quads: 60 hubs x 6 owners x 8 lines.
- `align_rate.py`: fraction of (frame, other block) pairs with pi_frame n W_block^perp != 0: I11 blkpartA 15.2%,
  E8 (#493) 11.1%.  So E8 is NOT block-aligned either; its quads work at frame level (cells aligned with sections,
  U_Phi 3-dim), with rank-4 quads whose perp (rank 4) holds the 6 owner cells.
- Rank constraint (exact): a hub frame X inside the layer frames pm(V_B) of k different blocks has X^perp >= sum of
  the V_B; two V_B meet in at most a cell-sum vector, so k >= 3 forces rank X <= 4 and k <= 4 at all.  Section owners
  (pairs in X^perp) allow the E8 shape (rank-4 hub, rank-7 perp holding several owner pairs).
- Incidences per line: frame-top sections ~45, block layers ~25 (one per block), E8 E-sets 24.  E8 serves its 24
  with 4.5 registers per line (3 branches + 1.5 empties) thanks to cell-sum butterfly inputs.

**Aligned partitions need >= 12 punctures (proven; `code/goodframe/maxalignP.py`, CP-SAT OPTIMAL in 2 s).**
- The largest family of pairwise compatible (aligned), line-disjoint PPTT frames has exactly 22 frames (WLOG it
  contains (4;01|23), S11 being transitive on PPTT frames).  So an aligned partition leaves >= 55 - 44 = 11 P lines
  punctured.  Then 165 - 44 = 121 T lines remain for TTTT frames, 121 = 1 (mod 4), so >= 1 T line is punctured too.
- Hence >= 12 punctures, more than the 11 totals that could act as P111-style pseudo-targets.  (Earlier: <= 4
  punctures infeasible.)  The full aligned maximum (with TTTT frames) is open; CP-SAT found 42 frames, bound 76.
- Context: P111-tuned (the frontier) is E8 with 9 punctured lines and R = 439 (v = 111); puncturing is a real lever
  there, through the pseudo-target totals.
- **Structure of the optimum:** the 22-frame aligned PPTT family found has all 22 frames with the SAME hub (4),
  i.e. it lives inside D10(4): a splitting of the K10 on the other points into 22 pairs of disjoint edges, missing
  P(5,7).  So a 12-puncture aligned partition must look like: 22 hub-h star frames + punctured P(h,.) x 10 +
  P(x,y) + T(h,x,y) + 30 pairwise aligned TTTT frames tiling the 120 triples of the other 10 points.
- **12 punctures: INFEASIBLE** (`align12.py`, exact CP-SAT, 3,167 s: 22 PPTT + 30 TTTT pairwise aligned frames).
- **Mixed hubs: an aligned PPTT family containing two different hubs has at most 12 frames** (`maxalignP_mixed.py`,
  OPTIMAL).  So every aligned family with >= 13 PPTT frames is hub-uniform, giving pP = 55 - 2n for n PPTT frames,
  and the T count forces pT = 1 - 2n (mod 4).  Puncture counts 12-15 are then either the infeasible case above or
  excluded by the congruence; mixed hubs need pP >= 31.
- **Conclusion (proven): every aligned good-frame partition has >= 16 punctured lines** (v <= 204), far beyond the
  11 totals available as P111-style pseudo-targets.  This closes the aligned-cell (E8 R420-type) route for I11.
- TTTT-TTTT compatibility by support intersection k (from `compat_anat.py`): k=1 always, k=2 4%, **k=3 never**, k=4
  17%, k=5 20%, k=6 7/15.  A TTTT frame is a Pasch configuration (4 triples, pairwise meeting in one point).

**Cell-sharing potential of block demands (exact per line; `code/goodframe/cellshare.py`, partition blkpartA).**
- 321 block demands (Q's, layers, lone-frame sections); each line lies in 30.3 of them (26-32).
- Best partner v of a line shares 9.6 of its demands (8-10).
- Minimum number of parts (partner cells or singles) that partition a line's demand set: mean 7.59 (6-9), all 220
  CP-SAT instances OPTIMAL; singles 1.06 per line.  E8 needs 3 cells per line for 24 E-sets.
- So, even before frames and cross-line consistency, cell-based line distribution in this family needs ~2.5x E8's
  cells per line, about 835 cells in total.
- Faithful relaxation (set cover: every demand containing u must contain at least one chosen partner of u; a cell
  then serves only the demands it is used for): **E8 = exactly 3 per line** (120/120 optimal, `cover_e8.py`;
  matches R420's 3 cells per line), **I11 block demands = 5.94 per line** (5-7; 203 optimal, 17 feasible at
  20 s; `cellshare_cov.py`).  At E8's 3 registers per cell that is R ~ 1,740; at a perfect 2 per cell ~ 1,090.
  Frame-top demands (CP-SAT partition, 50 demands per line): 6.45 per line (6-7; feasible, 10 s per line, upper
  bounds; `cellshare_frame_cov.py`).  Both I11 families need about twice E8's cells per line.  This is the misalignment barrier in numbers (a relaxation of the
  family, not an all-word bound).

**Pair-parity lemma (proven; complements the mod-4 point lemma).**  Count T lines through a point pair {x, y}:
an octet holds 2 of them for each of its 12 cross pairs (pairs from different matching edges) and 0 for its 3
matched pairs; a lone TTTT frame holds 1 per cross pair.  Every P edge lies in exactly one PPTT frame, so mod 2:
  Z := e0 + sum_{complete stars} K_{1,4}(hub; F4) + sum_{single PPTT frames} K_{1,4}(hub; endpoints)
       + sum_{punctured T lines} K_3(triple)
must equal the mod-2 sum of the lone frames' cross-pair graphs, each a K_{2,2,2} (two-frame stars contribute 0;
e0 = the punctured P edges).  So the number of lone frames is at least the minimum number of K_{2,2,2}s summing to
Z, and one lone frame needs Z to be exactly one K_{2,2,2}.  This explains why the CP-SAT T-side solves for the
(6,3,3) P sides with |O| = 6 were INFEASIBLE at presolve (`pairparity.py` filters P sides exactly).

**D10 decomposition (verified for all 220 targets).**  With D10(h) = K_h(10 points) (the decoder-total frames):
  R(t) = XOR over {h : t in D10(h)} of (D10(h) n t-perp),
i.e. 3 pieces for a T line and 9 for a P line.  In D10(h) the piece of a line of the s_h-cell {P(xy), T(hxy)} is
the D8 star K_h(10 - xy) plus its cell partner; both cell members share the same D8.  T targets fit the 2-arrival
floor exactly (3 pieces).  P targets do not: 9 pieces, and any rank-9 frame inside span L(S9) is degenerate, so
their L(S9) part must be split over frames that also contain some T(ab.) lines.

**Session 6b additions (exact unless marked).**
- **D8 nodes = s-cell perps (verified 495/495, `scratchpad/hub/dnode.py`).**  For every s_h-cell {P(jk), T(hjk)}
  the lines orthogonal to both are exactly D8(h;O) = P(O) u K_h(O), O = [11] - {h,j,k} (56 lines, rank 8 inside the
  rank-9 cell perp).  So R(t) = sum over the s-cells c containing t of (N(D8_c) + partner of t in c).  Each D8 node
  has only the 2 cell lines as users (its perp holds no other line).
- **P targets do have legal 3-hyperplane covers** (the sampling run `legalcover.py` that reported none for t = 0, 20
  was only a failed random search; it was stopped).  Explicit cover of R(P(xy)), S9 = A7 u B2, written as
  weightings c on S9 (P(ab) in H iff c_a = c_b; T(abc) in H iff c_a + c_b + c_c = 0; T(xym) in H iff c_m = -s):
  c = (1^7, -2^2), s = 2 (66 lines); c = (0^7, 1, -1), s = 0 (70 lines); c = 1^9, s = -1 (45 lines = A8 + T(xy.)).
  All three are closed, rank 9, nondegenerate, inside R(t), and their union is R(t).
- **Flats of R(P(xy)) (exact description).**  Every hyperplane flat other than span L(S9) contains T(xym) for m in
  exactly one value class of c, and its Lambda-part (Lambda = span L(S9), radical delta = (1^9; 3)) is a rank-8 flat
  of the 120 L(S9) lines; L(S9) maps bijectively onto the 120 E8 lines of Lambda/delta.  A hyperplane contains delta
  iff sum(c) = 0.
- **Block partitions:** B = 26 with stars (6,3,3) plus the pair-parity condition is INFEASIBLE (`exact26pp.py`,
  CP-SAT, 423 s).  `pairparity.py` (exhaustive P-side filter) hit the 30-min limit with no result.
- **Rank-8 covers of R(T) (argued by hand, not machine-checked).**  Write T(ijk)-perp = A + <g_i, g_j, g_k> with
  A = span P(O) (7-dim) and T(hab) = g_h + (e_a + e_b - const).  If three subspaces of rank <= 8 covered R(T(ijk)),
  then: one of them is a D8(h;O) (case I) or all three meet A in hyperplanes and project to the three coordinate
  planes of R^3 (case II) or mixed ranks (cases III, IV).  Two affine hyperplanes cover the 28 K8 edge points
  e_a + e_b only as the parallel pair {p_x = 0} u {p_x = 1}, which forces all three A-parts equal to {x_x = 0} and
  leaves P(x, O - x) uncovered (case II); the other cases fail on the same edge-cover counts.  Consequence if
  confirmed: every T target has a collector whose last read happens at a hyperplane of t-perp, and in the reach
  lemma every T line needs >= 4 low registers (or direct low reads).  The P case looks the same but is unchecked.
- **Node algebra (exact, small).**  At a frame where users bring pieces a_i and leave with a_i + N (telescoping),
  the map is I + 1 c^T, invertible iff the number of combined pieces is even.  So 3 piece-bringing users of a
  section cannot all take it without a 4th register; 2 users plus 1 piece register work (1 dead register).  This
  gives the D8-node design (each D8 node has 2 users and cover number 3) at least one dead register per node,
  i.e. ~500 for the T side alone, so D10-piece tops are not competitive.
- **Telescoping A3 tops tested (exact, `scratchpad/hub/tele1.py`).**  Idea: T(ijk)'s two triangle collectors both
  take N(A3-perp) first (it cancels in the target's sum) and bring it as a piece to their triangle sections, so a
  triangle section {T(abx), T(aby), P(xy)} could be assembled by its two T takers plus the P user as contributor
  with zero waste.  Result: the contributor piece c = N(Q-perp) + N(A3-perp) + N(A3'-perp) has rank 9 in all 1,512
  choices (so it needs >= 2 subframes, i.e. one extra register per section), and no 3 contributions of P(2,3)
  sum to R(P(2,3)) (all 528,988,320 triples checked).  So this zero-waste variant fails; waste >= 1 per triangle
  section remains.  (The A3 defect line also cannot be read in-chain: no section of the A3 top contains it.)
- **2-hyperplane covers of sections (exact checks of found splits; `scratchpad/hub/kappa2b.py`, `cov2.py`).**  Most
  plane sections ARE covered by two hyperplanes of their own span, contrary to "full sections need 3": the
  triangle sections PTT71 (unique cover: F_a = 64 lines = P(O') + P(ij) + K_i(O') + K_j(O'), rank 8, users = the
  same A2; F_b = 28 lines = P(O') + T(k,x,O'), rank 7; 21 shared lines free) and PPP85 (F_S8 + T(xyz)) split into
  two nondegenerate parts; PT-disj66, TT56, PP70 also have splits (some found splits have a degenerate part).
  D8 nodes (56) and TT* (61) have no vanishing quadric, so they need >= 3 pieces.  A 3-user section with such a
  split can give its users {p, q, p+q} with no extra register (inputs p, q, empty).
- **Partial-section tops do not exist for T targets** (`ptop2.py`, `ptop3.py`): over all 136 plane sections of
  T(0,1,2) that have 2-covers (112 two-user cells, 24 three-user triangles; triangle covers exact, cell covers as
  found), no choice of 3 sections and contents in {N(H), p, q} (all splits of the shared lines) gives exactly
  R(t).  The minimum defect is 1, reached by 1,480 combinations, all with full sections: exactly the known A3 tops.
  So T targets need either a 4th collector (defect) plus >= 1 extra register per full section with 3 users, or
  non-section collector contents.  This matches the old A3/TT* floor (R >= 715 within that class).
  Same for P targets: over the 165 plane sections of P(0,1) with 2-covers (120 cells, 45 triangles) there is no
  exact partial-section top either.
- **Mixed tops (exact within the stated families; `scratchpad/hub/mixtop2.py`, `mixtop3.py`).**  For T(0,1,2):
  13,720 closed rank-8 frames W-perp (W spanned by t and two lines; 3-6 users each; at most 47 lines).  No cover of
  R(t) by three of them, and no cover by one plane section plus two of them.  Covers by three plane sections:
  1,036 (frame tops), and in 1,260 orientations two of the three can be shrunk to rank-8 parts, but all of these use
  2-user cell sections.  P(0,1) has no cover by three plane sections at all.  P(0,1): 9,030 closed rank-8 frames
  (at most 47 lines); no cover by three of them and none by a plane section plus two of them.
- **Barrier summary (session 6b).**  Every target needs >= 3 collectors ending in proper subframes of t-perp;
  rank-9 last frames have <= 3 users, rank-8 ones <= 6.  Within all section-type tops checked exactly (full plane
  sections, A3-perps, 2-cover parts, mixed rank-8/9 covers) the only low-defect tops are the A3/TT* ones, whose
  sections need >= 1 extra register each and whose defect needs a 4th collector; this is the old floor R ~ 715
  against break-even ~720-760.  The only unexcluded route is a network whose collector contents are not section
  sums or 2-cover parts (general combinations of >= 3 pieces brought by the users themselves), i.e. a
  "gossip" network in which arrivals do the middle work.  No such network has been constructed or excluded.
  In floor terms (NOTES-full-log "exact room"): all-word sink floor 426; break-even ~633 (k4) - 730 (k3), i.e. a
  middle of <= 0.94-1.38 v above the floor, whereas E8's best words sit 1.58 v (R420) and 2.05 v (P111) above
  theirs.  So an I_{11,1} gain needs a middle more efficient than R420's on a less aligned system.
  At the top level such contents are locally unconstrained (every subset of a 2-coverable section is a sum of two
  pieces with proper spans), so the decisive question is the middle (ranks 5-8): whether collectors can acquire
  their pieces by exchanges at shared frames without extra registers.
- **Gossip primitive (exact algebra).**  At a frame with n collectors each bringing one distinct atom whose XOR is
  the frame sum, all n can leave with (frame sum + own atom) iff n is even (J + I invertible over F2), or one leaves
  with the full sum and the rest with sum + own.  So D-star hubs D(h;Q5) (20 lines, 20 users) can self-assemble
  from one line per user with no extra register; the open issue is returning the lent atoms.
- Parity covers of K8 by K_k (needed to write K_h(O) through K_k hubs): none by triangles, minimum 6 by K4s
  (exact, `k8par2.py`), K5 undecided (CP-SAT UNKNOWN at 120 s).
- `dec12w.py` (window-12 sparse decoder SAT, rows <= 110) was stopped after ~100 CPU-minutes without a result.
- **I11 sections are 2-coverable, E8 sections are not (exact, `scratchpad/e8cmp/e8kappa.py`).**  In E8 no
  quadric vanishes on E7 (63), D6 = cell perp (30) or E6 = A2 perp (36), so every E8 section needs >= 3 pieces;
  most I11 plane sections (triangles PTT71/PPP85, cells PT-disj66, TT56, PP70) split into two pieces.  So at a
  2-user I11 section the two users can each bring one piece and leave with the complement (telescoping), with no
  extra register, which is impossible in E8.  This is a structural point in I11's favour that the earlier
  accounting (which used E8-like kappa >= 3) did not use; it matters only if the targets' telescoped chain sums
  can be made exact (2-level chains: no, `ptop2/3`; 3-level chains G1 < G2 < H through 2-cover part flats: no,
  `ptop4.py`, 0 exact tops for T(0,1,2) over all 195 sections; the part flats add few new contents).
- **Telescoped frame tops are exact (inclusion-exclusion, exact identity).**  For any 3-section union cover
  H1, H2, H3 of R(t) (e.g. the cell sections of a good frame {t,b,c,d}), the chains K -> H12 -> H1, H23 -> H2,
  H31 -> H3 (Hij = Hi n Hj, K = H1 n H2 n H3, each collector taking the full sum at every frame) give contents whose
  XOR is exactly R(t).  In a good-frame block every frame is shared (K: 4 users, triples {x,y,z}-perp: 3, cells: 2),
  and with c_xy = t_xyz + t_xyw + k + E_xy the cell assembly reduces to "the bottom pieces of the two collectors
  entering C_xy sum to the exclusive set E_xy".  So the top itself can be junk-free; the whole cost is delivering
  E-sets and K-sums from the lines, i.e. the middle, where the cell-sharing relaxation needs ~6 cells per line
  (E8: 3).  This restates the barrier at its true location: a gain needs a top whose demands are cell-aligned
  (every target's collector contents never split a chosen cell), which is the open "cell-hub" lead.
- **4-collector rank-8 tops exist for T targets** (`cover4.py`, CP-SAT): R(T(0,1,2)) is covered by 4 closed rank-8
  frames with >= 3 users each (3 is impossible by `mixtop2.py`), so the minimum is exactly 4 in that family.
  Such tops avoid rank-9 frames but cost 3 arrivals per target (floor R = 451); session 3's middle walls for
  rank-8 tops (>= 1,001 in the examined families) apply.
- **D4-hub form of T targets (exact identity).**  K8 has the parity cover by six K4 blocks {s u m_1, ...} (a
  special pair plus three 4+4 splits), so with G_Q = D(i;Q) + D(j;Q) + D(k;Q) (rank 6, 27 lines, users T(ijk) and
  the 6 P lines on O - Q):  R(T(ijk)) = sum over the 6 blocks Q of N(G_Q) + N(A2(ijk)), and N(G_Q) = sum_h
  N(D(h;Q)) + N(A2(ijk)) with D4 hubs D(h;Q) shared by 30 targets.  The G_Q are specific to the target (990 of them
  over all T targets) and pairwise unions of G_Q's have <= 2 users, so this E8-like quad structure does not give a
  cheap middle either.

**Session 6c (2026-10-16): stop budget, other Lorentzian systems, cell-hub sizing.**
- **Hosting wall and stop budget (exact pricer arithmetic, `code/price/budget.py`; scratch `price/budget_zero.py`).**
  For v = 220, h = 11 the idle slots host 18 residuals per port copy, so 9R <= 7,920: **R <= 880 is a hard wall**
  (beyond it the pricer has no hosting).  Every verified I11 word so far (best 3,681) is beyond the wall.  Inside
  it, the budget against P111-tuned (in units of split cost) is 24.7 at R = 700, 22.5 at 760, 21.0 at 800, 19.5 at
  840.  The split cost per register is ~0.006 per stop at rank 1 or 10 and ~0.012-0.013 per stop near mid-rank;
  example chains: 0-7-9-11 0.017, 0-3-5-7-9-11 0.031, 0-1-2-4-6-8-11 0.033, 1-2-11 0.006, 0-1-9-10 0.011.
  So break-even is ~840 if registers average a 3-stop chain (~0.017) and ~650 if they average 5 stops (~0.032).
  The old "630-730" range corresponds to the heavier shapes of section 1.  A frontier word therefore needs BOTH
  R ~ 650-840 AND few stops per register.  P111 (E8, h = 8) uses ~5.3 jumps per register, which h = 11 cannot afford.
- **Other Lorentzian systems (estimate, #620 helper model `scratchpad/lor6/screen.py`).**  For each window h, the
  decoder cost per line x* at which floor (1.93 v) + middle M v ties P111, and the line count needed with c totals
  at rank h - 1:

  | h | x* (M = 1.58, R420-quality), abs / rel | v needed (c = h), abs / rel | best known system |
  |---|---|---|---|
  | 9 | 0.545 / 0.555 | 132 / 130 | LP bound 136 (F2 rank <= 8 forces x >= 9/17 = 0.53) |
  | 10 | 0.500 / 0.522 | 180 / 172 | 165 (I_{10,1}), 176 abstract (x = 0.625 actual) |
  | 11 | 0.454 / 0.489 | 242 / 225 | 220 (I_{11,1}, x = 0.500) |
  | 12 | 0.407 / 0.456 | 324 / 290 | 298 lattice (x ~ 0.48-0.52) |
  | 13 | 0.359 / 0.423 | 434 / 369 | 364 (I_{13,1}, x = 0.429) |
  | 14 | 0.311 / 0.390 | 585 / 467 | 455 |
  | 16 | 0.220 / 0.331 | 1093 / 725 | 680 |

  With a P111-quality middle (M = 2.05) every requirement grows by another 5-15%.  The T_h families (v = C(h,3),
  h point totals at rank h - 1, x = 6/(h - 2)) miss by more: x = 0.50 at h = 14 (x* <= 0.39), 0.43 at h = 16
  (x* <= 0.33).  So no known Lorentzian unit
  reaches x* even under the optimistic piece scaling: I_{13,1} misses by 1.3% (rel) and I_{11,1} by 2% (rel); under
  abs both miss by 10-20%.  At h = 9 a unit would need v >= 133 (9 totals at rank 8) against the clique-LP bound
  136 (F2 rank <= 8, x >= 9/17 = 0.529 < x* = 0.545); the only 136-line class configuration (O^-(8,2)) did not
  realise below real rank ~19 (numerical, NOTES-full-log), so h = 9 needs a near-extremal configuration that is
  not known to exist (not excluded).  h = 8 is E8.
- **Whole-lattice unit searches (exact within the scope; `scratchpad/lor7/orbits_free.py`, the lor3 orbit search
  without the w-perp constraint, entries |x| <= 2, |y| <= 3, norms +-2, +-4, +-6, odd-or-zero products).**  All of
  I_{10,1} (window 11): the maximum invariant system under S10, S9xS1, S8xS2 and S5xS5 is 176 lines (the I_{10,1}
  family 165 + 10 norm-4 + 1 norm-6 vectors), below I_{11,1}'s 220 at the same window.  All of I_{11,1} (window 12):
  231 under S11, S10xS1, S9xS2, S6xS5, far below the ~290-324 that window 12 needs.  Heuristic reason the I_{n,1}
  family is close to optimal: height-1 lines (x; 1) need norm-3 vectors x with pairwise products in {0, 1, 2}, a
  spherical 3-distance set, whose size is at most C(n+2,3) + C(n+1,2) ~ n^3/6, and the triples already give C(n,3).  Changing the system therefore does not remove the barrier; I_{13,1}'s tops are also worse
  (section 3d: T 3-section tops need R >= 1,352 > its tie point ~1,280).  The lever stays the middle network.
- **Cell incidences on partA (exact counts).**  Every one of the 54 partition frames shows all 6 of its pairs as
  R(t) n F for some targets (22-38 targets per pair) and its full quad to 30 targets: 9,320 pair incidences and
  1,460 quad incidences (10,780 cell reads instead of 25,128 line reads, a factor 2.33).  So a cell-hub middle has
  7 cell registers per frame (378) before any copies, on top of the ~382-register top.
- **Cell-hub chain cost (estimate).**  Collectors that read cells at a nested sequence of hubs need chains like
  0-3-5-7-9-11 (0.031) and cell registers 0-1-2-4-6-8-11 (0.033); at R = 760 (top 382 + 378 cells, no copies) the
  stop cost is ~0.032 x 760 + ~5 for sources and targets = ~29 against a budget of 22.5.  So direct cell reads at
  multi-level hubs cannot reach break-even even with zero copies; they can only cut R toward ~1,000-2,000.
  The exact cell-respecting 3-cover SAT (`scratchpad/blk/cellcover_sat2.py`, exact rank-9 degeneracy clauses; the
  earlier "outside" clause was too strong, so its UNSAT answers were not certificates) is running on all targets.
- **Cell reads do not shrink the demand content (exact counts).**  A cell-respecting collector top has 3 private
  collectors per target, i.e. 10,780 cell units of demand; the E-set top already shares each E-set between its 2
  users and Q between 4, i.e. 10,661 line units.  The factor 2.33 from reading cells is cancelled by the lost
  sharing, so cell-hub direct reads alone do not cut R; any gain must come from hub sharing below the top.
- **Varying-part hub capacity on partA (exact per hub; relaxed greedy cover; `scratchpad/hubrank/`).**  Hubs
  Z = W-perp, W = closure of 1-3 consumer pairs (152,772 hubs); at Z the parked registers needed = F2 rank of the
  consumers' restricted E-set rows.  Best hubs: rank 1, 3 consumers, 78 incidences (star-block structure); the
  capacity histogram peaks at 4-8 incidences per register.  A lazy greedy cover of the 9,320 E-set incidences by hubs
  with >= 2 consumers (chain nesting ignored, cost of building the parked contents ignored, Q sets not included)
  needs **591 hub registers** (60% of the incidences cost 151 at >= 24 per register, the rest falls off to ratio 2).
  With the ~382-register top that is already ~970 > 880, the hosting wall, before any parked content is built.
  So on partA even an idealised one-level varying-part hub middle cannot reach the priceable range (heuristic: greedy,
  not a bound).
- **Hub-sharing middle in the block builder (measured; `scratchpad/blk/build_hubm.py`, a copy of `build_blk.py`
  with a HUBS stage).**  One greedy hub per top demand (2-pair hubs, 44,905 candidates), parked registers = F2 basis
  of the users' rows, residual contents to the Paar middle.  Same options without quad merges
  (`PAIR=1 PCHAIN=1 PIECES=paar HOP=0 MP=1`): baseline R = 3,908; HUBMODE=hop (one assembler per user) 218 parked
  registers serving 348 tops / 5,032 incidences, **R = 4,129**; HUBMODE=read (the accumulating source or the
  in-chain targets read the hub registers themselves, no assemblers) **R = 4,657-4,717**.  Removing hub parts from
  the tops destroys Paar's sharing (top terms 5.3 -> 7.4 per top, carriers +349, copies +270), and the hub contents
  still have to be built.  So hub sharing does not cut R on this top; the Paar middle already captures the common
  structure.  (Side fix found here: `mp_refine` accepted a top demand as a child when its content, but not its
  frame, lay inside the parent's frame; the scratch copy now also checks the frame.  The repo builder never hit it.)
- **Why the middle is about 2x harder than E8's (exact counts).**  The E-set load per line is 9,320 / 216 = 43
  (E8: 2,880 / 120 = 24), because |R(t)| = 115-129 is about twice E8's 63 while the register budget per line at
  break-even is about the same (~3.3-3.8 helpers per line).  So an I_{11,1} middle must deliver ~1.8x more line
  incidences per register than R420's.  Alignment alone would not close this: with aligned cell sums one hub level
  still needs ~650 registers (section 3e count), i.e. R ~ 1,200 with the top.
- **Sparse decoders (the only lever on the middle load itself).**  A decoder is any rank-c F2 matrix B with
  B_tt = 1 and off-diagonal support inside the orthogonality graph; target t reads c_t = row t (not necessarily all
  of R(t)).  Counting allows rows as small as v/c - 1 (~19 at c = 11).  But B0 is the unique rank-11 decoder, and its
  row space C_11 (the totals' code) has weight distribution 90^66, 104^495, 110^924, 116^495, 130^66, 220^1 (exact,
  2,047 codewords).  If a rank-12 decoder's row space contains C_11, every sparse row r_t would satisfy
  r_t + r_t' in C_11, i.e. weight >= 90, so its rows cannot be sparse; rank-12 row spaces not containing C_11
  remain open (`scratchpad/dec/dec12w.py` was stopped earlier).  Also rank 12 costs x = 0.545, which cuts the tie
  helper density to ~1.9-2.3 per line (est_model: x 0.50 -> 2.66/3.34, 0.55 -> 1.91/2.32, 0.60 -> 0.96/1.36), so
  even a very sparse rank-12 decoder would need R <~ 470.
- **"Readers do the middle" (tree of telescoped hubs; counting estimate).**  Free registers are the 216 sources
  (any work at frames containing their line) and the 216 targets (in-chain reads, long chains are affordable at
  ~0.006-0.013 per stop).  If hub frames form a tree (each frame always entered from the same parent), one register
  per node holding N(Z - parent) gives every reader passing Z the telescoped sum N(Z) at no copy cost.  But
  (i) 3 full-section readers cannot XOR to R(t) exactly (defect >= 1, `ptop2/3`), so each target needs its in-chain
  node, one source arrival and two helper arrivals (~432 helpers); (ii) rank-9 leaves have <= 3 users, so >= 288
  leaves for ~864 node uses; (iii) every line needs one carrier per tree node where it first appears, and the leaves
  containing a line form an antichain of ~90 sections.  This puts R above ~1,000 before carriers, again past the
  wall.
- **Breakthrough candidates checked after "look for breakthroughs" (session 6c, exact unless marked).**
  - *Scatter as a broadcast channel:* any register can be retained and scattered into any set of targets for one
    copy child of its frame rank, so retaining N(X) would remove N(X) from every target's phase-B reads.  But
    retained copies are unhostable mass: with a plausible 3-stop histogram at R = 600-760, adding 220 rank-1 retained
    registers leaves the pricer with no root at all, whereas 20 extra helpers cost only ~1.5%.  Dead.
  - *A2 cells on the source side* (3 lines in a rank-2 frame, 3 registers in and out, no empty): every output sits at
    a frame containing the A2, so it only reaches A2-perp targets, and the 3-covers of R(s) by plane sections are only
    good 4-frames and PPP triples (section 2a), so A2 planes cannot carry a source's 3 branches.  Dead.
  - *R420 transfer (3 registers per cell, R ~ 770 or ~3.5 v):* needs an aligned partition.  Best known 4-puncture
    partitions carry ~5,920 odd (E-set, frame) intersections (`scratchpad/part/minodd_2.log`), each a single-line
    hub input.  **The minimum puncture count for an aligned good-frame partition is exactly 52 (proven: CP-SAT
    OPTIMAL, obj = bound = 52, `code/goodframe/aligncp_min.py` run on `scratchpad/part`; WLOG frame (4;01|23) fixed,
    valid since < 55 punctures leaves a P line live).**  So aligned partitions exist only for v <= 168 (42 frames;
    a randomised greedy, `scratchpad/part/aligngreedy.py`, finds 168 lines in seconds).  An aligned R420 port on v = 168 would sit
    near R ~ 3.5 v ~ 590, but its decoder cost x = 110/168 = 0.65 puts the tie helper density near zero, so
    alignment by heavy puncturing does not help the price.
  - *Sparse decoders:* see above (rank 11 unique; rank-12 row spaces containing C_11 cannot be sparse).  A
    simulated-annealing search over B = U W^T (`scratchpad/sdec/sdec_ls.py`) started from B0 at rank 12 only finds
    B0-like decoders (total row weight 25,955 vs 26,070); random starts at ranks 12, 14 and 16 stay at ~7,000
    violations (method too weak; inconclusive).
  - *Cheaper retained pieces for B0:* the decoder cost is the sum of the frame ranks of the retained registers, not
    10 per total.  B0 = S P with 12 pieces needs 12 low-rank line sets in ONE coset of C_11 (pieces of weight <= 85
    cannot lie in C_11, whose minimum weight is 90) whose pairwise sums span C_11; that would give cst <= 108 (rank 9)
    or 96 (rank 8) instead of 110.  Among 14,355 structured low-rank candidates (plane sections, D10 n t-perp, stars
    K_h(S8), K_h(S9), L(S8), D10(i) n D10(j); `scratchpad/dcost/coset.py`) no coset holds 12.  A coset with this
    property would need each D10 total covered by two hyperplanes, which D10 does not allow.  Not pursued further.
- `exact25pp.py` (B = 25 partition + pair parity) was stopped after ~2.7 h wall without a result.  `cover4.py` P side:
  R(P(0,1)) is covered by 5 closed rank-8 frames with >= 3 or >= 4 users and by 6 with >= 5 or >= 6 users (CP-SAT
  FEASIBLE, optimality not proven; 3 is impossible by `mixtop2.py`, so the minimum is 4 or 5).

**Session 6d (2026-10-16): new line systems — break-even grid, inequalities, h = 9 closed for root-like systems.**
- **Break-even grid** (#620 helper model, `scratchpad/newunit/tiegrid2.py`; rho* = helpers per line that ties P111-tuned,
  abs/rel; "-" = cannot tie even with zero helpers):

  | h | x: rho* |
  |---|---|
  | 3 | 0.67: 12.0/9.8; 0.8: 4.87/3.19; 1.0: - |
  | 4 | 0.75: 4.54/3.15; 0.85: - |
  | 5 | 0.8: 0.46/0.21; 0.9: - |
  | 6, 7 | - for every x >= (h-1)/h |
  | 8 | 63/111: 3.95 (P111 itself); 0.7: 0.69; 0.8: - |
  | 9 | 0.5: 4.31/4.53; 0.53: 3.78/3.98; 0.6: 2.17/2.37; 0.7: 0.16/0.23 |
  | 10 | 0.5: 3.51/3.88; 0.6: 1.52/1.83 |
  | 11 | 0.4: 4.25/4.84; 0.5: 2.66/3.34; 0.6: 0.96/1.36 |
  | 12 | 0.4: 3.59/4.27; 0.5: 2.17/2.74; 0.6: 0.55/0.98 |

  Small windows would need x <= ~0.8 (h = 3) or ~0.76 (h = 4); single-field units have x >= 1 there (known).
- **Inequalities for norm-2 lines with products in {0, +-1}** (d_t = number of non-orthogonal partners,
  `scratchpad/newunit/ineq_check.py`):
  - (F1) Euclidean R^h: sum d_t >= 4(v-h)^2/h + 4(v-h).  E8 meets it with equality (6,720).
  - (F2) Lorentzian R^{h-1,1}: sum d_t >= 4(v-h+1)^2/(h-1) + 4(v-h+1).
  - (F3) With w = F2 rank of the Gram mod 2: average |N[t]| >= (v - 2^{w/2})/2, from the eigenvalues +-2^{w/2} of
    (-1)^{B(a,b)}.  E8 64 >= 52, I_{11,1} 119.5 >= 94.  So B0-type units carry about v/2 correctors per target unless
    v is close to 2^{w/2}.
  - **Correction:** the O^-(8,2) nonsingular graph has B = 1 degree 72, so D = 9,792 >= the F2 bound 8,704 at h = 9.
    F2 does NOT exclude it.  An earlier hand estimate (degree 63) was wrong.
- **Theorem (exact): a root-like system at h = 9 has at most 127 lines** (norm-2 vectors in R^{8,1}, products in
  {0, +-1}; `code/h9/rootlike_bound.py`, about 1 min).
  1. *Frame-free systems have <= 119 lines.*  The Gram mod 2 is alternating of F2 rank <= 8, so the lines map to a
     symplectic F2^8 with B = 1 exactly on non-orthogonal pairs (twins allowed).  Lines with images in one Lagrangian
     are mutually orthogonal.  Double counting over the 2,295 Lagrangians (135 through each nonzero vector, checked by
     enumeration) gives v <= 119 when no Lagrangian holds 8 lines.  So every system with >= 120 lines contains 8
     mutually orthogonal lines.
  2. *Systems with an orthogonal 8-frame.*  Any other line has x_i = <u, e_i> in {0, +-1}, support k >= 4 and an
     E-perp part with gamma^2 = k/2 - 2.  Products are rational only inside a class:
     - A: k in {4, 6};
     - B1: k in {4, 5};
     - B2: k in {4, 8} (k5-k8 pairs are parity-incompatible);
     - C: k in {4, 7};
     - Euclidean: k = 4 only.

     Same-support sign patterns form diameter-<= 3 codes (Kleitman bound 2k).  Support families obey parity rules.
     In B1, a k5 support containing T kills one k4 class on T.  Exact support-level maxima (CP-SAT OPTIMAL) give:

     | class | max lines |
     |---|---|
     | Euclidean | 120 |
     | A | 104 |
     | B1 | 127 |
     | B2 | 122 |
     | C | 78 |
  3. Heuristic: a 180 s max-clique local search (`scratchpad/h9/dls.c`) on every class stalls at 112 + 8 = 120, i.e.
     E8.
  - The #620 model needs v >= 130 (rel) / 132 (abs) at h = 9 with an R420-quality middle (c = h totals at rank h - 1),
    so **root-like Lorentzian units at h = 9 cannot reach the tie line**.
  - Still open: the general class model, i.e. complex orthogonal representations of O^-(8,2), possibly with products
    outside {0, +-1}.  This is excluded only numerically (LM residual^2 = 114 - 6h; NOTES-full-log), not proven.
  - **Session 6h, vector-level class maxima (exact CP-SAT; `scratchpad/h9x/b1clique.py`).**
    - Method: the frame is forced, one non-k4 line is fixed WLOG (signed permutations and n -> -n are transitive),
      and the solver takes the maximum clique of compatible vectors.
    - Results:
      - **B2** (k4 + k8): 107 lines, OPTIMAL (98 k4 + 8 frame + 1 k8).
      - **B1** (k4 + k5): proven bound <= 111 (best found 88).
    - Every class system that actually uses the timelike direction therefore has <= 111 lines (A <= 104,
      C <= 78 from the support level).  The support-level 127 was loose.
    - **h = 9 root-like systems with more than 111 lines must be frame-free, hence <= 119.**
    - 119 is reached only if every Lagrangian holds exactly 7 lines.  The 119 singular points of O^-(8,2) do this:
      Q restricted to a Lagrangian is a nonzero linear form, so the Lagrangian holds 7 nonzero singular vectors.
      Their orthogonality graph is the polar graph srg(119, 54, 21, 27).
    - **The 119-point quadric is NOT root-like realisable (proven).**
      - Local structure: for a totally singular line l = {p, a, p+a}, l^perp minus l holds 20 points in 5 cosets
        x + l.  Each coset is 4 mutually collinear points, and points in different cosets are never collinear
        (the quotient is the 5-point ovoid Q^-(3,2), which has no lines).
      - So a realisation needs 20 norm-2 vectors in span(u_p, u_a, u_p+a)^perp = R^{5,1}: 5 groups of 4 mutually
        orthogonal vectors, with all cross products +-1.
      - Proof that this is impossible:
        1. Take group 1 as v_1..v_4 spanning P.  Every other vector is w = (1/2) sum s_i v_i + n with
           s in {+-1}^4 and n null in P^perp = R^{1,1}.  So n is in R e, in R f, or 0.
        2. The sign classes mod +- split into 4 even and 4 odd.  Same parity, different class gives
           h.h'/2 = 0; different parity gives +-1; same class gives +-2.
        3. Two vectors of the same parity in different groups need n.n' = +-1 or +-3 != 0, so one is e-type
           and the other f-type.  Hence each parity occupies at most 2 groups, and no vector has n = 0.
        4. So groups 2-5 are 2 pure-even and 2 pure-odd groups.  Each group is single-typed and uses its 4
           classes once.
        5. The magnitudes then satisfy a b = 1 and a' b' = 1 (same-parity cross pairs), and a b' = 2 and
           a' b = 2 (opposite-parity mixed pairs need |n.n'| = 2).  These are inconsistent: a' b' = 4.
      - LM agrees: best residual^2 18.7 over 20 seeds (`h9x/local20.py`).
      - The big LM on all 119 points (`h9x/qreal.py`) was stopped once the proof was in.  The E8 control
        (O^+(8,2) nonsingular at (8,0)) converges to residual^2 1.8e-28.
    - **Still open at h = 9:** frame-free multisets with twins.  The exact ILP (`h9x/lagms.py`) attains 119 with
      15 doubles and 1 triple, and >= 117 with 22 doubles, so the combinatorial bound alone does not close
      117-119.  The f = 0.5 lever model needs v >= 117 at R = 3.5v (`lor6/levneed.py`).
    - Exact max clique in E8 (+) <-2> = E7 (+) U, |m| <= 1, with a timelike line (`h9x/e8m2.py`): 107 found;
      the bound stalled at 132 and the run was stopped.
  - **Session 6h, h = 9 non-root-like systems (products any odd integer, even norms).**
    - The 127/119 ceilings do not apply.
    - Combinatorial cap: 136 lines if all lines are spacelike (Lagrangians hold <= 8).  A timelike line raises the
      Lagrangian cap to 9, but every 9-loaded Lagrangian needs exactly one timelike line, and the timelike lines
      are pairwise non-orthogonal.  153 would need them to form an ovoid of W(7,2), which does not exist.
    - Load per line is E8-like (|R(t)| ~ v/2 ~ 65), so this is the window where an R420-type middle is least
      implausible.  The h = 9 need is 117-132 lines.
    - Zero-pattern local screen (`h9x/genlocal_zero*.py`, `zerolm*.py`):
      - Method: only the zeros are enforced; norms are fixed at +-2; non-orthogonal products are kept >= margin.
      - Margin 0.3: 6/6 sampled 125-126-line multisets fail, residual^2 0.24-0.76.
      - Margin 0.05: 3/3 fail with 0.0029-0.012, i.e. about 1-5 x margin^2.
      - The residual scales like margin^2.  That would mean some non-orthogonal products are forced to zero.
      - **Caveat (control failure):** the same margin-LM did not realise E8's own pattern at (8,0) in 300
        iterations (seed 0, residual^2 19.5), so these failures are not yet reliable.  A rerun with 12 seeds x 2000
        iterations, plus an E8 control at 6 seeds x 1500, is in progress (`genlocal_zero05b.py`).
      - **The quadric's 20-point local structure is realisable once products are free** (`h9x/q20free.py`:
        residual^2 ~1e-29 at margins 0.3, 0.05 and 0.01 in R^{5,1}).  So the obstruction that kills the root-like
        119-point quadric does not apply to non-root-like systems.
      - Integral attempt in E8 (+) <-2> with the 56 quadric roots kept as E8 roots: impossible (`q119/lifts.py`).
        - Each of the other 63 classes is collinear with 24 of the 56, and those 24 span the whole E8 part.  Every
          lift would then lie on the timelike axis.
        - A realisation must tilt the 56 out of a positive 8-space.
      - If the 119-point quadric is non-root-like realisable with odd integer products, up to 9 more points can be
        added (pairwise non-orthogonal, at most one per Lagrangian), for <= 128 lines at h = 9.  Its load is lighter
        than E8's: |R(t)| = 54.  Open.
    - Lines needed at R = 3.5v (generic chains, `lor6/h8need.py`):
      - cst 56 (c = 8): 95 / 90 / 87 for f = 0 / 0.25 / 0.5;
      - cst 63: 107 / 102 / 97.
    - Exact class maxima with an orthogonal 7-frame and a timelike-using line (`h9x/h8class.py`, OPTIMAL):

      | class | max lines | composition |
      |---|---|---|
      | {4,5} | 43 | 7 frame + 12 k4 + 24 k5 |
      | {4,6} | 29 | 7 frame + 21 k4 + 1 k6 |
      | {4,7} | 57 | 7 frame + 49 k4 + 1 k7 |

    - So every h = 8 Lorentzian root-like system with > 57 lines is frame-free (no 7 mutually orthogonal lines),
      including the 70-line DLS systems.
    - **Mixed sign (norms +-2, products 0/+-1), exact** (`h9x/h8mixed.py`).
      - With a spacelike 7-frame, the classes are {4s,5s,0t,5t}, {4s,6s,4t}, {4s,7s} and {4s,kt}.  Maxima: 64
        (E7 + one timelike line orthogonal to it), 44, 41, 63 and 30.
      - Each single timelike type admits at most 1 line, since two such lines would need x.x' >= k + 2.
      - Inertia: the spacelike cubes give a Phi-positive block (<= 91) and the timelike cubes a Phi-negative block
        (<= 29), so mixed systems have <= 120 lines.
      - Frame-free mixed systems allow <= 6 spacelike + 1 timelike per Lagrangian.
        - Local screen (`genlocal_pm.py`): norms +-2, and both perp signatures (p - k, 1) and (p - k + 1, 0)
          tried.
        - All 6 sampled 87-line multisets fail a local 13-17-line configuration (best residual^2 4.0-18.8).
          Numerical.
    - Frame-free bounds: <= 102 (Lagrangians hold <= 6), <= 91 (inertia).
    - An 85-91-line frame-free system with a cst-56 decoder and an R420-quality middle at f >= 0.5 is the only
      h = 8 opening, and none is known.
  - **E8's orthogonality pattern in R^{7,1}** (the "same structure, Lorentzian form" loophole).
    - All norms +2: impossible.  An 8-frame of mutually orthogonal lines must contain exactly one timelike line.
    - Norms +-2 with one timelike frame line f_0, odd integer products: impossible by parity.
      - A line w whose Hamming support S contains f_0 has norm (p_1^2 + p_2^2 + p_3^2 - p_0^2)/2 with odd p_i.
      - The numerator is 2 mod 8, so the norm is odd.
      - The same argument kills any choice of equal frame norms 2m: the numerator 2(1 + 4k) = 2m * even forces
        m odd and an odd norm.
    - **General case, proven: no realisation by non-null vectors in R^{7,1}, for any norms and any products**
      (exact counts plus CP-SAT).
      1. An 8-frame is an orthogonal basis of R^{7,1}, so by Sylvester it holds exactly one timelike line.
      2. Two timelike vectors are never orthogonal.
      3. E8 has 2,025 8-frames with 135 through each line.  So the timelike lines number exactly
         2,025 / 135 = 15, and they are pairwise non-orthogonal.
      4. But E8's largest pairwise non-orthogonal set has 8 lines (CP-SAT OPTIMAL).  Contradiction.
      - E8's structure cannot be reused in a Lorentzian form at the same window.
    - **Same configuration, new form (exact linear algebra, `h9x/formspace.py`).**  Consider symmetric forms M
      with e_i^T M e_j = 0 on every orthogonal pair:
      - E8's 120 lines: the space is 1-dimensional (M = c * Gram).
      - P111's 111 lines: also 1-dimensional.
      - So no Lorentzian form keeps P111's (or E8's) projective configuration and orthogonality pattern.  The
        verified E8 words cannot be reread as Lorentzian words.
      - Largest E8 subsets that keep their pattern under a Lorentzian form with odd-or-zero integer products
        (`h9x/e8sub.py`):
        - Forms diagonal in an 8-frame (30 integer choices, exact CP-SAT max independent set): best 71 lines.
        - Rank-1 changes M = G - c v v^T: S = (lines perp v) + a pairwise non-orthogonal set.  That is
          <= 63 + 8 = 71, attained with v a root.
        - The h = 8 window needs 85-95 lines.  Closed for E8-derived configurations.
      - Numerical control (`h9x/orthjac.py`, (8,0)): the zero pattern alone recovers E8, with all products +-1.
  - **Local realisability screen for frame-free windows** (numerical, `h9x/twinlocal.py`, `genlocal.py`,
    `genlocal2.py`).
    - Method:
      1. Draw F2 multisets in symplectic F2^8 that meet the Lagrangian cap (CP-SAT with random objectives).
      2. Pick k = 3-4 mutually orthogonal lines.
      3. The lines orthogonal to all of them must embed root-like in R^{p-k,1}.
      4. Test that by LM, 3 seeds.
    - Every sampled multiset failed a local test, with best residual^2 2.85-14:

      | window | cap | sizes sampled | multisets | result |
      |---|---|---|---|---|
      | h = 9 | 7 | 117-118 (twins) | 10 | all excluded |
      | h = 8 | 6 | 87 and 97-99 | 12 | all excluded |

    - Numerical evidence on samples, not a proof.  It agrees with the proven quadric obstruction.
- **Decoder value (exact pricer, `code/price/pricer.py`).**  The deficit is T(h v - (h+1) cst) (#545's rank-mass
  identity) and does not depend on R.
  - On P111, one unit of decoder constant is worth +2.80%, and one whole helper (8 mass units, R - 1) +0.135%.
  - Full E8 at cst = 70 would have deficit value 960 - 630 = 330 > P111's 321.  On R420's skeleton (0.0016538 at
    cst 72) that is about +5.6%, i.e. above P111-tuned.  At cst 71 it ties.
  - So a non-star full-E8 decoder with cst <= 70 would set a new frontier without touching the middle.
  - Window <= 9 forces B0 and 72 (format-limits C.6 / #446 Theorem C).  Window >= 10 is listed upstream as open
    ("non-star decoder").
- **Window-10 E8 decoders (session 6d, `scratchpad/dec10/`).**
  - SAT (`w10struct.py`, `e8dec.py`): window-10 decoders exist.  One example is B0 plus a rank-3 change on 23 rows:
    two targets get weight-2 rows, and 21 rows each lose the same 2 lines.
  - Its best decomposition (`bestdec.py`, exact selection in `exactsel.py`) costs exactly 72 = 2 + 7 + 7 + 7 x 8.
    The structure is a "pseudo-puncture":
    - a frame piece serves the two sparse targets (cost 2);
    - their two stars cost 7 each;
    - the column-space deficient codewords are incompatible (dot products 1).
  - Accounting for pseudo-punctures of k mutually orthogonal lines: frame piece k + k stars at 7 + (9 - k) full at 8
    = 72 for every k.  The same tie appears when one P111 line is un-punctured: its row costs a piece of rank 1,
    giving value 896 - 576 = 320 vs 321.
  - Random 10-star templates (sources in z_j-perp, or readers in z_j-perp; cost 70) are UNSAT within a second.
  - Running: all E7-deficient 10-piece decoders with the solver choosing sides and centres (`e7def.py`), and
    "8 full + 2-3 tiny pieces of <= 2-3 lines" (`tiny.py`, cost <= 68-70).
  - Conjecture (not proven): every E8-pattern decoder costs >= 72 - (#punctured lines), so each puncture saves at
    most 1 and P111's 321 is the E8 maximum.
  - **Reduction (exact).**
    - Every valid decoder N differs from B0 only on orthogonal pairs.  A singleton piece ({t}, {s}) with t _|_ s has
      pairing rank 0, so B0 = N + (free pieces).  Hence min cost over all decoders and all windows equals the min cost
      over all rectangle decompositions of B0, with any number of pieces.  The window plays no role.
    - The window-9 result covers only the 9-piece (codeword) decompositions, where every reader set spans.
    - A piece with source set or reader set in a lower-dimensional flat is cheap (stars 7, frame pieces k,
      single-source pieces 1).  The open question is whether XOR cancellation among such pieces can rebuild B0 below 72.
  - Within-a-decomposition sums give no useful bound: rank(G o C) <= cost (C the integer cover counts) only yields
    cost >= 8 (G itself has the required zero pattern).
  - Mutually orthogonal sub-systems give cost >= sum of their own minima (block-diagonal restriction).  The best
    split is E8 itself.
  - In both cost-72 decompositions found, sum_j P_Uj P_Vj = 9 I exactly (U_j, V_j = reader and source spans).
    Rank >= trace for these products, so "sum of traces >= 72 for every decomposition" would prove the floor.  It is
    being tested (`htest.py`); not proven.
- **Double-star decoders (new, exact; reproducible check `code/dstar/double_star.py`, ~1 min; search in `scratchpad/dec10/dstar2.py`).**  Take centres p_1..p_9 with affinely
  independent classes summing to 0.  Each B-dual vector b_j is then the class of a line p'_j, with p'_j _|_ p_j and
  p'_j non-orth to p_k for k != j.  B0 restricted to the live lines equals sum_j N[p'_j] (x) N[p_j].
  - When all 18 lines are punctured, piece j has sources in p_j-perp and readers in p'_j-perp.  Its pairing rank is
    6, so Theorem C allows cost 54 on 102 live lines.  The deficit value is 8v - 9 cst = 330 vs P111's 321.  Such sets
    exist (found by direct construction).
  - In general each puncture saves exactly one cost unit (cost = 72 - k).  The x = 54/102 that format-limits quotes
    as hypothetical is realised as a decoder decomposition.
  - Price model (P111 profile with the copies and the mass identity adjusted; `code/price/pricer.py`): with R at the
    hosting wall 4v, every partial double-star beats P111-tuned.

    | partners j | v | cst | R | vs P111-tuned |
    |---|---|---|---|---|
    | 1 | 110 | 62 | 439 | +0.69% |
    | 3 | 108 | 60 | 432 | +3.05% |
    | 5 | 106 | 58 | 424 | +5.63% |
    | 9 | 102 | 54 | 408 | +11.1% |

    The binding constraint is R <= 4v.
  - **On P111's own punctured set:** piece 5 (centre line 66) has partner line 87, which is live in P111.  With 87
    also punctured (P110), the 62 readers of total 66 are all orthogonal to 87 and span 87-perp, the sources span
    66-perp, and the pairing rank is 6 (verified on the e8 geometry of the R420 skeleton).
  - **Format obstacles (why this is not yet a word).**
    1. bitE8/1 keeps targets at frame 0 until the scatter, so a COPY costs the full frame dimension of its total
       (7) whatever the readers.  The saving needs the copy dropped to the frame <87> and read there by its 62
       readers in phase B.
    2. <87> is spanned by a punctured line, so it is not a live-label frame; the word format and xcheck must accept
       vector-given frames.  format-limits rule 2 classes general nondegenerate frames as spec.
    3. A priced drop event for a retained total (non-nested step d(f, g) = 6) is needed in the checker and pricer.
    4. On the P111 word, 57 of the 120 phase-B gates that write those readers sit at frames without 87.  Each needs
       F -> F + <87>, and the helpers read must climb, conflicting with later non-orthogonal readers unless sub-copies
       are used.  Sub-copies taken at <87> cost one helper each (~0.135%); the saving is ~2.8%.
  - Multiple double-star pieces conflict (targets read several totals at different stations).  Without copy trees,
    one piece per word is the realistic case.
  - **Corrections after exact repricing (P110 single double-star on the P111-tuned profile).**
    - Each reader must stop at <87>, which adds a rank-1 block (a split r -> 1 + (r-1)).  In the nine-stage root each
      split costs about q (r ln r - (r-1) ln(r-1)) copy units.
    - With 62 readers the net is +0.26% (splitting rank-2 blocks), +0.10% (rank 3), -0.08% (rank 5), instead of the
      ideal +0.68%.
    - The hosting wall at v = 110 is 440, so only one extra helper fits.
    - Propagating "readers' later frames must contain 87" through the P111-tuned phase B
      (`scratchpad/dec10/conflict87.py`): 524 of 712 gates must grow by 87, 336 z registers get forced, and 49 gates
      conflict with targets not orthogonal to 87.
    - Verdict: the single double-star is worth at most about +0.26% and only after a format extension plus a
      re-scheduled phase B.  It is not a drastic gain.
    - The full double-star (x = 54/102, +11% model at R = 408) additionally needs R <= 408 and multi-station
      schedules.  About 4 splits per target (~400 splits) would cost several percent.  It stays a lead, not a word.
  - Eligible punctured sets under #543's plan (gen_p3 eligibility, seed 552; 18 eligible lines): 17,478 affinely
    independent 9-sets, of which 12,963 have at least one partner piece (up to 5).
    - The hosting wall allows only one extra puncture at R = 439 (v >= 110).  So at most one partner piece is usable
      on today's skeleton.
    - Partners in lines 0..7 are not allowed (#493's frame-zero isometry).
    - A conflict-free choice would still need the format extension; the payoff cap is ~+0.26%.  Not pursued.
  - **Current-format cost is source-side only.**  With targets at frame 0 at the scatter, a piece costs dim span(its
    sources), whatever its readers.
    - A source set inside a 6-dim subspace would need >= 27 punctures in a star.
    - So in today's format P111's nine rank-7 stars (63) are the E8 optimum among the decompositions examined.
    - Reader-side savings (double-stars) need cuts.
  - **P110 cut on the P111-tuned word is blocked (exact, `scratchpad/dec10/conflict87b.py`).**  All 49 conflicting
    phase-B gates read a helper that is written again between the readers' cut and the conflicting read.  No
    reordering of the existing phase B removes them, so a redesigned phase B would be needed.
  - **Stage count:** nine stages (K = 4) is optimal for P111's profile.
    - K = 3 caps hosting near R = 253.
    - K = 5 gives -1.30%; K = 6 gives -3.42%.
  - Timed out without an answer (inconclusive, ~50 min each):
    - window-10 E7-deficient decoders, mixed and source-only sides;
    - symmetric root-hyperplane decoders;
    - the doubled-E8 rank at windows 16 and 17.
- **Schedule lever (outside units; exact repricing of the unchanged P111-tuned profile).**
  - The B_K schedule splits each pre-stretch (2p+1)a of pair p >= 1 into [2pa, a].  Each bridge (dst p-1, src p)
    needs pair p at the bridge level while p is idle (common frame at every gate).
  - With unsplit stretches the idle slots become [42, 21, 28, 35, 14, 49] instead of [42, 14, 7, 28, 28, 7, 14, 42, 7].
    Hosting capacity per port copy rises from 18 to 21, and P111-tuned reprices at **+6.13% (0.0018397)** with no
    change to the word.
  - Why it is forced today: with one active pair per stage (format-limits row 13, a convention), one of the two
    pairs a bridge couples is always idle.
  - A schedule with two active pairs per stage could put bridges between active pairs.  It changes the local word
    (4V data + R), (Sch) and (Dfc), and needs a new template, global audit and interface proof.  No such schedule is
    on record.
  - Independent 3-stage motifs per pair (3 pairs, no bridges) avoid splits but cut hosting to 14 slots per copy.  The
    wall drops to about R = 345, which is below P111's 439.
  - Not a word-level contribution; recorded as the largest quantified lever found this session.
  - **Closed for one active pair per stage (exact; `scratchpad/sched/`).**
    - Split-free means every mid-chain bridge sits at a block junction (both pairs at existing vertices), with any
      bridges at start and end.
    - The symplectic structure of locals and bridges (bridges = diag(A, A^-T)) makes start/end bridges complete the
      identity iff the middle product has zero X->X and Y->Y blocks.
    - Pair K-1 is touched only by the last junction and its own block.  So that junction must be +-identity and the
      block a signed swap (trace 0; a two-shear product has trace 1).
    - Induction inward makes every junction trivial and every block a 3-shear signed swap: independent triples.
    - Priced with the unchanged P111-tuned local word (`scratchpad/sched/genprice.py`):

      | triples | stages | result |
      |---|---|---|
      | 3 pairs | 9 | hosting wall (cap 3108 < 3951) |
      | 4 pairs | 12 | -69% |
      | 5 pairs | 15 | -71% |
      | 6 pairs | 18 | -73% |

      The idle fraction dominates.
    - So the split is the necessary price of B_K's 2-local chain.
    - **Two pairs active together do not help either (exact).**  With L_i = [[I, -E_i], [D_i, I]] (diagonal F/R masks)
      and a bridge diag(A, A^-T) between two rounds, L_2 J L_1 is anti-diagonal only if A = E_2 A^-T D_1, forcing
      E_2 = I, then D_2 = 0 and A^-T = 0, a contradiction.  So simultaneously active pairs also need 3 locals each.
      Confirmed by search (`scratchpad/sched/pairgroup.py`).
    - With unit-shear locals, a 2-local pair needs a bridge partner that is mid-idle, so the split is intrinsic.  The
      +6.13% "no split" value would need locals doing more than one shear (a different unit word).
- **Helper entrance-rank lever (quantified; blocked by the D interface).**
  - A helper entering at a rank-e frame has residual width 8 - e (#370's template, complex PR558).  Width-7 residuals
    fill the 666 rank-7 idle slots per replica that are paid in full today.
  - Mixed-width hosting on the P111-tuned profile (`scratchpad/sched/mixwidth.py`, greedy; -0.12% control at n = 0):

    | helpers at entrance rank 1 | vs P111-tuned |
    |---|---|
    | 50 | +0.90% |
    | 100 | +1.93% |
    | 200 | +4.07% |
    | 300 | +6.42% |
    | all 439 | +11.15% |

  - P111-tuned's helpers first act at rank-1 (286) or rank-2 (153) frames, so the structure is there.
  - But all 439 appear in D: their dirt leaks into targets, and the mutable interface compensates it at frame 0 while
    targets sit at 0.  So helpers must enter at frame 0 (H2).
  - Words whose helper dirt never reaches targets (#370's all-column format) allow entrance ranks but historically
    needed R ~ 750-865.  A word that is clean on only part of its helpers would be the target; not attempted.
- **Repeated labels (twin ports, the "vector-linear" class format-limits leaves open): no gain (argued).**
  - Adding one twin of line t to E8: B0's labels are unique at window 9 (C.6), and the layer-1 labels of
    N(t) u {t} span the whole 9-dim label space.  The twin's U-label is orthogonal to all of them, so it is 0,
    contradicting W.U = 1.  So every twin raises the window.
  - Twins of non-orthogonal lines form larger identity blocks (clique bound 8r for r copies).  Each twin then costs
    at least a piece while adding 8 to 8v, so the deficit value does not grow.
  - **Doubled E8 (240 ports): window 16 is UNSAT** (gauge-fixed on the 16 clique ports, `scratchpad/dec10/twins2.py`,
    1 s; CaDiCaL, no proof log).  So rank >= 17 and x >= 17*8/240 = 0.567, no better than P111's 0.568 even at
    rank 17.  **Window 17 is UNSAT too (10 s), so the doubled-E8 minrank is exactly 18 = 2 x 9** (B0 (x) I attains
    it).  Twins give x = 0.6, no gain.
  - *Trivial ports* (a twin whose decoder row is only itself: copy rank 1, no helpers) add one port and raise the
    hosting wall by 4, at -1 deficit unit.
    - Exact repricing on P111-tuned: -0.68% per trivial port.  The deficit cost comes with extra rank-1 blocks.
    - Padding the double-star P102 with 8 trivial ports (v 110, cst 62, R 439): +1.03% before its splits.  About 400
      splits would cancel this.  Dead end.

**Lever inventory vs P111-tuned (session 6d; exact pricer unless marked).**

| lever | size if available | status |
|---|---|---|
| new unit, h = 9 root-like | - | impossible (<= 127 lines, needs 130+) |
| decoder constant | +2.8% per unit | E8 floor 72 - #punctures conjectured; P111's 63 likely optimal in the format |
| double-star decoder (cut at partner line) | P110 <= +0.26%; P102 +11% model | needs a cut format; P110 blocked by 49 phase-B conflicts; P102 needs R <= 408 |
| twin / trivial ports | - | doubled-E8 minrank 18 (SAT); trivial ports -0.68% each |
| stage count | - | 9 optimal (K = 3 wall, K = 5 -1.3%) |
| unsplit idle stretches / any other K = 4 schedule | +6.13% ideal; <= +0.67% at 9 stretches | **closed for K <= 4** (6e): uncoupled bridges, splits, passive pairs, parallel levels all searched or proven; every feasible layout <= B_K's. K >= 5 open (B_5 -1.30%) |
| helper entrance rank (width 8 - e) | up to +23% (MILP, all 438 width 7) | **one helper done: E1 rank 2, +0.0604% (official chain)**; all other conversions closed on P111-tuned/E1 (6f: #434 criterion, any-time injection, rescheduled A, frame cascades all 0) |
| non-partition E8 skeleton (free top) | full E8 beats P111-tuned iff R <= ~382 | route-level bound running (`scratchpad/cellb/routefree.py` on fgd4_1_0/1_3) |

**Session 6e (2026-10-16): schedule space reopened and closed again; banks; parallel levels.**
- `code/sched/schedule_checks.py` reproduces the session-6d schedule numbers.
  - The shipped recipe composes to the identity.
  - Unsplit stretches: +6.13%.
  - Coupled junction-only searches: 0 solutions.
  - Independent triples: hosting wall at 9 stages, -69% at 12.
- **Correction to 6d.**
  - The 6d closure ("split-free needs 3-shear signed swaps") assumed coupled bridges diag(A, A^-T).
  - X -> X and Y -> Y additions are separate gates, so a junction may apply diag(A, B) with A, B independent.
  - With uncoupled junctions, split-free schedules DO exist:
    - K = 2: 8 of 15 canonical pair sequences, e.g. (0,0,1,0,0) and (0,1,0,1,0), all F R F R F;
    - K = 3: 50 of 301, e.g. the hub (0,0,1,0,2,0,0) with integer SL2 junctions, verified anti-diagonal with
      unimodular blocks.
  - They are not better:
    - the best K = 3 slot multiset is B_3's own (28, 28, 14, 14, 7, 7);
    - the K = 4 hub (0,0,1,0,2,0,3,0,0) has exactly B_4's multiset (+0.00%).
- **Exact F_2 test (rigorous).**
  - An integer schedule reduces mod 2 to an F_2 schedule with GL2(F_2) junctions.
  - Over any field, rk(XX) + rk(YY) starts at 2K, ends at 0 and changes by <= 1 per local, and the first local
    cannot lower it.  So with 2K + 1 locals every later local lowers it by exactly one.
  - Exhaustive BFS over F_2 (`scratchpad/sched2/feasp2.py`) is therefore a complete necessary test for integer
    schedules, and exact for the F_2 payload of the bit contract.
- **Invariant theorem (proven, any field, any bridges: coupled or not, junction or split).**
  - Put U_X = span of the x-parts of the X rows, W_X = span of the x-parts of the Y rows, and I(X) = dim(U_X ∩ W_X).
    Define I(Y) the same way.
  - A reducing R needs I(X) >= 1 and lowers it by exactly one; it raises I(Y) by at most one.  The same holds with
    X and Y exchanged for F.  Transforms diag(A, B) on any set of pairs leave U, W and I unchanged.
  - The first local leaves I(X) + I(Y) <= 1, and every later local keeps it there.
  - Consequences:
    - locals strictly alternate F R F ... F;
    - **two locals can never share a level.**
  - This kills the "parallel level" lever.  2K + 1 invocations on L < 2K + 1 levels would keep D = T(2Kv - s cst)
    (mass identity checked) while m = 1 + L a shrinks: hypothetically +12% at L = 8, +15.6% at L = 7, +30% at L = 5
    (`scratchpad/sched2/parprice.py`, banks included).  Impossible: L = 2K + 1.
  - Enumeration confirms it: K = 2, L = 4 has 0 feasible programs (`levelp.py`, `levelall.py`).
- **Banks (pricing correction).**
  - Unhosted residuals on bank streams cost only their local runs: a bank adds m to mW and its coordinates are the
    local helper climbs.
  - Overflow beyond the hosting wall is therefore legal at reduced value.  The 6d "K = 3 hosting wall" is really
    -1.77% with banks (B_3 split slots), and K = 2 is -8.8% (`scratchpad/k3/banks.py`).
  - Check: K = 4 with all residuals banked gives 1.6185e-3, matching format-limits A.5 step D (1.6183e-3).
- **Stretch-count pricing (unchanged local word, K = 4).**
  - Hosting per port copy is 27 - (#stretches) whenever every stretch is <= 8 stages.
  - So >= 10 stretches always lose, even with banks: best -1.46% at 10, -3.48% at 11.
  - With 9 stretches (B_4 has 9) the best conceivable multiset is (49, 49, 49, 7 x 6) at +0.67%.  B_4 sits at 0.00%.
  - A pair active only at stage 0 is impossible: its rows freeze after junction 1 with a nonzero x-part.  So no
    56-stretch exists.
  - K = 5 serial: the best 12-stretch multiset is +0.01%; B_5 is -1.30%.
- **K = 4 junction-only (uncoupled), exhaustive over F_2: closed.**
  - Checked: all 3,236 canonical pair sequences whose slot multiset prices >= 0 (`scratchpad/sched2/runp2.py`,
    6 min).
  - Exactly 4 are feasible:
    - (0,0,1,0,2,0,3,0,0), (0,0,1,0,2,0,3,3,0), (0,1,1,0,2,0,3,0,0) and (0,1,1,0,2,0,3,3,0);
    - all are hub patterns with exactly B_4's multiset (42, 42, 28, 28, 14, 14, 7, 7, 7), +0.00%.
  - So uncoupled junction-only schedules cannot beat P111-tuned.  This is rigorous for integer schedules too
    (reduction mod 2).
  - Split-allowed layouts are being searched exhaustively over F_2 with a C engine (`scratchpad/sched3/splitc3.c`
    plus `drive.py`: <= 3 splits, <= 1 per time, canonical forms).
  - On the B_4 shape (0,0,0,1,1,2,2,3,3) all 23 feasible split sets are found.  The best is B_4's own placement
    (+0.000%); the others run -0.04% to -0.30%.
  - **Complete over the candidate list (one split per boundary).**
    - Candidates: every K = 4 sequence with a positive split option that passes the touch-time theorem; no-split
      options are already excluded by the junction-only enumeration.  That is 377 sequences, 80 min on 4 cores.
    - 49 are feasible: 44 reach exactly B_4's multiset (+0.000%) and 5 reach -0.159%.  None is positive.
    - Two splits at the same boundary need GL4 transforms (`splitc5.c`, `drive_double.py`).  Over 94 sequences,
      2 are feasible, both at +0.000%.
    - So every K = 4 schedule with all four pairs active tops out at B_4's layout.
  - **Passive pairs (new).**
    - A pair that is never active but is touched by splits is algebraically possible:
      - K = 2: (0,0,0,0,0) with pair 1 split at boundaries {1, 3};
      - K = 3: (0,0,1,0,0,1,0) with pair 2 split once, at boundary 3.
    - The touch-time theorem still applies.  These layouts were missing from the candidate lists above.
    - K = 4 passive-pair candidates (`splitlist3.py`, then interval-filtered): 397 sequences, searched with
      `splitc6.c` (subset pruning against the allowed split sets, up to 3 splits per boundary).  26 are feasible,
      all exactly at B_4's multiset.
    - Passive pairs need >= 2 touches, so stretches = splits + (#passive) + ... allows up to 6 splits when only one
      pair is active.  These 39 extra sequences (`splitlist4.py`, 4,277 options) are being searched;
      13 feasible so far, all at B_4's multiset.
  - **K = 3 closed (rigorous).**
    - Every positive candidate (active pairs 1-3, any splits, passive included, touch-time plus interval
      filters): 16 sequences, all INFEASIBLE over F_2.
    - Every multiset with >= 6 stretches is negative under the rigorous upward-relaxed pricer (all slots fully
      hosted, exact deficit): the best is -1.49%.
  - **Rigorous stretch-count pricing** (upward-relaxed hosting, exact deficit; merging stretches never lowers the
    price):
    - K = 4: >= 10 stretches <= -0.97%;
    - K = 5: 12 stretches <= +2.04%, 13 <= +0.25%, 14 <= -1.46%.
  - **K >= 5 is open.**
    - B_5 is -1.30%.  Beating P111-tuned needs a K = 5 layout with <= 13 stretches distributed far better than
      B_5's.  No such layout has been seen for K <= 4.
    - The merged-middle bound (touch-time theorem plus the interval-lemma cap 2K - 2 on any stretch) is too weak:
      K = 5 <= +7.31%, K = 6 <= +7.53%.
    - Closing it needs the K = 5 layout search.  The engine `scratchpad/sched3/splitk.c` handles K <= 6; the
      candidate generator is not written yet.
  - **Interval lemma (proven).**
    - Statement: if d pairs are untouched during g consecutive stages b1..b2-1, then g - [b1 = 0] <= 2(K - d).
    - Proof: the dormant rows are frozen, so Phi(b1) <= Phi_D + 2(K - d) and Phi(b2) >= Phi_D, and Phi drops by
      exactly one per local except the first.
    - Effect on the candidates: all-active 377 -> 289 sequences, double split 360 -> 84 options, passive
      14,371 -> 3,915 options (397 sequences).  The best surviving potential is still +3.73%, so the F_2 searches
      remain necessary.
- **Touch-time theorem (proven).**
  - Φ = 2f + Φ_t, where f counts the untouched ("fresh") pairs, whose rows are unit vectors in coordinates nobody
    else uses.
  - If Φ_t = 0 while f >= 1, then U_X and W_X live on disjoint coordinates, so I(X) = I(Y) = 0 and no later local
    can reduce.
  - Since Φ = 2K - b + 1 after stage b - 1, the k-th pair to be touched (in touch order, k = 0..K-1) is first
    touched at boundary <= 2k.
  - Over F_2 the reversed schedule is again a schedule (F, R and transforms are involutions or invertible).  So the
    k-th pair counted from the end is last touched at level >= s - 2k.  For integer schedules, reduce mod 2.
  - Hence the pre-stretches, sorted, are <= (2, 4, ..., 2K - 2), and the post-stretches too.  B_K attains every
    bound with equality and adds K - 1 middle stretches of length 1.
  - Any better layout would have to fit the forced >= K - 1 units of middle idle into fewer, longer middle
    stretches.  No feasible example has been found.  Conjecture: >= 3K - 3 stretches always, which would make B_K's
    multiset optimal by majorization.
- **FRONTIER BEATEN (session 6e): one entrance-rank-1 helper on P111-tuned, c = 0.0017343471029 (+0.0531%).  Current
  best (session 6f): the same helper at entrance rank 2, c = 0.001734473240795253742474 (+0.0604%), official chain;
  package `research/e8-bit-p111-e1/`.**
  - **Mechanism: double-read dirt cancellation.**
    - Helper 248 (register 470) has one write, A[230] `h248 += x77` at the line frame 79 (line 77).
    - It has one reader, A[1993] `h222 += h248` at the same frame (the tuner's "hoist").
    - Change: start h248 at frame 79 and insert an early gate `h222 += h248` at frame 79 right before A[230].
    - The dirt of h248 now enters h222 twice and cancels, so h248 leaves D; D loses 470 in 55 target gates and
      nothing else.
    - h222's chain is unchanged (79 is already its first frame).  C is rebuilt as the literal reverse.
    - h248 loses its 0 -> line rank-1 run, so the local profile is {1: 1322, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11,
      7: 19}, mass 5128 = 8R - 1 + 63 + 14v.  Its residual width is 8 - 1 = 7.
  - **Checks.**
    - Exact F_2 replay on all 661 columns with 439 dirty helpers symbolic: PASS.
    - H1-H5 and U / J = I / K = D / C = U^-1: all hold.  This uses `xcheck_e1.py`, which is xcheck_p.py with one
      relaxation: a helper that D does not read may start above frame 0.
    - #543's lemma uses frame 0 only for "every register D touches".  Entrance ranks are the #434 mixed-width
      residual wrapper (w = 8 - entrance rank).
  - **Price.**
    - Exact window-aware hosting MILP (`scratchpad/ent1/hostwin.py`, SCIP optimal): every residual of call i
      goes into a slot whose window contains i, using the nine slot types {p0 post 42 [3-8], p1 pre 14 [0-1],
      p1 one-level 7 [2], p1 post 28 [5-8], p2 pre 28 [0-3], p2 one 7 [4], p2 post 14 [7-8], p3 pre 42 [0-5],
      p3 one 7 [6]}, followed by the exact root.
    - Control: it reproduces P111-tuned's c = 0.0017334270395898443 exactly.
    - E1: c = 0.0017343471029, **+0.0531%**.  Remainders per replica: {42: 10, 2: 434, 6: 442, 7: 663, 5: 2, 4: 442};
      three of the nine width-7 residuals fill one-level 7-slots.
    - #1023's slot model, which skipped the timing check, gave +0.068%..+0.082%.
  - **Upgraded to entrance rank 2 (session 6f): c = 0.001734473240795253742474 (+0.0604%), official chain.**
    - The three gates on 470 (the inserted read, A[230] and A[1993]) move from frame 79 to frame 186 = span(root 33,
      root 77), which is A1xA1 and x77's next frame; 470 starts at 186.  Width 6.
    - Profile {1:1321, 2:1344, 3:78, 4:44, 5:102, 6:12, 7:18}, mass 5127.  xcheck_e1 PASS.
    - Frame 186's isometry has 30 dyadic route factors (cap 77).
    - Needs `global_k --no-banks` plus `emit_k --host-all`: in the default mode one stage leaves {6: 32} for banks,
      and that has no exact width-64 tiling.
    - The MILP (`code/price_e1.py`, general widths) gives the same c.  This is now the package's word; verify.sh
      passes.
    - Eleven stages (PR #493's chain via PR #545's adapt): c11 = 0.001712057989263075621738, +0.0646% over
      P111-tuned's eleven-stage price.  This needs a mixed-width nominator (`code/host11_e1.py`) and
      `local_audit.py` edits that drop the all-zero-entrance asserts.  The audit passes and the outer assembly is
      47/47.
    - Exit/cleanup retiming for 470 would end it at its entrance frame 186, which is equivalent to removing helper
      470 (444 reads x77 directly at 186 at A[1994]).  That is helper deletion, which the user's rules say not to
      pursue, so it was not pursued.
  - **Official chain confirms it (session 6f).** Package: `research/e8-bit-p111-e1/` (README, verify.sh,
    EXPECTED.json); `bash verify.sh DIR` passes end to end in about 100 s.
    - PR #510's nine-stage chain (parameterised by P111's adapt9p.py, hosting programme with `--discover`) gives
      **c = 433586775730751599903/(2.5·10^23) = 0.001734347102923006399612**.  This is exactly the MILP value.
    - Hosted audit PASS: 126432/126432 residuals hosted whole, 0 banks.
    - Official C++ legality and columns_h / columns_k accept start frame 79 natively; rank mass 5128.
    - Three listed adaptations:
      - frame 79 = root (0,1,0,-1,1,0,1,0) is not a coordinate root, so its isometry needs a route factor (17
        dyadic factors).  The vendored validator allows swaps only; `isometry_e1.py` also replays scale/add factors,
        capped at 77 (the geometry's max_route_factors, already charged in assemble9's selector bill);
      - `--no-banks`, because exact width-64 bank tiling needs ENT even (32·(8R−ENT) ≡ 0 mod 64), and every
        residual is hosted anyway;
      - the selection discovered by the hosting programme.
    - The control run of P111-tuned's own verify.sh reproduces 0.001733427039589844234749.
  - **Scaling the lever on this word: closed (exact, session 6f; `code/entrance/`).**
    - Slot-model value if it scaled: 10 / 100 / 438 width-7 helpers give +0.57% / +6.1% / +23%.
    - #434's time-0 donor criterion: 0/438.  At most 6 eligible donors per helper; K has rank 111.
    - Dual-set injection at any time, `g += S_h(p)`, where S_h(p) is the unique register set summing to e_h, with F
      any listed frame nested for g and all of S: 0/438.  Only 2-9 distinct frame-compatible alpha per helper.
      Predictions were verified against forward replay.  This required fixing a stale-alpha bug at the scatter.
    - An earlier "437 convertible" span count was a bug: it allowed reads of h below its entrance frame.
    - **Rescheduling A (any topological order of the touch DAG) in the regime S = {p} ∪ sources: 0/438**
      (`code/entrance/relax3.py`).  The bound is DAG-constrained: an injection lies between g's touches k, k+1, p's touches
      j, j+1, and each source's chain positions, with no path from successors to predecessors and pairwise checks
      only, so it is an over-approximation.  An earlier "17 pivots" came from a bug that accepted source positions
      after a B touch; `multi5.py`, the real constructor, converts 0 of those 17.
    - Why (inspection): helpers sit in mutual-addition elimination networks (a += b, b += a at D4 block frames).
      Their readers are read before they read the pivot, and many helpers are read directly by targets in B, where
      only the frame-0 D pre-read can cancel.
    - Scripts: `code/entrance/` (multi3/4/5, relax3, raise, cascade, span, pricew, splitval; they read the E1
      word from `research/e8-bit-p111-e1/data`).  `span.py` and `multi.py` are superseded: the first allowed reads
      below the entrance frame, and the second is the fixed-schedule pure-window version.
    - Open: a new A-section plan in which a pivot's readers are untouched helpers whose first frame contains E_p,
      read p before being read themselves, and with no target reading p.  Then k_p = Σ k_readers, which is #434's
      relation, automatically.
    - Reader census on E1: 225 helpers are read directly by a target, so only D can cancel them.  Of the other 214,
      only 470 (E1), 462, 467, 469 and 444 have one reader.  Example of the geometric block, pivot 462 (h240, line
      47): its reader h127 has chain {58} -> {48,58} -> D4 block 506, and source x47 has {47} -> {47,58}.  No common
      frame exists before 506, and an uncompute/recompute variant fails at x47's next frame.
  - **Frame-only coordinated moves on E1: none (exact, `code/entrance/cascade.py`).**  Merge two consecutive frame segments
    of one register, cascading forced lifts forward or forced lowerings backward:
    - upward, 2360/2360 infeasible: 1483 hit a target's t-perp in B, 549 D, 328 a retained total's COPY gate;
    - downward, 2360/2360 infeasible: 2333 reach a source's start line, 27 fixed gates.
    - The frame chains are rigid between the source lines and the target, retained-total and D bounds.  PR #589's
      tuner (transports, Steinberg, frame passes) also finds 0 moves on E1.
  - **Raised entrance (session 6f, `code/entrance/raise.py`): 0/438.**  Lift a pivot's first gate to any listed frame F'
    between the join of its operands' current frames and the meet of their next frames.  F' must have an orthogonal
    live-root basis (any rank).  Then use pure-window donors with gc <= F' <= gn: k_p is never in the span.  (This is
    the move that gave 470 rank 2.)
  - **Lead, format-level and conditional: charged residual splits on bit (`code/entrance/splitval.py`, with `pricew.py`).**
    - Format-limits C.8 (#451's trace obstruction) says an exact split w = a + b needs a cross-term repair of at
      least min(a, b) doubly paid coordinates, one helper per piece, or a new priced hub primitive.
    - Mass-consistent model of a 7+1 split with the minimal repair: the pieces occupy 7 + 1 + 1 cells and add one
      local rank-1 child per split per call (local +1, idle −1, so the deficit identity holds).
    - Exact window-aware MILP on P111-tuned:

      | splits per call | 10 | 50 | 100 | 150 | 200 | 300 | 439 |
      |---|---|---|---|---|---|---|---|
      | c vs P111-tuned | +0.50% | +2.52% | +4.84% | +7.07% | +7.93% (feasible, not proven optimal) | +5.85% | +3.09% |

    - That is about 10x the complex-side estimate (C.8: <= +0.67%, uncharged), because bit remainders are
      fragmented into 2/4/6/7-cell leftovers.
    - Not a construction: it needs a proven split primitive, and the true repair cost may exceed the lower bound.
      An earlier version of this model that broke the mass identity priced at -27%, so model mass consistency
      matters.
  - **Exit rank for E1's h470: no.**  Its dirt column is now clean (only 470 holds e_470 after B).  But its inverse
    row (the dual set at the end of B, 10 registers) has end-of-B frames spanning all 8 dimensions.  The bit chain's
    global_k also asserts full final frames for helpers.
- **Rank-7 helper ends (exit rank) on the bit word: not applicable to P111-tuned as built.**
  - The complex side has rank-7 helper ends: AlexS's #1030, ported to k8 by #1090; see
    `research/complex-rank7-end-pair/PROOF.md`.  A helper may end in a dimension-7 subspace U when:
    - its dirt column in the raw word has only the diagonal entry;
    - the end-of-B frames of its inverse row (in U^{-1}) span U;
    - then an early cleanup gate at U restores it, and its residual width drops 8 -> 7.
  - On P111-tuned (`scratchpad/exitr/exit2.py`):
    - only 9 of 439 helpers have clean dirt columns;
    - inverse rows have 3-27 registers;
    - their end-of-B frames span all 8 dims for every helper.
  - So there are 0 candidates without restructuring phase B.  A first cruder census (span of all A/B partners) also
    gave 0.  Width-7 headroom for PR589 was priced by #1023, but no narrower bit helper exists yet.
- **Helper budget for a new E8 skeleton (exact pricer, `scratchpad/budget/budget.py`).**
  - Setup: v = 111, cst 63, P111-tuned's data and copy runs, every helper with the same run pattern, whole hosting
    plus banks.
  - P111-tuned's helpers have 2,159 runs per local word ({1: 996, 2: 1041, ...}), 4.9 per helper.
  - Break-even helper counts:

    | helper runs (ranks) | break-even R |
    |---|---|
    | 2 runs: (1,7) / (2,6) / (4,4) | 642 / 597 / 568 |
    | 3 runs: (1,2,5) / (2,2,4) / (2,3,3) | 529 / 505 / 498 |
    | 4 runs: (1,1,2,4) / (1,2,2,3) / (2,2,2,2) | 478 / 463 / 454 |
    | 5 runs: (1,1,2,2,2) | 432 |
    | 8 rank-1 runs | 374 |

  - A redesign must therefore trade stops for helpers at about these rates.  A telescoped hub tree (2-3 runs per
    register) needs carriers for each line's first-appearance antichain and lands at ~600-800 registers (estimate).
- **Non-partition E8 free-top route bound** (`scratchpad/cellb/routefree.py`, 5,000 s CP-SAT): inconclusive.
  - fgd4_1_0: best sum j_C = 120, lower bound 15.
  - fgd4_1_3: best 120, lower bound 45.
  - R >= 2v + sum j_C gives only R >= 255-285, while full E8 needs R <= ~382 to beat P111-tuned.  Not closed.

**Session 6g (2026-10-16): line-count ceiling for root-like systems (inertia bound), larger-system searches.**
- **Theorem (proven; exact check `code/inertia/inertia_bound.py`, 4 s).**
  - Setting: a root-like system in a real quadratic space of signature (p, q), h = p + q, i.e. vectors with
    <u, u> = 2 and pairwise products in {0, +-1}.
  - Bound: v <= pi, the positive index of inertia of Phi(a, b) = <a, b> - (1/4)<Ta, Tb> on Sym^3(V), where T is
    the metric contraction.
  - Proof: Phi(u^3, w^3) = <u,w>^3 - <u,w> is 6 on the diagonal and 0 off it, so the u_i^3 span a Phi-positive
    subspace of dimension v.
  - Closed form, from Sym^3 = ker T (+) im T*, T T* = (h+2)/3, and Phi = kappa(1 - kappa/4) on im T*:

    | h | Lorentzian bound C(h+1,3) + (h-1 / 0 / 1) | attained or best known |
    |---|---|---|
    | 9 | 128 | the 6d case analysis gives 127; E8-type 120 |
    | 10 | 165 | **165 = I_{10,1}, attained** |
    | 11 | 221 | 220 = I_{11,1} |
    | 12 | 287 | 286 = I_{12,1} |
    | 13 | 365 | 364 = I_{13,1} |
    | 16 | 681 | 680 = I_{16,1} |

    The middle term is h-1 for h < 10, 0 at h = 10 and 1 for h > 10.  The Euclidean bound C(h+2,3) (h < 10) gives
    E8's 120 at h = 8, attained.
  - The script checks every closed form by exact rational inertia, and checks Phi(u_i^3, u_j^3) = 6 delta_ij on
    I_{10,1}, I_{11,1} and E8 (written as w-perp in I_{8,1}, w = (1^8; 3) timelike).
  - **Consequence: the I_{n,1} family is the largest root-like Lorentzian system at every window, up to one line.**
  - The 6c break-even grid needs, with h totals at rank h-1 and an R420-quality middle (rel / abs):

    | h | v needed (rel / abs) | ceiling |
    |---|---|---|
    | 10 | 172 / 180 | 165 |
    | 11 | 225 / 242 | 221 |
    | 12 | 290 / 324 | 287 |
    | 13 | 369 / 434 | 365 |
    | 14 | 467 / 585 | 456 |
    | 16 | 725 / 1093 | 681 |

    At h = 9 the need is 130 against a ceiling of 128.  Extended (`scratchpad/lor6/tie_big.py`, same model, rel),
    need vs ceiling:

    | h | 15 | 17 | 18 | 19 | 20 | 21 | 22 |
    |---|---|---|---|---|---|---|---|
    | need | 582 | 901 | 1,123 | 1,408 | 1,779 | 2,280 | 2,983 |
    | ceiling | 561 | 817 | 970 | 1,141 | 1,331 | 1,541 | 1,772 |

    The abs model has no tie at all from h = 21.  The gap widens with h, so 9 <= h <= 22 is covered and larger
    windows are worse.
  - So **no root-like Lorentzian system reaches the tie line in the #620 model**, whatever its construction.
  - The remaining loopholes are a decoder cheaper than h(h-1) on a near-extremal system, and systems that are not
    root-like (other norms, odd products of size >= 3, or abstract-class representations).
    - For a decoder at h = 11 and v = 220-221: cst <= 107-108 instead of I_{11,1}'s exact optimum of 110.
    - At h = 12 and 287 lines: cst <= 130.
    - The margins at h = 12-13 are about 1%, inside the model's own error.  The model also assumes an R420-quality
      middle, which for these loads (|R(t)| ~ v/2) is itself optimistic.
- **Exact B0 decoder costs (matroid greedy over all 2^c - 1 codewords, real rank of each support;
  `scratchpad/h10/deccost.py`):**

  | system | lines | F2 rank c | cst | x |
  |---|---|---|---|---|
  | I_{10,1} | 165 | 11 | 99 | 0.600 |
  | I_{11,1} | 220 | 11 | 110 | 0.500 |
  | I_{12,1} | 286 | 13 | 143 | 0.500 |

  - At even n the P lines form an extra codeword (weight C(n,2)).
  - The 220-line system that CP-SAT found at h = 11 (by y: 55 / 109 / 56) has the same weight distribution and cost
    as I_{11,1} (110).
- **Larger-system searches (heuristic, superseded by the theorem):**
  - CP-SAT max clique, h = 11, w-perp pool with y <= 2 (682 lines): best 220, bound 230.  With y <= 3 (2,013
    lines): best 220.
  - DLS max clique over other even lattices at h = 10 (w = (1^10;1), (3,1^9;3), (3,3,1^8;3); y <= 2): 120, 120, 86,
    all below II_{9,1}'s 165.
- **Systems that are not root-like (heuristic searches, exact decoder costs):**
  - Odd-or-zero pool at h = 11 (`scratchpad/mixn/poolmix.py`; w-perp of I_{11,1}, |x_i| <= 1, |y| <= 3, norms
    2/4/6, 17,358 lines): DLS max clique gives 220 in 3 seeds x 400 s.  Every best clique is root-like (norm 2
    only), either I_{11,1} or its y = 0/1/2 image.
  - The 298-line h = 12 system (220 T + 66 P + 12 norm-6 vectors (-1^11, 2; -3); products 0, +-1, +-3) has an exact
    min-cost B0 decoder of 155 (c = 13), x = 0.520.  That is worse than I_{12,1} (0.500); the 6c range "0.48-0.52"
    resolves to its top end.
  - **Every line compatible with all of I_{n,1} (exact, `scratchpad/ext/extras.py`).**
    - Odd-or-zero products with every P(ij) force x to take at most two values a, b with a - b odd.  The T
      products then leave only a few cases.
    - n = 11: exactly 11 extra lines N_a = (1^10, 2 at a; 4), norm -2 (timelike), products 0/+-1 with I_{11,1} and
      -3 among themselves.  This is the "231 abstract" system.
    - n = 13: none.
    - n = 10: 11 extras (10 of norm -4, (3 at a, 2 elsewhere; 7); one of norm -10, (3^10; 10)), all mutually
      compatible.  The 176-line system has exact cost 110, x = 0.625 (I_{10,1}: 0.600).
    - n = 12: 91 extras (norms 6, -4, -12).  The largest compatible set has 13 (CP-SAT optimal: the 12 norm-6
      (-2, 1^11; 3) plus the norm -4 (1^12; 4)).  The 299-line system has exact cost 156, x = 0.522
      (`scratchpad/ext/extend_all.py`).
    - n = 14: extras of norms +-20 and -70 exist (not costed).
    - In every case each extra line costs one decoder unit, so extending I_{n,1} never lowers x.
    - The 231 system has c = 11, but each extra line enters one D10 total and makes it full rank: exact min cost
      121, x = 0.524.  Each extra line costs exactly one decoder unit, so (110 + k)/(220 + k) > 0.5: no gain.
  - **h = 9, not root-like** (`scratchpad/mixn/poolgen.py`; w-perp of I_{9,1}, characteristic w, |x_i| <= 2,
    |y| <= 3-4, odd-or-zero products; DLS 240-300 s):

    | pool | w | norms | lines | best clique |
    |---|---|---|---|---|
    | 1 | (3,1^8; 3) | +-2 | 2,416 | 120 (E8, root-like) |
    | 2 | (1^9; 1) | +-2 | 13,680 | 113 |
    | 3 | (3^3,1^6; 3) | +-2 | 4,358 | 67 |
    | 4 | (5,3^4,1^4; 5) | +-2 | 3,608 | 86 |

    - No vector of the (3,1^8; 3) pool with norms +-2/4/6 (20,806 lines) is compatible with all 120 lines of
      that E8 (exact), so E8 does not extend at h = 9 inside the pool.
    - Nothing approaches the 130 that h = 9 needs.
  - **h = 8 Lorentzian (signature (7,1); same m as E8, so no window penalty).**  The root-like ceiling is 91
    (theorem).  Odd-or-zero pools with norms +-2 (w = (1^8; 1), (3,1^7; 3), (3^2,1^6; 3); 1-5k lines) give DLS
    best 69, 70 and 49.  A 22,722-line pool with norms up to +-6 was too large for DLS (37).  Nothing near the 111
    lines that P111 has.
  - **Exact stop map for I_{11,1}** (`scratchpad/lor6/stopmap.py`; even splits; sources ks, targets kt, helpers
    kh stops; break-even R vs P111-tuned):

    | kh (helper stops) | 2 | 3 | 4 | 5 | 6 |
    |---|---|---|---|---|---|
    | break-even R | 851 - wall | 711-828 | 650-757 | 609-709 | 580-675 |

    The range spans ks 1-3 and kt 2-4.  Two-stop helpers cannot share: each read pushes the read register, so a
    source feeds hubs at <= ks frames while its value must enter about 90 incomparable rank-9 sections.  Real
    designs therefore sit at E8-like 4-5 stops, where R must be <~ 650-750.
  - Mixed-sign root-like systems (norms +-2, products 0/+-1; `scratchpad/mixn/poolrl.py`, |x_i| <= 2,
    |y| <= 4):
    - h = 11 pool: 6,644 lines, of which only 11 are timelike (the N_a); DLS best 221 = I_{11,1} + one N_a, since
      N_a.N_b = -3.  Its decoder costs 111 (x = 0.502).
    - h = 10 pool: 1,575 lines, none timelike; DLS best 165.
  - E8 plus twins (same F2 class) at rank 9-10 (`scratchpad/h9b/twins.py`, equality-only LM with an E8 control that
    passes at rank 8):
    - (8,1): residual^2 about 2.67 per twin (2.67, 5.33, 10.7, 21.3, 32.0 for 1, 2, 4, 8, 12 twins).
    - (9,0) and (9,1): exact up to 2 twins, then 5-21.
    - Analytically, with the E8 part rigid a twin must lie on the normal of R^8 and so is orthogonal to everything.
      Twins therefore cannot carry E8's middle into a 130+-line unit at h = 9.
- **Optimistic ceiling of I_{11,1} (exact pricer, `scratchpad/lor6/optbe.py`).**
  - Setup: minimal stop counts; sources one climb 1 -> 11; targets 0 -> t-perp in 1 or 2 climbs; helpers
    0 -> 11 in 1 or 2 climbs; 11 copies of rank 10; mass identity exact.
  - Every R up to the hosting wall (880) beats P111-tuned, for every split tried.
  - At the all-word floor R = 426 the price would be c = 0.0025-0.0029, against 0.00173.
  - So the potential is large, and the binding constraint is how many stops the sharing needs.
    - R420 runs about 4.5 children per register.
    - At 3-5 stops the break-even falls to about 650-840 (6c budget).
  - The open question is exactly a design with R <~ 700-840 at E8-like or cheaper stop counts.
- **New lever: entrance-ranked in-chain nodes (E1's double read, generalised; pricing exact, design open).**
  - **Mechanism.**
    - A helper N that D does not touch may start at its home frame E (the xcheck_e1 relaxation).
    - Every register that reads N must also read it once while N is still empty, at E, before N's first write.
      N's dirt then enters each reader twice and cancels.
    - Every reader of N must therefore pass through E in its chain, so N serves only in-chain readers.
    - N's own writes (its injections) must happen in phase B, after its readers' pure reads.  The format allows
      this: B z-gates are legal and C reverses them.
    - N then has width h - rank(E) and climbs E -> 11 in 1-2 steps.
  - **Price (exact pricer, best-fit mixed-width hosting calibrated against `pricer.price`;
    `scratchpad/lor6/entmap.py`, `mixbe.py`, `cstbe.py`).**
    - All helpers entering at rank e:

      | e | stops after entrance | break-even R |
      |---|---|---|
      | 0 | 2 | 872 |
      | 3 | 3 | 1,104 |
      | 5 | 2 | 1,475 |
      | 7 | 2 | 2,119 |

    - Mixed population: 440 frame-0 carriers (5-6 stops), sources with 3-5 stops, targets with 2-3, plus nodes at
      e = 5-9 with one stop.  Break-even allows H = 580-1,920 nodes.
    - The decoder must stay near 110-121: at cst 121, H <= 390-740; at cst >= 132 nothing breaks even.
  - **What binds then.**
    - Node registers become cheap; carriers (frame-0 registers injecting line values into nodes) and their
      chains do not.
    - Each injection of a line at a node reaches only the chains through that node: about 60 at rank 2, about 15
      at rank 8, 1-3 at rank 9.
    - A target's own chain reaches at most a rank-9 shared frame (<= ~65 lines of R(t)); the remaining >= 53
      lines need proxies, i.e. consumed frame-0 registers, which can be the 2 exit helpers per line.
    - Rough fan-out count: about 25 injections per target, ~5,500 in total, against ~2,000 that 660 carriers
      (sources + exit helpers, ~3 nested injections each) can make.  **Estimate, not a bound.**
  - Worked count (exact arithmetic; D/E hierarchies of I_{11,1}).
    - Readers of "lines on W" (|W| = k >= 4) are exactly the P(xy) with x, y outside W: C(11-k, 2) readers.
    - Readers of D_k(p, W) are T(p,x,y) and P(x,y) for x, y outside W u p: 2 C(10-k, 2) readers.  So D8(p,S) has
      2 readers, D7 6, D6 12, D5 20, D4 30.
    - The cheapest telescoped trees still pay at their exclusive leaves.  For P targets (E8(M) totals via
      "lines on W", W growing to the 9-set M) the leaves alone need 55 x C(9,2) = 1,980 injections; all levels
      together about 2,650.
    - T targets via D8 chains pay >= 14 new lines per D8 node at fan-out 2, about 21 per target, i.e. about 3,500.
    - Together these are far above the ~2,000 injections that ~660 carriers can make at ranks 7-9.
    - Caveat: multi-stop nodes can aggregate along their own chains, provided all their readers pass through the
      node's entrance frame.  That can move injections to lower ranks; it is not modelled here.
    - Aggregation check (format rules, structural argument; not a word-level bound).
      - Suppose node N must hold content assembled off its reader's chain (frames below G that are not on the
        reader's chain).  Then the reader's pure read has to precede N's first write.  Done at a frame below G,
        it requires the reader to pass through N's entrance frame; done at G, it pushes N to G before N can
        collect anything.
      - Such "top-step" content therefore needs frame-0 aggregators or carriers, i.e. the carrier budget.
      - In I_{11,1} the top step of a D8(p,S) leaf is the star of the last point: 7 cells
        {P(xj), T(xja)} at incomparable rank-2 frames, with only 2 readers.  Sections are no better: e.g.
        {T(abc), P(bc)}-perp n lines = D8(a,S) exactly.
      - This needs >= ~495 frame-0 aggregators plus their carriers, against a frame-0 budget of ~600 that the
        exit helpers already use.
      - So the entrance lever does not rescue I_{11,1} (structural count, not a word-level proof).
      - Refinement: dirt cancels for any two reads of N by the same reader ("differential" reads; the reader gets
        N's content change in between).  An entrance-ranked aggregator can therefore collect off its readers'
        chains, provided every reader passes through its entrance frame (pure read there) and its final read
        frame.  Many aggregators can share one entrance frame.  This removes the "must be frame-0" step above,
        but not the fan-in limit: a chain contains one frame per rank, so k incomparable cell frames still need
        about k pushed registers.  The I_{11,1} D8-leaf count stands.
  - **Conversion test on the best verified I_{11,1} word** (`scratchpad/lent/convert.py`, exact timeline replay of
    word_blkA4).
    - Rules: entrance frame = the helper's first-write frame; each helper reader needs a pure read before that
      write, at a point where its frames nest; no dirt leak in between; D reads of the helper are dropped.
    - Result: 16 of 3,656 helpers convert (ranks 2:6, 3:2, 4:1, 7:4, 8:3).  397 are read by targets (written in
      phase A, so they cannot be pure-read first), 11 are retained, and 3,232 fail on reader frames or timing.
    - The cause is structural: carriers' first writes sit at single-line frames, and a reader's chain contains
      only one rank-1 frame.  The lever needs a design built for it, not a retrofit.
  - **I_{13,1} with the lever: the strongest Lorentzian candidate (model).**
    - Break-even R (all helpers at entrance rank >= 1, 4-5 stops): I_{11,1} 870-1,010 (3.5v = 770); I_{12,1}
      950-1,040 (1,001); I_{13,1} 1,400-1,535 (1,274); I_{15,1} 2,000-2,190 (1,960).
      (`scratchpad/lor6/i13ent.py`.)
    - R420-analogue on I_{13,1} with R420's own per-role chains scaled to h = 13 (sources 5 stops, targets 2,
      helpers about 6; R = 3.5v = 1,274; `r420i13.py`):

      | entrance-ranked helpers | vs P111-tuned |
      |---|---|
      | none (all frame-0) | -3.6% (break-even R about 1,165) |
      | 546 at rank 2 | +9.0% |
      | 546 at rank 4 | +15.0% |
      | 910 at rank 2 | +13.5% |
      | 910 at rank 4 | +21.8% |

    - Floor 706 frame-0 plus 568 hubs at e = 5-8: +8% to +22% (`i13mix.py`).
  - **Structure of I_{13,1} (exact; `scratchpad/i13a/`).**
    - Good 4-frames come in the same two orbits as in I_{11,1}: PPTT {P(ab),P(cd),T(abx),T(cdx)} (19,305) and
      TTTT Pasch frames (51,480); 70,785 in all, all good and mutually orthogonal (checked).
    - A partition needs 39 PPTT + 52 TTTT frames.  Compatibility degrees: 13,548 (PPTT) and 9,784 (TTTT) of
      70,785.  The matrix agrees with an independent implementation on 24,000 pairs and is symmetric.
    - **No aligned (pairwise compatible) partition without punctures** (`exact13.py`, exhaustive).
      - Proof: WLOG a fixed PPTT frame, since every partition has one and S13 is transitive on them.
      - The DFS closes after 3 nodes: P(04) has 2 compatible covering frames, and each kills 96 lines.
    - **Critical-line lemma.**  After a PPTT frame with apex x and pairs ab, cd, each apex line P(ax), P(bx),
      P(cx), P(dx) has exactly 2 compatible covering frames, and either choice leaves 96 lines uncoverable.  With
      fewer than 96 punctures, every chosen PPTT frame therefore has its 4 apex lines punctured.
    - **Counting.**  Every live P line then has a common dead neighbour, so 78 - Pp <= sum_x C(d_x, 2) with
      sum d_x = 2 Pp.  Hence **Pp >= 12**, with equality only for the star: all P(x, .) punctured and all 33 PPTT
      frames with apex x.
    - Exhaustive iterative deepening (`punct13.py`): no aligned partition with <= 10 punctures.
    - **Star case** (`star13.py`, `star13b.py`, `stardfs.py`): all 1,485 star frames are mutually compatible, and
      one TTTT frame fits a full star matching.  But the joint exact DFS finds no aligned completion with <= 40 T
      punctures.  So aligned partitions need >= 12 + 41 punctures in the star case.
    - **Caveat.**  Pairwise alignment is stronger than what R420 uses: R420's E-sets are exact unions of the
      cells of their two feeding quads, while 5,760 (cell, E-set) pairs are split (3f re-check).  So these closures
      do not exclude an R420-type I_{13,1} middle.
    - **PG(2,3) structure (new).**  K13 decomposes into 13 K4s, the lines L_k = {k, k+1, k+3, k+9} mod 13 of
      PG(2,3); K11 has no such decomposition (max 6), which is the I_{11,1} obstruction.
      - The blocks D4(p_k, L_k) with apex offset 4 give 39 good PPTT frames with no punctures, and the other 208 T
        lines admit an exact Pasch tiling: a full good-frame partition (`pg23part.py`).
      - Each block's 3 frames share Q = D8(p, S8) (56 lines, rank 8), the analogue of E8's complementary D4
        (12 lines).  TTTT frames have 42-line Q-parts.
      - Unlike E8's, no two PG(2,3) blocks are orthogonal, because lines of PG(2,3) always meet.
    - **Alignment of I_{13,1} partitions (session 6h; `scratchpad/i13a/diag13.py`, `scratchpad/i13s/`).**
      - Metrics per partition:
        - compatible frame pairs (strict alignment = all 4,095);
        - frame-mate fraction (share of a line's demands, Q-parts and E-sets, that contain a frame-mate; E8 R420
          = 1);
        - per-line cell cover (minimum partners so that every demand containing u contains one; E8 = 3.00).
      - **PG(2,3) partition:** 559 / 4,095 compatible pairs, frame-mate fraction 0.23, greedy cover 7.03 per line.
        The exact per-orbit cover (`pg23z.py`, CP-SAT) has proven lower bound 6 on all 24 of 28 Z13 line orbits
        finished, with 6-7 achieved, against E8's 3.
      - **Calibration (exact):** in E8 a random disjoint pair of good frames is compatible 13.4% of the time
        (1,109 of 8,277 for a fixed frame).  I_{13,1} gives 14-19%.  So R420's full alignment is structural, not
        statistical, and I_{13,1} has to supply an equivalent structure.
      - **Rigidity (exact on samples):** freeing k frames of the PG(2,3) partition and re-covering the freed
        lines by good frames gives only the original cover for k = 2, 3, 4 and 6 (200 / 60 samples).  It gives 2
        covers in 1 of 200 samples for k = 5 and 1 of 60 for k = 8.  Annealing over such moves (`sa13.py`)
        never moved.  Partitions can only be changed globally.
      - **Symmetric classes (exhaustive enumeration, sampled scoring; `sympart.py`):**
        - Z13:Z3-invariant partitions: 13,151.  Best of 200 scored: greedy cover 6.33, compat <= 949,
          frame-mate fraction <= 0.35.
        - Z13-invariant partitions: > 10^6 (enumeration capped).
      - **Per-line ILP over all partitions (`coverlb.py`, `coverflat.py`).**
        - E8 control: exactly 3 under both the pattern model and the flat model (demand = section flat rather
          than E-set), OPTIMAL.
        - I_{13,1} P line: best found 7, CP-SAT bound 1.  Uninformative; the runs were killed for memory
          (15 GB).
        - The reach-type necessary condition (R(u) minus the mates must be covered by partner perps) gives 3
          for E8, I13 T and I13 P alike (`reachlb.py`), so it does not separate the systems.
      - **Load (exact counts).**  The PG(2,3) partition has 611 distinct demands holding 28,808 line-incidences,
        79 per line.  E8 R420 has 190 demands with 3,000 incidences, 25 per line.  I_{13,1} therefore carries
        3.2x E8's per-line demand load before any misalignment cost.
      - **Break-even R/v with the lever, by system** (`scratchpad/lor6/levbe.py`; generic chains: sources 2 stops,
        targets 3, frame-0 helpers 5, hubs 2; fraction f of helpers are hubs at entrance rank e):

        | system | f = 0 | f = 0.25, e = 2 | f = 0.25, e = 4 | f = 0.5, e = 2 | f = 0.5, e = 4 |
        |---|---|---|---|---|---|
        | E8 (cst 72) | 3.27v | 4.07v | 4.10v | 4.63v | 4.97v |
        | I_{10,1} | 1.90v | 2.39v | 2.41v | 2.90v | 3.04v |
        | I_{11,1} | 2.94v | 3.67v | 3.69v | 4.15v | 4.45v |
        | I_{12,1} | 2.43v | 3.04v | 3.06v | 3.53v | 3.78v |
        | I_{13,1} | 2.89v | 3.61v | 3.62v | 4.08v | 4.38v |
        | I_{16,1} | 2.51v | 3.15v | 3.15v | 3.63v | 3.86v |

        - In this model every Lorentzian system allows less R per line than E8 at equal lever use (I11 and I13
          about 0.3-0.6v less).
        - A Lorentzian word must therefore be at least R420-efficient per line while carrying about 3x the
          per-line load.
        - The R420-analogue rows above (+9-22%) assumed R = 3.5v; at the measured load and misalignment that
          assumption is not supported.
      - **Near-top hubs and the binding frame-0 budget** (`scratchpad/lor6/highent.py`, `longcarrier.py`).
        - A hub's price scales with its residual width h - e, so hubs entering near rank h - 1 (one stop) are
          almost free.  Break-even R with a fraction f of helpers as hubs at entrance e:

          | system | e | f = 0.5 | f = 0.75 | f = 0.9 |
          |---|---|---|---|---|
          | I11 | 4 | 4.8v | 6.0v | 6.9v |
          | I11 | 10 | 5.6v | 10.2v | 18.5v |
          | I13 | 4 | 4.8v | 6.0v | 6.9v |
          | I13 | 12 | 5.5v | 10.1v | 19.6v |

        - What binds is the number C of frame-0 helpers.
          - I11 with hubs at e = 10: C = 300 allows up to 3,250-4,630 hubs, depending on carrier stops (5-11)
            and target stops (3-10).  C = 500 allows <= 2,650, or none at long chains.  C = 700 loses outright.
          - So any I11 design must run on about 220 sources + <= 300-450 frame-0 carriers, with everything else
            entrance-ranked.
        - That is the regime of the session-6g aggregation count.  Rank-7-9 leaves need about 6,150 injections
          (2,650 P-side + 3,500 T-side) into incomparable leaf frames.
          - A chain visits one frame per rank.  It may feed several hubs that share that frame, but not hubs at
            incomparable frames of the same rank.
          - So 520-670 frame-0 registers reach at most 1,560-2,000 distinct rank-7-9 leaf frames.
          - The near-top-hub pricing does not lift this budget.  Structural count, not a word-level bound.
        - Hub mechanics, from gcheck semantics plus the E1 rule:
          - A hub's chain starts at its entrance frame, so it can never visit a lower frame.
          - Hub-to-hub transfer is therefore consumption: the child climbs into the parent's frame, so each hub
            feeds at most one parent.
          - Only frame-0 registers (sources, carriers, targets) read hubs at several levels and carry sums
            upward.
          - Hence sharing = several frame-0 readers passing through one hub frame, and copying = a frame-0
            carrier reading a hub at F and being consumed at a higher frame.
        - D8 version of the count (I_{11,1}).
          - T(abc) needs 3 D8 totals and P(bc) needs 9.  Each of the 495 D8 totals has 2 users: 990 incidences.
          - A target's chain visits one rank-8 frame, so at most 220 incidences are in-chain reads at the D8
            frame itself.
          - Every other incidence needs the D8 total moved to a frame on the user's chain.  That move is a
            consumption (one per assembly) or a frame-0 carrier that visited that D8 frame, and a carrier visits
            only one rank-8 frame.
          - So >= 770 extra assemblies or carrier transfers, against <= 300-450 frame-0 carriers.  Extra
            assemblies push the same problem down to the rank-7 parts.
        - Pricing the profile this argument implies (`scratchpad/lor6/mixprice.py`, exact pricer, best-fit
          hosting):
          - Ingredients: 300 long-chain carriers; 440 P-side transfers entering at rank 2-3 (P targets' 8
            non-chain D8's only share low frames); 330 T-side transfers at rank 7 (entering at P(S)); 495 D8 hubs
            at rank 8; 220 top hubs at rank 10.
          - That bare profile, with no assembly hubs, gives R = 1,785 at -11.1% (kt = 4) / -13.4% (kt = 8).  A
            leaner variant gives -14.6% / -16.7%.
          - Adding 1,000 assembly hubs at rank 5-7 hits the hosting wall.
          - **The D8-based hub-native route for I_{11,1} loses in the model**: the near-frame-0 P-side transfers
            dominate.
        - Tried and failed: a 3-D8 "triality" cover of P targets' E8(W).
          - E8 = D4 + D4' plus three 32-line pieces would give tot E8(W) as 3 D8 totals instead of the apex 9.
          - In I_{11,1}, D4 + D4' already spans 8 of E8(W)'s 9 degenerate dimensions, so only one D8 flat contains
            a given D4 + D4' (`h10b/triality.py`: 630 pure D4 flats, no cover).
        - Counter-check: a pure counting relaxation (target t takes <= L_k lines at level k from frames shared by
          <= maxreach(k) targets) needs only about 168 carrier chains.  So the obstruction is structural
          (consumption plus one frame per rank), not counting.
      - **Stage template** (`scratchpad/lor6/kstage.py`, each against P111-tuned at the same template):
        - 11 stages (K = 5) moves E8 and P111 by <= 0.01v but costs I11 0.12-0.16v and I13 0.17-0.22v.
        - The template is not a Lorentzian lever.
      - **Decoder sensitivity, same model** (`scratchpad/lor6/cstbe2.py`):

        | system | decoder cst | f = 0 | f = 0.25, e = 4 |
        |---|---|---|---|
        | I_{11,1} | 110 (B0) | 2.94v | 3.69v |
        | I_{11,1} | 100 | 3.62v | 4.51v |
        | I_{11,1} | <= 90 | 4.00v (hosting wall) | 5.33v (wall) |
        | I_{13,1} | 156 (B0) | 2.89v | 3.62v |
        | I_{13,1} | 140 | 3.44v | 4.29v |
        | I_{13,1} | <= 120 | 4.00v (wall) | 5.13-5.33v |

        - Ten decoder units are worth about 0.7v of middle (I13: 1 unit ~ 12.5 helpers at f = 0).
        - Consequence for sparse-row decoders:
          - The cheapest way to empty a target's row is an extra mutually orthogonal piece containing it (row = the
            piece, cost +1 per line).  This is the "pseudo-puncture" of the window-10 E8 decoders.
          - It saves only that target's share of the middle, about 1-3 helpers, against about 12.5 helpers per
            decoder unit, so pseudo-punctures do not pay.
          - A sparse decoder must remove more than 12.5 helpers of load per extra decoder unit.
        - **I_{10,1} decoders (exact; `scratchpad/h10b/`).**
          - All 11 symmetric 165-line h = 10 systems (S10 ... S2^4 x S1^2, lor3) have B0 rank 11 and
            cst 99 = 11 x 9.
          - The lowest-load Lorentzian system is I_{10,1}: |R(t)| = 87-92 against v = 165, about 1.4x E8 per line.
            If its decoder fell to 90, its break-even would be 2.80v / 3.52v / 4.31v at f = 0 / 0.25 / 0.5.
          - Minrank: the max pairwise non-orthogonal set is only 9 (I11: 10).  But the SAT model proves no rank-10
            decoder exists (`rank10.py`: clique labels fixed WLOG by GL(10,2); INFEASIBLE in 10 s).  The rank-11
            control is FEASIBLE and verified, with B0-like rows of weight 88/93.
          - So every I_{10,1} decoder has >= 11 pieces, and cst 90 would need 11+ pieces of rank <= 8.
          - Whether B0 is the unique rank-11 I10 decoder is undecided: `rank11uniq.py` / `rank11min.py` were stopped
            after about 75 / 26 CPU-minutes without a verdict.
          - Same SAT for I_{12,1} and I_{13,1}:
            - Both have a 12-line pairwise non-orthogonal set; B0 has rank 13.
            - Rank-12 decoders are INFEASIBLE: I12 in 238 s, I13 in 8 s (12-clique labels fixed WLOG).
          - **Decoder minrank equals B0's rank for I_{10..13,1} (11, 11, 13, 13).**  A cheaper decoder can only come
            from lower-rank pieces, never from fewer pieces.
        - With standard source labels (I_{n,1} labels in F2^n), w_t is forced to B0's for every T target:
          span(u_s : s in NO(t)) is the 12-dim hyperplane F2^{[13] minus abc} + even(abc).  So sparse rows need
          richer source labels.  A sub-B0 decoder (still conjectured impossible for
          I_{11,1}, see dfam above) is the only lever comparable to the entrance lever.
        - Even so, a <= 4-5v middle is required, against the best verified 16.6v.
      - **I_{13,1} D10 decomposition and its chain conflict (exact semantics of gcheck).**
        - Let d(p; bc) = tot D(p, [13] minus {p,b,c}) (858 D10 totals).  Then T(pbc) needs
          d(p;bc) + d(b;pc) + d(c;pb) + 3 P lines, and P(bc) needs sum over p of d(p;bc) + the 11 lines T(bck).
          Each d has exactly 2 users.
        - Lemma: T(pac)^perp intersected with I([13] minus {p,c}) equals D(a, M) exactly, with M = [13] minus
          {p,a,c}.  So a single register serving both users of d(a;pc) must be read by T(pac) at D(a,M) itself,
          in T's chain.
        - A chain holds one rank-10 frame, so T(pac) can share at most one of its three d's with the P users.
          The other two need separate registers: >= 572 extra registers in this architecture, before assembling
          858 + 286 totals from lines.  This lands well above the 1,300-2,100 break-even range.
      - **R420 analogue grid on I_{13,1}** (`scratchpad/lor6/r420grid.py`, R420's role chains):

        | R | f = 0 | f = 0.5, e = 2 | f = 0.5, e = 4 | f = 1, e = 4 |
        |---|---|---|---|---|
        | 1,274 | -3.6% | +9.9% | +17.4% | +26.8% |
        | 1,500 | wall | +1.2% | +8.9% | +18.3% |
        | 1,750 | wall | -9.0% | -1.6% | +10.0% |
        | 2,000 | wall | wall | -9.4% | +2.7% |

        - Rough count for an aligned I_{13,1} R420 analogue:
          - E-sets of about 46 lines from 2 nodes each;
          - nodes of about 13 cells, shared 6 ways;
          - about 3,500 injections, giving R ~ 2,000.
        - That breaks even only with essentially all helpers entrance-ranked at rank 4.  Estimate, not a bound.
  - **The same lever on E8** (`scratchpad/lor6/e8ent.py`; P111 histogram, best-fit mixed-width hosting, which
    reproduces P111's 0.0017330528; model, not the official chain).
    - Converting n helpers to entrance rank e, i.e. removing one rank-e child each and shrinking their residual
      width to 8 - e:

      | n | e = 1 | e = 2 |
      |---|---|---|
      | 50 | +4.4% | +4.8% |
      | 100 | +7.4% | +9.3% |
      | 200 | +10.3% | +15.0% |

    - E1 (one helper, e = 2) gained +0.06% officially, consistent with about 0.06-0.1% per helper.
    - P111's own structure admits only E1's conversion (session 6f closures): its helpers are written in phase A
      and read by targets through D pre-cancellation.
    - A word redesigned so that hubs are written in phase B after their readers' pure reads, and read only
      in-chain, could convert many.  **This is the most valuable lead found in session 6g, and it is for E8, not
      Lorentzian systems.**
  - Status: a genuinely new design dimension; no previous session considered entrance ranks for Lorentzian
    middles.  It moves the I_{11,1} question from "R <~ 700" to "injections <~ 2,000 with carriers <~ 660".
    The same lever applies to E8 designs, where it was used for only one helper (E1).
- **Cheaper I_{11,1} decoders (current format: cost = sum of piece ranks; `scratchpad/dfam/`).**
  - Reformulation (exact).  For a fixed piece family, readers exist iff, for every target t, e_t restricted to
    N'(t) = {t} u NO(t) lies in the F2 span of the restricted piece indicators.  Each target is an independent
    linear check.  Dually, every pair (t, Y) with t in Y, Y inside N'(t) must be hit by some piece S with
    |S n Y| odd.  So the minimum-cost decoder is a hitting-set problem.
  - Facts:
    - Any 11-piece decoder equals B0 (minrank 11, B0 unique), so it costs >= 110: all codewords of C_11 have
      rank-10 supports.
    - No S11-invariant family is cheaper than 110: point-indexed piece classes have rank >= 9, A9 pieces miss
      every T target, and pair-indexed pieces of rank 1 miss T targets.
  - Searches over 1,390 structured flats up to Z11 (lines on k-sets, A_k, D_k(p,S), B_p(S), unions; closed under
    span), exact per-target checks:
    - Z11-invariant families of two orbits with cost <= 110: 566,392 tested, 0 valid.
    - Three orbits with cost <= 99: 10,820,183 tested, 0 valid.
    - Three orbits with cost <= 110: 24,041,562 tested, 0 valid.
    - Greedy (served/cost) collapses to the single-field decoder (cost 220): uninformative.
  - Conjecture (analogue of E8's 72 - #punctures): every I_{11,1} decoder costs >= 110.  Not proven.
- **Numerics caution:** a random-start LM with a faithfulness penalty (|<u,v>| >= delta on non-orthogonal pairs;
  `scratchpad/h9b/realize.py`) fails to realise even E8's pattern at rank 8 (residual^2 28).  Only equality-only
  relaxations with a passing E8 control, such as quad/orthrep.py, are informative.  The O^-(8,2) result
  (residual^2 = 114 - 6h, 6d) was obtained with such a relaxation.

## 3g. Session 6i (2026-10-17) — shared non-line entrance frames ("z-groups")

**Price identity (exact algebra on `pricer.py`).**
- Whenever every residual is hosted (below the hosting wall), the deficit is m W - mass = T (8 v - 9 cst).
  - It does not depend on R, the entrance ranks or the stops: a hosted helper's local mass cancels the idle mass
    it displaces.
  - So c is set by cst and by the log-spread D = sum z_r r ln(m/r) of the children (local pieces x T L, idle
    remainders x T): roughly c ~ T (8 v - 9 cst) / D.
- Consequences:
  - The trivial identity decoder (every source retained at its line, cst = v) has negative deficit: no root.
  - The ideal one-stop word with R = 0 gives c = 0.0039 for I_{11,1} (+125%), 0.0041 for E8.  So helpers cost
    only through D (fragmentation and hosting remainders), never through mass.
  - (`scratchpad/lor7x/ideal.py`.)

**The z-group mechanism (new; format-level argument plus exact pricing, no word built yet).**
- Pick a non-null vector z in the ambient.  Every target t with t perp z may take span(z) (rank 1, nondegenerate)
  as its first frame in phase B, right after the scatter.
- A helper that D does not read may start at span(z): the E1 relaxation, "start above frame 0".
  - All its later frames contain z, so it can be read only by registers whose frames contain z.  In particular
    every target that reads it is perp z.
- If no gate touches the group's helpers until every group target has stood at span(z), the targets can cancel
  any combination of group dirt there.
  - The group helpers are still pure at that point, so each target adds its own dirt row (its K-row restricted
    to group helpers).
  - This is exactly the D phase, moved from frame 0 to span(z).  The interleaved-B lemma (H1-H5) covers it: the
    target reads are B target gates.
- Inside a group the helpers are therefore as flexible as frame-0 helpers.
  - There are no in-chain reader conditions and no fan-in limit; they may collect anywhere.
  - Their residual width is h - 1, which packs the a-multiple idle slots exactly.
- Costs:
  - *Contagion.* Any register that meets a group helper has z in its frames from then on, so it serves only
    targets perp z.
  - In particular a source can feed one group directly.  Each further group needs a frame-0 copy of x_s, a
    "branch" taken at span(s) before the source is contaminated.
  - With g groups the frame-0 count is (g - 1) v.
  - Each group target pays one extra rank-1 piece (its stop at span(z)).
  - There is no sharing between groups, except through frame-0 registers.
- **I_{11,1} needs at least 3 groups** (proven, short argument).
  - With two normals, every pair {x,y} must have b_x = b_y in one of them, so one normal has constant b.  That
    normal is perpendicular to no T line, and the other would need all 165 T sums equal, so b constant: zero
    in the ambient.
  - Three groups exist: z1 = (-1, 1^10; 3) (norm 2, perp the 165 lines of I_{10,1}(W), W = [11] - {0}),
    z2 = (2, 1^10; 4) (norm -2, perp all T(0xy) and P(xy) on W), and z3 = (3^11; 11) (timelike, perp all 55 P).
  - Three groups give frame-0 count 2v, the same as the old branch floor (3 non-target registers per source).
    Everything else could be width-(h - 1) group helpers.
  - The cover above is very unbalanced: 165 / 45 / 10 targets.
- **Budget (exact pricer; `lor7x/zbudget.py`, `zbudget2.py`).**
  - All helpers at entrance 1, k = 4, sources and targets at 3 stops: break-even R <= 917 (4.17v) for I_{11,1}
    and 1,476 (4.05v) for I_{13,1}.  All helpers at frame 0 give 666 and 1,078.
  - 2v frame-0 branches plus group helpers at entrance 1:

    | system | group helpers H (stops 3/2/3/3 .. 5/2/5/4) |
    |---|---|
    | I_{10,1} (cst 99) | 0-113 (0-0.7v) |
    | I_{11,1} | 300-454 (1.4-2.1v) |
    | I_{13,1} | 472-718 (1.3-2.0v) |
    | E8 (control) | 214-300 (1.8-2.5v) |

  - Smallest window sizes at R = 3.5v with every helper at entrance 1 (`lor7x/h9need.py`):
    - h = 9, cst 72: v >= 117-120.
    - h = 10 needs v >= 154-158 only at cst 90.  I_{10,1}'s decoder costs 99, and then all-entrance-1 break-even is
      R <= 465-548 (2.8-3.3v), about 0.9-1.4v above its ~1.9v floor.  That is no better than I_{11,1}'s
      frame-0 room.
- **Branch registers must be frame-0 in any word (format-level argument).**
  - A non-source register that holds x_s at a one-line frame (a "branch" of the 3-section floor) gets x_s from
    one of two places:
    - from the source s itself, at a frame on s's chain.  Every such meeting puts the meeting frame into s's
      chain, so all of these registers are confined along one nested chain: one branch per source.
    - from a register present at span(s).  Only frame-0 registers, s itself, and helpers entering at span(s)
      can be there.
  - A helper entering at span(s) needs its dirt cancelled by readers that pass span(s).  That is impossible for
    group helpers, and possible for only the ~v/leftover targets whose rank-1 frame is span(s).
  - So the ~2v - v/leftover extra branches per source are frame-0 helpers: about 426 for I_{11,1} and 706 for
    I_{13,1}, in every word, with or without the lever or z-groups.
  - Best case (exact pricer): frame-0 count at that floor, everything else at entrance 1:

    | system | stops ks/kt/kc/kh | max total R |
    |---|---|---|
    | I_{11,1} | 3/2/3/3 | 896 (4.07v) |
    | I_{11,1} | 3/3/4/4 | 785 (3.57v) |
    | I_{11,1} | 5/2/5/4 | 743 (3.38v) |
    | I_{13,1} | 3/2/3/3 | 1,449 (3.98v) |
    | I_{13,1} | 5/2/5/4 | 1,205 (3.31v) |

  - So the non-branch middle may use only 1.4-2.1v helpers: R420-sized (1.5v), at 2-3x R420's per-line load.
    The prior rank-8 section walls (>= 1,001 total) miss even the most generous row by about 12%.
  - At R = 1,000: all helpers at entrance 1 give -5% to +2%; 440 frame-0 plus the rest at entrance 1 give
    -6% to -12% (`lor7x/` inline runs).
- **Relative-efficiency framing (exact pricer).**
  - Let eta = c / c_ideal, where c_ideal is the same system's one-stop R = 0 price.
  - E8's best words sit at eta ~ 0.38-0.40: R420 0.001654 / 0.004097 = 0.404; P111-tuned 0.001733 / 0.004561 (cst 63) = 0.380.
  - Beating P111-tuned needs eta >= 0.444 for I_{11,1} (c_ideal 0.0039) and about 0.448 for I_{13,1}.
  - z-groups multiply eta by about 1.12 on R420-like structures.  So a Lorentzian word needs E8-best eta just to
    tie, and strictly better than E8-best to win.
- **What it does not change.**
  - The aggregation layer still has to be about R420-efficient: about 1.5v helpers beyond the 2v branches, against
    a 1.4-3x per-line load.
  - The prior frame-0 middle walls (>= 1,001 total for rank-8 section tops) carry over unchanged to a single
    group, because group helpers are only as flexible as frame-0 helpers.  Splitting into groups only adds
    cost.
  - So the z-group lever removes the lever's fan-in obstruction (section 3f) but not the middle-quality
    obstruction.
- **Format check: PASS (exact).**
  - Toy word `code/zgroup/zdemo.py`: 4 timelike groups (90/58/44/28 targets), 877 frame-0 branches, 11 totals at
    FULL, and 26,070 direct group helpers starting at span(z_j); R = 26,958.  Price is irrelevant here.
  - It passes `code/zgroup/gcheck_z.py`.  That checker is gcheck.py plus exactly two changes:
    - the E1 relaxation: a helper that D never reads may start above frame 0;
    - the mixed-width rank-mass identity, sum (h - start dim) + cst + 2v(h - 1) = 274,989.
  - Every other check is unchanged:
    - exact F2 values on all 27,398 columns;
    - nested climbs, content in frame, nondegenerate frames;
    - H1-H5, and C as the literal reverse.
  - So group-D at span(z) in phase B is legal under the same rules as E1.
- **Timelike group vectors.**
  - If z is timelike, every frame containing z is nondegenerate: z^perp is positive definite.  So group frames
    never degenerate.
  - A spacelike z can fail.  For example, z1 has <z1, u> = -2 on every line u through point 0, so span(z1, u)
    is degenerate (u + z1 is null).
  - The best timelike cover of I_{11,1} found has 4 groups (`zgroup/tlcover.py`, greedy).  One group is
    D10(i)-like: z = (2, 1^10; 4) is perp exactly D10(0).
- **Sparse decoders (session 6i, exact linear algebra).**
  - A rank-12 code C containing C_11 is C_11 + <xi>.  A target t can use the new coset only if
    xi|N(t) is in C_11|N(t).
  - Solving the F2 system (xi plus one I_t per target, `sdec/coset.py`):
    - when all 220 targets use the new coset, the solution space is exactly C_11, so there is no extension;
    - the same holds for the star or co-star of a point, for all P targets, for all T targets, and for random
      sets of 20-160 targets.
  - So C_11 + <xi> changes only a handful of rows.  The useful case is pseudo-puncture-like: xi equals a
    codeword plus a set inside the common perp of the few changed targets.  This confirms the 6c note.
  - A new annealer that optimises W exactly per target (`sdec/sdec.c`) accepts no move away from B0 at rank 12
    or 13: B0's basin is rigid.
  - Z11-invariant CP-SAT models (`sdec/z11sat.py`: 20 orbit representatives, U and W with cyclic M = P (+) I):
    - rows <= 116 at rank 12: UNKNOWN after 600 s;
    - rows <= 130: OPTIMAL in 7 s (control: B0 is feasible).
    - Minimising the total representative row weight (MINW=1, 1,800 s each): best 2,370 at both rank 12 and
      rank 13.  That is exactly B0's 5 x 129 + 15 x 115.  The bounds (14, 7) are uninformative.  No
      Z11-invariant decoder sparser than B0 was found.
  - Decoder-cost sensitivity under an R420 structure with z-groups (exact pricer): every cst unit is worth about
    1.1-1.2%.
    - I_{11,1}: cst 100 gives +9.9%, 90 gives +21%.
    - I_{13,1}: cst 143 gives +4.9%.
    - I_{12,1}: cst 130 gives +0.2%.
    - So a decoder below n(n-1) would be the strongest single lever, but the codewords rule out the easy route:
  - Codeword support ranks (exact, `sdec/lowrank_cw.py`): in C_11, C_12 and C_13 every codeword has support rank
    >= h - 1.  Only the n coordinate totals reach h - 1; all others are full rank.
    - So every decomposition into minrank-many pieces costs >= n(h - 1).
    - A cheaper decoder needs more pieces whose low-rank supports cancel in combination: a 12+ piece
      decomposition, as with E8's double stars.
  - Annealing over piece sets from a pool of 13,277 closed nondegenerate supports (`scratchpad/dpool/`):
    12,540 rank-9 sections {p,q}-perp, 495 rank-8 flats, and the D10, I10 and t-perp sets at rank 10.
    - Target t is served iff its membership vector is not in the span of its non-neighbours' vectors.
    - From B0 with K = 12 at budget 109: stays feasible but stuck at cost 118 (B0 plus one piece).
    - From random rank-9 sets: 216-220 of 220 targets unserved.
    - Inconclusive: no cheaper decoder found, and the feasible region looks like an isolated basin around B0.
- **E-set structure, I_{11,1} vs E8 (exact; `scratchpad/eset/esets.py`, `e8esets.py`).**
  - This is what free recombination with cheap in-frame scratch still has to route: E(t,e) = lines perp t, e and
    not perp the other two frame members.

    | | E8 (R420 skeleton) | I_{11,1} (4-puncture good partition) |
    |---|---|---|
    | sections | 180 | 324 |
    | E-set size | 16 | 22-38 |
    | E-sets per line | 24 | 32-51 |
    | F2 rank of all E-set vectors | 38 of 120 lines (0.32) | 108 of 216 (0.50) |

  - In both systems every line has its own membership pattern, so atoms are single lines.
  - E8's E-sets live in a 38-dimensional space, which is what lets quads assemble them from cell sums.
    I_{11,1}'s need 108 dimensions with about 1.8x the incidences per line.
  - So even with free recombination, the I_{11,1} E-set layer carries roughly 2x E8's independent content per
    line.  This is consistent with the misalignment verdict.
- **Odd-or-zero extensions of I_{11,1} (exact enumeration, `scratchpad/nrl/compat11.py`).**
  - Search: lattice vectors in w-perp with |coords| <= 3, even nonzero norm, and odd-or-zero products with all
    220 lines.
  - Only the 11 timelike D10 normals (2, 1^10; 4) (norm -2) survive, up to S11 and sign.
  - Adding them gives a rank-11 decoder (label e_i), but piece i becomes D10(i) + z_i, of rank 11.  So each one
    costs a decoder unit: 231 lines at cst 121 (deficit 770 - k).
  - I_{11,1} is saturated: non-root-like products give no room inside this coordinate range.
- **Zero-waste mover skeleton (session 6i; pricer `lor7x/zw.py`, best-fit mixed hosting).**
  - Registers: v sources, 2v frame-0 relays (3 movers per line, the floor), and one frame-0 or group "dead"
    register per needer-shared section.  Everything else is in-chain lever scratch.
  - **Lever scratch cannot absorb rank loss** (linear algebra).
    - When two needers must leave a frame with equal x-content, the outputs lose a dimension.
    - A lever hub brings its own dirt dimension and can never drop it from useful registers.  Writers that have
      pure-read the hub re-inject its dirt.
    - So each shared section needs one dead register whose dirt is cancellable at the targets: frame-0 (D) or
      z-group (group-D).  That is R420's empty, one per D6 section.
    - At any meeting frame, the number of dead registers needed is rank(input x-span) minus rank(output x-span).
  - **In-chain reads remove part of that.**
    - Each target reads its frame's Phi-perp total (rank 6-7) and one matching section (rank 9) from in-chain lever
      hubs, which needs no copies.
    - That leaves 4 needer-shared sections per frame: 216 dead registers instead of 324.
  - Price (I_{11,1}, cst 110; stops kc/ks/kt as listed):

    | v | registers | price vs P111-tuned |
    |---|---|---|
    | 220 | 440 relays + 216 dead (2 pieces) + 162 lever hubs | +3.0% to +7.4% |
    | 216 | same | +0.3% to +4.6% |
    | 220 | 440 relays + 324 dead (2 pieces) | -0.5% to +2.3% |

  - **Why it is not a word: the E-set rank gap (exact, `scratchpad/eset/erank.py`).**
    - E8 R420: every E-set has 16 lines and rank 6, and splits exactly into two rank-4 hubs (8 + 8 lines).
    - I_{11,1}: E-sets have 23-37 lines and rank 8-9.  A greedy rank-7 hub covers 16-22 lines, and the rest
      still has rank 3-8.  So big E-sets need two hubs of rank 7-8, or 3-4 hubs of rank 5-6.
    - A rank-7/8 hub H must lie inside every section it serves.  So the served pairs live in H-perp (rank 3-4,
      at most ~12 lines), and each hub serves at most ~3-6 sections.
    - That brings back the kappa_5 forced-closure waste of the rank-8 walls: >= 400-560 extra movers, giving
      R ~ 1,000+ and about -10% to -15%.
  - The decisive structural quantity: E8's E-sets have rank 6/8 and halves 4/8; I_{11,1}'s E-sets have rank
    8-9/11 and halves ~7/11.  Lorentzian E-sets are relatively higher-rank, so hubs are shared by too few sections.
- **Punctured aligned I_{11,1} re-check (exact, session 6i; `scratchpad/punct/`).**
  - The 168-line live set of the 52-puncture aligned partition (`part/aligned_part_min.pkl`) would need decoder
    cost <= ~80 for an aligned R420-type word (R = 3.5v) to win, even with z-groups.
    - Pricer: v = 168, R = 3.5v with floor frame-0 plus entrance-1 helpers gives +40% at cst 58, +6% at 80,
      -9% at 90 and -40% at 110.
  - Facts:
    - The largest pairwise non-orthogonal clique in L has 10 lines.
    - A rank-10 decoder for L is INFEASIBLE (SAT, 2 s), so the minrank is 11.
    - B0|L costs 110 (all 11 pieces are rank 10).  One C_11 codeword has rank 9, so 109 is available.
  - Getting to <= 80 would need many pieces of rank <= 7, against minrank 11.  Not found, and not plausible
    given the full-system searches.  The punctured aligned route stays closed.
- **h = 9 window, numerics (session 6i).**
  - The orthogonality (zero) pattern of the 119-point O^-(8,2) quadric does not realise in R^{8,1}.  Margin-0.05
    LM, 3 seeds, 300 iterations: residual^2 376 / 455 / 384.
  - The E8 control (120 lines in R^8) reaches 8.5e-29 at its second seed.
  - So even a non-root-like realisation is numerically excluded (evidence, not proof).
  - Q^-(7,2) does admit a spread of 17 totally singular planes (CP-SAT OPTIMAL; `q119/spread.py`; 765 planes).
    That is moot given non-realisability.
  - The non-root-like local screen (`h9x/genlocal_zero05b.py`) stopped after 3 multisets with best
    residual^2 0.003-0.008.  Those residuals are too small to count as exclusions: inconclusive.
- **E-set ranks of I_{13,1}'s PG(2,3) partition (exact; `scratchpad/eset/erank13.py`).**
  - Good frames give E8-like parity: every outside line is perp to 0, 2 or 4 frame members (2,496 / 25,896 /
    4,368 (frame, line) pairs).  Q-parts: 42 lines rank 9 (TTTT), 56 lines rank 8 (PPTT).
  - E-sets (sections have rank 11 = h - 2):
    - PPTT frames: three 32-line E-sets of rank 10, which split E8-style into 16 + 16 lines at rank 6 + 6
      (relative 6/13, E8 4/8); one 80-line and two 60-line E-sets of rank 11 (full section rank; a greedy rank-8
      hub covers 24-32 lines and leaves rank 9-11).
    - TTTT frames: all six E-sets have 46 lines at rank 11 (greedy rank 8 covers 28, rest rank 10).
  - So only the 12 within-pair PPTT E-sets per block are E8-like; the rest repeat I_{11,1}'s rank gap.
- **Maximal orthogonal frames of I_{11,1} (exact enumeration; `scratchpad/eset/tenenum.py`, `tenframe.py`).**
  - There are exactly 10,395 = 11 x 945 sets of 10 mutually orthogonal lines.  Each is a D10 frame: an apex a and
    a perfect matching M of the other 10 points, {P(m), T(m a) : m in M}, perp to the D10 normal (1^10, 2; 4).
  - Every one holds 5 P lines, so no partition into 10-frames exists (it would need 110 P lines).
  - Class structure is very regular: every outside line is perp to exactly 5 or 6 frame members, giving 25 classes:
    - 10 between-pair D10 blocks B_pq (8 lines, rank 4), each needed by the 6 members of the other 3 pairs;
    - 10 blocks C_pqr = {T(ijk) : i in p, j in q, k in r} (8 lines, rank 4), each with 5 users;
    - 5 blocks A_q = {P(a q_x)} u {T(p p' q_x)} (10 lines, rank 6), each with 5 users.
  - A target in pair r needs 13 (T) or 14 (P) blocks plus 9 partners.  The 6 B blocks and 8 of the partners
    together are exactly the D8 total d(a; r) of section 2e, so this is a refinement of the apex/D8 decomposition
    (each D8 total = 6 rank-4 blocks + 8 frame lines for a matching of its 8-set), not a new top.
  - Load if 33 frames carry all 220 targets (5 T + about 1.7 P each): 33 x 210 = 6,930 block incidences, 31.5 per
    line (E8 R420: 25).  The 6g D8 count still applies: block contents must reach 3 incomparable rank-8 frames
    D8(r-bar) each, so the transfers, not the load, bind.
- **First price of a verified Lorentzian word (exact; `code/price/bankprice.py`).**
  - Model: mixed-width best-fit hosting, with overflow residuals on width-m bank streams (the `k3/banks.py` model).
    Controls reproduce P111 (0.00173305282534) and R420 (0.00165382699015) exactly.
  - `word_blkA4` (R = 3,656, cst 121, local histogram from gcheck): 7,920 residuals hosted, 24,984 banked (3,021 banks
    per replica), **c = 0.000492650689, -71.6% vs P111-tuned**.  So the best verified word is now priced; it is
    about 3.5x below the frontier.
- **Per-line cell cover (exact CP-SAT per line; `code/zgroup/coverline.py`, `tencover.py`).**  The minimum number of
  cell partners a line needs so that every demand containing it contains a partner; this is the bottom-level
  register count of an R420-type cell network.
  - E8 R420 4-frame top (210 demands, load 27 per line): exactly 3 for all 120 lines.
  - I_{11,1} 10-frame top (33 D10 frames, 825 demands, load 31.5 per line): 11 (54 lines) or 12 (166 lines), each
    proven optimal for that cover.  Its small blocks have different block-mates in every frame, so the 10-frame top
    is dead at the bottom.
  - I_{13,1} PG(2,3) (6h): 6-7.
- **E-set half sharing and alignment, E8 vs I_{11,1} (exact; `code/zgroup/ehalves.py`, `halfshare.py`,
  `halfglobal.py`, `halfanat.py`, `halfalign.py`, `misalign.py`).**
  - Sign halves: E(t,e) = E+ u E-, with E+ = {u : <u,k> = <u,l>} (k, l the other two members).  Each half lies in a
    pencil room f-perp + u of rank h - 3.
  - E8 R420: halves of 8 lines at rank 5 (the full pencil room); 120 distinct halves fill 360 slots, every half
    shared by exactly 3 sections; Q-parts shared by 3 frames (10 distinct).
  - I_{11,1} old partition (`goodpart.pkl`): halves of 10-26 lines at rank 7-8; all 648 distinct (no sharing);
    Q-parts unshared.
  - Over all 20,790 good frames, every I_{11,1} half occurs in 2 or 3 frames, always pairwise disjoint:
    - in exactly 3 frames: the 3 PPTT frames of a complete star-D4 block K_h(S4) (12 lines; 12 distinct halves per
      block, of 12/17/26 lines; the 3 frames also share their Q-part, the star D6 K_h(W));
    - in exactly 2 frames: the 2 TTTT frames of a Pasch pair (the two parity classes of transversals of one perfect
      matching of a 6-set).
  - So a partition built from complete star blocks and Pasch pairs has E8-style sharing.  But at most 8 star blocks
    are line-disjoint (CP-SAT found 6, bound 8; K4 packings of K11 are small), so most PPTT frames stay in partial
    blocks.
  - Alignment (every E-set a union of partition cells, i.e. even intersection with every partition frame): **E8 R420
    is fully aligned** (all 180 E-sets: 0 odd intersections; Q-parts too).  This corrects the 6h caveat that R420
    uses less than pairwise alignment.  Sign halves themselves are not cell unions in E8 (8 odd intersections each);
    R420's feeding quads are.
  - The old I_{11,1} partition has 6,588 odd (E-set, frame) pairs (11-32 per E-set) and 1,108 odd (Q, frame) pairs.
    Since aligned I_{11,1} partitions need >= 52 punctures (6c), an exact R420 copy is excluded; the remaining
    question is the minimum misalignment, each odd pair costing a single-line input or a correction.
  - Units are internally aligned (`unitcompat.py`): 0 odd pairs inside a star block and inside a Pasch pair.
    Between two line-disjoint units, disjoint point supports give 0, but overlapping supports average 9-47 odd pairs
    (zero-cost in only 0-32% of samples).  On 11 points almost every pair of 5-6-point supports overlaps, so a
    partition of ~25 sharing units still carries thousands of odd pairs, the same order as the old partition.
    Sharing therefore does not buy alignment, and the R420-type I_{11,1} middle stays excluded short of the
    52-puncture aligned partitions (whose 168-line decoder would have to cost <= 80).
  - Misalignment totals (odd (E-set, frame) + odd (Q, frame) pairs; `misalign_n.py`): E8 R420 0; I_{11,1} old
    partition 6,588 + 1,108 = 7,696; I_{13,1} PG(2,3) 19,448 + 3,900 = 23,348 (20-54 per E-set).  Annealing over
    I_{11,1} partitions (`misalign_sa.py`, remove 2-4 frames and re-cover, <= 4 punctures; moves are accepted, so the
    partitions are not rigid) moved 7,696 to 7,190 in 20,000 steps (a second 60,000-step run from that state: 7,149).  An R420-type middle with
    corrections would tolerate on the order of 100-150 odd pairs (about one extra register each against the
    roughly 0-140 helpers of slack at break-even), so the frame-cell family misses by about two orders of
    magnitude.
  - Best decomposed sharing search so far (`sharepart3.py`, 6 fixed complete blocks + CP-SAT, 4 punctures): 41
    touched groups = 492 distinct halves (old partition 648; counting bound about 25 groups = 300).
- **Rank-7 block groups: the closest Lorentzian blueprint so far (model; `unitspan.py`, `code/price/leverbp.py`).**
  - The 3 frames of a complete star-D4 block share f-perp (rank 7), so all 12 block targets can stand there.
    Helpers entering at f-perp are then a rank-7 z-group: width 4, freely combinable inside the group, and
    group-D at f-perp cancels their dirt.  Pasch pairs likewise give a rank-7 group of 8 targets.
  - Unit contents (exact): a star block has 12 distinct halves (7 x 12 lines rank 7, 1 x 26 lines rank 7, 4 x 17
    lines rank 8) and a Q-part of 30 lines rank 6; a Pasch pair has 6 x 12 (rank 7) and 6 x 17 (rank 8) halves and
    Q of 25 lines rank 7.  All spans are nondegenerate.
  - Delivery: one frame-0 mover per rank-7 half, two per rank-8 half, one per Q, arriving at the half's pencil room;
    the rest is width-4 group helpers.  Star block about 17 movers per 12 targets, Pasch pair about 19 per 8, so
    a best partition (about 6 complete blocks, partial blocks, 13-14 Pasch pairs) needs about 435-450 frame-0
    movers, close to the 426 branch floor.  Group helpers: about 3-4 per target.
  - Price (exact pricer, bank overflow): 450 movers + 660 width-4 helpers give -2.0% / +5.6% / +13.6% for
    stops s6-m5-h4-t3 / s4-m4-h3-t2 / s3-m3-h2-t2; with 1,100 helpers -14.2% / -7.5% / +0.3%.
  - **Lever calibration on E8 (exact pricer, R420 role chains reproducing its published histogram;
    `code/price/e8block.py`).**
    - Adding 360 width-4 rank-4 block-group needers while keeping R420's registers: -17.8%.
    - Replacing 240 of R420's frame-0 needer-carriers by them: +11.8%.
    - So group helpers pay only if they remove frame-0 registers.  In R420 those registers also carry the cell
      and quad levels (3 per cell, the cell floor), so they cannot simply be dropped; this is why 0 of 420 convert
      (6g).
    - For I_{11,1} the same holds: frame-0 registers are fixed by assembly, and cheap delivery saves little on top.
  - **Why it is not a word: assembly.**  Each mover must arrive carrying its half (12-26 lines), built from lines
    along a nested chain below rank 7.  The distinct half+Q load is about 4,870 incidences (22 per line) against
    E8 R420's 1,080 (9 per line, assembled by 540 registers through aligned cells).  The halves are not cell
    unions (misalignment above), so the 6g injection count applies: on R420's scaling, assembly needs about 2.5x
    E8's registers per line, far beyond the 450-mover frame-0 budget.  The blueprint fixes delivery, not assembly.
- **Rectangle tops are infeasible as exact covers (exact F2 linear algebra; `rectcover.py`, `rectpert.py`).**
  - A demand d delivered to every line perp to it is a rectangle of the orthogonality relation.  Apex D5s
    K_h(S5) are perp to exactly their complementary D5 K_h(S5'): 20 x 20, the largest rectangles (load ~6 per
    line on paper, E8 R420: 9).
  - Over all 26,070 ordered orthogonal pairs, the 2,772 apex-D5 rectangles span rank 2,101.  Adding all apex and
    coordinate families K_h(S), L(S) for |S| = 3..6 (10,131 rectangles) gives rank 5,004.  The all-ones vector is
    in neither span, so no exact mod-2 cover by full rectangles exists.
  - Per target, demands of the families K_h(S), L(S) (|S| = 3..8) lying inside t-perp span only rank 120 of 129
    (P targets; the 9 lines T(abk) lie in no such demand) and 84 of 115 (T targets; the 3 inner P lines and the
    apex gluing are missing).  With singles the only decomposition left is the apex one, R(T(abc)) =
    K_a(C) + K_b(C) + K_c(C) + 3 P lines, i.e. the known D8 route.  High-sharing tops are not available.
- **Sub-110 decoders: a cleaner reformulation and one closed family (session 6i; `code/dec108/`).**
  - Take pieces v_k supported in nondegenerate frames F_k.  If span(v_k) contains C_11, every target is served
    (use B0's row), and cst = sum rank F_k.
  - C_11 lies in that span iff there are columns a_k in F2^11 with label(u) in span{a_k : u in F_k} for every line
    u (label(u)_i = [u in D10(i)]).
  - **Coordinate flats are closed (proof).**  Take frames L(S) (lines with support inside S; rank |S| for
    |S| <= 8, 10 at |S| = 10).
    - Let A_X be the span of the columns of the flats containing the point set X.  Then e_x+e_y+e_z must lie in
      A_xyz, which is inside A_xy, and 1+e_x+e_y must lie in A_xy.
    - So A_xy contains 1+e_z for every z outside xy.  Those vectors span 10 dimensions, so at least 10 chosen
      flats contain every pair: sum_k C(|S_k|, 2) >= 550.
    - Pairs per unit cost are at most (s-1)/2, so cst >= 550 / 4.5 = 122 > 110 for |S| <= 10; only FULL frames
      (s = 11) reach 110.
  - Random annealing over 12 rank-9 frames (sections, {z_i, z_j}-perps, {z_i, line}-perps) stalled at 207 of 220
    lines violating the condition (`dec_sa.py`).
  - Z11-cyclic families (exhaustive; `dec_z11.py`): 11 shifts of one rank-9 section {p,q}-perp (all 1,185
    section orbits) plus the invariant frame z3-perp (rank 10, all P lines), columns rot^k(a0) for all 2,047 a0,
    and a12 in {all-ones, 0} (cost 109).  No decoder found.
  - Coset structure (`cwpair2.py`).  In a 12-piece decoder whose code is C_11 + <xi>, the pieces off C_11 are
    c_k + xi, and every difference c_k + c_l (a nonzero codeword) must lie in L(F_k) u L(F_l).
    - C_11 has 11 S11-orbits of nonzero codewords, sum of s coordinate totals, with weights
      90/90/116/116/110/110/104/104/130/130/220.
    - Over a pool of 25,224 frames (sections, t-perps, D10, I10, A10, coordinate flats, apex D's), the cheapest
      two-frame covers are 10 (s = 1, one D10 frame), 13 (s = 3, 9: t-perp + the 4-line flat of t's support),
      20 (s = 2, 4, 6, 8, 10), and none for s = 5, 7, 11.
    - So coset pieces pairwise need r_k + r_l >= 11-13, and the tau-type differences form a triangle-free graph.
      This gives cost >= 120 - 3.5 n for n coset pieces: not yet a proof of >= 110, but no cheap structure
      appears.
  - Partial proof for 12 pieces.  Change basis so that 11 independent columns become e_1..e_11 and the 12th is b,
    with w = |b|.
    - Codewords c_j = v_j (b_j = 0) need r_j >= 10, and c_j = v_j + v_12 (b_j = 1) need rank(F_j + F_12) >= 10.
    - Pairs inside B u {12} need rank sum >= 11: a tau-difference forces one frame to contain a whole D10 span,
      since two hyperplanes never cover the D10 roots.
    - Hence cost >= 110 for w <= 1, and cost >= 115.5 - 4.5w in general.
    - Closing w >= 2 needs line counts.  The largest nondegenerate frames found (`maxlines.py`) hold 4, 10, 20,
      35, 56, 84, 70 and 165 lines at ranks 3-10, against codeword weights >= 90.
  - **Pool theorem (exact; `cwpair_light.py`).**  In the S11-invariant pool of 25,224 frames (all sections, t-perps,
    D10, I10, A10, coordinate flats L(S) for |S| = 3..8, apex D's K_h(S) for |S| = 3..7), no two frames of rank
    <= 9 have line sets covering the support of any nonzero C_11 codeword (all 11 orbits checked).
    - Consequence: any decoder built from pool frames whose code is C_11 + (at most 2 extra dimensions) costs
      >= 110.
    - Proof sketch.  Pieces fall into classes by their coset of C_11.  Two pieces of one class differ by a nonzero
      codeword, so at most one per class is light (rank <= 9).  C_11 itself admits only heavy pieces.
    - With one extra dimension: >= 11 heavy pieces, cost >= 111.  With two: at most 3 light pieces; if there are
      3, their coset representatives sum to a codeword of support rank >= 10, so their ranks sum to >= 10 and
      cost >= 10 x 10 + 10 = 110.
    - Three or more extra dimensions are not covered (a Fano-type configuration of 7 light pieces survives the
      counting).  General frames outside the pool are not covered either.
- **Theorem (computer-assisted): every I_{11,1} decoder costs >= 101 (`code/declp/`).**
  - Scope: any number of pieces, any nondegenerate frames, any rank, code containing C_11 or not.  B0 costs 110,
    so decoder changes are worth at most 10 units (about 11.7% of price).
  - Clique lemma.  For a pairwise non-orthogonal set Q, the rows r_q (q in Q) restrict to the unit vectors on Q.
    So at least |Q| pieces meet Q, hence at least |Q| piece frames F_k have L(F_k) meeting Q.
  - LP.  Take weights mu_Q >= 0 with sum_{Q meets L(F)} mu_Q <= rank F for every frame.  Then
    cost = sum_k rank F_k >= sum_Q mu_Q |Q|.  L(F) is always a flat, and rank of its span <= rank F, so it
    suffices to impose the constraint on every flat, with its span rank, and on the full frame.
  - Data (exact):
    - all 467,181 maximal non-orthogonal cliques of size >= 9: 38,786 of size 10, 17 S11-orbits (`cliques.py`,
      `corbits.py`);
    - all 56,498 S11-orbits of flats of ranks 1-10 (2, 7, 25, 95, 378, 1,535, 5,555, 14,921, 22,418, 11,562;
      `flats.py`).  Closure is exact mod p (every minor is <= 2^12 < p).  Orbits use an individualisation-
      refinement canonical form with transposition pruning; completeness holds because every rank-r flat is a
      rank-(r-1) flat plus one line.
  - Optimum `declp.py corbits.pkl`: LP value 99.672501; the rescaled weights certify exactly 5,847,985/58,672.
    - Tight flats: rank 8 (56 lines), rank 9 (85 and 63 lines), rank 10 (109 lines).
    - Weights sit on the 11 P-star cliques, two other 10-clique orbits (495 and 1,320) and a 55-orbit of all-T
      9-cliques.
    - Adding the 11 orbits of 9-line sub-cliques Q - q (`subcl.py`, `declp.py corbits2.pkl`) leaves the value unchanged.
  - Room this leaves (bank-aware break-even, `code/price/bebank.py`): at cost 100, R <= 766-927 all frame-0, or
    890-1,097 with the 426-helper floor at frame 0 and the rest at entrance 1.  At B0's 110 the figures are
    617-756 and 721-896.  The best verified word has R = 3,656, and the load-22 model estimate is about 1,580.
  - Minrank-11 families (`declp3.py`).  Add 12 orbits of SAT-certified minrank-11 sets (16-33 lines; orbit sizes
    1.66M-39.9M, exact counts by `c/orbmeet` on the 877 near-tight flats, integer union-bound ceilings elsewhere).
    The certified value rises to 100.647393, so (costs are integers) every decoder costs >= 101.  One minrank-11
    orbit (|Y| = 16) carries about 22 of the ~100.6 units.  Two small flats priced by the union bound were tight;
    `declp4.py` converts these to exact counts iteratively.
  - Dual-guided column generation (`colgen.py`, duals of the clique LP): 25 of 25 minrank-11 sets found have
    reduced score 10.21-10.53 < 11 (improving), with 15-16 lines.  They enter the iterative certified LP (`declp4.py`).
  - Ceiling of the method: the rank-10 frames t-perp meet every maximal clique except those through t, which
    caps any clique LP near 104.8.  Small sets of minrank 11 (a 10-clique plus 6-8 lines, found by SAT in
    `mr11.py`) could lift it, but exact counts for their large S11-orbits cost ~1-2 CPU-hours per orbit
    (`c/orbmeet.c`, validated against explicit orbits).
- **Rank-12 decoders: they exist outside C_11, but stay B0-like (exact SAT; `code/dec12/`).**
  - Setting.  A decoder is B = W U^T over F2 (labels in F2^c) with B_tt = 1 and B_ts = 0 for every non-orthogonal
    pair; row t of B is what target t reads.  B0 (rank 11, unique) reads the whole perp: rows of weight 115 (T)
    and 129 (P), 26,070 in total.  Sparse rows are the only decoder-side lever on the middle load.
  - Row space need not contain C_11.  A kernel witness z (U^T z = 0, Mz != 0, with M the D10 incidence) is
    satisfiable at c = 12 in 17 s (`dec12c.py 12`), so the pool theorem's "code contains C_11" hypothesis is
    not WLOG.  With J independent witnesses (`dec12j.py`), dim(S cap C_11) = 6 is reached (J = 2 and J = 4
    both give dim(S + C_11) = 17); J = 6 is running.
  - All six rank-12 decoders found have the same shape (`scost.py`, exact matroid greedy over all 4,095 vectors
    of S):
    - 11 pieces of rank 10 (weights 82-90), plus one small piece: an orthogonal set of 2, 6 or 8 lines, or a
      5-7-rank set of 6-10 lines.
    - Costs 112, 115, 116, 116, 117 and 118.
    - Row-weight savings against B0: 243, 358, 1,143, 1,140, 294 and 1,535 (at most 5.9%).
    - D = B + B0 has rank 3-11; rows mostly drop the small piece's lines, saving 42-192 entries per unit of
      extra decoder cost.
  - Forcing sparsity: ">= 2 rows each saving >= 20" is SAT (two rows cut to weight 5, total saving 358,
    cost 115), and ">= 6 rows saving >= 45" is SAT (35 s; a 6-line orthogonal piece, cost 116, saving 1,140).
    In both, the sparse rows are the targets inside the small piece.  ">= 30 rows saving >= 10" is SAT after 92 min:
    B0 + x y^T (rank-one change, 30 targets x 10 mutually orthogonal lines, a rank-4 10-line piece; row space
    contains C_11), cost 114, saving 300.  ">= 11 rows saving >= 45" was stopped after about 2 h without a verdict. (`dec12s.py`)
  - Price.  At the model exchange rate (one decoder unit is worth about 1-1.3% of middle load, i.e. 260-350 row
    entries, whether R is about 1,600 or 3,700), a piece that saves at most about 190 entries per unit loses.  Decoders of cost
    >= 120 are fatal in any case (tie density at the 426 floor).  So rank-12 decoders do not open the
    sparse-row lever; at most they trim a few percent of load at a net loss.
- **O^-(8,2) nonsingular points: the minus-type sibling of E8 at h = 9 (session 6i; `code/ominus/`).**
  - Motivation.  E8's 120 lines are the nonsingular points of O^+(8,2) with "orthogonal iff omega = 0".  The 136
    nonsingular points of O^-(8,2) meet the h = 9 non-root-like cap of 136 exactly.  An earlier run found no
    realisation below real rank ~19 (section 3f, NOTES-full-log); this is an independent re-check with value estimates.
  - Combinatorics (exact, `comb.py`, `minrank.py`):
    - B0 = J + Omega has F2 rank 9.  Every point has |t-perp| = 63 (E8: 63).
    - The largest non-orthogonal clique has 7 points (E8: 8), but rank-8 decoders are UNSAT, so the minrank is
      9.  The E8 control is UNSAT at 8 as well.
    - Row-space weights are 64, 72 and 136.
    - Against a Lagrangian frame, the other points split into 112 of support 4 and 16 of support 8 (E8: 112 and
      0).  The frame + support-4 part is not E8's graph (degrees 55/63; `sub120.py`).
  - Value if it existed (bank-aware shape model, `be9.py`, h = 9, cost 72 = 9 pieces of rank 8).
    - Break-even R = 502-600 (3.69-4.41 v), against P111-tuned's own 3.84-4.57 v and its actual 3.95 v.
    - So it would be on a par with P111 at equal helper density.  Cost 64 would give 4.74-5.59 v; cost 81
      would give 2.46-3.01 v.
  - Not realisable (numerical, `realize.py`, analytic sparse Jacobian; the E8 control reaches residual^2 1.9e-29):
    - All 16 seeds stall at residual^2 439-477 in R^{8,1}, R^{9,0} and R^{7,2} (margin 0.3); about 177 of that is
      the orthogonality equations alone.
    - With margin 0.01 the residual^2 is 240, almost all in the norm term: the vectors collapse toward null.
    - Evidence, not proof.  Together with the earlier quadric (singular-point) exclusion, the E8-sibling family
      at h = 9 is closed.
- **Apex families force the D8 decomposition (exact F2 + CP-SAT; `code/apexd5/fam.py`).**
  - Using full apex sub-systems K_h(S) as shared demands, a target's need decomposes as
    R(T(abc)) = sum over h in abc of sum_{S in F_h, S avoiding abc} K_h(S) + 3 P lines, and similarly for P(bc)
    (plus 9 lines T(bck)).
  - This works iff each apex family F_h of k-subsets of the other 10 points covers, for every pair bc, every pair
    xy outside bc an odd number of times by the sets avoiding bc.
  - Results: k = 5 and k = 7 are infeasible (inconsistent F2 system); k = 4 and k = 6 need all 210 subsets; k = 8
    needs all 45, which is exactly the apex D8 decomposition (495 D8 totals, 2 users each, load ~126 per line).
  - So apex D5 sharing (20 users per demand) is impossible, and apex tops reduce to D8, whose transfer count (6g)
    already kills them.
  - I_{13,1} (12 points per apex, `famn.py 12`): k = 4, 5, 7, 8, 9 infeasible; k = 10 needs all 66 (the apex D10
    decomposition of 6h); k = 6 feasible but CP-SAT found only all 924 sets.  Same outcome as I_{11,1}.
  - Parity view: with h(X) = #{S in F containing X} mod 2, the condition is
    h(xy) + h(xyb) + h(xyc) + h(xybc) = 1 for disjoint pairs xy, bc.  All cells (2-subsets) satisfy it with load
    4.5 per line but 126 deliveries per target; all 8-subsets the reverse (126 / 4.5).  Uniform k-families work
    only when C(m-2, k-2) + C(m-4, k-4) is odd.
  - Counting bound for any apex family (I_{11,1}).
    - Each of the 45 x 28 requirements (xy | bc) needs a set S containing xy and avoiding bc.
    - A set of size s meets C(s,2) C(10-s,2) <= 100 of them and costs s(s-1) lines of load plus (10-s)(9-s)
      deliveries, at least 0.4 per requirement.
    - So load per line + deliveries per target >= 504 x 11 / 220 = 25.2, plus 3-9 single-line deliveries,
      against E8 R420's 9 + 7 = 16.  Apex tops are at least ~1.6x E8 before any alignment cost.
    - I_{13,1} (m = 12, 13 apexes, v = 364): the same bound gives 2,970 requirements at >= 0.267 each, i.e.
      load + deliveries >= 28.3 per line.
    - Mixed set sizes (CP-SAT, `code/apexd5/fammix.py 10 900`, objective load + deliveries per apex, all
      1,013 subsets of size >= 2): the best family found in 900 s is again the uniform D8 family (2,610 per apex,
      i.e. 126 + 4.5 per line).  The solver bound stayed at 0, so this is heuristic; the proven bound is still 25.2.
  - Why sharing is capped (load argument).
    - With about 7 deliveries per target, demands average about 17 lines.  A 17-line demand of rank 7 has at most
      12 users (the lines of its rank-4 perp, at most a D4), so the load is at least 118/12, about 10 per line.
    - Reaching that needs most demand mass in perfectly shared demands, e.g. star-D6 parts K_h(W6) used by all
      12 lines of the complementary star block.  Only Q-parts achieve this.  Using full K_h(W6) demands
      everywhere is the k = 6 apex family, which parity forces to be all 210 subsets (load ~315 per line).
    - Partial demands lose users.  The best realised load is 22 per line (3-fold shared halves); E8 R420 has 9.
  - D8-route detail (by hand).  The three D8 totals of T(hbc) share the rank-7 room A7(S) (P lines on
    S = [11] - hbc), which lies in the perps of T(hbc), P(hb), P(hc) and P(bc).  So T targets can take their 3
    D8 totals through width-4 group helpers entering at A7(S).
    - A P target stands in only one such room, so 8 of its 9 D8 totals need frame-0 transfers (the 440 P-side
      transfers of 6g).
    - The D8 T-star parts {T(hxy) : xy in S} put every T line into 84 distinct demands.  The route is
      assembly-bound, consistent with 6g.
- **Target taps are impossible (format, exact).**  A target cannot serve as a relay for another target.  After the
  scatter its x-content always contains its own line (B_tt = 1, and no frame on its chain contains t), so no
  frame inside another target's t-perp admits reading it.  H5 alone would allow paired reads that cancel on y.
- **Open.**
  - Balanced group covers (I_{10,1}, I_{11,1}, I_{13,1}) whose groups have aligned, R420-like internal block
    structure.
  - A toy word through a gcheck variant that allows helper starts at span(z) when D does not read them.
  - Official-chain realisability of span(z) (route factors) for non-root z.

### 3g (end). Final 6i additions: decoder >= 102, good-frame weight spectrum, cell-graph alignment

- **Decoder bound, iterated certified LP (`code/declp/declp4.py`, `cgloop.py`, `colgen.py`).**
  - Round 1 of the iterated LP (cliques + minrank-11 families guided by column generation, exact on near-tight
    flats, union bounds elsewhere): LP 101.429859, CERTIFIED 101.429859, so **every I_{11,1} decoder costs >= 102**.
  - Dominant weights: clique orbit 11 (0.0981), orbit 55 (0.0365), small weights on orbits 495 and 1320, and one
    minrank-11 family of size 15 (orbit 55440).
  - Rounds 2+ (NX raised by 30 per round, new columns from `colgen.py`) were still running at the time of this
    commit.  The 102 bound is therefore final for the record; any later round can only raise it.
  - The gap to B0 (110) is now at most 8 units, worth at most about 8% (break-even R shifts about 75 per 5 units).
- **Good-frame weight spectrum, I_{11,1} (exact, `code/declp/frcover2.py`).**
  - A frame is 4 mutually orthogonal lines; w(F) = #{targets t not in F : |F cap t-perp| odd}.
  - 1,926,540 frames.  Weight distribution: 0 (20,790), 90 (277,200), 104 (381,150), 110 (762,300), 116 (485,100).
    The mean is 106.3.  **Good frames are exactly the weight-0 frames** (TTTT 13,860 + PPTT 6,930); every other
    frame has weight >= 90.  The weight-0 frames cover all 220 lines.
  - E8 control (`code/declp/frcover.py E8`): 122,850 frames, 9,450 of weight 0, and an exact cover of weight 0
    exists (CP-SAT OPTIMAL, 15 s): R420's partition is fully aligned.
  - **No partition into good frames exists for I_{11,1}** (parity, proven): a good frame is TTTT (0 P lines) or
    PPTT (2 P lines), so it contains an even number of P lines, and 55 is odd.  The restricted exact cover over
    frames of weight <= 40 (`frcover2.py 40 1800`) was running at the time of this commit; by the parity argument it
    cannot be feasible, and any partition must use frames of weight >= 90.
- **Partner structure is the same in both systems** (`partners3.py`): for every line s, every partner triple N in
  s-perp has all 3 orthogonal pairs (I_{11,1}: 252 triples for P, 840 for T; E8(M): 315 for both), so minimum
  degree 3 holds in both.  The difference is purely parity and alignment.
- **Cell-graph annealing for aligned low-degree orthogonal graphs** (`cellgraph.py`, logs `cg_lam1.log`,
  `cg_lam05.log`).  Starting from blkpartA (690 odd components, 3.14 per target), the simulated annealing reaches
  about 1.04-1.3 odd components per target, but only at mean degree 6-8 (the E8 R420 graph has degree 3 and 0).
  So the I_{11,1} cell architecture pays about 3-8 extra registers per cell, consistent with the R >= 770
  "perfect analogue" bound and the 52-puncture alignment result.
- **Status.**  Nothing in this block changes the verdict: the best verified word stays word_blkA4 (R = 3,656,
  -71.6%), no Lorentzian frontier is known, and the middle (registers per cell below 3) remains the only lever.

## 3h. Session 7 (2026-10-17) — z-groups re-priced: totals feeders and the E8 cover number close the lever

Scripts and logs: `code/s7/` (run from that directory; the pricers import `code/price/pricer.py`).  Frontier used
throughout: E1, c* = 0.001734473240795253742474 (`research/e8-bit-p111-e1`).

- **Exact linear budget at the frontier (exact algebra on `pricer.py`; `qbudget.py`, `marg.py`).**
  - F(q) is increasing, so c >= c* iff sum_r z_r cost(r) <= m W - mass, with cost(r) = r((m/r)^{c*} - 1).
    When every residual is hosted, m W - mass = T (8 v - 9 cst) (the 6i price identity).  In units of T, local
    children count x 9 and idle remainders x 1.  So "reaching the frontier" is one linear inequality.
  - Budgets: I_{11,1} at cst 110: 770; one-stop sources and targets plus the idle slots of a helper-free word
    cost 341.1, leaving **1.949 per line** for helpers and extra stops.  P111 (v 111, cst 63): 1.795 per line.
    E8 (cst 72): 1.503 per line.  So I_{11,1} has slightly *more* helper budget per line than P111, for twice the
    demand per line (118.5 against ~57).
  - Helper costs (average per helper, I_{11,1}, exact hosting): frame-0 one-stop 0.22-0.30; entrance-1 one-stop
    0.00-0.21 (free while the rank-10 idle slots last); entrance-1 (2,8) 0.08-0.28; frame-0 with 7 pieces 0.54-0.64.
    A frame-0 helper costs about 1.4x an E8 one (mass 11 against 8).
- **z-group allowance with uneven stops (exact pricer with banks; `grid2.py`, `grid3.py`, logs).**  The 6i table
  (1.4-2.1v group helpers) used even splits.  With uneven pieces (one large piece per register) and 2v frame-0
  entries, break-even allows up to 2.0-3.5v entrance-1 group helpers at cst 110 and 1.0-2.9v at cst 121
  (`grid3.log`).  But see the next two items: both assumptions fail.
- **Totals-feeder lemma (new, format-level, proven).**  In any word, for each line u let R1(u) be the first
  register that holds x_u-dependent content at a frame containing u and some other line (it exists because every
  line lies in some retained total, whose frame has rank >= 10, and both operands of a gate climb to the gate
  frame).  A register is "clean for u" just before it becomes R1(u), and history only grows, so **u -> R1(u) is
  injective: >= v distinct registers are contaminated before the scatter.**
  - In a frame-0 word these are the cell/branch merges the middle does anyway, so the totals cost nothing extra
    (R420, P111, blkA4 form their totals from dead registers).
  - In a *pure* z-group word (every target grouped) group helpers are untouchable in phase A, and the frame-0
    entries must stay clean for phase B.  So the totals need dedicated feeders: about v consumed frame-0
    registers (a balanced feeder tree can at best let half of them double as mildly contaminated entries, and
    only when the contamination misses their group readers).  Block copies do not help: a copy taken at a phase-A
    block frame B can carry only one vector, and the totals restricted to B have the label rank of B (rank 2
    for every cell, 5 for a D4 apex block of 12 lines).
  - Priced (`grid3.py`, inline runs): I_{11,1} with 3 groups needs 3v frame-0 registers (2v entries + v
    feeders, or sources as feeders and 3v entries).  At cst 121, entries (1,1,9), targets (1,2,7) the group
    helpers allowed are <= 1.0v at the most favourable stops; at R420-like stops (entries (1,1,2,7)) the word is
    already -1.4% with zero group helpers.
  - Frame-0 world for comparison (`f0grid.log`, totals from spent registers): 2v branches plus a frame-0 middle of
    0.3-2.1v.  So **z-groups give I_{11,1} no more middle room than frame-0 helpers**; the 6i statement "z-groups
    bring an R420-quality I_{11,1} middle up to a tie" (-3.3% to +0.3%) is withdrawn: that model charged neither
    the feeders nor the cross-group entries beyond 2v.
- **E8 needs 4 z-groups (exact, exhaustive; `e8cover.py`, `e8cov4.py`, `e8cov6.py`).**
  - All 77,488 line-spanned hyperplanes of E8 were enumerated (types by line count: 63 (E7) 120, 42 (D7) 1,080,
    37 (E6+A1) 3,360, 28 (A7) 8,640, 23 (D5+A2) 30,240, 22 (A6+A1) 34,048; A4+A3 and A4+A2+A1 sections have <= 16
    lines and cannot complete a 3-cover).  A 3-cover needs a set of >= 40 lines, i.e. an E7 or a D7 section; with
    one representative of each (W(E8) is transitive on roots and on norm-4 vectors) no pair of further hyperplanes
    covers the rest.  **No 3 hyperplanes cover the 120 lines; 4 do** (63 + 63 + 42 + 37).
  - Cheapest target-to-group assignment for that 4-cover (CP-SAT optimal, `e8grp.py`): sum_s |groups(s)| = 465,
    i.e. **345 frame-0 entries** (2.9v), against R420's 240 carriers.
  - Priced: sources (1,2,2,1,1), 345 entries (1,1,2,2,1,1), 180 group empties (2,2,2,1), targets (1,2,4), free
    totals: **-12.2%**; with 40/120 totals copies -15.2% / -21.3%.  The 6i lever "B. z-grouped R420, +3-6%" is
    therefore closed in its pure form; R420 with all 180 empties grouped *and* only 240 carriers (+1.9%) is not
    realisable, because 3 groups do not exist.
- **Structural identity (exact): I_{11,1} demands are E8 decoder totals.**  For a 9-set M = [11] - {i,j} the
  lines on M form the E8 copy E8(M) (degenerate span: radical w_M = sum_M e_x + 3f, null).  Its 9 #370-type decoder
  totals are D_p(M) = K_p(M - p) (p in M), the D8 apex blocks.  Then
  R(T(p,i,j)) = D_p(M_ij) + D_i(M_pj) + D_j(M_pi) + {P(pi), P(pj), P(ij)} and
  R(P(i,j)) = sum_{p in M_ij} D_p(M_ij) + {T(i,j,k)}.  So an I_{11,1} word must compute, at rank-8 frames, all
  495 decoder totals of the 55 E8 copies that E8 words only retain at the full frame from dead registers.  Within
  one apex p the 45 totals are the "all-but-two" coordinate sums of D10(p) over coordinate frames span(eps_W);
  every route found to them hits the D8-transfer obstruction already recorded in 3g.
- **Rank-10 totals as virtual targets (observation, not built).**  B0's total tot_i = N(D10(i)) is exactly the
  "demand" of the timelike normal z_i = (2 at i, 1 elsewhere; 4) of D10(i): the lines perp z_i.  So a frame-0 word
  can retain tot_i at its rank-10 frame z_i-perp by treating z_i as an 11th-kind pseudo-target, as P111 does for its
  punctured lines (#545/#589: the total reads at p-perp what the removed target would read).  The cost is about 11
  extra target demands (5% of the middle load) that must be complete by the scatter, plus phase-A carriers where the
  middle runs in phase B (P111 needed 10).  It recovers cst 110 against blkA4's 121: by `f0grid.log` about 1v of
  extra middle helpers at the frontier.  It does not close the factor-2 middle gap.
- **New infrastructure (`code/s7/zw/`).**  `space.py`: exact subspaces (RREF over Q, Gram form, perps,
  nondegeneracy, line masks) for arbitrary, non-line frame vectors.  `zword.py`: a word builder with z-groups
  (group helpers start at span(z_g); group-D reads inserted at the head of B) that emits bitGen/1+mut for
  `zgroup/gcheck_z.py`.  Not yet used for a full word.
- **Knock-on: the h = 9 window closes too.**  The 6h/6i requirement "h = 9 needs 117-119 lines" was computed
  with the entrance-lever / z-group model (3.5v at 25-50% entrance helpers).  Without the lever the h = 9
  requirement is the frame-0 one recorded in 6d (about 130 lines), above the proven frame-free ceiling of 119 (and
  framed h = 9 systems have <= 111, P111's own count at h = 8).  So no h = 9 system can tie P111 unless a middle
  better than R420 exists.  (Inference from the recorded numbers, not a new computation.)
- **Price of progress (`mix.py`, inline).**  Frame-0 I_{11,1} words with sources (1,2,7), targets (2,8), 2v
  branches (1,1,2,7) and a middle with pieces (2,3,6): at cst 110 the break-even is R ~ 840; R = 1,100 / 1,320 /
  1,760 / 2,200 price at -16.7% / -26.1% / -39.7% / -49.1%; at cst 121 the same R give -27.4% / -35.6% / -47.4% /
  -55.6%.  The best word (R = 3,656, cst 121, heavier stops) is -71.6%.
- **Session 7b: the exit-rank lever on bit words (new analysis; `code/s7/exitmix.py`, `code/s7/e8a/`).**
  - The complex side lets a helper end in a rank-(h-1) subspace U (#1030/#1090, `research/complex-rank7-end-pair`),
    which drops its residual width by one.  Bit-side transcription (format-level, needs its own lemma like E1's):
    helper h may end at U if (X1) no z-gate ever reads h (targets may, D cancels its dirt); (X2) an early cleanup
    h += sum of the inverse-row registers of h restores it, every such register sitting in a frame inside U at that
    moment and climbing to U for the gate; C then reverses every z-gate except those writing h.  Proof sketch: by
    (X1) no other register's evolution involves h, so skipping h's reversals leaves C = U^{-1} on all other
    registers, and the cleanup sets h to its dirt.
  - Size of the prize (exact pricer, `exitmix.py`): on P111-tuned's shape, letting the needer-type helpers (chains
    ending t-perp -> full) end at t-perp gives +5.3% (25% of them), +7.7% (50%), +11.6% (all), because width-7
    residuals tile the 666 rank-7 idle slots per replica that width-8 helpers cannot use.  R420 with every helper
    exiting: +15.8%.
  - As built: **0 candidates** (`exitcensus.py`).  E1: 429 of 439 helpers are read by z-gates; the 10 others have
    inverse rows spanning rank 8.  R420: all 420 are read by z-gates.
  - E1's 9 retained-total helpers are the nearest miss: no z-reader, 3 writes, inverse row of 5 registers at the
    scatter (one spans rank 7).  But each total reads the source of its d-line at the line frame and a shared D6
    helper (o1, later read at another target's perp); re-reading either inside p-perp drags it into p-perp and
    breaks its later chain.  Routing those contributions through registers that end at p-perp needs one extra
    width-8 copy per total, a net loss.
  - Adding fresh exiting needers instead of converting existing helpers loses (-0.8% to -9% for 37-150 of them,
    `exitmix.py` inline): the lever pays only by converting registers, and R420/P111 registers are fully
    multi-role.  Like the entrance lever, it needs a ground-up design; no candidate design is known.
- **Delivery count for the apex-D8 class of I_{11,1} words (counting, not a bound over all words).**  With B0, T(abc)
  needs the three D8 totals D8(a;bc), D8(b;ac), D8(c;ab) and P(bc) needs the nine D8(p;bc).  A D8 register can be
  read in-chain at its rank-8 frame by chains passing it (one rank-8 frame per chain) and then consumed into one
  reader's perp.  The cheapest assignment lets each P target absorb its nine D8 registers at its perp and gives each
  T target three in-chain reads (target chain plus 2 needers): 495 D8 hubs + 330 needers = 825 registers before
  any D8 is assembled, against a total frontier budget of about 840 (cst 110, moderate stops).  So this class
  cannot reach the frontier.
- **Verdict after session 7.**  No change to the best word (blkA4, -71.6%).  The z-group lever, the last
  Lorentzian-specific lever left by 6i, is closed for I_{11,1} (totals feeders) and its E8 stepping stone (B) is
  closed in pure form (4 groups).  What remains is lever A, a middle strictly more efficient than R420 per
  incidence, which would first be an E8 result.

## 3i. Session 7c (2026-10-17) — I_{13,1} re-priced with lean shapes; register identity; hub/2-cover census

Scripts: `code/s7/i13budget.py`, `i13tot.py`, `i13tot2.py` (pricing, logs beside them) and `code/s7/i13n/` (geometry,
PG(2,3) partition and demands, hub and 2-cover census; logs beside them).

- **Frontier allowance for I_{13,1} at cst 156 is larger than the R420-shape numbers suggested (exact `mix.py`
  pricer, best-fit hosting, all helpers one shape, no fixed branch helpers).**  Max helpers / v keeping c >= E1:

  | sources / targets | (11,1,1) | (10,1,1,1) | (2,9,1,1) | (4,7,1,1) | (1,1,9,1,1) | (2,3,8) | (11,2) dead |
  |---|---|---|---|---|---|---|---|
  | (12) / (12) | 4.72 | 4.30 | 4.10 | 3.90 | 3.96 | 4.12 | 4.92 |
  | (12) / (11,1) | 4.62 | 4.21 | 4.02 | 3.82 | 3.87 | — | 4.82 |
  | (12) / (10,1,1) | 4.52 | 4.12 | 3.93 | 3.73 | 3.79 | — | 4.71 |

  So an I_{13,1} word with lean stops may have R ~ 1,400-1,680 (3.8-4.6v), against the 1,165 (3.2v) obtained in 6h
  with R420's own per-role chains.  (Collector shapes end ...,1,1: last climb to t-perp, then to full.)
- **Register identity used for design (exact bookkeeping).**  Every z-register ends consumed at a target top or dead,
  so R + v = sum_t c_t + dead.  At a pool (frame) the arriving x-contents keep their rank under the invertible
  gates; a pool whose only useful output is one vector N(F) kills (arrivals - 1) registers.  With B0 every target's
  demand is its full perp, so every reader of a frame F wants all of F's lines once: pools built from flat sums are
  rank-1 pools, and each formed flat costs (inputs - 1) dead registers.  Fresh helpers that only copy N(F) out of a
  pool cost registers but no dead.
- **t-perp has no 2-cover by sections (exhaustive for T(012), P(01); `secs.py`).**  Sections X-perp (X an A2 or a
  cell containing t) have 90-166 lines; the best 2-union has 167 of 183 (T) / 212 of 231 (P) lines; every 3-cover
  is by three cell sections (4,005 for T(012), 495 for P(01)).  Hence c_t >= 2 for frame-type tops, and R >= v + dead.
- **PG(2,3) frame top, demand census (`part13.py`).**  91 good frames (39 PPTT + 52 TTTT), 637 demands (611
  distinct), sizes Q 42/56, E-sets 32/46/60/80, load 79.1 per line (E8 R420: 25).
- **Hub census (`hubs1.py`, `hubs1.log`).**  All 176,354 distinct pairwise intersections (>= 6 lines) of the 611
  demand frames, with users = demands whose frame contains the hub:
  - large hubs (20-50 lines) serve 2-5 demands (the two that define them, rarely more);
  - the best users/size ratios are 6-line rank-3 hubs with 42-45 users delivering about 3.3 lines each.
  - A butterfly hub only avoids waste when it serves at least as many demands as it carries lines; no large hub
    comes close, so the PG(2,3) demands cannot be fed by a few big shared hubs.
- **2-covers of demand frames are rare (`cover2.py`; hyperplanes S cap u-perp, u a line of S).**  Only the 118-line
  sections have them (28 each, best 69 + 115 lines with 66 shared); the 90/138-line sections and both Q types have
  none.  So most formed flats need >= 3 inputs, i.e. >= 2 dead each.
- **Estimate (counting, not a bound).**  Frame top: c_t = 2, so R = v + dead.  About 640 demand pools at >= 2 dead,
  plus their sub-flats, put dead at roughly 1,300-2,000 and R ~ 1,650-2,350 (4.5-6.5v), against the 3.8-4.6v
  allowance.  So a flat-sum middle on this top is still 1.0-1.4x over; R420 itself has dead = 1.5v because its
  D4 butterflies emit 12 distinct corrections (shared o1 compromises + private Q-deliveries).  An I_{13,1} middle
  needs the same compromise/correction structure, with dead <= ~3v (c_t = 2) or <= ~2v (c_t = 3).
- **Per-line pool cover (`poolcov.py`, `wcover.py`, CP-SAT exact on samples).**  A collector picks x_u up at a
  rank-2 pool <u,w> only if <u,w> lies in its demand frame, i.e. w in S_E.  This is weaker than the cell-sum cover
  of 6h (6-7 per line), which needed w in E itself.
  - With line partners w the minimum is exactly 4 on all 16 sampled lines (E8 R420: 3).
  - With arbitrary vectors w of the line space it is 2 (P(01)) or 3 (P(26), T(012), T(235)), with groups of up to
    76 of 86 demands.
  - So the bottom level is E8-like.  A collector, however, passes one rank-2 pool, so this only says that x_u can
    reach every demand; it does not feed 23-47-line parts.
- **Demand structure (`drank.py`).**  F2 rank of the 611 PG demands is 219 of 364 (0.60; E8 0.32, I_{11,1} 0.50).
  The 780 distinct sign halves (16/30/64 lines) fill 1,092 slots, so sharing is 1.4 per half (E8: 3, the maximum).
  E-sets of rank 11 are all 2-coverable by proper subflats of their section (`ecover.py`); Q-parts need 3.
- **Width-12 (exit) prize for I_{13,1} (exact `exitmix.py`; `i13exit.py`, `i13exit.log`).**  Idle slots are
  multiples of a = h - 1 = 12, so width-12 residuals tile them exactly.  With half the helpers consumed collectors:

  | collectors / dead | width 13 | collectors exit at t-perp (width 12) |
  |---|---|---|
  | (11,1,1) / (11,2) | 4.72v | 5.76v |
  | (10,1,1,1) / (10,3) | 4.41v | 5.38v |
  | (2,9,1,1) / (8,5) | 4.20v | 5.13v |
  | (4,7,1,1) / (2,9,2) | 3.99v | 4.84v |

  - About +1v of allowance: with it, the 4.5-6v flat-sum estimates above would reach the frontier.
  - **Why it is not available (argument, from the exit lemma of 3h/7b).**  The cleanup of an exiting helper must
    read its whole inverse row inside U = t-perp.  The inverse row of a collector that picked anything up from a
    shared pool contains that pool register, which can then be dragged into one target perp only.
    - So only collectors fed exclusively by registers dead afterwards (or owned by the same target) can exit.
    - Converting a consumed collector costs one extra pure-merger register per consumed demand (+1v for the frame
      top), against about +0.4v of allowance when ~20% of helpers exit.  Net loss, as for P111 in 7b.
    - Line copies cleaned by their own source: at most one per source.
    - Entrance (z-group) width 12 stays closed by the totals-feeder lemma.
  - Open: a gate pattern whose inverse rows are target-local by construction, e.g. pools whose registers all die
    into one target perp after their last pickup.
- **Half sharing over all good frames of I_{13,1} (exact enumeration; `halfshare.py`).**  70,785 good frames
  (19,305 PPTT, 51,480 TTTT) give 386,100 distinct halves.  Each half lies in exactly 3 frames (77,220: the 3 PPTT
  frames of a complete star-D4 block) or exactly 2 (308,880: the 2 TTTT frames of a Pasch pair, i.e. the 8
  transversals of a perfect matching of a 6-set).  As in I_{11,1}, E8-style sharing needs a partition into complete
  star blocks and complete Pasch pairs.
  - Complete blocks holding all 78 P lines force their 4-sets to form a 2-(13,4,1) design, i.e. PG(2,3) (unique, so
    fixing L_k = k + {0,1,3,9} is WLOG); only the 13 apexes p_k (not on L_k) are free.
- **No fully shared partition exists (proven; `paschpair.py`, `paschcyc.py`, `apexpar.py`).**
  - Parity lemma: a Pasch pair on matching {aa', bb', cc'} contains each of its 12 cross point pairs in exactly 2 of
    its 8 triples.  The T lines left by the blocks contain the point pair {a,b} 10 - 3 m_ab times, with
    m_ab = #{k : p_k = a, b in L_k} + #{k : p_k = b, a in L_k}.  A Pasch-pair tiling needs every m_ab even.
  - CP-SAT over all apex assignments: INFEASIBLE.  (When each point is the apex of exactly one block, this is
    Baer's theorem: the relation would be a polarity of PG(2,3) without absolute points.)
  - Direct tilings for the original PG apexes and for the three valid cyclic offsets c = 4, 10, 12: INFEASIBLE
    (also Z13-invariant: INFEASIBLE).
  - The same parity count rules out I_{16,1} (2-(16,4,1) = AG(2,4); 13 - 3 m_ab even needs m_ab odd on all 120
    pairs, but sum m_ab = 80).  Among practical I_{n,1}, complete star blocks plus Pasch pairs never tile.
  - Near-full sharing: the minimum number of point pairs with odd leftover count is between 7 (bound) and 10
    (found; apexes [12,7,1,1,1,7,12,11,7,7,1,2,11]; `minodd.py`).  Each unpaired Pasch frame fixes the parity of 12
    pairs, so only a few frames need to stay unpaired; 208 = 8 x 26 then forces >= 2 unpaired frames, so at most
    25 pairs.
  - Max-pairs CP-SAT (`maxpairs.py`, free apexes, hinted by PG(2,3); 1,500 s, not optimal): 17 complete Pasch
    pairs + 18 unpaired TTTT frames.  Evaluated with `eval13.py` against PG(2,3):

    | partition | half sharing | half + Q load / line | demand F2 rank | odd (demand, frame) pairs |
    |---|---|---|---|---|
    | PG(2,3), offset 4 | 1.40 | 58.0 | 219 | 21,930 |
    | 17 Pasch pairs | 1.90 | 43.1 | 202 | 21,402 |

  - So sharing lowers load by about a quarter but leaves misalignment unchanged (cf. I_{11,1}: sharing does not
    buy alignment).  An R420-type cell/quad middle stays excluded on every I_{13,1} frame top.
- **First verified I_{13,1} word (`code/s7/i13w/`).**  The I_{11,1} block-top builder (`build_blk_pairs.py` + `lw.py`)
  ported with n from env `LWN` (copies only; the I_{11,1} code is unchanged).  One I_{13,1} change: block layer frames
  that are degenerate in I_{13,1} (a rank-9, 64-line layer) are skipped and those sections use their plain E-set.
  - Build: `LWN=13 PCHAIN=1 QMERGE=1 QALL=1 PIECES=paar HOP=0 MP=1 python3 build13.py pg23_blocks.pkl OUT` on the
    PG(2,3) partition (13 star blocks + 52 single TTTT frames), about 4.5 min.
  - `word13_pg_v1.json.gz`: **gcheck PASS**, R = 8,665 (23.8v), 13 totals at the full frame (cst 169), 5,597 frames.
    Roles: 4,921 line copies, 3,370 carriers, 361 empties, 13 totals.
  - Price (`bankprice.py`): c = 0.000382970, **-77.9% vs P111-tuned** (best I_{11,1} word: -71.6%).  This is the I_{13,1}
    baseline; the frontier allowance is 3.8-4.6v, so the generic piece middle is ~5-6x too large.
  - Same builder on the 17-Pasch-pair partition (`maxpairs_blocks.pkl`: 13 star blocks, 17 two-frame Pasch blocks,
    18 single frames): `word13_mp_v1.json.gz`, **gcheck PASS, R = 7,367 (20.2v), c = 0.000441391, -74.5%**.
    Pieces per top fall from 11.9 to 8.0; sharing is the only lever that moved R.
- **Content per register: why I_{13,1} needs ~3x R420's middle efficiency (counting from exact data).**
  - Distinct demand content (halves + Q-parts, line incidences): E8 R420 120 x 8 + 10 x 12 = 1,080, i.e. 9 per line,
    carried by R + v = 540 registers (2.0 per register).  R420 itself: 360 registers are read by targets (all
    sources and 240 helpers) and 180 never are (1.5v pure middle).
  - I_{13,1}: 43.1 per line on the 17-pair partition, about 36 with the 25-pair maximum.  At the frontier allowance
    (R + v <= ~5.6v) that is >= 6.4 per register, about 3.2x R420.
  - So an I_{13,1} frontier word needs a middle about three times more efficient per unit of distinct content than
    the best E8 middle; such a middle would first make E8 words leap past the frontier (lever A).

## 4. Next goals (priority order)

**Session 7 update (details in 3h).**  Items 6i-B (E8 z-group lever) and the z-group half of 6i-A are closed:
pure z-group words pay ~v totals feeders (proven lemma) plus cross-group entries (E8: 4 groups, 345 entries).
The only open lever is a middle strictly more efficient than R420 per incidence; any such middle should be
demonstrated on E8 first, where it would move the frontier itself.

**Session 6i, final assessment (details at the end of 3g).**
- The binding quantity is assembly, not delivery.
  - Delivery can be made cheap: rank-7 block groups (z-groups whose group frame is a frame-perp shared by a star
    block's 12 targets) turn needers into width-4 helpers.
  - Assembly cannot: the distinct demand load is about 22 line-incidences per line even with E8-style half
    sharing (E8 R420: 9), and I_{11,1}'s halves are far from cell unions (about 7,200 odd (E-set, frame) pairs at
    best, against 0 for R420).
  - On R420's scaling, assembly alone needs about 2.5x E8's registers per line, while the budget is about 1.2-1.3x.
- Later in 6i (decoder and system closures):
  - D4-block tops (exact, `code/declp/d4top.py`).  All 2,310 D4 flats of I_{11,1} are apex blocks K_p(A) with 30
    users each, the apex D6 K_p(W) on the other six points.
    - T(abc)-perp = sum over p in abc of K_p(S) + 3 P lines, and each D8 K_p(S) = 7 D4 blocks (a Fano plane on 7
      points of S plus the 8th point): 21 D4 totals + 3 singles.
    - P(bc)-perp = E8(M) + 9 T lines, with E8(M) = sum of 9 D8 blocks.
    - The span checks agree (T: residual 3 singles; P: the 9 lines T(bck) are in no D4 inside the perp).
    - Scheduling kills the sharing.  A target reads at most one D4 at its rank-4 frame, and a D4 read at a rank-8
      frame afterwards serves only that D8's two users.  This is the D8-route transfer obstruction again.
  - Price sensitivity to target stops (bank-aware shape model, cst 110): going from 2 to 10 target stops lowers
    break-even R by only about 110 (617-756 -> 525-648), roughly 16 target stops per helper.  A source's readers
    still form one nested chain, and each target holds one frame per rank, so the branch floor is unaffected.
  - **Proven: every I_{11,1} decoder costs >= 101** (clique + minrank-11 hitting LP over all 56,498 flat orbits,
    exact certificate).  The decoder side is worth at most 9 units (about 10.5%).
  - Rank-12 decoders can avoid C_11 but stay B0 plus one small piece; sparse rows lose at the exchange rate.
  - The minus-type E8 sibling (O^-(8,2), 136 lines at h = 9) would sit at P111 parity but does not realise.
  - Stage count does not help the verified word.  Mixed-size apex families: nothing better than D8 found.
  - blkA4 uses a cost-121 decoder: its 11 D10 totals are XORed from leftover registers at the full frame.
    Retaining them at their rank-10 D10 frames would price -67.4% instead of -71.6% (`code/price`, exact).  As a
    retrofit it is impossible: in a rebuild (`code/d10ret/build_d10.py`, R = 3,656 reproduced, gcheck PASS) all
    68-82 operands of every total sit outside its D10 frame.  Building the totals inside the frames would take
    hundreds of extra copies, since each line lies in 3 or 9 incomparable D10 frames.
- Closed this session: 10-frame tops, full-rectangle tops, target taps, R420-type copies (alignment needs 52
  punctures), sharing partitions (no alignment gain), random sub-110 decoder searches over sections.
- Still open (none promising):
  - a decoder below 110 (`dec108/dec_flat.py`, coordinate-flat pieces under the C_11-containment
    reformulation, was running);
  - an assembly scheme for misaligned halves at about E8's register cost per incidence;
  - an all-word lower bound that would close the question rigorously.

**Session 6i priority list (refines 6h; details in 3g).**
- Calibration: the generic chain pricer puts R420-like structures as follows.

  | structure | E8 | I_{11,1} | I_{13,1} |
  |---|---|---|---|
  | R = 3.5v, stops 5/2/5, all frame-0 | -5.3% | -10.7% | -11.4% |
  | same, z-groups (floor frame-0, rest entrance 1) | +2.8% to +6.3% | -3.3% to +0.3% | -4.0% to -0.7% |

  - The frame-0 E8 row matches the real R420 (-4.6%).
  - So a z-grouped R420 would be an E8 frontier.  For Lorentzian systems, z-groups only bring an R420-quality
    middle up to a tie.
- A. *A middle better than R420 per incidence* (the only remaining Lorentzian lever).
  - Budget with z-groups: about 4.5-4.8 registers per line including sources (R420: 4.5).
  - I_{11,1} carries about 2x the load and is unaligned (>= 52 punctures).
  - Prior per-design walls are >= 5.5 registers per line.
- B. *E8 lever at scale* (stepping stone, not a Lorentzian result).
  - Restructure R420 so that its 180 empties are z-group-local or in-chain scratch.  Model: +3-6% over
    P111-tuned.
- C. *Decoder:* Z11 rank-12/13 row-weight minimisation (`sdec/z11sat.py`, MINW=1).  Rows of weight ~50 would
  halve the load at +10-11 cst.
- D. *Systems:* only a new system with E8-like alignment and x <~ 0.5 at h <= 13 would change the picture.
  - Every system examined (I_{n,1}, punctured, h = 8/9, mixed norm, twins) is capped or misaligned.

**Session 6h priority list (supersedes the older ordering for the Lorentzian question).**
- A. *Entrance lever at scale.*  Every Lorentzian route in the models needs 25-50% of helpers as entrance-ranked
  hubs.  This is unproven beyond E1's single helper, so demonstrate it first on E8 (a lever-native redesign),
  then port it.
  - Exact conversion test on R420's own word (`scratchpad/r420lev/convert_e8.py`, the session-6g timeline rules):
    **0 of 420 helpers convert as built.**
    - 240 are the needers that targets read at t^perp (rank 7) in phase B.
    - 171 fail on reader timing or frames: a quad partner's chain passes through its own cell, not the helper's.
    - 9 are retained totals.
  - So the lever needs a ground-up redesign: helper writes moved into phase B after the readers' pure reads,
    with entrance frames on every reader's chain.  This holds even for R420.
  - R420 helper roles (exact profile).
    - Carriers are first written at rank 1 (the line).  Each is then read by its cell-mate at rank 2, by 3-4
      quad partners at rank 4, and by a D6 node or a target at rank 6/7.
    - Entering at the cell fails: the quad partners come from other cells.
    - Entering at the quad fails twice:
      - targets (chain 0 -> cell -> t^perp) never pass through quads;
      - quad-entrance sum registers would need about 6 line registers per line at quads, against the 3 per line
        that R420 packs.
    - A lever-native E8 word is therefore a new design, not an R420 edit.
    - Sketch of a first lever-native step (not built):
      1. Each D6 = {t,e}^perp lies in exactly two target perps (D6^perp holds only t and e).  If both users route
         0 -> cell -> D6 -> t^perp, a hub entering at D6 (rank 6, width 2) can be pure-read by both and written in
         phase B with the shared content.
      2. A chain holds one rank-6 frame, so each target gets one such hub.  At best 60 D6 hubs serve 120
         targets, replacing 120 needers.  The other two needers per target stay.
      3. Open: whether t's and e's Q-deliveries can be merged into the shared hub content, and the re-pricing.
- B. *A <= 4-4.5v middle for I_{11,1} / I_{13,1}* at E8-like stop counts.  No mechanism is known.  The
  constraints are a 3.2x per-line load, misaligned partitions, and carrier-limited injections (section 3f).
- C. *Frame-free near-extremal systems.*
  - h = 8 needs 85-91 lines with a cst-56 decoder; h = 9 needs 117-119.
  - Every framed system is capped well below (h = 8: <= 57; h = 9: <= 111).
  - Sampled near-extremal F2 multisets all fail local realisability (`h9x/genlocal*.py`).
  - A proof would close both windows.
- D. *I_{11,1} decoder < 110.*
  - The non-symmetric lazy-cut ILP (`dfam/declazy.py`, 15,246 structured flats, cost <= 109) was stopped after 41
    iterations: every candidate left 207-220 of 220 targets unserved.  Inconclusive; the cuts are too weak.
  - Decoder minrank equals B0's rank for I_{10..13,1} (SAT, `h10b/rank10.py`), so only lower-rank pieces could
    help.

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
       - **Min-release (`lttri_rho5_minrel.py`, node 0, every sub-problem solved to optimality):** at least 8 of the
         54 coverage-forced memberships must be released, and at least 2 of the 3 users must release (OBJ=users
         optimum 208 = 2 users + 8 lines).  A transversal T(x,y,z) (x in A) lies in a triangle node's perp iff that
         node splits {y,z}, so a multiplicity-1 transversal lies in no other triangle node of T(A).  Every target
         already sits in exactly 4 triangle nodes, so each releasing user must trade one triangle section for a
         non-triangle section.
       - **Counting (modifications of this design):** removing r triangle nodes creates <= 3r releasing targets,
         each in 3 retained nodes, so at most 9r/2 retained nodes can be zero-cost; all zero-cost needs r >= 40,
         i.e. 120 non-triangle sections (`lttri_remove.py` attains r = 40, so it is optimal).
       - **But leaving one node cannot release (proven, `lttri_needrank.py`):** for all 660 (node, user) pairs, the
         lines of R(T(X)) covered only by that node among X's 4 nodes (25 lines) have rank 8 = the rank of the node
         perp.  A replacement section must contain them, so its frame IS the old frame, and it holds no transversal
         released at another node.  So the r = 40 configuration is dead; releasing targets must leave >= 2 triangle
         nodes (`lttri_remove.py` with MINLEFT=2, `lttri_leave2.py` for which frame pairs can replace two nodes).
       - **Leaving two nodes cannot release either (proven, exhaustive):** over all 14,945 rank-3 frames through
         T(X), for every pair of left nodes the only frame pair covering the 50 needed lines is the original pair.
         Checked for the 3 target-orbit representatives of the design's 55-element affine symmetry group
         (x -> ax+b, a in {1,3,4,5,9}), so it holds for all 165 targets.  `lttri_leavek.py` (CP-SAT) agrees.
       - **Leaving three nodes CAN release** (`lttri_leavek.py 3 0`: feasible for all 4 choices).  But then each
         releasing target sits in only one retained triangle node.  Counting: zero-cost retained nodes <= r/2, so
         the triangle lower bound only falls from 220 to 220 - 1.5r, while 3r non-triangle sections appear.  Full
         zero cost needs r >= 147 of 220, so the triangle design essentially dissolves.  **Verdict for (c'):**
         mixed covers built from this triangle design pay >= 1 register per retained node except through
         near-total replacement.  This is no longer a triangle-family idea; it is the general design problem.
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
