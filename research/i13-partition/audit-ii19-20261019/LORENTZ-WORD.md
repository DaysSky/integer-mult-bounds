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

## Above the frontier under one format extension: hyperplane-ended cleanup (verified in the extension)

`lorentz_r434_hpe.json.gz` (`hpe_lorentz.py`) is the r434 frontier embedded in the same II_{1,9} system.

- **Construction.**
  - Its whole helper network stays inside the hyperplane U = sp^⊥ = E8, which contains every helper's
    content.
  - Every helper ends at U, and the cleanup C (the literal reverse) runs at U.
  - Only sources (U → full₉) and targets (t^⊥_E8 → t^⊥_E8 ⊕ ⟨sp⟩) step into the special direction, each
    by one rank-1 climb.
- **Checker.** `gcheck_hpe.py` is `gcheck.py` plus one optional key, `hyperplane_end = U`:
  - helpers end at U and C runs at U;
  - the mass identity becomes (h−1)R + cst + 2v(h−1);
  - helper residuals are hosted at width h − 1.
  - The diff is 24 lines. Without the key it reproduces gcheck exactly: r434 c = 0.0017443859508 and the
    lifted word above, both checked.

| check | result |
|---|---|
| `gcheck.py` (current format) | REJECT: final full frame (helpers end at U) |
| `gcheck_hpe.py` | PASS; hist {1: 1534, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18, 8: 2}; mass 5328 = 8·434 + 64 + 2·112·8 |
| nine-stage c | **0.001764387789905888286536 = +1.147% vs the frontier** |
| seven stages (hostable now: width-8 residuals fill 8k slots) | 0.0017686125 = +1.389% |

**Mechanism.**

- At h = 9 the idle windows have capacities 8, 16, 32 and 48, and the helpers keep their h = 8 width 8,
  so every residual packs exactly (`bit589-width-packing`'s width lever).
- The idle remainder becomes 357 whole rank-48 slots per replica, with no fragments.
- The ports pay the extra dimension: 222 rank-1 climbs, the special line, and m = 73.

**What this is and is not.**

- **Not a Lorentzian advantage.** Signature is price-invisible: a +2 special line gives the same word and
  price. The ingredient is a decoupled extra dimension, so that one hyperplane holds the entire helper
  network.
- **Not available to E8 at h = 8 in this form.** No hyperplane contains all E8 helper contents.
  Per-helper hyperplane ends or rank-one entrances are different extensions. `bit589-width-packing` prices
  them at up to +17–23% for E8 if every helper converts.
- **Proof obligation (open).**
  - The precedent, `research/hyperplane-end-lean`, proves Lemma A with a hyperplane terminal frame for
    complex-side helpers with a single cleanup gate, under an exact factorization (N) per (E, U) pair.
  - This word needs the bit-side analogue for all 434 helpers, with their full literal-reverse cleanup
    at one hyperplane.
  - It also needs the bit-side window-timing check that `bit589-width-packing` lists as not done.

## Stacking levers on the extension word (measured, 2026-10-19)

- **Other bases.** Under the extension the lift ≈ its h = 8 base + 1.2 points, and the bases keep their
  order: r434 +1.15%, P111-tuned +0.47%, R420 −4.05%, R480 −7.92%. R480's local histogram was
  recovered from its published nine-stage profile and reproduces its c exactly. So r434 is the right
  base, and middle gains transfer about one-for-one.
- **Value of a helper.** Each helper removed at the r434 shape is worth about +0.15%:

  | R | 409 | 384 | 359 | 334 | 309 |
  |---|---|---|---|---|---|
  | 9 stages | +4.6% | +8.3% | +11.9% | +15.6% | +19.5% |
  | 7 stages | | | +12.2% | | +20.7% |

- **Rescheduled inlining** (`inline_resched_census.py`).
  - Test: the target reads a wire's inputs itself in phase B at their scatter-time frames.
  - Result: 0 / 225 wires. 180 read registers that change afterwards (the r434's running-sum
    accumulators are read mid-accumulation), and 42 fail the flag condition.
  - With the two earlier censuses, no mechanical trim of the r434 middle exists.
- **Scope rules.**
  - Idle slots without a bridge split: the extension word goes to +2.23%, r434 itself to +6.20%.
  - Seven stages: +1.39%.
  - Each rule lifts E8 at least as much as the Lorentzian word.

- **Target-side slice geometry** (`slice_cover.py`, exhaustive over normals from the E8 roots and norm-4
  vectors). κ(E7) = 3, and the only 3-covers are D6 triples. Fixing an E6 slice (shareable by an A2's 3
  targets) forces 4 slices in total. A shared D6-sum per orthogonal target pair saves at most 0.5 wires
  per target, about +8%, and its feeding network faces the nested-chain bottleneck that pinned every
  earlier design.
- **E1-style entrance helpers** (`entrance_census.py`; mechanism of `research/e8-bit-p111-e1`, accepted by
  the official C++ checkers).
  - Width 8 − rank; rank-1 entrances fill the 7k slots, which `bit589-width-packing` prices at +3.2% for
    37 helpers and +6.7% for 74.
  - On the r434: 1 of 434 helpers converts. 225 are target-read wires, 199 have a reader that cannot make
    the early dirt read, and 9 are totals.
  - The lever is real, but this middle admits it once, as on P111.

**Where that leaves a significant gain.** It needs a new middle with about 60 (for +10%) to 125 (for +20%)
fewer helpers at the r434's shape (E8 lever A). The same middle lifts the E8 frontier by about the same
amount.

## Open next questions

1. **Bit-side hyperplane-ended cleanup.**
   - Relevance: decides whether `lorentz_r434_hpe` (+1.15%) is a frontier word. The same construction
     applies to any E8 word lifted by a decoupled line.
   - First step: state (N) for (E, U) = (0, sp^⊥) in the bit labels and check it against the
     `hyperplane-end-lean` template.
   - Blocker: H4 is the obstruction both here and in `bit589-width-packing`.
2. **E8 lever A at h = 8** (a middle about 14% better than r434).
   - Relevance: transfers to this word at a roughly constant −12% offset; the only route to a frontier
     Lorentzian word in the current format.
   - First step: the record's R ≈ 350 target at the r434 shape. That means roughly one private wire per
     target, with the target's own chain carrying a 6-dim slice.
   - Blocker: a new A-DAG to feed the slices.
3. **Format levers.**
   - The cut-format double star is about +10 points on the lifted family.
   - Idle slots without a bridge split are +5.2 points; they lift E8 too.
4. **Completeness.** Settle whether the outer pipeline needs the (root, special) pairs. If it does, a
   design with cheap special carriers under R ≤ 4v is needed.

## Reproduce

```sh
python3 lift_r434.py --emit lorentz_r434_lift_best.json   # greedy placement, ~30 min; prints min/max/best
python3 ../../lorentzian-frame-cell-handoff/code/tword/gcheck.py lorentz_r434_lift_best.json.gz --price
python3 inline_census.py; python3 helper_inline_census.py
python3 hpe_lorentz.py lorentz_r434_hpe.json && python3 gcheck_hpe.py lorentz_r434_hpe.json --price   # extension word
```
