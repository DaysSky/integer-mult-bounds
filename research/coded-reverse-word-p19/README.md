# The p=19 coded-reverse controller word: invoice, guards and physical pair

**The p=19 coded controller word has raw complex root 0.007578535; its full 39-stage
controller diagonalizes to the standard outputs with denominator 13; its tail
guards pass at 0.0034 and the outer ledger fails only the BIT cap. The physical
S/L/R pair is exact. The per-stage native adapter, field-map tariff, denominator
13/52 and compiler remain open.**

PR4940's coded reverse controller at p=19 (pattern `IIIIIIIIITTTTTTTTT`) is the
formal controller whose complex-side invoice and p=19 guards clear 0.0034; the supplied outer ledger passes at 0.0033999971 and is BIT-limited at exactly 0.0034. The p=8 word is not
admissible there: its delta guard is 1.4628 at 0.0034. The p=19 word has
alpha=0.995794, gamma=0.963763, delta=0.951561 at 0.0034, so all three strict
tail guards pass; the outer ledger passes at 0.0033999971 and at 0.0034 fails
only `actual_bit_above_effective`. The raw complex root is 0.007578535, versus
0.0030218 for the standard controller; the conditional endpoint is 0.0034,
+12.5% over 0.00302015.

The physical PR4933 code is `C = K^-1 (A tensor I) K`, not scalar `A`. The
companion package gives the exact local pair

```
S = Q D C^-1 Q^-1 D^-1,  R = Q C Q^-1,  L = D Q C^-1 Q^-1 D^-1,
L (T B) R = standard,
```

on the signed code, with two independent implementations and rejection controls.

## Verified here

- p=19 tail guards at 0.0034: alpha, gamma, delta all pass;
- p=19 raw complex root 0.007578535;
- outer ledger: 0.0033999971 passes; at 0.0034 only the BIT cap fails;
- p=2 448x448 coded controller identity;
- the local S/L/R pair and its controls.

## Verified full p=19 controller diagonalization

The p=19 coded controller (39 stages, pattern `IIIIIIIII`+`T`x9) diagonalizes
to the standard outputs
`[(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(19,2)]`
with standard denominators `[1]` and coded denominators `[1,13]`.

## Open next questions

- the per-stage native adapter for the physical code;
- the fixed-tape field-map tariff, denominator 13/52, ambient-rank-153 compiler
  constants, BIT-side admission and kernel review.

## Reproduce

```sh
python3 -B research/coded-reverse-word-p19/verify.py          # fast receipt
python3 -B research/coded-reverse-word-p19/full_p19_diagonalization.py  # long full p=19 run
```

## Credit

PR4940 coded reverse controller: Cayden Burkart / SethBurkart123. PR4933 signed
physical code: Dillon. PR4929 center-free producer: Dugongue / mdumitrean.
PR5036 physical gap: JoyboyBrian. PR4440/4470 controller and query thinning:
Cinna Davis / 1337isnot1337. Retained lineage as credited in those packages.
