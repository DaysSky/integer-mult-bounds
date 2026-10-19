# II19 audit (2026-10-19): errors in the current findings and what they unlock

Scratch audit of `research/i13-partition` (the II19 / Lorentzian arc), prepared for DaysSky with
assistance from Claude. It does not edit `SESSION-SUMMARY.md` or `HANDOFF-121LINE.md`; the corrections
are recorded here. Labels: **verified** (exact computation in this directory, unmodified pricer and
gcheck), **model** (exact pricer applied to a transplanted histogram, which is not a word), **open**.

## Bottom line

Several II19 closures rest on a wrong decoder statistic. Correcting it **raises the II19 ceiling by 7–8
points** at the record word's own middle shape (8.4 at R/v 3.9; 7.2 at the hosting wall). It also turns the record word into a genuinely
Lorentzian word at no cost. **No correction found here yields a frontier-crossing II19 word by itself.**
The binding constraint is the window penalty, quantified in §3. At h = 9 a frontier-quality middle
needs a decoder cost per line x ≤ ~0.51. The best in-format II19 decoder is 64/112 = 0.571.

## 1. Errors, ranked by effect on II19's c

### E1. "The special kills the span-7 window" is false (verified, largest effect)

- **Claim:** SESSION-SUMMARY:1909–1910 and :1885 say the 121 family is capped at deficit 9,952, so
  "the only lever left = the R".
- **Error:** `ii19_121sub.py` takes decoder totals from codewords of rowspace(B0). Every root is
  orthogonal to the special, so every B0 root row contains the special, and no codeword spans 7.
- **Correction:** the (root, special) entries are free in the decoder (HANDOFF 1068). A block-diagonal
  decoder (the punctured E8 totals plus a singleton total for the special) is valid.
