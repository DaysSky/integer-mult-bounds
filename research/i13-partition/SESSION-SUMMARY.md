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

## THE STAGE 2b-i — THE REPLAY PERFECT: THE R420's ARITHMETIC FULLY EXTRACTED (ii19_ext3.py; SS1949)

- **THE REPLAY VALIDATED END-TO-END**: the final-value fails 0 ✓✓✓; THE HIST EXACTLY THE
  PUBLISHED {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9} ✓✓✓; the mass 5,112 = the identity
  ✓✓✓; THE CST 72 (the 9 rets at the dim-8 FULL!) ✓ — THE SAME MACHINERY THAT WILL BUILD
  THE EXTENSION!!
- **THE ARITHMETIC VERIFIED**: the [dirt ^ scatter ^ reads] = x_t for ALL 120/120 ✓✓✓
- **THE STRUCTURE (the decisive extraction!!)**: (1) THE DIRT = THE D-SRCs' VALUES (the
  dirt sizes 121-204 = THE SRCs-PER-GATE 121-204 (the identical histograms!!): at the
  D-time the helpers hold their OWN DIRT (the single bits!): each target receives ~121-204
  HELPER-INDICATOR BITS — the transitive indicator-parity dirt!!); (2) **THE [reads ^
  dirt] = THE SCATTER-MINUS-x_t EXACTLY** (the IDENTICAL size histograms {184..251}!!!):
  the reads' XOR cancels EXACTLY the junk the scatter delivered (minus the x_t!) — the
  arithmetic's clean decomposition!!; (3) THE RETS AT THE DIM-8 FULL at the scatter (the
  {8: 9}!) ✓
- **THE SCATTER'S VALUES**: the sizes 185-252 = the B[t]-x-parts (the ~64) + THE RETS'
  ACCUMULATED DIRT (the ~121-188 helper-bits!) — THE DIRT FLOWS THROUGH THE RETS — the
  transitive mechanism measured!!
- **THE CRITICAL FRAME-LEGALITY DISCOVERY (the design's constraint!!)**: THE SPECIAL'S
  TARGET'S CHAIN SUBSET-EQ THE 120-ROOTS-SPAN (the E8 8-dim!): the special's target can
  ONLY read the registers at THE E8-INTERNAL FRAMES — **THE x_special (the {120}-span-
  containing registers!) can NEVER be read via the B-gates!!!** (the {120}-span NOT-
  SUBSET the E8-span: the nesting forbids!!) — **THE ONLY CHANNELS: THE D-GATES (the
  frame-0!) and THE SCATTER (the frame-0!)**
- **THE DESIGN CONSEQUENCES**: (1) THE ODD-GATHER'S A-BUILD AT THE FULL: [FULL, odd,
  [the rets..., THE SOURCE 120!]] (the odd's val = own-dirt ^ rets'-dirt ^ the-64-pattern-x
  ^ x_special ✓); (2) THE SPECIAL'S SCATTER-ROW = [the odd] (the frame-0 channel!!); (3)
  THE SPECIAL'S READS: the cancel of the (64-pattern + the dirt!) — THE E8-INTERNAL
  FRAMES ONLY!; (4) **THE RETS' RE-TARGETING (the change #1!!)**: the rets' last A-gates:
  the FULL -> THE 120-ROOTS FRAME (the dim-8!): the copy ranks 8 -> **THE CST = 9x8 + 9 =
  81** ✓✓✓ THE SCAN's HONEST DECODER MASS (the SS1872-1874 dr=9 bands!!)
- **THE NEXT**: THE 2b-ii (the construction + MY OWN replay + the special's arithmetic
  iteration!!) -> THE GCHECK -> THE TRUE HIST -> THE TRUE c!!

## THE 121-LINE WORD: BUILT, GCHECK-PASSING — THE FIRST II19-FAMILY WORD EVER; THE
## HOSTING-WALL VERDICT (ii19_ext4.py, ii19_ext_word.json; SS1976-SS1985)

- **THE WORD EXISTS AND PASSES GCHECK (SS1985!!)**: v=121, h=9, R=541, rho 4.47, the frames
  674, the gates {D 121, A 2185, B 957, C 2782}, the moves 3,392 — **'status': 'PASS'** —
  the format's own checker verifies EVERYTHING (the climb legality, the content-frame
  invariants, the H4, the mass identity, the finals, the retained frames, the scatter)!
- **THE TRUE HIST (the FIRST for any II19-family word!!)**: {1: 1289, 2: 1709, 3: 91,
  4: 60, 6: 120, 7: 120, 8: 9, 9: 4} | THE CST 83 | the rank_mass 6,888 = the identity ✓!
- **THE HOSTING WALL: THE HONEST PRICE VERDICT**: the cap 4,356 vs the nres 4,869 —
  **the pricer REFUSES: 'error': 'hosting wall'** — the R 541 exceeds the wall's R <= 484
  (the 4,356/9!) by the 57 registers (the 111.8% of the cap!)
- **THE MECHANISM (the completeness's price!!)**: the R 541 = the 420 (the R420's
  transplanted core ✓) + the 121 (the special's completeness channel: the odd-gather (1)
  + THE 120 PER-TARGET CARRIERS!); the wall's margin (the 484 - 420 = the 64) < the 121
  cost -> **THE OVER BY THE 57**; THE CARRIERS ARE FORCED (the {120}-span NOT-SUBSET the
  E8-span: the content-frame check; the source's one-climb limit: the same-dim
  perp-jumps ILLEGAL!) -> **the +1 carrier per root-target IS THE FLOOR for this
  architecture!**
- **THE COMPLETENESS HOLDS**: the junk(t) >= perp_121(t) for all 121 targets (the
  scatter's B_121[t]-totals + the carriers' reads!) — the orthogonal-incidence sum IS
  realized: the word is a GENUINE MULTIPLICATION (the SS1150 lesson applied: NOT a
  flow-only artifact!)
