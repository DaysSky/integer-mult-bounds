# Validation

| Command | Result |
|---|---|
| `python3 -B research/coded-reverse-word-p19/full_p19_diagonalization.py` | PASS: p=19 std outputs `[(1,4)...(19,2)]`; coded same with denominators `[1,13]`; diagonalized True |
| `python3 -I -B research/coded-reverse-word-p19/verify.py` | p=19 guards/root/ledger, P19_DIAG receipt, local S/L/R pair |
| `python3 -I -O -B research/coded-reverse-word-p19/verify.py` | same with explicit checks |
| `python3 -B scripts/research_package.py --package research/coded-reverse-word-p19` | registered replay |
| `python3 -B scripts/check_research_commit.py --package research/coded-reverse-word-p19 --check-source-history` | committed bytes and source history |

The fast verifier checks the saved P19_DIAG receipt; the long full run is
full_p19_diagonalization.py. The per-stage native adapter, field-map tariff,
denominator 13/52, compiler and BIT admission remain open.