- **Verified (`audit_decoder112.py`):**
  - The r434 frontier word's own decoder was extracted by replay: 9 totals at dimension 7, cst 63,
    zero violations.
  - Adding the special as a singleton total gives a valid decoder for the 112-line system
    (P111's 111 lines plus the special) in 9 dimensions.
  - Its frames are nondegenerate and its contents lie in their frames, for special norm +2 and −2.
  - Result: **cst 64, deficit 10,240**. The record's method on the same 112 lines finds only
    span-8/9 codewords (cst ≥ 72, deficit ≤ 7,936).
- **Price (model, `audit_ladder.py`), W4-tuned shape:**

  | R/v | 121 lines (record, cst 73) | 112 lines (cst 64) |
  |---|---|---|
  | 3.90 | −22.98% | **−14.59%** |
  | 3.50 | −18.60% | −9.53% |
  | 4v wall | −24.09% | −15.75% |

- **Caveat:** in E8, puncturing 9 lines raised R/v (R420 3.5v to P111 3.95v; the transplant reproduces
  the published +4.79% as +4.12% at the achieved R). The 112-line wall is R ≤ 448, so the realized gain
  depends on building it under 448.

### E2. Decoder floors computed from a fixed pattern (verified, systemic)

A decoder is any F2 matrix with B_tt = 1 and B_ts = 0 on non-orthogonal pairs, and free on orthogonal
pairs. Cost is the sum of the retained-frame ranks. Three facts follow directly:

- **(a) free entries:** rank(B0) is one completion's rank. It is not a lower bound.
- **(b) singleton:** cst(S ∪ {ℓ}) ≤ cst(S) + 1 for any non-null line ℓ.
- **(c) orthogonal sum:** if T ⊥ S, then cst(S ∪ T) ≤ cst(S) + cst(T).

The only general lower bound used here is the size of a pairwise non-orthogonal set, which forces an
identity block. Places where the record used rank(B0), rowspace(B0) or an arbitrary basis as a floor:

| place | record verdict | corrected status |
|---|---|---|
| `ii19_fresh1.py:15` (rho screen) | "E8⊕U family closed at the rho-level"; rho(k) = 9 + 2k kills mixtures | screen invalid; by (b), mixtures cost ≤ +1 cst per added line |
| SESSION-SUMMARY:2298 (§752) | v-up DEAD: "+14 cst/line", v=112 at cst 77 → −29.78% | by (b), cst ≤ 64 at v = 112; v-up is mildly negative, not dead |
| SESSION-SUMMARY:1850 (2-class) | "rho 240 → CST ≥ 240×9 → deficit −629,760" | trivial decoder cst = 240; class-blocked ≈ 162 (deficit +14,784). The build-level walls (nat53–60) and the h=10 penalty remain |
| `ii19_nat31.py` (k=−1) | "CST 441 → no root at every R" | 441 sums span dimensions over an arbitrary rref basis, so it is only an upper bound. The system is also odd (I8 ⊕ [−1]), so it is not in II_{1,9} |
| `ii19_nat183.py` (241 shell) | "rank 241/241" | wrong statistic, but the kill stands: the 120 norm-4 lines (r,1) are pairwise non-orthogonal (ip r·s + 2 ≠ 0), so cst ≥ 120 |
| HANDOFF-121LINE:29 | "II19 full-361 by decoder rank 241" | retracted in the record's own opening block (class-blocked rank 28, cst 235); the real closure is the h=10 penalty |

At h = 10 the valid intervals are weak (`audit_nonorth_lb.py`: lower bounds 16 / 24). A tie needs
cst ≤ 108 for the 240-line 2-class and ≤ 162 for the 361. The best valid constructions sit at ~162 and
235, so these are undecided at the decoder level, not dead by rank. A reopening is unlikely.

### E3. Signature labels (verified)

- **The record word is not Lorentzian as built.** `ii19_fullraise_tuned` uses form diag(1^8, 2), which is
  positive-definite (E8(2) ⊕ ⟨2⟩). By the program's own §432 criterion it is off-program, like E8.
- **It can be made Lorentzian for free.** With the special's norm set to −2 (E8 ⊕ ⟨e−f⟩ ⊂ II_{1,9},
  signature (8,1)), the unmodified gcheck returns an identical PASS, histogram and c
  (`audit_lorentzian_flip.py`). All 725 frames split: 551 lie in the E8 coordinates and 173 contain the
  special. The Gram determinants therefore only change sign, so any word built this way transfers.
- The same holds for the 112-line decoder (E1).
- **Consequence:** signature is invisible to the price in this format. The h=9 penalty is the cost of the
  extra dimension, not of being Lorentzian.
- `ii19_nat183.py:99` calls its positive-definite form (x·x' + 2aa') "hyperbolic".
- nat31, nat183 and the 361 build their level classes from sign-canonical roots. That keeps one of
  (α,1,·) and (−α,1,·), which are distinct lines, so those systems depend on an arbitrary sign convention.

### E4. Smaller ledger errors (verified; no verdict changes)

- **Deficit formula:** HANDOFF.md:1679 writes the deficit as T(hv − (h+1)cst). The pricer is exactly
  T(2Kv − (2K+1)cst) = 32(8v − 9cst), independent of h and R. Profile mass is exactly
  T(2K+1)(cst + 2K(h−1)v). Checked to the unit on P111, R420, r434 and W4 (`audit_pricer.py`). At h = 9
  the handoff form overstates the deficit by 15%.
- **Hosting wall:** nat173/174 and SESSION-SUMMARY:2346 compare against "R ≤ 591". The wall at
  v = 121 is 4v = 484. The kill survives (472 + 491 dups).
- **"P111 = the absolute max-deficit system"** (SESSION-SUMMARY:1898) maximizes the absolute deficit over
  star/codeword decoders only. The objective that matters is deficit/mass ≈ (8 − 9x)/(9x + 72(h−1)). The
  handoff's own double-star beats P111 on both measures at its Theorem-C cost (54 on 102 lines). That
  cost needs the cut format; in bitE8/1 the double-star costs 63.

