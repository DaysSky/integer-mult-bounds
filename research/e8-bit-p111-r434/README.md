# P111 with an exhaustive keeper plan and cell-sum helpers: R = 434

This package lowers the helper count of PR #555's punctured E8 bit word (P111, v = 111, decoder constant 63) from 439
to **434**. The format, the unit, the checkers and the pricing pipelines are P111's. Only the block-local "keeper plan"
changes (which free keeper lines the mini-nodes see, and which D6 they go to), together with a second kind of extra
helper. The nine-stage bit c rises above the selected bit frontier, E1 (`research/e8-bit-p111-e1`).

| | P111-tuned (PR #589) | E1 | this package |
|---|---|---|---|
| helpers R | 439 | 439 (one at entrance rank 2) | **434** (all at frame 0) |
| bit c, nine stages (PR #510's chain parameterised by P111's `adapt9p.py`) | 0.001733427039589844234749 | 0.001734473240795253742474 | **0.001744385950814795279853** (`1744385950814795279853/10^24`): **+0.5715% over E1**, +0.6322% over P111-tuned |
| bit c, eleven stages (PR #493's chain via PR #545's `adapt.py`) | 0.001710951900777583975622 | 0.001712057989263075621738 | **0.001721409334720288323589**: +0.5462% over E1, +0.6112% over P111-tuned |
| local paid profile | `{1:1323, 2:1342, 3:79, 4:44, 5:102, 6:11, 7:19}` | `{1:1321, 2:1344, 3:78, 4:44, 5:102, 6:12, 7:18}` | `{1:1311, 2:1339, 3:69, 4:45, 5:103, 6:12, 7:18}` (rank mass 5,089 = 8R + 63 + 14v) |

This is bit headroom only. κ is complex-bound with every cited complex supplier (#548, #544, #535, #531), exactly as
for P111, P111-tuned and E1, so the selected κ does not change.

## Where P111's five extra helpers went

P111's bill is 429 + extras: 240 carriers, 180 cell empties and 9 pseudo-target totals, plus 10 extra carriers. The
extra carriers bring to a block's phase-A mini-node the lines that no free keeper or freed source holds. A junk wire is
needed only when a block node has more outputs than independent inputs. Both depend only on block-local choices. For
block B these are:

- the free-keeper line of each of B's six non-dual cells (2^6);
- which keeper becomes the third register of each (z,z) D6 of comp(B) (6!);
- the receivers of the pseudo-target totals of comp(B) (3 each);
- the punctured lines.

P111 drew the first two from `plan_thirds` with seed 552 and searched seeds 0..1700 with a few receiver draws. The
receiver census (`research/p111-receiver-census`) then exhausted the receivers for that frozen draw, and found 439.

1. **Exhaustive keeper plan (gen_p3's own accounting).** `code/census.py --old` enumerates all 46,080 × 3^k choices
   per block. For the shipped puncture set the minimum is **8** extra carriers (R = 437), against 10. Blocks 0 and 5
   each save one.

   `--old --all` repeats the census for every subset of eligible lines of every complementary block pair. It then
   combines the subsets over all 17,478 affinely independent puncture sets (lines 0..7 live, as in P111). The minimum
   is 8, attained only by P111's own puncture set; the next best set needs 13. So P111's puncture choice was optimal,
   and its keeper draw was not.

2. **Cell-sum helpers (`code/gen_p4.py`).** In the optimal plans the missing lines come in cells. In block 0, for
   example, both totals τ15 and τ66 lack exactly x49 + x63, and {49, 63} is a cell of block 0. A cell-sum helper
   reads that cell's empty register at the cell frame, after the cell gate and before the quads, so it holds
   x_a + x_b. It then climbs to the block frame D4(B) like an extra carrier.

   One such helper replaces two extra carriers whenever the totals need only the sum. It also serves as a junk
   direction in B's phase-B block node: the helper plus its two sources has x-part 0, as an extra carrier plus its
   source does in gen_p3. The block cost becomes max(|E|, junk directions needed).

   The census (default mode) finds the exact minimum per block: **B0: 1, B1: 1, B3: 1, B5: 2**, i.e. 5 extra helpers
   and R = 434. Block 1 cannot do better in this unit: its node has 10 live outputs (block 0's targets minus two
   punctures) over 9 live inputs (block 1's sources minus three), so it needs a junk direction in any case.

3. **Choice among the optimal plans.** The per-block optima are many (B0: 1,914 plans, B1: 28,804, B3: 2,180,
   B5: 13,668), and they differ in the stop profile. A scan built words with one block varied at a time and scored
   each exact local profile:
   - blocks 0 and 3: every optimal plan gives the same profile;
   - blocks 1 and 5: 2,500 plans each (a sample);
   - the best block-1 plan, then the tuner (step 4), gave the best exact price among the combinations tried.
   This selection is a sampled search, not an optimum. `data/params.json` is the chosen plan.
   Its extras are: block 0 the cell sum x49 + x63; block 1 one extra carrier (x3), which is also the block's forced
   junk direction; block 3 the cell sum x29 + x97; block 5 the cell sums x24 + x100 and x40 + x84.

4. **PR #589's tuner.** `code/tune434.py` runs P111-tuned's `tune.py` (imported unchanged; the loop of its
   `apply.py --discover`, fee rate 0.001733) to its fixed point on the base word. It finds one transport: the profile
   changes by +e1 - e2 - e4 + e5, with zero rank-mass change. Only A, B and C change, and they are written in the
   tuner's one-source-per-gate form, which gives more gates (A/B/C 2,108/918/2,591) for the same additions. The tuned word is the
   shipped word, and the untuned base word is shipped too, so the tuner step is checked exactly.

Both accountings are re-implemented independently in `census.py`'s block evaluator and calibrated against full builds:

- `--calibrate 30`: the block evaluator equals gen_p3's helper count on 30 of 30 random keeper plans;
- gen_p4's count equals gen_p4's build with the extras the evaluator names, on 30 of 30.

The shipped word was built from `data/params.json`, and every helper starts at frame 0.

## Checks (`bash verify.sh /fresh/dir`)

0. Manifest.
1. **Rebuild.** The base word is rebuilt from #543's frozen L3 plan and `data/params.json` by `code/gen_p4.py`, and
   the shipped word from the base word by `code/tune434.py`; both match the shipped files (decompressed
   payloads, as CONTRIBUTING.md recommends for regenerated gzip artifacts). **Control:** `gen_p4.py` fed P111's own keeper plan (`data/params-p111.json`, seed 552 written out)
   rebuilds P111's shipped word exactly. So gen_p4 is gen_p3 plus the cell-sum option.
2. **P111's independent checker, unchanged** (`xcheck_p.py`):
   - labels and frames;
   - exact F2 replay on all 656 columns, with dirty helpers symbolic;
   - the nine totals at the punctured hyperplanes, COPY ranks 7 × 9;
   - the interleaved interface lemma H1–H5 with U, J = I, D = K, C = U⁻¹;
   - P111's word-level controls (9/9 negative rejected, 1/1 positive accepted) and punctured-design controls (4/4).
3. **Hub checkers.** PR #545's v ≤ 120 form of #370's checker refuses on a source write, as for P111, and its relaxed
   copy passes. #493's `interface.py` refuses at check (4).
4. **Official cohort checkers (C++)** at (v, R) = (111, 434): legality, rank mass 8R + 63 + 14v; formal columns at
   five, nine and eleven stages, with all omitted-bridge controls; record mutants; Gram witnesses.
5–6. **Nine-stage price.** PR #510's chain, parameterised by P111's `adapt9p.py`, 32 replicas. The hosting
   programme's selection is rediscovered (`data/selection9-r434.json`). Template, parent and hosted audits pass, and
   every residual is hosted whole.
7. **Eleven-stage price.** PR #493's chain via PR #545's `adapt.py`. Its selection is rediscovered
   (`data/hosting11-r434.json`).
8. **Summary.** The results are compared against `EXPECTED.json`, and against E1's and P111-tuned's `EXPECTED.json`.

## Scope

- **Same unit and contract as P111.** P111's checker accepts the word without modification. No entrance conversion is
  used. The exact single-column entrance census that rediscovers E1's helper on P111-tuned finds no convertible helper
  on this word, before or after tuning (see the open questions).
- **What is claimed.** A finite nine-stage bit word with exact replay, the official cohort checkers and the hub
  pipelines, with the c above. The census minima are exact for the stated generator families (gen_p3 and gen_p4
  accounting under #543's frozen L3 plan). They are not lower bounds for other skeletons or plans. No new complex
  result, no change to κ, and no all-size theorem is claimed.

## Open next questions

1. **E1's entrance conversion on this word.**
   - Relevance: about +0.06% per convertible helper.
   - First step: give a cell-sum helper the cell of the designated keeper that reads it, so that the keeper can
     pre-read it at the cell frame (rank-2 entrance), and add that pairing to the census objective.
   - Blocker: a helper that also serves as a phase-B junk direction passes its dirt to targets through the block node.
2. **Other L3 plans.**
   - Relevance: the plan fixes the eligible lines and the non-dual cells. One extra helper (block 1's junk direction)
     is forced by the odd puncture count, so at most 4 more helpers are at stake (about +0.3%).
   - First step: `research/lorentzian-frame-cell-handoff/code/s8/plansearch.py` (CP-SAT plans with random objectives,
     a lower bound per puncture set, then sampled keeper plans).
   - Blocker: one plan solve plus screening takes minutes, and the exhaustive census takes about 7 min per puncture set.
3. **Extras beyond one cell.**
   - Relevance: the remaining extras in block 5 need two independent directions.
   - First step: list the registers that sit at frames inside D4(B) during phase A.
   - Blocker: a helper visits only one rank-2 frame below D4(B), and no register is parked at the rank-3 frames there.
4. **The gen_p4 census over all puncture sets.**
   - Relevance: completeness of the minimum.
   - First step: `census.py --all` in its default mode (an estimated 1-2 hours on 4 cores).
   - Blocker: none. Under gen_p3 every other set costs at least 13, and gen_p4 at best halves the line count, so a
     gain is unlikely.

## Reproduce

```sh
bash research/e8-bit-p111-r434/verify.sh /fresh/output/dir     # about 5 minutes; python3 >= 3.11 with numpy, sympy,
                                                                # scipy; a C++17 compiler; Boost headers
python3 -I -B research/e8-bit-p111-r434/code/census.py --calibrate 30   # seconds
python3 -I -B research/e8-bit-p111-r434/code/census.py                  # gen_p4 minima, shipped set (~7 min, 4 cores)
python3 -I -B research/e8-bit-p111-r434/code/census.py --old            # gen_p3 minima, shipped set
python3 -I -B research/e8-bit-p111-r434/code/census.py --old --all      # all puncture sets (gen_p3)
```

The census outputs are in `data/census/`. `verify.sh` does not run the census, so the minima rest on those logs and on
re-running the script.

Prepared by DaysSky with assistance from Claude. Apache-2.0.
