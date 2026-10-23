# A full p=8 coded-reverse controller word with a better complex supplier

**The p=8 coded controller is a complete controller word with raw complex root 0.007926; the physical S/L/R pair is exact at the native pair. The per-stage native adapter, field-map tariff, denominator 13/52 and compiler remain open.**

PR4940 constructs a coded reverse controller from the center-free coded word:
every reverse stage carries the code `A`, every thin forward stage is mixed by
`A^-1`, and the controller is the standard one up to the boundary
`(A on x) Standard (A^-1 on x)`. Its verifier diagonalizes the coded controller
for p = 3, 4, 5, 8 with the standard outputs, checks the p=2 448x448 conjugation
and prices the raw complex root. At **p=8** (pattern `IIIITTT`) the coded word
has raw complex root **0.007926**, versus 0.0030218 for the standard controller;
the outer ledger accepts up to 0.0033999971 and at 0.0034 fails only the BIT cap.
That is a genuinely better complex supplier word: the complex side stops
binding, and the conditional endpoint is 0.0034 (+12.5% over 0.00302015).

The native physical code of PR4933 is `C = K^-1 (A tensor I) K`, not the scalar
`A`.  The companion package supplies the exact physical local pair

```
S = Q D C^-1 Q^-1 D^-1,   R = Q C Q^-1,   L = D Q C^-1 Q^-1 D^-1,
L (T B) R = standard,
```

on the PR5036 witness and random banks in two independent implementations.  This
package composes the verified p=8 coded controller with that physical pair
adapter.

## What is verified here

`verify.py` runs both certificates and checks:

- the p=8 coded controller diagonalizes to the standard outputs, with the only
  new boundary denominator 13;
- the p=2 448x448 coded controller equals `(A on x) Standard (A^-1 on x)`;
- the coded raw complex root is 0.007926 and the p=19 root 0.007579;
- the outer ledger passes at 0.0033999971 and at 0.0034 fails only the BIT cap;
- the physical S/L/R local pair is exact on the signed code, with the controls
  rejecting the literal scalar `A^-1` source, the `C^-1` source without the
  changed boundary, and the identity output boundary;
- the local invoice reproduces the p8/p19 roots and the outer ledger.

## Scope

The p=8 coded controller word and the physical local pair are verified.  The
per-stage native adapter (every reverse/thin stage, bridge and IDLE), the
fixed-tape field-map tariff for the added codes, the denominator 13/52
implementation, the ambient-rank-153 compiler constants, BIT-side admission,
hosted CI and formal-kernel review remain open.  No new selected kappa is
claimed; the conditional endpoint is 0.0034.

## Reproduce

```sh
python3 -B research/coded-reverse-physical-word-p8/verify.py
```

## Open next questions

1. A stage-by-stage physical adapter: every p=8 reverse stage with the physical
   `C`, every thin forward stage with `S`, every bridge and IDLE, and the pair
   identity at each thick/thin boundary.
2. The fixed-tape field-map tariff for the added `C/C^-1` and boundary maps.
3. The denominator 13/52 implementation, the ambient-rank-153 compiler
   constants, BIT-side admission, hosted CI and formal-kernel review.

## Credit

PR4940 coded reverse controller: Cayden Burkart / SethBurkart123. PR4933 signed
physical code and normalizers: Dillon. PR4929 center-free producer: Dugongue /
mdumitrean. PR5036 physical gap: JoyboyBrian. PR4440/4470 controller and query
thinning: Cinna Davis / 1337isnot1337. Retained native, Clifford, ownership,
compiler and precision lineage as credited in those packages.