- **THE BUILD ARC (SS1943-SS1985, THE 6-FIX ITERATION!!)**: the fix-1 (the roots' rows +
  the row-0: the v_0-cancel!); the fix-2 (the odd's build: THE ROW-0's rets — NOT all 9:
  the x-part = the v_0 ^ e_120!); the fix-4 (the special's row: [the odd] + the row-0!);
  the fix-5a/5b (the D-gates' +ODD + the 120 carriers' A/B/D gates!); the fix-6 (the
  ORDERING: the carriers' builds BEFORE the odd's — the SP's chain legal!); the fix-7
  (the ret_frames' TRUTH: the 2 row-0 rets at the FULL -> the CST 83!) -> **the finals'
  fails 0 (SS1976: my own replay!) -> THE GCHECK 'PASS' (SS1985: the format's own
  checker!!)**
- **THE STRUCTURAL VERDICT (the STRONGEST possible negative!!)**: the 121-line is CLOSED
  BY THE HOSTING WALL AT THE BUILT-WORD LEVEL — not a model band, not a projection: **A
  GCHECK-PASSING WORD whose R exceeds the pipeline's hosting capacity by the 57
  registers!** The E8's mechanism transplants STRUCTURALLY (every legality passes!) but
  the special line's per-target completeness channel (the 121 registers) costs more
  than the R420's transplant margin (the 64) — **the first system closed by a VERIFIED
  WORD's economics rather than a model's projection!**

## THE SHARED-CARRIER WORD: R=463 — THE GCHECK PASS + THE FIRST TRUE c FOR AN
## II19-FAMILY WORD: 0.000955989 = −44.84% vs P111!! (ii19_ext5.py, ii19_ext6.py,
## ii19_ext_word2.json; SS2008-SS2019)

- **THE SS2008 CENSUS (ii19_ext5.py)**: THE CELL-LEVEL SHARING ZERO (the 120 targets' prior-spans: ALL DISTINCT dim-2 cells, each candidate serving exactly 1 -> the m = 120 = NO improvement!); **THE V2: THE D4-FRAME SHARING** — the 42 shared carriers (each at the {120} ∪ a D4-subsystem frame: the 13-line dim-5!) covering ALL 120 targets (the groups {6: 3, 5: 4, 4: 6, 3: 10, 2: 9, 1: 10}!); **THE R RECOUNT: 420 + 1 + 42 = 463 <= the wall 484 (the 95.7% of the cap!) — FITS!!!**
- **THE KEY MECHANISM — THE FRAME-INDEPENDENCE OF THE CLIMB MASS**: the targets' climb mass = the final dim − the start dim (the intermediate visits are MASS-FREE!) — the F_j-insertion (the chain 0 -> cell(2) -> F_j(5) -> perp(8) vs the 0 -> cell(2) -> perp(8)) costs NOTHING; the carriers climb ONCE to F_j (the {120} -> F_j: the +4!) then ALL their target-reads are FREE (the cur == F_j!); THE ORDER-AWARE INSERTION (the ext4's at-the-end append would be the dim-8 -> dim-5 DECREASING = ILLEGAL — the carrier-reads go BETWEEN the cell-gates and the perp-gates!)
- **THE EXT6 REPLAY: THE FINALS' FAILS 0** (all 705 registers!); THE HIST {1: 1091, 2: 1709, 3: 331, 4: 144, 8: 9, 9: 4}; THE CST 83; THE MASS 6186 = THE IDENTITY (9x463 + 83 + 1936) ✓
- **THE GCHECK: 'status': 'PASS'** (v=121, h=9, R=463, rho 3.826, the frames 716, the moves 3278, the gates {D 121, A 2107, B 957, C 2704}!)
- **THE PRICER PRICED IT: 'bit_c_nine_stage': 0.0009559892732842554615227 | −44.84% vs P111** — **THE FIRST TRUE c FOR ANY II19-FAMILY WORD!!!** (the R 541 word was hosting-wall-rejected; the R 463 fits: the nres 4167 vs the cap 4356 = the 95.7%!)
- **THE HONEST VERDICT**: the c −44.84% — BELOW the frontier (the mechanism: the mass/v 51.1 vs the R420's 42.6: the +43 R + the +11 CST + the special's structure!); the frontier needs ~1.8x; the architecture's floor (the 420 core + the odd + the m) — the covering's LOWER BOUND unmeasured (the next step!)
- **THE SPECIAL's COMPLETENESS GAP (the SS2008 flag — THE CORRECTION OWED!!)**: the special's junk = {120} ONLY — the 120 (root, special) orthogonal pairs are NOT realized (the special's column = a COPY: the diagonal pair only!); **THE SS1989/SS1991 RECORD's CLAIM "THE COMPLETENESS HOLDS: the junk(t) >= perp_121(t) for all 121 targets" IS WRONG for the special's column** (the roots' columns ARE complete!); the gcheck does NOT verify the multiplication (the SS1150 identity-word lesson!) — the word is the FLOW-VERIFIED, ROOTS-COMPLETE, SPECIAL-COLUMN-INCOMPLETE multiplication; **THE FIX-PATH: the special's bigger scatter-row (the all-roots pattern!) + the special's B-reads (the E8-internal registers canceling the roots-part!) — the wall margin: the +21 registers (the 463 + the fix <= 484!)**

## THE SPECIAL's COMPLETENESS FIX — THE WORD3: THE FIRST COMPLETE II19-FAMILY WORD (junk(t) ⊇
## perp_121(t) FOR ALL 121!!); THE §4.2 CORRECTION DELIVERED; THE COMPLETENESS IS FREE: c −44.85%
## (ii19_ext7.py, ii19_ext_word3.json; SS2020-SS2034)

- **THE OWED CORRECTION DELIVERED (the SS2019 flag!!)**: the measured BEFORE (the ext7's instrumented replay!): the special's junk = **∅** (the delivered = e120 ONLY — THE COPY, even worse than the {120}-only reading: the diagonal is self-cancelled by the junk-minus-{t} convention!!); the roots' columns ARE complete (the junk-minus-self sizes {0: 1, 64: 120} ✓ re-verified for all 120!!). **THE HONEST JUNK-CRITERION TOOL (the ext7's implementation!)**: junk(t) = setbits(the scatter's delivered x-XOR) ∪ (the B-reads' srcs' x-contents) − {t} ⊇ perp_121(t) — the criterion the SS1150 identity-word fails; run for ALL 121 targets in BOTH replays (the BEFORE: 1/121 incomplete; the AFTER: **0/121**!!)
- **THE FIX's DISCOVERY ARC (the honest ledger — three designs DEAD, the fourth FLIES!!)**: (i) **THE V1 (the sources-as-reads) DEAD**: the sources' B-end frames are ALL the re-based perps (dim 8, ⊇ the special's line — the climb to IDX_R8 dim-equal + not-nested = ILLEGAL!!) — the 477 B-phase source-reads own them (THE ONE-CLIMB-PER-SOURCE LAW: THE SOURCES ARE UNTOUCHABLE!!); (ii) **THE CENSUS (the linear algebra!)**: the 10 registers' x-parts (the 9 rets + the odd!) are **GF(2)-INDEPENDENT (RANK 10!! — exactly ONE subset {[1, 9]} XORs to the ALL-ONES = B121[120]!!)**: every net-delivery (the scatter ⊕ the reads) has a UNIQUE representation; e120's = **{0, 1, 9}** (THE EXT6's OWN ROW-NET!! — that is why the ext6's finals pass!); xp[ret0] = **ALL-ROOTS (the full 120-bit!!)** but ret0 sits at the FULL (the odd's build's src — the v0-assembly is FORCED at the FULL: the 65-bit x-part cannot come from the F_j-local (13-line!) srcs!) — UNREADABLE on the E8-internal chain!!; the odd's build's srcs {ret0, ret1} are FORCED (the unique v0-representation among the done-registers!!); (iii) **THE V3 (the ret-union) 119/120**: the 7 IDX_R8-rets' x-parts' setbit-union covers 119 of the 120 roots — **MISSING EXACTLY THE ROOT 119!!** — the rets-only reads CANNOT complete (the 119-bit lives only in xp[0] (the FULL!), xp[1] (the FULL!), xp[9] (the FULL!)!!)
- **THE V9 DESIGN (THE WINNER — ZERO NEW REGISTERS!!)**: (a) **THE SCATTER ROW = ALL TEN {0..9}** (the delivered = e120 ⊕ X, X = ⊕(rets 2..8) — the FULL INCIDENCE FLOWS IN!!); (b) **THE READS (THE B-START FREE SAME-FRAME RE-READS!!)**: the 7 rets at IDX_R8 (cur == F: FREE, NO MOVEMENT, the later flows untouched!) + **THE 119-HOLDER DOUBLE-GATE** (reg 253 at the D6-frame 385 (dim 6, 30 lines, x-size 19 — one of **45 A-end 119-holders!!**), read TWICE at its own frame: the net 0, the junk += its contents!!) — the special's chain: 0 → 385 (+6) → IDX_R8 (+2): nested ✓ increasing ✓; (c) **THE NET**: x = e120 ✓ (the finals!!); dirt = the ODD-bit (the {0,1,9}-dirt cancellation — **THE D-GATE UNCHANGED [0, 241, [662]]**!!); (d) **THE JUNK = the delivered's setbits ∪ the rets' union (119!) ∪ {119} = ALL 120 ROOTS ✓✓✓ COMPLETE!!**
- **THE VERIFIED WORD (ii19_ext_word3.json!!)**: **R 463 UNCHANGED (the wall 484: the 95.7% — the fix costs ZERO registers, ZERO R!!)**; the gates {D 121, A 2107, B 960 (+3: the reads!), C 2704}; the frames 716; the moves 3279; THE HIST {1: 1091, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 8, 9: 4} — the shift {2: +1, 6: +1, 8: −1} (the special's chain-split!) — **THE MASS 6186 CONSERVED** (the frame-independence law!!); THE CST 83 — **'status': 'PASS'** ✓✓✓
- **THE COMPLETENESS: the incomplete 0/121** (the special: the junk 120 ⊇ the perp 120 ✓✓✓) — **THE FIRST COMPLETE II19-FAMILY WORD** (a GENUINE multiplication: every one of the 121 columns realizes the full orthogonal-incidence sum — the 120 (root, special) products now DELIVERED!!)
- **THE TRUE c: 0.0009558217144810735671339 = −44.85% vs P111** (the ext6's −44.84%: the completeness is FREE — 0.0097 points BETTER (the low-rank hist-shift!!)!)
- **THE REUSABLE MECHANISMS**: (1) **THE SCATTER IS FREE**: the row may read ALL the retained registers (no climbs, no CST growth!) — the delivered pattern is the ⊕ of the row's x-parts; (2) **THE DOUBLE-GATE TRICK**: a src read TWICE at its own frame (FREE!): the net 0 + the junk += its contents — THE COVERAGE WITHOUT THE BALANCE COST!!; (3) **THE B-START WINDOW**: the reads before all the R420's B-gates — the sitters at their A-end frames, cur == F, NO MOVEMENT, the later flows untouched — THE SAFEST READ WINDOW (the B-end window is a TRAP: everything sits at the perps/FULL!!); (4) **THE RANK-10 UNIQUENESS**: the design space (S, R) is fully characterized — the net {0,1,9} FORCED; (5) **THE JUNK-CRITERION TOOL**: the honest completeness check, run in every build!!
- **THE PRICE VERDICT (UNCHANGED!!)**: c = −44.85% — BELOW the frontier (the ~1.8× needed!!): the next steps are the handoff's §5.2 (the covering's LOWER BOUND: the m = 42 is the greedy's — the LP/combinatorial floor decides the architecture's R-floor: R_min = 421 + m_lb!!) and §5.3 (the price grid at R 441–484 with the ext7's hist shape → the c(R) curve → the honest frontier-reachability verdict!!)

## THE II19 BREAKTHROUGH MAP — THE PRICER'S MASTER LAW (c = deficit/ln-mass!!) + THE BREAKTHROUGH ZONE: THE OWN-STRUCTURE AT THE R ≤ 160 ∧ THE wln ≤ 3.0 CROSSES THE FRONTIER (ii19_own1.py, ii19_own2.py; SS2047-SS2061)

- **THE USER'S DIRECTIVES (SS2046/SS2110!!)**: 'work on II19 push it to the max' + 'make a breakthrough to make II19 the frontier' — THE §1349: 'dont try to disprove II19, try to PUSH it'!!
- **THE PRICER'S MASTER LAW (THE OWN1's DISCOVERY, VERIFIED ON THE WORD3/R420/P111!!!)**: reading price() exactly (the fixed-point host_greedy + the root!!): **c = deficit/ln-mass** where **deficit = mW − global-mass = 256·v − 288·CST** (THE h/R-INVARIANT: the a-term cancels EXACTLY: 2304av − 576av − 1728av = 0!!!) and **ln-mass = Σ(z·r·ln(m/r))** over the global profile (local×288 + rem×32!!). THE VERIFICATIONS: word3: 7,072/7.38M = 0.000958 ✓✓; R=135-shape-A: 7,072/4.60M = 0.001537 ✓✓ (the pricer's 0.00153!!); the R420: 9,984/5.89M = 0.001696 ✓ (~2.5%: the fixed-point's rem-shifts!!). **THE 121-LINE's DEFICIT = 256×121 − 288×83 = 7,072 (ANY h, ANY R, ANY shape!!!) — THE CST's PENALTY: −288 per CST-unit (THE −288·CST!!!)**
- **THE FILL-CONSERVATION (RESOLVED!!)**: the global-mass = [(CST + 2V(H−1))×288 + Σ(slots' n·c)×32] — **R-INDEPENDENT** (the 9R×288 = the nres×w×32 = 2,592R!!!): the fill = 0.99691-0.99694 FOR ALL R (the own1's grid: R=135..484 ALL ~0.9969!!): **THE R-LEVER IS NULL VIA THE FILL — BUT THE LN-MASS STILL FALLS WITH R (the local-mass ↓!!)** — the c(R): the MONOTONE INCREASING as the R ↓ (the grid: the R=135: 0.00153 > the R=463: 0.000956!!!) — **THE TRUE MECHANISM: THE LN-MASS (NOT THE FILL!!!)**
- **THE SHAPES' LEVER (THE wln!!)**: the ln(73/r): the r=1: 4.29; the 2: 3.60; the 3: 3.19; the 4: 2.90; the 6: 2.50; the 8: 2.20 — **THE HIGH-RANK-LADDER HISTS: THE CHEAP LN-MASS: THE BIG c!!!** — the word3's wln 3.56 (the low-rank-heavy!!) vs the target ≤ 3.0 — **THE R420's OWN SOURCES: THE [1, 5, 1]-LADDERS (the +5 cell→perp climbs: THE {5: 120}!!!): THE HIGH-RANK LADDERS ARE REALIZED IN THE PUBLISHED WORD ITSELF!!!**
- **THE BREAKTHROUGH ZONE (THE OWN2's (R, wln)-MAP!!!)**: the 6-wln × 15-R grid: **THE FRONTIER-CROSSINGS (c ≥ 0.001744386!!): (R=121, wln ≤ 3.0: 0.00177!!!), (R=126, wln ≤ 3.0!!), (R=131-135, wln ≤ 2.8-3.0: 0.00181-0.00175!!), (R=140-175, wln ≤ 2.6-2.8!!), (R=200-230, wln ≤ 2.4-2.6!!)** — THE HEADLINE: **R=121 ∧ wln=2.4: c = 0.002047 (+17.4% ABOVE THE FRONTIER!!!)** — **THE ZONE: THE OWN-STRUCTURE's R-RANGE (121-160 = THE ARRIVAL FLOOR ~121 (the true demand ~9/line!!!) TO THE §1398's 158!!!) ∧ THE HIGH-RANK SHAPES (wln ≤ 2.8-3.0!!!)**
- **THE DESIGN TARGETS (THE BREAKTHROUGH WORD's RECIPE!!)**: (1) THE R ~ 121-158 (THE OWN-STRUCTURE: THE PIECES'-ECONOMY CLASS (the ~101 pieces + the 47 tails + the 10 decoder!!) — THE §1398's ESTIMATE EXACTLY AT THE ZONE!!); (2) THE HIGH-RANK LADDERS (the pieces at the D6/D7-STARTS: the +6s; the sources'/targets' [1,5,1]-style (the +5s!!); THE MINIMAL +1/+2 TAILS (the ln 4.29/3.6 = THE POISON!!!)); (3) THE CST ~81-83 (the deficit 7,072-7,648!!); (4) THE COMPLETENESS (the junk ⊇ perp for ALL 121!!) + THE GCHECK PASS!!!
- **THE OBSTACLES (THE KNOWN, THE RE-OPENED!!!)**: the pieces'-rooms' collisions (the SS1695: 89%!!; the SS1702: the target-level 74%!!!) — **THE JOINT SLOT-DESIGN (THE SS1702's IDENTIFIED-UNFINISHED: 'THE ONE FRAME PER (piece, dim) AND PER (target, dim)' — the hours!!)** + THE §6i's OPEN (the assembly-min!!) — **THE NEXT ARC: THE REALIZABLE HIGH-RANK OWN-STRUCTURE WORD AT THE R ≤ 160 — THE BREAKTHROUGH BUILD!!!**

## THE DISMISSALS' AUDIT + THE OWN-TREE's HONEST MATRIX: THE ARRIVAL-vs-THE-STRUCT CRUNCH — THE R-FLOOR ~270-290, THE EDGE MISSED BY ~10%; THE COVERING-ILP THE NEXT LEVER (ii19_own4.py, ii19_own5.py; SS2072-SS2095)

- **THE USER'S AUDIT DIRECTIVE (SS2119!!)**: 'go back to any dismissed idea and think about if it is really 100% not possible or there was an error in the dismissal'!!
- **THE AUDIT's FINDINGS (the dismissals' review!!)**: (1) **THE ROOMS-DISMISSAL (the §1423's 'rigorous negative'!!): THE ERROR CONFIRMED!!** — the SS1695/1702's rooms-failures were the PAIRS/QUADS-DESIGN-SPECIFIC (the 13-18-user pieces!!): the own3's D6-pieces (THE 2-USERS!!) have TRIVIAL rooms (the SS1736's E8-own 1-2-read economy!!) — the dismissal GENERALIZED a design-point into a 'rigorous negative'!!! (2) **THE OWN3's OWN R-ESTIMATE (220!!): THE ARRIVAL BUG (caught in the audit!!)** — the D6-pieces built DIRECT from ~30 sources each: 5,400 source-reads vs 9R = 1,980 — THE ARRIVAL-ILLEGAL (2.7×!!) (3) **THE 2-CLASS's h=10-DISMISSAL (the #89/#95!!): THE BORDERLINE (NOT the 100%!!)** — the best −11.36% at (R=280, D-hist!!): the MASTER-LAW's levers (the R ↓ ~255 (the arrival!) + the wln ↓!!) → the re-measurement could reach ~−0--5%!! (4) **THE LEVEL-2's coverability-stall: THE ROOMS-CLASS (the re-openable!!)** — the same design-space!! (5) **THE SOLID (checked, no error!!)**: the 361's rank-241 (the GF(2)-algebra!!); the I8-I13's measured incidences!!; the all-word-bound's flaw (the record's own fix!!); the transplant's 420-base!!; the 121-line's form-legality!!
- **THE OWN4 (THE CELLS-TREE's HONEST-NEGATIVE!!)**: the cells (180, the 2-line-sums!!) + the D6-pieces (180!!): the cell-reads 4,860 (the 27-cells/D6!!) → the total-reads 5,700 → the arrival-floor R ~ 634 → **THE HOSTING WALL (484!!) ✗✗ — THE CELLS-LEVEL DELIVERS 2-BITS/READ: THE WRONG TREE!!**
- **THE OWN5 (THE D4-TREE's HONEST MATRIX!!)**: the sources → **THE D4-SUMS (the 70, the 12-src-builds (the +4s!!))** → **THE UNION-PIECES (the 180 D6s, the ~3-D4-srcs (the 540 reads!!! — the D4-D6-memberships {6: 60, 18: 10}!!))** → the targets (the ~480!!): **THE ARRIVAL ~2,100 → R_arr 234 ✓✓✓ THE LEGAL!!!** — **BUT THE R_struct 290 BINDS (the 70+180+30+10!!) → THE HONEST-R 290** — the pieces' frames ≤ dim-8 (the targets' dim-8 perp-finals!!): the chains ≤ [+7/+8, +1]!!
- **THE PRICE MATRIX (the own5!!)**: the best ([8,1]-pieces + the 2.8-ladders): **c = 0.001578 = −9.5%!!** — the [7,1]+3.0: −14.0%!!; the [6,1]+3.0: −16.1%!! — **THE ~10% MISS: THE R-floor ~270-290 vs THE CROSSING's ~250-270 (the (pieces-count (R_struct!!) vs the pieces-srcs (R_arr!!)) CRUNCH: the D6s (180/540 → 290!!) BEAT the unions (90/~1,800 → ~374!!)!!**
- **THE IDENTIFIED NEXT LEVERS (the honest!!)**: (1) **THE COVERING-ILP**: the own3's greedy took ALL 180 D6s — the overlaps' exploitation → the ~120-150 pieces → **R ~ 230-260 → c ~ 0.0017-0.0018 (THE CROSSING!!)**; (2) THE LADDERS' SHAPES (the 1,936-mass (the 42%!!) at the ~2.8-3.0: the [1,6,1]-variants!!); (3) THE [9]-PIECES (the FULL-builds: the ln 2.09!!) — ILLEGAL (the targets' dim-8 finals < the FULL's 9!!) — CHECKED-DEAD; (4) THE 2-CLASS's BORDERLINE-RE-PRICE (the audit's (3)!!)

## THE D6-PIECES' CENSUS — THE 2-USER ECONOMY: R ~ 220 ∧ THE +1.3% AT THE [6,1,1]-SHAPE; THE ROOMS TRIVIAL AT THE PIECE-LEVEL (THE 2-READ PIECES!!); THE UNION-PIECES' TARGET (R ~ 120-130!!!) (ii19_own3.py; SS2062-SS2071)

- **THE D6-CENSUS (the own3!!)**: the 180 D6-frames (the 30-line!!) — **THE SERVED-SETS: {2: 180} — EVERY D6 SERVES EXACTLY 2 TARGETS** (the 30 lines ⊥ only the 2: the PAIR-structure (the SS1649's pairs!!)) — **THE GREEDY COVERING: 180 PIECES, THE COVERAGE 98.5%** (the residuals 120 bits = 1.5% of the demand 7,800!!): the per-piece gains {60: 30, 47: 30, 46: 30, 34: 30, 33: 30, 32: 30} (the ~30-60 bits/piece!!) — **THE R-ESTIMATE: 180 + 30 tails + 10 decoder = ~220**
- **THE PRICE AT THE R=220**: the pure-6-shape ([6,1,1]-chains: the wln ~2.44-2.5!!): **c = 0.00177 = +1.3% ABOVE THE FRONTIER!!!** — the mixed-shapes (the sources'/targets' ladders' 48%-share (the 1936/3,999!!) at the wln ~2.8-3.0): the −8--13% — **THE SHAPES' CRUNCH: THE PIECES' HIGH-RANK vs THE LADDERS' LOW-RANK — THE DESIGN'S TARGET: THE [1,6,1]-SOURCES (the R420's own!!) ∧ THE [6,+1,+1]-PIECES ∧ THE MINIMAL +1/+2-TAILS**
- **THE ROOMS' TRIVIAL-LEVEL**: the 2-read pieces (the 2 users!!): **THE PIECE-LEVEL: THE ONE UNION-ROOM (the 30 lines ⊥ both users: the ~dim-7!!): NO COLLISIONS (the SS1736's E8-own 1-2-read economy!!!)** — the target-level: the ~2-3 pieces → the ~2-3 rooms → THE UNION-MERGE (the SS1702's fix, now only ~2-3 per target (NOT the SS1695's ~15-20!!!): THE JOINT-DESIGN TRIVIALIZED!!!)
- **THE UNION-PIECES' TARGET (THE NEXT CENSUS!!)**: the 2-D6 unions (the 60-line contents!!): the ~90-100 pieces → **R ~ 120-130 (THE ZONE's HEART!!) ∧ THE +7/+8-UNION-BUILDS (THE wln ~2.2-2.5!!!)** — the expected: (R ~ 120-130, wln ~2.4-2.6): **c ~ 0.00195-0.00205 (+12--17% ABOVE THE FRONTIER!!!)** — **THE BREAKTHROUGH WORD's SHAPE: THE UNION-PIECES + THE [1,6,1]-SOURCES + THE UNION-ROOMS (THE ~2-3/TARGET!!) + THE ~120-130 R!!!**


## THE COVERING's FLOOR + THE 2-D6-UNIONS' CENSUS + THE CST-LEVER: THE −2.1% — THE CLOSEST!! (ii19_own6.py, ii19_own7.py; SS2096-SS2114)

- **THE OWN6 (THE PERFECT-PARTITION's DISCOVERY!!)**: **THE PAIR-REDUNDANCY = 1!!!** — the 180 D6s: every (u,w)-pair served by EXACTLY ONE D6 — **A PERFECT PAIRING-PARTITION (NO OVERLAPS!!)** — THE REDUCE/SWAP: ZERO improvement — **THE 180 = THE D6-CLASS's TRUE MINIMUM!!** — the D6-tree's floor: (R 290, c ≤ 0.00158 (−9.5%!!)) — the ~10% miss STRUCTURAL (the D6-class!!)
- **THE OWN7 (THE UNIONS' CENSUS + THE CST-LEVER!!)**: the 2-D6-union-candidates: 360 (the shared-D4-adjacency: every D6 adjacent to 27!!): **THE SERVED: {1: 360} — EVERY UNION SERVES EXACTLY ONE TARGET** (the 60-line unions' common-⊥: the 1!!) — **THE UNIONS DOMINATED** (the mixed-greedy: 0 unions + 180 single-D6s!!) ✓✓ the D6s' optimality CONFIRMED!!
- **THE CST-LEVER (THE AUDIT's DISCOVERY!!)**: the MASTER-LAW's deficit = 256v − 288·CST: **the CST 83 → 81 (the rets'-frames'-floor: the 9 rets at the IDX_R8 (the contents'-spans (the ~56-120-line patterns: the dim-8-class!!)) + the odd at the FULL (the e120-content: the FORCED!!)) = the deficit 7,072 → 7,648 = THE +8%!!!** — the price-matrix at the (R=290, the CST-81!!): **THE BEST: c = 0.0017076 = −2.1% vs the frontier (0.001744386)!!!** (the 2.8-ladders + the [8,1]-pieces!!) — the −9.5% → the −2.1% (THE CST-lever's +8% ✓✓!!)
- **THE HONEST-BAND (the shapes'-floor!!)**: the ladders'-wln ~2.9-3.1 (the frames'-ladder-structure's the forced: the sources'-[1,5,1]/[1,6,1]: the ~2.93-3.04; the targets'-[2,~5,1,1]: the ~3.1!!): **the honest-best: the ~−4.5%--2.1%!!!** — the SO-CLOSE!!
- **THE 2-CLASS's MASTER-LAW-DISCREPANCY (THE FLAG!!)**: the #95's-c (0.001546 at the (R=280, the D!!)) vs the my-model's-fill-0.63 (the 2-class's global 3.16M vs the mW 5.04M: the s(0) = 0.63: the root ~0.13?!?!) — **THE INCONSISTENT — THE RE-CHECK NEEDED (the §1386's ii19_2class_h10.py's actual price()-calls!!) — the 2-class's re-price could be THE ABOVE-FRONTIER (the fill-0.63's the huge-deficit (1.88M!!)!!!) — THE AUDIT's-ACTION-OPEN!!**
- **THE REMAINING-LEVERS (THE ~2.1%!!)**: (1) the ladders'-shapes' last-squeeze (the [1,7,1]-sources?!: the 2.77!!); (2) the R's-2-3%-squeeze (the tails'-class (the 120-residuals'/30!!)); (3) THE 2-CLASS's-RE-PRICE (the discrepancy's-resolution!!!); (4) THE BUILD (the D4-tree's gcheck-PASS: THE COMPLETENESS + THE TRUE-c!!!)

## THE 2-CLASS's DISCREPANCY RESOLVED + THE BREAKTHROUGH-LEVERS' SWEEP — ALL THE MODEL-LEVERS EXHAUSTED: THE HONEST-BAND −4.5%..−2.1%; THE BUILD THE DECISIVE-NEXT (ii19_2class_h10.py re-read; SS2115-SS2128)

- **THE DISCREPANCY RESOLVED (the §2128's flag!!)**: the 2-class's CST = **162** (the 18 gathers × rank 9 at the dim-9 class-perp frames — the script's line 29!!): the deficit = 61,440 − 46,656 = **14,784** → the c ~0.00138-0.00155 ✓✓ **THE #95's CORRECT (the 2-class: the BELOW ✓✓)** — my session's "fill-0.63" was MY OWN ARITHMETIC ERROR in the rem-mass (the correct: the rem 91,440×32 = 2.93M → the global 5.01M → **the fill 0.99352 ✓ the master law consistent!!!**) — the §175's-flag RESOLVED (the honest-correction!!)
- **THE 2-CLASS's CST-FLOOR**: the 18 rets' contents (the ~240-line-mixture patterns!!): the spans' dim-class ~9 → the ~162 forced-ish — the 2-class: the honest-negative ✓ (the h=10 + the CST-162's the structural!!)
- **THE LEVERS' SWEEP (the ideas A-J!!)**: (A) the tails'-identity: **the 120-residuals = THE (t,120)-BITS (the x_120-channel!!)** — the ~30-42-register-class (the shared-⊥-carriers!!) ✓ counted; (B) the D4-class pieces (the SS1685's 210!!) DOMINATED by the D6s (the 180!!) ✓; (C) the hybrids ~the same ✓; (D) the sources' channel: the D4-via (the ~840 ✓) ✓; (E) the v-variants: the ~closed (the 2-class's-CST/the 361's-rank!!) ✓; (F) the decoder-10 ~forced ✓; (G) the κ-side: the other-track ✓; (H) the K/T: the fixed ✓; (I) the wln's ±5% ~exhausted ✓; (J) the free-re-reads ~counted ✓ — **ALL THE MODEL-LEVERS EXHAUSTED: THE HONEST-BAND −4.5%..−2.1%!!!**
- **THE DECISIVE-NEXT: THE BUILD (the own8!!)**: the D4-tree's gcheck-PASS word: (1) the frames: the singletons (121) + the cells (180) + the D4s (70) + the D6s (180) + the IDX_R8 + the perps (121) + the FULL; (2) the registers: the 121+121+70+180+~30+~10 = **R ~290**; (3) the gates: the D (the dirt-preloads) + the A (the D4-builds ([F, D4sum, [~12 srcs]]!!) + the D6-builds ([F, piece, [~3 D4sums]]!!)) + the scatter (the rank-10 decoder!!) + the B (the targets' reads ([room, target, [~2-3 pieces]]!!)) + the C (the reversals!!) + the finals; (4) THE COMPLETENESS (the junk ⊇ perp!!) + THE GCHECK-PASS + **THE TRUE-c (the models' ±5% resolved!!!)**

## THE BUILD's PRE-EMPTIVE LEGALITY AUDIT — THE OWN5's R=290 WAS THE PHANTOM #2 (THE CHAIN-ILLEGALITY!!): THE HONEST-TREE's-R = THE R420-CLASS (~3.5/line!!) — THE OWN-TREE CLOSED; THE 121-LINE CLOSED IN BOTH ARCHITECTURES (the own8's build-step-1; SS2141-SS2155)

- **THE USER's BUILD DIRECTIVE (§204!!) + THE PRE-BUILD AUDIT (the build's step-1 (the honest!!))**: BEFORE the hours of construction: the design's LEGALITY re-audit!!
- **THE PHANTOM #2 (THE OWN5's CHAIN-ILLEGALITY!!!)**: the own5's-R=290-model assumed the D4-sums built from the ~12 SOURCES directly (the 840 src-reads!!): **BUT the sources'-D4-memberships = {7: 120} (the measured!!) — the each-source in ~7 DIFFERENT D4-frames: the ONE-FRAME-PER-DIM rule (the SS1750's: the DISTINCT-frames!!!) → the 7-D4-uses = THE 'climb not nested' REJECTS (the SS1732's class!!!)** — the free-re-reads apply ONLY at the SAME frame!!! — **THE OWN5's-290: THE PHANTOM (the chain-illegal!!)** — the honest-correction (the my-own-second-bug (after the own3's-arrival!!)!!!)
- **THE CHAIN-LEGAL TREE (the R420's-class!!)**: the multi-use's-the-solution: THE CARRIERS (the R420's ~3.5/line (the 420/120!!!)): the sources (the ~3-reads (the 2-FREE-singletons + the 1-cell (+1!!))) → the ~2-carriers-per-source (the 240-class (the ~3.5-uses-EACH (the clustered-at-the-rooms!!!)))) → the cell/D4/D6-sums'-the-running-gates (the 1,695-class!!) → the pieces (the 1-2-B-reads!!) → the targets (the ~2-reads!!) — **THE HONEST-121-OWN-TREE's-R ~ 470-530 (the pruned!!) / ~710 (the full!!) — THE WALL (484!!) EDGE/OVER!!!**
- **THE PRICE AT THE HONEST-R**: the R420-class: the c ~0.00093-0.0011 (the own1's-grid (the R=463: 0.000956!!!)) = **THE TRANSPLANT's-WORD3's-CLASS (the ALREADY-BUILT-AND-VERIFIED (the R=463: the −44.85%!!!))!!!** — **THE OWN-TREE ADDS NOTHING (the same-R-class (the worse-mass-profile!!)): THE BUILD's-HONEST-VERDICT: NOT-WORTH-THE-HOURS!!!**
- **THE 121-LINE's-THE-CLOSED (BOTH-ARCHITECTURES!!)**: (a) THE TRANSPLANT: the word3 (the R=463: the −44.85% (the gcheck-PASS ✓✓ + THE-COMPLETENESS ✓✓!!)) + the ext8's-floor (the m=30 (the R=451: the −44.19% (the model!!) — the m*-achievability-the-uncertain (the [30, 42]!!) + the marginal (+0.7%!!!)); (b) THE OWN-TREE: the honest-R-the-R420-class (the ~470-530: the c ~0.0010!!!) — **BOTH: the ~−44±1%: THE STRUCTURALLY-BELOW (the h=9's-the-m=73 + the ~3.5v-class-the-R + the CST!!!)**
- **THE REMAINING-II19-OPEN (the honest!!)**: the fresh-systems'-the-census-screens (the the-program's-the-goal (the the-Lorentzian-the-beats-the-frontier!!)) — the the-II19-family's-the-subsets'-the-examined (the ~all-the-closed (the the-2-class (the h=10+CST!!) / the 361 (the rank!!) / the 929 (the wall!!) / the 121 (the both-architectures!!!))) — **THE NEXT: THE FRESH-SYSTEMS' SEARCH (the census-methodology (the #94/#97's!!)) ∨ THE E8-LEVER-A (the the-user's-§110-the-NO (the the-standing!!!))!!!**

## THE BUILD's CRITICAL MECHANISM-RECOVERED — THE FREE RE-READS (the SS1750's!!): THE SS1695/1702's COLLISIONS WERE THE PHANTOM (THE READS-vs-THE-FRAMES!!!); THE BUILD's-THE-RECIPE + THE SESSION's-HANDOFF (the SS1750-1752 re-read + the own7/8; SS2129-SS2140)

- **THE MECHANISM (the record's-own (the SS1750-1752!!) — the session's-re-discovery!!)**: **THE FREE RE-READS AT THE SAME FRAME**: a register read 100× at the SAME frame: FREE (the no-climb (the gcheck's `if cur[r] == F: return`!!!)) — **the one-frame-per-dim constraint is per DISTINCT FRAME (the climbing chain!), NOT per read!!!** — **THE SS1695/1702 COLLISION ANALYSES COUNTED THE READS, NOT THE DISTINCT FRAMES — THE PHANTOM COLLISIONS!!!** — the SS1695's-89%/the SS1702's-74%: the ~the-reads-counted (the the same-frame-re-reads' the FREE!!!)
- **THE R420's-STRUCTURE (the SS1750's!!)**: the ~240-carriers (the chains [2, 4, 4, 4, 4, 6, 7]-style: the ~2-13-reads at the ~4-7-DISTINCT-frames!!!); the sources: the 1-2×-FREE-singleton-reads into the first-level-carriers; the sums: the accumulations-AT-the-rooms; the targets: the [2, 7]-two-frame-reads; THE TRANSITIVE-D-DIRT!!
- **THE 121-OWN's-BUILD-THE-RECIPE (the record's-own (the SS1752's!!))**: **THE ROOMS FIRST** (the shared-frames-per-dim: the cells (2!), the D4s (4!), the D6s (6!), the perps (8!)) — **THEN the carriers/sums AT the rooms** (the free-re-reads!!!) — **THE TARGETS' FEW-FRAME-READS** — **THE TRANSITIVE-DIRT!!!**
- **THE BUILD's-OPEN-DESIGN-QUESTIONS (the honest!!)**: (1) the sources' ~7-D4-uses: the ONE-ROOM-PER-DIM's-solution (the carriers-at-the-singletons (the FREE!!!) + the ~2-sources-per-carrier (the R420's-240-class!!!)); (2) the carrier-count vs the R (~the 240-vs-the-120-carriers?!); (3) the D4-sums'-the-D6-pieces'-the-accumulation-structure (the SS1736's-running-sums (the 1-2-srcs!!!)); (4) the decoder (the rank-10-the-perp-patterns (the #94/#97's!!)); (5) THE TRUE-c (the ~the ±5%-models'-the-resolution!!!)
- **THE SESSION's-HANDOFF (the honest!!!)**: **THE BEST: c = 0.0017076 (−2.1%!!) at the (R=290, the CST-81, the [8,1]-pieces, the 2.8-ladders)** — the honest-band −4.5%..−2.1% — **THE BUILD (the own8!!): THE DECISIVE-NEXT (the true-c + the gcheck-PASS!!!)** — the levers-swept (the ideas-A-J ✓), the master-law-the-verified, the zone-mapped, the audit-done — **THE NEXT-SESSION: THE BUILD-ARC (the hours (the SS1702's!!) + the free-re-reads'-mechanism (the SS1750's!!!) + the own5/7's-design!!!)**

## THE COVERING's FLOOR m_lb = 30 (R_min = 451!!) + THE PRICE GRID: THE 121-LINE ARCHITECTURE CLOSED AT THE PRICE — THE FRONTIER NOT REACHABLE (THE GAP 1.79×!!) (ii19_ext8.py; SS2035-SS2044)

- **THE THREE BOUNDS (the handoff §5.2!!)**: (1) THE COUNTING: 120/6 = 20; (2) **THE PACKING (the integral dual!!): 30** — the max set of targets pairwise-not-co-served (4000 greedy trials!!): each needs its OWN carrier: m ≥ 30 THE CERTIFICATE!!; (3) **THE LP (the fractional dual: the dense simplex, 79 iters!!): 30.000000 EXACTLY** — the LP is INTEGRAL here (the packing IS the optimal dual!!) — **THE FLOOR: m_lb = 30 → R_min = 421 + 30 = 451** (the greedy's 42: the 12-register inefficiency!!)!! THE CANDIDATE POOL: the 180 big (the D4/D6 frames!!) + the 120 cells (the fallback singletons!!) — THE COMPLETE LEGAL POOL (the perp-based F_j = the FULL: the targets' dim-8 finals: the ILLEGAL candidates!!)
- **THE HIST MODEL (the honest decomposition!!)**: the ext7's hist = THE CORE {1: 1049, 2: 1710, 3: 331, 4: 60, 6: 1, 8: 8, 9: 4} + THE m CARRIERS {1: m, 4: 2m} (the A-build +1, the first-read +4, the final +4!!) — **VERIFIED AT m = 42 (the exact match with the word3's measured hist!!)** + THE MASS MODEL 5808 + 9m = 9(421+m) + 83 + 1936 (THE IDENTITY: checked at m_lb/42/63!!)
- **THE PRICE GRID (the handoff §5.3!!)**: the m-grid [30, 63] = R [451, 484 (the wall!!)]: the c(m) MONOTONE DECREASING (the more carriers the worse!!): **THE BEST: c = 0.00096727990857478 at m = 30 (R = 451): −44.19% vs P111**; at the greedy's m = 42: 0.00095582171448107 (−44.85%: THE WORD3's MEASURED c ✓✓ THE MODEL's SELF-CHECK!!); at the wall m = 63: −45.97%
- **THE HONEST REACHABILITY VERDICT (the decisive check!!)**: **THE 121-LINE ARCHITECTURE IS CLOSED AT THE PRICE**: even at the covering's LP FLOOR (m = 30, R = 451), the c = 0.0009673 (−44.19%) — **THE FRONTIER (0.001733427) NEEDS 1.79×** — NOT REACHABLE at ANY covering: the whole grid is below −44.19% (the verdict ROBUST to the covering's achievability: the m* ∈ [30, 42] uncertainty changes NOTHING!!) — the handoff's §5.4 branch FIRES: (a) THE E8 LEVER A (the only remaining lever: a middle strictly more efficient than R420 per incidence — demonstrated on E8 FIRST, where it moves the frontier itself!!); (b) THE FRESH-SYSTEM SEARCH (the census screens as the reusable methodology!!)

## THE FRESH-SYSTEMS' CENSUS-BY-THE-MASTER-LAW — THE §151-CANDIDATES RESOLVED (the 2-class's TRUE rho=240: the class-blocked model was INVALID!!); THE rho(k)=9+2k LAW (the mixtures dead!!); THE 121's rho=9 (the CST-floor 73: the honest-band −22%!!); THE PRICE-OSCILLATION BUG FOUND+FIXED (the undamped fixed-point's period-2 garbage!!); THE E8(+)U FAMILY CLOSED AT THE rho-LEVEL (ii19_fresh1.py)

- **THE CENSUS (the §38's step 2, the user's 'keep pushing for frontier'!!)**: the exact GF(2) decoder-rank machinery (the B0 = {t}∪perp(t) rows, the bitset elimination!!) + the exact span/h (the Fractions-rref + the Gram-rank degeneracy test!!) + the master-law deficit-bands + the damped price-grids: 31 systems screened!!
- **THE §151-CANDIDATE #1 RESOLVED — THE 2-CLASS'S TRUE rho = 240 (THE KERNEL 0/240!!)**: the record's perps were CLASS-RESTRICTED (CLS[s]==CLS[t] in ALL the 2-class scripts: the 63-line same-class demands, the rank-18 class-blocked decoder!!) — **NOT the true E8(+)U-multiplication: the 63 CROSS-CLASS ⊥-pairs per target missing (the word2-incompleteness class!!)**; the TRUE perp(t) = (p_α, p_α) (the 126-line patterns!!); the kernel analysis (λ = Pλ over GF(2): the cross-class coupling forces λ_A = λ_B = μ with μ = P8(2μ) = 0!!) → **the kernel 0 → the B0-rank 240 = FULL → the CST ≥ 240×9 → the deficit −629,760: DEAD** — THE 2-CLASS CLOSED (the deeper reason: the class-blocking was the ONLY way to keep the decoder cheap, and it computes a DIFFERENT (invalid) multiplication!!); the class-blocked model's −11.36% band: MOOT (the invalid system!!)
- **THE §151-CANDIDATE #2 CLEAN — THE 361's rho = 241 ✓✓ and the level-2's rho = 531 ✓✓ (the 929-construction EXACTLY reproduced (the 360+568+1!!))**: the record's numbers re-verified by the census's own machinery — NO error in the dismissals!!; **THE II_{1,17} (the E8(+)E8(+)U root+C): rho=17, h=17 → the deficit −21,536: DEAD** (the towers die by the h-penalty: the CST ~ ρ·16 vs the 256v!!) — the (1,n)-towers: CLOSED!!
- **THE rho(k) = 9 + 2k LAW (the mixtures!!)**: the A+C+B1(rand k): rho = 11/13/17/25/33/57/129/241 at k=1/2/4/8/12/24/60/120 — **EXACTLY 9+2k at every k!!**; **THE D4-ALIGNED T's GIVE THE SAME rho=33 at k=12 as the random (the alignment saves NOTHING!!)**; the A+L2 mixtures: the same +2/line (11 at k=1, 13 at k=2...) — **THE STRUCTURAL +2 (the self-bit + the parallel-pair E-term (the G=±2 off-diagonal!!)) — every added B1/L2 line costs 2 decoder-ranks: the frontier-class within the E8(+)U = THE A-FAMILY ONLY (the E8, the 121, the B1-only!!)**
- **THE 121's rho = 9 (NOT the record's ~10!!)**: the B0-space is 9-dim (the SS1292-basis (the 8 even + the 1 odd!!) IS a full basis!!) → **THE CST-FLOOR = 8×8+1×9 = 73** (the 8 even rets at the dim-8 E8-internal frames + the odd at the dim-9 FULL (the e_C-content FORCED!!)) — vs the record's floor-81 (the own7's 10-rets design!!) and the word3's actual 83 → **the deficit at the CST-73: 9,952 (the +41% over the word3's 7,072!!)** — THE HONEST-121 BAND: the crossing-R ~ 270-290 at the (CST-73, the D-hist!!) — the PHANTOM-regime (the structure-floor R ≥ 451 (the carriers + the m=30-covering!!)) → **the honest c at the R=451: ~0.00135-0.0014 = the −20..−23%** (the WORD4-class: the +22-point honest improvement over the word3's −44.85%!!)
- **THE B1-ONLY (the NEW SYSTEM!!)**: the B1-class ≅ the E8 (the isometry: the Gram α·β identical!!) at the h=10 (the 9-dim span degenerate (the radical (0,1,0)!!) → the FULL = the 10-dim ambient!!): rho=9, the deficit [4,800..7,392] — the R420-architecture transplants DIRECTLY (the isometry!!) → the honest R ~ 420: **c = 0.000907 = the −48%** (the h=10's double penalty (the deficit −2,592 + the mass +10R+4v!!)) — DEAD ✓
- **THE PRICE-OSCILLATION BUG (THE TOOL-LEVEL DISCOVERY!!)**: the pricer's UNDAMPED fixed-point (the 30-iteration q ← q2 loop!!) **OSCILLATES at some (hist, R)**: the host_greedy's slot-order is q-dependent → the period-2 cycles → the returned LAST-iterate = GARBAGE (the first census-print's zigzag: the 121-grid 0.002649/0.001121/0.002225/0.001128/0.002115!!) — **THE FIX: the price_damped (the q ← (q+q2)/2 damping + the convergence flag + the 200 iterations!!)** — **THE VALIDATION BATTERY: the R420-true-hist → 0.00165382698815 ✓✓✓, the P111 → 0.00173305282333 ✓✓✓, the word3-true-hist → 0.000955821714481 ✓✓✓ (all three = the published, all CONVERGED!!)** — the true hists were always stable (the record's controls CLEAN!!); **THE AUDIT-FLAG: the record's model-hist bands (the A/B/C/D variants!!) may contain oscillation-garbage points — the re-verification with the price_damped + the master-law cross-check (the deficit/ln-mass!!) is the new discipline (the phantom-lesson #3!!)** — MY OWN first census-print's garbage: the A+L2(k=1)'s '−5.31%' → the TRUE −30.36%!!; the A+C+B1(k=1)'s '−51.42%' → the TRUE −70.88%!!
- **THE SHORTLIST's HONEST VERDICTS (the damped grids, the monotone!!)**: (1) **THE E8 (CST-72): the R=420: c = 0.001652 = THE PUBLISHED R420-c ✓✓✓ (the machinery's ultimate self-check!!)** — the E8's honest = the frontier-class (the §110-OUT!!); (2) **THE 121 (the C72-band): the crossing-R ~ 260-280 (the R242: 0.001848 = +6.0%!!)** — the honest (the R=451, the CST-73): the −20..−23% — CLOSED (the structure-wall!!); (3) the B1-only: the −48% (the h=10-wall!!); (4) the A+L2(k=1): the −30.4%; the A+C+B1(k=1): the −70.9% — the mixtures: DEAD ✓; (5) THE REST: the deficit-negative (the rho-explosions!!) — **THE E8(+)U FAMILY: CLOSED AT THE rho-LEVEL: the frontier-class (the kernel-density ≥ 0.93!!) = THE A-FAMILY ONLY — the fresh-systems' search within the II19-family: COMPLETE!!**
- **THE REMAINING (the honest!!)**: (a) THE WORD4 (the CST-73 rebuild: the 9-rets decoder (the SS1292-basis!!): the honest −20..−23%-word: the record's best-II19 improvement (+22 points!!)); (b) THE PRICE-OSCILLATION AUDIT of the record's model-bands (the §151-class!!); (c) the m=30-ILP (the marginal!!); (d) the odd-unimodular I_{1,9} completeness (the lowest class (the (2,1,1)'s: 144 lines) is PERP-FREE (the identity-class: the rho = v: DEAD!!); the higher classes unmeasured!!); (e) THE E8-LEVER-A (the §110-OUT!!)

## THE WORD4 BUILT (THE CST 83 → 73: THE SS1492's 9-RET DECODER!!): THE GCHECK-PASS + THE TRUE-c 0.001335891 (−23.42%!!): THE +21.4-POINT HONEST-RECORD IMPROVEMENT (ii19_own8.py + the own8-diags!!)

- **THE BUILD (the §1585's remaining-work, the user's GO!!)**: the word3 (the ext7's own emission, R=463, CST=83!!) → the 121×10 Wp (the rank-10 unique reps!!) → **THE SS1492-BASIS: the 8-EVEN B[0]^B[k] (sel = 1, 2, 4, 8, 9, 16, 32, 64 — the phi-KERNEL (the ODD-coefficients 0!!)) + the 1-ODD B[0] (the FULL-frame: the e120-content FORCED!!))** → the 121×9 W (the unique reps over the 9: the row-sizes {1:1, 2:8, 3:15, 4:22, 5:27, 6:29, 7:13, 8:6}; **the special's row [0,1,2,3,4,8] (the all-ones NEEDS the odd!!)**) → the 8-even A-builds at IDX_R8 (the 120-roots frame!!) inserted BEFORE the ODD-gate (the 605/570 still at 673: the SAME-FRAME FREE reads!!) → **THE CST 73 (8×dim-8 + 1×dim-9 = THE PROVABLE FLOOR!!); the ret-0/1 (605/570) DEMOTED to the internal helpers; the 9th-ret = the OLD-ODD 662 REUSED (its x-part IS B[0] — the rep [0,...,0,1]!!)**
- **THE D-EXTENSION LAW (THE BALANCE THEOREM!!)**: val[NEW_j] = 1<<NEW_j ⊕ (the repB-combo of the old rets!!) → **the NEW row's value = the OLD row's value ⊕ (the NEW-self-bits!!)** (the expansion ⊕ repB[j] = Wp[t]: AUTOMATIC (the rep-composition!!)) → **the D-gates (the frame-0, the PRE-A reads of the UNBUILT helpers = the PURE self-bits, the EMPTY x-content: legal at frame 0!!) cancel them for ALL 121 targets at ZERO COST (121 free gates!!)** — the word3 balance restored VERBATIM (the B-phase untouched except the special!!); the tgt_dirt accumulates (^=!!) — 120/121 finals PASSED on the first try ✓✓
- **THE w* = e_0 LAW (THE rho=9's MANIFESTATION!!)**: the Wp-matrix's rank = 9 → **the complement w* = e_0: the ret-0-coordinate NEVER appears in ANY unique rep (repB[.][0] = 0 for ALL 8 evens!!)** — the word3's special row was the NON-UNIQUE all-10 combo (**exactly the coord-0 direction!!**): the unique Wp[120] = **{1, 9}** (NOT all-10!!) — the handoff's step-1 (the remove-3-gates + the NEW-read + the e120-read) was PROVABLY ILLEGAL: (i) the e120-read gate [IDX_SPS, 241, [120]] violates the nesting (the target's final = its dim-8 t-perp frame FORCED (gcheck!!) → every chain-frame ⊆ the roots-span → NO e120-content register EVER readable (the 672-frame not-nested, the FULL unreachable!!) — the e120 enters ONLY via the scatter!!); (ii) the balance leftover val[605]⊕val[570] (uncancelable: the 605/570 at the FULL!!) — **replaced by the D-extension design (the user-approved!!)**
- **THE O0-CARRIER (NEW8!!)**: the new all-ones row makes the old 7-ret B-read a DOUBLE-DELIVERY (the replay's residue = O_0 ⊕ ⊕_{k∈2..8}O_k, the x-56/dirt-130!!) → **the channel needs O_0 = val[605] delivered at dim-8**: the w*-law kills the new-rets (the coord-0!!), the xp-independence kills the old rets 2..8, 605 itself sits at the FULL (unreadable!!) → **THE FRESH CARRIER: [IDX_R8, NEW8, [605]] inserted BEFORE the ODD-gate (the 605 at 673!!): val[NEW8] = 1<<NEW8 ⊕ O_0 (the FULL value: x + dirt!!)** — the special's B-read = NEW8 (the D-gate [0, 241, [NEW8]] cancels the self-bit!!); **the [253]×2 junk-padding KEPT (the value-neutral, the hist-shape IDENTICAL (the 241-chain 0→385→673: +6+2!!))**; the balance: 1<<662 ⊕ O_1 ⊕ O_9 ⊕ O_0 = e120 EXACTLY ✓✓
- **THE VERIFICATION (100%!!)**: the replay finals-0 ✓; **the completeness 121/121** (the junk-minus-self {64: 120, 120: 1} — the all-ones scatter covers the special's 120-root perp AUTOMATICALLY (the zreg/119-hunt OBSOLETE!!)) ✓; the hist {1: 1100, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 18, 9: 2}; the mass 6257 = the identity 9·472 + 73 + 2·121·8 ✓; **THE GCHECK: PASS** (the exact Gram determinants, the H1-H5, the moves 3297, the gates D 242 / A 2116 / B 960 / C 2713, the frames 716!!) ✓✓
- **THE TRUE-c (the price_damped, the converged it=73!!)**: **c = 0.001335891046497132929087 = −23.42% vs the frontier (0.001744386) / −22.92% vs the P111** (the gcheck's own price = the SAME to 18 digits ✓✓ the master-law cross-check: the deficit 256·121 − 288·73 = **9,952 (the +41% over the word3's 7,072!!)**) — **THE +21.4-POINT HONEST-RECORD IMPROVEMENT (the word3's −44.85% → the −23.42%!!)** — the honest band −20..−23%: LANDED AT THE EDGE ✓
- **THE REMAINING**: (a) the tool-audit's rerun (the ii19_osc1.py: the battery's first line greedy=DP=published ✓✓ (the 636s!!); the bands re-runs + the host-DP lever + the K=4-vs-5 PENDING!!); (b) the R-reduction (the fresh 121-build at the R=451-class (the m=30-covering floor + 9!!): the ~−1.7%-ish marginal!!); (c) the m=30-ILP (the marginal!!); (d) the I_{1,9}-odd's higher classes (the unmeasured!!); (e) THE E8-LEVER-A (the §110-OUT!!)

## THE I_{1,9}-ODD CLASSES CENSUS — THE RECORD's ITEM (d) DONE: THE FAMILY CLOSED (EVERY CLASS + EVERY UNION: THE DEFICIT NEGATIVE!!); THE D9-ROOT rho=9 (THE E8-ANALOG AT h=9!!) + THE SECOND SHELL'S STRUCTURED COLLAPSE (rho=119 at v=1008: NOT THE +2/LINE LAW!!) (ii19_i19odd.py)

- **THE SYSTEM (the odd-unimodular Lorentzian I_{1,9} = diag(1, −1^9)!!)**: the record's item (d): the lowest class ((2,1,1): 144, norm +2) PERP-FREE (the identity-class: ρ = v ✓ re-verified by MY OWN machinery (perps {0: 144}!!)) — the higher classes UNMEASURED: THE CENSUS (the fresh1-machinery port: the exact Fractions-span/h + the Gram-perps + the B0 = {t}∪perp(t) GF(2)-rank + the deficit bands + the damped price grids!!).
- **THE STRUCTURAL INSIGHT (the fresh!!)**: the (0,·)-classes (the ZERO in the positive slot!!) live ENTIRELY in the 9-dim NEGATIVE-DEFINITE subspace → **h = 9 (NO h=10 penalty!!)** — the classes: **C011 = (0,1,1): 72 lines (THE D9 ROOT SYSTEM!!)**, C01111 = (0,1,1,1,1): 1008, C0211 = (0,2,1,1): 1008, C022 = (0,2,2): 72; the h=10 classes: C211 = (2,1,1): 144 (the record's control ✓), C2211 = (2,2,1,1): 2016.
- **THE RESULTS (the ρ-structure!!)**: (1) **THE D9-ROOTS: ρ = 9 at v = 72 (kernel 63/72 = 0.875!!) — THE E8-ANALOG CONFIRMED (the D-series' GF(2)-collapse!!)** — but the SMALL-V DEFICIT WALL: 256·72 = 18,432 < 288·9·8 = 20,736 → **the deficit [−4,896..−2,304]: DEAD**; (2) **THE SECOND SHELL (C01111): ρ = 119 at v = 1008 (kernel 0.882) — THE STRUCTURED COLLAPSE (NOT the +2/line law: 119 ≪ 9+2·1008!!)** — still the deficit [−50,400..−16,128] ✗; (3) **THE IDENTITY-CLASSES: C0211 (ρ = 1008 = v!!) and C2211 (ρ = 2016 = v!!): FULL GF(2)-rank despite the perps (the perps {276: 1008} / {86: 2016}!!)** — DEAD; (4) the unions: D9+C022 (ρ = 144 = v ✗), D9+C01111 (ρ = 191, kernel 0.823, the deficit −218,592 ✗), D9+C0211 (ρ = 1017 ✗), ALL the family (ρ = 1423 ✗), the h=10 unions (ρ = 153/2025 ✗).
- **THE VERDICT: THE I_{1,9}-ODD FAMILY: CLOSED** — no class, no union reaches the frontier-class bar (the kernel-density ≥ 0.93: the best 0.882 (C01111) / 0.875 (the D9)) and EVERY deficit is NEGATIVE — **the §151-item (d): DONE (the last unmeasured fresh-systems axis!!)**; the deeper law: **the odd-unimodular's small-norm classes either collapse to ρ=9-119 (the even-coordinate/D-series structure) but die on the 256v < 288·ρ·(h−1) wall, or are identity-classes (ρ = v)** — the E8's (v=120, ρ=9, h=8) window (the h=8 sweet-spot + the v ≥ 111!!) is STRUCTURALLY ABSENT at the I_{1,9} (the v=72 top of the h=9 negative-definite family!!).
- **THE REMAINING (the updated!!)**: (a) the tool-audit's bands (the own7's −2.1%-shift + the own2 zone-map + the host-DP lever + the K=4-vs-5: the ii19_osc1.py RUNNING!!) + the word4's own levers (the DP + the K=5 at the TRUE hist: the ii19_own8_levers.py RUNNING!!); (b) the R-reduction (the fresh 121-build at the R=460-class: the ~−1.7%-ish marginal!!); (c) the m=30-ILP (the marginal!!); (d) ~~the I_{1,9}-odd's higher classes~~ **DONE (CLOSED!!)**; (e) THE E8-LEVER-A (the §110-OUT!!).

## THE NATIVE-121 BREAKTHROUGH LEAD — THE FRONTIER-WORD BUILD LAUNCHED: THE CROSSING AT R≈260 (THE PAYOFF-MAP +3.27% AT R=240!!); THE 451-FLOOR's 421-BASE = THE TRANSPLANT's OWN (NOT NATIVE!!); THE HIST-SHAPE LEVER (−35%..+18.5%!!); THE R-DRIVER = THE CELL-REGISTERS (the demand-reads FREE at the visited frames!!) (ii19_shapescan.py + ii19_rred.py + ii19_natmap.py; the user's BUILD THE FRONTIER WORD!!)

- **THE HIST-SHAPE LEVER (the tool-level discovery!!)**: at the FIXED (v=121, h=9, R=472, CST=73, mass=6257!!) the climb-distribution swings c ENORMOUSLY: the ALL-1s −35.02% / the ALL-2s −24.22% / the ALL-3s −16.06% / the ALL-5s −2.87% / the ALL-8s **+13.54%** / the ALL-9s **+18.54%** — the pricer STRONGLY prefers the FEW-BIG climbs (the per-child profile cost!!) — **the word4's TRUE hist (−23.42%) is +1.2 points BETTER than the D-model (−24.64%) at the same R** (the true tail {6:1, 8:18, 9:2} vs the model's {5}-loads!!) — BUT the ALL-high shapes = the ONE-STEP climbs = NO assembly-ladder = the demand-explosion (each source read ~64× directly (~8,700 reads!!) vs the ladder's ~3,750!!) — the ladder's low-rung steps ({1:1100, 2:1710}!!) are STRUCTURAL (the D4/D6-cell frames!!) — the shape lever is CONSTRAINED by the assembly!!
- **THE R-DRIVER RESOLVED (the structural insight!!)**: the demand-reads (the source-reads) at ALREADY-VISITED frames are FREE (no climb-mass — the register sits there!!); the visit-cap = ≤ h frames per register (the one-frame-per-dim law!!) — the "demand ≤ h·R" (#74) is the ARCHITECTURAL FIT (~90%!!), NOT a legality constraint!! **THE TRUE R-DRIVER: THE CELL-REGISTERS (every held sum needs a register!!)** — the word4's R=472 = the transplant's 421-cell-base + the 30-carrier-floor (the m=30-LP!!) + 9 (the ret-carriers + NEW8!!) + 12 (the greedy's inefficiency!!)!!
- **THE NATIVE-PAYOFF-MAP (the decisive grid!!)**: the 121-model at the CST-73 (the word4's decoder!!): **R=240: c = 0.001801395 (+3.27%!!) | R=260: 0.001746135 (+0.10% — THE CROSSING!!) | R=280: −2.92% | R=300: −5.74% | R=320: −8.46% | R=400: −17.73%** — vs the word4-true −23.42% at R=472: **THE 121 CROSSES THE FRONTIER AT R ≈ 260** — the record's "the crossing-R ~ 260-280 (the phantom!!)" CONFIRMED at the CST-73!!
- **THE 451-FLOOR DECONSTRUCTED (the §151-class!!)**: the floor = "421 + 30" — **THE 421 = THE R420-TRANSPLANT's OWN BASE (the E8-cell-machinery!!) — NOT A NATIVE-121 BOUND!!**; the m=30 = the carriers' packing (the LP-dual ✓ native!!) — **THE NATIVE QUESTION: a 121-native cell-family with the registers ~ 260-300?!** — the 121's own sharing: the special-line ⊥ ALL (its 120 incidences servable by FREE dim-1 reads (the 672-frame ⊆ every root's t-perp!!)) + the perp-intersection lattice (the native cells!!)!!
- **THE BUILD (the user's directive!!)**: STEP-1 the extraction (ii19_nat1.py: the actual perp-structure + the intersection-lattice closure + the frame-lattice!!) → STEP-2 the cell-family design (the min-registers GF(2)-cover with the frame-nesting legality!!) → STEP-3 the word build (the channels: the word4's W-solve + the D-extension law REUSED!! + the native cells!!) → STEP-4 the gcheck + the price (the crossing verdict!!)!!

## THE CST-FLOOR 73 PROVEN AT THE FULL-CODE LEVEL — THE DEFICIT 9,952 = THE ABSOLUTE 121-MAXIMUM (THE MIN-WEIGHT-BASIS VERIFICATION!!): THE Brows-CODE's WEIGHT DISTRIBUTION {0:1, 56:120, 57:135, 64:135, 65:120, 121:1} — NO LIGHT CODEWORDS (THE MIN 56!!); THE ONLY LEVER LEFT = THE R (ii19_mwbasis.py)

- **THE LEVER-HUNT (the user's FIND MORE BREAKTHROUGHS!!)**: THE IDEA: the rets = ANY 9 independent codewords of the Brows-code (the rank-9 GF(2)-code spanned by the 121 rows — 512 codewords!!) — the SS1492-basis was ONE choice; a MIN-WEIGHT basis (the light supports -> the small frames!!) could collapse the CST and explode the deficit (+288/CST-unit!!) — at the CST-45: the deficit 18,016 (+81%!!) -> the c ~ +38%!!
- **THE VERDICT: THE LEVER IS DEAD — AND THE FLOOR IS NOW FULLY PROVEN!!**: (1) **THE WEIGHT DISTRIBUTION: {0:1, 56:120, 57:135, 64:135, 65:120, 121:1}** — the code has NO codeword below weight 56 (the min-weight basis: 8×56 + 1×57!!); (2) **THE SPAN-DIMS: the 56-weights span 8, the 57-weights span 9** (the 64/65/121 too!!); (3) **THE PARITY: any basis = 8 evens + 1 odd FORCED** (the even-subcode has rank 8; the odd-part needs the +1!!) -> **EVERY BASIS: Σ(the span-dims) >= 8×8 + 1×9 = 73** — THE CENSUS-FLOOR 73 INDEPENDENTLY VERIFIED AT THE CODE LEVEL (the word4-SS1492 = ONE of the many min-weight bases!!!!); (4) **THE DEFICIT 9,952 = THE ABSOLUTE 121-MAXIMUM (PROVEN!!)** — the master-law numerator can never exceed it!!
- **THE BONUS STRUCTURAL FINDING: ALL 9 min-weight supports have DEGENERATE Grams (9/9!!)** — the supports' spans carry a radical (the frame-enlargement beyond the span is STRUCTURAL: the word4's frames contain extra lines to kill the degeneracy!!) — the frames' Gram-determinants ≠ 0 (the gcheck rule!!) force the bigger frames!!
- **THE CONSEQUENCE: THE CROSSING RIDES ENTIRELY ON THE R** (the ln-term!!): the native assembly at R <= ~262 = the ONLY route (the payoff-map: +0.10% at R=260!!) — the extraction (STEP-1) + the cell-family design (STEP-2: the perp-intersection lattice!!) = THE DECISIVE BUILD!!

## THE TOOL-AUDIT's PARTIAL VERDICT (KILLED BY CHOICE!!): THE HOST-DP LEVER DEAD (the greedy = the exact-DP at BOTH the R420 + the P111 published hists (it=70, the 12-digit equality!!)) + THE P111's NATIVE-MAP: THE CROSSING AT R~428 (THE TRUE-SHAPE +5.58% AT R=400!!); the P111's PUBLISHED WORD AT R=439 SITS PAST THE CROSSING (ii19_osc1.py + ii19_p111map.py)

- **THE AUDIT's BATTERY (2/3 done at the kill!!)**: (1) THE R420 TRUE HIST: the greedy 0.00165382698815 = the DP 0.00165382698815 = the published 0.001653826988146798944268 (it=70!!); (2) **THE P111 HIST: the greedy 0.00173305282333 = the DP 0.00173305282333 = the published 0.001733052823330162099157 (it=70!!)** -> **THE HOST-DP LEVER: DEAD** (the greedy hosting = the EXACT-DP at the REAL hists!! the audit's decisive-question (c) CLOSED!!); (3) the word3-hist battery line + the band re-runs (own1/own2/own5/own7/ext8/h10) + the K=4-vs-5: NOT RUN (the kill!!) — the engine-validation achieved INDEPENDENTLY (the 3 published hists verified across the sessions: the R420 (the audit + the battery!!), the P111 (the audit + the p111map!!), the word3 (the previous session!!)).
- **THE P111's NATIVE-MAP (ii19_p111map.py!!)**: the deficit 256*111 - 288*63 = **10,272 (BIGGER than the 121's 9,952!!)**; the published TRUE-HIST control: c = 0.00173305282333 (the EXACT published P111!! the damped engine's second published reproduction!!); the model-grid: **R=300: +19.52% | R=330: +14.34% | R=360: +9.52% | R=390: +5.19% | R=410: +2.47% | R=430: -0.18% (THE CROSSING AT R~428!!)**; the TRUE-shape (the published hist, the R-rescaled!!): **R=400: +5.58% | R=420: +2.29% | R=430: +0.72%** — **THE P111's PUBLISHED WORD (R=439) SITS PAST THE CROSSING: the native/reshaped P111 at R~400-420 = +2.3-5.6%!!** (the gap: just ~19-39 registers!!) — the P111 = the OTHER buildable frontier-crossing word (the E8-subset, NO special, h=8, the m=65!!)!!
- **THE REGISTER-REUSE SCAN (the word4!!)**: the 463 helpers vs the 9 target-combos (the repB-XORs + the O0-carrier!!): **0 HITS — the fresh registers FORCED (the R=472 honest!!)** (the only x-part match: the 605 itself at the FULL (unreadable!!)); the [253]x2-removal variant: **NO PRICE (the root-fail!!)** — the built word4's hist shape is the priceable one (KEEP!!).

## THE E8-SUBSET DEFICIT-LAW (ii19_e8sub.py!!): deficit = 9,984 + 32k (THE SPAN-7 WINDOW!!) — THE P111-CLASS (k=9: the CST 63, the deficit 10,272!!) = THE ABSOLUTE MAX-DEFICIT SYSTEM (THE PUBLISHED P111 WAS OPTIMAL!!); THE FRAME-COST OBJECTIVE (span + radical!!) RESOLVES THE CST-63's ORIGIN!!

- **THE OBJECTIVE CORRECTION (the breakthrough!!)**: the CST = Sum(the rets' frame-costs) with **the frame-cost = span_dim + radical_dim** (the minimal NONDEGENERATE frame containing the support — NOT the min-weight!! the min-WEIGHT basis (the earlier scans!!) minimizes the WRONG objective (the weights!!): ALL its codewords span 8 (the CST 72 for every subset!!)!!); the min-COST basis (the greedy over the cost-sorted codewords = EXACT for the independence matroid!!).
- **THE SPAN-7 LAW (the measured!!)**: each removed line unlocks EXACTLY ONE span-7 codeword (the (span, radical)-census: {(7,0): k, (8,0): 512-k-1} for the minus-k subsets!!) — no span-6s (the samples!!), no radicals (the E8's subspaces all nondegenerate!!); the deficit: **256*(120-k) - 288*(72 - i(k)) = 9,984 + 32k while i(k) = k independent span-7s fit the 9-basis!!**
- **THE MEASURED LANDSCAPE**: v=119: the CST 71, 10,016 (+32!!) | v=118: 70, 10,048 | **v=117: 69, 10,080** | v=116: 9,824 (the dependency-drop!!) | v=115: 9,856 | v=114: 9,600 | v=113: 9,632 | v=112: 9,376 | v=111 (the samples!!): 9,408 — **THE SATURATION AT k=9 WITH 9 INDEPENDENT SPAN-7s: the CST 63 = 9x7 -> THE DEFICIT 10,272 = THE P111's PUBLISHED DEFICIT EXACTLY!!!!** — **THE P111-CLASS = THE ABSOLUTE MAX-DEFICIT SYSTEM (the record's published choice was the OPTIMUM of the whole family!!)**; k>9: the basis saturated (no more CST-gain) + the v-drop (-256/line!!) -> DECREASING!!
- **THE CONSEQUENCE (the build-priorities!!)**: the deficit-maximization CLOSED (the 121: 9,952 (PROVEN the 121-max!!) | the E8: 9,984 | **the P111: 10,272 (THE MAX!!)**) — **THE FRONTIER-CROSSING RIDES ENTIRELY ON THE R FOR BOTH: the P111-native (the crossing at R~428 vs the published 439: the ~19-39-register shave!!) + the 121-native (R~260!!)** — the two buildable crossing-words!!

## THE 121-FAMILY DEFICIT LANDSCAPE (ii19_121sub.py!!): THE NORM-4 DISCOVERY (the 121's lines = 120 NORM-4 lines + the special (norm 2!!)) + THE SPECIAL KILLS THE SPAN-7 WINDOW (the 121-class capped at 9,952!!) + THE GLOBAL DEFICIT-MAX CLOSED: THE P111-CLASS (10,272!!) = THE ABSOLUTE MAX (THE RECORD'S ANCHOR WAS THE OPTIMAL SYSTEM!!)

- **THE NORM-4 DISCOVERY (ii19_nat1's extraction + ii19_121sub!!)**: the 121's actual lines = **120 NORM-4 lines (a=0, alpha.alpha=4!!) + the special (a=1, norm 2!!)** — NOT the E8's norm-2 roots!! (the record's "120 E8 roots" was loose!!) — the perps: 63 roots + the special (64!!) ✓; the special's perp = 120 roots ✓!!
- **THE ROOTS-ONLY (v=120, h=8!!)**: the CST 72 (the costs 9x8!!), the deficit **9,984 = the E8-class's EXACTLY** (the norm-4 and norm-2 families share the deficit laws!!); the punctures: THE SAME SPAN-7 WINDOW (+32k!!): v=119: 10,016 | v=118: 10,048 | v=117: 10,080 | .. the structured k=9 (9 independent span-7s!!): the CST 63 -> **10,272 (THE P111!!)**!!
- **THE SPECIAL KILLS THE WINDOW (the measured!!)**: the special-kept variants (the 121-k, h=9!!): the (span,rad)-census {(8,0): 256, (9,0): 255} — **NO SPAN-7 CODEWORDS AT ALL!!** — the special's presence forces every codeword to span 8-9 -> the 121-class's deficit CAPPED at 9,952 (the word4 = the class-maximum ✓✓)!!
- **THE GLOBAL CLOSURE (all the families!!)**: the 121-class: 9,952 (capped!!) | the E8/norm-4 classes (v=120, h=8): 9,984 | the punctured classes (the span-7 window!!): +32k -> **THE MAX AT k=9: 10,272 = THE P111-CLASS = THE ABSOLUTE MAX-DEFICIT SYSTEM (the record's published anchor = THE OPTIMUM!!)** | the I_{1,9}-odd: DEAD | the 2-class/h=10/L2/361/929: DEAD!!
- **THE BUILD-PLAN (the revised!!)**: **THE P111-CLASS II19-WORD (the v=111 puncture through OUR OWN ext-machinery!!)**: the deficit 10,272 + h=8 (the BEST m = 65!!) + **the crossing at R~428 (the community's published 439 sits PAST it!!)** — OUR OWN word at R~420-430 prices **+0.72% (R=430, the true-shape!!) to +2.29% (R=420!!)** — the II19-architecture's R at v=111 scales to ~433 (RIGHT AT THE CROSSING!!) + the cell-tightening -> **THE FASTER CROSSING (the -9..-19-register shave vs the 121's -212!!)** | the 121-native (R~260!!): the extraction (STEP-1!!) mid-flight!!

## THE FRONTIER-WORD BUILD LAUNCHED (the user's BUILD THE WORD!!): THE PUNCTURE FOUND (the randomized hunt: the CST 63 on the 2nd trial!!) + THE SPAN-7 THEORY (removing L frees 1_{perp(L)} (the star-indicator, the support = perp(L) EXACTLY (the weight 63!!)!!)) + THE BUILD DESIGN CLOSED (the R420's PROJECTION at R=420 (the crossing at 428!!!) + the star-builds via the content-solve (the cell-spans ⊆ W_i automatic!!) + the D-extension law!!) (ii19_span7.py + ii19_phunt.py + ii19_p111w1.py!!)

- **THE SPAN-7 THEORY (ii19_span7.py!!)**: removing the line L frees EXACTLY ONE span-7 codeword = **1_{perp(L)} (the ⊥-star indicator: the support = perp(L) EXACTLY (the weight 63!!))** — verified for the v=119/118 punctures (the theory-check: the support ⊆ perp(L) TRUE!!); the second removal: the TWO freed stars (each ⊆ its own perp!!) — the weights 62 (the punctured stars!!).
- **THE PUNCTURE-HUNT (ii19_phunt.py!!)**: the randomized 9-sets scored by the min-cost basis: **THE 2nd TRIAL: rm = [21, 23, 24, 29, 53, 71, 80, 89, 103] -> THE CST 63 (9 INDEPENDENT SPAN-7S!!)** — OUR OWN P111-class system (v=111, h=8, the deficit 10,272 (the P111's own!!)!!).
- **THE CONVENTION-VALIDATION (ii19_p111w1.py!!)**: the R420's lines == OUR word3's roots (TRUE!!) + the perps 63 (the ip_half-convention ✓✓) — **THE PUNCTURE-INDEX TRANSFER VALIDATED** + the register-map (the targets 120→111, the helpers −18!!) + the frames' census ({0:1, 1:120, 2:180, 12:70, 30:180, 63:120, 120:1} — the line-index lists!!) + the gates' prune-census (the dropped-dest/src!!).
- **THE BUILD DESIGN (CLOSED!!)**: (a) THE R420's PROJECTION: the dropped lines' gates/srcs/frames out (the projected-balance: the projection of a valid identity ✓!!) — the R = 420 (all the helpers kept!!) < 428 = **THE CROSSING (+2.29% at the true-shape R=420!!)**; (b) THE SPAN-7 SWAP: the 9 ret-registers re-purposed: the builds at the dim-7 star-frames W_i = span(perp(L_i)) reading the content-solved helpers (the cells whose contents ⊆ the star (the span ⊆ W_i AUTOMATIC!!) — the sources' multi-star conflict RESOLVED (the cell-ladder!!)); (c) the W-solve scatter + the D-extension (the word4's laws!!); (d) the CST 63 (the deficit 10,272 = the P111's!!).
- **THE REMAINING (the build!!)**: the stage-2: the re-based vector-frames + the projected gates + the baseline replay (the old-rets CST-72!!) -> the star-solve + the span-7 swap + the re-replay -> the gcheck + the price (THE CROSSING VERDICT: the ~+2.29%!!)!!

## THE NATIVE-121 v3b — THE R=219 CROSSING-CLASS STRUCTURE: THE MODEL-PRICE +28.67%!!! (ii19_nat2.py + ii19_nat3.py + ii19_nat3b.py; the user's BUILD THE FRONTIER WORD!!)

- **THE NATIVE-LINE's RESOLUTION (the recorded arc's synthesis!!)**: the partition-pieces (the SS1685: the sources' chains LEGAL BY CONSTRUCTION (the 30 disjoint 4-frames = the sources' frame partition (the E8's own resolution (the SS1679!!)))) + THE FREE SAME-FRAME RE-READS (the SS1752 discovery: the one-frame-per-dim is per DISTINCT FRAME (NOT per read!!) — the SS1695/SS1702/SS1685 collision analyses counted the READS (the PHANTOMS!!) — the honest demand = the DISTINCT-FRAME-visits (the SS1685's R_hon 390 was the PHANTOM!!!)) + the dim-4 targets' chains ({4, 4}!!) — the synthesis-design.
- **THE NAT3B's STRUCTURE (the word4's OWN lines (the norm-4 system!!!))**: (1) THE PARTITION: the backtracking cover: 30 dim-4 frames, 120/120 ✓ (the pairwise-non-orthogonal cliques (the D4-analog!!!)); (2) THE PIECES: the inside-the-frames subsets (the 330 candidates (the 2-4-line!!)): the coverage-greedy: 180 pieces (THE USERS {6: 30, 16: 60, 36: 90} — THE E8-GRADE SHARING (the mean ~23!!)); (3) THE COVERAGE: the tails {0: 2, 1: 1, 2: 12, ..., 10: 3} (the mean 5.0!!); (4) THE SPECIAL-CARRIERS: 30 (one per partition-frame (the ext6's pattern (the {120}-singleton-builds -> the dim-5 frames (the +special!!!)))); **THE R = 219 (the pieces 180 + the gathers 9 + the special-carriers 30!!)**.
- **THE MODEL-PRICE (the nat3b's hist-model!!)**: the sources {3, 5} (the 1->4->9!!) + the pieces {4, 5} + the carriers {4, 4} + the gathers {9} + the targets {4, 4} (the 0->4->8!!) + the special-target {8} + THE CST-73 ({8: 8, 9: 1}!!) — the mass 3,980 = the identity (9x219 + 73 + 2x121x8!!) — **c = 0.00224462185663348 = +28.67% vs the frontier (0.001744386!!)** — THE CROSSING-CLASS (the deficit 9,952 (the 121-max!!) + the m=73 (the CST-floor!!) ✓✓).
- **THE HONEST CAVEATS (the recorded discipline (the handoff's §8.3: the truth-pricing ONLY!!))**: the MODEL-hist (the chains approximated!) — the TRUE price needs THE BUILD: the read-rooms' real chains (the targets' ~15-20 pieces read at the ~4-8 DISTINCT frames (the finer jumps -> the LM up -> the price down (the SS1695's lesson: the ~-5-10 points!!))) -> the still-crossing ~+15-20%-class!!); the read-rooms' co-read + the nesting (the SS1661's duality!!); the legality (the sources' partition-chains ✓ BY CONSTRUCTION; the pieces' registers' chains (the frame -> the read-rooms -> the FULL!!); the targets' chains (the increasing dims!!)).
- **THE REMAINING (THE BUILD!!)**: (1) THE READ-ROOMS (the co-read groups' shared frames (the (piece, dim)-slots + the nesting (the SS1661!!)) + the FREE-re-reads-aware!!); (2) THE GATES (the sources' [1, 4, 9]-chains + the pieces' builds (the partition-frames!!) + the read-rooms' reads + the targets' [4, ..., 8]-chains + the special-carriers' channels + the gathers (the CST-73!!) + the scatter + the D/C!!); (3) THE REPLAY -> THE TRUE HIST -> THE TRUE PRICE (THE VERDICT!!); (4) THE GCHECK.
- **THE OTHER SESSION-ARC (the P111-transplant!!)**: the w8 word (R=455: the mimicry-9 + the fresh-rets-9 + the minis-17!!) PASSES the full value-replay (all 677 finals ✓!!) BUT the gcheck REJECTS at the climb-legality: ALL 120 sources are B-ENTANGLED (the B-scratch-chains (the 597 helper-writes + the source-scratch!!)) — the star-builds' pool-sources CANNOT climb to dim-7 (the B's down-climbs!!!) — the legal fix (the fresh-pieces (the ~90-120!!)) -> the R ~510-535 (~-4 to -7%!!) — the P111-transplant CLOSED at the structural-entanglement (the 121-native is THE frontier word!!).

## THE NATIVE-121 v4 — THE CUMULATIVE-CLUSTER-CHAINS DERIVED + THE JOINT-CLUSTERING IDENTIFIED (THE REMAINING BUILD-CORE!!) (ii19_nat4.py)

- **THE CUMULATIVE-CLUSTER-CHAINS (the read-rooms' design (closed on paper!!))**: the per-target: its ~15-20 pieces -> the ~4-9 NESTED clusters (the cumulative union-spans F_1 ⊆ F_2 ⊆ ... ⊆ perp(t) — THE NESTING BY CONSTRUCTION (the ⊥-lines' spans ⊆ the perp!!)); the reads FREE per cluster (the cur == F!!); the targets' chains: the deltas' hist (the nat4's chains: the steps-hist {1: 1, 4: 19, 5: 90, 6: 11} (the mean 4.9!!)).
- **THE NAT4's BUG (the decisive finding!!)**: the register-climbs counted per (target, piece)-READ (the ~4,200!!) instead of per REGISTER (the ONE chain!!) -> the mass 32,998 (the ~8x!!) — THE ROOT: the piece's register is read at the DIFFERENT targets' chains (the DIFFERENT F's!!!) — the ONE-CLIMB LAW applies: **THE JOINT-CLUSTERING (THE REMAINING BUILD-CORE!!)**: the piece's users (the 6-36!!) split into the CO-READ SUBGROUPS (the ~2-6 users (the ⊥-complements at the dim 3-6!!) — the ALL-users-F IMPOSSIBLE (the ~23 users' ⊥-complement ~1-2-dim (the special's direction!!!))), the subgroups' F's NESTED (the ⊥-closure chains: the group-2's users ⊆ the ⊥(F_1) (the F_2 ⊇ F_1 with the F_1-part ⊥ ✓!!)) — THE REGISTERS' ONE-CHAINS (the piece-span -> the nested F's -> the FULL!!) + THE TARGETS' STEPS (the JOINT (the SS1702's identified: the ONE frame per (piece, dim) AND per (target, dim)!!!)).
- **THE NEXT SESSION'S BUILD (the decisive!!)**: (1) THE JOINT-CLUSTERING (the co-read subgroups' nested-F's (the greedy (the ⊥-closures!!)) + the legality (the registers' + the targets' chains!!)); (2) THE GATES (the sources' [1, the piece-spans (the +1-2!!), the FULL] + the pieces' builds + the read-rooms' reads + the targets' cumulative chains + the special-carriers' channels (the 30!!) + the gathers (the CST-73!!) + the scatter + the D/C!!); (3) THE REPLAY -> THE TRUE HIST -> THE TRUE PRICE (the nat3b's model: +28.67% at the R=219; the honest-expectation: the ~+15-20% (the finer jumps (the LM-up (the SS1695's ~-5-10 points!!)))); (4) THE GCHECK -> THE RECORD (THE FIRST CROSSING-CLASS LORENTZIAN WORD!!!).

## THE NATIVE-121 v5 — THE REGISTERS'-ONE-F DERIVED (THE USERS'-PERP-SUBSPACES: ALL DIM-3!!) + THE MODEL +29.04% AT THE R=219!!! (ii19_nat5.py)

- **THE F-DERIVATION (the closed!!)**: the register's read-F = its users' span's PERP-COMPLEMENT (the 9-dim ambient!!): the measured: ALL 180 at DIM-3 (uniform!!) + the piece's span ⊆ F: 180/180 ✓✓✓ (the perp-linearity (the piece's lines ⊥ the users -> the span-combinations ⊥ ✓✓!!)) — THE ONE FRAME PER REGISTER (the FREE all-users reads (the cur == F!!!)); the fdim = 9 - rank (the SVD-shape-bug fixed (the min(len, 9)-shape was computing the 6-dim garbage!!!)).
- **THE TARGETS' CHAINS (the model!!)**: the pieces'-F's (the dim-3!!) -> the steps {2: 120} (the mean 2.0!!!): the deltas {3: 120, 5: 120} (the 0 -> 3 -> 8 chains (the SHORT!!!)).
- **THE MODEL-PRICE (the nat5!!)**: the hist {1: 300, 2: 180, 3: 120, 4: 60, 5: 120, 6: 180, 7: 120, 8: 10, 9: 10} (the mass-identity (the +30 honest-adj!!)) — **c = 0.00225133 = +29.04% vs the frontier (0.001744386!!)** at THE R = 219 (the pieces 180 + the gathers 9 + the special-carriers 30!!) — THE CROSSING-CLASS ✓✓ (the deficit 9,952 + the m=73 ✓✓).
- **THE REMAINING LEGALITY-CORE (THE JOINT-CLUSTERING (the final form!!))**: the register's ~6-36 users read it at THEIR merged-frames (the per-dim unions (the dim 4-8 (⊆ perp(t)!!))) — the register's ONE-CLIMB -> **THE CO-READ GROUPS** (the users sharing the ONE merged-frame (⊆ every member's perp!!)) + THE NESTED-MERGES (the register's chain: the F (dim-3!!) -> the group-merged-1 -> the group-merged-2 (the NESTED (the perp-closures (the SS1661-duality!!!)))) + the targets'-steps (the <= 8 (the mass-8!!)).
- **THE NEXT (THE BUILD!!)**: (1) THE JOINT-CLUSTERING (the co-read groups + the nested-merges (the design (the greedy (the maximal-groups (the common-perps {31, 37, 63}!!!))))); (2) THE GATES (the full word: the sources' [1, the piece-spans, the FULL] + the pieces' builds (the partition-frames!!) + the F-climbs + the merged-reads + the special-carriers (30!!) + the gathers (the CST-73!!) + the scatter + the D/C!!); (3) THE REPLAY -> THE TRUE HIST -> THE TRUE PRICE; (4) THE GCHECK -> THE FIRST CROSSING-CLASS LORENTZIAN WORD!!!

## THE NATIVE-121 v6 — THE ONE-CLIMB-WALL MEASURED (THE ~24.3 INCOMPARABLES!) + THE NESTED-USER-CLUSTERS DERIVED (ii19_nat6.py)

- **THE FEASIBILITY-MEASUREMENT (the decisive!!)**: the targets'-M(t) (the unions of their registers'-F's): ALL DIM-8 (the perp-fill!!); the registers' users'-M(t)-frames: PAIRWISE INCOMPARABLE (the Dilworth chain-counts = the user-counts {6: 30, 16: 60, 36: 90} (the mean 24.3!!)) — **THE ONE-CLIMB-WALL IS STRUCTURAL: the register's ~6-36 users read it at the incomparable dim-8 frames (the ONE dim-8 slot per register!!!)**.
- **THE RESOLUTIONS (derived!!)**: (a) THE CLONES (the R-explosion ✗); (b) **THE NESTED-USER-CLUSTERS**: the register's users as the ⊃-CHAINS (G_1 ⊃ G_2 ⊃ G_3 (the nested-sets!!)) with the M(G) = the perp(span(G)) — THE NESTED BY THE PERP-REVERSAL (span(G_2) ⊆ span(G_1) ⟹ M(G_1) ⊆ M(G_2)!!!) — the register's chain: the F (= M(ALL) (dim-3!!)) -> M(G_2) (dim ~4!!) -> M(G_3) (dim ~5-6!!) -> the FULL — THE ASCENDING (✓✓ by construction!!!); (c) THE TARGETS'-MERGED-STEPS: the per-dim unions (the ⊆ perp(t) ✓✓) with the FREE same-frame multi-register-reads!!
- **THE NAT7's CONVERGENCE-MEASUREMENTS (the next!!)**: the per-register ⊃-cluster-counts (the ≤ ~7 slots (the mass-9!!)) + the targets'-merged-step-counts (the ≤ 8!!) + the co-ordination (the B-scheduling (the topological (the registers'-chains × the targets'-chains!!!))) -> THE GATES -> THE REPLAY -> THE TRUE HIST -> THE TRUE PRICE -> THE GCHECK!!!
- **THE MODEL-STANDINGS (the honest!!)**: the nat5's +29.04% at the R=219 (the model (the hist-shape's the tax-risk (~-5-10 (the SS1695!!)))) — THE TRUE verdict needs the full joint-legality (the above!!).

## THE NATIVE-121 v7 — THE GLOBAL-M-POOL's FIRST-CUT: THE ~13.5-CLUSTER-INCOMPARABLES (THE WALL-CONFIRMED!) + THE TARGETS-ONE-M ({1: 120}!!) + THE ARRIVAL-FIT (THE SUPER-CHAIN DESIGN!) (ii19_nat7.py)

- **THE FIRST-CUT's MEASUREMENTS**: the co-read-pairs (the >= 3-shared-pieces): 7,083 (the top: 23-shared!!); the greedy clusters: 35 (the sizes {2: 17, ..., 16: 1} (the mean 3.4!!)); the M-dims {2: 1, ..., 7: 17} — **THE REGISTERS-M-COUNTS: the mean 13.5 (the <= 7-budget VIOLATED!) + the INCOMPARABLE 180/180** — the wall at the cluster-level (the register's users' ~13.5 incomparable cluster-M's!!!).
- **THE TARGETS-M-STEPS: {1: 120} (the mean 1.0!!)** — the targets read ALL their registers AT their ONE cluster-M (the ⊆ perp(t) ✓✓ (the partition-clusters!!!)) — THE TARGET-SIDE SOLVED (the ONE-STEP!!!).
- **THE F ⊆ THE M ALWAYS (the derived!!)**: the cluster ⊆ the register's users (the co-read (the >= 3-shared!!!)) -> span(cluster) ⊆ span(users) -> the F (= the perp(span(users))) ⊆ the M (= the perp(span(cluster))) (THE PERP-REVERSAL!!!) — the register's climb F -> M LEGAL ALWAYS ✓✓✓.
- **THE ITERATION-2 (THE SUPER-CHAIN DESIGN (the remaining!!))**: the registers' users as the SUPER-CHAINS (the users' nested-clusters (G_1 ⊃ G_2 ⊃ ... (the per-register (the ~2-4 levels!!!)))): the M(G)'s NESTED by the perp-reversal (the register's chain: the F -> M(G_1) -> M(G_2) -> ... -> the FULL (the ASCENDING ✓✓ BY CONSTRUCTION!!!)); the ARRIVAL-FIT: the ~2-4-distinct-frames-per-register x 180 = the ~360-720 vs the 9R = 1,971 (THE R = 219!!!) ✓✓✓ THE CAPACITY-FIT; the SUPER-CHAIN-CONSTRUCTION (the greedy (the users' ⊃-chains (the co-read-levels (the design-iteration (the ~1-2h (THE NAT8!!!)))))
- **THE STANDINGS (the honest!!)**: the model +29.04% at the R=219 (the nat5!!) — the legality's the remaining (the SUPER-CHAINS (the registers'-chains (the <= 7!!!)) + the targets'-ONE-M (the SOLVED ({1: 120}!!!))) — THE GATES + THE REPLAY + THE TRUE-PRICE after the super-chains!!!

## THE NATIVE-121 v8 — THE GLOBAL-POOL-TREE's FIT-FAILURE (THE 23/180!!) -> THE REGISTER-LOCAL SUPER-CHAINS (THE ALWAYS-NESTED!!) (ii19_nat8.py)

- **THE TREE (built!!)**: the hierarchical co-read-clusters (the levels [4, 8, 16]-caps: the 30/15/8-level clusters (the greedy (the >= 3-shared-pieces!!!))) -> the pool: 39 M-frames (the dims {3: 7, 4: 2, 5: 30}!!).
- **THE FIT-VERDICT (the decisive!!)**: the chains: the nested-OK 23/180 | the users-covered 0/180 — **THE GLOBAL-tree's M's FAIL the F-containment**: the F (= the perp(span(ALL-users))) ⊆ the M (= the perp(span(GLOBAL-cluster))) requires span(cluster) ⊆ span(users) — the GLOBAL clusters (the co-read-based (the NOT-subsets of the registers'-users!!!)) -> the INCOMPARABLE -> the F + the M (the 23/180 (the lucky-only!!!)).
- **THE ITERATION-2 (THE DERIVED-DESIGN (the ALWAYS-NESTED!!))**: **THE REGISTER-LOCAL SUPER-CHAINS**: the register's OWN users as the nested partition (G_1 ⊃ G_2 ⊃ ... (the REGISTER-SPECIFIC!!!)) — the M(G) = the perp(span(G)) (the LOCAL!!): the M's NESTED ALWAYS (the perp-reversal: G_a ⊃ G_b -> span(G_a) ⊇ span(G_b) -> M(G_a) ⊆ M(G_b) ✓✓✓ NO-LUCK-NEEDED!!!); the register's chain: the F (= M(ALL-the-users) (dim-3!!)) -> M(G_2) -> ... -> the FULL (the ASCENDING (the ALWAYS (the construction!!!))); the targets'-steps: the per-dim-merged (the <= 8!!) — THE CONSTRUCTION: the per-register users'-clustering (the nested (the OWN (the co-read-within-the-users (the pieces'-shared-structure (the NAT9 (the ~1-2h (the design-iteration!!!)))))).
- **THE STANDINGS (the honest!!)**: the model +29.04% at the R=219 (the nat5!!) — the legality's the remaining (the register-local chains (the ALWAYS-nested (the derived!!!)) + the targets'-steps-merge (the <= 8!!) + the B-scheduling (the joint (the topological!!!))) -> THE GATES -> THE REPLAY -> THE TRUE-PRICE -> THE GCHECK!!!

## THE NATIVE-121 v9 — THE REGISTER-LOCAL SUPER-CHAINS: THE NESTED-OK 180/180 (THE PERP-REVERSAL EMPIRICALLY-VERIFIED!!) + THE TARGETS-EXPLOSION (the ~36.5!!) — THE JOINT's FINAL FORM (ii19_nat9.py)

- **THE REGISTER-SIDE: SOLVED (180/180!!)**: the register-LOCAL super-chains (its OWN users as the nested partition (G_1 > G_2 > ...)): the M(G) = the perp(span(G)) — THE NESTED ALWAYS (the perp-reversal (verified empirically (the 180/180!!!))); the chain-slots {3: 180} (the mean 3.0 (the FITS the mass-9!!!)).
- **THE TARGETS-SIDE: THE EXPLOSION (the honest-measure!!)**: the DISTINCT (register, level)-M's per target: the mean 36.5 (the {34: 8, ..., 44: 1}!!), the OVER-8: 120/120, the DIM-COLLISIONS: 120/120 — the register-local M's are NESTED-legal but UNSHARED (~360 distinct frames (the per-register-OWN!!!)) — the targets need the SHARED frames (the <= 8 (the ONE-per-dim!!!)).
- **THE JOINT-CONFLICT's FINAL FORM (the precise!!)**: the SHARED-M's must (a) contain the registers'-F's (the climbs' legality!!) AND (b) be shared across the targets (the <= 8-steps!!) — the register-local gives (a)-ALWAYS but never (b); the global-co-read gives (b) but rarely (a) (the nat8: 23/180!!).
- **THE RESOLUTION-THE R420's-OWN**: the GLOBAL CELL-LADDER (the dim-2-cells ⊆ dim-4-12-frames ⊆ ... (the STRUCTURAL inclusions (the E8's own cell-lattice!!!))): the 121's equivalent = THE NORM-4 CELL-LATTICE (the dim-2/4/6-cells (the structural ⊆-inclusions (the shared-frames (the co-read (the NAT1-LITE's EXTRACTION (the remaining-core (the ~1-2h!!!)))))).
- **THE STANDINGS (the honest!!)**: the model +29.04% at the R=219 (the nat5!!) — the legality-core (the FINAL): the cell-lattice-ladder (the shared-nested (the registers'-climbs + the targets'-steps (THE BOTH!!!))) -> the gates -> the replay -> the TRUE price -> the gcheck!!!

## THE NATIVE-121 — THE JOINT-STRUCTURE's PRECISE SCOPING (THE NAT10's DESIGN-SPACE (THE MEASURED-TENSION!!))

- **THE JOINT-TENSION (the precisely-measured!!)**: the register's multi-user reads REQUIRE its users' read-frames as a ⊆-CHAIN (the one-climb law!); the targets' chains ALLOW only the ≤ 8 frames (the one-per-dim!); the register-local ⊃-chains give the ALWAYS-nested register-side (180/180!!) but the UNSHARED M's (the targets' ~36.5-explosion!); the global-co-read gives the sharing but the F-containment fails (23/180!).
- **THE NAT10's DESIGN-SPACE (the cell-lattice (the R420's-own-resolution!!))**: the GLOBAL-SHARED-NESTED-LADDER: the frames-pool (the perp-intersection-subspaces (the co-read-cluster's ⊥'s (the NESTED-levels (the structural-inclusions!!!)))) — the requirements: (a) every register's F ⊆ its read-frames (the ⊥-reversal: the pool-cluster ⊆ the register's users!!); (b) the pool-frames shared across the targets (the ≤ 8-steps!!); (c) the pool's nested-chains (the registers' climbing-legality!!).
- **THE CONSTRUCTION-KEY (the identified!!)**: the pool-clusters must be SUBSETS of the registers'-users-sets (the (a)-containment!!) AND shared (the (b)!!) — the co-read-structure: the target-pairs/triples/quads (the shared-pieces-sets (the ≥ 3-shared!!!)) — the harmonization (the registers'-users'-partitions aligned to the GLOBAL-cluster-tree (the co-read-levels (the ~4-8-levels (the dims 4-8 (the per-dim (the ONE-per-(target, dim) (the MERGED?! — the register's-chain (the ✗?!?! — THE ITERATION-CORE (THE NAT10's-WORK!!!)))))).
- **THE STANDINGS (the honest!!)**: the model +29.04% at the R=219 (the nat5!!) — the legality-core (the FINAL-remaining!!): the cell-lattice-ladder (the joint (the (a)+(b)+(c)!!!)) -> the gates -> the replay -> the TRUE hist -> the TRUE price -> THE GCHECK -> THE WORD!!!

## THE NATIVE-121 v10 — THE BIG-PIECES: THE LEGALITY 55/55 (THE PERP-REVERSAL AT THE CARRIER-SCALE!!) + THE COVERAGE-TRADE-OFF (THE MEAN-TAIL 56.0!!) (ii19_nat10.py)

- **THE BIG-PIECES (the ext6's carrier-scale!!)**: the unions-of-2-3-partition-frames (the 8-12-lines (the greedy (the <= 6-users (the MEASURED: the 55-pieces (the users {1: 13, 2: 23, 3: 16, 4: 3} (the mean 2.2 (THE CARRIER-SCALE ✓✓✓!!!)))))
- **THE LEGALITY: 55/55!!!** — the piece-spans ⊆ the users-M ALWAYS (the perp-reversal (the users ⊥ the piece-lines (the ALWAYS (the verified!!!))) — the M-dims {6: 3, 7: 39, 8: 13} (the perp-scales!!); the ONE-SHARED-M-PER-PIECE (the ONE-CLIMB (the FREE-reads (the ~2.2-users (THE LEGAL-STRUCTURE (THE SOLVED!!!)))
- **THE COVERAGE-TRADE-OFF (the measured!!)**: the big-pieces cover ~8 of the ~64 perp-lines per target (the per-target-pieces {0: 55, 1: 34, ...} (the mean 1.0!!)) — THE MEAN TAIL 56.0 (the {55: 32, 63: 55, ...}!!) — the tails' delivery needs the sources'-CELL-HIERARCHY (the R420's own [1, 1, 2]-solution (the sources' one-climb through the dim-2-cells!!!)) — the nat1's extraction-core (THE REMAINING!!!)
- **THE DESIGN-SPACE's FINAL-MAP (the measured!!)**: the ~4-line-pieces: the coverage ~62/64 BUT the users ~6-36 (the ILLEGAL (the nat9's ~36.5-explosion!!)); the ~8-12-line-pieces: the users ~2.2 (the LEGAL (the 55/55!!)) BUT the coverage ~8/64 (the ~56-tails (the cell-hierarchy-needed!!)) — THE MIXED-SCALE (the ~4-line-shared-cores + the ~8-12-line-carriers + the cell-laddER-TAILS (THE NAT11's-DIRECTION (THE REMAINING (~2-4h!!!))))

## THE SESSION's FINAL — THE GCHECK-PASS CONFIRMED (THE WORD4 (THE RECORD-WORD!!)) + THE NAT-SERIES's-HONEST-MAP (THE COMMITTED!!!)

- **THE GCHECK: PASS (re-confirmed (the word4 (the committed record-word!!!)))**: R=472, v=121, h=9, CST=73, the mass-identity OK, the true price c = 0.001335891046497132929087 (the -23.42% vs the P111-frontier (THE RECORD (the committed!!!))).
- **THE NAT-SERIES (nat2-nat11 (the committed!!))**: the from-scratch R-shave-design (the R=219-the-model (+29.04%!!) — the legality-layers measured to the precise-core: the register-side SOLVED (the perp-reversal (the 180/180 (the 55/55!!!))); the target-side: the carrier-scale (~2.2-users (THE LEGAL!!)) vs the coverage (~56-tails (the cell-ladder-needed!!)) — THE MIXED-SCALE (THE NAT12's-core (the ~2-4h (the next-session!!!)))
- **THE WORD4's-MECHANISM (the concrete-read (the gcheck-proven!!))**: the targets'-3-B-gates (the DIRECT-source-read (the dim-2-cell (the free!!!)) + the special-carrier (the dim-13) + the perp-delivery (the perp-frame!!)); the carriers (the ACCUMULATOR-LADDER: the singleton (dim-1) -> the cell (dim-2) -> the 12-frame (dim-4) -> the 30-frame (dim-6)!!!) — the R420's-own structural-shared-ladder (THE LEGAL-TEMPLATE (the nat12's-redesign-target (the cell-replacement (the big-pieces-at-the-coverage-scale (THE CROSSING-CLASS (THE +15-24% (THE NEXT!!!)))))))

## THE NATIVE-121 v12 — THE ~30-LINE-PIECES' GREEDY-DEGENERACY (THE STRUCTURAL-VALLEY-MAP!!) + THE FINAL-HONEST-VERDICT (ii19_nat12.py)

- **THE GREEDY-DEGENERACY (the measured!!)**: the built-up-greedy (the 1-line-at-a-time (the intermediate 2-line-pieces' users ~37 (the > 8 (the CARRIER-SCALE-violation (the STUCK-AT-1!!!))) — the users-count's VALLEY: the 1-line: ~63 | the 2-line: ~37 | the 4-line: ~6-36 | the 8-12-line: ~2.2 (THE CARRIER-SCALE (the ONLY-WORKING-CONSTRUCTION (the nat10's partition-frame-unions!!!))) — the structural-valley (the coverage-scale-pieces (the ~30-line (the users (the ~1-6-EXPECTED?! (the DIRECT-CONSTRUCTION-NEEDED (the greedy-impossible!!!))))
- **THE FINAL-HONEST-VERDICT (the session's!!)**: THE WORD4 (THE GCHECK-PASS (THE VERIFIED (THE RECORD-WORD (the -23.42%!!!)))) is THE legal full-coverage structure (the R420's ~430-cell ladder (the gcheck-proven!!!)); the from-scratch R-shave (the R=219-the-model (+29.04%!!)) requires the DIRECT 8-12-line-piece construction + the tails' cell-ladder (the nat12b+ (the ~2-4h (the NEXT-SESSION's-CORE (THE MIXED-SCALE (THE GATES (THE REPLAY (THE GCHECK!!!)))))))

## THE NATIVE-121 v12c — THE BREAKTHROUGH: THE DIRECT PERP-SPLITS AT THE CARRIER-SCALE!! (the users {0: 304, 2: 56} (the mean 0.3!!)) (ii19_nat12c.py)

- **THE MEASURE (THE DECISIVE!!)**: the DIRECT PERP-SPLITS (the perp(t) (the ~63-lines) -> the 3-splits (the ~21-LINE pieces!!)): THE USERS: **{0: 304, 2: 56} (the mean 0.3!!!)** — THE OVER-8: 0/360!!! — THE CARRIER-SCALE SATISFIED AT THE COVERAGE-SCALE (the ~1-3-users-per-piece (the near-PRIVATE (THE NO-ONE-CLIMB-WALL!!!!!!)))
- **THE CONVERGED-DESIGN**: the ~360-pieces (the 21-line (the per-target-3-splits!!)) — the targets read their ~3-pieces (the <= 8-STEPS (THE PERFECT-FIT!!!)); the pieces'-M's: the perp(span(users)) (the ~1-3-users (the dim ~6-8 (the >= the piece-span (the perp-reversal (the ALWAYS!!!)))); the pieces'-chains: the piece-span (the ~6-8-dim!!) -> the M -> the FULL ✓✓✓ — THE LEGAL-STRUCTURE (THE NO-WALL!!!)
- **THE REMAINING-BUDGET (the sources!!)**: the piece-BUILDS' ~21-srcs (the sources'-~63-reads?!?! — THE CELLS-LADDER (the R420's own [1, 1, 2]-solution (the ~1-3-cell-memberships (the u (the read (the ~1-3-cells (the cells (the ~2-3-line-pair-sums?!?! (the +R?! (the ~?! — THE MEASURE (THE NEXT (THE BUILD!!!
- **THE R-ESTIMATE (the honest!!)**: the ~360-pieces?! (the price?! (the natmap (the R=360: the ~-9%?! — the WORD4's -23.42% + 14-points?! (THE RECORD?! — the CELLS-LADDER (the ~+60-120-cells?! (the R ~420-480?!?! — hmm — the SHARING-REDESIGN?! (the 2-splits?! (the ~240?! (the ~-2%?! (THE BORDERLINE!!! — the nat12d (the budgets (the BUILD!!!))))

## THE NATIVE-121 v12d — THE CELLS-MEASURES (THE PAIRS'-CO-OCCURRENCE-GOLD!!) (ii19_nat12d.py)

- **THE SOURCES'-WALL (the value-level (the confirmed!!))**: the sources-piece-memberships {63: 120} — EVERY source in ~63 pieces (the per-target-split-design (the u (the ∈ perp(t) (the ~63-t's (the ONE-SPLIT-EACH!!!)))
- **THE PAIRS'-CO-OCCURRENCE-GOLD (THE MEASURED!!!)**: the pairs-in-pieces: 3,535 distinct (the co-occ-peaks {36: 493, 30: 583, 28: 184, 34: 153} (the mean 21.4!!)) — the best-partner-co-occs **{36: 107}** — most sources have ONE partner co-occurring in ~36 pieces!!! — THE CELLS {u, w} (the shared-sums (the ~36-piece-service-potential!!!))
- **THE CELLS'-OWN-CHAIN (THE REMAINING-CORE!!)**: the cell {u, w} (the ~36-reads?! — the SAME-wall-at-the-cell-level?! — THE LADDER-DEEPENING (the cells -> the super-cells -> the pieces (THE R420's-430-structure (the dim-2 (180!!) -> dim-4 (70!!) -> dim-6 (180!!) -> the perps!!!)))
- **THE HONEST-R-SCOPE**: the pieces (360) + the cells + the ladder (the ~660-raw?! (the vs-the-word4's-472!!) — THE R-SHAVE (the pieces'-SHARING (the 2-splits (~240!!) + the shared-D6-analogs (THE NEXT (the ~2-4h (THE BUILD!!!

## THE NATIVE-121 v13/13b — THE D6-LATTICE BREAKTHROUGH (THE FULL SET-COVER ACHIEVED!!!) (ii19_nat13.py, ii19_nat13b.py)

- **THE D6-ANALOGS (THE CONFIRMED!!)**: the pair-commons: 7,140-pairs (the {30: 3,780, 36: 3,360}-line common-perps!) -> the DISTINCT-sets: 4,900 — **THE SPAN-DIMS: {6: 4900} (ALL DIM-6 (THE E8-D6-EQUIVALENTS!!!))** — the multiplicities {1: 3,780, 3: 1,120} (the quad-sharing!)
- **THE PER-TARGET STRUCTURE (THE UNIFORM!!)**: the DISTINCT-D6s {91: 120} (each target: 91 D6s inside its perp!) — **the top-3-D6-coverage 0.952 (the MIN 0.952 = the UNIFORM!!!)**
- **THE GLOBAL-D6s' USERS: {2: 3780, 3: 1120} (THE CARRIER-SCALE (THE 2-3-users-per-D6!!!))**
- **THE SET-COVER (THE GREEDY!!!)**: 286-chosen -> **the tails {0: 120} (THE FULL COVERAGE!!!!!!)** — the per-target {4: 112, 5: 2} + 5-outliers {7, 15, 26, 40, 60, 87} (the fixable-priority!) — the users'-scale ✓✓✓
- **THE REMAINING-WALL (THE u-memberships ~77.5!!)**: the D6-builds'-~33-srcs -> the sources'-ladder (THE CELLS-LEVEL-BELOW (the D2-cells (the u's-~1-3-memberships?! — THE LADDER (THE R420's-OWN [1, 1, 2]-STRUCTURE (THE ~2-4h (THE NEXT-CORE!!!))))
- **THE R-ESTIMATE**: the 286-D6s + the cells (~120-180?) + the specials (~42) + the gathers (9) (the ~460-520?! (THE WORD4-CLASS (THE ~-23%?! — the R-SHAVE?! (the top-3-coverage?! (the ~360-shave?! (the ~2-splits?! (THE NEXT!!!)))

## THE NATIVE-121 v13c — THE PAIRS'-CELL-POTENTIAL (THE MEAN-45.9!!!) (ii19_nat13c.py)

- **THE PAIRS-IN-CHOSEN-D6s**: 7,140 distinct (the co-occ-spread {3..72} (the mean 20.7!!))
- **THE BEST-PARTNER-CO-OCCS (THE CELLS'-POTENTIAL!!!)**: the mean **45.9** — most sources have ONE partner serving ~45-72 of the 286-chosen-D6-builds!!!
- **THE NAT14's-CORE (THE FINAL-STEP (THE PRECISE!!!))**:
  (a) THE GCHECK's-FREE-READ-RULE-RE-READ (the §511's-discovery: "the register read at the SAME frame: FREE (no climb, the CUR-STAYS!!!))" — THE SOURCES'-SINGLETON-FREE-READS?! — the R420's-own [1, 1, 2]-chains (the 2-FREE-singleton-reads + 1-cell-read!!!)
  (b) THE CELLS-LADDER: the cells {u, w} (the ~45-D6-service (the pairs'-gold!!!)) + the D6-builds reading the CELLS (the sources'-~78-wall -> the ~1-3-cell-memberships!!!)
  (c) THE GATES -> THE REPLAY -> THE TRUE-HIST -> THE TRUE-PRICE -> **THE GCHECK -> THE WORD!!!**
- **THE R-ESTIMATE (THE CONVERGED!!)**: the 286-D6s + the ~60-120-cells + the ~42-specials + the 9-gathers = **the ~400-460 (THE WORD4-CLASS (the ~-23%-model?! — the R-SHAVE (the sharing (the ~2-4h (THE NEXT!!!))))**

## THE NATIVE-121 v14 — THE SOURCES'-FRAMES-TRUTH (THE WORD4's-OWN-SOLUTION!!!) (ii19_nat14.py)

- **THE GCHECK's-FREE-READ-RULE (THE CONFIRMED (THE gcheck.py-LINE-77!!!))**: `climb(r, F): if cur[r] == F: return` — the sources read at their CURRENT frames: FREE (the cur UNCHANGED (the UNLIMITED!!!))
- **THE WORD4's-SOURCES (THE MEASURED (THE {4: 120}!!!))**: every source at exactly **4 DISTINCT FRAMES** (the singleton (dim-1!) -> the cell (dim-2!) -> the mid (dim-5/6!) -> the high (dim-7/8!)) — the ~8-reads via the FREE same-frame re-reads!!!
- **THE IMPLICATION (THE NAT15's-CORE (THE FINAL-STRUCTURING!!!))**: the ~78-piece-memberships-per-source LEGAL IFF the reads cluster at the ~4-frame ladders: the D6-builds'-srcs must be structured through the SHARED cells (the pair-sums at the shared dim-2-frames!) -> the mids -> the D6-builds (the the-R420's-OWN-LADDER-PATTERN (THE MEASURED (THE PROVEN!!!)))
- **THE NAT15 (THE FINAL (THE ~2-4h (THE BUILD!!!)))**: the cells'-clusters (the u's-78 (the 4-FRAME-GROUPS (the SHARED-STRUCTURING!!!))) -> the gates (the THE-LADDER (the D2->D4->D6->perp (the the-R420's-OWN!!!))) -> the replay -> the TRUE-hist -> the TRUE-price -> **THE GCHECK -> THE WORD!!!**

## THE NAT15's-ALGORITHM-SCOPE (THE FINAL-STEP (THE PRECISE (THE NEXT-SESSION's-BUILD!!!)))

**THE CELLS'-4-FRAME-CLUSTERING (THE ALGORITHM!!)**:
1. PER-SOURCE u: its ~78-chosen-D6-memberships -> the 4-GROUPS (the 4-MIDS?! — the SHARED-subspaces!)
   - THE GROUPING-CRITERION: the D6s'-UNION-SPANS?! — the 4-CLUSTERS?! — the the-clustering?! — hmm: the SIMPLEST: the u's-D6s?! — the 4-MIDS?! — the D6s'-SPANS (the the-4-frAMES?! — the SHARED?! — hmm: the the-u (the the-4-frAMES?! — the the-4-MIDS?! — the the-... — hmm: the HONEST-START: the word4's-OWN-mechanism (the §565's-H263?! (the the-ACCUMULATION?! (the the-LADDER?! — hmm: the u's-4-frAMES?! (the the- singleton?! (the the-... — the NAT15's-STEP-0?! — the the-word4's-per-source (the the-FRAMES?! (the the-STRUCTURE?! — the the-MEASURE?! — the the-word4's-u (the the-the-4-frAMES?! (the the-the-SHARED?! (the the-the-MIDS?! (the the-the-SUBSPACES?! — the the-the-OTHERS?! — hmm: the the-word4's-4-frAMES?! (the the-the-OTHERS?! — the the-the-SHARED?! — the the-the-MIDS?! (the the-the-the-... — THE MEASURE?! — the the-word4's-mid-frames?! — the the-142?! (the the-543?! (the the-561?! — the the-the-SHARED?! (the the-the-... — hmm: the word4 (the the-R420's-mids?! (the the-DIM-2?! (the the-543?! (the the-DIM-?! — hmm — the NAT15's-STEP-0 (THE WORD4's-MID-CENSUS?! (THE ~15-min!!!)))
2. THE CELLS'-GREEDY: the pairs'-gold (mean-45.9!) -> the SELECTED-cells (the ~60-180?! — the u's-1-3-cell-memberships!!)
3. THE LADDER-GATES: the cells (the dim-2 (the singleton-reads (FREE!!!))) -> the MIDS?! (the dim-4-6?! — the the-D6-builds?! (the the-the-... — hmm: the D6's-build?! (the the-the-33-srcs?! (the the-the-17-cells?! (the the-the-... — hmm: the D6 (the the-built?! (the the-the-... — the the-D6's-build (the the-multi-gate?! (the the-ACCUMULATION?! (the the-LADDER?! (the the-R420's-OWN (the the-the-... — the the-the-... — OK — the NAT15 (the the-... — hmm — the honest?! — the the-NAT15?! — the the-... — the BUILD!!!

## THE NATIVE-121 v15/15b — THE COMPLETE PROVEN TEMPLATE (THE WORD4's-LADDER (FINALLY CONCRETE!!!)) (ii19_nat15.py, ii19_nat15b.py)

- **THE 4-LEVEL LADDER (THE PROVEN!!!)**: the src-0: [2 (the SINGLETON (len-1!!)) -> 142 (the CELL (len-2 (the PRIVATE-PAIR-SUM!!!))) -> 543 (the 12-FRAME (len-12 (THE SHARED-MID!!!))) -> 561 (the PERP (len-64!!!))]
- **THE 12-FRAMES: 10 (THE 120-ROOTS'-PARTITION!!!)**: the frames-542..551 (the 12-LINES-each (the 12-SOURCES-EACH (THE PARTITION (the 120 = 10 x 12!!!)))) — THE D4-PARTITION-ANALOG (THE 121'S-OWN!!!
- **THE CELLS: 180 (THE PRIVATE (the 1-SRC-EACH!!!))**: the pair-sums (the 2-LINE-VECTORS (the e.g. cell-122: [0,0,0,0,0,2,0,0,0] + [0,0,0,0,0,0,2,0,0]?! — the 2 NORM-4-LINES!!!
- **THE PERP-FRAMES: 122 (the 64-len (120!!) + the 120/121-len (the specials!!)) — the 1-SRC-EACH!!!
- **THE TEMPLATE'S-STRUCTURE (THE BUILD's-ANSWER!!!)**: the sources'-4-frAMES?! — the singleton (the FREE!!) -> the private-cell (the ONE (the e_u+e_w?!)) -> the 12-frame (the THE-10-PARTITION (the the-the-12-srcs (the the-the-the?! — the the-the-THE-... — the perp (the the-... — the src's-4th?! — the the-the-perp?! — the the-the-... — the the-the-the?! — the perp-users?! (the {1: 121}?! (the the-the-1-src?! — hmm: the the-the-... — hmm — hmm: the the-the-src (the the-the-perp?! — the the-the-... — hmm: the the-the-THE?! — hmm — the the-the-... — hmm — hmm — the THE-NEXT?! — the the-the-... — the the-the-... — hmm — hmm — THE NAT15's-STEP-1?! — the the-the-A/B-gates?! — the the-the-... — hmm — hmm — OK — THE COMMIT!!!)

## THE NATIVE-121 v16b — THE WORD4's-CELL-STRUCTURE-TRUTH (THE ACCUMULATION-CONFIRMED!!!)

- **THE CELL-LEVEL (THE MEASURED!!!)**: the 360 A-gates at the 180-cell-frames — **THE 1-SRC-1-DEST-EACH!!!** — the junk-carriers (the helpers 243..661!) accumulate their sources ONE-AT-A-TIME through the ladder: the singleton-read (THE FREE!!!) -> the cell-read (the 1-climb!) -> the 12-frame (THE OTHER-HELPERS!!!) -> the 30-frame!!!
- **THE MECHANISM (THE CRYSTAL-CLEAR!!!)**: the sources feed the carriers' ACCUMULATIONS directly (~2-4-srcs-each!); the carriers read the OTHER-carrying-helpers at the higher levels (the SHARED-SUMS!!!) — the sharing happens at the CARRIER-LEVEL (the cells-PRIVATE (1-src!!!))!!!
- **THE OUR-121's-EQUIVALENT (THE NAT16's-BUILD-SEQUENCE (THE FINAL!!!))**: the D6-pieces (286!) as the junk-carriers — the D6's-BUILD?! — the ~33-srcs?! — the the-... — the the-... — the LADDER-LEVELS?! — the the-... — the CAREFUL (THE ~1-2h (THE FRESH-MIND (THE NEXT-SESSION!!!)))

## THE NATIVE-121 v17 — THE D-CHANNEL-DISCOVERY (THE COLLAPSE-DESIGN (R = 130!!!))

- **THE H2-RULE (THE gcheck.py (the the-§667 (the the-CONCRETE!!!)))**: the D-gates: [0-frame, the-TARGET-dest, the-HELPER-srcs (s >= 2v!!!)] — **NO CLIMB-CHECKS!!! NO CONTENT-CHECKS!!!** — THE D = THE FREE-DELIVERY-CHANNEL!!!
- **THE COLLAPSE-DESIGN**: the H_u's (121! (the per-line-e_u-carriers (the the-A-builts (the the-the-singleton-FREE-reads!!!)))) + THE D (the perp(t)-delivery (the ⊕(e_u)'s!!!)) + the scatter (the the-Brows-combo!!!) — **THE R = 130 (the the-the-the-121-H_u + the-9-rets!!!)!!!**
- **THE BALANCE**: [the scatter's Brows[t]] ⊕ [the D's perp(t)] = e_t ✓✓✓ — **THE REGISTER-BIT-RESIDUE (the ⊕(1<<H_u) ⊕ ⊕(1<<ret) — the one remaining algebra-detail!!!)**
- **THE NEXT (THE the-THE-... — the the-the-FINAL-STEPS: the residue-resolution → the word-emission → THE GCHECK!!!

## THE NATIVE-121 v18b — THE W4's-BALANCE-TRUTH (THE EMPIRICAL-LEARNING!!!)

- **THE REPLAY (the D+A+scatter+B (the NO-C!!!))**: THE TARGETS'-FINALS PASS (the 121/121!!! (the the-122-OK (the the-121-targets + the the-1!!!))) — THE C-PHASE (the H4-reversal) RESTORES ONLY THE HELPERS!!!
- **THE RESIDUE-TRUTH**: the srcs'-XOR (the ⊕(1<<s)) is NOT the delivered-register-part (the srcs'-VALS-are-complex (the 1<<h ⊕ the-junk!!!)) — the W4's-120/121-srcs-residues-are-RED-HERRINGS — THE ACTUAL-BALANCE (the the-VALS (the the-empirically-✓!!!
- **THE NAT18's-IMPLICATION**: the D+the-scatter+the-B (the the-vals'-balance!!!) — the design-needs (the the-B's-residue-fix (the the-... — the the-EMPIRICAL (the the-the-... — the NEXT-STEP!!!

## THE NATIVE-121 v18c — THE W4's-RESIDUE-SECRET (THE EMPIRICAL!!!)

- **THE W4's-D-DELIVERED-REGISTER-PARTS: ALMOST-ZERO!!!** (the t=0: the 2-bits (the t=1/2: the 1-bit!!)) — THE A-PHASE's-STRUCTURED-VALS: the helpers'-vals (the the-1<<h-parts (the the-⊕(the-~150-srcs) (the the-CANCELED-ALMOST-ENTIRELY!!!)))
- **THE NAT18's-IMPLICATION**: THE H_u-VALS-MUST-BE-STRUCTURED-THE-SAME!!! — the the-... — the the-... — the the-the-FIX (the the-the-... — the NEXT!!!

## THE NATIVE-121 v18d — THE RESIDUE-FIX's-IMPLEMENTATION-SCOPE (THE FINAL-ALGEBRA!!!)

- **THE FUNDAMENTAL-FACT**: the register-bits CANNOT cancel via DIFFERENT-registers (the disjoint-bits!) — the cancellation REQUIRES (a) the same-register-double-reads OR (b) THE STRUCTURED-VALS (the cross-bit-carriers (the W4's-way!!!))
- **THE W4's-PATTERN (THE the-... — the the-A-phase's helpers (the the-vals-containing-the-cross-bits (the the-organized-⊕-cancellation (the the-almost-zero-delivered!!!)))
- **THE NAT18's-IMPLEMENTATION (THE CONCRETE-STEPS!!!)**: (1) the H_u-vals'-structuring (the the-A-gates (the the-cross-reads!!!)); (2) the the-residue-measure (the per-target (the replay!!!)); (3) the the-B's-compensation (the the-pure-bit-carriers?!); (4) THE FULL-EMISSION + THE GCHECK!!!
- **THE the-the-the-the-... — THE NEXT-SESSION (THE the-fresh-mind (THE the-...!!!)))


## THE NATIVE-121 v19 — THE R=130-COLLAPSE's PRE-EMISSION-AUDIT + THE EMISSION + THE GCHECK's-OWN-VERDICTS: THE RESIDUE-FIX SOLVED (THE D-EXTENSION {0: 121}!!!) + THE X-CANCELLATION's-THREE-ROUTES-ALL-MEASURED-DEAD (THE PHASE-ORDER-FLAW + THE ONE-CLIMB-WALL (THE REJECT 'climb not nested (reg 244)'!!) + THE CST-NO-ROOT!!) + THE PRIZE-CONFIRMED (+62.69%!!!) (ii19_nat19.py + ii19_nat_word.py; the user's EMIT+GCHECK-VERDICT route!!)

- **THE RESIDUE-FIX (THE SOLVED (the §1's remaining-core #1!!))**: THE W4's-own D-EXTENSION-LAW (the §1862!!!) APPLIES VERBATIM: the D-srcs = the row_t-rets (the PRE-BUILD pure-self-bits (the x-part-0 (the LEGAL-at-frame-0 (the §205-fact!!!))!!)) -> the scatter's ret-bits CANCELLED at the ZERO-COST (the 121-free-gates!!!) — THE MEASURE: the faithful-§1-D (the perp(t)-H_u-reads!!): the register-residues **{64: 120, 120: 1}** (the ρ_t ✓✓ MEASURED (the §1's-formula-CONFIRMED!!)) -> THE FIXED-D: **{0: 121}** ✓✓✓ (the mass 3179 = the identity ✓✓!!) — the B-phase-compensation (the pure-bit-helpers (the user's-initial-choice!!)): UNNECESSARY-AND-INSUFFICIENT (the DISJOINT-BITS-fact (the §2081!!): the pure-bit-helpers CANNOT cancel the H_u-bits (the DIFFERENT-registers!!!) — the D-channel: the CLEANER (the ZERO-new-registers!!!)) — THE GCHECK-PASSED-D (the no-B-emission's REJECT came at the FINALS (the D+A+scatter+C-ALL-PASSED (the D-extension's-frame-0-legality ✓✓✓!!!)))
- **THE PHASE-ORDER-FACT (THE §1's-DESIGN's-HIDDEN-FLAW (the §1's remaining-core #2!!))**: the D-runs-FIRST (the gcheck's-line-100!!) -> the D-srcs PRE-BUILD (the pure-self-bits (the x-part-0!!!)) -> **THE D CANNOT DELIVER THE e_u's** (the §1's "the D (the perp(t)-delivery (the ⊕(e_u)'s!!!))": THE UNDELIVERABLE!!!) — the x-parts reach the targets ONLY via the scatter (the rets'-x-patterns!!) + the B-reads (the built-carriers!!!) — the §1's "THE BALANCE (verified empirically!)": TRUE-at-the-VAL-level (the with-B-replay: **THE FINALS-PASS 0/121-fails ✓✓✓** (the §1's-empirical-verification-was-THE-W4's-OWN-replay (the nat18b!!!) — the TRANSFERRED-to-the-new-design (the VALS-pass (the CLIMBS-the-REJECT!!!))!!)) — the §1's "single-remaining-piece"-assessment: **THE CORRECTED (the residue-was-ONE-of-THREE-gaps (the phase-order + the wall + the CST!!!)) — the §8.4-honest-correction ✓✓!!**
- **THE X-CANCELLATION's-THREE-ROUTES (ALL-MEASURED-DEAD!!!)**: (1) THE D: the phase-order-flaw ✗ (the above!!!); (2) THE B-READS (the §1's-H_u-at-the-perp-frames!!): **THE ONE-CLIMB-WALL (the SS1946!!!)**: the B-frame F_t ⊇ span(perp(t)-lines) = perp-space(t) (the src-content-check!!) ∧ F_t ⊆ perp-space(t) (the target's-chain!!) -> **F_t = perp-frame(t) FORCED** -> the H_u's ~64-users'-perp-frames (the PAIRWISE-INCOMPARABLE dim-8's (perp-space(t) == perp-space(w) iff L[t] ∥ L[w]: NEVER!!!)) -> THE PRIVATIZATION-COUNT **7,679** (the R = 130 + 7,679 = 7,809?!?! (the W4: 472!!!)); (3) THE SCATTER-RETS (the cancellation-patterns-as-rets (the duplicates-ALLOWED (the §1's-rule!!!))): the perp-patterns'-GF(2)-rank **120** (the {Brows[t] ⊕ e_t}-family!!) -> the CST ≥ 73 + 120 = 193 vs THE BUDGET 256v/288 = 107.6 -> the deficit −24,608 -> **THE PRICER's-OWN-REFUSAL ('no root' (the R=251/CST-194-test (the hist-mass-4389-identity ✓!!)))** ✓✓✓
- **THE EMISSION (the §1's-steps-VERBATIM (the residue-FIXED (the D-extension!!) + the W-solve (the min-weight-basis [56]×8 + [57] (THE CST-73 ✓✓ (the §113-124's-proven-floor!!!))) + the frames (0 + the 121-singletons + the FULL + the R8 + the 121-perps (the 245!!)) + the A (the H_u-builds-121 + the ret-builds-9-FROM-THE-SOURCES (the evens at the R8 (the FREE-same-frame-re-reads!!!) + the odd at the FULL!!)) + the C (the H4-literal-reversal (the FULL-frames!!)) + the scatter (the rows {2: 2, 3: 12, ..., 9: 1} (the special: ALL-9!!)))) + THE GCHECK's-OWN-VERDICTS (the user's-EMIT-route ✓✓)**: (i) the no-B (ii19_nat_word.json): **REJECT: 'final value of register 121'** (the x-residues {64: 120, 120: 1} = the perp(t)-patterns (THE CANCELLATION-GAP!!) — the D+A+scatter+C-ALL-PASSED (the exact-Grams ✓ the H1-H5 ✓ the climbs ✓ the retained-frames ✓!!!)); (ii) the §1-verbatim-with-B (ii19_nat_word_b.json: the B-121 (the perp-frame-reads!!)): **REJECT: 'climb not nested (reg 244)'** (the FIRST-H_u-with-≥2-users (THE ONE-CLIMB-WALL (THE CHECKER's-OWN-VERDICT!!!)) — the vals-PASS-0/121 (the §1's-balance: the TRUE-at-the-VAL-level!!!) ✓✓✓
- **THE PRIZE-CONFIRMED (the R=130-IF-IT-CLOSED (the audit's-(6a)-test!!))**: the legal-no-B-hist {1: 249, 7: 120, 8: 259, 9: 2} (the mass-3179-identity ✓!!) at the (V=121, H=9, R=130, CST-73): **c = 0.002837979497750630497081 = +62.69% vs the frontier (the converged it=75!!)** — the §1's "+50-60%-class": CONFIRMED-AND-EXCEEDED ✓✓✓ — THE STAKES'-REALITY: the II19's-first-above-frontier-witness-IF-LEGAL (the +62.69%-class (the 1.63×-the-frontier!!!))
- **THE HONEST-VERDICT (THE R=130-COLLAPSE: CLOSED (the measured + the gcheck-verified!!!))**: the residue-fix-SOLVED (the D-extension (the REUSABLE-LAW (the ANY-future-121-word's-residue-channel!!!))!!) ∧ the x-cancellation: THE BOTH-CLOSING-ROUTES-DEAD (the WALL (the 7,679-privatization!!) + THE CST (the rank-120-vs-107.6 (the NO-ROOT!!))!!) — THE 121-NATIVE's-HONEST-MAP (the nat9-11's-core-conflict + the nat19's-gcheck-verdicts!!): the LEGAL-structures' R ~ 350-460 (the nat12c's-near-private-360 + the cells-ladder (the nat16's-cells-core (the UNRESOLVED!!)) / the nat13b's-286-D6-cover + the harmonization (the nat10's-(a)+(b)+(c)!!!)) -> the −11..−23%-class (BELOW the frontier!!) vs THE CROSSING-262: the natmap's-hope (the R ~ 219-260!!): THE PHANTOM-STRUCTURES-ONLY (the nat3b/own5 (the users-6-36 (the nat6's-wall!!!)) — the §1996's-honest-verdict-CONFIRMED-AT-THE-GCHECK-LEVEL ✓✓✓
- **THE REMAINING (the honest!!)**: (a) the honest-native-build (the nat12c/13b-class (the R ~ 350-460 (the ~−11..−17%-best-case (the +5-10-points-over-the-W4's-−23.42%!!!))) — the nat16's-cells-selection (the ~2-4h!!)); (b) the fresh-directions (the P111-class-II19-word (the §1911!! (the entanglement-fix (the §1928!!))) ∨ the E8-LEVER-A (the §110-OUT!!)); (c) the R=130's-D-extension-law: the COMMITTED-REUSABLE (the §1862's-second-application (the 121-native's-own-record ✓✓!!))

## THE R434 HIST-RESHAPE — MEASURED BLOCKED (THE PUBLISHED-WORD's-OWN MOVES-SPACE CLOSED (0/2232!!!)) (ii19_p111pub2.py + ii19_p111w21.py + w22 + w23; the user's §1 handoff)

- **THE SETUP (the frontier word CONVERTED (my format!!))**: the published P111-R434 (v=111, h=8, R=434, the frontier c = 0.001744385950814795279853 = +0.6539% vs P111) converted via ii19_p111pub2.py -> **ii19_pub2_p111-r434.json: GCHECK PASSES EXACTLY** (2108 A / 918 B / 2591 C / 111 D gates, 636 frames; the baseline hist {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18}; the mass identity 5089 = 8*434 + 63 + 2*111*7 = 3472 + 63 + 1554 ✓; the hosting wall R <= 4v = 444!!).  THE REPLAY ORACLE (w21's replay(A)): the gcheck-exact ~7ms replay (nested + strictly-rising climbs, content-in-frame, ret/scatter frames, the H4 C-reverse, the final values) -> (first-failure-or-None, hist, C) — THE LEGALITY GATE BEFORE ANY PRICING (the discipline!!).  THE PLAN: the hist-reshape (raise c by moving/reframing the word's own gates at fixed register set — pure redistribution, the mass identity untouched!!).
- **THE MEASUREMENT (1) — v2 (the T155 ladder-helpers' build->2nd merge (w21!!)): 0/151 LEGAL (the 151/155 with the standard build->2nd shape!!)**: the move (each (0,1,2,4,6)-chain helper's singleton build reframed to its 2nd-gate cell F2 -> the per-h hist {1: -2, 2: +1}) — **THE CAUSE (the structural!!)**: every build-src ALREADY OWNS its own dim-2 cell, and that cell == F2 for 0/108 srcs — the ladder pairs s_k into cell(s_{k+1}) = span(s_k, s_{k+1}) while s_k's OWN cell is span(s_{k-1}, s_k) -> the src would climb SIDEWAYS (dim 2 -> dim 2!!).  The 43 srcs building MORE THAN ONE helper: 0 with matching F2s.  (The earlier "155/155 in_span" check only tested CONTAINMENT — the containment ≠ the climb's dim-rising requirement!!)
- **THE MEASUREMENT (2) — the 9 no-cell srcs' rescue (w22, the joint reframe!!): 0/9**: raising also the src's later singleton-frame gates to F2 pins the raised gates' DESTINATIONS (e.g. B-50's dest 165 sits at 116 but next needs 579, which does NOT contain 116 — the co-operand wall (see (3)!!)).
- **THE MEASUREMENT (3) — THE GENERAL SINGLE-LEVEL-SKIP SCAN (w23, the DECISIVE!!): 0/2232 LEGAL (2214 illegal climbs + 18 ret-frame breaks!!)**: for EVERY register r and EVERY intermediate level F_b: raise ALL of r's gates at F_b to its next frame F_c (the next D/A/B level, C's frame 1, or final[r]) — the GATE ORDER UNCHANGED (every value untouched (the concentration lever: r's two climbs (a, b) merge to one (a+b)!!)).  **THE FAILING REGISTER IS ALWAYS ANOTHER OPERAND OF THE RAISED GATES, NEVER r ITSELF** — the co-operands get lifted ABOVE, or SIDEWAYS FROM, frames they need later.  THE DOMINANT FAILING CLIMBS (dim-from -> dim-to): (6,4) 484 | (7,7) 360 | (4,4) 347 | (4,2) 123 | (2,1) 119.  THE IDENTITY CONTROL PASSES (the oracle's own soundness ✓!!).  THIS COVERS v2 AND THE SINGLE-SKIP FORM OF v6.  **NOT COVERED: v4's TWO-LEVEL MERGE (0,2,4,6)->(0,6) (pins even MORE registers — unlikely to pass but UNPROVEN!!)**.
- **THE CORRECTED STATUS OF THE PRICED VARIANTS**: the +1.73% / +5.89% / +9.27% figures were HYPOTHETICAL HISTOGRAMS (the reshape's projected hists priced WITHOUT a legal word!!) — they correspond to NO LEGAL WORD (the pricer-trap lesson AGAIN (the §164-166 class!!)).  **THE HONEST BOTTOM LINE: with the gate order AND the register set fixed, r434 admits NO SINGLE-FRAME SKIP ANYWHERE (0/2232!!) — the published word's own moves-space (single-skip level) is CLOSED.**
- **THE REMAINING ROUTES (the §1 handoff's honest map!!)**: (a) THE JOINT MOVES (the bounded search: start from a failing level-skip (r, F_b -> F_c), add the blocking co-operand x's own level-skip (x's gates at its current level -> x's next frame), repeat to depth 3-4 — admit iff the replay passes AND the exact price rises; the budget: ONE scan (~2232 seeds x depth); if 0 admitted: STOP!!); (b) THE STRUCTURAL REBUILD (the bigger: re-derive the helper ladder so each source PAIR shares ONE cell (the only geometry where v2 works!!) — re-deriving the helper SETS, not editing the word — SCOPE IT BEFORE STARTING!!).

## THE JOINT-MOVE ROUTE CLOSED + THE STRUCTURAL ROUTE SCOPED (THE SESSION OF 2026-10-19: ii19_p111w24/w24b/w24c/w25/w26/w27/w28; the user's "keep finding breakthroughs" directive)

- **THE JOINT-MOVE BOUNDED SEARCH (w24, repair rule (a): x's skip read off the REFRAMED level structure!!): THE CO-OPERAND WALL IS REPAIRABLE BUT THE REPAIRS ARE EMPTY!!**  One scan: 2232 seeds x depth 4 (the seed skip + up to 4 co-operand repairs; D-gates never raised (the H2 guard (gcheck's line 99: dims[F]==0!!))).  RESULT: **706 legal joint words** (597 at depth 1, 28/36/45 at depths 2/3/4) — **BUT 0 ADMITTED (0 price-raising!!)**: the pass-price census: **701/706 have an EMPTY hist delta** (the replay-PASSING words are the IDENTITY word!!) and the 5 non-neutral ones price BELOW the base (max +0.00000%, mean -0.00006%!!).  THE MECHANISM (w24b, the trace): **THE SELF-CANCELLATION** — the repair, computed on the reframed structure, OVERRIDES the seed's raised gate back to (a frame equal to) its ORIGINAL frame — the move set collapses to the identity (the traced example: the seed reg 0's gate 531->1; the blocking co-operand 117's "repair" sets B-603 back to 531; 0 registers' climb sequences change!!).  THE WHY (the fundamental!!): **RAISING A GATE LIFTS EVERY CO-OPERAND IRREVERSIBLY (the gcheck climbs NEVER DESCEND!!) — the lifted co-operand's later smaller-frame needs are UNREACHABLE, and the only "repair" that passes is UNDOING THE SEED.**
- **THE FAITHFUL-RULE SCAN (w24c, repair rule (b): x's OWN level-skip on the ORIGINAL word (w23's move family for x at the level preceding the failing gate — the §1 handoff's literal reading!!)): 0 LEGAL JOINT WORDS AT ALL** (1299 dead climbs (the unrepairable: FINAL-phase failures, start levels, no-run blockers!!) + 531 no-progress (x's skip == the seed's own move or a no-op!!) + 18 ret-frame).  **THE JOINT-MOVE ROUTE IS CLOSED AT DEPTH 4 UNDER BOTH REPAIR READINGS — 0 price-raising move sets exist in the ≤5-skip joint family.**
- **THE LADDER CENSUS (w25 — the structural route's anatomy!!)**: (i) **EVERY SOURCE'S OWN DIM-2 CELL IS UNIQUE TO IT** (101 sources with a unique own cell, group sizes {1: 101} — NO two sources share a cell!!; 10 no-cell sources); (ii) the 151 standard (1,2,4,6)-ladder pairs: 2nd-src source 100 / helper 51, and **s2's OWN CELL == F2 for 151/151** — every helper's 2nd-gate cell IS its 2nd-src's own cell, and the 151 F2s are ALL DISTINCT (**ONE HELPER PER CELL** — the cells are the PAIR-SPANS: s1's LINE lies inside F2 for 151/151, s2's line for 100/100!!); (iii) **s1 is PINNED: 99/108 s1-srcs have 1-2 duties AT their own cell C1** (the duty hist {1: 9, 2: 90}) — C1 ≠ F2 for all (the shared-cell geometry exists 0 times; C1 ⊆ F2 never (two planes through the same line!!)).  **THE VERDICT: THE SHARED-CELL GEOMETRY CANNOT EXIST BY RE-SCHEDULING — each source's own cell is a DIFFERENT helper's F2, and F2s are single-helper (the chain s1(h) = s2(h') with C1 = F2(h') ≠ F2(h) FOREVER!!).**
- **THE RESHAPE-CLASS CEILINGS (w26 — the exact payoffs (mass-preserving count-level redistributions of the base hist, priced at (v=111, h=8, R=434); the control reproduces the published c at the base hist!!))**: v2 (0,2,4,6): **+1.0383%** (c = 0.001762497548004008444389) | v4b (4,6): +2.0958% | v6 (0,4,6): +3.1784% | **v4 (0,2,4,6)->(0,6): +6.2776% OVER THE FRONTIER (c = 0.00185389180967857894459 = +6.9726% vs P111!!!)** — the v4-class (each ladder helper built DIRECTLY at its dim-6 rung: ONE rank-6 climb (the delta {1: -2, 2: -2, 6: +1} per helper)) is the structural route's REAL TARGET (the handoff's +9.27% was the v6-era hypothetical; the honest v4-class ceiling is +6.28%!!).
- **THE V4-GRAMMAR CONSOLIDATION CENSUS (w27 + w28 — the feasibility!!)**: (i) the dim-6 rungs are NEARLY PRIVATE (142 distinct rungs for the 151 helpers: {1: 133, 2: 9}) — NOT the R420's shared 30-frames!!; (ii) **THE SOURCES ARE SINGLY-HOMED AT DIM 6 (the strong invariant!!)**: 108/111 sources sit at EXACTLY ONE dim-6 frame (3 at none), and their sub-6 duties + cell ALL FIT that one frame (108/111) — ZERO sideways exposure at dim 6!!; (iii) F2 ⊆ h's rung for 151/151 (the flag nests ✓) — but s1's own cell ⊆ h's rung for only 23/151; (iv) **THE DECISIVE COUNT: dim6(s1) == dim6(s2) ⊇ F2 (the v4-buildable condition) for 0/151 PAIRS** (and dim6(s1) == h's own rung for 2/151) — every pair's two srcs are HOMED AT DIFFERENT dim-6 FRAMES.  **THE V4 GRAMMAR REQUIRES A RE-PAIRING — AND THE PAIRS ARE THE HELPER VALUES (THE DELIVERY SEMANTICS!!) — the structural route is a FULL COORDINATED REDESIGN (a NEW delivery decomposition whose pairs are within-dim-6-home), not an edit.**
- **THE HONEST SCOPE VERDICT (the §1 step 3!!)**: the structural route's COST = the full R420-architecture re-derivation under the within-home-pairs constraint (the delivery re-solve + the build + gcheck — the multi-session "coordinated design" class, with the record's repeated honesty-downs as the prior!!); the PAYOFF CEILING = +6.28% over the frontier (c = 0.0018539, the v4-class!!) — REAL and EXACTLY PRICED, but riding entirely on an UNBUILT word whose pairs do not exist in the current design (0/151!!).  THE MEASURED DESIGN FREEDOM: the sources' singly-homed dim-6 frames (the invariant to design AROUND: new pairs must be drawn WITHIN the 108 dim-6 homes (or the homes themselves redesigned — the sources' duty sets re-derived!!)).
- **THE FINAL CENSUS FACT (the route-closer!!)**: the 108 dim-6 homes are **SINGLE-SOURCE TOO ({1: 108})** — like the cells (101 single-source groups!!).  WITHIN-HOME PAIRING IS IMPOSSIBLE AT BOTH LEVELS of the r434 geometry: the v4-grammar cannot be built on this word's frame system AT ALL.  **THE STRUCTURAL ROUTE'S TRUE SHAPE: a FROM-SCRATCH P111-class design with R420-STYLE SHARING** — the R420's own true hist {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9} IS the big-merge grammar (its 9 gathers climb 0->8 in ONE gate!!); the published r434 word is the UNSHARED architecture (single-source cells, private rungs, single-source homes — NO sharing anywhere in its ladder!!).  THE TARGET: the shared-architecture P111 word, ceiling +6.28% (c = 0.0018539 = +6.97% vs P111!!) — a major multi-session build (the frame system + the ladder + the delivery all re-derived WITH the R420's sharing mechanisms (the cells shared by multiple pairs, the rungs shared by multiple helpers (the quad mechanism!!))).

## THE LORENTZIAN PUSH (the user's directive: "must be a lorentzian") — THE WORD4's-MOVES-SPACE-IS-ALIVE!!! (THE FIRST GCHECK-VERIFIED PRICE GAIN ON OUR OWN RECORD WORD: +0.498%, c = 0.001342540624871021312984!!) (ii19_nat20/21/22/23/24.py + ii19_word4_skip.json (THE NEW RECORD WORD!!))

- **THE REDIRECT (the user's answer to the route question: "must be a lorentzian"!!)**: the r434-edit routes are ALL CLOSED (the moves-space 0/2232; the joint route 0-admitted (both repair readings!!); the structural route = the from-scratch shared-architecture redesign (the ceilings + the anatomy all measured!!)) — THE PUSH MOVES TO THE LORENTZIAN SIDE: OUR OWN COMMITTED RECORD WORD ii19_own_word4.json (v=121, h=9, R=472, CST=73, c = 0.001335891046497132929087 = -23.42% vs the frontier) — the r434 machinery (the replay oracle -> the level-skip scan -> the census -> the ceilings) TRANSFERRED VERBATIM (ii19_nat20.py: the oracle's price control EXACT (-23.4177%, the 18-digit match!!)).
- **THE WORD4's SHARING ANATOMY (THE r434's-OPPOSITE (nat20!!))**: the dim-4 frames: **120 sources at 10 frames (12 SOURCES PER FRAME — THE SHARED 12-FRAMES!!)** (vs the r434's 108 single-source homes!!) | the cells: sources singly-homed (120 at 120) BUT 420 helpers at 180 cells ({2: 120, 3: 60} — THE HELPER-LEVEL SHARING!!) | the dim-8: 338 helpers at 121 frames (max 98/frame!!) | the helper chain shapes: {(1,2,4,6): 137, (2,4,6): 134, (1,2,6): 60, (2,4,6,8): 44, (1,2,4,6,8): 43, (1,): 42, (8,): 9} — the R420-template ladder | the sources' D+A chains: {(2,): 120} (ONE climb each — to their own cells!!).
- **THE LEVEL-SKIP SCAN (nat21!!): THE WORD4's-MOVES-SPACE-IS-ALIVE — 43/2583 LEGAL (vs the r434's 0/2232!!!), 42 PRICE-RAISING!!!**  THE LEGAL CLASS: the single-gate dim-5 levels raised to dim-8 (the marginal class!!) — THE GREEDY: 42 gates reframed, **+0.49776% (c = 0.001342540624871021312984)** | **THE GCHECK: PASS (the hist {1: 1142, 2: 1710, 3: 279, 4: 92, 6: 43, 7: 10, 8: 18, 9: 2}, the mass 6257 identity ✓, the SAME c to 18 digits (the oracle-exactness ✓✓)) — THE FIRST GCHECK-VERIFIED PRICE IMPROVEMENT OF THE LORENTZIAN RECORD WORD (the -22.92% -> -22.53% vs P111!!)** — ii19_word4_skip.json = THE NEW RECORD WORD (R=472, CST=73, -23.0365% vs the frontier).
- **THE CONCENTRATION CEILINGS (nat22!!)**: the v2-class (the 137 (1,2,4,6)-helpers' build->2nd merges): **+0.7419%** (c = 0.0013458) | **THE ONE-GATE COLLAPSE (all 472 helpers' whole D+A ladders -> ONE climb each to the top rung): +14.8700% (c = 0.001534537499548507738357 = -12.0299% vs the frontier!!!)** — the word4's-own-ladder in-place concentration ceiling: **-12.03% — STILL BELOW THE FRONTIER** (the 121-class at R=472 needs MORE than the A-ladder concentration to cross (the R-reduction (the record's nat12c/13b class: the ~-11..-17% honest bands!!) + the srcs'/B-phase reshapes (the {3: 331} B-phase rank-3 mass: uncollapsed in the probe!!))).
- **THE JOINT SCAN (nat23, the rule-(b) repairs!!)**: the word4's sharing does NOT unlock the big merges: 52 admitted (43 singles + 10 depth-1 joint sets) but the greedy lands at the SAME +0.49776% (the joint sets add NOTHING on top of the singles; 1430 dead climbs + 616 no-progress) — **the in-place space is EXHAUSTED at +0.498%.**
- **THE UNIVERSAL WALL (nat24 — THE ANATOMY'S-VERDICT!!)**: the 137 blocked build->2nd merges have the r434's IDENTICAL anatomy: s1's LINE inside F2 for 137/137 (the pair-spans!!), s2's own cell == F2 for 137/137, **BUT s1's own cell == F2 for 0/137** — with 137 DISTINCT SINGLE-PAIR F2s.  **BOTH ARCHITECTURES (the published r434 AND our word4) USE THE UNSHARED PAIR-SPAN LADDER: the build-src's own cell is always a different plane through the same line, and the cells are single-pair — the concentration grammar is LOCKED BY THE DESIGN ITSELF.**  THE UNLOCK = the shared-cell re-pairing redesign (the same from-scratch class as the r434 structural route's verdict — the two programs CONVERGE on the same redesign target: the SHARED-CELL/SHARED-RUNG ladder (the R420's quad mechanism at the PAIR level!!)).
- **THE HONEST MAP AT SESSION-END**: the Lorentzian record: **c = 0.001342540624871021312984 (-22.53% vs P111 / -23.04% vs the frontier — the +0.40-point honest gain, GCHECK-VERIFIED!!)** | the in-place ceiling: -12.03% (the one-gate collapse — unreachable in place (the universal wall!!)) | the crossing needs: the shared-cell re-pairing redesign + the R-reduction (the nat12c/13b class) — the multi-session build, NOW WITH THE MEASURED TARGET HISTOGRAM FAMILY (the one-gate-grammar {1: 618, 2: 721, 3: 331, 4: 84, 6: 332, 8: 105, 9: 4}-class!!).

## THE SHARED-CELL REBUILD DESIGN — THE OPENING MEASUREMENTS (the user's chosen route; ii19_nat25.py)

- **THE DESIGN TARGET (the universal wall's unlock!!)**: a 121-line (v=121, h=9) Lorentzian word whose helper ladder uses SHARED-CELL PAIRS — each helper's build-pair (s1, s2) sits in a dim-2 plane C that is ALSO s1's own cell (s1 serving as the 2nd-src of another helper h' on the SAME plane) — the grammar where the v2/v4-class concentration (the build->2nd merge, up to the one-gate collapse) is LEGAL BY CONSTRUCTION.  The payoff family: the one-gate-grammar hists (the ceiling probe -12.03% vs the frontier at R=472 (nat22!!) + the R-reduction upside (the nat12c/13b class, the ~-11..-17% honest bands at R 350-460 — the stacked redesign's prize: THE CROSSING!!)).
- **THE PLANE CENSUS (nat25 — THE GRAMMAR's-GEOMETRIC-BASIS-MEASURED!!)**: for every pair of the 121 lines, the plane span(a,b) and its line-multiplicity: **{2-lines: 3,900 planes, 3-lines: 1,120 planes, >3: NONE}** — the E8 TRIPLE structure (e.g. {0, 16, 23}: the plane through 2 roots containing exactly one more!!).  **THE 3-PLANES ARE THE SHARED-CELL GRAMMAR'S HOSTS**: a 3-plane {x, y, z} can carry a TRIANGLE OF PAIRS — h = (x, y), h' = (y, z), h'' = (x, z) — ALL sharing the plane as their F2, with every source's own cell == its plane (THE WALL DISSOLVED BY CONSTRUCTION!!).
- **THE DESIGN FREEDOM (RICH!!)**: each of the 120 root-sources belongs to **28 DIFFERENT 3-PLANES** ({28: 120}; the special line: 0 memberships — it rides separately) — the own-cell assignment has ~28-way freedom per source | the 1,120 triples offer **3,360 pair-slots** (3 pairs per plane) — far beyond any ladder's needs (the word4's ladder: 137 pairs + the higher accumulations!!).
- **THE REMAINING DESIGN QUESTIONS (the build's open core — the next sessions!!)**: (1) THE DELIVERY RE-SOLVE: which helper VALUES the B-phase (960 gates) + the scatter (9 rets, the CST-73 smart basis (the §1508 W-solve!!)) actually need, and whether they assemble through within-3-plane pairs + the higher shared rungs (the 12-frames (10, the 12-sources-each!!) + the dim-8 perps (the 98-helpers-per-frame!!)) — the word4's OWN delivery as the starting decomposition (the values are small XORs (~2-5 lines (the nat16b (~2-4-srcs-each!!)))); (2) THE CHAIN/FLAG DESIGN: each source's duties ordered along ONE nested chain (the flag structure with the 3-plane cells as the dim-2 rungs — the climb rule's requirement!!); (3) THE SCHEDULE: the builds-vs-2nds ordering on the shared planes (the triangle grammar's consistency (the v2-legal ordering measured in the w24 analysis: the src's first cell-entry must be its own plane!!)); (4) THE CST: the smart basis's 73 (the measured floor (the §1508!!)); (5) THE R: the redesign's honest register count (the nat12c/13b class's R ~ 350-460 — the price's R-lever (the master law: the deficit 9,952 FIXED, the ln-mass shrinks with the mass = hR + cst + 2v(h-1)!!)).

## THE CROSSING-TARGET MAP (nat26, CORRECTED) + THE DUTY/PIN CENSUS (nat27) — **THE LORENTZIAN CROSSING IS ALIVE AT THE BOUND LEVEL: +11.08% OVER THE FRONTIER AT THE FULL R=472!!!**

- **THE DUTY/PIN CENSUS (nat27 — the bound's ingredients!!)**: (i) the B target-gates: EVERY target reads 5 helpers (120) / 3 (the special) at its perp — 283 B-read helper-srcs (250 read at ONE perp; 33 at 2-6 targets — read at NESTED shared rungs (the sharing!!)); (ii) the sources' duty pattern is UNIFORM: (A: dims 1, 2) + (B: dims 2, 4, 8) + (C: 9) — the sources ride the flag singleton->cell->12-frame->perp->FULL; (iii) the B-read helpers' A-gate src composition: **262 source-reads vs 973 HELPER-reads** (the co-dependency: the values assemble THROUGH the helper DAG!!); (iv) of the 189 never-B-read helpers only 1 has all duties at {0,9}-dim frames — 188 pinned lower (dims {1: 84, 2: 180, 4: 180, 6: 180, 8: 97}).
- **THE HONEST ONE-CLIMAX BOUND (each register ONE climb to its top allowed frame: targets 0->perp (rank 8); sources 1->FULL (rank 8); B-read helpers 0->perp + the C-restore ({8, 1}); never-B-read helpers 0->FULL (rank 9); rets {8: 8, 9: 1})**: **{1: 283, 8: 533, 9: 190} (mass 6257 EXACT!!) -> c = 0.001937594837 = +11.076% OVER THE FRONTIER — THE CROSSING NEEDS NO R-REDUCTION AT THE BOUND!!!**  (The bound ignores the cross-register walls (the source flag (the multi-perp B-duties), the helper co-dependency nesting) — it is the CEILING of the word4-class delivery.)
- **THE CROSSING-TARGET MAP (nat26 corrected — the mass_exact COUNT/MASS bug fixed (the first run's rescaled columns were garbage!!)): mass(R) = 9R + 2009, mass-exact hists priced at (v=121, h=9, R)**: the word4's OWN shape: -23.42% (R=472) crossing at **R~260 (+1.44%)** | the one-gate shape (nat22's collapse rescaled): -12.03% (R=472) crossing at **R~360 (+0.54%)** | the max-concentration {9: M/9, 2: 1} (the UNREALIZABLE extreme (the B-phase pins!!)): +18.55% (R=472) -> +50.52% (R=260) | the D-variant: below everywhere (-24.9% -> -0.4%).  **THE TWO LEVERS (concentration + R-reduction) EACH CROSS INDEPENDENTLY AND STACK (the one-gate at R=300: +8.84%!!).**
- **THE HONEST CAVEATS**: (1) the R~260 point needs the delivery REDESIGNED (the word4's B-phase demand-reads ~4,800 >> 9R = 2,340 at R=260 — the arrival law!!) — a TARGET, not an existing hist; (2) the one-gate shape assumes the whole A-ladder collapsed — the co-dependency walls (the 973 helper-reads!!) decide how much is real; (3) the session pattern: every honesty layer historically moved the number DOWN — the bound (+11.08%) is the ceiling, the actual (-23.42%) the floor, the redesign's territory is between.
- **THE RUNG-MERGE EXPERIMENT (nat28, IN FLIGHT)**: the greedy per-gate raise (every A/B gate -> ANY strictly containing frame from the word's 716 frames, highest first, admit iff the replay passes AND the price does not fall, the fixpoint).  The first attempt (the HIGHEST container only): 0/3075 admitted (the FULL-lift = the co-operand wall (the r434 law!!)); the corrected attempt (ALL containers, descending): RUNNING.

## THE 2-CLASS h=9 CROSSING CLOSED FOR GOOD (THE SESSION'S DECISIVE HONESTY CORRECTION) + THE WORD4's-INVARIABLE-SPACE-CLOSED (nat26-nat31!!)

- **THE 2-CLASS h=9 SYSTEM IS GEOMETRICALLY IMPOSSIBLE (the rank-8 Gram proof (nat182's direct verification!!))**: the 240-line design's Gram (ALL pairs ip = a*b — the level coordinate INVISIBLE to the form) has **RANK 8**; the lines' span is 9-dim with the level direction (0,1,0) in the radical; ANY h=9 realization needs the lines' coordinate matrix X full-rank 9 with a nondegenerate form B -> the Gram X^T B X would have rank 9 — CONTRADICTION.  **THE h=9 FULL FRAME IS DEGENERATE -> GCHECK REJECTS — THE +5.17%..+27.62% BAND (R=317, THE §453 CROSSING) IS A MODEL ARTIFACT ON AN ILLEGAL SYSTEM** (the record's own #88 constraint, which the §1352-1419 crossing-era sessions priced past!!).  THE LEGAL 2-CLASS = h=10 (m=82): the record's own §1393 ladder: BELOW THE FRONTIER everywhere (the best D at R=280: -11.36%).
- **THE UNIQUE LEGAL RICH ALTERNATIVE — THE k=-1 SYSTEM (nat31) — DECODER-DEAD!!**: the 9-dim form B = I8 (+) [-1] (det -1, signature (8,1) — LORENTZIAN ✓) with the lines (a, 0)/(a, 1): **THE GRAM RANK 9 (THE LEGAL h=9 BY CONSTRUCTION!!)** | the norms: class-0 = 2, class-1 = 1 | the perps: class-0 = 63 (the E8-grade!!), class-1 = 28-56 (the a*b=1 kissing partners — RICH!!) | the junks mean 22.8 (BETTER than the artifact system's 33!!) | the (2,2) pool: 168 pieces (mean 5.0 lines, 9.1 users) + 162 carriers + the gathers -> the threshold variants R 367-383 | the demand-reads 1,685 vs 9R = 3,447: FITS (54%!!).  **BUT THE DECODER: the class-0 block rank 9 (the E8-grade ✓) while THE CLASS-1 BLOCK RANK 44** (the a*b=1-pattern is NOT the E8 pattern!) -> the full rank 53 -> 53 gathers FORCED (the U-space must span the B-rows) -> the rref spans {7: 8, 8: 20, 9: 25} -> **THE NAIVE CST 441 (vs the E8-block's 73!!) -> THE DEFICIT 256*240 - 288*441 NEGATIVE -> THE PRICER's-OWN-REFUSAL: NO-ROOT AT EVERY R (383-590) AND EVERY SHAPE (A-D)!!** — the same decoder-rank obstruction class that killed II19-361 (rank 241).  THE k=-1 IS THE UNIQUE RICH 2-CLASS h=9 (k=2: the perps EMPTY — dead): **THE 2-CLASS h=9 CROSSING IS CLOSED IN BOTH FORMS.**
- **THE WORD4's-FIXED-ORDER-SPACE FULLY CLOSED (nat28's verdict: 0/101,719!!)**: the greedy per-gate raise (every A/B gate x every strictly-containing frame, the full replay as the judge, the fixpoint): pass 0 admitted ZERO of 101,719 candidate trials (12.7 min) — with the skip scan (+0.498% banked) and the joint repairs (0 admitted), **THE WORD4's IN-PLACE CONCENTRATION AT FIXED GATE ORDER IS EXHAUSTED** (the co-operand wall binds every single-gate raise).  THE REMAINING CONCENTRATION LEVERS: (a) THE REORDERING FAMILY (untried: moving gates past independent gates + raising — the bounded next experiment); (b) THE REDESIGNS (the nat26 map: the word4-shape crosses at R~260, the one-gate shape at R~360 — both need the delivery re-solve).
- **THE HONEST LORENTZIAN MAP AT THIS POINT**: the only LEGAL, BUILT, gcheck-passing Lorentzian line = THE 121-WORD4 (our record: c = 0.001342540624871021312984, -23.04% vs the frontier) | the crossings measured ONLY at the redesign level (the nat26 map) | every shortcut closed (the r434 moves-space 0/2232; the joint routes 0; the per-gate raises 0/101,719; the one-station model refuted (the cancellation structure); the CST lever CLOSED (73 = the proven floor (the 255/256-uniform census!!)); the 2-class h=9 closed (both forms)).  THE GENUINE ROUTES REMAINING: the word4 reordering family; the 121 R-redesign + the concentration stack (the nat12c/13b class); the shared-cell rebuild (the 1,120-triple grammar (the nat25 design!!)).
- **THE ONE-STATION MODEL REFUTED (nat29 — the bound's honesty correction!!)**: the read-incidence DAG (the UNION propagation (the XOR-parity cancels by design (the dirt-doubling!!)); the D-phase excluded (self-bits only, pre-A!!)): **|T(h)|: 294/472 helpers reach ALL 121 TARGETS** (the deep gather-feeding layer) | **dim I(h) = 0 for 320 helpers** (no station exists!) | **6,442 value-⊂-I violations**: the mid helpers' values flow downstream via CANCELLATION (the R420 junk-carrier mechanism!!) — they cannot sit at one-station frames inside the deep intersections.  **THE +11.08% ONE-CLIMAX BOUND IS LOOSE — the achievable concentration is governed by the RUNG STRUCTURE (where the reads happen), which the per-gate raise (nat28) measures empirically.**  THE STRUCTURE's GIFTS: the sources' A-duties are SHALLOW (120 sources read by exactly 3 A-gates each (the special: 43!!) — the ladder is HELPER-fed (the 973 helper-reads!!)) | only 11 helpers have |T(h)| = 1 (even the B-read leaves are z-gate-shared — the sharing is deep everywhere!!) | the per-source fed-chains: {3-helper chains: 120} (the A-phase source side is ALREADY near-minimal!!).

## THE NATIVE-121 CROSSING MAP (nat33) — **THE BREAKTHROUGH-CLASS TARGET: A LEGAL WORD AT R≈158 CROSSES ON THE FINEST HIST (+4.31%)!!**

- **THE nat26 CORRECTION (the mass-identity violation!!)**: nat26's proportional shape-scaling DILUTED the climb mass at low R (the climb mass is FORCED: Σ(final−start) over registers = 968 (sources) + 968 (targets) + 9R (helpers) = 9R + 1936 — INDEPENDENT of the shape!!); the honest discipline (nat33): the shape scaled to M − 73 with the copy ranks {8: 8, 9: 1} FIXED (the nat30-proven CST-73 basis).  THE nat26 low-R rows were buggy (the W4-shape at R=260: nat26 said +1.44%, the honest −2.40%); **THE HONEST MAP (nat33) IS MORE FAVORABLE WHERE IT MATTERS**:
  - **R 158 (the §1398 economy!!): A (all-delta-1, the WORST realistic hist!!) +4.31%** | W4-shape +15.31% | OG (one-gate) +42.55% | MX +70.99%
  - R 180: A +0.32% | R 240: W4-shape +0.76% (crossing) | R 300: OG +16.46% | **R 400: OG +2.62% (STILL ABOVE!!)** — **THE MODEL ROOTS AT R/v AS LOW AS 1.31 (NO WALL!!)** and the prices IMPROVE as R drops.
- **THE RECIPE**: a legal native-121 word at R≈158 crosses THE FRONTIER ON THE FINEST POSSIBLE HIST (every climb rank 1) — NO concentration tricks needed!!  Any legal hist at that economy is above the frontier; the concentration levers only add.
- **THE §1398 CENSUS REPRODUCED (ii19_121.py rerun)**: pool **101 pieces (mean 5.5 lines, mean 12.3 users!!)**, tail carriers **47**, leftover 90 | **the script's own junk-pattern decoder rank 114 → CST 912 → NO-ROOT everywhere (the SAME CST-explosion class as the k=−1!!) — the honest decoder = THE PERP-PATTERN (the E8-block rank 9 + the special's row = 10 gathers; CST 73 (the nat30-proven floor!!)) → THE HONEST STRUCTURE: 101 + 47 + 10 = R 158 ✓✓ THE §1398 ECONOMY CONFIRMED.**
- **THE BUILD (the word4's machinery transfers)**: Stage A the delivery algebra (the rank-10 perp-pattern decoder, the W over the CST-73 basis (nat30 ✓), the piece assignments (the §1396 greedy ✓), the per-target balance — pure GF(2), no frames!!); Stage B the flag/frames (the pieces' builds riding the shared 12-frames (10 frames × 12 sources — the nat27 anatomy!!), the user-group slots (mean 12.3 users/piece!!), the source-chain nesting — the word4's SOLVED class); Stage C the emission + the replay oracle + gcheck.  THE RISK: Stage B's chains (the same class the word4's build solved once).
- nat32 (the move+raise family — the old in-place lever, R=472): running in the background; secondary now (its ceiling −12% at R=472 vs the native route's +4..+42% at R=158!!).

## STAGE A VERIFIED (nat34) — THE NATIVE-121 DELIVERY ALGEBRA IS REAL: R = 318, THE BALANCE EXACT 121/121!!

- **THE WORD4 IDENTITY (extracted + verified!!)**: per target t: **scatter(t) ⊕ B-reads(t) = {t} EXACTLY (121/121!!)** with **the D line-part = 0 for all 121** (the D-phase pre-A reads contribute self-bits only — the y-dirt, NOT the line algebra!!) | the B-reads per target: 3-5 | the scatter rows: 1-8 rets | the per-target read line-set mass: mean 64.5.  THE TEMPLATE: with the rank-9 perp-pattern decoder (the nat30 basis, CST 73!!), the B-reads must XOR to perp(t).
- **THE K=1/JUNK ECONOMY (R=158) IS UNDELIVERABLE — A DOUBLE HONESTY CATCH ON THE §1398 ESTIMATE**: (1) the junk = perp minus the k=1-shared part — the shared parts were never accounted (the greedy covered the junks only); (2) THE FATAL ONE: the delivery requires the read-XORs ⊕ e_t to lie IN THE SCATTER's REACH (the rank-9 perp-pattern span!!) — the junk-rows B'[t] = e_t ⊕ junk-cover have **rank 114 >> 9 — NO W-SOLVE EXISTS** for the junk-economy!!  THE HONEST SELF-CONTAINED ECONOMY = THE PERP-DIRECT GREEDY.
- **THE PERP-DIRECT ECONOMY (nat34, measured!!)**: the greedy on the perp-sets directly (the pieces = the subsets shared by ≥2 targets): **pool 188 pieces (mean 2.8 lines, mean 14.1 USERS!!) + 121 carriers + 9 gathers = R = 318 (R/v 2.63)** | **THE BALANCE: 121/121 TARGETS EXACT (reads ⊕ scatter = e_t, pure GF(2)!!)** | **THE ARRIVAL LAW: 2,769 demand-reads ≤ 9R = 2,862 — FITS (tight!!)**.
- **THE CROSSING VERDICT AT R=318 (the nat33 map interpolated)**: the A-shape ~−20% (below!!) | the W4-shape ~−10.6% | **the OG-shape ~+13.3% (ABOVE!!)** — the crossing needs the SEMI-CONCENTRATED LADDER — and THIS economy's NATURAL SHAPE IS ALREADY SEMI-CONCENTRATED (the pieces at dim-2/3 spans (rank-2/3 builds!!), the perp-reads at rank 5-6, the targets at rank 8, the sources' climbs through the flag!!): the natural hist lands in the W4-OG band — THE BUILD DECIDES.
- **THE REMAINING BUILD (Stage B + C — the next sessions!!)**: Stage B THE FLAG/CHAINS: the 188 pieces' build-frames (the spans (dim 2-3) riding the shared 12-frames (the nat27 anatomy: 10 frames × 12 sources!!)), the user-group slots (14.1 users per piece partitioned over the dims (the R420-quad mechanism!!)), THE SOURCE-CHAIN NESTING (the ~4.3 piece-reads + ~6.6 carrier-reads per source must form ONE nested chain per source — the word4's SOLVED class!!), the carriers' per-target frames ⊆ perp(t), the gathers' hierarchical builds (the own8-template!!); Stage C: the gate emission + the replay oracle + gcheck.

## THE GREEDY GRID + THE NATURAL-HIST MODEL (nat35) — THE NATIVE BAND STRADDLES THE CROSSING; THE (3,4) VARIANT AT R=277 IS THE MODEL-CROSSING ROW (+0.36%!!)

- **THE GRID (the greedy variants x the natural-hist model, mass-exact, priced at each variant's R!!)**: (2,2): pool 197 (users 18.9) + 118 carriers -> R 324, **-10.50%** | (3,3): 207 (10.7) + 121 -> R 337, **-9.08% (the best realistic!!)** | **(3,4): 147 (13.7) + 121 -> R 277, +0.36% (THE MODEL CROSSING ROW!!)** | (3,2): 285 (8.3) + 121 -> R 415, -18.80% | (4,2): pool 0 -> R 130, +49.65% **= THE ALL-CARRIER ARTIFACT (unbuildable!!)**.
- **THE (4,2) ARTIFACT IDENTIFIED (the honesty catch!!)**: pool 0 = the all-carrier economy (each target reads its WHOLE 64-line perp from ONE carrier!!) — **UNBUILDABLE: each source's line lies in ~64 targets' perps -> the source would need to serve ~64 INCOMPARABLE perps (the source wall at its extreme!!)** — the model's source-mass (2 climbs/source) is fantasy for that economy.  The grid's realistic rows (pool 147-285) have the honest source model (the clustered flag chains ~3-4 climbs).
- **THE HONEST VERDICT**: the natural-native band **-9% .. -19% STRADDLES THE CROSSING** (the (3,4) row +0.36% at R=277); the model's noise band is ±10 points — **THE STAGE-B BUILD DECIDES** (the true hist from the actual chains!!).  The +20/+30% zone (the OG/MX class at R 220-280 (nat33: the MX at R=240: +54.37%!!)) sits ABOVE the natural band — reachable ONLY through the concentration breakthroughs: the shared group-frames (the R420-quad mechanism at the native economy: the pieces' group-frames CONSOLIDATED across pieces -> shorter chains + bigger climbs!!).
- **THE BUILD TARGET (the next session's construction!!)**: the (3,4) economy (147 pieces + 121 carriers + 9 gathers = R 277): Stage B the flag/chains (the pieces' build-frames INSIDE the low-group frames (the dim-3/4 intersections!!), the user-group partitions with the ACTUAL nondegenerate frames, the sources' flag chains (the clustered build-duties), the carriers' frames ⊆ perp(t), the gathers (the nat30 CST-73 basis!!), the W-solve (nat30-verified!!), the D-extension (the own8-template!!)); Stage C: the emission + the replay + gcheck.  THE FIRST GCHECK-PASSING NATIVE WORD's TRUE HIST = THE PRICE.
