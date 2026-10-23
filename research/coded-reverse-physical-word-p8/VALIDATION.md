# Validation

Environment: CPython 3.12 with numpy 2.3.5, macOS.

| Command | Result |
|---|---|
| `python3 -I -B research/coded-reverse-physical-word-p8/verify.py` | PASS: p=8 coded controller, p=2 448x448, 0.007926 root, physical S/L/R pair, outer ledger |
| `python3 -I -O -B research/coded-reverse-physical-word-p8/verify.py` | PASS: explicit need() checks |
| `python3 -B scripts/research_package.py --package research/coded-reverse-physical-word-p8` | registered package replay |
| `python3 -B scripts/check_research_commit.py --package research/coded-reverse-physical-word-p8 --check-source-history` | committed-byte and source-history check |

The subprocess verifiers are the PR4940 package and the companion physical-pair
package. The full native per-stage word, fixed-tape tariff, denominator 13/52,
compiler and BIT admission are not run.
