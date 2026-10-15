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
11 totals at rank 10), not words.  A word must reach roughly **R <= 600 with one-level-like chains** to beat
P111-tuned.

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

**Assessment.**
- **heuristic:** no Lorentzian frame-cell architecture found beats P111-tuned.  The binding reason is structural:
  sections, exclusive parts and triple-overlap blocks are 2-5x larger than the largest shareable nodes (~20-30 lines),
  whereas in E8 the triple part B' (12 lines) is itself a node.
- **proven gap:** a rigorous all-word bound is still missing.  The union-coverage LP only gives 660, and exact-assembly
  bounds were derived only for the classes above.

## 4. Next goals (priority order)

1. **Frame-routable source system** (the only route to an R420-style cheap top).
   - Find a good-frame system, with defects allowed, whose own (or freely chosen) frame sections are routable: every
     u in {t,e}-perp has a system cell inside it.
   - Then R(t) = 3 shared section totals + mate corrections, giving 3 deliveries per target with free in-chain reads.
   - Previous local search (lsa5: Z11, own frames, objective 1000*no_route + defects) got stuck above 2000 no-route
     pairs; redesign it.
   - Structured idea: apex block pairs D(A,p) ⊥ D(B,p) (5|5).  Each D5 hub splits into 5 PPTT frames {P(ij), T(ijp),
     P(kl), T(klp)}, the analogue of E8's D4|D4 blocks.  Parity forces defects; measure unroutable pairs for block-
     structured systems first.
   - Success target: unroutable pairs below about 50, and the mate-correction system solvable.
2. **Laminar "public frame" middle.**
   - Small flats lying inside many sections, where broadcasters and collectors meet.
   - Every collector's reads must lie on one nested chain (the analogue of R420's quads).
   - Search jointly over broadcaster chains and collector chains; coverage counting allows it (frames with about 10
     lines and about 7 users suffice).  Nesting is the binding constraint.
3. **Exact-read-aware system search.**
   - Score systems by an LP relaxation of the read set-packing (`lexact.py` model) inside `lsa6.py`, not by pool
     counting.  Current best exact floor: 567.
4. **Close CP-SAT gaps** for the best systems (559-567): longer runs, more workers, cuts.
5. **Apex route.**
   - Find frame-legal ways to share D8 totals: 495 totals, 2 users each.
   - P targets need 9 apex terms, so a P-specific top is needed (P(bc)-perp contains E8(M)).
6. **Pricing gate.**  Any candidate word must reach R <= ~600 with one-level-like chains; price it with gcheck
   `--price` and compare with P111-tuned 0.001733427039589844.

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
