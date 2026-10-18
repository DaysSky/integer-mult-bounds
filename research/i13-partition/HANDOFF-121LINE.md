# THE HANDOFF PROMPT: THE 121-LINE II19 WORD — THE FIRST PRICEABLE II19-FAMILY WORD; THE COMPLETENESS FIX + THE FRONTIER QUESTION OPEN

(Read this file fully; it is self-contained. The running record is
`research/i13-partition/SESSION-SUMMARY.md` — the last three blocks cover this arc.)

## 0. THE FIRST ACTION (the concrete opener, ~5 minutes)

Reproduce the state before anything else:

```bash
cd /Users/dayssky/integer-mult-bounds
~/.venv/bin/python3 research/i13-partition/ii19_ext6.py && \
~/.venv/bin/python3 research/lorentzian-frame-cell-handoff/code/tword/gcheck.py \
  research/i13-partition/ii19_ext_word2.json --price
```

Expected: the ext6's replay prints `THE FINALS: the fails 0` and `the mass 6186 vs the
identity 6186: MATCH!!`; the gcheck prints `"status": "PASS"`, `R: 463`,
`"bit_c_nine_stage": "0.0009559892732842554615227"`,
`"vs_P111_percent": -44.83784565508706`. If both reproduce, continue to §5.

## 1. THE MISSION (the context, 6 lines)

The integer-multiplication-bounds program's bit-side frontier sits at the E8 words:
P111-tuned c = 0.001733427 (the reference), R434 c = 0.001744386 (+0.57%), E1 c =
0.001734473; R420 c = 0.001653827 (its true hist {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9},
mass 5112). The Lorentzian program's goal: a word for a Lorentzian-embedded system
(II_{1,9} = E8 ⊕ hyperbolic) whose TRUE c beats the frontier. Every other system examined
is closed by measurement (I8-I13 by exact-cover/census screens; II19 full-361 by decoder
rank 241; the 2-class 240 by the h=10 degeneracy; II19 level-2 by the hosting wall
Σc_t 9,570 vs 4,851). The 121-line system is where words have now been BUILT, GCHECK-
VERIFIED, and (one of them) PRICED.

## 2. THE HEADLINE (where the last session left off)

THE 121-LINE SYSTEM (120 E8 roots + the special line (0,...,0,1), norm 2, orthogonal to
all 120 roots; span dim 9; h=9; the form diag(1^8, 2); v=121; m=73) HAS TWO BUILT,
GCHECK-PASSING WORDS:

1. `ii19_ext_word.json` (built by `ii19_ext4.py`, R=541): 120 per-target carriers.
   GCHECK PASS. HOSTING-WALL REJECT (nres 4869 vs cap 4356 = 111.8%) — unpriceable.
2. `ii19_ext_word2.json` (built by `ii19_ext6.py`, R=463): **42 SHARED CARRIERS (the
   D4-frame sharing!)**. GCHECK PASS. **THE PRICER PRICED IT: c = 0.0009559892732842554615227
   = −44.84% vs P111 — THE FIRST TRUE c FOR ANY II19-FAMILY WORD.**

The ext6's true hist: {1: 1091, 2: 1709, 3: 331, 4: 144, 8: 9, 9: 4}; CST 83; mass
6186 = the identity (9·463 + 83 + 2·121·8); gates {D 121, A 2107, B 957, C 2704};
moves 3278; rho 3.826; mass/v 51.1 (vs the R420's 42.6).

## 3. THE ARTIFACTS

- `research/i13-partition/ii19_ext4.py` — the R 541 word builder (the 6-fix iteration's
  history; the fix-7's ret_frames truth = CST 83).
- `research/i13-partition/ii19_ext6.py` — **THE CURRENT BEST WORD BUILDER** (the census
  core + the 42 shared carriers + the order-aware insertion + the replay + the emission).
  READ THIS FIRST — it is the complete build recipe.
- `research/i13-partition/ii19_ext5.py` — the shared-carrier census (the cell-level
  sharing is ZERO — all 120 targets read DISTINCT dim-2 cells; the D4-frame candidates
  give the 42-group covering: groups {6:3, 5:4, 4:6, 3:10, 2:9, 1:10}).
- `research/i13-partition/ii19_ext_word.json` / `ii19_ext_word2.json` — the two words.
- `research/e8-bit-r420/data/bitE8mut-r420.json.gz` — the R420 source word. Its frames
  are LINE-INDEX LISTS (line-counts: {0:1, 120:1 (FULL, index 1), 1:120 (singletons,
  indices 2..121), 2:180 (cells), 12:70 (D4s), 30:180 (D6s), 63:120 (perps)}); its
  'form' key is a STRING TAG, not a matrix — use the plain dot product; its scatter rows
  deliver the B[t]-totals ({t} ∪ perp(t) patterns).
- `research/lorentzian-frame-cell-handoff/code/tword/gcheck.py` — the checker.
- `research/lorentzian-frame-cell-handoff/code/price/pricer.py` — the pricer
  (price(local, v, h, R): L = 2K+1 = 9, m = 1+9(h−1), nres = R·9 vs cap = 36v).
- `research/i13-partition/SESSION-SUMMARY.md` — the running record; the last three
  blocks are this arc. Earlier lorentzian context is in the older blocks.

## 4. THE HONEST LEDGER (read before building anything)

1. **THE PRICE IS BELOW THE FRONTIER**: c = 0.000956 = −44.84%. The frontier needs
   ~1.8×. Mechanism: mass/v 51.1 vs the R420's 42.6 (+43 R, +11 CST, +1 line). The
   architecture's floor: R ≥ 420 (the R420's published core) + 1 (the odd-gather) + m
   (the covering number; greedy gave 42, the LOWER BOUND is unmeasured).
2. **THE SPECIAL's COMPLETENESS GAP — A CORRECTION IS OWED**: the special target's
   junk = {120} ONLY — the 120 (root, special) orthogonal pairs are NOT realized; the
   special's y-column computes a COPY (the diagonal pair only), not the incidence sum.
   The committed record (SESSION-SUMMARY, the fe6301f9-era block, and the commit
   message) claims "COMPLETENESS HOLDS: junk(t) ⊇ perp_121(t) for all 121 targets" —
   that is WRONG for the special's column (the roots' columns ARE complete). gcheck does
   NOT verify the multiplication (the identity-word counterexample, SS1150); it verifies
   the flow. The word is: FLOW-VERIFIED, ROOTS-COMPLETE, SPECIAL-COLUMN-INCOMPLETE.
   THE FIX-PATH is §5 step 1.
3. **THE WALL MARGIN**: R 463 vs the wall 484 (R ≤ 4v; cap 36v, nres 9R) — the +21
   registers of room, enough for the completeness fix's reads.
4. **THE HOSTING WALL (the measured law)**: nres = 9R ≤ cap = 36v ⇒ R ≤ 4v. The R 541
   (4.47v) was rejected; the R 463 (3.83v) passes at 95.7%.

## 5. THE NEXT STEPS (ranked)

1. **THE SPECIAL's COMPLETENESS FIX** (honest-critical, small — do this first):
   (a) CENSUS: is the (v_0 ^ all-roots)-pattern in the scatter-rets' span? The special's
   scatter-row must deliver (all-roots ^ e_120) so junk ⊇ perp(special) = the 120 roots.
   Enumerate the 2^10 combos of the 9 u_k + the odd's x-part (the odd's x-part =
   v_0 ^ e_120 by construction).
   (b) READS: the special's B-gates at E8-internal frames on its chain (its chain is
   confined to the 120-roots-span!): find R420 helpers whose contents XOR to the
   all-roots pattern — a GF(2) solve over the helpers' line-contents (~2000 helpers ×
   120-bit space), legality-filtered (frames must nest along the special's chain).
   (c) RECOUNT: R 463 + the fix's registers ≤ 484 ✓ (+21 margin).
   (d) REBUILD → GCHECK → COMPLETENESS CHECK (junk(t) ⊇ perp(t) for ALL 121!) → TRUE c.
2. **THE COVERING's LOWER BOUND** (decides the architecture's floor): the m = 42 is the
   greedy's; compute the LP/combinatorial lower bound over the D4-frames' served sets.
   R_min = 421 + m_lb. Then run the pricer at the R grid (441–484) with the ext6's hist
   shape → the c(R) curve → the honest frontier-reachability verdict for this
   architecture.
3. **THE PRICE SENSITIVITY**: the R420 at R 434 (v 120) prices +0.57%; the 121-line's
   structural extra (+1 line ⇒ +29 R net + 11 CST) suggests the frontier is NOT
   reachable at this architecture — but the pricer grid measurement is the decisive
   check, not the estimate.
4. **IF THE 121-LINE CLOSES AT THE PRICE**: (a) THE E8 LEVER A (the handoff's "only
   remaining lever": a middle strictly more efficient than R420 per incidence — to be
   demonstrated on E8 first, where it moves the frontier itself); (b) the fresh-system
   search with the census screens as the reusable methodology.

## 6. THE BUILD RECIPE (the ext6's 10 sections — the reusable template)

(0) LOAD the R420; build V9 = the 120 lines + [0]*8+[1]; V=121, H=9, R=463.
(C1) CENSUS: prior-spans = each target's LAST non-perp B-gate frame (all 120 are
     DISTINCT dim-2 cells); served(X) = {u : P_u ⊆ X as sets AND every line of X ⊥ u};
     greedy over the R420's dim-4/6 frames → the 42 carrier groups.
(1) FRAMES: re-based (add the special to the FULL and the 63-perps → the 64-line
     dim-8 frames); + IDX_SPS (the {120}-singleton); + IDX_R8 (the 120-roots, dim 8);
     + the m F_j = sorted(X ∪ {120}) (13-line dim-5). LCDIM = {0:0, 1:1, 2:2, 3:3,
     12:4, 13:5, 30:6, 64:8, 120:8, 121:9}.
(2) REGISTERS: remap (sources +0, targets +1, helpers +2); ODD = 2V+421−1 = 662;
     CARR[j] = 663..704.
(3) START/FINAL: sources start at their singleton frames (indices 2..121); the special
     starts at IDX_SPS; targets final = the re-based perp frames; the special's final
     = IDX_R8.
(4) GATES: remapped R420 gates; the rets' F==1 gates re-targeted to IDX_R8 (copy ranks
     8); the 42 carriers' A-builds [IDX_SPS, CARR[j], [SP]] (val = own-dirt ^ {120});
     THEN the odd's A-build [IDX_FULL, ODD, row-0-rets + [SP]] (its x-part = v_0 ^ e_120);
     D-gates: +ODD on all, the special's NEW D-gate [0, V+SP, [ODD]], and each root
     target's D-gate gets +CARR[j_t]; THE ORDER-AWARE B-INSERTION: for each target's
     non-perp B-gate, append the gate THEN [F_IDX[j], V+t, [CARR[j]]] — the carrier
     read goes BETWEEN the cell-gate and the perp-gate.
(5) SCATTER: roots' rows = R420's row + row-0 + [9] (GF(2)-collapsed: duplicates cancel);
     the special's = [9] + row-0; ret_frames = the FIX-7 TRUTH: the row-0 rets and the
     odd at IDX_FULL, the other 7 at IDX_R8 → CST 83.
(6) C: the H4 literal reverse of the z-gates (the A+B gates with non-target dests), all
     at IDX_FULL.
(7) REPLAY: climb (cur == F ⇒ FREE; hist[Δdim] += 1); phases D → A → scatter → B → C →
     final climbs.
(8) FINALS' CHECK: want = (1 << r) ^ (1 << (r−V)) for targets, else (1 << r).
(9) HIST/MASS: mass must equal H·R + CST + 2V(H−1).
(10) EMISSION: the word JSON (form num = diag(1^8, 2), den 1; lines = V9; frames as
     VECTOR LISTS; start/final/D/A/B/C/ret/ret_frames/scatter).

## 7. THE MECHANISMS DISCOVERED (the reusable levers)

- **THE D4-FRAME SHARING**: a carrier at F = {120} ∪ (a D4-subsystem) serves every
  target whose prior-span (cell) lies inside the D4 AND who is orthogonal to all its 12
  lines. The greedy covering gave 42 carriers for 120 targets.
- **THE FRAME-INDEPENDENCE OF THE CLIMB MASS**: a register's climb mass = final dim −
  start dim; intermediate visits are MASS-FREE. Inserting shared frames into chains
  costs nothing.
- **THE FREE SAME-FRAME RE-READS**: cur == F ⇒ no climb, no mass — the carrier is read
  by many targets at its ONE frame for free.
- **THE ONE-CLIMB-PER-SOURCE LAW**: same-dim frame jumps are ILLEGAL (a source read at
  many different perps needs per-target channels; shared carriers at common frames are
  the legal sharing).
- **THE ORDER-AWARE INSERTION**: per-register frames must strictly increase; appending
  at the end can create DECREASING climbs (the ext4's carriers-at-the-end would have
  been dim-8 → dim-5 = illegal; that is why the ext6 inserts between cell and perp).
- **THE CONTENT-FRAME CHECK**: only the SRCs' contents must lie inside the gate's
  frame; the dests' contents are NOT checked (the targets may hold y_t bits at frames
  not containing t).
- **THE CARRIER-AS-CHANNEL PATTERN**: the special's x reaches the roots' reads ONLY via
  carriers built at the {120}-singleton then climbing to a shared frame — the
  {120}-span is not inside any E8-internal frame.

## 8. THE VERIFICATION DISCIPLINE (the hard-earned rules)

1. gcheck is NECESSARY-NOT-SUFFICIENT: it verifies the flow (nondegenerate frames,
   nested+increasing climbs, src content-frames, the H4 reversal, the mass identity,
   the finals, the retained frames' consistency, the scatter at frame-0) — NOT the
   multiplication's completeness. The completeness check is SEPARATE: for EVERY target
   t, junk(t) = (the scatter's delivered x-pattern ∪ the reads' x-contents) minus {t}
   must ⊇ perp(t). The identity word passes gcheck while computing only a copy.
2. The hosting wall: nres = 9R ≤ cap = 36v ⇒ R ≤ 4v; the pricer REFUSES over-wall
   words ('hosting wall' error). Price nothing that has not passed the wall.
3. Truth-pricing only: price at the TRUE hist (replay/gcheck-extracted), never model
   bands (the model bands overstated by 1.19–1.57× in earlier sessions).
4. Honest corrections: wrong claims get retracted and corrected in the record (the
   §1150/§1301 precedent). Never leave a false claim committed.
5. The special line's semantics: perp(special) = all 120 roots — the special's column
   needs ALL 120 products; the special's chain is confined to the 120-roots-span (it
   can only read E8-internal registers).

## 9. THE STANDING DIRECTIVES (the user's, from the last sessions)

- "whatever it takes. keep pushing the frontier" / "keep pushing II19" / "keep finding
  breakthroughs on lorentzian" / "keep going for II19 there is still potential" /
  "keep going" / "context is NOT LOW — ASSUME IT'S INFINITE".
- The user values honest negatives as much as breakthroughs; every claim must be
  verified at the deepest layer available before being recorded.
- Session convention: results are recorded in SESSION-SUMMARY.md and committed+pushed
  (standing permission for commits in this research branch: claude/jolly-noether-*).
- Do not ask whether to continue; the directives above are the standing answer.

## 10. THE RECORD (the convention)

Append findings to `research/i13-partition/SESSION-SUMMARY.md` in the established style
(the `## THE ...` blocks with the SS-numbered references), then commit+push with the
full findings in the commit message. Keep the honest ledger current — especially the
owed correction of the completeness claim (§4.2 above) the moment the fix or the
correction is verified.
