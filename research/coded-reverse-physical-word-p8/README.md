# p=8 coded-reverse controller word: formal controller and local pair; 0.0034 endpoint retracted

**Correction: the p=8 coded controller has raw complex root 0.007926, but its
p=8 delta guard is 1.462814 at 0.0034, so the p=8 word is NOT admissible at
0.0034. The 0.0034 endpoint belongs to the p=19 word. The p=8 formal controller
and the local S/L/R pair are verified; the per-stage native adapter, field-map
tariff, denominator 13/52 and compiler remain open.**

The p=8 formal controller diagonalizes to the standard outputs with denominator
[1,13] (the PR4940 verifier). The local pair is exact. The p=8 delta guard
fails at 0.0034; the p=19 word passes its guards at 0.0034 and is the admissible
0.0034 candidate (see research/coded-reverse-word-p19).

## Open next questions

- the per-stage native adapter for the physical code;
- the fixed-tape field-map tariff, denominator 13/52, ambient-rank-153 compiler
  constants, BIT-side admission and kernel review.

## Reproduce

```sh
python3 -B research/coded-reverse-physical-word-p8/verify.py
```

## Credit

PR4940 coded reverse controller: Cayden Burkart / SethBurkart123. PR4933 signed
physical code and normalizers: Dillon. PR4929 center-free producer: Dugongue /
mdumitrean. PR5036 physical gap: JoyboyBrian. PR4440/4470 controller and query
thinning: Cinna Davis / 1337isnot1337. Retained native, Clifford, ownership,
compiler and precision lineage as credited in those packages.
