# Slow-reach screen (2026-10-19): result

This is a follow-up to `BREAKTHROUGH-MAP.md` §5, open question 1, prepared for DaysSky with assistance
from Claude.

- **Question:** is there a line system whose orthogonal sets stay large along short frame chains ("slow
  reach", so fewer relay helpers) while it keeps a decoder as cheap as the frontier's?
- **Why it matters:** that combination is what a wide-margin II19 middle would need.
- **Answer: no.** Across 21 systems, plus a search over E8 puncture sets, reach and decoder cost trade
  off monotonically. The frontier's own unit (P111) sits at the knee. The native Lorentzian systems have
  worse reach and heavier demand than E8.

## Metrics (`screen_reach.py`; definitions in its docstring)

- **x = cst/v, valid bounds.**
  - Upper bound: the exact min-cost star decoder of the B0 completion (cost-ordered basis, cost = span +
    radical), capped by the trivial decoder (x ≤ 1).
  - Lower bound: a pairwise non-orthogonal set, which is weak.
- **r2:** the fraction of perp(s) still orthogonal to the best nondegenerate 2-frame ⟨s, u⟩. This is
  E8's first reach step, 36/63.
- **relays:** a proxy. It counts the extra 2-frames through s, i.e. registers whose first frame is ⟨s⟩,
  needed to keep perp(s) in reach. Greedy, per line.
- **price:** the r434 shape transplanted to (v, h, cst, R = 3.91v), i.e. a frontier-quality middle.
  - "core" is the system as is; "lift" adds the −2 special line (h + 1, Lorentzian, cst + 1).
  - A model, not a word; "–" means no root.
- **window h:** the span dimension (sub-E8 cores use their own span).

## Results (`screen_reach_results.json`)

| system | v | h | x upper | r2 | relays | price core | price lift (II19) |
|---|---|---|---|---|---|---|---|
| E8 | 120 | 8 | 0.600 | 0.571 | 3.00 | −10.2% | −24.3% |
| **P111 (r434 lines)** | 111 | 8 | **0.568** | 0.604 | 2.86 | **+0.0%** | −15.9% |
| E8 minus 9 (greedy, `screen_puncture.py`) | 111 | 8 | 0.568 | **0.620** | – | (same x) | (same x) |
| D8 + 48 half-roots | 104 | 8 | 0.615 | 0.624 | 2.41 | −15.0% | −28.6% |
| D8 + 32 | 88 | 8 | 0.727 | 0.652 | 2.03 | −49.8% | −58.0% |
| D8 + 16 | 72 | 8 | 0.889 | 0.741 | 1.88 | – | – |
| D8 + 8 | 64 | 8 | 1.000 | 0.829 | 1.31 | – | – |
| D8 | 56 | 8 | 1.000 | 0.968 | 1.00 | – | – |
| D9 / D10 / D12 | 72 / 90 / 132 | 9 / 10 / 12 | 1.000 | 0.98–0.99 | 1.00 | – | – |
| E7 | 63 | 7 | 0.778 | 0.500 | 2.00 | −58.4% | −66.6% (h=8 Lorentzian) |
| E6, A7, A8, D7, D4+D4 | | | 0.78–1.00 | 0.40–0.95 | | – | – |
| E8+⟨−2⟩ levels 0,1 (native, h=9) | 2280 | 9 | ≤ 1 (lb 0.018) | **0.390** | **5.01** | ? | ? |
| E8+⟨−2⟩ level 1 (native, h=9) | 2160 | 9 | ≤ 1 (lb 0.020) | **0.375** | **7.02** | ? | ? |
| II_{1,9} levels 0–1 (native, h=10) | 601 | 10 | ≤ 1 (lb 0.040) | 0.555 | 3.00 | ? | ? |
| II_{1,9} with (a,1,−1) (native, h=10) | 2761 | 10 | ≤ 1 (lb 0.019) | 0.727* | 4.09 (ub) | ? | ? |

\* Hub artifact (`screen_shell2761.py`). Nearly every line's best partner is the special (0,1,1), which
is orthogonal to 2,280 of the 2,760 other lines. There are 0 lines with a ≥ 90% partner. Per-target
demand is 451–1,072 lines (E8: 63). The B0 completion has rank 2649/2761.

## Reading

1. **The trade-off is monotone.**
   - Along D8 → E8 (adding half-roots), reach falls 0.97 → 0.57 exactly as the decoder falls 1.0 → 0.60.
   - Puncturing E8 moves both together, ending at P111: x 0.568, r2 0.60–0.62. Past 9 punctures the
     in-format cst is frozen at 63, so x rises.
   - Every point with better reach than P111 has a worse decoder. The x needed for a II19 tie (≤ 0.51 at
     h = 9) is unreachable on this front.
2. **The mechanism is structural.**
   - With an F2-labelled decoder, orthogonal sets are label hyperplanes, and two of them meet in half.
     So r2 ≈ ½ is built in.
   - Reach above ½ needs label coincidences (D_n's twins e_a ± e_b). Twins add dimensions that every
     decoder piece must span, so x → 1.
3. **Native Lorentzian systems reach worse, not better.**
   - E8+⟨−2⟩ shells: r2 0.38–0.39 and 5–7 relays per line, against E8's 0.57 and 3.0.
   - The II_{1,9} systems: r2 ≈ E8's or a hub artifact, with ≥ 3 relays per line and much heavier demand.
   - Their decoders are undecided by valid bounds, but even a cheap decoder would meet a heavier middle.
4. **One small degree of freedom found.** An E8 puncture set with P111's decoder cost (63/111) and
   reach 0.620 instead of 0.604. It may make a slightly leaner middle possible for the E8 frontier
   itself, and through the lift for II19. Its effect on R is unmeasured.

## Open next questions

1. **Test the r2 = 0.620 puncture set in the r434 build pipeline.**
   - Relevance: the only lead from this screen. Small, and it applies to E8 first.
   - First step: rebuild the r434 middle on this live set and compare R.
   - Blocker: the r434 builder's dependence on its specific puncture geometry.
2. **Native Lorentzian decoders.**
   - A low-rank completion for the 601/2761 shells is unexcluded: valid lower bounds are only 0.02–0.04.
   - It would not by itself yield a lean middle (point 3).
3. **The wide-margin question now rests on lever A** (a better E8 middle) or on format extensions. Both
   are in `BREAKTHROUGH-MAP.md`.

## Reproduce

```sh
python3 screen_reach.py        # all systems, ~2 min; writes screen_reach_results.json
python3 screen_puncture.py 1   # greedy E8 puncture path (x, r2), ~5 min
python3 screen_shell2761.py    # class breakdown of the 2761-line shell, ~2 min
```
