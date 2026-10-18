# SESSION SUMMARY (2026-10-18): I_{13,1} architecture search — findings, corrections, and state

Prepared by DaysSky with assistance from Claude.  Everything here is scratch research; labels:
**proven** (exact/exhaustive computation), **modeled** (pricer/ILP within a stated model), **estimate**.

## CORRECTIONS (post-verification; supersede numbers below where they conflict)

- **Frontier moved (parallel session, research/e8-bit-p111-r434): the new best c is 0.0017443859508
  (+0.57% over E1, R = 434).**  Re-priced against the NEW frontier: the dead-573 model design's kappa
  (0.0017529) is +0.49% ABOVE it; kappa crosses the new frontier at dead = 584 (R = 1,312 = 3.60v).
  All "break-even ~685/935/705" numbers below refer to the OLD frontier and shift accordingly (~+11
  registers of allowance each).
- **ALL-WORD LOWER BOUND (skeleton, session-end; allword_lb.py).**  Counting argument over any word:
  total line-slot transfers T must cover (a) the system constant sum_t |R(t)| = 70,356 (mean perp
  193.3), plus (b) each non-source register's own content arriving somewhere: T >= 70,356 + (R - v).
  Visit cap: T <= 13 R (one frame per dimension, gcheck climb rule).  => 13R >= 70,356 + R - 364
  => **R >= 5,833 = 16.0v for ANY I_{13,1} word**; kappa at that R (best histogram shapes) =
  0.0005923 = **-66.0% vs the new frontier**.
- **THE BOUND IS BROKEN — E8 control fails it (post-session check).**  Applied to E8 the same
  argument gives R >= (120 x 63 - 120)/(8 - 1) = 1,063 > R420 = 420, contradicting the verified word.
  The flawed step is (iii): "T >= sum_t |R(t)|" counts each target's need separately, but one built
  sub-sum (a shared quad total, read by 12 targets) discharges many targets at once — E8's true
  demand incidence is 9/line, not |R(t)| = 63/line.  What survives: (i) the visit cap T <= hR and
  (ii) the assembly-tree facts are fine; the per-architecture closures below stand unchanged (the
  PG-top and half blueprints genuinely pay their MEASURED incidence counts 28,808 / 13,508 — those
  come from the demand structures themselves, not from the flawed step).  A real all-word closure
  needs a lower bound on the SHARED-CONTENT minimum (min over all demand decompositions of total
  incidence) — that is exactly the open assembly question (6i lever A), NOT settled by this counting.
- **II19 BREAKTHROUGH TRACK (session-closing; the strongest result of the program).**
  II19 = E8 (+) U levels 0-1: 361 lines, h = 10, ceiling 1.84x E8.  Measured gates: span OK
  (all classes), covers OK (c_t 4-12; level-1 targets close at weight 4 exactly), partition
  FOUND (15 disjoint flats, ZERO leftover: sizes [31,45,46,46,47,50,51,60x8] — the R420-style
  zero-waste assembly skeleton), budget 15.0v at cst 90 (13.4v at cst 120 — decoder-robust),
  level-2 escalation closed (v=929 stalls: demand outgrows coverability).  PROJECTION-BAND
  PRICING (mix.price, cst 90, best shapes): c_t 8/dead 100 -> R 7.3v, kappa +69.2%; probe-
  measured c_t 10.3/dead 300 -> 10.1v, +34.1%; worst case c_t 12/dead 600 -> 12.7v, +13.3%.
  EVERY band clears the frontier 0.0017444.  HONEST GATES REMAINING: the coordinated design's
  true Sigma c_t (running at session close), the assembler's true middle count (partition
  bounds it low), decoder design (cst robustness proven, construction open), gate/frame
  legality simulation, and the exact pricer at the TRUE histogram — the difference between
  'prices above the frontier in every measured band' and 'a frontier word' (the pricer-trap
  lessons of this session apply in full).
- **THE INLINE-DELIVERY GRAMMAR — THE VERDICT FLIPS (ii19_tiles2.py + threshold analysis).**
  Popularity-first refinement converged at pool 5,362 (fixed point; 92% of reads ride the
  top-3,000).  KEY STRUCTURAL FACT: single-use tiles are not worth registers.  INLINE
  GRAMMAR (E8's mechanism): keep tiles used >= 2x as registers (2,230), INLINE single-use
  tiles' contributions as raw SOURCE-LINE reads (work, not registers).  R = 2,337 (R_id,
  measured) + 2,230 (tiles) + 90 (decoder) = 4,657 = 12.90v — UNDER the 15.0v budget (5,414)
  and the 13.4v pessimistic (4,846).  PRICED at the measured histogram (H = R - 3v
  convention, shape grid, best shapes [9]/[9]/[9] at cst 72): c = 0.0022990 (+31.80% vs
  frontier) corrections counted; +36.73% corrections free; deeper-inline (>2) threshold:
  +57.89%/+65.02%.  Every number in this band is from a COMPLETED computation (design
  361/361, tiling 2,375 pieces, refinement converged, threshold measured) — the pricer-trap
  lesson applied.  GATE 1 (WORK DENSITY) — CLOSED FAVORABLY (computed from ii19_tiles2.pkl): total assembly
  arrivals 42,597 (tile reads 26,552 + inline line reads 7,658 + tile-build reads 5,638 +
  leftover singles 2,749) vs capacity h*R = 10 x 4,657 = 46,570 -> utilization 91.5%
  (E8 R420 reference: 3,000/3,360 = 89.3%; arrivals/line 118 vs capacity/line 129 — E8:
  25 vs 28).  The two-sided frontier condition (the framework that killed the I13 designs
  at 192/line unshared) passes: the inline grammar is arrival-tight like a frontier word.
  The price model is register-census-centric (pricer.py read and verified — identical
  conventions for E8 and II19).  REMAINING GATES: (2) Stage-4 legality simulation (inline
  source reads at legal gate frames; tile-register ranks); (3) decoder construction
  (cst robust through 120).
- **GATE 3 (DECODER) — THE KILL: THE DECODER RANK OBSTRUCTION (ii19_decoder_rank.py,
  ii19_decoder2.py, headroom scans).**  The format's decode structure (geom.py convention):
  GF(2) labels u_s with u_s . u_t = 1 iff (s = t or G[s,t] = 0) — U U^T = M — REQUIRES
  width >= rank(M).  MEASURED: rank(M) = 241 for II19's full 361-line system (each level
  class alone: rank 9, E8-grade; the cross-class twist (alpha,1,0).(beta,0,1) = alpha.beta+1
  explodes the rank 24x beyond the natural family's ~10).  The congruence construction:
  309 columns, W W^T = M verified; centre totals 34/309 closed (legality failing; the E8
  level-0 control: 0/9 closed — the congruence is not the natural structure, but the
  WIDTH BOUND is construction-independent).  THE HEADROOM SCAN (decisive): at EVERY H
  convention (3,484 / 3,574 / 3,757), cst [1]*241 — the IMPOSSIBLE best case, every total
  rank 1 — prices c ~ 0.0007 = -57.6% to -59.6% vs the frontier; every realistic structure
  (rank >= 2) NO ROOT.  The width-241 decoder is fatal at any total structure and any
  convention.  VERDICT: II19 is CLOSED by the decoder rank obstruction.
- **RETRACTION/SUPERSESSION:** the inline-grammar band (+31.80% at R = 4,657, committed
  f0c88b61) assumed a ~10-register decoder (cst [7]*10); the rank computation refutes that
  assumption — the true decoder costs >= 241 registers.  The +31.8%/+36.7% bands are
  SUPERSEDED.  The resource-gate record STANDS as measured: Sigma c_t = 2,698 (R_id 6.5v),
  tile pool 2,230 (R = 4,657 = 12.9v under the resource budget), arrivals 91.5% (E8-grade).
  II19 passed every gate it could pass; the decode structure is the kill — the same rigor
  as the I13 four-part obstruction, now for the even-unimodular II family.
- **LESSONS + OPEN QUESTIONS for future sessions:** (1) the decoder rank screen
  (rank(M) vs the natural width) is a MINUTES computation that gates everything — run it
  at the census stage BEFORE architecture development (the II19 arc could have been
  screened at its start); (2) whether a NON-STANDARD decode mechanism (staged/multi-layer,
  exploiting the level structure — each class decodes at width 9) could exist for II19 is
  a format-redefinition question, not a word in the existing format.  The frontier stands
  at E8 R434 (+0.57%), unbeaten.
