# P111-tuned with one entrance-rank-2 helper (E1)

This package raises the nine-stage E8 bit supplier above P111-tuned (PR #589,
`research/e8-bit-p111-tuned/tune/`). One helper of that word now starts at a rank-2 frame instead of frame 0. A single
inserted gate cancels the helper's dirt, so the frame-0 preconditioner no longer needs to read it. To our knowledge this
is the first constructed bit helper narrower than width 8: PR #1023 priced width-7 bit helpers hypothetically and
listed their construction, window timing and re-audit as open obligations.

| | P111-tuned (PR #589) | E1 (this package) | change |
|---|---|---|---|
| bit c, nine stages (PR #510's chain, 32 replicas, parameterised by P111's `code/adapt9p.py`) | 0.001733427039589844234749 | **0.001734473240795253742474** (`867236620397626871237/(5·10^23)`) | **+0.0604%** |
| bit c, eleven stages (PR #493's chain as parameterised by PR #545's `adapt.py`) | 0.001710951900777583975622 | **0.001712057989263075621738** (`856028994631537810869/(5·10^23)`) | **+0.0646%** |
| local paid profile | `{1:1323, 2:1342, 3:79, 4:44, 5:102, 6:11, 7:19}` | `{1:1321, 2:1344, 3:78, 4:44, 5:102, 6:12, 7:18}` | rank mass −2 |
| helper residual widths per call | 439 × 8 | 438 × 8 + 1 × 6 | |
| κ with #548 / #544 / #535 / #531's complex b | complex-bound | unchanged (complex-bound, 47/47 strict) | none |

This is bit headroom only. κ is complex-bound with every cited complex supplier and with the selected frontier's
complex side. Nothing here changes the selected κ.

## The change (`code/build_e1.py`, byte-for-byte rebuilt by `verify.sh`)

In P111-tuned, helper 248 (register 470) is first written by A[230] = `[79, 470, [77]]` (`h248 += x77` at frame 79, the
line of root 77). PR #589's hoist later reads it at A[1993] = `[79, 444, [470]]` (`h222 += h248`, same frame). E1 makes
three changes:

1. A copy of the hoisted gate, `h222 += h248`, is inserted immediately before A[230].
2. The three gates on register 470 (the inserted read, A[230] and A[1993]) move from frame 79 to frame 186 =
   span(root 33, root 77), a rank-2 plane spanned by two orthogonal live roots. This is the frame x77 climbs to next
   (at A[426]). Register 444 climbs 0 → 186 → 509 instead of 0 → 79 → 509; block frame 509 contains 186.
3. `start[470] = 186`. Helper 248 enters at the rank-2 frame 186 instead of frame 0.

Register 444 now reads 470 twice: once while 470 holds only its dirt `d`, and once later when it holds `d + x77`.
Over F2 the two dirt copies cancel, so 444 receives exactly what it received before, minus `d`. The raw word's target
outputs lose the helper-470 column: 55 targets drop 470 from their D sets, and the symmetric difference of the
recomputed D with P111-tuned's is exactly {470}. Since no D gate reads 470 any more, 470 need not sit at frame 0 when D
runs. C is rebuilt as the literal reverse of the z-destination gates of A and B at the full frame (A 2,076 gates, C
2,575). Every other field of the word is P111-tuned's (asserted by `verify.sh`).

In pricing terms, helper 248's residual has width 6 (= 8 − entrance rank) instead of 8. The rank mass drops by two per
local invocation: legality rank mass 5,127 = 8R + 63 + 14v − 2. The local profile changes by
`−2 e1 + 2 e2 − e3 + e6 − e7`. Helper 470 loses its 0 → 79 run, and its C climb becomes 186 → full (rank 6) instead of
79 → full (rank 7). Register 444's runs (1, 3) become (2, 2). Frame 186 is the largest possible entrance: an earlier
frame for 470's write would have to lie inside x77's next frame, which is 186.

This is the response-kernel mechanism of PR #434's early-reset kernel ("start each pivot at E, emit donor += pivot at E
… the exact response relation cancels the omitted compensation"). Here the donor read is placed at time 230 instead of
time 0, the donor is register 444 itself, and the relation is a single equality.

## Checks (`bash verify.sh /fresh/dir`, about 100 s; passes)

1. The word is rebuilt from P111-tuned's shipped word and matches byte for byte. The residual isometries are rebuilt.
   The script asserts that E1 differs from P111-tuned only in `start[470]`, the inserted gate, the two reframed gates,
   D, C and `stats`.
2. **Independent exact replay.** `code/xcheck_e1.py` is P111's `code/xcheck_p.py` with two listed edits, marked
   `[E1 VARIANT]` in its docstring:
   - the replay's start check exempts helpers that no D gate reads;
   - H2 ("D at frame 0") requires frame 0 only for targets and for the helpers D reads.
   It reports legality and exact F2 replay on all 661 columns (dirty helpers symbolic), and the interleaved
   interface lemma H1–H5 with U, J = I, D = K and C = U⁻¹. P111's word-level and punctured-design mutation controls
   run against this checker: 9/9 + 4/4 negative controls rejected, 1/1 positive control accepted. The unmodified
   `xcheck_p.py` refuses, as expected ("helper 470 does not start at frame 0").
3. **PR #545's relaxed copy of #370's checker refuses.** It asserts an all-zero start for targets and helpers, the
   requirement E1 relaxes. `verify.sh` asserts that this is the refusal reason.
4. **Official cohort checkers (C++, freshly compiled).** These are `legality_h.cpp` (reads the initial frames from the
   records) and `columns_h` / `columns_k` (F2 formal columns at five, nine and eleven stages, with all omitted-bridge
   controls). All accept the word, together with the e8ham Gram witnesses. The rank mass is 8R + 63 + 14v − 2.
5–6. **PR #510's nine-stage chain**, parameterised by P111's `adapt9p.py`, with three listed differences from
   P111-tuned's `verify.sh`:
   - **Residual isometries.** These are `data/residual-isometries-e1.json` (`code/make_iso_e1.py`): PR #443's frame-0
     record plus a record for frame 186. Its entrance basis is roots 33 and 77; its residual basis is six further live
     roots completing an orthogonal frame. Root 77 = (0,1,0,−1,1,0,1,0) and root 33 = (1,1,0,0,−1,−1,0,0) are not
     coordinate roots, so the record needs genuine route factors: 30 factors (4 swaps, 5 scalings, 21 additions, all
     dyadic). The vendored validator accepts swaps only, because every entrance frame of R715/R740 is spanned by
     coordinate roots. `code/isometry_e1.py` is that validator with one change: it also replays the port routes'
     `scale`/`add` factors exactly, with dyadic scalars, at most 77 factors. 77 is the geometry's
     `max_route_factors`, which `assemble9.py` already charges per residual route in the finite selector bill.
     `code/adapt_e1.py` wires it into `global_k.py` and `audit_parent_k.py` (two import edits). With a route factor
     present, the parent audit's control "omit a residual route factor" is no longer vacuous, and it is rejected.
   - **`global_k.py --no-banks` and `emit_k.py --host-all`.** This is the chain's own host-every-residual mode. The
     width-64 bank template is a fallback for unhosted residuals, and it tiles exactly only if the leftover widths
     admit a zero-padding tiling. With the default hosting objective, one stage leaves the 32 width-6 residuals for
     banks, and `{6: 32}` has no exact width-64 tiling, so that run fails. In host-all mode every residual is hosted
     whole (P111-tuned also has 0 banks).
   - **Discovered hosting selection.** The hosting programme (`emit_k.py --discover --host-all`) finds the selection
     `data/selection9-e1.json`, and `verify.sh` checks that it is rediscovered. The hosted audit passes: 126,432 of
     126,432 helper residuals hosted whole, 0 banks, 16 mutations rejected, deficit 10,272. The global profile is
     `{1:380512, 2:400960, 3:22464, 4:26816, 5:29376, 6:17536, 7:26432, 22:32, 42:320}`.
7. **Eleven-stage chain** (PR #493's, as parameterised by PR #545's `adapt.py`, the way P111-tuned's `verify.sh` runs
   it). The vendored hosting nominator asserts that every helper starts at frame zero. `code/host11_e1.py` is the
   same nominator with residual widths read from the start frames, and the same integer programme forcing every
   residual onto an idle child. Its selection is frozen in `data/hosting11-e1.json` and rediscovered.
   `code/adapt_e1.py` points `emit.py` and `local_audit.py` at the E1 validator and isometry file. In
   `local_audit.py` it drops the two asserts that encode the all-zero entrance (exactly one isometry record, entrance
   rank 0). The audit still compares the template's isometries and entrance-rank total with what it recomputes.
   Emit, independent audit (PASS) and the outer assembly give c₁₁ = 0.001712057989263075621738 (+0.0646% over
   P111-tuned's eleven-stage price). The finite physical prefix grows, which affects only the cutoffs: the
   assembly's 47/47 inequalities pass.
8. The summary checks the nine- and eleven-stage c and κ against `EXPECTED.json` and against P111-tuned's.

**Independent price check.** `code/price_e1.py` computes the price separately from the chain. It runs an exact
window-aware hosting MILP over the B_4 idle-slot template (ortools/SCIP; nine slot types per port copy with their call
windows; any residual widths), then iterates the exact root of the nine-stage pricer to its fixed point. It reproduces
P111-tuned's c (0.0017334270395898443) and E1's c (0.0017344732407952538), both MILP-optimal. It is not run by
`verify.sh`.

## Scope and review points

- **Entrance contract.** The relaxation of P111's all-zero start for non-D helpers is the contract that the vendored
  nine-stage `global_k.py` already states: "the original all-zero-start requirement is replaced by the verified
  kernel entrance contract" (explicit residual isometries and mixed-width banks, PR #439 / #443 lineage, used by
  #434). E1 exercises it with a non-coordinate entrance frame, hence the isometry change. The all-column F2 replay
  (xcheck_e1, `columns_h`, `global_k`'s template replay) covers arbitrary helper contents. 470's dirt reaches no target,
  and 470 ends at the full frame holding e_470.
- **Status of that contract on the record.** #434, #439 and #443 are unreviewed in the hub's ledger. The entrance
  mechanism itself is maintainer-validated on the complex side, and E1 is its bit instance with (E, U) = (frame 186,
  full frame):
  - #484 (compatible entrance gauges, shared-donor kernels, normalized residual wrappers: full replay) and #509
    (entrance-gauge lemmas: Lean build and axiom reports), in `docs/research/community-formal-20261012-review.md`;
  - the residual rule for an entering helper with entrance E and terminal U, residual T_U T_E⁻¹ and width
    dim U − dim E, in `docs/research/community-hyperplane599-review.md`;
  - #569's incorporated entrance promotions.
- **Inherited scope.** The mutable-basis interface for source writes (#425 / #493 / #510 scope (d)) is P111-tuned's,
  unchanged, as is the complex side. The eleven-stage price (step 7) is reported for comparison with P111-tuned's
  package; the selected bit rate is the nine-stage one.
- **What is claimed.** A finite nine-stage bit word with exact replay, the official cohort checkers, and the
  parameterised #510 chain with the three listed adaptations, giving the c above. No new complex result, no change to
  κ, and no all-size theorem is claimed.

## Why only one helper (negative results, exact)

The lever is large in the slot model. With `code/price_e1.py`'s model, width-7 helpers each worth one rank-1 child:
10 helpers give +0.57%, 100 give +6.1%, and 438 give +23%. Converting a helper h needs its target-response column
k_h ∈ F2^111 to be cancelled by legal reads of h. The following was measured on E1's word, with the exact adjoint α
(target influence of a register's content at a time) and exact frame nesting:

- **Direct target readers.** 225 helpers are read directly by a target in B. Only the frame-0 D pre-read can cancel
  their dirt.
- **#434's criterion** (donors read the pivot at time 0, at E, with E inside each donor's first frame): 0 of 438
  helpers. Each helper has at most 6 eligible donors (first frames: 286 lines, 153 rank-2 frames), and the K matrix
  has rank 111.
- **Any time, fixed schedule.** Dirt is injected as `g += S_h(p)`, where S_h(p) is the unique register set whose
  current values sum to e_h, so injection works at any time, not only before h's first write. F ranges over any
  listed frame nested between the current and next frames of g and of every member of S. 0 of 438 helpers convert:
  only 2–9 distinct frame-compatible α vectors per helper. Predictions were checked against forward replay.
- **Rescheduled A.** Any topological order of the touch DAG keeps every register's frame chain. Injections may then be
  placed anywhere consistent with the DAG, in the regime where the pivot has read only sources. This is an
  over-approximation (pairwise acyclicity only), and it gives 0 of 438.
- **Frame-only coordinated moves.** Merging two consecutive frame segments of a register, with forced lifts cascading
  forward or forced lowerings cascading backward, is infeasible for all 2,360 segments in both directions. The cascades
  reach target t-perp frames, retained-total COPY gates, D, or source start lines. PR #589's tuner finds no move on E1.

So on this word the mechanism is limited by frame locality: helpers live on single lines and planes, inside
mutual-addition networks. Scaling it needs a word whose helpers' frame chains admit many donors.

## Open next questions

- A word design (a different A-section plan for the L3 skeleton) in which a pivot's readers are untouched helpers
  whose first frames contain the pivot's entrance, read the pivot before being read themselves, and no target reads
  the pivot. Then k_p equals the sum of the readers' columns, which is #434's relation, automatically. The slot model
  says 100 width-7 helpers would be worth about 6%.
- Non-full helper ends for the bit chain. After E1, helper 470's dirt column is clean (only 470 holds e_470 after B).
  Its inverse row at the end of B spans all 8 dimensions. A cleanup retimed to just after its last read
  (`[186, 470, [77]]`, with the C gates on 470 replaced by their net effect `444 += x77`) would end it at its entrance
  frame 186, so it would never climb. That is equivalent to removing helper 470: register 444 can read x77 directly at
  frame 186 at A[1994]. It is a helper removal, not pursued here. The bit `global_k.py` also asserts full final frames
  for helpers, so any exit-rank construction needs an adaptation of the chain, as the complex side has (#1030 / #1090).

## Files

- `data/bitE8mut-p111-e1.json.gz`: the word (canonical JSON, gzip mtime 0). `data/residual-isometries-e1.json`,
  `data/selection9-e1.json`.
- `data/hosting11-e1.json`: the frozen eleven-stage hosting selection.
- `code/build_e1.py`, `code/make_iso_e1.py`: builders. `code/host11_e1.py`: the mixed-width eleven-stage nominator. `code/xcheck_e1.py`: the E1 variant of P111's checker.
  `code/isometry_e1.py`, `code/adapt_e1.py`: the isometry validator and its wiring. `code/price_e1.py`: independent
  MILP pricer (needs ortools and mpmath).
- `verify.sh`, `EXPECTED.json`, `LICENSE`.

## Attribution

Built on PR #589's P111-tuned word (DreamingOfClouds; `research/e8-bit-p111-tuned/tune`) and its package
(`research/e8-bit-p111-tuned`, prepared by eumemic with Anthropic Claude assistance). That package carries PR #555's
punctured R439 word: #545's punctured-star unit, by DreamingOfClouds, on #543's R420 L3 skeleton, by eumemic. The
nine-stage chain is PR #510's (DreamingOfClouds; #463 / #443 / #442 / #315 lineage, with the residual-isometry format
of #443 / #439 by chafreaky). The response-kernel entrance mechanism is PR #434's. The width slot-model estimates
follow #1023 (thakrarsagar), and the rank-7 end criteria follow #1030 / #1090. Prepared with Anthropic Claude
assistance; Apache-2.0.
