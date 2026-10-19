# A better Lorentzian word: the r434 frontier lifted into II_{1,9} (2026-10-19)

Prepared for DaysSky with assistance from Claude. It follows `AUDIT.md`, `BREAKTHROUGH-MAP.md` and
`SCREEN-REACH.md`.

## Result (verified)

`lorentz_r434_lift_best.json.gz` passes the unmodified `gcheck.py --price`:

| quantity | value |
|---|---|
| system | P111's 111 lines + one special line of norm −2, h = 9, form diag(1^8, −2) (signature (8,1); E8 + ⟨e − f⟩ inside II_{1,9}) |
| v, R, cst | 112, 434, 64 (10 totals) |
| histogram | {1: 1239, 2: 995, 3: 463, 4: 31, 5: 54, 6: 87, 7: 20, 8: 11}; mass 5762 = 9·434 + 64 + 2·112·8 |
| c (nine-stage) | **0.001533132530491818482343** |
| vs the frontier r434 (0.0017444) | **−12.11%** |
| vs the record's best Lorentzian word (W4 tuned, −22.98%) | **+10.87 points** |

## Construction (`lift_r434.py`)

1. **Base.** The frontier's own middle: the r434 word in the record's gcheck format
   (`ii19_pub2_p111-r434.json`).
2. **Decoder.** The special decodes as an orthogonal singleton total (`AUDIT.md` E1): cst 63 + 1.
3. **The lift.**
   - A set U of r434 frames carries the special direction (F → F ⊕ ⟨sp⟩).
   - U contains the full frame and every target perp. It is closed upward along every register's chain.
   - U excludes the source singletons, frame 0, the totals' frames and everything below them in the
     totals' chains.
   - Every old register then gains exactly +1 rank, once.
4. **Placement.** Optimized greedily for the price. The minimal U gives −12.77%, the maximal U −12.15%,
   and the greedy optimum −12.11%. So placement is worth ≤ 0.7 points; the rest of the cost is the
   window's mass penalty (`BREAKTHROUGH-MAP.md` §4).
5. **The special's registers.** The special source sits at ⟨sp⟩ (its retained total). The special
   target reads only that total and ends at sp^⊥ = E8.

## Validity scope

- **Format: valid.**
  - gcheck checks the frames' nondegeneracy, nested climbs, content-in-frame, the F2 semantics on all
    columns, H1–H5, the H4 reversal and the mass identity.
  - The decoder is valid under the community's definition: B_tt = 1, B_ts = 0 on non-orthogonal pairs,
    free otherwise (HANDOFF lines 1068 and 1442; sparse rows allowed).
- **The record's stricter "junk completeness" criterion is not met** on the 112 (root, special) pairs.
  - Root targets never see x_sp, and the special target never sees the roots.
  - The record retracted "completeness forces B = B0" itself (SS1515) but later used the criterion
    again.
  - Completing it here is blocked cheaply: 92 of the 111 targets' first frames are cells inside the
    totals' build chains, so they cannot carry the special direction.
  - Carriers (the record's ext6 route needed 42) would push R past the hosting wall 4v = 448.
  - The W4 meets the criterion at −22.98%.
- **Lorentzian in the strict sense.** The ambient form and the lines' span have signature (8,1). The
  special line is decoupled (orthogonal to every root), as in the record's 121 family.

## Pushing further: what was tried on the r434 middle

The remaining 12.1% is the h = 9 penalty. Since signature does not enter the price, a frontier Lorentzian
word needs an E8 middle about 14% better than the r434's. Two mechanical trims were measured:

| mechanism | census |
|---|---|
| inline a private wire into its target (`inline_census.py`) | 0 / 225 wires inlinable: every wire absorbs a register reused later; only 38 are frame-compatible |
| delete a single-read helper by letting its reader absorb its inputs (`helper_inline_census.py`) | 4 single-read helpers, all blocked; 341 of 429 helpers are read ≥ 4 times |

- **Target-side structure.** Every target reads a source at its cell, a source at t^⊥, and 2 strictly
  private wires (13–26 lines each). That is the 3-slice floor for covering E7.
- **Conclusion.** The r434's middle is fully shared, which matches the record's "merge-optimum of its
  grammar". The record's nat134 A-DAG flattening (R ≈ 243) has no recorded outcome, and its
  recomposition is reported to fail.

## Open next questions

1. **E8 lever A at h = 8** (a middle about 14% better than r434).
   - Relevance: transfers to this word at a roughly constant −12% offset; the only route to a frontier
     Lorentzian word in the current format.
   - First step: the record's R ≈ 350 target at the r434 shape. That means roughly one private wire per
     target, with the target's own chain carrying a 6-dim slice.
   - Blocker: a new A-DAG to feed the slices.
2. **Format levers.**
   - The cut-format double star is about +10 points on the lifted family.
   - Idle slots without a bridge split are +5.2 points; they lift E8 too.
3. **Completeness.** Settle whether the outer pipeline needs the (root, special) pairs. If it does, a
   design with cheap special carriers under R ≤ 4v is needed.

## Reproduce

```sh
python3 lift_r434.py --emit lorentz_r434_lift_best.json   # greedy placement, ~30 min; prints min/max/best
python3 ../../lorentzian-frame-cell-handoff/code/tword/gcheck.py lorentz_r434_lift_best.json.gz --price
python3 inline_census.py; python3 helper_inline_census.py
```