- **THE II19-NATIVE DECODER (user directive: "push II19, nothing E8-dependent") — THE
  RANK OBSTRUCTION DISSOLVES; THE HONEST WINDOW-PENALTY LAW CLOSES II19.**
  (a) THE TRUE DECODER DEFINITION (HANDOFF 1068, gcheck.py): B = U W^T with B_tt = 1 and
  B_ts = 0 ONLY on non-orthogonal pairs — asymmetric labels, FREE on orthogonal pairs.
  The "decoder rank obstruction" (rank(M) = 241) tested the WRONG convention (the
  symmetric full-pattern U U^T = M = J + G — only the naive B0).  THE CLASS-BLOCKED
  DECODER (ii19_classdecoder.py): B = the within-class symmetric blocks (3 x the
  root-lattice pattern) + the special singleton — VERIFIED VALID (diagonal all 1, zero
  support violations, rank 28 = 3x9+1 exactly).  The word: 3 disjoint root-lattice-class
  subwords + glue: branches 722, middle 3x194, retained 28 (cst 235), junk = the
  within-class perp (mean 62.8, the special line trivially 0).
  (b) THE MASKED-DEMAND FREEDOM: rows need not be the full perp (HANDOFF: "not
  necessarily all of R(t)"); the counting bound rows >= v/c - 1 ~ 12 gives f >= 0.19.
  (c) THE MODEL-BIAS DISCOVERY (a fifth artifact class): the mix.price model prices the
  P111 structure at 1.185x and the R420 at 1.313-1.570x their published TRUE c's —
  the model is OPTIMISTIC (compressed [7]/[9]-shapes price better than true fine climb
  structures; small-r mass is heavier in the root equation).  ALL the session's
  model-priced bands are optimistic by ~1.2-1.6x.  HONEST PRICES: true-word histograms
  via pricer.price only (the controls reproduce the published c's exactly).
  (d) THE HONEST CLASS-WORD PRICES (mass-exact identity hists, E8-proportioned shapes,
  hyper-sensitive: +-0.3% mass -> +-35% c): f=1.0: 0.000981 (-43.75%); f=0.5: 0.001112
  (-36.23%); f=0.25: 0.001192 (-31.65%); f=0.19 (the counting bound, mass/v = 42.5 BELOW
  the R434's 43.5): 0.001213 (-30.45%).  The mask gains only ~13 points of the 44-point
  gap — the penalty is STRUCTURAL.
  (e) THE WINDOW-PENALTY LAW (the coherent close): verified true c's fall steeply with h:
  h=8 (E8 R434): 0.0017444; h=10 (the II19 class word, estimated): ~0.0010-0.0012;
  h=11 (word_blkA4, verified): 0.0004927; h=13 (word13, verified): 0.0004433.  The fixed
  2v(h-1) mass (18/line at h=10 vs 14 at h=8), the m = 1+L(h-1) window (82 vs 64), and the
  width-10 hosting children (rank-8 leftovers vs the E8's rank-1) are the mechanism.
  THE CEILING MODEL (v/(h+4)^2, II19's "2.21x potential") IS NOT REALIZABLE — the I11's
  verified word (ceiling 0.98x, true c -71.6%) already showed the gap.  VERDICT: II19's
  class word is a REAL, VALID word family priced -30 to -45% vs the frontier; the frontier
  lives at h=8 (E8 R434), unbeaten.  Future: the true build (gcheck-exact) pins the exact
  c (+-few points, cannot close -30%); frontier work remains E8-internal.
- **ASSEMBLY VERDICT (ii19_assembly_par.py, two-phase 10-worker).**  The TRUE naive
  hierarchical middle of the v1 design: distinct lvl5 1,875 + distinct lvl4 5,534 + gates/8
  2,619 = 10,028 registers -> R = 12,365 = 34.3v, vs the 3,077-3,275 mids budget — DEAD by
  2.3x.  lvl4 reuse {1: 5506, 2: 28}: sub-flat sharing does NOT materialize; intermediates
  are as pair-specific as the pieces.  THIS SUPERSEDES the trueprice's optimistic content//17
  band (4,136 mids -> +1.79% with free corrections): the measured naive middle is 10,028 and
  v1 prices ~-45% vs the frontier.  HONEST CAVEAT: the assembler's random sparse sampling
  undercounts achievable sharing — a deliberately coordinated assembly is open, but the
  burden of proof is on it.  THE E8 CONTRAST (the fix identified): E8's pieces are small
  XORs of SHARED CARRIERS (quads = 2 cells; carriers are the branch registers) — middle
  nearly free by GRAMMAR.  A v3 grammar: smaller pieces (rank 4-5) built from 2-3 shared
  carrier totals (rank 2-3 flats) — projected carriers 500-800 + gates ~ 700-1,000 middle
  registers, UNDER the 3,077 budget.  v2 (running) attacks content at the piece level;
  its ledger informs whether v3's carrier grammar is the move.
- "573 proven optimal" = optimum over menus capped at 200 covers/demand, with leaf fills free.  The
  model's true optimum is 0 (all-leaf); the model does not charge leaf fills, which are branch/delivery
  registers and are NOT free.  Read every "cost" in this file as capped-menu, leaf-free accounting.
- The saved `chosen` was regenerated after an index-bug fix (deadmin_primal.py); corrected design:
  619 used pieces (46 leaf), 618 distinct frames (frame-sharing diagnosis still holds).  Feeding
  recomputation: content sizes sum 16,029, merge-ins 15,411, frames/line 43-188 (median 76).  The
  "~2,500 mids" is an ESTIMATE, not a bound (and shifts if leaf delivery is charged instead).
- The +13.6% block-group rows are session 6i and I_{11,1}; the I13 "+5.9%" rows used I11's 450 movers
  and ignore §3h feeders (I13 needs ~886 movers) — they do not bound the I13 blueprint.
- halves_assembly v1 (0 pieces) was a model artifact; v2 (content pieces) returned OPTIMAL 0 non-leaf
  / 363 leaf pieces = the trivial all-leaf optimum (any half = 1 line + leaf fill of the rest, charged
  0).  **The halves-assembly-budget question is NOT answered by this model**: the cost lives in leaf
  DELIVERY (pushing ~16k line-slots into 576 half-rooms), which the set cover does not charge.  The
  blueprint-level computation that does answer it: per-target reading-chain registers (halves_struct.py
  min_private: 6 halves/target on 3-dim chains 9/10 -> 11 -> 12) + the mover count for the reading
  frames.  That is the next session's first task.
- **Blueprint ledger (session-end, honest):** 576 half-registers (each half's closure lies inside ALL
  its readers' t-perps — delivery free, 2-6 readers), pair-mid feeding 241 (greedy shared-pair) to
  6,754 (no sharing), Q 91, branches 728, movers ~886 (I13, not I11's 450), §3h feeders on top:
  **total R ~ 3,200-3,700 = 8.8-10.2v**, and break-even needs R <= ~1,400 (3.9v).  kappa at ~10v is
  ~0.00040-0.00046 (-70%).  **The maxpairs half blueprint does not reach the frontier either** —
  the half layer alone (576 + 241 + 91 + 728 = 1,636) is over the whole-word budget before movers.
- The bug diagnosis in the old halves paragraph below is wrong (v1 required whole flats inside the
  half, which are almost never subsets of the half's content — not "candidate filter" issue).

## Sign convention (verified; do not repeat this session's error)

**kappa = c is the exponent saving in T(n) = O(n (log n)^{1-kappa}).  HIGHER c IS BETTER.**
P111-tuned c = 0.001733427039589844 is the best word; E1 (frontier) c = 0.001734473240795253742474.
More helpers raise c (up to the hosting wall); better histograms raise c at fixed count.
The Lorentzian question: can a Lorentzian word MATCH or EXCEED E8's c at a legal register count?

## What this session built (all in research/i13-partition/, python = ~/.venv/bin/python3)

1. **I13 geometry + censuses** (`base13.py`, `lgeo13.py`, `reach13.py`):
   - 70,785 good 4-frames (TTTT 51,480 + PPTT 19,305), all nondegenerate; P 78 (even), T-T degree
     sum 702 (even) — both I11 parity obstructions vanish.
   - Reach table (max perp size by frame rank): 2:138, 3:77, 4:56, 5:31, 6:30, 7:15, 8:12, 9:3
     (I11: 8:6 — I13's rank-8 reach is double).
2. **Partition** (`part13.py` Z13-invariant INFEASIBLE; `part13free.py` no-symmetry **OPTIMAL**):
   a partition of all 364 lines into 91 good frames (39 PPTT + 52 TTTT), `partition13.pkl`.
   **This rediscovered session 6h's PG(2,3) partition** — already known (`code/s7/i13n/pg23part.py`),
   already analysed (misaligned: per-line cover 6-7 vs E8 3; misalignment 23,348 odd pairs) and
   already built into the best verified I13 word (R = 7,314, -74.4%).
3. **Dead-minimizer (the session's main program)** on the PG frame top's 610 demands
   (`deadmin_instance.py` -> 223,755 candidate flats; `deadmin_menus2.py` -> 122k covers, 57,030
   distinct pieces; `deadmin_lp.py` LP floor 150.05; `deadmin_primal.py`):
   - **proven (CP-SAT OPTIMAL): 573 non-leaf pieces assemble all 610 demands** (content-piece model:
     disjoint flat-sum covers <= 4 pieces + free leaf fills; pieces shared across demands).
   - `deadmin_primal2.py` rank-weighted variants: 577-589 pieces with shallower profiles.
4. **Pricer scans** (exact pricer via `code/s7/exitmix.py`, `mix.py` — path fixes applied to those
   files): full kappa-vs-shape landscape at dead = 573, R = 1,301 = 3.57v:
   best histogram kappa = 0.0017529 (**+1.06% over P111-tuned**) at branches (1,1,2,3,6),
   dead pieces (2,3,8); sensitivity across shapes +5.7% .. -1.4%.
5. **The feeding-layer reality check (the decisive negative)** on the actual optimal design:
   - 824 DISTINCT piece frames for 827 used pieces (822 singletons: no frame sharing);
   - every line's content must reach 22-267 piece frames (median 92); branch copies (2/line, ~5
     nested stops) cover ~3,640 frame visits against 18,781 required merge-ins;
   - **mid-layer lower bound ~2,500 extra registers** -> R ~ 3,800 = 10.4v -> kappa far below
     break-even.  The +1.06% assumed free feeding; it is not free.  Same verdict class as I11.
   - **Root cause (new, precise):** the set-cover model shared PIECES but the optimum chose DISTINCT
     FRAMES per demand.  Sharing pieces != sharing frames.  Any future attempt must charge for
     distinct frames in the ILP objective ("frame-aligned" designs) — this is the algebraic content
     of R420 alignment (E8: 70 quads + 180 D6 frames for 180 cells; I13 PG top: 824 frames/827 pieces).

## The honest bottom line for the PG-frame-top architecture

- Top assembly alone: 573 registers (proven optimal within the model).
- With feeding: >= ~2,500 extra (incidence bound) -> the architecture lands far below break-even.
- The verified word13 (R = 7,314) remains the best I13 word; nothing this session beat it.

## The live lead at session end: the 6h rank-7 block-group blueprint

- Delivery: rank-7 f-perp group frames shared by 12 targets (star block) / 8 (Pasch pair) — the
  strongest delivery sharing known for I13.  6h priced 450 movers + 660 group helpers at
  **+13.6%** (best shape) BEFORE assembly costs; today's scans: at 1,250 total frame-0 registers
  the blueprint prices **+5.9%**; the assembly layer must fit in ~650 registers for kappa > 0.
- **This session's last computation (halves_assembly.py, COMPLETE but BUGGY):** built the 576
  distinct halves of the maxpairs partition (301 x 16 lines, 262 x 30, 13 x 64;
  `halves_maxpairs.pkl`) and ran the same set-cover.  **Result OPTIMAL objective 0 is a BUG**: the
  menu builder returned only leaf-fill covers (1 cover per half, 0 pieces) because the candidate
  filter `A & h` used A as a subset of the half's CLOSURE frame but the DFS needs pieces whose
  LINES are inside the half's CONTENT (A & ~S == 0 tests the frame, not the content overlap with
  the half E; dem_cand included flats A <= S with A & h possibly 0, and covers_of requires covering
  E's lines but candidates A with A & E == 0 can't cover, so every DFS hit the leaf-fill branch
  immediately).  **FIX NEEDED: dem_cand[h] must filter A & h != 0 (it does: `A & h`), so the real
  bug is elsewhere — check whether `cl(h)` for a 16-line half is huge (rank 10 room) making
  candidates A mostly disjoint from h, and whether the DFS's first-uncovered-line loop actually
  finds no candidate covering it (then leaf fill is correct but the model then says: halves are
  served by leaf fills = in-chain line reads at the half's room — which IS a legitimate reading:
  the halves may not need assembly at all if the group targets read lines directly... resolve what
  leaf-fill means here before trusting either reading).**
- Pricer sanity at 1,100 frame-0 + 660 group helpers (7,11): **+5.89%**; at 1,450: -8.8%.
  So the blueprint's assembly budget for kappa > 0 is ~650 registers.

## Other runs still suspended (resumable)

- `n13allcovers.py P` (PID 4410) and `T` (PID 4420) — SIGSTOPped at ~31 CPU-min: exhaustive 4-covers
  of R(t) by rank-3-frame perps per Stab(t)-orbit (P: 24 orbits, T: 29 orbits enumerated so far).
  Resume with `kill -CONT 4410 4421`.  Purpose: whether I13's rank-11-section 4-covers have smaller
  minimum overlap than I11's 33 (disjoint covers would reopen the 4-section class).

## Key session lessons (for the next session)

1. **Always verify the sign of kappa against README before interpreting pricer output.**  Higher = better.
2. Histogram pricers price REGISTER POPULATIONS, not functionality: a kappa number is meaningful only
   for a register set that actually implements the word (feeding + delivery included).  The +32% at
   dead 0 and the +28% at entrance-rank pieces were both functionality-free illusions.
3. The binding quantity in every I13 architecture is FRAME SHARING (delivery + assembly), not piece
   count.  Frame-aligned ILPs are the right next tool.
4. "X is optimal" claims must name the model (what is free, what is charged); every surprise this
   session came from an unstated free lunch (leaf fills, feeding, entrance legality).

## Files (research/i13-partition/)

base13.py, lgeo13.py (geometry, S13 canon); part13.py/part13free.py/partition13.pkl (partition);
reach13.py/.pkl (reach table); n13allcovers.py (covers, suspended); n13nodes.py (killed, size-2
flats: 57,278); deadmin_instance.py/.pkl; deadmin_menus2.py/.pkl; deadmin_lp.py;
deadmin_primal.py/.pkl (573 design); deadmin_primal2.py (+ _a000/_a025/_a05/_a10 rank-weighted);
halves_maxpairs.pkl (576 halves); halves_assembly.py (BUGGY — see above); RESULT.md (earlier
verdicts, now superseded by this file on the feeding-layer and sign issues).

## Suggested next steps (priority order)

1. Fix halves_assembly.py semantics (what does leaf-fill mean for a HALF: the group targets read
   the half's lines in-chain at their group frame — that is the 6h blueprint's own mechanism, so
   leaf-fill may be legitimate; make the model match the 6h mover/group-helper structure exactly
   and re-price).
2. Frame-aligned ILP: charge distinct frames (pieces + 3 x new frames) in deadmin_primal and see
   the true two-layer optimum of the PG top; compare against the 6h blueprint's sharing.
3. Resume the cover enumerators for the 4-section class overlap census.
4. Do NOT build on the +1.06% / +24% / +28% histogram numbers — all three lacked a layer.

## THE E8 SPARSE-DECODER ARC (phases 1-3; e8_rowspace.py, e8_enrich.py, e8_sparse_word.py)

- **PHASE 1 — the rank-9 space PROVEN rigid (100% exhaustive):** all 512 codewords of B0's
  row space: weights {0: 1, 56: 255, 64: 255, 120: 1}; every target's ONLY legal codeword
  is its own full perp (weight 64).  No sparse decoder at rank 9 — proven, not assumed.
  (RAM note: the first run had a broken basis reduction — 48 pseudo-basis vectors, a 2^48
  enumeration, a 22 GB explosion, killed; the dict-pivot elimination is the fix, plus an
  abort guard.  The macOS ru_maxrss is in bytes — the old 'rss MB' labels were KB.)
- **PHASE 2 — THE SPARSE DECODERS EXIST (the HANDOFF's lever realized):** the cancellation
  construction r'_t = r_t XOR ind(perp(t) & perp(x_t)): rows legal BY CONSTRUCTION (the XOR
  only removes bits from the full perp).  Every orthogonal pair's common perp is EXACTLY
  30 lines (a striking uniformity: 7,560 pairs, one size).  Greedy partner curve:
  k=1: rows 34, rank 113 | k=2: rows 30, rank 33 | k=3+: rows 4, rank 57 (saturated).
  The k=2 candidate: demands 30 lines/target (vs B0's 63) at rank 33 (vs B0's 9).
- **PHASE 3 — THE ECONOMICS (three walls, all measured):**
  (a) THE SHARING LOSS: the uncoordinated greedy randomizes the junks — 120 distinct sets,
  pairwise overlaps mean 9.2 (the I13 pair-specific signature): the E8's shared middle
  calculus is destroyed; the honest middle stays ~120-160, not the linear-scaled ~90.
  (b) THE CST PENALTY: the retained 33 registers (cst ~200 est.) vs B0's 9 (cst 72): at
  R-parity the decoder-side cost exceeds the load savings.
  (c) THE PRICE REGIME: the frozen-shape family reproduces the R420's published c EXACTLY
  (0.001653826988146798944268, ratio 1.0000 — the perfect control) and prices the R434
  parameters at 0.0016257 (the R434's own hist differs: the 7.3% calibration).  But the
  ENTIRE k=2 grid (R 323-403, mass/v 36.8-43.4) returns NO ROOT: the root's existence is
  R-driven, not mass-driven — the model roots only at R/v >= ~3.5 (the published words:
  R420 = 3.50v, R434 = 3.62v, P111 = 3.95v).  The lighter sparse words (R/v 2.7-3.4) fall
  in the IDENTITY-WORD CLASS: the model's refusal band.
- **THE VERDICT:** within the regime, the k=2 word prices BELOW the frontier (the cst +
  the sharing penalties); outside the regime, unpriceable (the hub's template question —
  the same open question as the identity word: whether the pipeline could ever use the
  lighter words).  THE FRONTIER (E8 R434, c = 0.0017444) STANDS UNBEATEN.
- **THE LIVE REFINEMENTS:** the frame-aligned cancellation (the coordinated partner choice
  preserving the E8 sharing — the R420's own x(t) 4-frame partners); the exact minimal-cst
  factorization of the k=2 decoder; the regime question itself.
- **THE SESSION-LEVEL DISCOVERY:** THE FORMAT'S VALIDITY LIVES IN THE PIPELINE/MODEL LAYER
  (the R/v ~ 3.5 regime), NOT THE CHECKER LAYER (the identity word passes gcheck!!).  The
  checker hierarchy: gcheck (flow) < xcheck (flow + the delivery decomposition) < the price
  model's regime (the pipeline's asymptotic requirements — the hub's #463/#510 template:
  THE OPEN FORMAT-THEORY QUESTION).  A gcheck PASS is necessary, not sufficient.

## THE II19 FRONTIER PUSH — h=10 LADDER CLOSED; THE 2-CLASS (h=9) CROSSING DISCOVERED (ii19_crossing.py, ii19_2class_crossing.py)

- **(a) THE h=10 LADDER: CLOSED (measured, mass-exact).**  The SS1215 "-8 to -11%" figure was
  the 51-mass-light artifact — the control in ii19_crossing.py exposes it: the mass-exact
  reconstruction of the SAME hist prices the class word at 0.000971703 (-44.3%), consistent
  with SS1217's own mass-exact correction (-42.35%).  The full R-ladder (810-1350, mass-exact,
  delta-1 and delta-2 extension variants): MONOTONE (smaller R -> better c), flooring at
  -25.5% (R=810, counting-bound-violating) / -27.7% (R=860, the counting bound: demands
  >= 13 at c=28).  NO CROSSING at h=10: the window (m=82, 2v(h-1)=6,498, width-10 hosting)
  is the measured wall.  The window-penalty law STANDS at h=10.
- **(b) THE 2-CLASS SUBSET (level-0 + level-1a: 240 lines, h=9, m=73, the rank-18
  class-blocked decoder, the E8-pattern 63-line demands) — never priced with this
  machinery.**  The HANDOFF's "h=9 closes" verdict covered only the small framed systems
  (<= 111 lines); this is a 240-line system — different territory.  The window at h=9:
  m=73, the window mass 16/line (vs h=10's 18, h=8's 14).  THE CROSSING CURVE (mass-exact,
  the transplant family): R=858 (the full E8-transplant x2): -21.15%; R=600: -3.01%;
  R=572 (the counting bound, demands ~13): -0.53%; R=560: +0.58%!!!  THE CROSSING IS AT
  R ~ 566 — AT THE COUNTING BOUND'S EDGE.  THE CONTROL: the E8 R420 true-hist reproduces
  the published c to 15 digits (0.001653826988147) — the pricing machinery is exact.
- **(c) THE HONEST FLAGS (the artifact discipline):**  (i) the shallow-end hist model (the
  transplant family x2 scaled) DISTORTS at mid << 180 — the mass-exact closure goes NEGATIVE
  (the rank-1 count collapses from 3,382 to 1,296 at R=560): the model's parts assume the
  full E8 word structure which does not exist in the shallow word.  The +0.58% number is
  model-shape-dependent — THE TRUE WORD'S HISTOGRAM DECIDES (the same artifact class
  retracted five times this session).  (ii) The counting bound at c=18: demands >= 13:
  the +0.58% point (demands ~11) violates it marginally; the first legal point prices
  -0.53% — a hair below the frontier.
- **(d) THE DECISIVE NEXT STEP: THE TRUE WORD BUILD.**  The 2-class system (240 lines,
  h=9) + the class-blocked decoder (rank 18, the verified machinery) + the cancellation
  demands (the E8 arc's construction: rows legal BY CONSTRUCTION) + the shallow middle
  (the shared covers for the ~13-line demands) + the branches + the retained -> gcheck ->
  THE EXACT HISTOGRAM -> THE TRUE PRICE.  THE FIRST II19-FAMILY WORD IN THE
  FRONTIER-PARITY ZONE: the model says the legal floor is -0.5% +- the shape's truth
  (the +-30%-in-c shape sensitivity measured all session): the build decides whether
  II19 beats the frontier.

## THE 2-CLASS MIDDLE ECONOMY — THE CROSSING IS INFEASIBLE (ii19_2class_true.py, ii19_2class_middle.py)

- **THE DEMANDS + THE DECODER (measured):** the class-blocked 2-class decoder VERIFIED at
  rank 18 exactly (the B construction needed the junk pattern filled — the first run's
  rank 240 was the identity-matrix bug).  The class perps: 63 uniform.  The cancellation
  demands (greedy and canonical, k=1/k=2): junks 33/29 lines, ALL counting-bound-legal
  (>= 13 at c=18), ALL sharing WEAK (240/240 distinct junks, overlaps 5.5-6.6 — the I13
  pair-specific signature; the E8 arc's lesson #1 repeated on II19).
- **THE REFINED-HIST BAND (mass-exact BY CONSTRUCTION, no closure distortion; the control
  reproduces the E8 R420 true-hist to 15 digits):** A (fine, all delta-1), B (E8-ish),
  C (coarse), D (the R420's OWN climb proportions {1: 26.2%, 2: 57.1%, 4: 4.8%, 5: 11.9%}).
  THE D VARIANT PRICES +4.97% / +5.35% / +6.79% AT R = 560/573/590 (the peak at 590!),
  crossing back below at R = 620 (-3.64%).  THE CROSSING ZONE: R ~ 560-590, mid 31-46/class.
- **THE PIECE ECONOMY (the decisive feasibility; the fixed greedy: the full-common growth,
  the uncovered real_users filter, the honest R = 480 + pool + 18):** for the canonical
  k=1 junks (33 lines, weak sharing), the greedy piece extraction gives a pool of
  **192 pieces** (mean 5.6 lines, mean 12.6 users, max 17), 260 singles (the direct
  source reads), the arrival saving 4,164 of 7,920 slots (53%).  THE ARRIVALS: 4,776 vs
  the capacity 9R = 6,210 (77%, FITS).  (The first run had two bugs: the x2 R-inflation
  (the pool is the TOTAL over both classes: 962 was wrong, 730 the fix) and the
  covered-blindspot in the real_users filter — both fixed before the verdict.)
- **THE HONEST VERDICT: THE CROSSING IS INFEASIBLE AT THE PIECE ECONOMY.**  The crossing
  needs mid ~62-92 TOTAL; the measured economy gives 192: the weak-sharing wall — the
  cancellation randomizes the junks and the middle cannot compress.  AT THE HONEST
  R = 690: A: -22.33% | B: -15.56% | C: -3.64% | D: -5.70%.  ALL BELOW THE FRONTIER.
  The best (C) is the least realistic shape (30% rank-5 mass vs the R420's 12%); the
  honest D: -5.70%.
- **THE II19 PUSH'S HONEST ENDPOINT:** the demand families: k=1 (33-line): the middle
  192 -> R=690 -> -3.6 to -22%; the full perps (63): the transplant middle 360 ->
  R=858 -> ~-15%; the deeper k=2 (29): ~-4 to -5%.  NO DEMAND FAMILY REACHES THE
  CROSSING.  The 2-class window (h=9, m=73) is materially better than h=10 (the best
  honest -3.64% vs the h=10 floor -25.5%) — THE CLOSEST ANY II19-FAMILY WORD HAS COME —
  but measured below at every configuration.  THE FRONTIER (E8 R434, c = 0.0017444)
  STANDS UNBEATEN.
- THE REMAINING CAVEATS: the greedy is a crude cover design (a better design could
  compress somewhat, but the needed ~2x compression against the measured weak sharing
  is unlikely); the coordinated/frame-aligned demand family (the sharing-preserving
  cancellation, the R420's own x(t) partners) was never piece-designed; the true shape
  (the build) sits between A and D.

## THE PUSH (SS1349 DIRECTIVE): THE HONEST R COMPOSITION — THE CROSSING IS ALIVE AND MODEL-VERIFIED (ii19_2class_push.py, ii19_2class_control.py)

- **THE CONVENTIONAL-BRANCH ERROR EXPOSED (the decisive correction):** the SS1331
  'R = 480 + mid + 18' added 480 branches BY CONVENTION (the E8 cell-machinery carriers).
  But the piece-word builds its pieces DIRECTLY FROM THE SOURCES (the A-phase: the helpers
  read the sources — the identity-word precedent, gcheck-PASS at SS1240!!).  NO PER-LINE
  CARRIERS ARE STRUCTURALLY NEEDED.  The honest structure: the pieces + the tail carriers
  (the per-target leftovers) + the retained.
- **THE THRESHOLD-TUNED POOLS (the greedy's natural knob, COOC x SAVETH):** (3,4): pool
  192 (mean 5.6 lines, mean 12.6 users), carriers 114 -> structure 324; (2,2): pool 202
  (mean 5.5, mean 12.1 users), carriers 94 (leftover 180 lines) -> structure 314 (R/v
  1.31).  THE ARRIVAL LAW (the E8-precedent scope: the B-PHASE demand reads only — the
  E8's own 3,000 = 25/line is the B-phase!!): the demand-reads 2,538-2,546 vs 9R =
  2,826-2,916: FITS (87-90%).
- **THE CROSSING AT THE HONEST STRUCTURES:** R=314: A +5.45% | B +13.07% | C +24.85% |
  D +33.12% (c = 0.002322061)!!  R=324: D +28.57%.  THE ENTIRE SHAPE BAND ABOVE THE
  FRONTIER — even the worst-case A variant!!  The whole R-ladder above from 314 to 605
  (D: +16.38% at 430, +19.66% at 460, +9.69% at 520, +6.99% at 605), crossing below
  only at 620.
- **THE CONTROL (ii19_2class_control.py — the decisive honesty check, mandatory after the
  SS1209 1.57x-bias lesson):** the refined price model (pricer.py), given the R420's
  EXACT true hist {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9} (mass 5,112 = 8*420 + 72 +
  2*120*7) at (v=120, h=8, R=420), reproduces the published c = 0.001653826988146799 to
  18 digits — THE RATIO 1.000000000.  THE MODEL IS EXACT AT TRUE HISTOGRAMS (the SS1209
  bias was the COARSE [7]-model, a different machine!!).  And the D variant's fractions
  ARE the R420's own climb proportions (0.2619/0.5714/0.0476/0.1190 on the non-retained
  climb mass 5,040) — the calibrated family.
- **THE HONEST REMAINING GATES:** (1) THE SHAPE: the A/B/C/D band brackets the true
  histogram (the build's output); even the worst (A, the all-delta-1 finest) is +5.45%.
  (2) THE REALIZABILITY: the joint chain/slot structure — the climb rule is ONE FRAME PER
  DIMENSION per register chain, so a piece of span ~dim 6 has read-slots only at dims 6/7/8
  (~3 slots, ~6-7 users per piece, not the greedy's 12.6!!) and each target's read-frames
  must nest as a flag; the pool likely resizes to ~350-450 (the price at those R's:
  D +7.8% to +19.7% — the crossing survives the resize!!) — UNMEASURED, the decisive gate.
  (3) THE BUILD: the full word -> gcheck -> the TRUE histogram -> the true price.
- **THE VERDICT: THE FIRST II19-FAMILY WORD ABOVE THE FRONTIER (at the model level).**
  The 2-class system (240 lines, h=9), the verified rank-18 class decoder, the legal
  cancellation demands (33-line junks), the honest piece economy, the structure R ~ 314-460,
  the price band +5.45% to +33.12% vs the frontier 0.001744386.  THE SS1331 'crossing
  infeasible' verdict IS SUPERSEDED — it was an artifact of the conventional 480 branches.

## THE SLOT REALIZABILITY GATE PASSES — THE CROSSING SURVIVES (ii19_2class_slots.py)

- **THE PIECES ARE LOW-RANK D4-LIKE SETS:** the span dims {2: 40, 3: 65, 4: 32, 5: 19,
  6: 32, 7: 13, 8: 1} — 105 of 202 at dim <= 3, 137 at <= 4 (the class-1 pieces carry
  +1 for the level direction).  THE SLOT CAPACITIES (the sum over the read-slots dims
  d0..8 of the max rank-bounded user-groups, the law rank(group) <= 9-d — the R420's own
  quad mechanism: 12 targets of rank 3 share the dim-6 frame!!): 55 pieces at capacity
  >= 20 (capped), the mean capacity 12.0 vs the mean users 12.1 — ONLY 5 OF 202 PIECES
  NEED RESIZE.
- **THE USER-SIDE PACKING: 0 UNPLACED** — every target's ~8-10 pieces pack into its chain
  slots (the greedy lowest-fit: dim 4: 1,350 placements, dim 5: 979, dim 6: 148, dim 7:
  67, dim 8: 2) with the unions' ranks <= the slot dims.
- **THE JOINT: the (piece, user) demand 2,452 vs the slot capacity 2,427 (101%)** — TIGHT
  but the pool resizes to ~205 only (from 202!!).  THE HONEST R = 205 + 94 + 18 = 317
  (R/v 1.32).
- **THE PRICE BAND AT R = 317: A +5.17% | B +12.78% | C +24.57% | D +27.62%** — THE
  ENTIRE BAND STILL ABOVE THE FRONTIER.  THE CROSSING SURVIVES THE REALIZABILITY
  MEASUREMENT.
- **THE FULL GATE LEDGER (every gate measured and passed except the build):**
  the system (240 lines, h=9) ✓ | the decoder (rank 18, the B-matrix verified) ✓ |
  the demands (the 33-line cancellation junks, counting-bound-legal) ✓ | the piece
  economy (202 shared pieces, mean 12.1 users) ✓ | the slot realizability (101% joint,
  0 unplaced) ✓ | the price band (+5.17% to +27.62% at the honest R=317) ✓ | the model
  (the control: ratio 1.000000000 at the R420 true hist) ✓.
- **THE ONE REMAINING GATE: THE BUILD** — the exact chains (the nested frame sequences
  with the Gram determinants), the exact gates (D/A/scatter/B/C with the content-frame
  invariants), the gathers' construction (the U-columns, ~30 lines each), the W-matrix
  (the scatter's rows), gcheck, the TRUE histogram, the TRUE price.

## The E8 sparse-decoder hunt + THE IDENTITY-WORD DISCOVERY (2026-10-18, later session)

- **THE E8 SPARSE-DECODER HUNT (e8_sparse_decoder.py):** B0 = (J+G) mod 2 verified (rank 9
  exactly, rows uniform 63).  The masked-demand freedom (HANDOFF 1444: "target t reads
  c_t = row t — NOT NECESSARILY ALL of R(t)") applied to the FRONTIER SYSTEM (E8, h = 8,
  no window penalty): a sparse decoder (rows ~12-25, above the counting bound v/c − 1)
  would shrink the demands from ~63 to ~12-25 lines/target -> the middle shrinks -> R ~
  320-375 -> mass/v ~ 36-40 vs R434's 43.5 -> c potentially +4-10%.
  MEASURED: RANDOM masks (300 trials per f in 0.2-0.6): rank min 117 at EVERY f — the B0
  rigidity is total (any random sparsification = a random matrix).  PREFIX masks (40
  shuffles per f): rank 75-107 — structure matters (75 vs 117 at f = 0.5!) but still too
  heavy: the honest word economics at rank 75 (cst ~ 6c ~ 450): mass/v ~ 43.9-45.1: NO
  win.  The frozen-shape calibration: the R434 parameters price 0.0016257 vs the true
  0.0017444 (the projection family UNDER-prices by ~7.3% — the true word's actual
  histogram prices better than the frozen-shape approximation).
  THE LOW-RANK SPARSE DECODER (c <= 25, rows 12-25): NOT FOUND in the masked families.
  The asymmetric (U != W), geometric/Weyl-structured, and row-space constructions remain
  UNEXPLORED — the concrete search target.
- **THE IDENTITY-WORD DISCOVERY (e8_identity_word.py + gcheck + xcheck_e1.py read) —
  THE CHECKER-SCOPE COUNTEREXAMPLE.**
  Built the trivial word: B = I (each target receives its own line's value via ONE
  retained register; NO phase-B reads; R = v = 120 helpers; the D-phase pre-reads cancel
  the scattered dirt by doubling).  **GCHECK PASSES IT**: status PASS, hist {1: 240,
  7: 360}, rank_mass 2760 = 8x120 + 120 + 2x120x7, gates D/A/B/C = 120/120/0/120.
  THE PRICE MODEL REFUSES IT: 'no root' (THE SS1515 CORRECTION: the implied root is
  q ~ -0.00127 (F(0) = +0.00195, F increasing in q) -> the word is worth c <= 0; the
  earlier '~0.38' reading was WRONG).
  (a) THE CONCLUSION DECOMPOSITION IS FLOW-LEVEL (xcheck_e1.py lines 346-366):
  U_block_form (z-registers hold no y-bits), J_identity (the targets' x-parts = x_t:
  THE DELIVERY), K_equals_D (the dirt cancels via the D-phase), C_is_U_inverse (the
  helpers restored).  NO products-coverage check exists in EITHER checker — the
  identity word passes all of these too (manual trace).
  (b) RETRACTION (the honest correction): the "completeness forces B = B0" derivation —
  that the junk must cover the perps because the products form at the reads — was
  WRONG.  The multiplication's products are extracted by the OUTER PIPELINE via the
  norm-polarization (Q(x+y) − Q(x) − Q(y) = 2<x,y>: the FULL double sum: no per-pair
  coverage needed inside the word).  THE SPARSE-DECODER FREEDOM IS RESTORED at the flow
  level; the II19 class-blocked decoder (rank 28, verified) and the masked families are
  flow-legal.
  (c) THE CHECKER HIERARCHY: gcheck (flow + H1-H5) < xcheck (flow + the conclusion
  decomposition) < the pipeline's requirements (the hub's #463/#510 template: what the
  words must supply for the asymptotic model to hold — the 'whole-call correlated-helper
  hosting and all-size realization' assumptions).  THE DECISIVE OPEN QUESTION: the
  pipeline's word requirements.  THE SS1515 CORRECTION: the identity word's implied c
  is <= 0 (the root q ~ -0.00127!!), NOT ~0.38 — the pricer does NOT reward this word
  (the 'n (log n)^0.62' reading was WRONG!!); the FLOW point stands (a copy word is not
  a multiplication) — so the pipeline's requirements MUST still exclude such words;
  WHERE and HOW they do is the open format-theory question.  A gcheck PASS is necessary,
  not sufficient: any word claim must also name the pipeline layer.
  THE FRONTIER (E8 R434, c = 0.0017444) STANDS UNBEATEN.  Live programs: the low-rank
  sparse-decoder search (c <= 25); the pipeline-requirements read (the #463/#510
  template).

## THE R420 ANATOMY: THE COMPLETE GROUND TRUTH — THE 121-LINE BUILD'S DESIGN REVOLUTION (r420_anatomy*.py)

- **THE FRAMES = THE LINE-INDEX SETS** (SS1446!!): the R420's 672 frames: {0: 1, 1: 120
  (the singletons), 2: 180 (THE CELLS: dim 2!!), 12: 70 (THE D4 12-line frames: dim 4!!),
  30: 180 (the 30-line frames: dim 6!!), 63: 120 (the perps: dim 7!!), 120: 1 (THE FULL:
  dim 8!!)} — THE SPANS OF THE LINE-SETS (NO arbitrary fillers!!): the FLAG DESIGN.
- **THE HELPERS = THE RUNNING SUMS** (SS1450!!): built INCREMENTALLY (1 src per A-gate!!)
  climbing the D4 flag (the singleton -> the cell -> the 12-frame -> the 30-frame ->
  FULL!!): the content grows WITH the frame (the content-frame invariant!!): the A-gates:
  2064 = 240 (singleton-starts) + 360 (cell-starts) + 1215 (THE 12-FRAME BUILDS: THE
  FRAME-SHARING ECONOMY!!!) + 240 (the 30-frames) + 9 BIG (23-46 srcs at FULL = the
  GATHERS: the hierarchical builds from the helper-totals!!!).
- **THE TARGETS READ ~4 REGISTERS ONLY** (SS1450/SS1458!!): 1 single-line source (at a
  cell-frame: dim 2!) + 1 multi-line accumulated source (24-30 lines!!) + 2 helpers
  (16-21 lines each!!) (at the perp-frame: dim 7!!): the targets' chains: 0 -> the cell ->
  the perp (the deltas [2, 5]!!!): THE PERP-CORRECTIONS (the SS1128 memory: 'the d-single
  (1 read) + the tops (3 needer-reads)' — CONFIRMED!!).
- **THE SEMANTICS VERIFIED: 120/120 targets: scatter ^ B-reads == {t} EXACTLY** (SS1458!!)
  — the scatter delivers B[t] (the 64-line sets via the W-rows: ~2-3 gathers per
  target!!); the B-reads XOR out perp(t) leaving {t}.
- **THE FORMAT CAVEAT**: the R420's word is in an OLDER format ('coords', no
  'ret_frames'!!) -> MY gcheck (SS1437) requires 'ret_frames': MY FORMAT = the identity
  template (SS1435; the SS1240 gcheck PASS!!): the D-phase = the dirt-doubling ONLY
  ([0, t, [the B-helper-srcs + the scatter-rets!!]] — the identity word's minimal
  structure; NOT the R420's massive 121-204-src D-gates (the other format's
  y-mechanics!!)).
- **THE 121-LINE TRANSPLANT DESIGN (THE NEW BUILD!!)**: (1) THE FLAG: the 121-line frames:
  the singletons (121) + the cells + the E8-D4 structures (+ the special: orthogonal to
  all: the +1-dim frames!!) + the perps (dim 8) + FULL (dim 9); (2) THE CORRECTIONS: the
  per-target B-reads: the XOR = perp(t) (64 lines for the roots / 120 for the special!!):
  ~4-5 registers (the sources + the running sums!!); (3) THE GATHERS: MY VERIFIED
  FACTORIZATION (SS1423: the 9 basis rows + the W!!) built hierarchically at FULL
  (CST = 9 x 9 = 81!!); (4) THE R420-ANALOG R (~425-485): MEASURED AT THE HONEST CST=81
  (SS1468): **-23% to -35% — the 'bigger R prices better' trend was WRONG: the
  R420-transplant economics DO NOT CROSS**; the best band point: C at R=300: -7.97% —
  THE 121-LINE MODEL BAND IS BELOW THE FRONTIER AT EVERY HONEST POINT.

## THE USER'S CHALLENGE (SS1469) + THE E8-DEPENDENCE AUDIT — 'are you sure R420 is the ground truth?'

- **THE ANSWER: NO.**  The R420's proper role: THE FORMAT-MECHANICS REFERENCE (the
  gate/chain/frame patterns, confirmed against gcheck!!).  It is NOT a design template:
  its D4 flag (the 180 cells, the 70 12-frames, the 180 30-frames!!) is E8-SPECIFIC
  GEOMETRY, and the 'design revolution / transplant' framing was OVERCONFIDENT — the
  honest-CST measurement (SS1468) shows the R420-analog R values DO NOT CROSS anyway.
- **THE E8-DEPENDENCE AUDIT:** (1) THE PRICE MODEL (mix.price/pprice): calibrated ONLY on
  E8 h=8 words — NO h=9 CONTROL EXISTS in the published word set: the h=9 band is an
  UNVERIFIED EXTRAPOLATION; (2) THE HYPERSENSITIVITY: the model near its root: ±0.3% mass
  -> ±25-35 points in c (DEMONSTRATED: the CST 72->81 (9 mass units!!) moved the best
  point +13.42% -> -7.97% (-21 points!!); the BASIS CHOICE (the pivot basis: all 9 gathers
  dim-9 -> cst 81; a smart basis: 8 dim-8 rows + 1 dim-9 -> cst ~73, plausible but
  UNMEASURED) swings the band ±20 points AGAIN) -> THE MODEL BAND IS NOT A VERDICT;
  (3) THE D VARIANT (the R420's climb proportions): an E8 SHAPE PRIOR, not a measurement;
  (4) THE D4-FLAG TRANSPLANT: E8-optimized (and now measured dead); (5) THE SYSTEM ITSELF:
  the 121-line = the E8 roots + the special — E8-based BY CONSTRUCTION (the h=9-valid II19
  subset): this dependence is GEOMETRIC/NECESSARY, not 'unnecessary'.
- **WHAT'S SOLID (the system-native, no-E8-prior measurements):** the h=9 legality (the PD
  span!!); the perp-pattern decoder rank 9 (THIS system's!!); the piece economy (156
  pieces, mean 2.9 lines, 16.5 users — the sharing is GENUINELY in this system's
  geometry!!); the slot packings (SS1419!!).  THE ONLY HONEST GATE: THE BUILD + the TRUE
  histogram + the TRUE price.  THE SESSION PATTERN (the Bayesian prior): every honesty
  layer this session has only ever moved the number DOWN (+33% -> h=10 -> -11%; +13.42% ->
  CST=81 -> -7.97%).

## THE PRICE MODEL AUDIT + THE SMART BASIS (cst=73 MEASURED, W PASS) — **THE CROSSING CLAIM RETRACTED BY THE SS1515 AUDIT: SEE THE NEXT SECTION** (ii19_121band2.py, ii19_121basis.py; SS1483-SS1508)

- **THE DIRECTION (SS1483!!): the user chose 'Audit the price model first'.**
- **THE PRICER READ (pricer.py, SS1488!!): THE WINDOW IS PIPELINE-DERIVED AND FULLY
  PARAMETRIC IN h — NOT E8-FITTED**: m = 1 + L(h-1) with L = 2K+1 = 9 (K=4, T=32: THE
  PIPELINE'S REPLICA/STAGE CONSTANTS — the #463/#510 template's 'nine-stage bit
  price'!!), a = h-1 (the idle-slot capacities!!), w = h (the residual width!!), W = 2KvT,
  the root: sum z_r (r/(mW)) (m/r)^q + 32 m (sum z) m^q / (1e16 W) = 1 with prof = the
  local hist x T x L (T=32 x L=9: THE x288!!); the hosting: nres = 9R vs cap = 36v (THE SS1515/SS1517 CORRECTION: THE WALL AT R = 484
  for v=121 (NOT 511!!): cap = 4,356 = 36v (the pricer's own error dict!!)); THE h=9 HOSTING
  PENALTY: the residual leftovers rank {3,5,7} at h=9 vs {2,4,6} at h=8.
- **THE HYPERSENSITIVITY: STRUCTURAL (THE 288x AMPLIFICATION!!)**: the ±9 local mass
  moves the c by ±26-29% (the observed CST 72->81 swing = -21 points: QUANTITATIVELY
  CONFIRMED!!) -> THE MODEL BAND AT THE ±10% CROSSING SCALE IS MEANINGLESS WITHOUT THE
  EXACT ACCOUNTING (the cst, the basis, the hist's mass-exactness!!).
- **THE SS1406/SS1468 BAND'S INT-TRUNCATION ARTIFACT (SS1492!!)**: the int() truncation
  lost ~4.4 mass -> the c INFLATED ~+11-14 points!!  THE HONEST HISTS: THE MASS-EXACT
  (the largest remainder with the r<=rem constraint!!) — gcheck's own assert demands
  mass == the identity EXACTLY.
- **THE HONEST BAND (ii19_121band2.py, SS1492!!)**: THE CONTROL: the R420 true hist: the
  model EXACT (ratio 1.000000000!!).  AT THE PIVOT BASIS (cst=81: all 9 gathers'
  contents span dim-9 -> the frames FORCED to FULL!!): DEAD (-16% to -41%!!).  AT THE
  SMART BASIS (the modeled cst=73): THE BAND STRADDLES THE FRONTIER (C: +2.77%/+3.66%,
  D: +5.20%!!) — **THE SS1515 AUDIT: the +3.66%/+5.20% figures came from WRONG-MASS
  (mOFF) histograms (band2's hist_exact lacked the r<=rem constraint!!): DROPPED**.
- **THE SMART BASIS CONSTRUCTED + THE CST MEASURED (ii19_121basis.py, SS1500/SS1508!!)**:
  the parity map phi (the column-120 bit: the special in the support!!) on the 9-dim row
  space: THE KERNEL (the 'even' combinations B[0]^B[k]: the specials cancel!!): dim 8:
  every kernel row's support contains NO special line -> its span <= dim 8 (GUARANTEED by
  the parity!!).  THE GREEDY (THE SS1496 BUG FIXED: append only rank-increasing
  candidates (the first 9 B-rows are DEPENDENT (the D4-ish line ordering!!)!!)): k =
  [1,2,4,6,8,10,12,56]; the even rows: supports 56-64 lines, SPANS DIM 8 (the E8-span!!)
  + the odd row B[0]: 65 lines, SPAN DIM 9 (the special: FORCED!!) -> **THE MEASURED CST
  = 8x8 + 9 = 73 EXACTLY (the prediction confirmed!!)**.
- **THE W-COORDS-FRAME BUG (the SS1500 'FAIL'!!)**: the solve's coords were relative to
  the REDUCED pivot rows, NOT the original basis -> the verification XORed the wrong
  rows (the §1423 script verified against the reduced rows (consistent!!); the SS1494
  script mixed the frames!!).  THE FIX (SS1502!!): the augmented reduction (the T-matrix
  snapshots: rw_k = Σ_j T[k][j]·basis[j]!!) -> W_orig = W_red x T: the coordinates over
  MY gathers (the even rows + the odd row: THE ONES THE BUILD'S SCATTER NEEDS!!).  **THE
  RE-RUN (SS1508!!): THE W-VERIFICATION PASSES: B[t] = Σ W[t,k]·u_k over the even/odd
  gathers for all 121 targets!!**  The W-weights: {1: 1, 2: 8, 3: 6, 4: 6, 5: 50, 6:
  36, 7: 6, 8: 7, 9: 1} (the mean 5.2).  THE PRINT-LABEL BUG FIXED (SS1506: '(span dim,
  support size)' — span_dim returns (rank, len)!!).
- **THE PRICE AT THE MEASURED CST=73 (the mass-exact hists!!)**: R=286: **C +2.77%** (c
  = 0.001792760!!) | R=300: C +0.69% | R=325: C -2.75% | R=350: C -6.00%; A/B/D below
  everywhere — **RETRACTED BY THE SS1515 AUDIT: shape C contradicts the design's own target
  chains (the jumps {1: 726, 2: 121}: NO rank-5 steps!!) and R=286 violates the arrival
  law (2,690 reads > 9x286 = 2,574: 105% OVER!!: R_honest >= 299): NOT a crossing at
  honest accounting (see THE SS1515 AUDIT section!!)**.
- **THE HONEST CAVEATS (the standing rules!!)**: (1) the A/B/C/D variants are SHAPE
  PRIORS (the C: {1: 0.30, 2: 0.20, 5: 0.50}!!): the TRUE word's hist decides ±several
  points (the ±26-point sensitivity!!); (2) R=286 = the 156 pieces + the 121 tails + the
  9 gathers — **THE SS1515 AUDIT: 'VERIFIED FEASIBLE' WAS FALSE: the slots.py check
  never tested NESTING (121/121 target chains cannot nest!!) and the build had ALREADY
  FAILED 85% of the reads (396/2,569 assigned: ii19_121_build2.py + the committed
  stage2a pkl!!) — a result this record OMITTED**; (3) THE BUILD remains the gate: the
  honest shape is A-like (the design's chains!!), the honest R >= 299 (the arrival
  law!!) — **the +2.77% is RETRACTED (SS1515!!)**; (4) the basis is NOT span-minimized (a min-Σ-span basis could give cst < 73:
  UNEXPLORED!!); (5) the special's 120-line demand rides the root-pieces (SS1423!!) but
  its chain packing is unverified in detail.
- **THE USER'S SS1503-1504 DIRECTIVE**: stop after finishing + committing; provide the
  audit prompt for a fresh agent.

## THE FRESH-AGENT AUDIT (SS1515): THE CROSSING RETRACTED — THE 121-LINE MODEL BAND DOES NOT CROSS AT ANY HONEST ACCOUNTING

- **THE AUDIT (the fresh agent; the user's SS1503 request!!): the +2.77% is NOT real at
  honest accounting.** The pricing reproduces exactly, but the configuration it prices
  is contradicted by the session's own design and build data on THREE INDEPENDENT
  COUNTS:
  1. **THE SHAPE (CRITICAL!!)**: the design's own target chains (ii19_121_design.pkl!!)
     climb 0->2->3->...->8: the jumps {1: 726, 2: 121} — 75% of the target mass at rank
     1, NONE at rank 5!!  Shape C (half the climb mass at rank 5!!) is CONTRADICTED; the
     design pushes toward shape A: **-15.85% at R=286**.
  2. **THE REGISTER COUNT (HIGH!!)**: the design's own arrival law: 2,690 reads vs the
     capacity 9x286 = 2,574 (105% OVER!!); R_honest = 299 (stored in the slots pkl but
     the ok check IGNORED it and printed 'FEASIBLE'!!).  Shape C by R: R=299: +0.85%,
     R=300: +0.69%, R=311: -0.84%, R=325: -2.75% — the record's own estimate (the
     honest R ~310-325!!) already put C BELOW.  The 9 gathers' own reads (521 lines!)
     are NOT in the 2,690; if they count: R >= 357 (C at R=350: -6.00%) — UNRESOLVED.
  3. **THE FEASIBILITY (CRITICAL!!)**: the build FAILS: ii19_121_build2.py assigns 396
     of 2,569 piece reads (2,173 FAILURES!!); the v1 crashes at L187.  THE NESTING: 121
     of 121 target chains and 100 of 121 source chains CANNOT NEST (the slots.py check
     treated each slot as an independent bin and NEVER checked that a register's
     successive frames nest; max_group (L208) defined but NEVER CALLED!!).  **NEITHER
     RESULT WAS IN THE RECORD — the 'verified feasible' caveat was FALSE (corrected
     in place above!!).**
- **THE MARGIN**: one decoder unit wide: cst 74 -> -0.20%.
- **MY VERIFICATION RUNS (SS1517!!)**: (a) THE HOSTING WALL: THE AUDITOR RIGHT, MY
  SS1488 NOTE WRONG: **cap = 4,356 = 36v (NOT 38v!!): the wall at R = 484/485 (h=9,
  v=121) and R = 480/481 (h=8, v=120)** — the pricer's own error dict (cap=4356,
  nres=4365 at R=485!!); (b) THE IDENTITY WORD: THE AUDITOR RIGHT: F(0) = +0.00195, F
  increasing -> the root q ~ -0.00127: the word is worth c <= 0 (the '~0.38' readings
  corrected in place!!).
- **THE AUDIT'S OTHER FINDINGS**: (4) the mOFF citations: the 'straddles' figures came
  from WRONG-MASS histograms (band2's hist_exact lacked the r<=rem constraint!!) —
  DROPPED (annotated in place!!); (6) **THE FRONTIER'S PROVENANCE: 0.001744386 is the
  BIT-side c (research/e8-bit-p111-r434/EXPECTED.json:99!!) — the selected
  certificate's κ = 0.001672660197076918 is bound by the COMPLEX side: EVEN A GENUINE
  BIT-SIDE CROSSING WOULD NOT MOVE THE SELECTED κ ('bit headroom only'!!)** — THE
  ENTIRE SESSION'S FRONTIER CHASE WAS BIT-SIDE; (8) a HANDOFF formula (L1679: 'T(hv -
  (h+1)cst)') holds only at h=8 (the pricer's deficit is T(8v - 9cst) for every h).
- **THE PER-CLAIM VERDICTS (the audit's!!)**: A (the 121-line legality: exact rational
  arithmetic, the Gram det 2 with all leading minors positive: PD!!): CONFIRMED ✓; B
  (the price model: m = 73, the x288, K/T the fixed defaults; cst 73->74 = -2.97
  points ✓; whether K/T were tuned to E8: UNVERIFIABLE; no h=9 control exists):
  CONFIRMED ✓; C: CONFIRMED for basis.py, ERROR for band2 ✓; D (the smart basis: the
  spans [(8,64), (8,56)x7, (9,65)]; the W PASS; THE RETAINED AT ANY FRAME DIM AT THE
  SCATTER LEGAL (gcheck L104-114) with dim h only at the final climb (L71, L124)!!):
  CONFIRMED ✓; E (R=286): **ERROR** ✓; F: the numbers CONFIRMED, the presentation
  ERROR (the commit headline b69e7f85 'THE CROSSING RETURNS' OVERSTATED!!) ✓; G (the
  earlier negatives, the h=10 band: its D hists 6 units mass-light — flattering — but
  the negative STANDS!!): CONFIRMED ✓; H (the conventions: T(n) = O(n(log n)^{1-κ}):
  HIGHER better ✓; both controls exact ✓; no sign errors ✓): CONFIRMED ✓.
- **THE MISSED LIST (the audit's!!)**: (1) a gcheck-passing word (NONE exists; the
  partial build FAILS 85%!!); (2) the shape from the design (the target side is
  A-LIKE!!); (3) the nesting checks in slots.py (max_group unused!!); (4) the arrival
  law in the verdict (price at R >= 299; the gathers' 521 reads unchecked!!); (5) **the
  span-minimizing basis (a dim-7 row -> +5.75%: UNSEARCHED — THE ONE REOPENING LEVER:
  the crossing needs Σ-span <= ~65-67 at the honest shape/R!!)**; (6) the special
  line's 120-read chain (only 6 of 156 pieces contain line 120: unchecked!!); (7) an
  h=9 calibration control (NONE!!); (8) **THE COMPLEX SIDE!!**.
- **THE HONEST BOTTOM LINE (the audit's!!)**: the 121-line model band does NOT cross at
  any honest accounting: the honest shape is A-like (-15.85% at R=286); the honest
  R >= 299 puts C below by R ~ 311; the build fails 85% of reads. WHAT WOULD SETTLE
  IT: a gcheck-passing word at h=9 with its exact histogram priced by pricer.py —
  **and the auditor's expectation: such a word prices BELOW the frontier.** THE
  SESSION PATTERN HOLDS FOR THE FOURTH TIME: every honesty layer moved the number
  DOWN (+33% -> h=10 -> -11%; +13.42% -> CST=81 -> -7.97%; +2.77% -> THE AUDIT ->
  below). AND THE REFRAMING: the whole chase was BIT-side — the selected κ
  (0.001672660197076918, complex-bound) would not move even from a genuine crossing.

## THE SPAN SEARCH (THE SS1515 AUDIT'S MISSED ITEM 5): THE LAST REOPENING LEVER CLOSED — THE CST FLOOR IS 73, PROVEN EXHAUSTIVELY (ii19_121span.py; SS1531-SS1536)

- **THE DIRECTION (SS1531!!): the user: 'keep pushing for frontier' -> the span-minimizing
  basis search (the audit's missed item 5: the ONE unsearched reopening lever!!).**
- **THE EXHAUSTIVE MEASUREMENT**: the parity kernel's ALL 255 NONZERO ROWS: **the span-dim
  histogram: {8: 255} — EVERY KERNEL ROW SPANS EXACTLY DIM 8; THE LOW-SPAN ROWS (dim <=
  7): ZERO!!**  The support sizes: min 56, mean 60.2, max 64 (the kernel's minimum
  distance ~56: the code is SPREAD OUT — the earlier session's ~30-line 'cancellation
  rows' were a DIFFERENT code (the masked rows!), NOT the perp-pattern kernel!!).
- **THE MIN-Σ-SPAN BASIS (the weighted matroid greedy!!)**: the spans [8,8,8,8,8,8,8,8] ->
  Σ = 64 -> **THE HONEST CST FLOOR = 64 + 9 = 73 (the odd row: FORCED!!) — EXACTLY the
  SS1500 greedy's basis: NO LOWER-CST BASIS EXISTS (the floor PROVEN by the exhaustive
  enumeration!!)**.  The W-verification on the alternate min-basis: PASS ✓ (the
  W-weights: {1: 1, 2: 8, 3: 2, 4: 10, 5: 50, 6: 36, 7: 11, 8: 2, 9: 1}: the mean 5.2).
- **THE PRICE AT THE PROVEN FLOOR (cst=73) OVER THE HONEST R GRID (>= 299!!)**: R=299:
  A -17.51% | B -7.21% | D -5.60% (the best!!) | R=310: A -18.87% | B -8.68% | D -7.09%
  | R=325: A -20.65% | B -10.61% | D -9.06% | R=350: A -23.45% | B -13.67% | D -12.13%
  (C dropped per the audit: contradicted by the design's own chains!!).
- **THE VERDICT: THE 121-LINE CROSSING IS CLOSED ON THE NUMBERS AT THE MODEL LEVEL**: the
  cst lever (the last reopening hope) is PROVEN at its floor (73: all 255 kernel rows
  measured!!), and at the floor over the honest R the band is **-5.60% to -23.45%: ALL
  BELOW THE FRONTIER** — and the unresolved extras (the gathers' 521 reads (R >= 357?),
  the build's nesting failure (85% unassigned!!)) would only make it WORSE.  THE
  100%-PROOF STANDARD (the user's SS1228!!) IS SATISFIED FOR THE CST LEVER: the floor is
  measured, not assumed.  THE REMAINING STEPS: the design-derived hist (the audit's
  missed item 2: the confirmation — the shape between the A-like targets and the
  unmeasured sources/helpers) and THE BUILD (the definitive word — the auditor's
  expectation: BELOW; the nesting must be fixed first).

## THE DESIGN-GROUNDED HISTOGRAM + THE HONEST-R BRACKET: THE CROSSING IS NOW A ±1% MARGINAL QUESTION (ii19_121designhist.py, ii19_121designhist2.py, ii19_121honest299.py; SS1547-SS1556)

- **THE LOG-MOMENT DISCOVERY (SS1547!!)**: at q ~ 0.0018 the price model is effectively
  a TWO-PARAMETER model: (the mass, LM = Σ mass_r·ln(m/r))!!!  The C variant (+2.77%!!)
  and the coarse-tail design hist (+2.77%!!) AGREE because their LMs agree (15,254 vs
  15,253!!) — the shape beyond the (mass, LM) pair DOES NOT MATTER (to the 1e-5
  level!!).  THE SS1547 R=299 COLUMN (+347%/+308%!!) WAS MY BUG: the INCONSISTENT
  PAIRING (the R=286-structured hist 117 mass light for R=299!!) — DROPPED; the
  consistent pairing ONLY!!
- **THE TRUE DESIGN SHAPE EXTRACTED (SS1547!!)**: the pieces' jumps {1: 379, 2: 181,
  3: 61, 4: 67, 5: 30, 6: 8, 7: 2}; the core (the pieces + the sources + the targets +
  the gathers + the copies): {1: 1532, 2: 341, 3: 95, 4: 100, 5: 64, 6: 18, 7: 3,
  8: 16, 9: 2} (the mass 3,494; the LM 12,595!!).  THE TAILS' BRACKET: the coarse
  (0->8->9): +2.77%!!; the fine (the target-like): -6.23%!!.
- **THE (b)-MODEL (THE DESIGN-GROUNDED TAILS!!) (SS1551!!)**: the tails' chains from
  the pkl's OWN data: 0 -> THE SPAN OF leftovers[t] ({2: 1, 4: 7, 5: 8, 6: 17, 7: 79,
  8: 9}!!) -> THE READ SLOT tgt_slot[(t, -1)] ({4: 3, 5: 9, 6: 18, 7: 81, 8: 10}!!) IF
  s > span (the tail at the span ALREADY satisfies the read: the src's frame ⊇ the
  gate's!!) -> 9!!  THE (b)-HIST: {1: 1548, 2: 425, 3: 113, 4: 116, 5: 76, 6: 35,
  7: 82, 8: 25, 9: 2}: the mass 4,583 EXACT (the identity OK!!); the LM 15,498
  (between the brackets: the coarse 15,254 / the fine 17,098!!).
- **THE PRICE: THE (b)-MODEL AT THE DESIGN'S R=286: c = 0.001770409 (+1.49%!!) — THE
  DESIGN-GROUNDED MODEL HIST CROSSES AT THE DESIGN'S OWN R!!**  (BUT R=286 VIOLATES
  THE ARRIVAL HEURISTIC: 2,690 > 9x286 = 2,574!!)
- **THE HONEST-R BRACKET (SS1556!!)**: the (b)-hist + the +13 slack registers (the
  consistent pairing: the mass 4,700 EXACT!!): THE COARSE-13 ({8, 1}: the
  optimistic!!): **c = 0.001747410 (+0.17%!!)** | THE FINE-13 (the piece-like: the
  pessimistic!!): **c = 0.001730020 (-0.82%!!)** — **THE BRACKET AT THE HONEST R=299
  STRADDLES THE FRONTIER: THE CROSSING IS NOW A ±1% MARGINAL QUESTION, DECIDED BY THE
  +13 SLACK REGISTERS' CHAINS (UN-DESIGNED!!).**
- **THE OPEN ITEMS (THE HONEST STATE!!)**: (1) the +13 slack registers: UN-DESIGNED
  (the R=299 redesign: the pool reshaped?!); (2) THE ARRIVAL-LAW SCOPE: the audit's
  question (the gathers' 521 reads + the A-src-reads ~1,470+ vs the sources' capacity
  9x121 = 1,089?!): UNRESOLVED — if the A-reads are capped too, R rises further and
  the price falls; (3) THE NESTING: 121/121 target chains FAIL (SS1515!!): NO WORD
  EXISTS; (4) THE PAYOFF: BIT-side only (the selected κ = 0.001672660197076918 is
  COMPLEX-bound!!).
- **THE VERDICT**: the design-grounded model band: +1.49% at R=286 (the infeasible
  R!!) -> +0.17%/-0.82% at R=299 (the un-designed slack!!) -> the marginal ±1%
  question.  THE ONLY SETTLEMENT: THE BUILD (the nesting fix + the R=299 redesign +
  the true word -> gcheck -> the TRUE hist -> the TRUE price!!) — and the deeper
  caveats (the scope questions, the bit-side-only payoff!!) make the honest
  expectation: BELOW.

## THE THRESHOLD SWEEP — THE COARSE DIRECTION CROSSES ROBUSTLY AT THE MODEL LEVEL; THE ALL-TAIL EXTREME EXPOSES THE PRICER'S SRC-WORK BLIND SPOT (ii19_121sweep.py; SS1572-SS1575)

- **THE SWEEP (SS1572!!)**: the piece economy's THRESHOLD (the greedy's stopping:
  saving >= TH — MY ARBITRARY SS1423-ERA CHOICE OF 4!!) IS THE UNEXPLORED DESIGN
  DIMENSION:  TH=6: R_hon 284, LM 14,325: **coarse-slack +4.47% / fine-slack
  +2.16%**;  TH=5: R_hon 290, LM 14,765: **+2.86% / +1.09%**;  TH=4 (the committed
  design!!): 299: +0.17%/-0.82% (the marginal bracket!!);  TH=3: 307: -2.47%/
  -2.54%;  TH=2: 322: -5.09%.  THE CONTROL PASSES EXACTLY (the TH=4 row = the SS1556
  numbers!!).  THE MECHANICS: the coarser pool shrinks R (286->268->256!!) AND
  coarsens the hist (the LM 15,498->14,765->14,325!!): BOTH push the price UP.
  **THE FINE-SLACK BRACKET (the realistic piece-like slack chains!!) IS ABOVE AT
  TH=5/6: +1.09%/+2.16% — THE MODEL-BAND CROSSING IS NO LONGER MARGINAL!!**
- **THE EXTENSION (SS1575!!)**: TH=7: 278: **+5.91%/+3.46%**; TH=8: 269:
  **+7.97%/+5.25%**; TH=10: 246: **+13.64%/+10.35%**; TH=12: 235: **+16.14%/
  +12.80%**; TH=16: 208: **+22.22%/+19.51%**; TH=24: 205: **+22.68%/+20.06%**;
  **TH=100 (THE ALL-TAIL LIMIT!!): R=130 (0 pieces: each target served by ONE
  register: its full-perp tail!!): +67.70% (!!)**.  The feasibility stays clean
  (unplaced 0, conflicts 0) through TH=24.
- **THE ALL-TAIL ABSURDITY — THE PRICER'S BLIND SPOT EXPOSED (the decisive honesty
  finding!!)**: the all-tail's '+67.70%' CANNOT BE TRUSTED: its A-phase reads ~121 x
  64 = 7,744 SOURCES (each tail's build = the full perp(t)!!) — the src-work ~2.4x
  the entire register-mass (3,179!!) — **THE PRICER'S MASS MODEL (the register
  chains ONLY!!) DOES NOT PRICE THE GATE SRC-READS**.  THE PIECES' TRUE PURPOSE (the
  greedy's saving k x u - (k+u) = THE SRC-READ SAVING: the u users read ONE register
  instead of k sources each!!) — NOT the register count (the all-tail has FEWER
  registers!!) — **THE SRC-WORK IS THE UNMODELED COST COMPONENT**, and the published
  words' piece structure (the R420!!) exists precisely to keep it proportional
  (~1:1 the srcs/mass at the published designs; the all-tail's ratio ~3.1: WAY OUT
  OF THE MODEL'S DOMAIN!!).
- **THE HONEST CROSSING CLAIM**: the model band (the pricer's domain!!): +1.09%
  (TH=5, fine!!) to +22.68% (TH=24!!) — ROBUST AT THE COARSE THRESHOLDS — but the
  src-work question (does the pipeline's true cost make the coarse direction's
  prices real??) is THE UNRESOLVED HONESTY GATE: the total-work view (the climbs +
  the srcs!!) puts the true optimum in the TH ~10-24 region (the total ~10,300 vs
  the TH=4's ~11,200 and the all-tail's ~13,100!!).
- **THE REMAINING GATES (updated!!)**: (1) THE SRC-WORK'S ROLE in the pipeline's
  cost model (the pricer's internals: the idle_slots/nres/the work definition!!)
  — THE DECISIVE READ; (2) THE NESTING (121/121 target chains FAIL: SS1515!!) —
  the build blocker; (3) THE PAYOFF: bit-side only (the selected κ is
  COMPLEX-bound!!).

## THE PRICER'S INTERNALS READ — THE SRC-WORK QUESTION SETTLED; THE ALL-TAIL'S LEGALITY RE-OPENED (pricer.py; SS1582)

- **THE PRICER'S CONFIRMED SCOPE (the code read!!)**: `price(local, v, h, R)`: the
  profile = the local hist x T x L (the 288 replicas!!) + the rem (the hosting
  leftovers!!) x T (the 32!!); the root: F(q) = Σ_r z_r (r/(mW)) (m/r)^q + 32m·tot·
  m^q/(1e16·W) − 1; m = 1 + L(h−1) = 73 (at h=9!!); W = 2KvT; the hosting: nres =
  R·L ≤ cap (Σ 2v·(c//w): the R ≤ 4v wall!!).  **THE MODEL'S ONLY WORD-LEVEL INPUT:
  THE REGISTER-VISIT PROFILE (the local hist!!) — THE GATE SRC-READS ARE ABSENT FROM
  THE MODEL (CONFIRMED BY THE CODE!!)**.  The controls (the `__main__`!!): the P111
  {1: 1321, 2: 1342, 3: 80, 4: 47, 5: 102, 6: 10, 7: 18} at R=439 + the R420 {1:
  1320, 2: 1440, 4: 60, 5: 120, 8: 9} at R=420: THE EXACT PUBLISHED REPRODUCTION ✓✓.
- **THE IMPLICATION**: the model IS the format's own cost model (the exact
  reproduction!!) — the c is determined by the register-visit profile ALONE: the
  src-reads are NOT an independent cost in the model.  THE COARSE DESIGNS' PRICES
  (+1.09% to +20.06% at TH=5-24!!) ARE THE MODEL'S TRUE VERDICTS on the register-mass —
  the src-proportionality caveat (the published words' ~1:1 src/mass ratio vs the
  coarse designs' ~1.3-1.7x!!) remains the extrapolation-domain question.
- **THE ALL-TAIL'S LEGALITY RE-OPENED (the decisive structural question!!)**: IF the
  read rule is 'the src's frame ⊆ the dest's frame' (the merge-in direction: the E8's
  cells: the sources at {s} (dim 1!!) ⊆ the cell's dim-2 frame ✓; the (b)-model's
  read-slot logic (s > sp!!) ✓✓), THEN the all-tail's A-gates are LEGAL (the sources
  at {s} (dim 1!!) ⊆ the tail's dim-8 span!!) — and the +67.70% would be a REAL model
  verdict on a LEGAL design!!! — **THE SANITY CHECK: the published E8 frontier
  (R=434!!) would be crushed by the all-tail E8 (R=129!!) — IMPOSSIBLE — SOMETHING
  MUST BLOCK IT**: the climb rule's exact form (the ⊆ vs the ⊇ direction!!), the
  sources' mandatory climbs (the mass identity's 2v(h−1)!!), the scatter's free-form
  exception (SS1126!!), or the C-phase's reverse: **THE GCHECK RE-READ (the
  climb/gate rules!!) IS THE DECISIVE NEXT STEP.**
- **THE STANDING**: the coarse direction's model crossings (+1.09% to +20.06%!!) +
  the pricer's confirmed scope (the srcs unpriced!!) + the all-tail's legality
  question (the gcheck rules!!) + the nesting failure (the SS1515 build blocker!!) +
  the bit-side-only payoff.

## THE (c)-CORRECTED SWEEP — THE GCHECK GATE RULE APPLIED; THE CROSSINGS SURVIVE AT TH >= 8 (ii19_121sweep.py; SS1589-SS1594)

- **THE GCHECK RE-READ (SS1589!!) — THE DECISIVE RULES**: `run()`: **ALL the operands
  (the dest AND the srcs!!) climb to the gate's frame** (`for r in [d] + srcs: climb(r,
  F)`!!); `climb()`: the operand's current frame MUST be a SUBSPACE of the gate's frame
  (`sub(cur[r], F)`!!) and EVERY climb is priced (the hist!!).  **THE SS1583 'SRC-WORK
  UNPRICED' WAS WRONG: the src-READS (the val ^= XORs!!) are free but the src-CLIMBS
  ARE the mass — the pricer prices them via the register-visit profile!!**  THE
  SCATTER: free-form (no climbs!!); the C-phase: the literal reverse of the A+B
  z-gates; the final climbs to the final frames ✓.
- **THE ALL-TAIL: ILLEGAL (the sanity restored!!)**: (a) a source at FULL (dim 9!!)
  CANNOT feed a dim-8 tail-build (FULL is NOT a subspace of the t-perp: the ⊆ rule!!)
  — the sources must pass the tail-spans BEFORE FULL; (b) one frame per dim per chain
  — a source read by ~64 tails would need ~64 different dim-8 frames: IMPOSSIBLE.
  **THE SS1575 '+67.70%' IS AN ILLEGAL DESIGN'S ARTIFACT** ✓ (the R=434 frontier's
  sanity restored!!).
- **THE (b)-MODEL'S BUG + THE (c)-CORRECTION (SS1591!!)**: the tail-builds'
  source-climbs were MISSING from ALL the hist models (the SS1551 (b)-model!!): the
  carriers' leftover lines must climb to the tail's span (dim 5-8!!) BEFORE FULL —
  THE SOURCES' CHAINS MUST INCLUDE THE TAIL-SPAN FRAMES.  The sources' total mass is
  FIXED (8 each — the identity!!); the DISTRIBUTION coarsens (the LM rises!!).
- **THE CORRECTED SWEEP (SS1594!!)**: TH=4 (the committed design!!): **-2.45%/-3.40%
  — BELOW (the marginal bracket KILLED!!)**; TH=5: -0.01%/-1.68% (BELOW!!); TH=6:
  +1.53%/-0.65% (straddles!); TH=7: +2.89%/+0.57%; **TH=8: +4.89%/+2.32%; TH=10:
  +9.74%/+6.67%; TH=12: +11.99%/+8.88%; TH=16: +17.46%/+14.96%; TH=24:
  +17.82%/+15.41%** — **THE CORRECTION (~-3 to -5 points!!) MOVED THE WHOLE CURVE
  DOWN BUT THE COARSE REGION (TH >= 7-8!!) STAYS ABOVE: the fine-slack (the
  REALISTIC piece-like slack chains!!) crossings at TH >= 8: +2.32% to +15.41%!!**
  The feasibility stays clean (unplaced 0, conflicts 0 at every TH!!).
- **THE STANDING (after the correction!!)**: (1) THE NESTING: the (c)-model ASSUMES
  the sources' chains can pass the tail-spans (the flag!!) — UNVERIFIED: the SS1515
  finding (121/121 target chains FAIL!!) + the sources' multi-tail-span requirement:
  the JOINT FLAG STRUCTURE is the build blocker (the nesting-aware redesign: the
  slots must be NESTED SUBSPACES, not independent bins!!); (2) THE PAYOFF: bit-side
  only (the selected κ is COMPLEX-bound!!); (3) THE CONTEXT: the session is ~1595
  turns deep — the nesting redesign + the build are the fresh session's natural work
  (the handoff: THIS summary!!).

## THE NESTING-AWARE CUMULATIVE PACKING — THE SS1515 TARGET-SIDE BLOCKER SOLVED (ii19_121nest.py; SS1604)

- **THE CUMULATIVE DESIGN (the user's SS1601 'no keep pushing'!!)**: F_d = span(the
  items at the dims <= d) (+ the fillers to the dim d, chosen INSIDE F_{d+1}!!): the
  cumulative unions are INCREASING BY CONSTRUCTION -> **THE NESTING IS AUTOMATIC!!**
  The fillers' existence: cum[d] ⊆ F_{d+1} with rank(cum[d]) <= d -> the dim-d
  extension inside F_{d+1} ALWAYS EXISTS ✓; the final: F_8 = the t-perp ✓; THE
  NONDEGENERACY IS FREE (the 121-line system's span is POSITIVE-DEFINITE: every
  subspace nondegenerate!!!).
- **THE MEASUREMENT (SS1604!!)**: **THE CUMULATIVE PACKING IS FULLY FEASIBLE AT ALL
  THREE CROSSING THs**: TH=8: **UNPLACED 0** (the slots {2: 121, 3: 97, 4: 87, 5: 75,
  6: 241, 7: 1391, 8: 407}; the placed-per-target ~14-24!!); TH=16: **UNPLACED 0**
  (the slots {2: 121, ..., 7: 886, 8: 315}; the ~12-17!!); TH=24: **UNPLACED 0** (the
  slots {2: 121, ..., 7: 851, 8: 318}; the ~12-17!!).  **THE SS1515 '121/121 TARGET
  CHAINS FAIL' IS SOLVED ON THE TARGET SIDE: the cumulative design nests by
  construction!!!**
- **THE REMAINING NESTING — THE ROOM STRUCTURE (THE E8'S OWN MECHANISM!!!)**: the
  gcheck's gate rule (ALL the operands climb to the gate's frame!!) -> THE PIECE'S
  READ FRAMES MUST BE SHARED BY ITS DIM-GROUPS OF USERS (one frame per dim per
  chain!!) -> at each dim d: the reads (t, p) form the bipartite graph: the CONNECTED
  COMPONENTS = THE ROOMS: each room needs ONE shared dim-d frame ⊇ the room's
  pieces' union ⊆ THE COMMON PERP of the room's targets (the pieces ⊥ ALL the
  room's targets!!) — THE ROOM FRAMES' EXISTENCE: THE NEXT DECISIVE MEASUREMENT; AND
  the cross-dim nesting: the target's rooms R_d ⊆ R_{d+1} (the room at the dim d
  inside EACH member's (d+1)-room: the combined-rank checks!!): the joint constraint
  (the SS1374-style rooms + the cumulative!!).
- **THE STANDING**: the (c)-corrected crossings (TH >= 8: the fine-slack +2.32% to
  +15.41%!!) + THE TARGET-SIDE NESTING SOLVED (the cumulative!!!) + THE ROOM
  STRUCTURE (the piece-side + the joint: the next gates!!) + the bit-side-only
  payoff.

## THE ROOM MEASUREMENT — THE GIANT COMPONENTS FAIL; THE SINGLE-PIECE ROOMS ALWAYS SAFE (ii19_121rooms.py; SS1611-SS1615)

- **THE SCRIPT'S TWO BUGS FIXED BEFORE THE RESULT (SS1609/SS1613!!)**: (1) THE
  TAIL-NODE BUG: the tails (pid -1!!) all shared ONE node ('p', -1) across the 121
  targets -> ONE GIANT FALSE ROOM: fixed to the per-target ('tail', t) nodes; (2)
  the tails' CONTENTS were missing from the rooms' perp-checks: fixed (leftovers[t]
  included!!); (3) the print bug: dict[:14] (the slice on a dict -> KeyError!!):
  fixed to the full sorted list (no truncation!!).
- **THE ROOMS (the connected components of the per-dim read graphs!!)**: the naive
  cumulative slots: TH=8: the dims {2: (10, 0), 3: (21, 0), 4: (16, 2), 5: (25, 4),
  6: (7, 1), 7: (19, 1), 8: (26, 1)}: **TOTAL PERP-FAILS 9**; TH=16: 11; TH=24: 11.
- **THE ROOM SIZES (pieces, targets, perp-OK!!)**: THE OVERWHELMING MAJORITY SAFE:
  the single-piece rooms (1, k, True) for k = 1..63 (60-67 rooms of (1, 1, True) per
  TH!!!) — **THE SINGLE-PIECE ROOMS ARE ALWAYS PERP-SAFE (p ⊥ ALL its users: p ⊆
  each user's junk!!!)**; the failures: the multi-piece rooms (2-3, k, False) + **THE
  GIANT COMPONENTS: (60 pieces, 80 targets, False), (75, 20, False), (165, 102,
  False) at TH=8** (the transitive merges via the shared pieces + the co-reads!!!).
- **THE STRUCTURAL RULE (the honest!!)**: the room's frame ⊇ the room's pieces'
  union ⊆ THE COMMON PERP of the room's targets: the single-piece rooms: p ⊆ ∩ its
  users' perps ✓✓ ALWAYS; the multi-piece rooms: the TRANSITIVE members (p read by
  t1, t2; q read by t2, t3: the component {p, q, t1, t2, t3}: p ⊥ t3 NOT
  guaranteed!!!) -> the giant components FAIL.
- **THE E8'S SOLUTION — THE ROOM-TOTALS (the composites!!)**: the co-read pieces
  (the same target, the same dim!!) merged into THE COMPOSITES (p ⊕ q: the single
  registers!!!): the composite's room = a single-piece room -> ALWAYS SAFE ✓✓; the
  composites SHARED across the targets with the same co-read sets (THE E8'S
  ROOM-TOTAL MECHANISM: the R420's 12-frames!!!) — THE R IMPACT (the composites'
  counts + the sharing statistics!!): THE NEXT MEASUREMENT.
- **THE STANDING (after the rooms!!)**: the (c)-corrected crossings (TH >= 8:
  +2.32% to +15.41%!!) + the target-side nesting SOLVED (the cumulative!!!) + THE
  ROOMS: the single-piece safety + the giant fails + THE COMPOSITE/ROOM-TOTAL
  DESIGN (the next gate: the composites' sharing + the R impact!!) + the bit-side-only
  payoff.

## THE COMPOSITE RECURSION — THE TRUE REQUIREMENT: THE JOINT ROOM-FLAG DESIGN (SS1616-SS1619)

- **THE COMPOSITE APPROACH RECURSES**: the co-read pieces merged into the composites
  (the single (t, d)-registers: the composite ⊥ its user -> the single-composite
  room SAFE!!) — BUT the composite's BUILD: the srcs (the pieces!!) climb to the
  composite's frame: the pieces' chains through the MULTIPLE composites at the same
  dim hit THE SAME TRANSITIVE MERGE AT THE SRC-SIDE (the piece p src of c1 (t1's
  co-read) and c2 (t2's co-read): the room {p, c1, c2}: c1's content ⊥ t2 NOT
  guaranteed!!!) — THE RECURSION NEVER ENDS AT THE NAIVE LEVEL.
- **THE E8'S ACTUAL SOLUTION — THE FULL JOINT FLAG (the D4 structure!!!)**: the
  R420's rooms (the 12-frames!!) are the NESTED flags (the 4-frames ⊂ the
  12-frames ⊂ ...!!) whose co-read sets ARE the D4 structures: the co-read unions ⊥
  the rooms' targets BY CONSTRUCTION (the D4!!!) — THE 121-LINE WORD NEEDS THE SAME:
  the piece economy WITH the room constraints (the co-read sets' unions ⊆ the common
  perps!!!) — THE ROOM-SAFE REDESIGN.
- **THE NEXT MEASUREMENT (the push!!)**: the room-aware RE-SLOT (the pieces -> the
  dims with the per-dim components' perp-safety!!!) + the composites' fallback (the
  room-unsafe pieces -> the per-target merges: the R cost!!) + the (c)-hist + the
  price: DO THE CROSSINGS SURVIVE THE ROOM-SAFE REDESIGN?!

## THE ROOM-SAFE RE-SLOT — THE CATASTROPHE AT ALL THREE CROSSING THs (ii19_121safe.py; SS1624-SS1628)

- **THE COMPLETE 3-TH VERDICT (SS1628!!)**: TH=8: **unsafe 89/108 (82%!!)**, the
  fallback 1,945 reads, R_str 2,183, NO-ROOT; TH=16: **unsafe 47/54 (87%!!)**, the
  fallback 1,512, R 1,696, NO-ROOT; TH=24: **unsafe 45/52 (87%!!)**, the fallback
  1,481, R 1,663, NO-ROOT.  THE NO-ROOT IS THE HOSTING WALL (the nres = 9R ~ 15,000
  >> the cap 4,356: THE R >> 4v = 484!!!) — the room-safe designs (my greedy's!!)
  are WAY beyond the wall.  (The KeyError crash at SS1624 — tgt_dims[t] not
  initialized for the no-read targets!! — fixed with setdefault at SS1626!!).
- **THE HONEST CAVEAT — MY GREEDY OVERSHOOTS**: the big-user-pieces-first ordering
  creates the components early; the later pieces (the overlapping-but-different user
  sets!!) fail the transitive perp-checks -> the 82-87% rejects.  THE NAIVE SLOTS
  (SS1615!!) had only 9 failing rooms (the giants: the ~165-item transitive
  components at the heavy dims 6-8!!) — THE TRUE OPTIMUM IS BETWEEN: the
  constraint-satisfaction (the pieces -> the dims with the per-dim perp-safety,
  minimizing the composites!!) — the repair (the local search: the giant rooms'
  pieces moved to the other dims!!) is the bounded attempt.
- **THE STRUCTURAL INSIGHT (the deeper!!)**: THE ROOM-SAFETY (the transitive
  perp-safety!!) IS NOT FREE FOR THE JUNK-INTERSECTION PIECES: the E8's D4 luck
  (the co-read sets ARE the D4 structures: perp-safe BY CONSTRUCTION!!!) does NOT
  transplant — the 121-line economy's co-reads create the giant transitive merges —
  THE ROOM-SAFE ECONOMY (the pieces CHOSEN with the co-read perp-safety!!) is the
  deeper redesign.
- **THE STANDING (after the room-safety layer!!)**: the model crossings (TH >= 8:
  the fine-slack +2.32% to +15.41%!!) are computed on the hist models ASSUMING the
  room-nesting — THE ROOM-SAFETY LAYER SHOWS THE NAIVE DESIGNS NOT REALIZABLE and
  the naive fixes catastrophic (my greedy!!!) — the remaining paths: (a) THE REPAIR
  (the local search: the giant rooms' pieces re-dimensioned!!) — the bounded
  attempt; (b) THE ROOM-SAFE ECONOMY — the substantial redesign (the pieces chosen
  so the co-read unions stay perp-safe BY CONSTRUCTION, the E8's D4 way!!); (c) the
  handoff (the fresh session with THIS record!!!).

## THE REPAIR SCAN — REPAIRABLE 0 AT EVERY TH; THE STRUCTURAL WALL CONFIRMED (ii19_121repair.py; SS1633-SS1636)

- **THE SCAN (SS1636!!)**: for each failing (piece, dim) pair (TH=8: 234 pairs!!):
  the alternative dims (the span + the cumulative rank + the merged perp-safety!!):
  **REPAIRABLE 0, UNREPAIRABLE ALL** — the fallback explosion (TH=8: the fb reads
  6,079!!): R 6,317 / TH=16: 5,265 / TH=24: 5,210 — ALL WAY BEYOND THE HOSTING WALL
  (484!!) -> NO-ROOT everywhere.  (The SS1609 tail bug was caught AGAIN in the
  repair script's component structures (the shared ('p', -1) nodes + the pool[-1]
  negative indexing!!) and fixed BEFORE the run at SS1634!!)
- **THE STRUCTURAL WALL (the mechanism!!)**: THE LIGHT DIMS (2-5!!) ARE FULL (the
  naive cumulatives: rank(cum[d'] + piece) > d' — the capacity check fails!!) and
  THE HEAVY DIMS (6-8!!) ARE TRANSITIVE-UNSAFE (the merged components' perp-fails!!)
  — **THE PIECES ARE TRAPPED: NO SAFE DIMS AT ANY SLOT ASSIGNMENT!!!**
- **THE COMPLETE VERDICT (the honest close!!)**: the naive junk-intersection
  economies are NOT REALIZABLE under the gcheck's room-safety: the model crossings
  (TH >= 8: the fine-slack +2.32% to +15.41%!!) stand ONLY on the unrealizable hist
  assumptions — the fixes (the re-slot greedy (SS1628!!), the repair/composites
  (SS1636!!)) explode the R (5,210-6,317 >> the wall 484!!).
- **THE STRUCTURAL INSIGHT (final!!)**: THE E8'S D4 LUCK (the co-read sets ARE the D4
  structures: perp-safe BY CONSTRUCTION!!!) DOES NOT TRANSPLANT — the room-safety
  must be CONSTRUCTED: THE ROOM-SAFE ECONOMY (the pieces CHOSEN so the co-read
  unions stay perp-safe BY CONSTRUCTION, the E8's D4 way!!!) — THE SUBSTANTIAL
  REMAINING REDESIGN.
- **THE SESSION'S HONEST PATTERN (the SS1470 observation, completed!!)**: every
  honesty layer moved the number DOWN (the CST: +13.42% -> -7.97%!!; the h=10:
  +33% -> -11%!!; the (c)-correction: +2.77% -> -2.45%!!) — **THE ROOM-SAFETY LAYER
  IS THE FIRST THAT BREAKS THE REALIZABILITY OUTRIGHT (not just the price!!): the
  naive designs DO NOT EXIST as legal words.**

## THE ROOM-FIRST DESIGN — THE CLUSTER CENSUS: +15.27% AT THE STRUCTURAL R = 271; THE CHAIN-BUDGET COLLISION (ii19_121cluster.py; SS1645-SS1649)

- **THE CENSUS (SS1649!!)**: the pair common-perps: {31: 3,780 (the ip = +-1 root
  pairs!!), 37: 3,360 (the orthogonal root pairs!!), 63: 120 (the special's pairs!!)}
  — ALL >= 12 (7,260/7,260!!); the greedy clusters: 141 groups (the sizes {6: 58,
  8: 16, 12: 10, 13: 8, ...} — **THE ~6-TARGET GROUPS: THE E8'S '70 quads x 6
  targets' ANALOG!!!**); the rooms: the dims {4: 8, 5: 128, 6: 4, 7: 1}, the
  contents {12: 8, 13: 128, 21: 4, 37: 1} (**the ~13-line dim-5 rooms: THE E8'S
  12-FRAMES ANALOG!!!**), the room-reads 967; the coverage: the mean tail 35.7 (the
  zero-tail 0; **the special's tail 102: the poor coverage (the 8 rooms x 13 lines:
  the ~18 unique!!)**); **THE R: 141 rooms + 121 tails + 9 gathers = 271; the demand
  1,088 (45% of 9R: the arrival law FINE!!); THE PRICE: +15.27% (the coarse AND the
  fine: the slack-0!!!) — THE CROSSING AT THE STRUCTURAL R WITH THE PERP-SAFETY BY
  CONSTRUCTION (the rooms' contents ⊆ the common perps!!!)**.
- **THE HONEST COLLISION (the chain budget!!)**: the rooms' dims are FIXED by the
  groups' common perps (the frames ⊆ the common perps: THE RAISING IMPOSSIBLE — the
  fillers would leave the common perp!!!); the targets' ~8 rooms are ~all at dim-5
  (the 128/141 dim-5 rooms!!): **THE TARGET'S CHAIN HAS ONE dim-5 SLOT — THE ~7 DIM-5
  ROOMS CANNOT SHARE IT** (the frames differ; the shared frame would need ⊆ EVERY
  user's perp: the contents fail the cross-users' perps!!!) — THE CHAIN-BUDGET
  COLLISION (the same class as the SS1515/SS1636 walls, but NOW THE CONTENTS ARE
  PERP-SAFE BY CONSTRUCTION: the question is the DIMS!!!).
- **THE IDENTIFIED FIX — THE DIM-DIVERSITY CLUSTERING**: the per-target rooms at
  the DISTINCT dims 2-8 (the cap 7!!): the un-grown pairs give the dim-7 rooms (the
  37-line contents: the BIG coverage!!), the grown groups the dim-5s — the target's
  ~7 rooms spanning the ~7 dims; the honest cost: the low-dim rooms' small contents
  (the dim-2-3 common perps: the ~2-5 lines!!) -> the bigger tails — THE
  MEASUREMENT (ii19_121cluster2.py!!!).
- **THE OTHER HONEST FLAGS**: (a) the special's delivery: the heavy tail 102 (the
  (c)-corrected mass counted ✓!!); (b) the threshold 12: the sensitivity
  unmeasured; (c) the payoff: bit-side only (the complex-bound κ!!); (d) the
  nesting: the rooms' frames' cumulative nesting along the targets' chains:
  unverified (the dim-diversity design's layer!!!).

## THE DIM-TARGETED CLUSTERING v4 — +26.31% AT R=229; THE NESTING GATE => THE GROUP-NESTING (THE FLAG!!) INSIGHT (ii19_121cluster3/4.py; SS1657-SS1661)

- **THE v3 (SS1657!!)**: the dim-aware stopping: 63 groups BUT the CP-PRESERVERS (the
  c's orthogonal to the WHOLE current common perp: the ⊥-complement's lines!!) stall
  the growth: THE DIM STUCK AT 7 -> 7,197 rejects -> the 112 targets with ONE room
  (the degenerate +36.81%: the SS1575 artifact class!!).
- **THE v4 (SS1661!!)**: THE DIM-TARGETED GROWTH (the c's must MOVE the dim (d2 !=
  d: the cp-preservers SKIPPED!!!) + land on a dim FRESH for ALL!!!) + THE FAST PATH
  (d = 9 - span_rank(grp): the ⊥-complement!!! verified vs SS1649/SS1657!!):
  **100 groups: the 60 dim-7 pair-rooms (the 37-line contents!!) + the 40 dim-6
  triple-rooms (the 21-line!!); THE PER-TARGET DIM-DIVERSITY {2: 120}: EVERY target
  has 2 rooms at the DISTINCT dims {6, 7} — THE CHAIN-SLOTS SOLVED BY
  CONSTRUCTION!!!**; the coverage: the mean tail 22.7 (the zero-tail 1!!); **THE R:
  100 + 120 + 9 = 229; the demand 360 (36% of 9R!!); THE PRICE: +26.31% (the coarse
  AND the fine: the slack-0!!) — THE BEST STRUCTURAL CROSSING YET: the perp-safety BY
  CONSTRUCTION (the contents ⊆ the common perps!!!) + the distinct chain-slots +
  the arrival 36%!!!**
- **THE NESTING GATE (the new wall, found in the analysis!!)**: the target's chain
  frames must NEST (F6 ⊂ F7 ⊂ the t-perp!!): the F7 = the dim-7 room's content's span
  (FORCED: the dim-7 content ⊆ F7 with the dims equal!!); the F6 = the dim-6
  content's span; the nesting ⇔ **span(dim-6 content) ⊆ span(dim-7 content) ⇔
  span(the dim-7 group) ⊆ span(the dim-6 group)** (the ⊥-duality!!!) — GENERICALLY
  FALSE (the c3 ∉ span([t, c1, c2])!!!): **THE v4's 2-ROOM CHAINS ARE ILLEGAL
  AS-IS**.
- **THE GROUP-NESTING INSIGHT (THE E8'S FLAG ANALOG!!!)**: the fix: **THE ROOMS'
  GROUPS NESTED along each target's chain: the pair [t, c1] ⊂ the triple [t, c1,
  c2] ⊂ the quad ... (the dims 7, 6, 5, ...!!)**: the contents nest (the dim-7 ⊇
  the dim-6!!): the frames nest ✓✓ LEGAL; the coverage: the XOR-unions (the dim-7 ⊕
  the dim-6 = the dim-7 − the dim-6 (the ⊆!!): the ~37 for t; the c1's: its own pair
  ⊕ this triple (the NEW ~9!!!): THE ROOMS USEFUL FOR THE OTHER USERS ✓✓✓ —
  **THE FLAG STRUCTURE = THE E8'S D4 WAY (the cells ⊂ the quads!!!)** — the v5: the
  nested-group clustering (the shared flags!!!).

## THE TAILS' SOURCE-CHAIN GATE — THE TOTAL COLLISIONS: THE WALL FOR EVERY ROOM-FIRST VERSION (ii19_121tails.py; SS1666-SS1671)

- **THE CHECK (SS1671!!)**: the v3's structure (the 63 rooms: the 60 dim-7
  pair-rooms!!!) + the tails (the ~27-line leftovers: the spans {1: 1, 7: 118, 8:
  2}!!!): **THE FRAME-LEVEL COLLISIONS: the (source, dim) slots 203; the
  distinct-frames-per-slot histogram {1: 60, 2: 24, 4: 1, 6: 1, 7: 1, 9: 2, 10: 2,
  14: 1, ..., 25: 8, 26: 8, ..., 41: 2, 42: 1}: THE COLLISION SLOTS 143/203
  (70%!!!); THE WORST SLOT: 42 DISTINCT FRAMES; THE EXCESS READS 3,081** — the
  sources' ONE-FRAME-PER-DIM chains CANNOT host the ~27 tails' builds (the ~dim-7
  spans: the ~14+ distinct frames per slot!!!): **THE TAILS' SOURCE-CHAINS ARE THE
  WALL — the SS1589's (b) class, the same as the SS1575 all-tail at the ~2.4x
  smaller scale!!**
- **THE VERDICT**: EVERY room-first version (the v1's +15.27%, the v3's +36.81%,
  the v4's +26.31%!!!) stands on the tails' builds whose source-chains collide
  TOTALLY — **THE PER-TARGET TAILS (the ~27-line leftovers at the ~dim-7 spans!!)
  ARE ILLEGAL AS-IS** — the fixes: (a) THE RECURSIVE ROOM-FIRST (the tail-rooms:
  the tail-groups' shared frames: the leftover co-occurrence!!!); (b) THE
  PARTITION-STRUCTURE (the per-target disjoint rooms: the XOR-clean coverage!!!);
  (c) the coverage improvement (the tails' shrink!!!).
- **THE ARC'S COMPLETE WALLS (all measured!!!)**: (1) THE CHAIN-SLOTS (the v1!!!)
  -> the dim-diversity (the v3/v4!!) ✓; (2) THE NESTING (the v4!!!) -> the
  group-nesting (the flags: the ⊥-duality!!!) ✓ at the XOR-cost; (3) THE
  XOR-CANCELLATION (the nested contents!!!) -> the delta-rooms/the
  disjoint-partition; (4) **THE TAILS' SOURCE-CHAINS (the SS1671!!!): THE WALL FOR
  EVERY VERSION** — the recursive room-first is the identified path.

## THE TAIL-ROOMS + THE FULL COLLISION CENSUS — THE ROOMS' SOURCES COLLIDE TOO; THE PARTITION INSIGHT (ii19_121tailrooms.py; SS1676-SS1679)

- **THE TAIL-ROOMS' GREEDY (SS1679!!)**: the pairs' shared leftover-lines: only 19
  tail-rooms formed (from the 6,497 candidates!!): THE GLOBAL CONSUMPTION STARVES the
  later pairs (the fresh-shared < 3!!!) — the residuals: the mean 25.2 (barely down
  from the 27.1!!!): the first cut INEFFECTIVE.
- **THE FULL COLLISION CENSUS (THE DECISIVE FINDING — the SS1676 fix: the ROOMS'
  sources INCLUDED!!!)**: the (source, dim) slots 313; the frames-per-slot histogram
  {1: 180, 2: 12, 33: 1, 34: 3, ..., 42: 14, ..., 52: 2, 59: 1}: **THE ROOMS'
  SOURCES COLLIDE MASSIVELY: the ~33-59 DISTINCT FRAMES PER SLOT (the ~30-50 room
  memberships per source line, ALL AT DIM-7!!!)** — **THE ROOMS' BUILDS ARE ILLEGAL
  AS-IS (the SS1589's (b) wall AT THE ROOM LEVEL!!!)** — the rooms' contents (the
  ~37-line FULL common perps!!) give each source ~30-50 rooms.
- **THE DEEPEST INSIGHT OF THE ARC (THE E8'S RESOLUTION DERIVED!!!)**: HOW DOES THE
  E8 AVOID THIS?! — **THE D4 PARTITION = THE SOURCES' FRAME PARTITION**: the 120
  roots partitioned into the 30 DISJOINT 4-frames; each source's cells ALL LIVE
  INSIDE ITS ONE 4-FRAME (the partition's disjointness!!!) — the sources' climbs:
  THE ONE dim-4 FRAME PER SOURCE ✓✓✓ NO COLLISION — **THE PIECES MUST BE
  PARTITION-STRUCTURED (the sources' ONE frame per dim!!!), NOT THE FULL PERPS!!!**
- **THE FULL E8-STYLE REDESIGN (the identified path!!)**: (1) THE PARTITION: the 121
  lines -> the ~30 4-frames (the E8's D4 partition of the 120 roots + the special's
  singleton!!); (2) THE PIECES: the INSIDE-the-frames subsets (the ~2-4-line cells
  with the ~12-30 users!!!); (3) THE READ-ROOMS: the co-read groups' shared frames
  (the perp-safe BY CONSTRUCTION ✓✓); (4) THE TAILS: the small leftovers — **the
  substantial remaining work** — the feasibility scan first (the partition + the
  pieces' users + the coverage + the R!!!).
- **THE PRICE NOTE**: the SS1679's +30.52% at R=211 (the (c)-model!!) — ON THE
  ILLEGAL structure (the rooms' source-collisions!!!) — the model crossings stand
  ONLY on the unresolved source-chain structure.

## THE PARTITION-STRUCTURED PIECE ECONOMY — THE FEASIBILITY SCAN: THE E8-GRADE ECONOMY EXISTS (ii19_121pieces.py; SS1682-SS1685)

- **THE SCAN (SS1685!!)**: **THE PARTITION: 30 DISJOINT 4-FRAMES, 120/120 COVERED (the
  E8's D4 partition's exact analog!!!)**; the piece candidates: 330 (the users {13: 30
  (the quads!!), 14: 120 (the triples!!), 31: 180 (the pairs!!)}); **THE GREEDY ECONOMY
  (TH_SAVE=4): 210 PIECES (180 pairs + 30 quads!!); THE USERS-PER-PIECE {13: 30, 16:
  120, 18: 60} — THE E8-GRADE SHARING (the E8's cells: the ~12 users!!!)**; **THE
  COVERAGE: THE LEFTOVERS {0: 1, 2: 120}: EVERY ROOT TARGET HAS ONLY 2 LINES UNCOVERED
  (the special: 0!!!)** — the pieces cover ~62/64 lines per target!!!; **THE SOURCES'
  CHAINS LEGAL BY CONSTRUCTION (the partition: the ONE 4-frame per source!!! ✓✓✓ THE
  SS1679 WALL AVOIDED)**.
- **THE R + THE ARRIVAL**: the pieces 210 + the tails 120 + the gathers 9 = R_struct
  339; **THE DEMAND 3,510 = 29/line (vs the E8's 25/line!!) — THE ARRIVAL LAW BINDING:
  9R >= 3,510 -> R_hon 390 (the slack 51!!)**; **THE PRICE AT R_hon 390: the coarse
  +2.77% / the fine -1.22% — THE BRACKET STRADDLES THE FRONTIER**.
- **THE KNOWN FIRST-CUT LIMITATION (the SS1682's honest flag!!)**: the
  reads-at-the-build: the target reads its ~21 pieces at the ~15-20 DIFFERENT 4-frames:
  THE ONE dim-4 SLOT COLLIDES — **THE READ-ROOMS NEEDED (the pieces' climb-frames: the
  co-read groups' shared frames: the E8's quads!!!)** — the pieces' contents (the ~2-4
  lines!!) make the read-rooms' contents the PIECES' UNIONS (the ~6-12 lines: NOT the
  full perps!!!) — THE SS1679 WALL AVOIDED BY CONSTRUCTION ✓✓✓.
- **THE REMAINING GATES**: (a) THE READ-ROOMS (the co-read clustering (the ~4-6-target
  groups: the E8's '6 targets per quad'!!!) + the dim-diversity (the SS1655-SS1661's
  lessons!!!) + the honest (c)-hist (the pieces' chains [0, 4, the read-dims, 9]!!!) +
  the re-price!!); (b) the demand/coverage trade-off (the TH_SAVE sweep: the coarser
  pieces: the fewer users: the lower demand!!!); (c) the payoff: bit-side only (the
  complex-bound κ!!).

## THE READ-ROOMS (THE PAIRS-ONLY FIRST CUT!!) — THE COLLISIONS AT THE PIECE LEVEL; THE PRICE DROPS BELOW (ii19_121readrooms.py; SS1690-SS1695)

- **THE RUN (SS1695!!)**: the read-rooms: 229 (the dims {2: 44, 3: 48, 4: 20, 5: 56,
  6: 60, 7: 1}!!); **THE RESIDUALS: 767** (the pieces' users NOT covered: the ~23% of
  the 3,390!!!) — the direct reads (the collision-y: the SS1682 flag!!); **THE
  PIECE-ROOM COLLISION CENSUS: {1: 41, 2: 128, 3: 6, 4: 92, 6: 46, 8: 50, 9: 4} —
  ONLY 41/367 SLOTS LEGAL (the ONE room!!!): THE ~89% COLLIDING (the 2-9 rooms per
  (piece, dim) slot!!!)** — THE SS1679-CLASS WALL AT THE PIECE-READ LEVEL; **THE
  PRICE: the coarse -4.41% / the fine -7.87% (BELOW THE FRONTIER!!)** — the hist's
  finer jumps (the pieces' [0, 4, the read-dims, 9]: the ~3-4 small climbs!!) moved
  the LM UP (15,805 vs the 14,362!!) -> the price DOWN (THE SS1547 TWO-PARAMETER
  MODEL: THE LOWER LM: THE HIGHER PRICE — the SS1572/SS1575 sweeps confirm!!!).
- **THE FIX IDENTIFIED — THE PER-PIECE PER-DIM ROOM-MERGING**: the piece's rooms at
  the same dim: THE MERGED (the ONE frame per dim!!!): the merged group = the union
  of the room-groups; the pieces ⊥ the unions BY CONSTRUCTION (the co-read!!!) ✓✓✓
  LEGAL BY CONSTRUCTION — the honest costs: (a) the merged rooms' co-read = the ∩
  (the fewer pieces per room!!!) -> the residuals grow?!; (b) THE TARGET-LEVEL
  COLLISIONS (the target's ~21 rooms at the same dim: the DIFFERENT unions!!!) — the
  census needed too!!! — THE MEASUREMENT (the next script!!).
- **THE REMAINING GATES**: (a) the merged rooms' legality (the piece-level ✓ by
  construction + the target-level: the census!!!); (b) the 767 direct reads; (c) the
  demand 3,510 (the arrival-bound R_hon 390!!!); (d) the payoff: bit-side only (the
  complex-bound κ!!).

## THE MERGED ROOMS — THE PIECE-LEVEL IMPROVED ~5x (11% -> 53% LEGAL!!); THE TARGET-LEVEL WALL (ii19_121merge.py; SS1698-SS1702)

- **THE RUN (SS1702!!)**: the merged rooms: 258 (the group sizes {2: 24, 4: 71, 6: 5,
  8: 66, 12: 38, 16: 50, 18: 4} — the pairs' unions ✓!!); the dims {2: 96, 3: 22, 4:
  61, 5: 75, 6: 2, 7: 2}; **THE PIECE-LEVEL CENSUS: {1: 288, 2: 114, 3: 55, 4: 30,
  ..., 14: 1} — THE LEGAL SLOTS 288/545 (53%!!) — UP FROM THE SS1695's 41/367
  (11%!!!): THE PER-PIECE PER-DIM MERGING IMPROVED THE PIECE-LEVEL LEGALITY ~5x**
  (the co-read pieces' memberships (the q's in the pids!!!) still create the ~47%
  colliding slots: the 2-14 rooms at the same dim!!); **THE TARGET-LEVEL CENSUS:
  {1: 116, 2: 77, 3: 58, ..., 11: 58, ..., 18: 4} — THE TARGET'S DISTINCT
  ROOM-FRAMES PER DIM: THE ~400/516 SLOTS COLLIDING (the 2-18 FRAMES AT THE SAME
  DIM!!!): THE SS1679-CLASS WALL AT THE TARGET LEVEL**; **THE PRICE: the coarse
  -2.41% / the fine -6.03% (BELOW!!) — the LM 15,383 (the hist similar to the
  SS1695's: the shape-sensitivity confirmed (the SS1547 two-parameter model!!!))**.
- **THE VERDICT**: the per-piece per-dim merging improved the piece-level legality
  (the 11% -> the 53%!!) BUT the target-level collisions are the wall (the ~74% of
  the slots!!!) — the pieces' read-rooms need **THE JOINT COORDINATION: THE ONE
  FRAME PER (piece, dim) AND PER (target, dim)!!!** — the SS1374-style slot design
  (the E8's D4 flag: the JOINT structure!!!) — the substantial remaining work (the
  CP-SAT/the joint greedy: the hours!!!).
- **THE HONEST STATE OF THE ARC**: the partition-structured piece economy (THE
  E8-GRADE ✓✓✓: the 210 pieces, the 13-18 users, the ~2-line tails, THE SOURCES'
  CHAINS LEGAL BY CONSTRUCTION (the partition!!!) — THE SS1679 WALL AVOIDED!!) +
  the read-rooms' layer (the piece-level ~47% + the target-level ~74% colliding!!!)
  — the joint coordination is the identified path; the price straddles at the
  arrival-bound R_hon 390 (the model level!!!) on the unresolved read-structure.

## THE R420's ACTUAL JOINT STRUCTURE — MEASURED (r420_rooms.py; SS1734-SS1736): THE REDESIGN'S GROUND TRUTH!!!

- **THE FRAMES' ENCODING**: THE FLAT LINE-INDEX LISTS (the SS1446 confirmed!!): {empty: 1,
  len-1: 120 (the singletons!), len-2: 180 (THE CELLS!), len-12: 70 (THE D4 ROOMS!), len-30:
  180, len-63: 120 (THE PERPS!), len-120: 1 (FULL!)} — **THE TRUE DIMS: {0: 1, 1: 120, 2:
  180, 4: 70, 6: 180, 7: 120, 8: 1}** — the cells dim 2; the 12-line rooms dim 4 (!!!); the
  30-line frames dim 6 (!!!); the perps dim 7; FULL dim 8 — **THE FLAG: 0-1-2-4-6-7-8!!!**
- **THE SOURCES' CHAINS: [1, 1, 2]** — every source: 3 A-gates: **2 READS AT ITS OWN
  SINGLETON (THE NO-CLIMB — FREE!!!)** + 1 read at its dim-2 CELL (the ONE climb 1->2!!)
  — the sources' chains: {s} -> the cell -> ... -> FULL ✓ NESTED!!!
- **THE A-GATES (2,064!!)**: {'0 srcs, 1 helper-src': 1,695 (!!!), '1 srcs, 0 helper-srcs':
  360, '0 srcs, 23-46 helper-srcs': 9} — **THE INCREMENTAL RUNNING SUMS (the 1,695
  helper-from-helper gates at the INCREASING frames!!) + the 360 source-reads (the 3 per
  source: the 2 singleton + the 1 cell!!) + THE 9 BIG GATES (the gathers at FULL!!)**
- **THE B-GATES (837!!)**: the 240 target-dest (the targets' reads!) + the 597 z-dest
  (**THE B-PHASE BUILDS TOO!!!**) — the per-target {2: 120}: **THE TARGETS READ ONLY 2
  GATES: the dims [2, 7] (THE CELL + THE PERP!!!)** — the targets' chains: 0 -> the cell
  (2!) -> the perp (7!) -> the final ✓✓ NESTED!!!
- **THE PIECES' READ-ROOMS: THE COLLISIONS ZERO!!!** — the helpers read in B: 240: the
  per-helper {1: 120, 2: 120} — **THE PIECES READ AT MOST TWICE: the dims [6, 7] (the
  INCREASING!!)** — **THE E8's ACTUAL ECONOMY: THE BIG RUNNING-SUM PIECES (the 1-2
  reads!!) AT THE SHARED BIG FRAMES (the dim-6 30-frames + the dim-7 perps!!) — NOT THE
  13-18-USER SMALL PIECES!!!**
- **THE D-GATES: 120 (one per target!!) — THE SRCS-COUNT ~121-149 (!!!)** — **THE
  TRANSITIVE INDICATOR-PARITY DIRT (the running sums LEAK the indicators; the D
  pre-reads the FULL transitive parity set!!! — the SS1733 analysis CONFIRMED!!)**
- **THE SCATTER**: the ret: 9 (the gathers!); the per-target lists of 2-8 (the W ✓); THE
  FORMAT: NO ret_frames (the old format!!) — my build: the current gcheck's format (the
  vector bases + ret_frames: the identity-word precedent!!)
- **THE FIRST-CUT REJECT (SS1732!!)**: 'climb not nested (reg 0)' — the sources' chains
  (the pieces-at-their-spans: the ~2-7 per source!!) — THE PREDICTED WALL ✓ the gcheck's
  feedback ✓
- **THE REDESIGN'S RECIPE (the E8's way!!)**: (a) THE CARRIERS: the sources read 1-2x at
  their OWN singletons (FREE!!!) into the first-level carriers; (b) THE INCREMENTAL TREE:
  the helper-from-helper running sums at the INCREASING flag-frames (the cells (2!) ->
  the rooms (4!) -> the big frames (6!) -> the perps (h-1!!) -> FULL (h!!)); (c) THE
  TARGETS: the ~2-4 reads each (at the cell-level + the perp-level frames!!); (d) THE
  TRANSITIVE DIRT: the D-srcs = the indicator-parity set of the read-vals (the
  SIMULATION!!!); (e) THE PIECES READ 1-2x (the big contents!!) — NOT the 13-18x small
  pieces — **MY SS1685 ECONOMY IS NOT THE E8's STRUCTURE: THE COMPLETE REDESIGN**

## THE R420 CONTROL — THE PERFECT MATCH: THE COMPLETE VERIFICATION MACHINERY VALIDATED (r420_tree.py; SS1742-SS1745)

- **THE VAL-SIMULATION (SS1742/SS1745!!)**: the full bitmask replay of the published R420:
  **THE FINAL-VALUE CHECK: 0 BAD REGISTERS ✓✓✓** (the semantics: the phases
  D/A/scatter/B/C, the climbs, the val-XORs — EXACTLY understood!!) — the hist's first
  reconstruction missed **THE COPY CHILDREN** (the gcheck's line 114: the rets' frames'
  dims x 9 = {8: 9}!!) — the 3.08x price artifact — **THE FIX (SS1743!!): the hist2 =
  the climbs + the copies: {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9} — THE MASS 5112 =
  THE IDENTITY (8x420 + 72 + 2x120x7) ✓✓✓**
- **THE CONTROL (SS1745!!)**: **THE RECONSTRUCTED c = 0.001653826988146798944268 —
  THE RATIO 1.0 vs THE PUBLISHED — THE DEVIATION 8.8e-21% (the mpmath precision
  floor!!!)** — **THE COMPLETE VERIFICATION MACHINERY VALIDATED END-TO-END: the word
  -> the replay -> the true hist -> the true price ✓✓✓ THE SAME MACHINERY THAT WILL
  VERIFY THE 121-LINE WORD**
- **THE R420's FULL TREE (the transplant recipe!!)**: (a) THE 540 build-dests = the 120
  sources + the 420 helpers (**THE SOURCES ARE ACCUMULATED TOO!!!**); the 360 carriers
  (the any-source-src!) + the 180 pure sums; (b) THE SUMS' CHAINS: the dim-2 first-gates
  (from the carriers!) then the dim-4 single-src accumulations (599!!) + the 84 dim-6 +
  the 9 dim-8 big finals (the 23-46 helper-srcs!!); (c) **THE TARGETS: the 2 gates: THE
  DIM-2 DIRECT SOURCE-READ (one junk line delivered at the cell!!!) + THE DIM-7 3-SRC
  TOP-SUM READ (the junk's bulk!)** — the read-gates {'dim 2, 1 srcs': 120, 'dim 7, 3
  srcs': 120} ✓; (d) THE GATHERS: the flag-chains (the dim-2/4/6 incremental!) + the
  dim-8 big finals ✓
- **THE REDESIGN'S RECIPE (the 121-line!!)**: the flag: the singletons (1!) -> the
  cells (2! the junk-pairs!) -> the partition 4-frames (4!) -> the big shared frames
  (6-7!) -> the perps (8!) -> FULL (9!); the sources read 1-2x free at the singletons +
  ~1x at the cells; the incremental tree (the dim-2 -> dim-4 -> dim-6 chains!); the
  targets: the ~1 dim-2 direct read + the ~3 top-sum reads at the perp-level frames;
  the gathers: the flag-chains + the big FULL finals; **THE TRANSITIVE D-DIRT (the
  simulation's parity!!)**

## THE R420's CARRIERS' CHAINS — THE FREE RE-READS AT THE SAME FRAME: THE MISSING MECHANISM (r420_tree.py; SS1750-SS1752)

- **THE CARRIERS' CHAINS (SS1752!!)**: the 240 helper-carriers read; the per-carrier
  read-count {2: 60, 4: 3, 5: 25, 6: 56, 7: 53, 8: 12, 9: 8, 10: 9, 11: 12, 12: 1, 13:
  1} — **THE CHAINS' DIMS: [2, 4, 4, 4, 4, 6, 7] etc. — THE REPEATED DIM-4 READS!!!**
  — the read-frames dims {2: 240, 4: 634, 6: 180, 7: 156, 8: 169} — the non-increasing
  flag: 179/240 — **THE RESOLUTION: THE RE-READS AT THE SAME FRAME ARE FREE (the
  gcheck's `if cur[r] == F: return`!!!)** — the carrier's 4 dim-4 reads: THE SAME
  12-FRAME (the ONE room per dim!!!) — THE R420 PASSES (the published word!!) ✓✓✓
- **THE DECISIVE MECHANISM (the missing piece of the whole 121-line arc!!!)**: the
  one-frame-per-dim constraint is per DISTINCT FRAME (the climbing chain!), NOT per
  read!!! — a register read 100x at the SAME frame: FREE (no climb, no cost, no
  collision!!!) — **THE ROOM SHARING IS THE ECONOMY (not the read-count!!!)** — the
  SS1695/SS1702 collision analyses counted the READS, not the DISTINCT FRAMES — the
  phantom collisions: the same-frame re-reads!!!
- **THE R420's FINAL PICTURE**: the flag 0-1-2-4-6-7-8; the carriers (the ~240!) with
  the ONE room per dim (the cell (2!), the 12-frame (4!), the 30-frame (6!), the perp
  (7!)) — the ~2-13 reads at the ~4-7 DISTINCT frames (the free re-reads!!!); the
  sums: the accumulations AT the rooms; the targets: the [2, 7] two-frame reads; the
  gathers: the flag-chains + the FULL finals; THE TRANSITIVE D-DIRT
- **THE 121-LINE'S RECIPE (complete!)**: THE ROOMS FIRST (the shared frames per dim:
  the cells (2!), the partition 4-frames (4!), the dim-6 analogs, the perps (8!)),
  then the carriers/sums AT the rooms (the free re-reads!!!), the targets' few-frame
  reads, the transitive dirt!!!

## THE h=10 DISCOVERY KILLS THE 2-CLASS CROSSING; THE 121-LINE SYSTEM (THE UNIQUE h=9-VALID II19 SUBSET): the CST=72 model-band crossing RETRACTED at the honest CST=81 (ii19_2class_h10.py, ii19_121.py, ii19_121v2.py)

- **THE h=10 DISCOVERY (the SS1380-1381 '100% verified' directive's first catch!!):** reading
  the identity-word template (e8_identity_word.py) + gcheck.py exposed that the 2-class lines
  (α,0,0)+(α,1,0) span a 9-dim space with a DEGENERATE form (the radical: the level direction
  (0,1,0)); gcheck line 71 forces the sources+helpers to end at a dim-h FULL frame, and every
  frame must be NONDEGENERATE (the exact Gram determinant!!) -> FULL = the 10-dim ambient ->
  h = 10, NOT 9!!!  THE ENTIRE SS1354/SS1374 CROSSING (+33% at h=9!!) WAS COMPUTED AT THE
  WRONG h.  THE HONEST h=10 BAND: -11.36% at best (D, R=280): THE 2-CLASS CROSSING IS DEAD.
  (The B/C variants' h=9-tuned constants were also fixed: clean mass-fraction models.)
- **THE DEMAND/DECODER CONSISTENCY (the SS1402 lesson):** the word's B determines BOTH the
  junks (the B-rows off the diagonal) AND the retained count (the GF(2) rank!!).  The
  min-index cancellation junks (33/57 lines) give the junk-pattern B the GF(2) rank 114 ->
  the decoder would need 114 retained (CST 912!!) -> NO ROOTS: DEAD.  THE CONSISTENT FAMILY:
  THE PERP-PATTERN DECODER (B[t] = {t} ∪ perp(t): THE R420'S OWN FAMILY!!).
- **THE 121-LINE SYSTEM (the UNIQUE h=9-valid II19 subset!!):** the 120 E8 roots + the
  special (0,1,1): the span dim 9 with the form x·x' + 2aa': POSITIVE-DEFINITE -> EVERY
  SUBSPACE NONDEGENERATE (the frame-friendly system!!) -> h=9 LEGAL (m=73: the
  P111-analogous window!!).  THE PERP-PATTERN DECODER: THE GF(2) RANK 9 EXACTLY (the E8's
  own!!).  The demands: 64 (the roots: 63+special) + 120 (the special: all roots).  THE
  SPECIAL RIDES FREE: 118 of its 120 demand lines covered by the pieces (every root-piece
  ⊆ the special's junk -> the special is a user of every piece!!).
- **THE PIECE ECONOMY (the consistent family!!):** pool 156 pieces (mean 2.9 lines — THE
  CELLS!! — mean 16.5 users, max 63: THE E8-GRADE SHARING!!!), 121 tail carriers, leftover
  1,128 lines.  THE STRUCTURE: 156 + 121 + 9 = 286 (R/v 2.36).
- **THE PRICE BAND — RETRACTED AT THE HONEST CST=81 (SS1468!!):** the SS1406 band
  (+10.19%/+13.42% at CST=72) WAS AN ARTIFACT OF THE WRONG CST: the gathers' contents (the
  ~65-line basis rows) span dim-9 -> their build frames are FORCED to FULL -> the copy
  ranks 9 -> CST = 81 (not 72!!).  AT THE HONEST CST=81 THE WHOLE BAND IS BELOW: R=286:
  D -14.86%; R=300: C -7.97% (the best!!) / D -11.13%; R=350: D -29.91%; the R420-analog
  R 440-480: -23% to -35% (THE TRANSPLANT ECONOMICS DO NOT CROSS!!); R=520: NO ROOTS.
  THE CROSSING CLAIM IS RETRACTED.  THE MODEL FRAGILITY EXPOSED: 9 mass units (the CST)
  moved the best point by -21 points (the ±0.3%-mass -> ±25-35-point sensitivity!!); the
  BASIS CHOICE (the pivot basis: all 9 gathers dim-9 -> cst 81; a smart basis: 8 dim-8
  rows + 1 dim-9 -> cst ~73, plausible but UNMEASURED) swings the band ±20 points AGAIN:
  THE MODEL BAND IS NOT A VERDICT — only a build's TRUE histogram + TRUE price is.
- **THE REMAINING GATES (the 100%-verification list!!):** (1) the arrival law: the demand-
  reads ~2,800 vs 9R -> the honest R ~310-325 (the utilization ~96%: TIGHT!!); (2) the chain
  slots: the target-side packing (~23 reads per target into the 8 chain slots!!), the
  source-side (~8.5 reads: the pieces ~3.7 + the gathers ~4.8!!), and the gather-builds
  (the U/W factorization: the 9 basis-row gathers at the dim-8 frames — the sources' dim-8
  slot collision: the build's decisive design question!!); (3) THE BUILD -> gcheck -> THE
  TRUE histogram -> THE TRUE price.

## THE 121-LINE'S D4 CENSUS v1 + v2 — THE 3150 ROOMS; THE PARTITION-ROOMS DO NOT COVER (ii19_121d4.py, ii19_121d4b.py; SS1772, SS1778)

- **THE v1 (SS1772!!)**: the 122,850 orthogonal quadruples -> **THE 3150 DISTINCT SPANS, ALL
  12-LINE** (the D4 sub-lattices!!!) — the per-root rooms: 315 each; **THE SPECIAL (120): IN
  NO ROOM** (the hyperbolic extension: orthogonal to all roots, in no roots' span!!); the
  perp-covers: every root-target: the **315 rooms inside perp(t)** (the 63 roots covered!!)
  + **THE REMAINDER: THE SPECIAL (the 1 line!!)**; the packing: the **6 rooms** (the 5 full +
  1 partial (the 3 new lines!)) + the special; the special-target: the 11 rooms, the remainder
  0; **THE WALL: the ~338 dim-4 frames per target** — the one-per-dim wall unless the unions
  (the 976,500 dim-6 (the 21/22-line!!)!!)
- **THE v2 (SS1778!!)**: THE DISJOINT-PARTITION ROOMS (the SS1685's 30 4-frames' spans!!) —
  **THE ROOMS COLLAPSE**: the 30 frames -> the ~10-15 DISTINCT D4 rooms (the rooms 0, 1, 2:
  THE SAME line-set!!!); the per-root room-counts {2: 96, 3: 16, 15: 8}; **THE PER-TARGET
  COVERS COLLAPSED: the partition-rooms DO NOT COVER THE PERPS** (the inside-rooms {2: 96,
  3: 16, 15: 8, 30: 1}; the packing: 1 room for 112 targets with **THE 52-LINE
  REMAINDERS!!!**) — **THE SS1685-PARTITION APPROACH IS DEAD FOR THE COVERS!!**; the
  special's (5)-check: the False = the t=120 self-case artifact (the special IS in every
  root-target's perp ✓✓✓ — the free same-frame re-reads at the special's span (the dim-1!!) ✓)
- **THE DESIGN'S REAL STRUCTURE**: the 3150-room economy: the per-target 6-room packings +
  the rooms' union (the sharing!) + the carriers' duplication needs — **THE R-WINDOW
  QUESTION (the decisive!!)**: the R420's own R/v = 3.5 (the 240 carriers + the 180 sums!!);
  the 121-line's HOSTING WALL: the R <= 484 (= 4v!!); **THE ROOM-UNION'S SIZE DECIDES (THE
  CENSUS v3: ii19_121d4c.py — the union + the sharing + the carriers' needs + the R estimate
  vs the wall!!)**

## THE CENSUS v3 — THE ROOM-UNION VERDICT: THE ROOM-FIRST DESIGN INFEASIBLE AT THE WALL (ii19_121d4c.py; SS1793)

- **THE UNION: 378 distinct rooms** (from 731 slots) — **THE SHARING WEAK: the
  users-per-room {1: 142, 2: 207, 3: 9, 4: 3, 6: 6, 7: 1, 8: 4, 9: 4, 12: 1, 13: 1} — THE
  MEAN 1.9 USERS** — NOT the E8's '70 quads x 6 targets' grade (the mean 6!!): the 142 rooms
  used ONCE + the 207 used TWICE — **THE I13 PAIR-SPECIFIC SIGNATURE, not the E8's
  shared-grade!!**
- **THE CARRIERS: the per-source room-appearances: THE MAX 105; the sum 4,536** — the
  duplication needs catastrophic (the 1-per-room-slot model: the 4,536 carriers!!)
- **THE R ESTIMATES: BOTH OVER THE WALL**: the duplication model: 4,536 + 378 + 130 =
  **5,044 vs THE WALL 484 (10.4x OVER!!)**; the R420-style minimal (2 per source):
  240 + 378 + 130 = **748 vs 484 (1.5x OVER!!)** — **THE ROOM-FIRST DESIGN IS INFEASIBLE
  AT THE HOSTING WALL**
- **THE STRUCTURAL CONCLUSION**: the E8's room economy (the 70 x 6: the demand-frame
  alignment!!) DOES NOT TRANSPLANT: the 121-line's perps need DIFFERENT rooms per target
  (the 6-room packings barely overlap: the mean 1.9!!) — **the same structural finding as
  the SS466-SS473 synthesis ('E8 wins by frame sharing; the I13 demands sit ~1 per frame
  regardless of partition'), now MEASURED at the room level for the 121-line!!**
- **THE 121-LINE PROGRAM'S COMPLETE VERDICT (measured at every layer!!)**: the
  pieces-economy (the SS1685: R 339, the arrival law OK!) FAILS the rooms (the SS1702
  chain walls!); the rooms-economy (the 3150!) FAILS the R (the v3!!) — **NO DESIGN WITH
  BOTH THE R <= 484 AND THE LEGAL ROOMS** — the system closes as a rigorous negative at
  the realizability layer
- **THE ASSETS (banked!!)**: the verification machinery (the R420 control: the ratio
  1.0!!), the R420's complete recipe (the flag, the free singleton-reads, the incremental
  sums, the [2, 7] reads, **THE FREE SAME-FRAME RE-READS**!!), the census (the 3150
  rooms, the special's structure, the 6-room packings) — all committed
- **THE REMAINING PATHS**: (1) THE E8 LEVER A (the frontier system's own open lever: a
  middle strictly more efficient than R420 per incidence — demonstrated on E8 first,
  where it moves the frontier itself!!); (2) the fresh-system search (the priority D: the
  census screen as the reusable methodology!!); (3) the handoff (the complete record
  committed!!)

## THE DIRECTION (SS1799): 'keep pushing lorentzian' — THE 121-LINE CLOSED; THE LEVEL-2 SCREEN NEXT

- **THE USER'S DIRECTIVE (SS1799!!)**: 'keep pushing lorentzian' — the Lorentzian
  program continues (NOT the E8 lever A, NOT the handoff!!)
- **THE MEASURED STATE**: every examined system closed by measurement: the I-family
  (I8-I13: the exact-covers, the census screens, the arithmetic!!); the II19 level-0
  (the decoder rank 241: the width fatal!!); the 2-class (the h=10 degeneracy!!); the
  121-line (the room-union: the R 748-5,044 vs the wall 484!!)
- **THE REMAINING LORENTZIAN OPENING (the biggest headroom!!)**: THE II19 LEVEL-2
  (v=929, the ceiling 4.74x!!): the probe stalled at 80-85 residual (the escalation
  closed at SS946-960!!) BUT THE STALL-TAIL ARCHITECTURE (the level-0's validated
  design: the bulk greedy at c_t ~9.5 + the tail closures!!) WAS NEVER APPLIED to the
  level-2 — the screen: (a) the construction re-read (ii19_l2_probe.py — LOCATED at
  SS1806-SS1807!!), (b) THE DECODER RANK (the B0's GF(2) rank for the 929 lines — the
  level-0's 241 was fatal; the level-2's: UNMEASURED — THE FIRST CHECK!!), (c) the
  c_t/budget arithmetic (the ceiling 4.74x: the R/v allowance!!), (d) the stall-tail
  probe (the tail closures!!)

## THE LEVEL-2's FIRST CHECK — THE DECODER RANK 531: FATAL-ISH PENDING THE PRICE (ii19_l2rank.py; SS1814)

- **THE SYSTEM (the SS1810 construction!!)**: the 929 lines (the norms ALL 2!!): the
  classes {(0,0): 120, (0,1): 120, (1,0): 120, (1,-1): 568, (1,1): 1}; the form x.x' +
  a.d + b.c (the 10-dim: h=10!!) — the construction VERIFIED (the 929 = 360 + 568 + 1!!)
- **THE PERPS**: the sizes 183-400 (the (1,-1) class: the ~183-215!!); **THE SPECIAL'S
  PERP: 688** (⊥ to all (α,0,0) + (λ,1,-1): the a+b=0 rule!!); the demands by class:
  {(0,0): 46,656, (0,1): 31,472, (1,0): 39,600, (1,-1): 119,016, (1,1): 688} — **THE
  TOTAL 237,432 (the ~256 lines/target!!)**
- **THE GF(2) RANK OF B0: 531** (of the 929!!) — vs the level-0's FATAL 241: the rank is
  2.2x the level-0's — **BUT THE WINDOW IS 2.6x (the v/m: the 929/82 = 11.3 vs the
  361/82 = 4.4!!) — the decoder RELATIVE to v: the 531/929 = 0.57 vs the 241/361 = 0.67
  — THE LEVEL-2's DECODER IS RELATIVELY SMALLER!!** — the width >= 531 -> the CST ~531 x
  the copy rank (~9-10) ~ 4,800-5,300 — **THE FATALITY IS NOW A PRICE QUESTION: does the
  2.6x window absorb the 2.2x decoder?!** — the level-0's answer at the same accounting:
  the width 241 -> the best case -57.61% (the NO ROOT at the realistic!!) — the level-2's:
  **THE PRICE CHECK (ii19_l2price.py — the SS1112-style: the decoder band at the level-2's
  window!!) — THE DECISIVE COMPUTATION**

## THE LEVEL-2's PRICE CHECK — THE HOSTING WALL: R <= 3,922 vs THE IDENTITY'S R ~8,640: CLOSED (ii19_l2price.py; SS1826)

- **THE CONTROL PASSES PERFECTLY**: the R420's true hist -> the published c (the ratio
  1.000000 ✓✓✓) — the calibration validated!!
- **THE HOSTING WALL (the pricer's own!!)**: the nres = 9R vs the cap = 38v = 35,302 ->
  **THE LEVEL-2's CEILING: R <= 3,922 (the 4.22v!!)** — EVERY BAND (the R 4,000-20,000,
  the decoder r=1-10, THE BEST CASE (r=1!!)) HITS THE WALL!!
- **THE REGISTER IDENTITY'S NEED**: the R = Σc_t − v ≈ 929 x 10.3 − 929 ≈ 8,640 (the
  probe-measured c_t ~10.3!!) — **OVER TWICE THE WALL (the 2.2x!!)** — even the E8-grade
  c_t = 5.2 would only barely fit (the Σc_t <= 5.22v = 4,851!!); the probe's measured
  covers: the 2x that!! **THE DECODER RANK 531 ON TOP** (vs the level-0's fatal 241!!)
- **THE LEVEL-K ESCALATION CLOSES STRUCTURALLY**: the wall screen Σc_t <= 5.22v — the
  measured ratios: the II19-0: 2,698 vs 1,885 (1.43x over!!); the level-2: 9,570 vs 4,851
  (1.97x over!!) — **the ratio WORSENS with the level** (the per-target demands grow ~190
  -> ~256 while the wall grows linearly!!) — the level-3+ strictly worse!!
- **THE LORENTZIAN STATE after the SS1830-1831 directives ('keep finding breakthroughs
  on lorentzian'!!)**: every measured system closed: the I8-I13, the II19-0 (the decoder
  241), the 2-class (the h=10 degeneracy), the 121-line (the room-union), the level-2
  (the hosting wall) — **THE ONE UNRESOLVED: THE I11's COIN-FLIP (the SS755-767: 'a
  coin-flip, not closed'!!): the budget 1,652 (7.51v!) with the layered middle 817 <=
  992 ✓ (the 17% margin!!) and the read-side gap c_t 8-10 vs <= 7.2 (the 1-3 gap: the
  sampled vocabulary vs the true ~10^5-10^6 population!!)** — THE NEXT SCREEN: the I11's
  hosting-wall check (the refined pricer at the v=220, the h=9!!) + the B0 rank + the
  wall/c verdicts at the R band

## THE I11's SCREEN — THE COIN-FLIP RESOLVES NEGATIVE (i11_wall.py; SS1842) + THE II19's WALL-BAND RE-OPENED (the SS1845 directive!!)

- **THE I11's SCREEN (i11_wall.py; SS1842!!)**: the system (the Geom(11)!!): the V=220, the
  perp sizes {114: 165, 128: 55}; **THE GF(2) RANK OF B0: 210 (of the 220!!)** — the
  near-full rank: THE DECODER FATAL (the precedents: the II19-0: 241; the level-2: 531;
  the E8: 9!!); **THE PRICE BAND (the h=12 (not the 9 of the SS1833 record!!), the
  m=100!!)**: the R <= 800: NO ROOT; the R >= 900: THE HOSTING WALL (the cap = 38v =
  8,360 -> the R <= 928!!) — **THE ENTIRE R RANGE UNPRICEABLE AT THE NAIVE MODELS!!**;
  the c_t arithmetic: the hosting needs the c_t <= 5.22; the crossing the <= 7.22; the
  measured 8-10 — **BUT MOOT: the decoder rank + the unpriceable window close the
  system!!** — **THE I11's COIN-FLIP (the SS755-767!) RESOLVES NEGATIVE BY MEASUREMENT**
- **THE LORENTZIAN DECODER SIGNATURE (the program-level insight!!)**: the Lorentzian
  perp-pattern decoders have NEAR-FULL GF(2) ranks (the I11: 210/220; the II19-0:
  241/361; the level-2: 531/929!!) EXCEPT the E8-embedded (the 121-line: the 9!!) —
  **THE HYPERBOLIC EXTENSION DESTROYS THE GF(2) STRUCTURE THAT KEEPS THE E8's DECODER
  CHEAP**
- **THE USER'S REDIRECT (SS1845!!)**: 'keep going for II19 there is still potential' —
  **THE WALL-BAND RE-OPENING**: the SS1112 decoder scan priced at the R ~4,657 — 3x OVER
  the hosting wall (the R <= 4.22 x 361 = 1,524!!) — **THE WALL-BAND R 600-1,524 (the
  mass/v ~60-67!!) NEVER PRICED FOR THE FULL-II19 AT THE REFINED PRICER!!** — the II19's
  ceiling 2.21x (the highest of any viable system!!); the read-side IF: the c_t <= 5.22
  (the measured 9.5-10.3: the 2x gap!) — **THE SCAN (ii19_wallprice.py): the price at
  the wall-band: 'IF the E8-grade covers exist, the price is X' — X decides the
  vocabulary hunt!!**

## THE II19's WALL-BAND SCAN — THE RE-OPENED QUESTION MEASURED AND CLOSED: NO BAND CROSSES (ii19_wallprice.py; SS1853, SS1857)

- **THE CONSTRUCTION VERIFIED**: the 361 lines (the 3 root-classes + the special ✓); the
  norms {2.0: 361} ✓; **THE GF(2) RANK OF B0: 241 ✓✓✓ — THE SS1112 NUMBER CONFIRMED BY MY
  OWN MACHINERY!!**
- **THE D-VARIANT BUG CAUGHT AND FIXED (the session's honesty pattern!!)**: the SS1853
  run's D masses were 2.19x INFLATED (the MASS fractions put into the hist's COUNT
  slots!); the fix (the counts = the mass/d + the remainder to the 1s!): the SS1857's D
  masses correct (the 10,739 = the naive's ✓)
- **THE WALL-BAND PRICES (the R 400-1,524 x the naive/D x the decoder r=1/10!!)**: **THE
  BEST: the D-variant at the R=400 with the r=1 decoder (the PHYSICALLY UNREALIZABLE
  best case!!): c = 0.001436290 (the -17.66%!!)** — the D is ~9 points better than the
  naive at every R (the SS1317's precedent confirmed!); the naive at the R=400: the
  -26.73%; both declining with the R (the -49.37% at the R=1400!)
- **THE REALISTIC DECODER (r=10)**: NO ROOT AT EVERY BAND (the +2,410 mass pushes over
  the window's no-root boundary!); **THE WALL EDGE (R=1,524): NO ROOT FOR ALL MODELS**
- **THE c_t REALITY CHECK**: the R=400's identity: the c_t = (400 + 361)/361 = 2.1 —
  **PHYSICALLY UNREALIZABLE** (the measured covers: the weight-2 impossible (the SS801:
  0/11 at the weight <= 3!!)); the realistic c_t 9.5-10.3 -> the R ~3,069 — 2x OVER THE
  WALL — unhostable!
- **THE DECISIVE CLOSURE**: even IF the E8-grade covers (the c_t <= 5.22) existed, the
  R = 1,444-1,524 prices land at the -48% to NO-ROOT — **THE FRONTIER QUESTION IS
  CLOSED INDEPENDENT OF THE COVERS!!**
- **THE VERDICT (the SS1845 'there is still potential' question!!)**: **THE WALL-BAND
  WAS THE ONE UNPRICED REGION — AND IT PRICES BELOW AT EVERY CONFIGURATION**: the best
  case -17.66% (the unrealizable!), the realistic NO-ROOT/unhostable — **THE II19
  CLOSED AT THE WALL-BAND: NO BAND CROSSES THE FRONTIER**

## THE R420-EXTENSION BUILD — STAGE 1: THE RE-BASE VERIFIED PERFECTLY (ii19_ext.py; SS1914)

- **THE ONE UNTRIED PATH (the commit 61d634e4!!)**: the R420's published word (the
  gcheck-PASSING design!) re-based to the h=9 (the +1 final climb per register: the nested
  chains 0->...->8->9 LEGAL!) + the special's extension -> the gcheck -> THE TRUE HIST ->
  THE TRUE c!! — THE BUILD ANSWERS THE AUDIT's #8/#14 BOTH (the climb shapes + the true c!!)!
  THE MILESTONE EITHER WAY: the FIRST gcheck-PASSING II19-family word (the real, constructed!)
- **THE LOAD (SS1914!!)**: the R420's word: the keys ['A','B','C','D','R','coords','final',
  'form','format','frames','h','lines','ret','scatter','start','v']; the 672 frames (the
  line-counts {0:1, 1:120, 2:180, 12:70, 30:180, 63:120, 120:1} — THE SS1261 ANATOMY
  CONFIRMED!!); the 120 lines (the sample [2,0,0,0,0,0,0,0] — THE NORM-4 REPRESENTATIVES!!)
- **THE 121-LINE SYSTEM**: the R420's own lines (+0 -> the 9-dim) + THE SPECIAL
  (0,...,0,1): **THE SPECIAL ⊥ ALL 120 ROOTS (0 FAILS!!)** ✓✓; the norms {2: 1, 4: 120} —
  THE CONVENTION FLAG: the R420's representatives are norm-4 (the doubled/halved-form
  convention!) vs the special at norm-2 — HARMLESS for the flow (the gcheck checks the
  ⊥-structure + the frames' spans, NOT the norms!!); the rref with the EXACT Fractions
  (the SS1716 lesson applied PRE-RUN: the float cancellation would have created the false
  pivots!!)
- **THE RE-BASE (the frames' map!!)**: the SAME line-lists for the 551 frames; THE FULL
  (the 120 -> 121: THE +SPECIAL!!) + THE 120 PERPS (the 63 -> 64: THE +SPECIAL — the
  special ∈ perp(t) for every root t!!) ✓✓
- **THE VERIFICATION (the spans over the 121-line form!!)**: **THE RE-BASED DIMS
  {0: 1, 1: 120, 2: 180, 4: 70, 6: 180, 8: 120, 9: 1} — THE EXPECTED EXACTLY!!** (the
  perps: the 63-line's dim-7 -> the 64-line's dim-8 ✓✓; the FULL: the dim-9 ✓; the
  full-frame dim check: 9 ✓; the perps' dims {8: 120} ✓!!)
- **THE STAGE 2 (the next!)**: (a) the format-dump (the 'form' field's convention + the
  'coords' + the 'start'/'final' — the Stage 2's exact semantics!!); (b) THE GATES' RE-BASE
  (the chains' +1 final climb: the h=8 -> 9!!); (c) THE SPECIAL'S EXTENSION (the 121st
  source/target + the junks: the special's = the 120 roots, the roots' = the +special!!);
  (d) THE GCHECK -> THE TRUE HIST -> THE TRUE c!!

## THE STAGE 2a — THE FORMAT-DUMP: THE COMPLETE SEMANTICS (ii19_ext2.py; SS1926)

- **THE FORM: '<x,y>/2'** — THE HALVED CONVENTION (the R420's representatives: the
  norm-4-in-x.y = the norm-2-in-the-halved — THE ROOTS!!) — THE SS1914 NORM FLAG RESOLVED;
  the ⊥-STRUCTURE UNAFFECTED (the halving preserves the orthogonality!) -> THE STAGE-1's
  DIMS STAND!!
- **THE FRAMES' ORDER (the 672!!)**: the empty(0) + THE FULL(1!!) + the 120 singletons
  (2-121!) + the 180 2-frames (122-301) + the 70 12-frames (302-371) + the 180 30-frames
  (372-551) + the 120 63-perps (552-671) ✓✓
- **THE START/FINAL (the len 660 = the 120 sources + the 420 helpers + the 120
  targets!!)**: the starts [2, 3, 4, ...] = the sources' singletons ✓; the finals
  [1, 1, 1, ...] = THE FULL (the frame index 1!!) ✓✓ (THE GCHECK LINE 71!)
- **THE GATES (the [frame, dest, srcs] triples!!)**: the A (2064 = the 1695 helper-builds +
  the 360 source-reads + the 9 gathers — THE SS1736 NUMBERS ✓); the B (837 = the 240
  target-dests + the 597 z-dests!); the C (2661 = the reverse-unbuilds AT THE FULL!); the D
  (120 = the scatter-dirt AT THE EMPTY FRAME (the frame 0!!) — THE SS1269's 'no frame
  constraint at the scatter' ✓!)
- **THE RET/SCATTER**: the ret [603, 568, 597, 583, 569, 604, 616, 596, 598] (the 9!); the
  scatter: the 120 per-target lists ([0, 1], [0, 2], [0, 3], [0, 1, 2, 3], ...) = the
  RET-INDICES ✓
- **THE STAGE 2's RE-BASE MAP (the design!!)**: THE GATES UNCHANGED (the frames' indices
  the same: the re-based lists IN-PLACE!!); the dims' shifts: the perp-frames 7 -> 8 (THE
  TARGETS' LAST CLIMBS +120!!) + the FULL 8 -> 9 (THE SOURCES'/HELPERS' LAST CLIMBS +540!!)
  — THE TRUE HIST = THE R420's + THE ~660 EXTRA MASS + THE SPECIAL'S EXTENSION!!
- **THE SPECIAL'S EXTENSION (the design!!)**: the +2 frames (the {120}-singleton + THE
  SPECIAL'S PERP (the 120 roots: the dim 8!!)); the +2 registers (the source 120 + the
  target 120!); the target's junk-delivery: THE W-ROW (THE SS1292's W-VERIFICATION: THE 121
  TARGETS VERIFIED!!) — the 9 gathers' reads (the E8-economical!) vs the 120 direct reads
  (+111 mass!) — THE W's RECOVERY (the on-disk check!): NEXT!!

## THE W-MACHINERY RECOVERED (ii19_121basis.py read; SS1932) — THE EXTENSION'S DECODER DESIGN

- **THE SS1292 SYSTEM (the 10-dim encoding!!)**: the 120 roots (the 8-dim + [0, 0]!) + the
  special [0]*8 + [1, 1] (THE (0,1,1)!!); the FORM[8,9] = FORM[9,8] = 1 (the x.x' + ab' +
  ba'!); the PERP masks; the B0 = PERP | self ✓
- **THE PARITY MAP PHI (the special-bit!!)**: the kernel (the dim 8): THE EVEN ROWS
  (B[0]^B[k]: THE SPECIALS CANCEL!) — the basis = the 8 even + the 1 odd (B[0]: the
  special-bit = 1!!) ✓; the greedy's RANK-INCREASING-ONLY (the SS1496 fix!!)
- **THE MEASURED CST = 73** (the 8 even rows' spans: the 8 each (THE SUM 64!) + the 1 odd:
  THE SPAN DIM 9 (the special in the support -> the +1 dim!) = 73 ✓✓ THE SS1308 PROVEN
  FLOOR!)
- **THE W-MATRIX (the SS1500 coords-frame fix!!)**: the augmented reduction -> the T-matrix
  -> W_orig = W_red x T — the coords over MY gathers ✓; **THE W-VERIFICATION: B[t] =
  SUM W[t,k].u_k FOR ALL 121 TARGETS: PASS!!**
- **THE EXTENSION'S DECODER DESIGN (the build's plan!!)**: (1) THE 8 EVEN PATTERNS: the
  pure-E8 (the no-special-bit!) -> IN THE R420's u_k-SPAN (the 9-dim E8 B0-space!) -> the
  even-totals = THE XORs OF THE R420's RET-TOTALS (the linearity!!) ✓ — NO new registers!;
  (2) THE 1 ODD PATTERN (B[0]: the 65-line: THE +SPECIAL!): NOT in the R420's span -> **THE
  +1 NEW REGISTER (THE ODD-GATHER: THE R 420 -> 421!!)** — the A-phase build (the reads of
  the R420's rets + the special's source!); (3) THE SCATTER'S W-ROWS: the SS1292's W (the
  121 x 9!) -> the expansion (the even-components -> the R420-ret-combinations; the odd ->
  the new register!); (4) THE ROOTS' +x_special (the junk: the 64-pattern!!): the delivery
  via the special's carrier (the {120}-singleton-frame register: SUBSET-EQ EVERY ROOT's
  64-PERP ✓✓!) + the B-cancel; (5) THE SPECIAL'S TARGET: the junk = the 120 roots: the
  reads at the frames SUBSET-EQ the 120-roots-frame (ALL THE R420-FRAMES SUBSET-EQ THE
  E8-SPAN ✓✓!)
- **THE NEXT**: THE GCHECK's RE-READ (the flow's exact semantics: the D-dirt / the
  B-cancel / the scatter!!) — the build's ground truth!!; THEN THE 2b (the design + the
  val-simulation!) -> THE 2c (THE WORD + THE GCHECK!!)

## THE GCHECK's COMPLETE SEMANTICS — THE BUILD'S FULL SPEC (tword/gcheck.py read; SS1937)

- **THE WORD FORMAT (the gcheck's input!!)**: the form = {'num': the matrix, 'den': the int}
  (THE FRACTION MATRIX!!); the lines = the h-dim vectors; **THE FRAMES = THE RREF BASES (the
  vector lists!), NOT the line-index lists!!** (the R420's line-lists: the DESIGN reference;
  the gcheck's: the bases!!); **'ret_frames' REQUIRED** (the R420 lacks it!!); the gates =
  the [F, dest, srcs] triples
- **THE REGISTER LAYOUT (nreg = 2v + R!!)**: the sources 0..v-1 (the start: the {s}-
  singleton frames! the val: the {s}!); the targets v..2v-1 (the start: THE FRAME 0! the
  val: the {v+t}!); the helpers 2v..2v+R-1 (the start: THE FRAME 0! the val: THE OWN DIRT!)
- **THE FINAL CHECKS**: the sources'/helpers' finals at THE DIM-h FULL; the targets' finals
  at THE DIM-(h-1) t-PERPS (the span PERP the target's line!!)
- **THE CLIMB**: THE SAME-FRAME RE-READS FREE (`if cur[r] == F: return`!!); the nested +
  the strictly-increasing dims; the hist += the delta
- **THE CONTENT-FRAME INVARIANT**: every gate's dest's content SUBSET-EQ the gate's frame;
  the target-dests: the srcs' contents SUBSET-EQ the frame
- **THE PHASES (THE ORDER!!)**: the D (the frame-0, the targets receive the helpers'
  dirt!) -> the A (the builds: NO targets!) -> **THE SCATTER** (the rets at their
  ret_frames! the targets at the frame 0! the targets XOR the scatter[t]-selected rets!
  **THE CST = THE SUM OF copy_ranks (THE RETS' FRAMES' DIMS!!)**) -> the B (the
  target-reads + the z-builds!) -> **THE C (THE H4 LITERAL REVERSE: the reversed (A+B)'s
  z-gates AT THE FULL FRAMES!!)**
- **THE SEMANTICS (the final values!!)**: the source s = THE {s}; the target t = THE
  {v+t} ^ {t} (THE y_t + x_t!!); the helper = THE OWN DIRT (the initial!)
- **THE MASS IDENTITY**: mass = h*R + cst + 2v(h-1) ✓; the price via the --price flag (the
  pricer + the P111 comparison)
- **THE 121-LINE'S CST 73 CONFIRMED AT THE CODE LEVEL!!!**: the 8 even rets at the dim-8
  frames (the copy rank 8 each!) + the 1 odd ret at the dim-9 (the FULL-span!): the copy
  ranks {8: 8, 9: 1} -> 73 ✓✓✓ — THE SS1308's PROVEN FLOOR IS THE GCHECK's OWN ACCOUNTING!!
- **THE EXTENSION'S DESIGN (the concrete!!)**: (1) THE ROOTS' TARGETS: THE R420's
  ARITHMETIC UNCHANGED (the same dirt/scatter/reads -> the x_t!); (2) THE SPECIAL'S TARGET:
  the final = the y_special + x_special: the scatter = THE ODD-GATHER's value (the
  B[0]-total: the 65-pattern incl. the x_special!) + the B-reads = THE ROOT-0's JUNK-CANCEL
  z-registers (the E8-internal frames SUBSET-EQ the special's 120-roots perp ✓✓!) XORing
  to the ({0} UNION the 63)-pattern; (3) THE SPECIAL'S SOURCE: the {120}-singleton start
  -> the FULL climb (the mass 8!); (4) the form: the diag(1^8, 2) (the den 1!); the frames:
  the Stage-1's line-sets -> THE BASES (the rref!)