## 2. Checked and not a lever

- **Stage count.** s = 2K+1 is a per-word choice (cf. `research/e8-r480-nine-stage`). Seven stages
  need R ≤ 2.29v and gain only +1.8 points at R = 150 and nothing at R ≥ 220. Eleven stages lose
  1.3% on r434 and 0.5% on W4.
- **Signature.** No effect on price (E3).

## 3. Why no II19 breakthrough follows from these corrections (model, `audit_pricer.py` §3)

Ties with the frontier at a frontier-quality middle (r434 shape at R/v = 3.91):

| h | x for a tie | x = 0.568 (P111) |
|---|---|---|
| 8 | 0.568 | +0.0% |
| 9 | ≈ 0.51 | −14.9% |
| 10 | ≈ 0.45 | −26.0% |

Each cst unit is worth ≈ 2.4–2.8%. The E8 + special family is an E8 word plus one dimension. Its
decoder is the E8-subsystem decoder plus 1 (E1/E2(c)), so it trails its h=8 parent by about 15% at equal
middle quality.

The ladder at the W4 shape (`audit_ladder.py`):

| system | decoder | price |
|---|---|---|
| 121 (record) | cst 73 | −22.98% |
| 112 (E1, in format) | cst 64 | −14.59% |
| 103 (double star + special) | cst 55 | −4.59% |
| 103 at R/v 3.50 | cst 55 | +1.12% |

The 103-line rows need the double-star copy read at the cut ⟨p'_j⟩. bitE8/1 does not provide that:
each copy still costs 7 (`lorentzian-frame-cell-handoff/code/dstar/double_star.py`, re-run, pairing
ranks 6 × 9 = 54 confirmed). So the only II19 route that reaches the frontier in this model is that
format extension plus an R420-density middle. That route would raise the E8 frontier first.

## Open next questions

1. **Build the 112-line Lorentzian word at R ≤ 448.**
   - Relevance: in-format, +7–8 points over the record.
   - First step: apply the W4 build to the P111 line set (or the r434 word plus the special), with the
     cst-64 block decoder and special norm −2.
   - Blocker: the E8 precedent suggests puncturing raises R/v.
2. **Cut-format double star at h = 9.**
   - Relevance: model −4.6% at the W4 shape.
   - First step: check whether the 9th dimension relieves the 49 phase-B frame conflicts recorded for
     P110 in HANDOFF.md.
   - Blocker: it is a format change, and it needs the scalar-interface lemma's coverage.
3. **Re-screen `ii19_fresh1.py` with valid bounds.** Use lower bounds from pairwise non-orthogonal sets
   and the rank of fixed (non-free) blocks, and upper bounds from block, singleton and class-blocked
   constructions. Cheap, and it settles which "rho-level" closures survive.
4. **Decide the completeness criterion.**
   - SS1515 (SESSION-SUMMARY:490) retracted "completeness forces B = B0". Later blocks reinstated the
     junk ⊇ perp criterion and used it to invalidate the class-blocked 2-class decoder.
   - The criterion is also met by the "double-gate" reads the record calls free.
   - First step: derive the requirement from the #463/#510 pipeline.

## Reproduce (from this directory; Python 3 with mpmath and numpy)

```sh
python3 audit_pricer.py          # closed form, stage count, x thresholds, calibration   (~1 min)
python3 audit_decoder112.py      # r434 decoder extraction; the cst-64 112-line decoder   (~1 min)
python3 audit_lorentzian_flip.py # record word under diag(1^8, -2): identical gcheck PASS  (~10 s)
python3 audit_ladder.py          # II19 decoder ladder at the W4 shape                     (~1 min)
python3 audit_nonorth_lb.py      # valid decoder lower bounds for the 2-class and 361      (~5 s)
```
