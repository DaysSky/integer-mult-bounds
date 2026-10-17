# Lorentzian bit supplier: where it stands after session 6i

Scratch research by DaysSky with assistance from Claude.  Not reviewed.  Details and scripts are in
[HANDOFF.md](HANDOFF.md) (section 3g) and `code/`.

## Question

Can a bit word on a Lorentzian line system beat P111-tuned (c = 0.001733427039589844, an E8 word)?

## Answer so far

**No such word is known.**
- The best verified Lorentzian word is `code/lbuild/word_blkA4.json.gz` (I_{11,1}, R = 3,656, cst 121).  It
  prices at **c = 0.000492650689, -71.6%** (`code/price/bankprice.py`, bank-overflow pricer; P111 and R420 controls
  exact).
- No mechanism found gets a Lorentzian word past a tie, even under idealised assumptions.

## Why (quantitative summary)

1. **Ideal price.**  Window h = 11 makes I_{11,1}'s best one-stop price about 15% below E8's (more lines per
   dimension, but a larger window).  A Lorentzian word must therefore beat E8's best relative efficiency (R420,
   eta = 0.404) by about 10% (eta >= 0.444).
2. **Even a perfect R420 analogue only ties.**
   - With z-groups (non-line entrance frames, format-validated) an R420-quality I_{11,1} middle prices at -3.3% to
     +0.3%.
   - That middle does not exist.  E8 R420's partition is fully aligned (0 odd (E-set, frame) pairs).
     I_{11,1} partitions carry about 7,150 even after annealing, I_{13,1}'s PG(2,3) partition 23,348, and aligned
     I_{11,1} partitions provably need >= 52 punctures.
3. **Assembly, not delivery, binds.**
   - Delivery can be made cheap: rank-7 block groups put a star-D4 block's 12 targets on one shared frame-perp,
     so their needers become width-4 group helpers.
   - Assembly cannot be made cheap.  Even with E8-style half sharing (star-D4 blocks 3-fold, Pasch pairs
     2-fold), each line lies in about 22 distinct demands, against E8 R420's 9.  The demands are not cell
     unions.
   - Exact pricing on E8's own role chains shows group helpers pay only when they remove frame-0 registers.
4. **Other tops.**
   - 10-frame (D10) tops: per-line cell cover 11-12, against E8's 3.
   - Full-rectangle tops (e.g. D5 x D5): no exact F2 cover exists.
   - Apex families reduce to the D8 route: apex D5s are infeasible, and the load + deliveries bound is >= 25.2,
     against R420's 16.
5. **Decoder.**
   - B0 (cost 110) is the unique 11-piece decoder.
   - Coordinate-flat decoders containing C_11 cost >= 122 (proof in HANDOFF).
   - Z11-cyclic section decoders at cost 109 do not exist (exhaustive).
   - Each decoder unit is worth about 1.1-1.2%, so no reachable decoder change closes the gap.
   - **Proven (computer-assisted): every I_{11,1} decoder costs >= 102** (clique + minrank-11 hitting LP over all
     56,498 flat orbits, certified 101.43 after the first column-generation round; earlier rounds gave 99.67, 100.65).
     Decoder changes are worth at most 8 units, about 9%.
   - Sparse decoder rows (the only decoder-side lever on load): rank-12 decoders whose row space misses C_11
     exist (SAT), but every one found is B0 plus one small piece.  They cost 112-118 and save at most 5.9% of the
     row weight, about 40-190 entries per unit of decoder cost, against about 260-350 entries per unit needed.
6. **Systems and format.**
   - Stage count does not help: the verified word prices -71.6% at K = 4 and -71.9% to -74.3% at K = 3, 5-12.
   - Root-like Lorentzian systems are capped at C(h+1,3) + 1 lines.
   - I_{11,1} is saturated for odd-or-zero extensions in the range searched.
   - h = 8 and h = 9 Lorentzian systems are too small; larger h lowers the ideal price further.
   - The minus-type sibling of E8 (136 nonsingular points of O^-(8,2), h = 9) would be on a par with P111 at equal
     helper density.  But its orthogonality pattern does not realise with non-null vectors in any 9-dimensional
     signature (numerical; the E8 control realises exactly).

## Best-case scaling estimate (model, not a bound)

- E8 R420 uses about 4.5 registers per line for a load of 9 plus 7 deliveries per target.
- Scaling registers with load + deliveries:
  - I_{11,1} at its best realised load (22, with 3-fold sharing) needs about 8.2 per line (R ~ 1,580).  That is
    about -35% with frame-0 helpers, or about -28% with z-groups.
  - Even at the unreachable load floor of about 10 per line, it is about 4.8 per line (R ~ 840), roughly a tie
    with P111-tuned.

## What would change the picture

- An architecture strictly more efficient than R420 per incidence, which would be a large E8 improvement first.
- ~~A decoder for I_{11,1} well below 110 (about 95 or less)~~: ruled out; every decoder costs >= 102 (proven), so the
  decoder can add at most about 9%.
- An assembly scheme for misaligned demands at E8's register cost per incidence.
- Alternatively, an all-word lower bound that closes the question rigorously; none reaches break-even yet (the
  proven floor is 426 frame-0 helpers against a break-even of roughly 720-900).

## Open next questions

1. Close the decoder gap 102-110: is B0 (110) optimal?  The clique LP caps near 104.8; minrank-11 families could go further.
2. Minimum misalignment of an I_{11,1} good-frame partition with 4 punctures (annealing reached 7,149).
3. A rigorous lower bound on assembly registers in terms of the per-line distinct demand load.
