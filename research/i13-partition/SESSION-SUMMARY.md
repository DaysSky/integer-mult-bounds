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
